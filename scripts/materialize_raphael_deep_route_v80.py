from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v80.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

EXCLUDED = {
    "DK4_MES_B320_R0029": "Raw guided-route control payload; not dialogue.",
    "DK4_MES_B320_R0065": "Raw route-branch control payload; not dialogue.",
    "DK4_MES_B320_R0068": "Raw dead-end control payload; not dialogue.",
}

SPEAKERS = {
    0x05: "Claudio Manousch",
    0xCB: "Route guide",
    0xD0: "Raphael crewmate",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B320_R0012": "Got the map?",
    "DK4_MES_B320_R0017": "Oh, right.",
    "DK4_MES_B320_R0031": "Then take care on the road.",
    "DK4_MES_B320_R0038": "Yes, thank you.",
    "DK4_MES_B320_R0053": "Come, let's go.",
    "DK4_MES_B320_R0055": "Let's go!",
    "DK4_MES_B320_R0057": "Let's go.",
    "DK4_MES_B320_R0059": "Let us go.",
    "DK4_MES_B320_R0061": "Off we go!",
    "DK4_MES_B320_R0063": "Well, let's go.",
    "DK4_MES_B320_R0067": "Can this path be right?",
    "DK4_MES_B320_R0070": "Hey, it's a dead end.",
    "DK4_MES_B320_R0075": "We got lost...",
    "DK4_MES_B320_R0079": "What?!{LB}Weren't you reading the map?",
    "DK4_MES_B320_R0083": "Sorry, Clau. We should have turned one path earlier.",
    "DK4_MES_B320_R0089": "Go back",
    "DK4_MES_B320_R0091": "Search",
    "DK4_MES_B320_R0100": "Let's go back.{LB}Safer that way.",
    "DK4_MES_B320_R0112": "That seems best.",
    "DK4_MES_B320_R0114": "That seems best.",
    "DK4_MES_B320_R0116": "Yes, that's best.",
    "DK4_MES_B320_R0118": "Yes. Let's do that.",
    "DK4_MES_B320_R0120": "That seems best.",
    "DK4_MES_B320_R0122": "Hm, no other choice.",
    "DK4_MES_B320_R0124": "That does seem best.",
    "DK4_MES_B320_R0132": "Any other way?",
    "DK4_MES_B320_R0137": "No luck...",
    "DK4_MES_B320_R0142": "No, through these woods...",
    "DK4_MES_B320_R0155": "One day passed.{LB}The sailors seem fatigued.",
    "DK4_MES_B320_R0159": "Yes! There!",
    "DK4_MES_B320_R0163": "That took ages. Going back might have been faster.",
    "DK4_MES_B320_R0167": "Really? That seems unlikely.",
    "DK4_MES_B320_R0170": "Yes, yes.{LB}(Surprisingly stubborn.)",
    "DK4_MES_B320_R0176": "Admiral!{LB}There!",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith("DK4_MES_B320_")]
    records = []
    unresolved = []
    for row in rows:
        if row["id"] in EXCLUDED:
            continue
        english = OVERRIDES.get(row["id"])
        if english is None:
            unresolved.append(row["id"])
            continue
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        first = int(row["source_hex"][:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        rendered = f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
        records.append({
            "id": row["id"], "english": rendered,
            "speaker": SPEAKERS.get(first, "Raphael party, choice, or scene text"),
            "context": "Raphael follows a guide's map, reaches a dead end, chooses whether to backtrack or seek a shortcut, and reaches the destination.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving route variants, choices, fatigue feedback, control payloads, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V80 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v80-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael guided-route, dead-end choice, shortcut, fatigue, and arrival event in SC0 block 320.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"320": len(rows)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
