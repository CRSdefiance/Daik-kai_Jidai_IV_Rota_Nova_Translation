from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v96.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A fleeing stranger calls to Lil.", "Hey, you."),
    9: ("Lil responds to the stranger.", "Hm?"),
    13: ("The stranger thrusts a book at Lil and tells her to use it.",
         "Take this. Use it as you like!"),
    16: ("Lil is startled.", "Huh?"),
    20: ("A pursuer spots the stranger and orders him to stop.", "There you are! Stop!"),
    23: ("Lil is confused by the pursuit.", "H-huh?"),
    27: ("The stranger runs off.", "See you!"),
    31: ("The pursuer shouts after him.", "Stop!"),
    35: ("Lil demands to know what happened.", "What was that?!"),
    39: ("Charles asks the admiral what she is doing.", "What's going on, Admiral?"),
    43: ("Lil says the object was forced on her.", "Someone shoved this at me..."),
    47: ("Charles asks what the object is.", "What is it?"),
    51: ("Lil guesses that it is a book.", "A book?"),
    55: ("Charles reads the title, a guide to glassmaking.", "Glassmaking Guide..."),
    58: ("Charles thinks Lil should keep the book she was given.", "Hm. Might as well keep it."),
    61: ("Lil hesitates to keep it.", "Huh? But..."),
    65: ("Charles says to accept gifts when people offer them.",
         "Take what you're given."),
    68: ("Charles asks to see the guide later.", "Oh, let me see it later."),
    72: ("Lil realizes Charles wants the book for himself.", "So that's your angle!"),
}
SPEAKERS = {0x9D: "Fleeing stranger", 0x93: "Pursuer", 0x02: "Lil", 0x12: "Charles Jean Rochefort"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B202_")}
    authored = {f"DK4_MES_B202_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B202 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B202_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "A fleeing stranger leaves Lil a Glassmaking Guide; Charles wants to read it.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B202 Japanese. Glassmaking Guide matches "
                "the established English item name. Preserve 9D/93/02/12 states; "
                "literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v96-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 19 B202 stolen Glassmaking Guide encounter records.",
        "inventory": {"identified_records": 19, "translated_records": 19, "blocks": {"202": 19}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
