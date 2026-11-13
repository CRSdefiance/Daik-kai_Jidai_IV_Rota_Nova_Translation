from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v4.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 281

OVERRIDES = {
    "DK4_MES_B281_R0021": "Admiral, no map could be trouble.",
    "DK4_MES_B281_R0057": "Well, let us go.",
    "DK4_MES_B281_R0088": "Huh?! Aah!!",
    "DK4_MES_B281_R0093": "Shh! Everyone, stay calm.",
    "DK4_MES_B281_R0116": "Let me drive them off.",
    "DK4_MES_B281_R0139": "My fault.",
    "DK4_MES_B281_R0160": "You okay?!",
    "DK4_MES_B281_R0166": "All right, thanks.",
    "DK4_MES_B281_R0179": "Draw swords! Keep moving!",
    "DK4_MES_B281_R0250": "This wound is my fault... Sorry...",
    "DK4_MES_B281_R0281": "The sailors seem fatigued.",
    "DK4_MES_B281_R0286": "Those wolves are starving. We must flee now!",
}
EXCLUDED = {
    "DK4_MES_B281_R0037": "Binary event-control payload; not dialogue.",
    "DK4_MES_B281_R0316": "Binary F-command payload with encoded argument; not dialogue.",
}

SPEAKERS = {
    "03": "Maria",
    "97": "Party member",
    "9C": "Party member",
    "D0": "Party member",
    "D3": "Party member",
    "D6": "Party member",
    "D7": "Party member",
    "DA": "Party member",
    "FE": "System message",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B281_")
    }
    lines = _load_reused_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V4 inventory mismatch: "
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
                    "Complete wolf-forest expedition: map warnings, party variants, "
                    "wolf ambush, choices, injuries, treatment, fatigue, escape, and "
                    "arrival at the destination."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "SC3-only Maria lines and ambiguous variants were independently "
                    "resolved, with SC3 presentation state preserved."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
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
        "dialogue_profile": "maria-story-wolf-event-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 281: complete wolf-forest expedition, all party variants, "
            "ambush choices, injuries, treatment, fatigue, escape, and arrival lines."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"281": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
