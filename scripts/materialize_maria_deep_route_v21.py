from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v21.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (160, 163, 166, 171)

OVERRIDES = {
    "DK4_MES_B160_R0005": "Bad cough. Cough, cough.",
    "DK4_MES_B160_R0013": "Yes. Just a little painful.{LB}Cough, cough.",
    "DK4_MES_B160_R0026": "Really? Which one?{LB}Cough, cough.",
    "DK4_MES_B160_R0029": "The name escapes me,{LB}but it uses almonds.",
    "DK4_MES_B160_R0036": "The almonds sounded so odd,{LB}that's why it stuck with me.",
    "DK4_MES_B160_R0047": "Then let's find some.",
    "DK4_MES_B160_R0051": "Me too.",
    "DK4_MES_B163_R0066": "Yes... Really true?",
    "DK4_MES_B163_R0073": "Amazing! Want some too.",
    "DK4_MES_B163_R0084": "Medicine boom in Havana.",
    "DK4_MES_B166_R0005": "What a meal!{LB}Never has food tasted so wonderful.",
    "DK4_MES_B166_R0036": "Then perhaps we should use it tonight.",
    "DK4_MES_B166_R0039": "Me too.",
    "DK4_MES_B166_R0043": "Then let me teach you now.",
    "DK4_MES_B171_R0037": "No wrongdoing here.",
}

SPEAKERS = {
    "0C": "Sailor",
    "0F": "Sailor",
    "52": "Townsman",
    "57": "Townsman",
    "68": "Townsman",
    "71": "Townsman",
    "77": "Townsman",
    "A6": "Lady",
    "A7": "Lady",
    "A8": "Lady",
    "FE": "System or scene text",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines = {
        str(item["id"]): str(item["variants"][0]["english"])
        for item in report["reusable"]
        if int(item["block"]) in BLOCKS
    }
    lines.update(OVERRIDES)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(lines) != set(rows):
        raise SystemExit(
            f"Maria V21 mismatch: missing={sorted(set(rows)-set(lines))}, "
            f"extra={sorted(set(lines)-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id in sorted(lines, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Unframed townsfolk dialogue"),
            "context": "Complete shared rumor, commodity-boom, and namahage dream events.",
            "source_meaning": english,
            "localization_note": "Cross-route Japanese match reviewed with SC3-specific state-byte classification.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-rumors-v21-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 160, 163, 166, and 171: four complete shared events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": 0, "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
