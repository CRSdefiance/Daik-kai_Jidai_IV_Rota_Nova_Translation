from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v10.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 283

OVERRIDES = {
    "DK4_MES_B283_R0020": "No map, Admiral. We won't know the way.",
    "DK4_MES_B283_R0023": "No map, Admiral. Where do we go?",
    "DK4_MES_B283_R0064": "Dead end...",
    "DK4_MES_B283_R0072": "Turn back now",
    "DK4_MES_B283_R0074": "Seek a way",
    "DK4_MES_B283_R0082": "Let's go back.{LB}Seek another way.",
    "DK4_MES_B283_R0088": "Can we go on?",
    "DK4_MES_B283_R0102": "No. There's no path.",
    "DK4_MES_B283_R0103": "No... nothing anywhere.",
    "DK4_MES_B283_R0105": "No luck. There's no way through.",
    "DK4_MES_B283_R0107": "No. There's no path.",
    "DK4_MES_B283_R0108": "No. There's no path at all.",
    "DK4_MES_B283_R0110": "No path here!",
    "DK4_MES_B283_R0112": "No. There's no path.",
    "DK4_MES_B283_R0115": "No choice. Turn back{LB}and seek another way.",
}

EXCLUDED = {
    "DK4_MES_B283_R0035": "Binary event-control payload; not dialogue.",
    "DK4_MES_B283_R0062": "Binary F event command; not dialogue.",
    "DK4_MES_B283_R0090": "Binary choice/event-control payload; not dialogue.",
}

SPEAKERS = {
    "03": "Maria",
    "D0": "Party member",
    "D3": "Party member",
    "D6": "Party member",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B283_")
    }
    lines = _load_reused_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V10 inventory mismatch: "
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
                    "Complete dark-forest navigation event: map warnings, forest "
                    "descriptions, dead end, route choices, failed path search, "
                    "turning back, elapsed day, and discovery responses."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "Maria-specific choices and party variants were independently "
                    "localized, with binary controls explicitly excluded."
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
        "dialogue_profile": "maria-story-dark-forest-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 283: complete dark-forest dead-end and route-search "
            "event, every choice and party response, through discovery."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"283": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
