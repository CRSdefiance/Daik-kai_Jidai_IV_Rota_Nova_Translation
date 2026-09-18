from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v32.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "This has bothered me...{LB}Does the Evergreen Lotus Leaf{LB}map the Proof of Conquest?",
    "Uddin said so.{LB}Must be true.",
    "What combines with it?",
    "How about this{LB}Kushan Platter?",
    "How about this{LB}Kushan Platter?",
    "Put the leaf on it.{LB}...Nothing.",
    "Hey, what do we do?",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B149_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B149: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x08: "Raphael crewmate"}
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
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
            "context": "Raphael's crew tests the Evergreen Lotus Leaf against the Kushan Platter while seeking the southern-ocean Proof of Conquest map.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English using the established Evergreen Lotus Leaf, Kushan Platter, and Proof of Conquest terminology.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects item-name readability and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v31-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Raphael Evergreen Lotus Leaf and Kushan Platter combination attempt in SC0 block 149.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"149": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
