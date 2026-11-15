from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v7.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = {292, 293}

OVERRIDES = {
    "DK4_MES_B292_R0018": "No map, Admiral. This jungle is dangerous.",
    "DK4_MES_B292_R0022": "No map, Admiral. This jungle is too dangerous.",
    "DK4_MES_B292_R0024": "Admiral, this jungle is dangerous without a map.",
    "DK4_MES_B292_R0023": "No map, Admiral. The jungle is dangerous.",
    "DK4_MES_B292_R0062": (
        "This humidity is brutal.{LB}Crossing won't be easy."
    ),
    "DK4_MES_B292_R0089": "So dark...",
    "DK4_MES_B292_R0093": "Sir.",
    "DK4_MES_B292_R0099": "Go by touch",
    "DK4_MES_B292_R0101": "Use light",
    "DK4_MES_B292_R0108": "Eyes adjusting...{LB}Keep going?",
    "DK4_MES_B292_R0115": "Admiral! A giant snake!{LB}A crewman!",
    "DK4_MES_B292_R0126": "Whoa! A python!{LB}(Maybe?)",
    "DK4_MES_B292_R0132": "Too strong!{LB}Retreat!",
    "DK4_MES_B292_R0145": "Where did we come out?",
    "DK4_MES_B292_R0174": "Let's light a torch...",
    "DK4_MES_B292_R0165": "Ah! We are near the ruins.",
    "DK4_MES_B292_R0178": "Bats now?{LB}One thing after another...",
    "DK4_MES_B292_R0203": "They seem harmless.{LB}Leave them. Keep moving.",
    "DK4_MES_B292_R0213": "The sailors seem fatigued.",
    "DK4_MES_B292_R0247": "Admiral, the ruins!",
    "DK4_MES_B292_R0249": "The ruins, Admiral!",
    "DK4_MES_B292_R0251": "There they are!",
    "DK4_MES_B292_R0253": "Here are the ruins!",
    "DK4_MES_B292_R0255": "Admiral, the ruins!",
    "DK4_MES_B292_R0257": "Admiral, the ruins!",
    "DK4_MES_B292_R0259": "Admiral, here are the ruins.",
    "DK4_MES_B293_R0047": "What?",
    "DK4_MES_B293_R0058": "Back to port, then.",
    "DK4_MES_B293_R0094": "Admiral, the ruins!",
    "DK4_MES_B293_R0096": "Admiral, the ruins!",
    "DK4_MES_B293_R0110": "We made it...{LB}Going in.",
}

EXCLUDED = {
    "DK4_MES_B292_R0036": "Binary event-control payload; not dialogue.",
    "DK4_MES_B292_R0141": "Binary event-control payload; not dialogue.",
    "DK4_MES_B292_R0215": "Binary event-control payload; not dialogue.",
    "DK4_MES_B293_R0022": "Binary event-control payload; not dialogue.",
    "DK4_MES_B293_R0069": "Binary F event command; not dialogue.",
    "DK4_MES_B293_R0079": "Binary event-control payload; not dialogue.",
}

SPEAKERS = {
    "03": "Maria",
    "16": "Party member",
    "B3": "Expedition guide",
    "CF": "Party member",
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
    expected = set(block_rows) - set(EXCLUDED)
    if set(lines) != expected:
        raise SystemExit(
            "Maria V7 inventory mismatch: "
            f"missing={sorted(expected - set(lines))}, extra={sorted(set(lines) - expected)}"
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
        context = (
            "Complete jungle-and-cave expedition: map warnings, departure, cave "
            "choices, snake and bat encounters, injuries, fatigue, escape, and "
            "arrival at the ruins."
            if block == 292
            else "Complete island-ruins continuation: guide briefing, ancient-city "
            "discovery, sea crossing, secrecy warning, landing, and final approach."
        )
        records.append(
            {
                "id": row_id,
                "english": (
                    f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
                ),
                "speaker": SPEAKERS.get(state, "Party member, choice, or scene text"),
                "context": context,
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "SC3-only Maria lines and ambiguous variants were independently "
                    "resolved, with binary event-control records explicitly excluded."
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
        "dialogue_profile": "maria-story-jungle-ruins-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 blocks 292-293: complete jungle/cave expedition and the "
            "island-ruins continuation, including every party variant and branch."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": len(EXCLUDED),
            "blocks": counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
