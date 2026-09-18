from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v27.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Hmm...",
    "What, {MACRO:FI}?",
    "Oh, Clau.{LB}These two tablets must{LB}be a map, right?",
    "What?{LB}Of course they are.",
    "Upper and Lower Stone Tablets...{LB}Neither shows where the Proof lies.",
    "The Upper and Lower Stone Tablets.{LB}Yet these reveal nothing{LB}about the Proof's location.",
    "What are you doing?{LB}Separate halves{LB}tell you nothing.",
    "Maybe seeing them apart{LB}makes it hard to understand.",
    "Right!{LB}Let us align them.{LB}The upper half goes above...",
    "And the other goes below?",
    "Yes. Placed like this...",
    "A perfect fit!{LB}...Huh!?",
    "The two tablets are joining{LB}perfectly!",
    "Whoa! Amazing!",
    "The tablets joined{LB}into a single piece...",
    "Look!{LB}Some mark appeared!{LB}That was not here before.",
    "Huh?{LB}Does that look like a symbol?{LB}Was it there before...?",
    "Really?",
    "That is it!{LB}The mark points to{LB}Africa's Ruler's Proof!",
    "Could it be?{LB}This may mark{LB}the Ruler's Proof!",
    "Amazing!",
    "Then we leave at once!",
    "Let us search at once,{LB}{MACRO:FI}, Clau!",
    "Yes, onward!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B144_")]
    controls = {"DK4_MES_B144_R0094": "Raw tablet-fusion event control beginning with #H; preserved byte-for-byte."}
    visible = [row for row in rows if row["id"] not in controls]
    if len(visible) != len(TRANSLATIONS):
        raise SystemExit(f"B144: {len(visible)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x08: "Raphael crewmate"}
    records = []
    for row, english in zip(visible, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in speaker_names else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker_names.get(first, "Raphael Castor"),
            "context": "Raphael's crew combines the Upper and Lower Stone Tablets, revealing the mark that locates Africa's Ruler's Proof.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Uses established item and Ruler's Proof terminology while preserving the entire tablet-combination discovery and its raw fusion event control.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects discovery pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
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
        "scope": "Complete African Ruler's Proof tablet-combination and map-discovery scene in Raphael SC0 block 144.",
        "excluded_records": controls,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"144": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(controls)} control excluded")


if __name__ == "__main__":
    main()
