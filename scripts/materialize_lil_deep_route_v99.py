from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v99.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A bird flaps nearby.", "flap, flap!"),
    9: ("Angelo recoils from the unfamiliar bird.", "Whoa! What's that?!"),
    13: ("The parrot mimics Angelo's question.", "WHAT'S THAT"),
    17: ("Angelo exclaims that the bird spoke human words.",
         "Mamma mia! You can talk?!"),
    20: ("The parrot mimics Angelo's astonishment.", "YOU CAN TALK"),
    24: ("Lil identifies the bird as a parrot.", "A parrot!"),
    28: ("Angelo realizes it is a parrot.", "A parrot, eh?"),
    32: ("The parrot mimics Angelo's realization.", "A PARROT, EH"),
    36: ("Angelo tells the parrot to stop copying him.", "Stop that!"),
    40: ("The parrot copies that command.", "STOP THAT"),
    44: ("Angelo finds the parrot amusing and decides to catch it.",
         "Oh, fun! Gonna catch you!"),
    47: ("Angelo lunges for the parrot.", "Here goes! Hah!"),
    51: ("The bird flaps amid repeated impacts and rustling.",
         "flap! Thud! Crash! Bang! Rustle!"),
    55: ("Lil says they have finally caught the parrot.", "Got you!"),
    59: ("Angelo breathes out, taunts the parrot, and laughs.",
         "Whew! Surrender now? Hahaha!"),
    63: ("The parrot repeats Angelo's challenge.", "SURRENDER NOW?"),
    67: ("Lil laughs that the captured parrot still sounds defiant.",
         "Ha! He's caught, but still talks like he won!"),
}
EXCLUDED = {
    "DK4_MES_B205_R0007": (
        "Four-byte 41 48 93 A8 packed parrot-scene payload, identical to the "
        "verified nontext payload in Maria SC3 B178; leave unchanged."
    ),
}
SPEAKERS = {0x0F: "Angelo Puccini", 0x02: "Lil", 0xFE: "Parrot or scene effect"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B205_")}
    authored = {f"DK4_MES_B205_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B205 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B205_R0007"]["source_hex"].upper() != "414893A8":
        raise ValueError("B205 packed parrot payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B205_R{number:04d}"
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
            "context": "Angelo and Lil chase and catch a parrot that mimics Angelo's words.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B205 Japanese and parallel event context. "
                "Preserve 0F/02/FE states and the parrot's repeated words; "
                "the packed event payload stays unchanged. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v98-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "17 B205 parrot encounter text records; one packed event excluded unchanged.",
        "inventory": {"identified_records": 18, "translated_records": 17, "blocks": {"205": 17}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
