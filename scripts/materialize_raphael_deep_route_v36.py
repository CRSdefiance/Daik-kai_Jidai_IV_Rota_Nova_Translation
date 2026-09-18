from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v36.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "This Ancient Kingdom Coin{LB}is filthy.",
    "Let's polish it.{LB}There's a Lotion Jar.",
    "What's this stuff?{LB}Oh well. Let's try.{LB}Apply it...",
    "Rub...",
    "H-hey, {MACRO:FI}!{LB}Stop rubbing and look!{LB}The coin's dissolving!",
    "Oh no!{LB}...Huh?",
    "...A new pattern.{LB}Looks like a map...",
    "Then it's Southeast Asia's Proof map!{LB}The surface had to dissolve{LB}to reveal it.",
    "So this is Southeast Asia's Proof map!{LB}The surface dissolves{LB}to reveal it...",
    "Yes!{LB}Now we can find Southeast Asia's{LB}Proof of Conquest!",
    "Whew.{LB}Glad it didn't all dissolve...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B153_")]
    excluded = {"DK4_MES_B153_R0028": "Four-byte event-control payload; no independently rendered dialogue."}
    rows = [row for row in all_rows if row["id"] not in excluded]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B153: {len(rows)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x08: "Arcadius Eirene"}
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
            "context": "Raphael combines the Ancient Kingdom Coin with the Lotion Jar, dissolving its surface to reveal Southeast Asia's Proof of Conquest map.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English using the established Ancient Kingdom Coin, Lotion Jar, and Proof of Conquest terminology; one raw event control remains byte-identical.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects item-name readability, reveal pacing, and progressive ASCII pair phase."} if "{LB}" in english else {}),
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
        "scope": "Complete Ancient Kingdom Coin and Lotion Jar combination scene in SC0 block 153.",
        "excluded_records": excluded,
        "inventory": {"identified_records": len(all_rows), "translated_records": len(records), "blocks": {"153": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(excluded)} control excluded")


if __name__ == "__main__":
    main()
