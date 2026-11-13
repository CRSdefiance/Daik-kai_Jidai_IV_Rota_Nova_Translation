from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v86.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    24: ("A man asks if his friend has heard the news.", "Hey, heard this?"),
    28: ("His friend asks what news.", "What?"),
    32: ("The man means the master of the mansion.", "The man at the mansion."),
    36: ("His friend asks if he means the unexplained illness.", "His strange illness?"),
    40: ("The man confirms it.", "Yeah."),
    44: ("His friend says everyone already knows about that illness.", "Everyone knows that."),
    48: ("The man asks whether he knows what happened afterward.", "And after that?"),
    52: ("His friend asks what happened afterward.", "After?"),
    56: ("The man says an ordinary medicine cured the illness at once.", "A drugstore remedy cured him outright."),
    59: ("His friend is surprised that a common medicine cured the mysterious illness.", "A common drug cured that illness?"),
    63: ("The man says it is an amazing story.", "Yes. Amazing, right?"),
    67: ("His friend wonders if the rumor is true.", "Yeah... Really?"),
    71: ("The man says it seems true, and the medicine is reputed to cure all illnesses.", "Yes. They say it cures any illness."),
    74: ("His friend wants some of the medicine for himself.", "Amazing! We ought to get some."),
    77: ("The man suggests going to buy it.", "Let's go buy it."),
    81: ("His friend agrees to go.", "Let's go."),
    85: ("The market notice predicts medicine will become popular in Havana.", "A cure may boom in Havana."),
}
SPEAKERS = {0x9F: "Townsman", 0x77: "Friend", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B190_")}
    authored = {f"DK4_MES_B190_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B190 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B190_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Havana rumor of a store-bought medicine curing a mysterious illness.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B190 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v86-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 17 B190 Havana medicine-rumor records.",
        "inventory": {"identified_records": 17, "translated_records": 17, "blocks": {"190": 17}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
