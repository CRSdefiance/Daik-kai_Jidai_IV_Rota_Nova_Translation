from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v47.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Hey, why are these in two pieces?", "Hey, why are these split up?"),
    9: ("Oh, you mean the Mysterious Upper and Lower Tablets?", "Oh, you mean the Upper and Lower Stone Tablets?"),
    12: ("They are separate, but seem to be two parts of one tablet.", "They look like two halves of one tablet..."),
    15: ("Look, they fit together like this!", "Look! They fit together!"),
    18: ("Oh, they fit perfectly!", "A perfect fit!"),
    22: ("This forms a map. Could it be the map to Africa's Ruler's Proof?", "A map! Could this lead to Africa's Ruler's Proof?"),
    25: ("Cheese? Where is it? I want some!", "Cheese?! Where? Gimme some!"),
    29: ("Emilio, not cheese, a map. Now let us search for the Ruler's Proof!", "Emilio, a map, not cheese! Come on, let's find the Ruler's Proof!"),
}
SPEAKERS = {0x02: "Lil Argot", 0x0E: "Emilio Ferrog"}
EXCLUDED = {"DK4_MES_B136_R0020": "Four-byte 23 48 9D A8 event payload between tablet assembly and map reveal; not dialogue."}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B136_")}
    authored = {f"DK4_MES_B136_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError("B136 coverage does not match clean source")
    if source_rows["DK4_MES_B136_R0020"]["source_hex"].upper() != "23489DA8":
        raise ValueError("B136 event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B136_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Lil and Emilio combine the Upper and Lower Stone Tablets, exposing Africa's Ruler's Proof map. Emilio mistakes 'map' for 'cheese'.",
            "source_meaning": source_meaning,
            "localization_note": "Clean Japanese reviewed in scene order. Preserves the two tablet item names, Ruler's Proof and Emilio's cheese joke. The intervening event payload stays unchanged. Guarded wrapping protects initial and continuation glyphs.",
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v46-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Eight B136 tablet-map dialogue records; opaque R0020 event payload excluded unchanged.",
        "inventory": {"identified_records": 9, "translated_records": len(records), "blocks": {"136": 8}},
        "excluded_records": EXCLUDED,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
