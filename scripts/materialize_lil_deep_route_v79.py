from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v79.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    9: ("A drinker challenges someone who questioned him.", "So what?"),
    16: ("The drinker asks whether wine tastes good.", "Wine? Any good?"),
    24: ("The drinker asks whether wine really tastes so good.", "That good, huh?"),
    31: ("The drinker orders a glass of wine to try.", "Barkeep! Bring me a glass of wine!"),
    35: ("The barkeep accepts the order.", "Sure."),
    39: ("The drinker gulps the wine.", "Gulp, gulp, gulp."),
    47: ("The drinker loves the wine and orders another glass.", "Delicious! Barkeep, another!"),
    54: ("The market notice says wine may boom in San Jorge.", "Wine may catch on in San Jorge."),
}
SPEAKERS = {0x60: "San Jorge drinker", 0x5C: "Barkeep", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B179_")}
    authored = {f"DK4_MES_B179_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B179 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B179_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "A San Jorge drinker tries wine, likes it, and prompts a local commodity boom.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B179 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v79-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 8 B179 San Jorge wine-boom text records.",
        "inventory": {"identified_records": 8, "translated_records": 8, "blocks": {"179": 8}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
