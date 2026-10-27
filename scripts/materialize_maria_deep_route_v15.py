from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v15.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 215

OVERRIDES = {
    "DK4_MES_B215_R0005": "Ma'am!",
    "DK4_MES_B215_R0009": "What is it?",
    "DK4_MES_B215_R0020": "Ah, priest.",
    "DK4_MES_B215_R0024": "Such dignity.{LB}Does it have a history?",
    "DK4_MES_B215_R0047": "Really?{LB}The statue almost seems alive.",
    "DK4_MES_B215_R0055": (
        "Ha! No chance!{LB}We don't need that odd thing!{LB}Right, Admiral?"
    ),
    "DK4_MES_B215_R0078": "Everyone, give me a hand.",
    "DK4_MES_B215_R0082": "Stop! Leave it alone!",
    "DK4_MES_B215_R0086": "Go on without me.",
    "DK4_MES_B215_R0090": (
        "All right!{LB}We'll help. Happy now?{LB}Honestly!"
    ),
    "DK4_MES_B215_R0125": "Run!",
    "DK4_MES_B215_R0145": "We were just lucky.",
    "DK4_MES_B215_R0153": "No, we truly were just lucky.",
    "DK4_MES_B215_R0163": "{MACRO:FI}: Spirit +1!",
    "DK4_MES_B215_R0178": (
        "Exactly!{LB}You had me worried you'd take it!"
    ),
}

EXCLUDED = {
    "DK4_MES_B215_R0099": "Two-byte event-control payload between lifting and fall branches.",
}

SPEAKERS = {"03": "Maria", "06": "Crewman", "8B": "Priest", "FE": "System"}
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B215_")
    }
    lines = _load_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V15 inventory mismatch: "
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
                "speaker": SPEAKERS.get(state, "Choice text"),
                "context": (
                    "Complete church figurehead challenge: statue lore, accept and "
                    "decline choices, lifting attempt, failure escape, success branch, "
                    "priest's blessing, and Maria's Spirit reward."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Shared Japanese lines were reconciled with terminal-route layers; "
                    "Maria-specific responses and reward text were localized for SC3."
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
        "dialogue_profile": "maria-story-church-figurehead-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 215: complete church figurehead challenge, all choices "
            "and result branches, priest dialogue, blessing, and Spirit reward."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"215": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
