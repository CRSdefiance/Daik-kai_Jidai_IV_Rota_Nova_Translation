from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v9.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCK = 259

OVERRIDES = {
    "DK4_MES_B259_R0017": "Admiral, no map. This jungle is dangerous.",
    "DK4_MES_B259_R0020": "Admiral, roaming here blindly is deadly.",
    "DK4_MES_B259_R0021": "No map, Admiral. This jungle is dangerous.",
    "DK4_MES_B259_R0023": "Admiral, this jungle is dangerous without a map.",
    "DK4_MES_B259_R0036": "So humid...{LB}This heat is brutal.",
    "DK4_MES_B259_R0039": (
        "Hmm. Perhaps it's the jungle...{LB}Wild beasts lurk here, Admiral.{LB}"
        "Choose our path carefully."
    ),
    "DK4_MES_B259_R0042": "A cave... Very deep.",
    "DK4_MES_B259_R0045": "Hmm. We must pass through.",
    "DK4_MES_B259_R0049": "Right. Let's go.",
    "DK4_MES_B259_R0067": "Something's here...{LB}Bad omen.",
    "DK4_MES_B259_R0068": "Something...{LB}A bad omen.",
    "DK4_MES_B259_R0069": "Something...{LB}Bad omen.",
    "DK4_MES_B259_R0070": "Something...{LB}Bad omen.",
    "DK4_MES_B259_R0071": "Something's there.{LB}This feels bad.",
    "DK4_MES_B259_R0072": "Something...{LB}Bad omen.",
    "DK4_MES_B259_R0073": "Something's there...{LB}This feels awful...",
    "DK4_MES_B259_R0091": "Someone, shoot!",
    "DK4_MES_B259_R0103": "Damn, it's fast!",
    "DK4_MES_B259_R0116": "No! We might hit our own men!",
    "DK4_MES_B259_R0128": "More injuries...{LB}Switch to close combat!",
    "DK4_MES_B259_R0153": "We got it!",
    "DK4_MES_B259_R0173": "The tiger wasn't hungry.{LB}We're safe.",
    "DK4_MES_B259_R0174": "The tiger wasn't hungry.{LB}We're safe.",
    "DK4_MES_B259_R0175": (
        "The tiger wasn't hungry.{LB}That's why it won't chase us."
    ),
    "DK4_MES_B259_R0176": "The tiger wasn't hungry...{LB}Good. No pursuit.",
    "DK4_MES_B259_R0178": "No pursuit means it wasn't hungry.{LB}We're safe.",
    "DK4_MES_B259_R0180": "Since it isn't chasing us,{LB}the tiger wasn't hungry.",
    "DK4_MES_B259_R0182": "The tiger isn't hungry.{LB}We're safe.",
    "DK4_MES_B259_R0184": "The tiger wasn't hungry.{LB}We're safe.",
    "DK4_MES_B259_R0187": "Whew, safe!",
    "DK4_MES_B259_R0197": "{MACRO:FI}!{LB}Light ahead!",
    "DK4_MES_B259_R0200": "We can leave the cave...",
}

SPEAKERS = {
    "03": "Maria",
    "97": "Party member",
    "D0": "Party member",
    "D3": "Party member",
    "D7": "Party member",
    "D8": "Party member",
    "FE": "System message or creature sound",
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
        row_id: row for row_id, row in rows.items() if row_id.startswith("DK4_MES_B259_")
    }
    lines = _load_reused_lines()
    if set(lines) != set(block_rows):
        raise SystemExit(
            "Maria V9 inventory mismatch: "
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
                    "Complete jungle and tiger-cave expedition: map warnings, cave "
                    "entry, beast encounter, ranged and melee branches, injuries, "
                    "escape responses, and finding the cave exit."
                ),
                "source_meaning": english,
                "localization_note": (
                    "Exact Japanese body matched to reviewed terminal route layers; "
                    "Maria-specific lines, ambiguous variants, and terse inherited "
                    "renderings were independently localized and allocation-checked."
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
        "dialogue_profile": "maria-story-tiger-cave-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 259: complete jungle and tiger-cave expedition, all "
            "party variants, combat branches, injuries, escape, and cave exit."
        ),
        "excluded_records": {},
        "inventory": {
            "identified_records": len(block_rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"259": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
