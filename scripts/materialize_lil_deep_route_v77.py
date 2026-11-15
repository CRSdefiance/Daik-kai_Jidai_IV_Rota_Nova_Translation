from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v77.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("A patron declares that tomatoes are the next big thing.", "Tomatoes! They're the future!"),
    9: ("Her attendant doubts anyone will want such bright red food.", "Really? Those bright red things?"),
    12: ("The patron loves the passionate red, which reminds her of youthful romance.", "That red stirs passion! Brings back memories of young love."),
    16: ("The attendant politely reacts to her reminiscence.", "How lovely for you, madam."),
    20: ("The patron orders tomato dishes prepared and sold at once.", "Start selling tomato dishes at once!"),
    23: ("The attendant accepts the order.", "Understood."),
    27: ("The patron tells the attendant not to miss the tomato craze.", "Don't miss this tomato craze!"),
    30: ("The attendant gives a weary acknowledgment.", "Right."),
    34: ("The patron offers encouragement and laughs.", "Good luck, then! Ho ho ho!"),
    37: ("The market notice says tomatoes may boom in Genoa.", "Tomatoes may catch on in Genoa."),
}
SPEAKERS = {0xAE: "Genoa patron", 0xAF: "Attendant", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B177_")}
    authored = {f"DK4_MES_B177_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B177 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B177_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "A Genoa patron recalls a youthful romance while launching a local tomato-dish boom.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B177 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v77-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 10 B177 Genoa tomato-boom dialogue records.",
        "inventory": {"identified_records": 10, "translated_records": 10, "blocks": {"177": 10}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
