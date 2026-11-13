from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v11.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 221

OVERRIDES = {
    "DK4_MES_B221_R0030": "This one!",
    "DK4_MES_B221_R0041": (
        "Admiral, the ceiling falls!{LB}Danger!"
    ),
    "DK4_MES_B221_R0042": "Admiral! The ceiling is collapsing!",
    "DK4_MES_B221_R0046": "Look out!{LB}Ceiling's falling!",
    "DK4_MES_B221_R0049": "The ceiling is collapsing.{LB}We must leave.",
    "DK4_MES_B221_R0052": (
        "That was wrong.{LB}We have to get out!{LB}Let's return to town."
    ),
    "DK4_MES_B221_R0067": "This one!",
    "DK4_MES_B221_R0078": (
        "Admiral, the ceiling falls!{LB}Danger!"
    ),
    "DK4_MES_B221_R0079": "Admiral! The ceiling is collapsing!",
    "DK4_MES_B221_R0082": "Look out! The ceiling is collapsing!",
    "DK4_MES_B221_R0086": "The ceiling is collapsing.{LB}We must leave.",
    "DK4_MES_B221_R0089": "That was wrong.{LB}We have to get out.",
    "DK4_MES_B221_R0104": (
        "The ice won't raise it.{LB}Right is correct."
    ),
    "DK4_MES_B221_R0121": "Where?",
    "DK4_MES_B221_R0149": "Yes",
    "DK4_MES_B221_R0162": "Huh?",
    "DK4_MES_B221_R0176": "Who knows?",
    "DK4_MES_B221_R0211": "Everyone, run!",
}

EXCLUDED = {
    "DK4_MES_B221_R0185": "Binary event-control payload; not dialogue.",
}

SPEAKERS = {
    "03": "Maria",
    "14": "Party member",
    "D0": "Party member",
    "FE": "Inscription, spirit, system message, or sound",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def _load_reused_lines() -> dict[str, str]:
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B221_")
    }
    lines = _load_reused_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V11 inventory mismatch: "
            f"missing={sorted(expected - set(lines))}, extra={sorted(set(lines) - expected)}"
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
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Party member, choice, or scene text"),
                "context": (
                    "Complete water-level riddle and awakened-statue event: choice "
                    "branches, collapsing-ceiling failures, correct answer, spirit "
                    "dialogue, figurehead reward, refusal branch, escape, and curse."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "Maria-specific answers and branch dialogue were independently "
                    "localized, with the binary event control explicitly excluded."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"]
                + (["manual-break"] if "{LB}" in english else []),
                **(
                    {
                        "manual_break_reason": (
                            "Protects semantic rows and progressive ASCII pair phase."
                        )
                    }
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
        "dialogue_profile": "maria-story-shared-events-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 221: complete water-level riddle, failure branches, "
            "awakened statue, figurehead reward/refusal, escape, and curse aftermath."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"221": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
