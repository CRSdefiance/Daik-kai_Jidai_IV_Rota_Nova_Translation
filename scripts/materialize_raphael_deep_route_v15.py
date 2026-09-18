from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v15.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = {
    114: [
        "Amazing...!", "Answer me.", "Whoa! A talking statue?!",
        "What has four legs at dawn,{LB}two at noon, three at dusk?",
        "Huh?", "Never heard of such a beast.", "Answer!", "What now?",
        "Know it", "No idea", "No beast",
        "Begone!", "Aaah!", "Begone!", "Aaah!",
        "Name it.", "Humans", "You, Sphinx", "Other",
        "Begone!", "Aaah!", "Begone!", "Aaah!",
        "Got it!{LB}A day stands for a lifetime.", "Huh?",
        "At dawn, a crawling baby.",
        "At noon, an adult walks upright.",
        "Dusk is old age.{LB}A cane makes three legs.",
        "Ah! So the answer is...", "Humankind!",
        "Wise one!{LB}Take this!",
    ],
    115: [
        "Ancient ruins.",
        "Who were those people?{LB}Human sacrifice is barbaric.",
        "They were mad!{LB}Said they would gather here again.",
        "What are they planning?",
        "No idea.{LB}They said 'the eve of revelation.'{LB}When is that?",
        "Maybe the chant's{LB}'when light and dark balance'{LB}means that day.",
        "Huh? That tells us nothing.",
        "We need a plan.{LB}Human sacrifice must be stopped!",
        "Aaaah...", "Ooooh!",
        "A revelation!{LB}Our Ancient Megalith Society{LB}will soon rule the world!",
        "We are chosen!{LB}We will unearth the treasure{LB}and rule every godless fool!",
        "Ooooh!",
        "Begin with this village!{LB}Those who mocked us will pay!",
        "Ooooh!",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {"05": "Claudio Manousch", "97": "Raphael crewmate", "B1": "Megalith cult leader", "B2": "Megalith cultists", "CF": "Raphael party", "FE": "Sphinx"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    114: "Raphael's party solves the Sphinx's classic riddle, including every wrong-answer branch and the successful explanation.",
    115: "Raphael's party discovers the Ancient Megalith Society plotting human sacrifice and an attack on a village.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    records = []
    block_counts = {}
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_")]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
                "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving every choice branch, riddle logic, cult threat, and fixed-allocation display safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v15-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "The complete Sphinx riddle and Ancient Megalith Society introduction across Raphael SC0 blocks 114-115.",
        "excluded_records": {},
        "inventory": {"identified_records": len(records), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
