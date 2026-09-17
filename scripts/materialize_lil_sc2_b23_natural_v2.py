from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/extracted_clean/data/SC2.DK4"
OUTPUT = ROOT / "translations/lil_natural_v2_sc2_b23_blocked.json"
FILE_PATH = "/data/SC2.DK4"
SOURCE_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"


DRAFTS = {
    "DK4_MES_B23_R0005": "Next up...",
    "DK4_MES_B23_R0009": "What? Aren't we finished already?",
    "DK4_MES_B23_R0013": "That was about handling the ship. Next, I'll explain how to assign the crew.",
    "DK4_MES_B23_R0018": "That's news to me...",
    "DK4_MES_B23_R0020": "I can figure it out without being told.",
    "DK4_MES_B23_R0030": "Oh? Then I can leave it all to you, right?",
    "DK4_MES_B23_R0040": "Ugh... What a pain.",
    "DK4_MES_B23_R0044": "Being an admiral is hard work. Or would you rather make me the admiral?",
    "DK4_MES_B23_R0047": "No way.",
    "DK4_MES_B23_R0051": "Then you'd better study properly.",
    "DK4_MES_B23_R0054": "Fiiine...",
    "DK4_MES_B23_R0058": "I'll explain how to assign officers and what each post does. Give every navigator a duty so your voyages run smoothly.",
    "DK4_MES_B23_R0062": "First, the captain is {MACRO:FI}, of course. A ship won't run smoothly without its captain. Except in an emergency, stay in the captain's cabin.",
    "DK4_MES_B23_R0065": "Next is the sail master, who adjusts the sails to the wind. It's an important job, and every mast needs someone assigned to it.",
    "DK4_MES_B23_R0069": "When the sails are set to Half, the sail master adjusts them automatically.",
    "DK4_MES_B23_R0072": "Oh! So if I use Half, I don't have to give any orders? You should've said so sooner!",
    "DK4_MES_B23_R0076": "Sometimes you'll need to sail at Full. Practice now so you don't panic when that happens.",
    "DK4_MES_B23_R0079": "Hmm...",
    "DK4_MES_B23_R0091": "Use the L and R Buttons to set the sails' direction. Properly trimmed sails increase the ship's speed.",
    "DK4_MES_B23_R0095": "With the stylus, the sails turn to the best angle automatically. Tap the flagship when you want to stop.",
    "DK4_MES_B23_R0104": "The helmsman turns the ship. That's important too. Assign someone skilled if you want the ship to turn quickly.",
    "DK4_MES_B23_R0107": "A good helmsman can also move the ship quickly into an advantageous position during battle.",
    "DK4_MES_B23_R0110": "A surveyor enables Auto Move and shows the fleet's latitude and longitude. That's another important post.",
    "DK4_MES_B23_R0120": "Oh, right! Let me be the lookout!",
    "DK4_MES_B23_R0123": "Good idea. With your powers of observation, Fernando, you're perfect for lookout duty.",
    "DK4_MES_B23_R0127": "Lookout? What's that?",
    "DK4_MES_B23_R0131": "Oh, come on! You're going to sea without even knowing what a lookout does?",
    "DK4_MES_B23_R0135": "Oh, be quiet! I only forgot for a moment!",
    "DK4_MES_B23_R0138": "Easy, both of you...",
    "DK4_MES_B23_R0142": "At sea, the lookout checks other ships' affiliations and the condition of nearby cities, then reports what they see.",
    "DK4_MES_B23_R0146": "The better their Observation, the farther away they can discover cities and rare items!",
    "DK4_MES_B23_R0153": "In the end, though, {MACRO:FI} decides everyone's assignments.",
    "DK4_MES_B23_R0157": "That's enough for an ordinary voyage. Hmm... Did I explain too much at once?",
    "DK4_MES_B23_R0161": "I'll just try it and see.",
    "DK4_MES_B23_R0166": "Press the X Button and choose Deck from the menu. On the Deck screen, you can change each navigator's assignment.",
}


SPEAKERS = {
    "02": "Lil Argot",
    "09": "Kamil",
    "14": "Fernando",
    "FE": "System tutorial",
}


def main() -> None:
    source = SOURCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise SystemExit("clean SC2 hash mismatch")

    records = {row.row_id: row for row in iter_mesfile_records(source)}
    if set(DRAFTS) - set(records):
        raise SystemExit(f"missing SC2 rows: {sorted(set(DRAFTS) - set(records))}")

    segments = IlnkContainer.parse(source).blocks[23].split(b"\0")
    blocked = []
    for row_id, draft in DRAFTS.items():
        source_row = records[row_id]
        index = int(row_id.rsplit("R", 1)[1])
        raw = source_row.raw_bytes
        lead = f"{raw[0]:02X}"
        has_state = raw[0] in {0x02, 0x09, 0x14, 0xFE}
        prior = []
        cursor = index - 1
        while cursor >= 0 and len(prior) < 3:
            if segments[cursor]:
                prior.append({"id": f"DK4_MES_B23_R{cursor:04d}", "hex": segments[cursor].hex().upper()})
            cursor -= 1
        prior.reverse()
        if has_state:
            speaker = SPEAKERS[lead]
            blocker = (
                f"SC2 B23 selector 0x{lead} is statically mapped to {speaker}; its exact "
                "portrait/nameplate presentation and this draft's final wrapping still need "
                "cold-boot confirmation."
            )
        else:
            speaker = "Choice menu"
            blocker = (
                "This source record is statically mapped as a bare choice label in the B23 "
                "two-option command sequence; its final menu placement still needs cold-boot "
                "confirmation."
            )
        if "{MACRO:FI}" in draft:
            blocker += (
                " FI is statically mapped to the default-route first name (Lil, three ASCII "
                "bytes); runtime expansion and line layout remain to be confirmed."
            )
        blocked.append(
            {
                "id": row_id,
                "draft_english": f"{draft}{{PAD}}",
                "speaker": speaker,
                "context": "Lil's opening voyage: Kamil teaches her how to assign navigators to Deck posts.",
                "source_meaning": draft.replace("{MACRO:FI}", "Lil"),
                "localization_note": "Natural American English; terminology follows the accepted Deck and sailing interface.",
                "source_hex_guard": raw.hex().upper(),
                "source_prefix_hex": lead if has_state else None,
                "preceding_nonempty_records": prior,
                "blocker": blocker,
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": False,
                },
            }
        )

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": FILE_PATH,
        "source_file_sha256": SOURCE_SHA256,
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "draft_status": "source-first-editorial-draft-blocked-runtime-unconfirmed-sc2-b23",
        "profile_note": (
            "Non-buildable draft. Lil SC2 block 23 is fully translated and its speaker selectors, "
            "choice records, command grammar, and default FI value are statically mapped. "
            "Portrait/nameplate effects, choice placement, FI expansion, and final layout require "
            "cold-boot confirmation."
        ),
        "control_map": {
            "speaker_selectors": {
                "02": "Lil Argot",
                "09": "Kamil",
                "14": "Fernando",
                "FE": "system tutorial panel",
            },
            "choice_labels": ["DK4_MES_B23_R0018", "DK4_MES_B23_R0020"],
            "choice_command_records": [
                "DK4_MES_B23_R0015",
                "DK4_MES_B23_R0017",
                "DK4_MES_B23_R0023",
                "DK4_MES_B23_R0025",
                "DK4_MES_B23_R0027",
            ],
            "default_route_macros": {"FI": "Lil", "FA": "Argot", "FO": "Argot Co."},
            "evidence": "docs/lil_sc2_b23_control_map.md",
        },
        "inventory": {
            "identified_records": len(blocked),
            "translated_drafts": len(blocked),
            "encodable_records": 0,
            "blocked_records": len(blocked),
            "missing_records": 0,
            "blocks": {"23": len(blocked)},
        },
        "records": [],
        "blocked_records": blocked,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(blocked)} blocked drafts")


if __name__ == "__main__":
    main()
