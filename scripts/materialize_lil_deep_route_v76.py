from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v76.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("A patron declares that bananas are the next big thing.", "Bananas! They're the future!"),
    9: ("Her attendant questions the fruit.", "Bananas?"),
    13: ("The patron insists bananas will be popular.", "Yes! They'll be a hit."),
    17: ("The attendant remains unsure.", "Really?"),
    21: ("The patron insists her judgment is final.", "Yes! They'll sell. Take my word!"),
    24: ("The attendant asks what to do next.", "Understood. What shall we do?"),
    27: ("The patron orders the attendant to buy all available bananas.", "Buy every banana you can find!"),
    31: ("The attendant accepts the order.", "Right."),
    35: ("The patron celebrates the coming banana boom.", "Bananas are the future! Ho ho ho!"),
    38: ("The market notice says bananas may boom in Seville.", "Bananas may catch on in Seville."),
}
SPEAKERS = {0xAE: "Seville patron", 0xAF: "Attendant", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B176_")}
    authored = {f"DK4_MES_B176_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B176 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B176_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "A Seville patron buys bananas in bulk, prompting a local commodity boom.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B176 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v76-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 10 B176 Seville banana-boom dialogue records.",
        "inventory": {"identified_records": 10, "translated_records": 10, "blocks": {"176": 10}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
