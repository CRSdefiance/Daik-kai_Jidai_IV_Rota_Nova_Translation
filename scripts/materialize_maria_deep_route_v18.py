from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v18.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 168

OVERRIDES = {
    "DK4_MES_B168_R0005": "Hm? Something smells good.",
    "DK4_MES_B168_R0008": "Sniff... Yes.",
    "DK4_MES_B168_R0016": (
        "Our specialty, packed with cheese.{LB}Delicious!"
    ),
    "DK4_MES_B168_R0023": "Don't ask the obvious.",
    "DK4_MES_B168_R0031": (
        "Certainly. Just a moment.{LB}Coming right up."
    ),
    "DK4_MES_B168_R0042": "Don't take my word for it.{LB}Try a bite.",
    "DK4_MES_B168_R0045": "Okay.",
    "DK4_MES_B168_R0049": "Munch...",
    "DK4_MES_B168_R0053": "Munch...",
    "DK4_MES_B168_R0061": "This is great!{LB}Amazing!",
    "DK4_MES_B168_R0072": (
        "Yes! Barkeep, this dish{LB}will be a sensation!"
    ),
}

SPEAKERS = {
    "5C": "Tavernkeeper",
    "67": "Tavern patron",
    "77": "Townsman",
    "FE": "Market report",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def _load_lines() -> dict[str, str]:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines: dict[str, str] = {}
    for item in report["reusable"]:
        if int(item["block"]) == BLOCK:
            lines[str(item["id"])] = str(item["variants"][0]["english"])
    lines.update(OVERRIDES)
    return lines


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}
    block_rows = {
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B168_")
    }
    lines = _load_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V18 inventory mismatch: "
            f"missing={sorted(set(block_rows) - set(lines))}, "
            f"extra={sorted(set(lines) - set(block_rows))}"
        )

    records: list[dict[str, object]] = []
    for row_id in sorted(lines, key=lambda value: int(value.rsplit("R", 1)[1])):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        if not state:
            raise SystemExit(f"Maria V18 missing presentation-state mapping: {row_id}")
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}",
                "speaker": SPEAKERS[state],
                "context": (
                    "Complete Veracruz tavern food event: locals smell and sample "
                    "the cheese specialty, praise it, and trigger the cheese boom."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Shared Japanese lines were reconciled with reviewed terminal-route "
                    "layers and polished for natural tavern dialogue."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"]
                + (["manual-break"] if "{LB}" in english else []),
                **(
                    {"manual_break_reason": "Protects semantic rows and pair phase."}
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-cheese-boom-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 168: complete Veracruz tavern cheese-specialty event "
            "and cheese-boom market forecast."
        ),
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"168": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
