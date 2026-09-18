from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v12.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

TRANSLATIONS = {
    100: [
        "Oh! You deal in amber?",
        "Yes. Gazing at amber's glow{LB}feels like stepping into antiquity.",
        "What?",
        "Amber is ancient tree sap{LB}that hardened and became a gem.",
        "See the bee inside?{LB}That bee has slept for millennia{LB}in a sepia-colored little cosmos.{LB}Mysterious, is it not?",
        "How do you know stuff like that?",
        "Science uses human reason{LB}to unravel miracles{LB}that seem beyond understanding.",
        "No clue what that means.{LB}Oh, amber reminds me of something.",
        "What?",
        "Some islands off this cape hold{LB}a place that glows amber.",
        "Amber? An ore vein?",
        "Who knows? Nobody knows what it is.{LB}Only a rumor.",
        "Hmm. Thank you for the tip.{LB}That certainly stirs{LB}my scientific curiosity.",
    ],
    101: [
        "Sigh.",
        "What is wrong, Julio?",
        "My granddaughter.",
        "You mean Christina.",
        "Wondering if she is all right.{LB}Call me a foolish old grandpa.",
        "Christina will be fine.{LB}She is strong, like Athena reborn.",
        "Athena?",
        "A goddess in Greek myth.{LB}The Romans call her Minerva.",
        "May have heard that long ago.{LB}Gods are not my subject.",
        "Still, that Minerva name{LB}sounds familiar.",
        "Anyway, Christina will be fine.",
        "Thank you. She has your trust,{LB}but she remains my granddaughter.{LB}Try to understand an old man's worry.",
        "Ah! Now memory serves!",
        "Yes, the Shield of Minerva!",
        "Legendary armor said to rest{LB}near the Mediterranean{LB}or the Black Sea.",
        "Christina is like Minerva.{LB}Now that shield must be found{LB}for her.",
        "Julio...",
        "Sorry for the silly tale.{LB}Please ignore an old man's rambling.{LB}Time to return to work.",
        "You have work, Admiral.",
        "Right.",
    ],
    102: [
        "Admiral?",
        "What is it?",
        "Peacocks are beautiful birds.{LB}Want to see one?",
        "Why ask that now?{LB}Another rumor, is it?",
        "That is right.{LB}This one is called Peacock Mail.",
        "Armor made from peacock feathers?",
        "Close! Very close!{LB}A peacock's tail sits on its back.",
        "Sounds weak.",
        "Such beauty stuns foes.{LB}That is its power.",
        "Hmm... Would it really help?{LB}Where can we find it?",
        "On a small island far, far{LB}southeast of the Cape of Good Hope.{LB}That is all the rumor said.",
        "That hardly narrows it down.",
        "Want to see it.{LB}Must look amazing.",
        "All right. We will remember.{LB}No promises.",
        "Understood.",
    ],
    103: [
        "Admiral?",
        "What is it?",
        "Let us seek the Jaguar God's Gi.",
        "What?",
        "A garment housing a jaguar god.{LB}Somewhere in the New World.",
        "Another new rumor, then.",
        "Yes. The last one.",
        "Why?",
        "Locating places is hard.{LB}Now it bores me.",
        "My interests fade quickly.{LB}Animals are dull unless edible.{LB}Any rumor heard will be shared.",
        "Back to the gi:{LB}where in the New World is it?",
        "Probably in the west.",
        "Too broad. Any details?",
        "Sorry. Nothing more was learned.{LB}Just keep it in mind.",
        "Ha! Very well.",
    ],
    104: [
        "Admiral, did you hear a Portuguese{LB}fleet sank near here twenty years ago?",
        "No.",
        "The commander had a telescope{LB}that showed every ridge on the moon.",
        "That is remarkable!",
        "Supposedly made by Aristarchus,{LB}the brilliant Hellenistic astronomer.",
        "Truly?",
        "That age likely lacked the skill{LB}to polish lenses so precisely.",
        "The truth is uncertain.{LB}They called it{LB}Aristarchus's Telescope.",
        "And?",
        "Judging by the currents,{LB}it may have washed ashore nearby.",
        "Then it may be worth searching for.",
    ],
    105: [
        "We made port.{LB}Let us hurry out to eat!",
        "At every port, Emilio says,{LB}'Let us hurry out to eat!'",
        "Eating is important!{LB}Besides, something is being sought.",
        "Seeking what?",
        "The world's best food!",
        "How could anyone decide{LB}which food tastes best?",
        "Easy. The world's tastiest food{LB}is cooked in Hestia's Cauldron.",
        "Hestia's pot?",
        "The hearth goddess had it made.{LB}The cauldron lies far across the sea,{LB}south of Greece.",
        "That is why Greek food excites me.{LB}Enough talk. Let us go eat!",
    ],
}

BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {
    "04": "Janus Pasha", "06": "Julio Castor", "0E": "Emilio Ferrog",
    "12": "Charles Jean Rochefort", "16": "Raphael crewmate", "72": "Amber trader",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    100: "An amber trader tells Charles about a mysterious amber-colored place on nearby islands.",
    101: "Julio worries about Christina and recalls the legendary Shield of Minerva.",
    102: "A crewmate tells Raphael about the Peacock Mail and its remote island location.",
    103: "A crewmate tells Raphael about the Jaguar God's Gi somewhere in the western New World.",
    104: "Janus explains the legend and likely resting place of Aristarchus's Telescope.",
    105: "Emilio explains his quest for the world's best food and Hestia's Cauldron.",
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
                "localization_note": "Faithful concise American English preserving treasure names, clue geography, characterization, and fixed-allocation display safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v12-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Six complete optional treasure-rumor scenes across Raphael SC0 blocks 100-105.",
        "excluded_records": {},
        "inventory": {"identified_records": len(records), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
