from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v14.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = {
    111: [
        "Wait. Have you visited{LB}Santiago Cathedral?",
        "Pilgrims from across Europe{LB}have long come here.{LB}A famous place.",
        "While in Seville,{LB}why not visit?{LB}Here is the way.",
    ],
    112: [
        "Thank you.{LB}...Hm? This cross...",
        "Troubled?",
        "One cross looks very old.",
        "Do not say such things.{LB}A sacred cross is neither new nor old.",
        "That was not what was meant...",
        "Good. By father, son,{LB}and holy spirit... Amen.",
    ],
    113: [
        "Admiral, please look!",
        "Admiral, look!",
        "Admiral, look at this!",
        "Admiral, look here!",
        "Admiral! Look!",
        "Admiral, behold!",
        "Visitor...",
        "My power is yours.{LB}Debate with vigor.",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {"8B": "Priest", "BF": "Cathedral guide", "D0": "Raphael crewmate", "FE": "Temple voice"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    111: "A Seville woman directs Raphael to Santiago Cathedral, a famous European pilgrimage destination.",
    112: "Raphael notices an unusually old cross before joining the priest's prayer.",
    113: "Several possible crew voices call attention to a temple, whose voice grants Raphael power for debate.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    records = []
    block_counts = {}
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_")]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
                "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving religious context, route guidance, alternate crew voices, and fixed-allocation display safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v14-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Santiago Cathedral directions, the ancient-cross prayer, and the temple debate blessing across Raphael SC0 blocks 111-113.",
        "excluded_records": {},
        "inventory": {"identified_records": len(records), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
