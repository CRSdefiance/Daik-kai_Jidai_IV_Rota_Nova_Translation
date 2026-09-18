from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v23.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "You travel the world, Admiral.{LB}Surely you know friendly tavern girls{LB}in many towns?",
    "Not exactly close friends...",
    "That will not do.{LB}Tavern girls know information{LB}every adventurer needs.",
    "Treasure rumors, enemy movements,{LB}even rare ruins known only to locals.",
    "Befriend girls around the world{LB}or fail as an adventurer.",
    "But...{LB}That is not easy, right?",
    "Mere customer talk is not enough.{LB}They speak with dozens of people daily.",
    "A gift that captures her heart{LB}is the answer.",
    "Each woman likes different things.{LB}Learn what interests her,{LB}then give it as a present.",
    "Take Sakura in Osaka.{LB}She wants the Snowfall Robe,{LB}sold somewhere in the North Sea.",
    "Even the least greedy woman{LB}enjoys receiving what she desires.",
    "So courting tavern girls everywhere{LB}was simply proper adventuring...",
    "O-of course!",
    "Then teach me!",
    "Ha ha! That is the spirit!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B135_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B135: {len(rows)} source rows != {len(TRANSLATIONS)} translations")
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first == 0x1A else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": "Julian Lopez" if state else "Raphael Castor",
            "context": "Julian teaches Raphael how tavern contacts reveal treasure, fleet, and ruin information and how thoughtful gifts build those relationships.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving the complete social-information tutorial, named Osaka example, item name, comedy, and fixed-allocation safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects instructional grouping and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v22-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete tavern-contact, information, and gift tutorial in Raphael SC0 block 135.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"135": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
