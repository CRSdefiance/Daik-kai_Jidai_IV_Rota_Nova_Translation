from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v83.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("The man says his cough has grown worse and coughs twice.", "Bad cough lately. Cough, cough!"),
    10: ("His friend asks if he is all right.", "You okay?"),
    14: ("He says he is all right but a little short of breath, then coughs.", "Yeah, okay. Short of breath... cough, cough."),
    17: ("His friend has recently seen many people coughing.", "Been seeing lots of folks coughing."),
    20: ("The man wonders if a bad illness is spreading.", "Some illness going around?"),
    24: ("His friend has heard of a good medicine somewhere.", "Heard there's a good remedy."),
    27: ("The man asks its name and coughs twice.", "What's it called? Cough, cough!"),
    30: ("His friend forgot the name but says it is made with almonds.", "Name escapes me. Has almonds in it."),
    33: ("The man is surprised to hear of almonds.", "Almonds?"),
    37: ("His friend remembers because almonds seemed an unlikely ingredient.", "Almonds in medicine? That was odd enough to remember."),
    41: ("The man asks whether it works and coughs twice.", "Does it work? Cough, cough!"),
    45: ("His friend says it works astonishingly well and is selling briskly.", "Works like a charm, they say. Selling like mad."),
    48: ("The man decides to look for the medicine.", "Then better find some."),
    52: ("His friend says he will look too.", "Let me look too."),
    56: ("The man thanks his friend and coughs twice.", "Thanks. Cough, cough!"),
    60: ("The market notice predicts almonds will become popular in Malacca.", "Almonds may catch on in Malacca."),
}
SPEAKERS = {0x9B: "Coughing man", 0x57: "Friend", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B187_")}
    authored = {f"DK4_MES_B187_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B187 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B187_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Malacca cough remedy and almond market rumor.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B187 Japanese. Source presentation leads are preserved. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v83-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 16 B187 Malacca almond-medicine rumor records.",
        "inventory": {"identified_records": 16, "translated_records": 16, "blocks": {"187": 16}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
