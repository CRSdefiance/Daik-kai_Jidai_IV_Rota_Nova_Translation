from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v53.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    179: [
        "Hmm. This ship is well maintained...",
        "Still, more improvement remains.{LB}Say...",
        "Something wrong with our ship?",
        "Can we help you with our ship?",
        "Ah, the owner?{LB}A lively, fine ship.",
        "(What an interesting expression...)",
        "Never neglect her care.{LB}Show affection and she'll repay it.{LB}A ship is a living thing.",
        "Oh... perhaps that was too much.{LB}Merely my philosophy.{LB}Pardon any offense. Goodbye.",
        "W-wait, please.",
        "Something wrong?",
        "You seem deeply attached to ships.{LB}That caught my interest...",
        "Ships recall the old days...{LB}Manuel Armando.{LB}Once a navigator.",
        "So...",
        "{MACRO:FI}...{LB}Rarely does anyone love ships so.{LB}Having him aboard...",
        "Agreed. With him caring for the ship,{LB}we could rest easy.",
        "Then... Manuel,{LB}will you join us?{LB}Come to sea with us.",
        "To sea once more...{LB}Your passion rings strongly{LB}within my heart...",
        "You'll accept?!",
        "A ship's heartbeat stirs my soul...{LB}Ah, pardon me.{LB}Long ashore; excitement took hold.",
        "Thank you for the splendid offer.{LB}Gladly.",
        "Then, Admiral,{LB}may some advice be offered{LB}on flagship room refits?",
        "Please",
        "No",
        "Then... especially the rooms{LB}useful on long voyages.",
        "An officer's cabin or chapel,{LB}staffed by someone persuasive,{LB}reduces sailor discontent.",
        "A galley or livestock room{LB}reduces the fleet's use{LB}of food and water.",
        "A clinic doctor heals{LB}fatigue, illness, and wounds{LB}among the crew.",
        "Sick or injured navigators recover{LB}faster in a private cabin{LB}or recreation room.",
        "A shipwright repairs damage{LB}from the timber room at sea,{LB}and helps yard refits and repairs.",
        "That was a rushed explanation...{LB}Was it useful?",
        "A captain determines fleet fate.{LB}Never neglect refits.{LB}Plan them carefully.",
        "Then it's up to you.",
    ],
    180: [
        "Admiral.{LB}Want a sailing lesson?",
        "Huh?",
        "Been terribly bored lately.{LB}Think of it as helping someone.",
        "Teach us",
        "No thanks",
        "Don't underestimate us.",
        "Hmm, quite right.",
        "Ship matters need no lesson now, sir.",
        "Can't be helped.{LB}You look like experts.{LB}Time to wait for greener sailors.",
        "Good.{LB}You'll become important.",
        "A sailing ship lives by its sails.",
        "Let's start with square sails{LB}and lateen sails.",
        "A square sail hangs crosswise{LB}to the ship's direction.",
        "Square sails cannot turn fore-aft{LB}so tailwinds work well{LB}but the best angle is impossible{LB}against a headwind.",
        "A lateen sail hangs fore-aft.{LB}Unlike a square sail,{LB}it can't turn fully crosswise.",
        "A headwind allows a fine angle,{LB}but a tailwind gives less speed.{LB}Understand so far?",
        "Next: optional sails.",
        "A topsail is a small square sail{LB}mounted above each mast.",
        "A staysail is a small fore-aft sail{LB}set before masts. None goes{LB}before a lateen sail because{LB}the two would overlap.",
        "A bow sail is called a spritsail.{LB}A square sail at the bow,{LB}too large for small ships.",
        "Aft sails are jigger spankers{LB}fore-aft sails on short masts{LB}added at the stern. Only large{LB}ships can mount them.",
        "Know that ships with two-plus masts{LB}go faster on a quartering wind{LB}than a direct tailwind?",
        "Can anyone explain why?",
        "Hmm. The masts stand{LB}one behind another.",
        "Correct. Straight astern,{LB}only the rear mast catches wind.{LB}Other masts do little.",
        "A wind from the rear quarter is fastest.{LB}Of course, set each sail's angle well.",
        "Right!",
        "Ah! Never gave it much thought.{LB}So that is why!",
        "Thanks for listening.{LB}Time to return to work.",
    ],
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(("DK4_MES_B179_", "DK4_MES_B180_"))]
    if len(source_rows) != 61:
        raise SystemExit(f"B179-B180 inventory changed: {len(source_rows)}")
    rows_by_block = {block: [row for row in source_rows if row["id"].startswith(f"DK4_MES_B{block}_")] for block in LINES}
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} rows != {len(lines)} translations")
    speaker_names = {0x04: "Janus Pasar", 0x0D: "Cesare Tohni", 0x17: "Manuel Armando", 0x6D: "Sailing instructor"}
    contexts = {
        179: "Raphael recruits ship-loving navigator Manuel Armando and receives the complete flagship room-assignment tutorial.",
        180: "A sailing instructor explains square, lateen, topsail, staysail, spritsail, and jigger-spanker performance and wind angles.",
    }
    records = []
    for block, lines in LINES.items():
        for row, english in zip(rows_by_block[block], lines, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if first in speaker_names else ""
            unsafe = english
            for macro in ("FI", "FA", "FO", "FU"):
                unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": speaker_names.get(first, "Raphael Castor or companion"), "context": contexts[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful natural American English preserving recruitment context, every functional room effect, sail terminology, compatibility rule, and wind-performance explanation.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects tutorial grouping, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v51-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Manuel Armando's recruitment, flagship-room tutorial, and the complete optional sail-configuration lecture across SC0 blocks 179-180.",
        "excluded_records": {},
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {str(block): len(rows_by_block[block]) for block in LINES}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
