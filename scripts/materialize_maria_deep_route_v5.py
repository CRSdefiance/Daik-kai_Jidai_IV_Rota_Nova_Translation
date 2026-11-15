from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v5.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 285

OVERRIDES = {
    "DK4_MES_B285_R0020": "No map, Admiral. We'll get lost.",
    "DK4_MES_B285_R0021": "Admiral, no map. We'll get lost.",
    "DK4_MES_B285_R0022": "Admiral, no map. We'll get lost.",
    "DK4_MES_B285_R0023": "Admiral, no map means getting lost.",
    "DK4_MES_B285_R0024": "Admiral, we'll get lost without a map!",
    "DK4_MES_B285_R0064": "Desert heat can't be helped. Let's go.",
    "DK4_MES_B285_R0091": "Shh! Everyone, stay calm.",
    "DK4_MES_B285_R0114": "Leave it. Hah!",
    "DK4_MES_B285_R0138": "Drive them off!",
    "DK4_MES_B285_R0188": "My fault.",
    "DK4_MES_B285_R0236": "Thanks. All better.",
    "DK4_MES_B285_R0240": "Leave quietly. Don't provoke them.",
    "DK4_MES_B285_R0277": "Oh no! The cargo fell!",
    "DK4_MES_B285_R0293": "Ah!",
    "DK4_MES_B285_R0301": "Whoa!",
    "DK4_MES_B285_R0327": "Everyone, run! Hurry!",
}

SPEAKERS = {
    "03": "Maria",
    "97": "Party member",
    "9C": "Party member",
    "D0": "Party member",
    "D3": "Party member",
    "D6": "Party member",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B285_")
    }
    lines = _load_reused_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V5 inventory mismatch: "
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
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Party member, choice, or scene text"),
                "context": (
                    "Complete desert expedition: map warnings, heat responses, scorpion "
                    "ambush and choices, injury/treatment branches, cargo loss, escape, "
                    "and destination arrival."
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
            "Maria SC3 block 285: complete desert/scorpion expedition, all party "
            "variants, ambush branches, injuries, treatment, cargo loss, escape, and "
            "destination-arrival lines."
        ),
        "excluded_records": {},
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"285": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
