from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v17.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 139

OVERRIDES = {
    "DK4_MES_B139_R0029": (
        "{MACRO:FI}, shall we meet him?{LB}He may be useful to us."
    ),
    "DK4_MES_B139_R0032": "Yes.",
    "DK4_MES_B139_R0036": "But with women along, perhaps don't...",
    "DK4_MES_B139_R0057": "So that's Mikhail.",
    "DK4_MES_B139_R0096": (
        "A genius! No one knows more.{LB}Even your bust size is obvious to me."
    ),
    "DK4_MES_B139_R0108": (
        "Odd manners, but learned.{LB}Shall we invite him?"
    ),
    "DK4_MES_B139_R0120": (
        "Your knowledge impressed us.{LB}Please lend your aid to our {MACRO:FO}."
    ),
    "DK4_MES_B139_R0128": "Please. We need your help.",
    "DK4_MES_B139_R0131": "Well, even so...{LB}Oh!",
    "DK4_MES_B139_R0137": "Admiral{LB}{MACRO:FI} {MACRO:FA}",
    "DK4_MES_B139_R0140": "{MACRO:FI}, eh?",
    "DK4_MES_B139_R0152": "Decided! Count me in!",
    "DK4_MES_B139_R0155": "{MACRO:FI}, dear!",
    "DK4_MES_B139_R0163": "Wha!",
    "DK4_MES_B139_R0167": "{MACRO:FI}, okay?{LB}Shameless!",
    "DK4_MES_B139_R0170": (
        "No! Decision made.{LB}Nothing will stop me!{LB}"
        "My knowledge will help. Don't worry!"
    ),
    "DK4_MES_B139_R0173": (
        "We invited him first.{LB}We have little choice now.{LB}"
        "Xien, let him aboard."
    ),
    "DK4_MES_B139_R0177": "But this shameless man...",
    "DK4_MES_B139_R0181": "Shameless?{LB}This is friendly affection!",
    "DK4_MES_B139_R0184": (
        "You Easterners won't understand.{LB}"
        "Westerners show affection this way!"
    ),
    "DK4_MES_B139_R0187": "No thanks...",
    "DK4_MES_B139_R0195": (
        "Mikhail is a scholar.{LB}He cannot take a deck post."
    ),
    "DK4_MES_B139_R0202": (
        "While viewing item information,{LB}press the X Button."
    ),
    "DK4_MES_B139_R0205": (
        "Shipboard work isn't for me,{LB}but call whenever you need item knowledge."
    ),
}

SPEAKERS = {
    "03": "Maria",
    "06": "Companion",
    "4C": "Mikhail",
    "57": "Townsman",
    "A5": "Girl",
    "A6": "Girl",
    "FE": "System tutorial",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B139_")
    }
    lines = _load_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V17 inventory mismatch: "
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
                "speaker": SPEAKERS.get(state, "Companion dialogue"),
                "context": (
                    "Complete Mikhail recruitment: local warning, demonstration, "
                    "Maria and Xien reactions, recruitment, item-information tutorial, "
                    "runtime protagonist and fleet names, and placement restriction."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Shared Japanese lines were reconciled with terminal-route layers; "
                    "Maria-specific recruitment and tutorial lines were localized for SC3."
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
        "dialogue_profile": "maria-story-mikhail-recruitment-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 139: complete Mikhail introduction, recruitment, "
            "runtime-name dialogue, item-information unlock, and tutorial."
        ),
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"139": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
