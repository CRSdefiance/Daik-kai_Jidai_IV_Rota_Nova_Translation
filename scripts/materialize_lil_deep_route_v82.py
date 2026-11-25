from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v82.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (184, 6): ("A woman enjoys a cup of tea.", "Ah, so good!"),
    (184, 10): ("Her companion praises tea.", "Tea truly is wonderful."),
    (184, 14): ("She wonders why tea did not become popular sooner.", "Why wasn't tea popular sooner?"),
    (184, 18): ("He says people failed to appreciate tea.", "People have no taste, it seems."),
    (184, 22): ("She asks him to buy more tea tomorrow.", "Nearly out of tea. Buy more tomorrow?"),
    (184, 26): ("He agrees to buy the tea.", "Of course. More tomorrow."),
    (184, 30): ("She says tea is delicious and soothing.", "Tea tastes so good. So soothing."),
    (184, 33): ("He says they cannot live without tea.", "We can't live without tea now."),
    (184, 36): ("The market notice predicts a Sofala tea boom.", "Tea may catch on in Sofala."),
    (185, 6): ("A woman complains about the cold.", "So cold... Brr!"),
    (185, 10): ("Her companion has not felt cold like this in years.", "Been ages since it was this cold."),
    (185, 13): ("She wants a fur coat to avoid freezing.", "Need a fur coat. This cold could freeze me!"),
    (185, 16): ("He says cold weather has raised the price of furs.", "Cold weather's made furs pricier."),
    (185, 19): ("She agrees and shivers.", "So they say... Brr!"),
    (185, 22): ("He hopes the weather warms up soon.", "Hope it warms up soon."),
    (185, 26): ("She still wants a fur coat while the cold lasts.", "Yes. Still want a fur coat."),
    (185, 29): ("The market notice predicts a Stockholm fur boom.", "Stockholm may see a fur boom."),
    (186, 5): ("A patron says the food needs more sweetness.", "Something's missing... Sweetness! That's what we need!"),
    (186, 9): ("Her attendant asks about sweetness.", "Sweetness?"),
    (186, 13): ("The patron says a light taste will not satisfy customers.", "Yes! This light taste won't satisfy customers. Sweetness matters!"),
    (186, 16): ("The attendant is doubtful.", "Does it?"),
    (186, 20): ("The patron insists she is right.", "Yes! Take my word for it!"),
    (186, 23): ("The attendant asks how to add sweetness.", "How do we make it sweeter?"),
    (186, 26): ("The patron leaves that problem to the attendant.", "That's your job to work out!"),
    (186, 29): ("The attendant gives a weary acknowledgment.", "Right..."),
    (186, 33): ("The patron says sweet foods will become popular.", "Sweet things are sure to catch on."),
    (186, 36): ("The attendant acknowledges her.", "Right."),
    (186, 40): ("The patron repeats the instruction and laughs.", "Keep it sweet! Do your best! Ho ho!"),
    (186, 63): ("The market notice predicts an Alexandria sweets boom.", "Sweets may catch on in Alexandria."),
}
SPEAKERS = {
    0xA4: "Companion", 0xA5: "Companion", 0xAE: "Alexandria patron",
    0xAF: "Attendant", 0xFE: "Market notice",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {
        row_id for row_id in source_rows
        if row_id.startswith(("DK4_MES_B184_", "DK4_MES_B185_", "DK4_MES_B186_"))
    }
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B184-B186 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Linked Sofala tea, Stockholm fur, and Alexandria sweets market scenes.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B184-B186 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v82-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 29 B184-B186 Sofala tea, Stockholm fur, and Alexandria sweets records.",
        "inventory": {"identified_records": 29, "translated_records": 29, "blocks": {"184": 9, "185": 8, "186": 12}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
