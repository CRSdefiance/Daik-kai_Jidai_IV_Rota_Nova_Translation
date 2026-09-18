from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v16.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {
    "DK4_MES_B116_R0003": "Raw event-control payload; not dialogue.",
    "DK4_MES_B116_R0036": "Raw event-control payload; not dialogue.",
    "DK4_MES_B116_R0087": "Raw event-control payload; not dialogue.",
}
TRANSLATIONS = {
    116: [
        "Hm?! Someone!",
        "Never thought people would come...",
        "Um... who are you?",
        "This ruin's guardian.",
        "What is this place?",
        "King Suryavarman the Second{LB}built this temple to unite with Vishnu{LB}and become god.",
        "Surya...? Vish...?{LB}Bah, none of that makes sense!",
        "Those who know not the Vedas{LB}may not approach.{LB}Leave.",
        "How can we earn his approval?{LB}And what are the Vedas?",
        "Myths behind Hinduism,{LB}the faith of this region... perhaps.",
        "Vishnu is a Hindu god, correct?",
        "Oh, well informed.",
        "...Hm?{LB}What is that?!",
        "The first Vedic scriptures!{LB}Who are you people?!",
        "Ah... now understood.{LB}At last you have appeared,{LB}and such a young boy.",
        "Very well.{LB}This is entrusted to you.",
        "An old coin?{LB}What is it?",
        "My duty is done.{LB}Unravel the rest yourselves.{LB}Now go.",
        "What did he mean?",
    ],
    117: [
        "Who are you?{LB}Could it be?",
        "Ah! Another believer at last!",
        "We fled Muslim rule{LB}and have lived quietly{LB}to preserve our faith.",
        "May we ask?{LB}Do you know the treasure gained{LB}by one who conquers the seven seas?",
        "You seek the Proof?{LB}God guided you here!",
        "Huh? You know of it?",
        "Know of it...?",
        "This lamp has been kept here{LB}since ancient times.{LB}Any seeker of the Proof needs it.{LB}Please take it.",
        "Please...{LB}Do not let the Proof fall{LB}into Ottoman hands.",
        "Understood.{LB}We will find it.",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {"05": "Claudio Manousch", "08": "Charles Jean Rochefort", "87": "Angkor guardian", "A0": "Hidden Christian"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    116: "At Angkor Wat, Raphael's party meets its guardian, identifies the Vedas, and receives an ancient coin tied to the Proof of Conquest.",
    117: "Hidden Christians explain their flight from Ottoman rule and entrust Raphael with an ancient lamp needed to seek the Proof of Conquest.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    inventory = {row["id"] for row in rows if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    records = []
    block_counts = {}
    translated_ids = set()
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            translated_ids.add(row["id"])
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"), "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving religious lore, Proof-of-Conquest clues, and fixed-allocation display safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    if translated_ids | set(EXCLUDED) != inventory:
        raise SystemExit("Raphael V16 inventory accounting mismatch")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v16-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Angkor Wat's Vedas guardian and the hidden-Christian lamp lead across Raphael SC0 blocks 116-117.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
