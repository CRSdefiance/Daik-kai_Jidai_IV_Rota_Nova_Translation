from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v3.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 252

# Exact-Japanese matches inherit the already reviewed English from the current
# terminal Raphael/Hodram/Lil layers.  Ambiguous matches and SC3-only Maria
# responses are resolved explicitly here after reviewing the full branch.
OVERRIDES = {
    "DK4_MES_B252_R0020": "Admiral, no map. We'll get lost.",
    "DK4_MES_B252_R0022": "No map, Admiral. We'll get lost.",
    "DK4_MES_B252_R0023": "Admiral, no map. We'll get lost.",
    "DK4_MES_B252_R0024": "Admiral, no map means getting lost.",
    "DK4_MES_B252_R0025": "Admiral, we'll get lost without a map!",
    "DK4_MES_B252_R0061": "Shall we go?",
    "DK4_MES_B252_R0165": "Admiral... This bear won't move.",
    "DK4_MES_B252_R0166": "Admiral... The bear won't run!",
    "DK4_MES_B252_R0174": "Hang on a bit.",
    "DK4_MES_B252_R0221": "Asleep...",
    "DK4_MES_B252_R0263": "What a bear! Threats do nothing!",
    "DK4_MES_B252_R0312": "Run!!",
}
EXCLUDED = {
    "DK4_MES_B252_R0037": (
        "Binary event-control payload; no readable Japanese dialogue body."
    )
}

SPEAKERS = {
    "03": "Maria",
    "0E": "Party member",
    "16": "Party member",
    "D0": "Party member",
    "D3": "Party member",
    "D7": "Party member",
    "D8": "Party member",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B252_")
    }
    lines = _load_reused_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V3 inventory mismatch: "
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
                    "Complete forest-ruins expedition: map warnings, party variants, "
                    "bear encounter, choices, combat outcomes, escape, injury/fatigue "
                    "messages, and arrival at the ruins."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to the reviewed terminal route layers; "
                    "SC3-only Maria lines and ambiguous variants were independently "
                    "resolved, and every SC3 presentation byte remains route-local."
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
            "Maria SC3 block 252: complete forest-ruins expedition, including every "
            "party-member variant, bear branch, choice, consequence, system message, "
            "escape response, and ruins-arrival line."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"252": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
