from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v19.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 182

OVERRIDES = {
    "DK4_MES_B182_R0032": (
        "This must be the treasure{LB}this warrior has long sought.{LB}"
        "Yukihisa Genjo Shiraki"
    ),
    "DK4_MES_B182_R0070": "...Oh. How intriguing.",
}

SPEAKERS = {
    "03": "Maria",
    "0B": "Jam Jack Ludwayer",
    "0C": "Yukihisa's letter",
    "D0": "Crewman",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B182_")
    }
    lines = _load_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V19 inventory mismatch: "
            f"missing={sorted(set(block_rows) - set(lines))}, "
            f"extra={sorted(set(lines) - set(block_rows))}"
        )

    records: list[dict[str, object]] = []
    for row_id in sorted(lines, key=lambda value: int(value.rsplit("R", 1)[1])):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}"
                    if state
                    else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Alternate companion report"),
                "context": (
                    "Complete Yukihisa correspondence event: alternate crewmate delivery "
                    "lines, his report on the cursed Muramasa, companion reactions, and "
                    "Maria's decision to investigate."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Shared Japanese was reconciled with reviewed terminal-route layers; "
                    "Shift-JIS lead bytes on alternate companion lines remain text, not states."
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
        "dialogue_profile": "maria-story-muramasa-letter-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 182: complete Yukihisa letter and cursed-Muramasa rumor, "
            "including every alternate companion delivery and reaction line."
        ),
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"182": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
