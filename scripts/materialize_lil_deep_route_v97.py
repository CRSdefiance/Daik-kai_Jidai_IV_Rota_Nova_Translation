from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v97.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Mikhail reacts to an unfamiliar object.", "What's this?!"),
    9: ("Lil asks what Mikhail has found.", "What is it?"),
    13: ("Mikhail points out the object.", "This thing here."),
    17: ("Lil wonders if it is an insect.", "A bug...?"),
    21: ("Mikhail notices a strange plant growing on it.",
         "But a strange plant grows on it."),
    24: ("Lil confirms Mikhail's observation.", "Oh, yes."),
    28: ("An herbalist identifies it as caterpillar fungus.",
         "That is caterpillar fungus."),
    35: ("The herbalist says people in China value it as medicine.",
         "China prizes it as medicine."),
    38: ("Lil is surprised that it is medicinal.", "Medicine?"),
    42: ("Mikhail considers its medicinal value.", "Hm. Medicine..."),
    46: ("The herbalist offers them a book.", "Yes. Take this."),
    50: ("Lil asks what the book is.", "What's this?"),
    54: ("The herbalist says it describes medicinal ingredients.",
         "A book about medicinal ingredients."),
    57: ("Lil hesitates to accept such a valuable book.",
         "Can we take such a costly book?"),
    60: ("The herbalist says he no longer needs it and gives it to Lil.",
         "No need for it now. Take it."),
    63: ("Lil still hesitates.", "But..."),
    67: ("The herbalist sees that Mikhail wants the book.",
         "Ho ho! Your friend wants it, though."),
    70: ("Mikhail admits he would like to read the book.",
         "Well... That book did catch my eye."),
    74: ("Lil offers to buy the book for 1,000 coins.",
         "Then sell it to us for 1,000 coins."),
    77: ("The herbalist asks for only 100 coins.",
         "Ho ho! Just 100 coins, then."),
    80: ("The system raises the named admiral's charm by one.",
         "{MACRO:FI}: Charm +1!"),
}
SPEAKERS = {0x4C: "Mikhail Lett", 0x02: "Lil", 0xAA: "Herbalist", 0xFE: "System notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B203_")}
    authored = {f"DK4_MES_B203_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B203 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B203_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        prose = english.replace("{MACRO:FI}", "")
        if "I" in prose or "F" in prose:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        if raw.count(b"FI") != english.count("{MACRO:FI}"):
            raise ValueError(f"{row_id}: name macro count changed")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Mikhail and Lil learn about caterpillar fungus and buy a medicine book.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B203 Japanese and parallel event context. "
                "Preserve 4C/02/AA/FE states and the FI reward macro. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v96-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 21 B203 caterpillar-fungus, medicine-book and reward records.",
        "inventory": {"identified_records": 21, "translated_records": 21, "blocks": {"203": 21}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
