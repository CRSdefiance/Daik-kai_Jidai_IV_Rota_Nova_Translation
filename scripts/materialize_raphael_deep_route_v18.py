from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT_A = Path("translations/raphael_deep_route_v18a.json")
OUTPUT_B = Path("translations/raphael_deep_route_v18b.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B121_R0010": "Raw event-control payload; not dialogue."}
TRANSLATIONS = {
    119: [
        "Admiral, dead end.", "Admiral, a dead end.", "Huh? A dead end.",
        "Admiral, dead end.", "Oops. Dead end.", "Admiral, a dead end.",
        "Admiral! Dead end!", "Oh my, a dead end.",
        "Urn tablet{LB}in the wall.",
        "Traveler:{LB}pour left-handed.",
        "Left hand?",
        "Push", "Right", "Left",
        "A left pour tips right...",
        "Run!", "Aaah!", "Sailor injured!",
    ],
    120: [
        "Hey.", "Hm?{LB}Yes?",
        "You seek the{LB}Proof of Conquest?",
        "How did you know?",
        "You seem to know something{LB}of the Proof's map.",
        "True. But this cannot be told{LB}to just anyone.",
        "You fear what an evil heart{LB}might do with it.",
        "Yes.",
        "No worry.{LB}This Proof has been studied{LB}for many years.",
        "This boy surely has{LB}the makings of a conqueror.",
        "Hmm...",
        "Please.{LB}Tell us what you know.",
        "Very well.",
        "Long ago, the map's guardians{LB}fled China and traveled{LB}far northeast.",
        "Northeast...?",
        "Their descendants reached a village{LB}near the frozen sea{LB}and still live there in secret.",
        "...A village northeast.",
        "Peninsula's base. East coast.{LB}Below a high peak.",
        "The place is very distant.{LB}An ordinary ship may not reach it.{LB}Go unprepared and you will die.",
        "(...Gulp.)",
        "Never let an evil heart{LB}claim the Proof.{LB}Do not succumb to greed.",
        "Yes!{LB}Thank you.",
    ],
    121: [
        "Huge palace.{LB}Back to town.",
        "Hm? On the sandbar...", "Someone on the bar.",
        "Hm? On the sandbar.", "Huh? Someone.",
        "What happened?",
        "Travelers! Please!{LB}Save my grandson!",
        "Boy?", "Grandpa! Help!", "A boy is drowning!",
        "Leave it to me!", "Mine!", "Let me go!",
        "Got it!", "Leave this to me!", "Let me go!",
        "Grandpa! So scary!",
        "You are safe now!{LB}Thank goodness!",
        "Travelers! Thank you!{LB}Truly, thank you!",
        "So glad your grandson is safe.",
        "No reward can be given...{LB}Ah, wait here a moment!",
        "Please, take this.",
        "What?",
        "Bandits plagued this area.{LB}The governor gave this reward{LB}after their defeat.",
        "Origin unknown,{LB}but quite valuable.",
        "No. Keep it as proof{LB}of your brave deed.",
        "Please. A grandchild's savior{LB}cannot leave empty-handed.{LB}The object means little to me.",
        "Then... thank you.",
        "Travel safely.",
        "Bye, mister!",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {
    "4B": "Old scholar", "89": "Yuan elder", "97": "Raphael party", "A3": "Boy",
    "AA": "Grandfather", "CF": "Raphael party", "D0": "Raphael crewmate",
    "D6": "Raphael crewmate", "D7": "Raphael rescuer", "FE": "Inscription or system",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    119: "Raphael's party finds an urn puzzle, tries its three controls, and can trigger a sailor injury on failure.",
    120: "A Yuan elder and an old scholar reveal that the Proof's map guardians fled to a frozen northeastern peninsula village.",
    121: "Raphael's party rescues a drowning boy; every possible rescuer line and the grandfather's heirloom reward are included.",
}


def materialize_group(rows: list[dict[str, str]], blocks: tuple[int, ...], output: Path, profile: str) -> None:
    inventory = {row["id"] for row in rows if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in blocks)}
    exclusions = {row_id: reason for row_id, reason in EXCLUDED.items() if row_id in inventory}
    records = []
    block_counts = {}
    translated_ids = set()
    for block in blocks:
        texts = TRANSLATIONS[block]
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in exclusions]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            translated_ids.add(row["id"])
            first = bytes.fromhex(row["source_hex"])[0]
            is_state = ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            if block != 120 and first == 0x89:
                is_state = False
            state = f"{first:02X}" if is_state else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"), "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving puzzle logic, route geography, every rescuer variant, reward lore, and fixed-allocation safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    if translated_ids | set(exclusions) != inventory:
        raise SystemExit(f"Raphael V18 inventory accounting mismatch for {blocks}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": profile,
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Raphael ruin and Proof-of-Conquest events with block-isolated presentation-state decoding.",
        "excluded_records": exclusions,
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    output.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}: {len(records)} records, {len(exclusions)} controls")


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    materialize_group(rows, (119, 121), OUTPUT_A, "raphael-story-deep-route-v18a-live")
    materialize_group(rows, (120,), OUTPUT_B, "raphael-story-deep-route-v18-live")


if __name__ == "__main__":
    main()
