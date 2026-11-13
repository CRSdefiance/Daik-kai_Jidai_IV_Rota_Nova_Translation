from __future__ import annotations

# The repository root is intentionally added before importing the local package.
# ruff: noqa: I001

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.script.arm9_profiles import PROFILES
from dk4tool.script.mesfile import export_mesfile_rows
from scripts.inventory_lil_route import inventory as inventory_lil_route


TRACKED_FILES = (
    "/COMMON/MESFILE.DK4",
    "/COMMON/HELP.DK4",
    "/data/SC0.DK4",
    "/data/SC1.DK4",
    "/data/SC2.DK4",
    "/data/SC3.DK4",
)

LIL_ROUTE_DRAFT_FILES = (
    "lil_natural_v2_sc2_b22_blocked.json",
    "lil_natural_v2_sc2_b23_blocked.json",
    "hodram_natural_v2_sc2_b27_blocked.json",
    "hodram_natural_v2_sc2_b66_blocked.json",
    "hodram_natural_v2_sc2_b146_blocked.json",
)


def source_path(root: Path, internal_path: str) -> Path:
    return root.joinpath(*internal_path.strip("/").split("/"))


def load_translated_records(translations: Path) -> set[tuple[str, str]]:
    translated: set[tuple[str, str]] = set()
    for path in sorted(translations.glob("*.json")):
        batch = json.loads(path.read_text(encoding="utf-8"))
        if batch.get("format") != "dk4-ilnk-translation-batch-v1":
            continue
        if batch.get('content_type') == 'common-native-layout-v1':
            # Audit coordinates include untranslated Japanese and are not
            # translation declarations in the original source coordinate space.
            continue
        file_path = str(batch.get("file_path", ""))
        for record in batch.get("records", []):
            if str(record.get("english", "")).strip():
                translated.add((file_path, str(record.get("id", ""))))
    for path in sorted(translations.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                if str(row.get("english", "")).strip():
                    translated.add((str(row.get("file_path", "")), str(row.get("id", ""))))
    return translated


def build_report(source_root: Path, translations: Path) -> str:
    translated = load_translated_records(translations)
    stack = json.loads((translations / "release_stack.json").read_text(encoding="utf-8"))
    lil_profile = max(
        (name for name in stack["profiles"] if name.startswith("lil-deep-route-v")),
        key=lambda name: int(name.rsplit("v", 1)[1]),
    )
    lil_profile_inventory = inventory_lil_route(lil_profile)
    unified_profile = max(
        (name for name in stack["profiles"] if name.startswith("all-routes-unified-v")),
        key=lambda name: int(name.rsplit("v", 1)[1]),
    )
    reblocking_config = stack['profiles'][unified_profile].get('common_native_reblocking')
    if reblocking_config:
        # Registered transforms enforce complete native-owner coverage. Count
        # their reviewed manuscripts in clean source coordinates, never the
        # relocated audit layout, which also contains untranslated Japanese.
        config = json.loads(Path(reblocking_config).read_text(encoding='utf-8'))
        for declaration in config['manuscripts'] + config.get('pre_repack_manuscripts', []):
            raw = Path(declaration['path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != declaration['sha256']:
                raise ValueError('Registered native manuscript differs from its reviewed hash')
            manuscript = json.loads(raw)
            gates = ('source', 'context', 'localization', 'naturalness', 'formatting')
            if not all(row.get('review', {}).get(gate) is True
                       for row in manuscript['records'] for gate in gates):
                continue
            for row in manuscript['records']:
                translated.add(('/COMMON/MESFILE.DK4',
                                f"DK4_MES_B{row['block']:02d}_R{row['record']:04d}"))
    for repair_key in ('common_blizzard_release', 'common_placeholder_release'):
        repair_config = stack['profiles'][unified_profile].get(repair_key)
        if not repair_config:
            continue
        repair = json.loads(Path(repair_config).read_text(encoding='utf-8'))
        for name, expected_hash in repair['dependencies'].items():
            raw = Path(name).read_bytes()
            if hashlib.sha256(raw).hexdigest() != expected_hash:
                raise ValueError('Registered native repair manuscript/evidence changed')
            manuscript = json.loads(raw)
            if manuscript.get('format') != 'dk4-common-entry-manuscript-v1':
                continue
            gates = ('source', 'context', 'localization', 'naturalness', 'formatting')
            if not all(row.get('review', {}).get(gate) is True
                       for row in manuscript['records'] for gate in gates):
                raise ValueError('Registered native repair has unreviewed entries')
            for row in manuscript['records']:
                translated.add(('/COMMON/MESFILE.DK4',
                                f"DK4_MES_B{row['block']:02d}_R{row['record']:04d}"))
    accepted = json.loads(
        (translations / "accepted_baseline.json").read_text(encoding="utf-8")
    )
    accepted_rom = str(accepted["rom"])
    accepted_sha256 = str(accepted["sha256"])
    rows: list[tuple[str, int, int, float]] = []
    common_block_counts: Counter[int] = Counter()
    total_records = 0
    total_translated = 0

    for internal_path in TRACKED_FILES:
        path = source_path(source_root, internal_path)
        exported = export_mesfile_rows(path.read_bytes(), internal_path)
        if internal_path == "/COMMON/MESFILE.DK4":
            for row in exported:
                block = int(str(row["id"]).split("_B", 1)[1].split("_R", 1)[0])
                common_block_counts[block] += 1
        ids = {str(row["id"]) for row in exported}
        done = (
            int(lil_profile_inventory["translated_record_count"])
            if internal_path == "/data/SC2.DK4"
            else sum((internal_path, row_id) in translated for row_id in ids)
        )
        count = len(ids)
        percent = done * 100.0 / count if count else 0.0
        rows.append((internal_path, done, count, percent))
        total_records += count
        total_translated += done

    total_percent = total_translated * 100.0 / total_records if total_records else 0.0
    mapped_ui = len(PROFILES["all"])
    common_done, common_count, _ = next(
        (done, count, percent)
        for path, done, count, percent in rows
        if path == "/COMMON/MESFILE.DK4"
    )
    common_half = math.ceil(common_count / 2)
    common_half_gap = max(0, common_half - common_done)
    common_half_surplus = max(0, common_done - common_half)
    through_14 = sum(count for block, count in common_block_counts.items() if block <= 14)
    through_18 = sum(count for block, count in common_block_counts.items() if block <= 18)
    from_19 = max(0, common_half - through_18)
    lil_drafts: set[str] = set()
    lil_blocks: Counter[int] = Counter()
    for filename in LIL_ROUTE_DRAFT_FILES:
        path = translations / filename
        if not path.exists():
            continue
        batch = json.loads(path.read_text(encoding="utf-8"))
        for record in batch.get("blocked_records", []):
            if not str(record.get("draft_english", "")).strip():
                continue
            row_id = str(record["id"])
            lil_drafts.add(row_id)
            block = int(row_id.split("_B", 1)[1].split("_R", 1)[0])
            lil_blocks[block] += 1
    maria_done = next(
        done for path, done, _count, _percent in rows if path == "/data/SC3.DK4"
    )
    lil_done = next(
        done for path, done, _count, _percent in rows if path == "/data/SC2.DK4"
    )
    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    lines = [
        "# Translation progress",
        "",
        f"Generated: {generated}",
        "",
        (
            "This is a rough, record-based estimate. A translated record can be one short "
            "label or several dialogue lines, so the percentage is a navigation aid rather "
            "than a word-count claim."
        ),
        "",
        "| File | Translated records | Detected records | Approx. complete |",
        "|---|---:|---:|---:|",
    ]
    for internal_path, done, count, percent in rows:
        lines.append(f"| `{internal_path}` | {done} | {count} | {percent:.1f}% |")
    lines.extend(
        [
            f"| **Tracked text total** | **{total_translated}** | **{total_records}** | **{total_percent:.1f}%** |",
            "",
            "## Shared dialogue milestone",
            "",
            (
                f"`/COMMON/MESFILE.DK4` has passed the 50% milestone by "
                f"**{common_half_surplus} records** ({common_done} translated; "
                f"the threshold is {common_half} of {common_count})."
                if common_half_gap == 0
                else f"`/COMMON/MESFILE.DK4` needs **{common_half_gap} more records** "
                f"to reach 50% ({common_half} of {common_count})."
            ),
            "",
            (
                f"- Milestone reference—blocks B00-B14: {through_14} records "
                f"({through_14 * 100.0 / common_count:.1f}%)."
            ),
            (
                f"- Through B18: {through_18} cumulative records "
                f"({through_18 * 100.0 / common_count:.1f}%)."
            ),
            (
                f"- The first {from_19} records from B19 reached the exact "
                f"{common_half}-record halfway mark."
            ),
            (
                "- Each block still requires an internal-entry-point audit before insertion; "
                "record count alone cannot prevent missing first letters."
            ),
            "",
            "## Route translation progress",
            "",
            (
                "- **Raphael (`/data/SC0.DK4`):** the V93 route profile translates every "
                "remaining visible Japanese record. Residual unmatched records in the table "
                "include controls, nontext payloads, and records whose translated layers do "
                "not use the ordinary one-record/one-ID accounting model."
            ),
            (
                "- **Hodram (`/data/SC1.DK4`):** the V32 route profile covers the complete "
                "story and all Japanese-bearing records identified by the route audit, while "
                "preserving the one verified nontext event payload."
            ),
            (
                f"- **Lil (`/data/SC2.DK4`):** The experimental {lil_profile} profile "
                f"covers **{lil_done:,}/6,608** source records; "
                f"{lil_profile_inventory['remaining_record_count']:,} remain and "
                f"{lil_profile_inventory['excluded_record_count']} are explicitly excluded. "
                f"{stack['profiles'][lil_profile]['note']}"
            ),
            (
                f"- **Maria (`/data/SC3.DK4`):** V111 is integrated with "
                f"**{maria_done}** source-reviewed records, including the route opening, "
                "shared expeditions and ruins, tiger cave, dark forest, the water-level "
                "riddle and awakened-statue event, the Basra art-market boom, ceramic-earrings "
                "and pirate-sword events, the church figurehead challenge, the complete "
                "stolen-amethyst tavern sequence, Mikhail's complete recruitment and "
                "item-information tutorial, the complete Veracruz cheese-boom event, "
                "Yukihisa's cursed-Muramasa correspondence event, the complete Hamburg "
                "ceramics-boom event, the Malacca almond and Havana medicine rumors, the "
                "Seoul chili-pepper boom, the complete namahage dream encounter, and eight "
                "additional commodity-rumor events covering Amsterdam wheat, Lisbon spices, "
                "Athens rubies, Sofala tea, Alexandria sweets, Osaka glass, Calicut dyes, "
                "and Hangzhou sake; plus the Genoa tomato, Sao Jorge wine, London gem, "
                "and Stockholm fur rumors, Julian and Safia's Medusa-shield conversation, "
                "and the Calicut cargo-thief reward and treasure lead; plus Carlo's inn and "
                "rope events, Filippo's Papal States rumor, Charles's West African mystery "
                "letter, and Jam's Gupta spirit-beast letter; plus the caterpillar-fungus "
                "medicine-book event, Jam's shachihoko figurehead incident, the parrot "
                "encounter, Cristina's swan clue, the Zhao Yun spear rumor, and the "
                "Kublai Khan Sea King sword legend; plus the Saladin armor, Charles "
                "Martel, Phidias chisel, Demon-Piercing Arrow, Frozen Rose, and King "
                "Solomon treasury events; plus the blood-red sword, Spear of Ares, "
                "seaman's gloves, Frozen Rose theft setup, living figurehead, and Jean "
                "Ramgio capture events; plus Janus's sword letter, the Solomon demon "
                "weapon, Noritsune armor, Dukov's mail, the martial-arts robe, Armadillo "
                "Steel Hide, Giant Tortoise Shield, Phoenix Bascinet, and Herophilus "
                "medical-book events; plus the Istanbul tobacco event, Avalon and "
                "regional ruin leads, pirate bounties and rewards, and commodity-share "
                "notifications; plus the northern-monk rumor, ghost-ship investigation, "
                "greatest-warrior shrine, Guam rescue, New World proof handoff, and "
                "sextant exchange; plus the Goryeo Celadon Burner rumor and the complete "
                "San Jorge anti-bandit armor, musket, and cannon supply chain; plus the "
                "injured defector's opening to the Macao smuggling conspiracy and the "
                "tavern informant's arrival lead and Maria's exposure of the false "
                "Portuguese missionary delegation; plus the staged governor's-office "
                "arrest, smugglers' capture, and defector recruitment; plus the Kyoto "
                "lead and all companion-specific Proof-map reminder variants; plus the "
                "Kyoto-map maze, both navigation choices, and every companion branch; plus "
                "the dancer's inland-mosque treasure lead and the complete carronade-defense "
                "research quest, all specialist branches, completion, and guild reward; plus "
                "the complete London Lime Drops scurvy-cure loan, one-month return, rewards, "
                "and the follow-up ruin lead; plus the Malacca shark-fin commission, alternate "
                "delicacy resolution, both reward tiers, jungle-kingdom rumor, and ancient-coin discovery; "
                "plus the complete jungle-map traversal, ancient-kingdom vista, and Turkish guild "
                "Ceuta speed-run contract; plus the complete giant-snake and bog expedition, "
                "the Colosseum ruin lead, and the desert/quicksand expedition with every "
                "companion branch and choice; plus the remaining Jacob, Gabriel, William, "
                "and Hernan bounty material, northern-monk rumor, imperial-palace lead, and "
                "ancient-map lead, with sixteen verified nontext tail controls classified; "
                "plus the Proof debate, Muramasa scenes, Kurushima and Escante confrontations, "
                "rival-pirate battles, and Yuris, Jacob, and Gabriel encounters; plus the "
                "Hernan battle, all Lil rescue outcomes, Escante aftermath, and Manuel's "
                "complete sea elegy; plus Aziza's complete mutiny, rescue and ransom "
                "branches, family history, departure from piracy, and recruitment; plus "
                "Aziza's rematches and the Ulysse, Jacob, and Gabriel bounty captures; plus "
                "the ghost-ship aftermath, ironclad clash, both Lil-rescue choices, and "
                "Clifford's intervention; plus Kuen's false-flag assault, Hodram's rescue, "
                "the anomalous-ship sightings, wako debrief, strategy reflection, coastal "
                "contracts, and colonial warning; plus Bergstrom's warning, Kamil's "
                "Argot connection, and Maria's first direct confrontation with Lil in Batavia; "
                "plus the Lil-rescue aftermath and both Uddin Company alliance branches; "
                "plus Nagalpur's collapse and Maria's Madagascar-inspired trade-port plan; "
                "plus Tamsui's founding, government negotiations, construction funding, "
                "English workers, wine delivery, and trading-post completion; plus Maria's "
                "first African landfall, the Espinosa plantation confrontation, condemnation "
                "of enslavement, and declaration against the company; plus the English "
                "colonial challenge, Espinosa's capture by his victims, the African "
                "regional-treasure lead, and Maria's public acclaim; plus the meeting "
                "with Raphael and Crow, fair-trade and Mediterranean debates, Maldonado "
                "alliance branches, and Richard's betrayal; plus Richard's defeat, the "
                "Hangzhou return, every Proof assembled, and the philosophical route "
                "epilogue about belief, legitimacy, peace, and responsibility; plus the "
                "complete alternate ending, public Ming fleet review, companion comedy, "
                "and historical narration; plus Angelo's complete fever dream, Bianca "
                "farewell, recovery, and new-family resolution; plus the complete "
                "Seville bullfight spectacle and Emilio Ferrog recruitment; plus "
                "Cristina and Mivor's complete London recruitment event; plus the "
                "London harbor rescue and their romantic follow-up; plus Gerhard "
                "Adernkatz's complete recruitment; plus Janus's recruitment, ship "
                "reward, and vessel-naming tutorial; plus Charles Jean Rochefort's "
                "complete science-and-explosions recruitment; plus the complete "
                "Golden Crown of Silla encounter with Julian; plus the stranger "
                "trust choice, item gift, and stat outcomes; plus Emilio's "
                "tomato-tasting and seedling gift event; plus the banana-theft, "
                "monkey chase, and unfamiliar-seed event; plus Gerhard's "
                "lost-Katzbalger reminiscence; plus the complete rogue-ninja "
                "black-garb rumor event; plus Charles's amber science discussion "
                "and glowing-island rumor; plus Julio's Shield of Minerva lead, "
                "Samwell's Peacock Mail and Jaguar God vest leads, the Telescope "
                "of Aristarchus rumor, and Emilio's Hestia's Cauldron rumor; plus "
                "the Muramasa viewing, church and Santiago leads, cross prayer, "
                "both complete temple riddles and every answer branch, the complete "
                "megalith-cult confrontation and companion variants, the hidden-believer "
                "lamp handoff, guild timing outcomes, sacred-pot maze trap, and the "
                "palace sage's Proof motive test and northeastern map-clan clue; plus "
                "the sandbar drowning rescue, grandfather's gift, and New World jade "
                "ruin; plus the complete Sao Jorge raider confrontation, recruitment, "
                "and tablet handoff; plus the Hindustan ruin lead, every figurehead "
                "identification variant, dagger reward, and Julio's Christina lead; plus "
                "Maria's confidence crisis with Xien, both response branches, the Staff "
                "of Guidance lead, restored resolve, and Spirit reward; plus every "
                "companion-specific shark warning; plus the Ceuta deadline, Mao's "
                "innocent encounter, Maria's public-fear confession, Ming recognition "
                "offer, and discovery of the East Asian Proof map; plus Kuen's injured "
                "defector, the Argot deception, Maria's global maritime mission, and her "
                "companions' pledges; plus the frightened townsman, Guam castaway request, "
                "and the Southeast Asian Proof-map item combination and reveal; plus "
                "Maria's first Nagalpur encounter and money-versus-dignity rivalry, the "
                "female admirer gift, and the Indian Ocean Proof-map item combination; "
                "plus the complete reward-and-punishment anecdote about Maria's command, "
                "African Proof-map tablet assembly, guard passage, Patterned Cloth lead, "
                "and Mediterranean Proof-map lamp reveal; plus the Bergstrom "
                "confrontation, Clifford's legacy and Proof-map key, the North Sea "
                "and New World Proof-map reveals, Al's recruitment, Angelo Puccini's "
                "recruitment, and Angelo's acceptance of Bianca's death and his new family; "
                "plus Carlo Sinato's complete recruitment and Cristina's flamenco performance; "
                "plus Samwell's coin-trick recruitment, Dias's gambling recruitment, Julio "
                "Erneco's recruitment and rivalry with Xien, and Manuel's recruitment and "
                "complete ship-room tutorial; plus Cesare Tohni's rescue, recruitment, and "
                "ship-purchasing tutorial, Yifa's recruitment and Sanghyeon dream, the Golden "
                "Crown of Silla conversation and Seoul tomb lead, the Seville banana boom, "
                "and the optional India and Arab-culture companion conversations; plus "
                "Julian's recruitment, Yukihisa's independent sword-search command, and "
                "Aziza's tavern confrontation and sword-interest setup; plus the glassmaking "
                "book handoff, Minotaur's Axe request, Excalibur and Avalon lead, and Attila's "
                "stolen-armor rumor; plus the Rocco Alemkel portrait and navigator-book "
                "discovery; plus every remaining Plett Perrault, Peralonso Aguirre, and Yuris "
                "Huigen bounty variant, capture, reward, reminder, and follow-up clue. All "
                "4,953 text records are translated; the remaining 57 unique records are "
                "verified nontext event-control payloads."
            ),
            (
                "- Lil B22 has a complete 49-record source-locked runtime layer with the "
                "Lil/Kamil/Emilio/Fernando selectors and route name macros mapped; it is "
                "included in the unified route candidate."
            ),
            (
                "- B23 covers the immediate Deck-post tutorial and has a seven-record control "
                "probe; B27, B66, and B146 are retained under historical Hodram filenames after "
                "their route ownership was corrected."
            ),
            (
                f"- The {unified_profile} profile combines Raphael V93, Hodram V32, {lil_profile}, "
                "Maria V111, the Amsterdam opening, the newest shared interface and layout "
                "layers, and the global COMMON spacing repair."
            ),
            (
                f"- Combined ROM and patch: [package and verification](../releases/{unified_profile.replace('-', '_')}/README.md)."
                if (Path("releases") / unified_profile.replace("-", "_") / "README.md").exists()
                else ""
            ),
            "",
            "## Integrated interface progress",
            "",
            (
                "- **Extras and Online:** complete accepted English pass for both Extras "
                "choices, all feature and tie-in pages, the Online banner, and all 13 "
                "baked text cards."
            ),
            (
                "- **Options and Sound Setup:** the full `Options` label, prompts, all 38 "
                "BGM titles, and all 57 SFX titles are accepted."
            ),
            (
                "- **Town Common menu:** all six radial labels and the Info, Functions, "
                "Options, Save/Load, Deck, Assign Sailors, and empty-Items paths covered "
                "by V6 are accepted."
            ),
            (
                "- **Accepted Deck patch:** all compact room names, requirement and "
                "restriction strings, ability names, the Y-button `Crew` label, all 71 "
                "previously overlong activity responses, and the final inherited Deck "
                "placeholder are included in the accepted V10 baseline."
            ),
            (
                "- **Runtime text safety:** the unified candidate validates packed-entry "
                "boundaries, renderer guards, literal-percent safety, dynamic F-initial crew "
                "names, full-name separators, and COMMON automatic wrapping."
            ),
            (
                "- **Canonical accepted baseline:** "
                f"`{accepted_rom}`, SHA-256 `{accepted_sha256}`."
            ),
            "",
            "## Other tracked work",
            "",
            (
                f"- ARM9/UI dictionary: {mapped_ui} mapped slots have English replacements. "
                "This is not shown as a percentage because the full set of text-bearing ARM9 "
                "slots has not yet been exhaustively classified."
            ),
            (
                "- Redrawn graphics and fixed ARM9 labels are tracked by source-locked "
                "translation batches and the accepted-layer registry; they are not included "
                "in the table above."
            ),
            (
                "- An in-game save can retain old names and labels. Coverage is measured "
                "against the clean ROM and translation sources, not save-state contents."
            ),
            "",
            "## How to refresh",
            "",
            "Run `python scripts/build_translation_progress.py` after adding or revising translation batches.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a rough per-file translation coverage report")
    parser.add_argument("--source-root", type=Path, default=Path("work/extracted_clean"))
    parser.add_argument("--translations", type=Path, default=Path("translations"))
    parser.add_argument("--out", type=Path, default=Path("docs/translation_progress.md"))
    args = parser.parse_args()
    report = build_report(args.source_root, args.translations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
