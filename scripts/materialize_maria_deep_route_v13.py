from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v13.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 179

OVERRIDES = {
    "DK4_MES_B179_R0016": "What's wrong?{LB}Oh, earrings?",
    "DK4_MES_B179_R0031": "Really? How so?",
    "DK4_MES_B179_R0038": "Hehe. Dancing...{LB}Well, Cristina?",
    "DK4_MES_B179_R0045": (
        "Wearing them isn't the only option.{LB}Give them to a woman at the tavern,{LB}"
        "and she'll adore you at once."
    ),
    "DK4_MES_B179_R0058": "Right.",
    "DK4_MES_B179_R0070": "We'll take them.",
    "DK4_MES_B179_R0079": "Buy it!",
    "DK4_MES_B179_R0105": "You can keep it!",
    "DK4_MES_B179_R0116": "Still don't get it?{LB}Then no sale. Go away.",
}

EXCLUDED = {
    "DK4_MES_B179_R0014": "Binary event-control payload between merchant and Maria lines.",
}

SPEAKERS = {
    "03": "Maria",
    "07": "Cristina",
    "AD": "Merchant",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B179_")
    }
    lines = _load_lines()
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V13 inventory mismatch: "
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
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": (
                    "Complete ceramic-earrings merchant event: sales pitch, Maria and "
                    "Cristina reactions, information-use explanation, purchase choice, "
                    "successful sale, and both refusal branches."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal-route layers; "
                    "Maria-specific dialogue and terse choices were localized for SC3."
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
        "dialogue_profile": "maria-story-earrings-event-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 179: complete ceramic-earrings merchant event with "
            "sales pitch, choices, purchase, refusal branches, and companion dialogue."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": {"179": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
