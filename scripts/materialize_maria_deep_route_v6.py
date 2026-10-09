from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v6.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 291

OVERRIDES = {
    "DK4_MES_B291_R0021": "No map, Admiral. We'll get lost.",
    "DK4_MES_B291_R0024": "Admiral, no map means getting lost.",
    "DK4_MES_B291_R0103": "Let's keep moving for now.",
    "DK4_MES_B291_R0136": "Seek a path",
    "DK4_MES_B291_R0143": "Push through the trees?",
    "DK4_MES_B291_R0167": "This is crazy... All right, go!",
    "DK4_MES_B291_R0173": "The sailors seem fatigued.",
    "DK4_MES_B291_R0178": "Let's find another way.",
    "DK4_MES_B291_R0213": "Moving in fog is risky. Let's wait for it to clear.",
    "DK4_MES_B291_R0257": "The fog finally cleared. Let's go.",
}
EXCLUDED = {
    "DK4_MES_B291_R0037": "Binary event-control payload; not dialogue.",
    "DK4_MES_B291_R0065": "Binary !F event command with encoded argument; not dialogue.",
    "DK4_MES_B291_R0105": "Binary F event command with encoded argument; not dialogue.",
    "DK4_MES_B291_R0180": "Binary choice/control payload; not dialogue.",
}

SPEAKERS = {
    "03": "Maria",
    "D0": "Party member",
    "D3": "Party member",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B291_")
    }
    lines = _load_reused_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V6 inventory mismatch: "
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
                    "Complete foggy-forest expedition: map warnings, fog responses, "
                    "navigation choices, dead ends, sailor fatigue, waiting branch, and "
                    "arrival at the destination."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "SC3-only Maria lines and ambiguous variants were independently "
                    "resolved, with event-control records explicitly excluded."
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
        "dialogue_profile": "maria-story-shared-events-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 291: complete foggy-forest expedition, all party variants, "
            "navigation choices, dead ends, fatigue, waiting branch, and arrival lines."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"291": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
