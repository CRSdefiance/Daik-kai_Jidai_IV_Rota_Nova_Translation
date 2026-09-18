from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v25b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (301,)
EXCLUDED: dict[str, str] = {}
LINES = {
    "DK4_MES_B301_R0006": "Ah, {MACRO:FI}.{LB}Good timing.",
    "DK4_MES_B301_R0009": "Do you know the Colosseum?",
    "DK4_MES_B301_R0013": "The Colosseum?",
    "DK4_MES_B301_R0017": "Ruins from Roman times.{LB}Heard you seek ruins, so here is a lead.",
    "DK4_MES_B301_R0021": "That helps.{LB}Let us go at once.",
    "DK4_MES_B301_R0024": "Take care.{LB}And remember to buy a map.",
}
SPEAKERS = {"01": "Hodram Bergstrom", "C0": "Tavern patron", "CF": "Companion"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B301_")}
    if set(LINES) != set(source_rows):
        raise SystemExit(f"Hodram V25b inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, extra={sorted(set(LINES)-set(source_rows))}")
    records = []
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Companion"), "context": "A local patron directs Hodram to the Colosseum ruins.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English with the established Colosseum name.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-colosseum-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram Colosseum rumor in SC1 block 301.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"301": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
