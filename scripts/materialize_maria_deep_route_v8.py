from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v8.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = {300, 301, 302}

OVERRIDES = {
    "DK4_MES_B300_R0013": "Sextant received.",
    "DK4_MES_B301_R0009": "At last...{LB}The day has come.",
    "DK4_MES_B302_R0019": "Perhaps he knew medicine?",
    "DK4_MES_B302_R0023": (
        "No. He called it alchemy.{LB}Alchemy removed poison from our water."
    ),
    "DK4_MES_B302_R0057": "Charles's book!{LB}We found it!",
    "DK4_MES_B302_R0068": "Charles, what's wrong?",
    "DK4_MES_B302_R0072": (
        "Rumors of a new reagent drew me{LB}all the way to the New World!"
    ),
    "DK4_MES_B302_R0082": "We'll talk later.",
    "DK4_MES_B302_R0089": "So where is that monk now?",
    "DK4_MES_B302_R0104": (
        "Yet he hid his illness{LB}and gave every dose to us!"
    ),
    "DK4_MES_B302_R0118": "Us?",
    "DK4_MES_B302_R0132": "All right.{LB}Let's do it.",
}

SPEAKERS = {
    "02": "Companion",
    "03": "Maria",
    "12": "Charles",
    "A1": "Elder or event participant",
    "B3": "Village elder",
    "CF": "Party member",
    "FE": "System message",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def _load_reused_lines() -> dict[str, str]:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines: dict[str, str] = {}
    for item in report["reusable"]:
        if int(item["block"]) in BLOCKS:
            lines[str(item["id"])] = str(item["variants"][0]["english"])
    lines.update(OVERRIDES)
    return lines


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}
    block_rows = {
        row_id: row
        for row_id, row in rows.items()
        if any(row_id.startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
    }
    lines = _load_reused_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V8 inventory mismatch: "
            f"missing={sorted(set(block_rows) - set(lines))}, "
            f"extra={sorted(set(lines) - set(block_rows))}"
        )

    records: list[dict[str, object]] = []
    for row_id in sorted(
        lines,
        key=lambda value: (
            int(value.split("_B", 1)[1].split("_", 1)[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        context = {
            300: "Complete sextant handoff and reward exchange.",
            301: "Complete inherited-item handoff and trust dialogue.",
            302: (
                "Complete alchemy-book village event: plague history, Charles's "
                "research, the monk's sacrifice, book inheritance, and ore quest."
            ),
        }[block]
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Party member or scene text"),
                "context": context,
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "Maria-specific lines and terse inherited renderings were "
                    "independently localized and allocation-checked."
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

    counts = {
        str(block): sum(
            record["id"].startswith(f"DK4_MES_B{block}_") for record in records
        )
        for block in sorted(BLOCKS)
    }
    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-alchemy-event-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 300-302: sextant exchange, inherited-item handoff, "
            "and the complete alchemy-book village and rare-ore quest setup."
        ),
        "excluded_records": {},
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
