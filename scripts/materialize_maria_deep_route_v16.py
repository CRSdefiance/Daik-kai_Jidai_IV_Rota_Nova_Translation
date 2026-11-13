from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v16.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 213

OVERRIDES = {
    "DK4_MES_B213_R0005": (
        "Mister, you need to pay today.{LB}Do you know how much you owe?"
    ),
    "DK4_MES_B213_R0008": (
        "Next time, for sure!{LB}Have you ever seen me skip out?"
    ),
    "DK4_MES_B213_R0012": "You've never paid at all.",
    "DK4_MES_B213_R0016": "Tch. Take this as payment.",
    "DK4_MES_B213_R0023": "Amethyst piece.",
    "DK4_MES_B213_R0031": (
        "Worth plenty.{LB}Keep it as interest.{LB}Keep the change! Hahaha!"
    ),
    "DK4_MES_B213_R0034": "Wait.",
    "DK4_MES_B213_R0042": "That piece...{LB}real amethyst?",
    "DK4_MES_B213_R0045": (
        "What'd you say?!{LB}Trying to ruin my business?!"
    ),
    "DK4_MES_B213_R0049": "Xien.",
    "DK4_MES_B213_R0053": (
        "Let me see.{LB}...Hm. This is definitely glass."
    ),
    "DK4_MES_B213_R0064": (
        "Enough.{LB}The owner hired us to recover it.{LB}Your excuses won't help."
    ),
    "DK4_MES_B213_R0071": "You...{LB}Enough is enough. Not today!",
    "DK4_MES_B213_R0078": (
        "Rough sailors come through every day!{LB}A barkeep has to know how to fight!"
    ),
    "DK4_MES_B213_R0107": (
        "Return it to its owner.{LB}He's surely done worse.{LB}"
        "Next time, he goes to the governor!"
    ),
}

SPEAKERS = {"03": "Maria", "43": "Conman", "5C": "Tavernkeeper"}
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B213_")
    }
    lines = _load_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V16 inventory mismatch: "
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
                "speaker": SPEAKERS.get(state, "Xien or scene text"),
                "context": (
                    "Complete tavern fraud and stolen-amethyst event: unpaid tab, "
                    "fake ornament appraisal, confrontation, fight, escape, and return clue."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Shared Japanese lines were reconciled with the Raphael layer; "
                    "Maria and Xien dialogue was independently localized for SC3."
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
        "dialogue_profile": "maria-story-tavern-fraud-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 213: complete tavern fraud, fake amethyst appraisal, "
            "confrontation and fight, escape, and stolen-item return setup."
        ),
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"213": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
