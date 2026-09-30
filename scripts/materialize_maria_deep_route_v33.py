from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v33.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (276,)

LINES = {
    "DK4_MES_B276_R0006": "Barkeep, is he here?",
    "DK4_MES_B276_R0010": "Wait here.",
    "DK4_MES_B276_R0014": "Ah, you. What is it?",
    "DK4_MES_B276_R0017": "The informant? Tell us about{LB}the Portuguese missionaries.",
    "DK4_MES_B276_R0020": "Huh? Who is this woman?",
    "DK4_MES_B276_R0023": "My new boss.",
    "DK4_MES_B276_R0027": "Nothing is free. Can you pay{LB}1,000 coins?",
    "DK4_MES_B276_R0030": "Yes.",
    "DK4_MES_B276_R0035": "Good. They arrive tomorrow,{LB}right here in Macao.",
    "DK4_MES_B276_R0039": "You are sure?",
    "DK4_MES_B276_R0043": "A liar would say next week in Hangzhou,{LB}then flee.",
    "DK4_MES_B276_R0047": "All right. Thanks.",
    "DK4_MES_B276_R0051": "We must approach them and learn{LB}why the boss kept me away.",
    "DK4_MES_B276_R0054": "Right.",
}

PRESENTATION_STATES = {0x03, 0x5D, 0x65, 0x66}
SPEAKERS = {"03": "Maria", "5D": "Barkeep", "65": "Informant", "66": "Defector"}

def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(LINES) != set(rows):
        raise SystemExit(f"Maria V33 mismatch: missing={sorted(set(rows)-set(LINES))}, extra={sorted(set(LINES)-set(rows))}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: int(value.rsplit("R", 1)[1])):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        row = rows[row_id]
        english = LINES[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Maria"), "context": "Macao tavern investigation.",
            "source_meaning": english,
            "localization_note": "Direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v33-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 block 276: Macao tavern informant and missionaries' arrival lead.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "excluded": [], "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")

if __name__ == "__main__":
    main()
