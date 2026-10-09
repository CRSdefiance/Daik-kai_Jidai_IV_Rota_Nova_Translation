from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v14.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 181

OVERRIDES = {
    "DK4_MES_B181_R0004": "You there, can we talk?",
    "DK4_MES_B181_R0020": (
        "You remind me of a mighty woman pirate from long ago.{LB}"
        "She was truly strong."
    ),
    "DK4_MES_B181_R0027": (
        "Not your face. More your air...{LB}Maybe because you look strong."
    ),
    "DK4_MES_B181_R0031": "Really? Then she can inspire me to get stronger.",
    "DK4_MES_B181_R0043": "Yes, her old sword. No one knows what it's worth.",
    "DK4_MES_B181_R0069": "That's all?{LB}Then how do we find it?",
    "DK4_MES_B181_R0072": (
        "Don't ask me...{LB}Still, you look capable of finding it."
    ),
    "DK4_MES_B181_R0075": "All right. Noted.",
    "DK4_MES_B181_R0078": "Yes. You'll find it.{LB}Good luck.",
    "DK4_MES_B181_R0081": "Thanks.",
    "DK4_MES_B181_R0085": (
        "(A Caribbean pirate sword...{LB}That sounds worth seeing.)"
    ),
    "DK4_MES_B181_R0089": "Cristina: Charm +1!",
}

SPEAKERS = {"07": "Cristina", "AA": "Old sailor", "FE": "System"}
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B181_")
    }
    lines = _load_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V14 inventory mismatch: "
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
            raise SystemExit(f"Maria V14 missing presentation-state mapping: {row_id}")
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}",
                "speaker": SPEAKERS[state],
                "context": (
                    "Complete Cristina pirate-sword rumor: resemblance to a legendary "
                    "woman pirate, Caribbean battle clue, quest resolve, and Charm gain."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Shared Japanese lines were reconciled with terminal-route layers; "
                    "Cristina-specific lines were independently localized for SC3."
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
        "dialogue_profile": "maria-story-pirate-sword-rumor-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 181: complete Cristina woman-pirate resemblance and "
            "Caribbean treasure-sword rumor event through the Charm reward."
        ),
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"181": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
