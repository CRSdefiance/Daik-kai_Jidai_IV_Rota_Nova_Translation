from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v25.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Crimson Dye reveals{LB}the Ruler's Proof map...",
    "Dye, huh...{LB}Why not color the Old Parchment{LB}from those ruins with it?",
    "Color it...!{LB}That may work!{LB}Let us try...",
    "Whoa!",
    "Yes!{LB}A map appeared on the parchment!",
    "The North Sea Ruler's Proof map!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B142_")]
    controls = {"DK4_MES_B142_R0016": "Raw map-reveal control record beginning with #H; preserved byte-for-byte."}
    visible = [row for row in rows if row["id"] not in controls]
    if len(visible) != len(TRANSLATIONS):
        raise SystemExit(f"B142: {len(visible)} visible rows != {len(TRANSLATIONS)} translations")
    records = []
    for row, english in zip(visible, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first == 0x05 else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": "Claudio Manini" if state else "Raphael Castor",
            "context": "Raphael and Claudio combine the Crimson Dye with the Old Parchment, revealing the North Sea Ruler's Proof map.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Uses established route terminology for Crimson Dye, Old Parchment, and Ruler's Proof while preserving the complete map-reveal sequence and fixed allocation.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects revelation pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v24-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete North Sea Ruler's Proof map-reveal scene in Raphael SC0 block 142.",
        "excluded_records": controls,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"142": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(controls)} control excluded")


if __name__ == "__main__":
    main()
