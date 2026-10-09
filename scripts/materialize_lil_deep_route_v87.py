from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v87.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    53: ("The father says only that dye can produce the desired color.", "Only that dye can make this color."),
    56: ("His son urges him to buy before other shops buy out the dye.", "Buy now, before other shops do."),
    60: ("The father hesitates.", "But..."),
    64: ("The son warns that waiting until it sells out will be too late.", "Wait too long and it'll be sold out."),
    68: ("The father doubts it will sell out and sees no need to hurry.", "No need to rush. Surely it won't sell out?"),
    72: ("The son insists the dye is popular and will sell out quickly.", "No, it's popular and will sell out."),
    76: ("The father remains uncertain.", "You think?"),
    80: ("The son insists he is right.", "Yes!"),
    84: ("The father agrees to leave the purchase to his son.", "All right, you decide."),
    88: ("The son asks his father not to sulk and promises the dye will bring a profit.", "Don't sulk, Dad. With this dye, we're sure to profit."),
    92: ("The father asks again if that is true.", "You think?"),
    96: ("The son firmly assures him.", "Of course!"),
    100: ("The market notice predicts dyes will become popular in Calicut.", "Dyes may catch on in Calicut."),
}
SPEAKERS = {0x56: "Father", 0x9A: "Son", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B191_")}
    authored = {f"DK4_MES_B191_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B191 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B191_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Calicut father and son consider buying scarce dye for their shop.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B191 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v87-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 13 B191 Calicut dye-market records.",
        "inventory": {"identified_records": 13, "translated_records": 13, "blocks": {"191": 13}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
