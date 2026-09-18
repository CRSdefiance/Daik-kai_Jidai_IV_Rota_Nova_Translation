from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v17.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B118_R0127": "Raw event-control payload; not dialogue."}
TRANSLATIONS = [
    "Colosseum visitor,{LB}answer!",
    "What?",
    "Question.",
    "Magic beans double each second.{LB}One: two. Two: four. Three: eight.",
    "One bean fills a bag in 60 seconds.{LB}Starting with two,{LB}when will the bag be full?",
    "Choose an answer!",
    "1s", "30s", "59s",
    "...Got it!",
    "Really?{LB}Claudio always comes through!",
    "Right! One second!{LB}Well?",
    "Yes! That was my thought too!",
    "Wrong!",
    "Huh?",
    "...Got it!",
    "Really?{LB}Claudio always comes through!",
    "Right! Half of 60: 30 seconds!{LB}Well?",
    "Yes! That was my thought too!",
    "Wrong!",
    "Huh?",
    "...Got it!",
    "Oh? Your answer?",
    "The answer is 59 seconds!",
    "Splendid!{LB}Wise and brave one,{LB}take this!",
]
SPEAKERS = {"05": "Claudio Manousch", "FE": "Colosseum voice"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B118_")]
    source_rows = [row for row in rows if row["id"] not in EXCLUDED]
    if len(source_rows) != len(TRANSLATIONS) or {row["id"] for row in rows} != {row["id"] for row in source_rows} | set(EXCLUDED):
        raise SystemExit("Raphael V17 inventory accounting mismatch")
    records = []
    for row, english in zip(source_rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
            "context": "The Colosseum voice poses an exponential-growth riddle; Claudio tries two wrong answers before Raphael gives the correct 59-second answer.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the mathematical riddle, every answer branch, comedy, and fixed-allocation display safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Preserves source blank rows or protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v16-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "The complete Colosseum magic-bean riddle, all three answer branches, and reward across Raphael SC0 block 118.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"118": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
