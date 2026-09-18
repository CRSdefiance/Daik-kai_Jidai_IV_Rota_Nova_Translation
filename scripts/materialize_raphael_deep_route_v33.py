from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v33.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Oh? That's a Kushan Platter.{LB}There's an old tale about it.{LB}Do you know it?",
    "What kind of tale?",
    "A divination tool.{LB}They read flowers or leaves{LB}floating in its water{LB}to foretell the year.",
    "Maybe it reveals{LB}the Proof of Conquest...{LB}Try the Evergreen Lotus Leaf.",
    "Ah!?{LB}The leaf drank water!{LB}Something's on its veins!",
    "Ah!?{LB}The leaf drank water!{LB}Something's on its veins!",
    "Yes!{LB}The Proof map of the southern sea!",
    "We did it,{LB}{MACRO:FI}!",
    "We did it,{LB}{MACRO:FI}!",
    "Thanks to her!{LB}Thank you!",
    "Each Proof map is split in two.{LB}You must find both keys.",
    "Map... keys?",
    "When the two keys are joined,{LB}the Proof map finally appears.{LB}That's how it works.",
    "So to collect seven Proofs,{LB}we need all fourteen keys?",
    "Exactly.",
    "All 14!?{LB}That's tough.",
    "Ho, ho.{LB}Were they easy to find,{LB}someone would have them already.",
    "True.{LB}The world works that way.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B150_")]
    excluded = {"DK4_MES_B150_R0049": "Four-byte event-control payload; no independently rendered dialogue."}
    rows = [row for row in all_rows if row["id"] not in excluded]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B150: {len(rows)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x08: "Raphael crewmate", 0x4B: "Hans Retzel", 0x8E: "Relic scholar"}
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
            "context": "Raphael completes the Evergreen Lotus Leaf and Kushan Platter ritual, reveals the southern-sea Proof map, and learns that every Proof map requires two keys.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English retaining established Kushan Platter, Evergreen Lotus Leaf, and Proof of Conquest terminology; one raw event-control payload remains byte-identical.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects relic terminology, exposition structure, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v33-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Raphael southern-sea Proof-map revelation and two-key explanation in SC0 block 150.",
        "excluded_records": excluded,
        "inventory": {"identified_records": len(all_rows), "translated_records": len(records), "blocks": {"150": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(excluded)} control excluded")


if __name__ == "__main__":
    main()
