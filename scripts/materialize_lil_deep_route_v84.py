from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v84.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("A lord calls a glass piece splendid, a true work of art.", "Splendid! A work of art!"),
    10: ("His attendant agrees with the lord.", "As you say."),
    14: ("The lord assumes so fine a piece came from a famous craftsman.", "A renowned artisan must have made such a fine piece."),
    18: ("The attendant agrees that it seems so.", "So it seems."),
    22: ("The lord did not know such objects had become fashionable.", "Hm. This is in fashion? Who knew?"),
    26: ("The lord asks what the object is called.", "What's it called?"),
    30: ("The attendant names it giyaman, meaning glass.", "Giyaman. Glass, my lord."),
    34: ("The lord repeats the name giyaman.", "Hm. Giyaman."),
    38: ("The lord orders all the glass in town gathered for his collection.", "Add it to my collection. Gather all the glass in town."),
    41: ("The attendant accepts the order.", "At once, my lord."),
    45: ("The market notice predicts glass will become popular in Osaka.", "Glass may catch on in Osaka."),
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B188_")}
    authored = {f"DK4_MES_B188_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B188 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B188_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if number == 45:
            if lead != 0xFE:
                raise ValueError(f"{row_id}: expected market notice state FE, got {lead:02X}")
            prefix, speaker = "{SPEAKER:FE}", "Market notice"
        else:
            if lead not in {0x82, 0x96}:
                raise ValueError(f"{row_id}: expected Shift-JIS text lead, got {lead:02X}")
            prefix = ""
            speaker = "Osaka lord" if lead == 0x82 else "Attendant"
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{prefix}{english}{{PAD}}",
            "speaker": speaker,
            "context": "Osaka lord admires giyaman glass and orders his attendant to collect it.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B188 Japanese. The 82/96 bytes are Shift-JIS "
                "text leads, not presentation states; FE is the market notice state. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v84-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 11 B188 Osaka giyaman-glass market records.",
        "inventory": {"identified_records": 11, "translated_records": 11, "blocks": {"188": 11}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
