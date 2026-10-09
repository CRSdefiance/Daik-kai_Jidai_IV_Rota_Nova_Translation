from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v85.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("A collector says he finally acquired the piece recently.", "At last, got hold of it."),
    9: ("Another collector asks if he means the ceramics.", "Oh, the ceramics?"),
    13: ("The first collector says it was as fine as he had hoped.", "Yes, as hoped. A superb piece."),
    16: ("The other collector asks to see the fine piece.", "Splendid! May one take a look?"),
    19: ("The first invites him to visit his house to see it.", "Please do! Come by my house."),
    22: ("The other says the collecting fad makes good ceramics hard to obtain.", "With everyone collecting ceramics, fine pieces are hard to find."),
    26: ("The first says people who do not know their value buy ceramics for the fad.", "They chase the fad, with no idea what it's worth."),
    30: ("The other finds that a nuisance.", "What a bother."),
    34: ("The first agrees emphatically.", "Quite right."),
    38: ("A swindler points out the two collectors.", "Look at those men over there."),
    42: ("His accomplice asks what is special about the two men.", "Those two? What is it?"),
    46: ("The swindler sold them worthless ceramics at an absurd price recently.", "They paid a fortune for our junk."),
    49: ("His accomplice, short of money, proposes approaching the easy marks again.", "Nice customers. Our pockets are light. Try them again?"),
    53: ("The swindler likes the idea.", "Good."),
    57: ("The accomplice agrees to approach them.", "Right. Let's go."),
    61: ("The swindler calls out to one of the gentlemen.", "Sir!"),
    65: ("The market notice predicts ceramics will become popular in Hamburg.", "Ceramics may catch on in Hamburg."),
}
SPEAKERS = {
    0x93: "Collector", 0x52: "Other collector", 0x68: "Swindler",
    0x71: "Accomplice", 0xFE: "Market notice",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B189_")}
    authored = {f"DK4_MES_B189_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B189 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B189_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Hamburg ceramic collectors and two swindlers exploiting the fad.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B189 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v85-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 17 B189 Hamburg ceramics-market and swindler records.",
        "inventory": {"identified_records": 17, "translated_records": 17, "blocks": {"189": 17}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
