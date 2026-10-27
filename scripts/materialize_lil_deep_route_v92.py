from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v92.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    10: ("A namahage calls for naughty children.", "Any naughty children here?"),
    14: ("The namahage repeats its call.", "Any naughty children here?"),
    18: ("The namahage asks whether the sailor has been naughty.", "Been naughty?"),
    22: ("Yukihisa demands to know who is there.", "Who?!"),
    26: ("The namahage asks the same question again.", "Been naughty?"),
    30: ("Yukihisa recognizes the namahage.", "...You're a namahage!"),
    34: ("The namahage asks again whether he has been naughty.", "Been naughty?"),
    38: ("Yukihisa says he has done nothing wrong.", "Done nothing wrong."),
    42: ("The namahage accepts that answer.", "Oh..."),
    53: ("Yukihisa realizes it was a dream.", "Dream?"),
    65: ("Angelo reacts in shock to what has appeared.", "Whoa! What is this?!"),
    72: ("Yukihisa notices something unexpected.", "Huh?!"),
    80: ("Yukihisa reflects that strange things happen.", "Strange things do happen."),
    84: ("Yukihisa plans to give the object to the admiral tomorrow morning.",
         "This goes to the admiral at dawn."),
    95: ("Angelo demands an explanation for what just happened.", "...What was that?!"),
}
SPEAKERS = {0xFE: "Namahage", 0x0C: "Yukihisa Genjo Shiraki", 0x0F: "Angelo Puccini"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B198_")}
    authored = {f"DK4_MES_B198_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B198 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B198_R{number:04d}"
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
            "context": "Yukihisa dreams of a namahage, then finds an object for the admiral.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B198 Japanese and parallel route context. "
                "Preserve FE/0C/0F states; literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v91-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 15 B198 namahage dream and mysterious-object records.",
        "inventory": {"identified_records": 15, "translated_records": 15, "blocks": {"198": 15}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
