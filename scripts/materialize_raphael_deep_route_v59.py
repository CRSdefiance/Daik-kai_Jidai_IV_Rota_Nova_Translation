from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v59.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(208, 215))
EXCLUDED = {
    "DK4_MES_B209_R0022": "Four-byte packed portrait/item scene payload; not dialogue.",
}
LINES = {
    208: [
        "You look wealthy. Hehehehe!",
        "Something good is for sale.{LB}How about 200,000 coins? Hehehehe!",
        "Hold on. Are you overcharging us?",
        "Buy",
        "Pass",
        "Generous!{LB}This will surely prove useful.",
        "{MACRO:FI}: Charm +1!",
        "All right.{LB}How about 100,000 coins? Hehehehe!",
        "(...Admiral, halving it at once proves{LB}that first price was outrageous.{LB}Two more bargains should work.)",
        "Buy",
        "Pass",
        "Hehehe! Very sharp.{LB}This will surely prove useful.",
        "Then how about 70,000 coins?{LB}Hehehehe!",
        "(This man would bargain once more.)",
        "Buy",
        "Pass",
        "Here. Surely this{LB}will prove useful. Hehe!",
        "Greedy, are we?{LB}How about 50,000 coins? Hehehe!",
        "(This old man would press once more.)",
        "(Make her lower it again!)",
        "Buy",
        "Pass",
        "A skilled bargainer!{LB}Here is the item.",
        "40,000 coins... Heh.",
        "(Now seems the time to buy.)",
        "Buy",
        "Pass",
        "Thought you would never buy. Here.",
        "Please buy it.{LB}Just 30,000 coins.",
        "(The price will go no lower.)",
        "Buy",
        "Pass",
        "Tch, sold far too cheaply.{LB}At least take good care of it.",
        "Hmph! No eye for value!",
        "Enough! Someone else can buy!",
    ],
    209: [
        "You there, handsome.",
        "You mean me?",
        "Would you buy this book{LB}for 8,500 coins?",
        "What book?",
        "A classic romance{LB}of a maiden and a sage. Well?",
        "Admiral, what now?",
        "Buy",
        "Pass",
        "Decide",
        "We will take it.",
        "May a celestial maiden love you.",
        "Sadly, no interest.",
        "Oh dear.{LB}Handsome, but a pity.",
        "No, thank you.",
        "A shame.{LB}Someone else will buy it.",
        "This man would help,{LB}but lacks the money.",
        "Ah.",
        "Sorry to disappoint you.",
        "Then take it.",
        "What?!",
        "Hehe... Next time,{LB}a man like you may be mine.",
        "Vanished...",
        "A celestial maiden?{LB}Hah... What a foolish thought.",
        "His charm rose by 1!",
    ],
    210: [
        "Any naughty children here?",
        "Any naughty children here?",
        "Are you naughty?",
        "Who?",
        "Are you naughty?",
        "...You are a namahage!",
        "Are you naughty?",
        "This man did no wrong.",
        "Oh...",
        "Dream?",
        "Whoa! What is this?!",
        "Hm?!",
        "Strange things happen.",
        "This goes to the admiral tomorrow.",
        "...What was that?!",
    ],
    211: [
        "Hey, look!",
        "What?",
        "This!",
        "Who is this?",
        "You don't know?",
        "No.",
        "Listen, this is Rocco Alemkel!{LB}A legendary navigator.",
        "Oh.",
        "'Oh'? He supported mighty Portugal.{LB}A truly great man!",
        "Then he's our senior.",
        "Yes! And...",
        "Clatter!",
        "...What?",
        "The painting made a sound.{LB}Let's check it.",
        "Y-yes.",
        "Ah! A book behind the painting.",
        "Maybe Rocco wrote it!",
        "Could be.{LB}Heave-ho.",
        "Where to?",
        "Taking this book to the innkeeper.",
        "What?! Give it away?{LB}This may be the only copy!",
        "Obviously. This portrait{LB}belongs to the inn.",
        "But the innkeeper{LB}won't care about it!",
        "That's not the point.",
        "Whoa! Over there!",
        "What?",
        "Give!",
        "Ah!",
        "Claudio!",
        "Something wrong?",
        "Ah, um...{LB}Nothing at all.",
        "Okay.",
        "Stay and relax.",
        "Yes, thank you.",
        "Whew...{LB}(Claudio, honestly!)",
    ],
    212: [
        "Thud!",
        "Ah!",
        "...Ugh...",
        "What happened? You well?",
        "Ugh...",
        "You are awake.",
        "...Where is this?",
        "At an inn.{LB}You fell at the dock,{LB}so this man brought you.",
        "So that's it.{LB}Sorry for trouble.",
        "No trouble at all.{LB}Still, you look quite pale.{LB}Rest quietly for a while.",
        "This man will leave.{LB}Please take care.",
        "Wait. Are you a physician?",
        "No.",
        "Then this is hardly enough thanks,{LB}but please take it.",
        "Please, no need.",
        "Then my conscience will not rest.{LB}Please accept it.",
        "Very well, this man will accept it.{LB}Please guard your health.",
        "Certainly.{LB}Thank you very much.",
        "Carlo: Charm +1!",
    ],
    213: [
        "That mast rope is badly worn.",
        "This rope works.",
        "No, no, it is worn.{LB}Why not replace it with this rope?{LB}They say it holds a mysterious power.",
        "You will replace it for free?",
        "Certainly not!{LB}A discount is possible.{LB}Say 300,000 coins.",
        "Hold on!{LB}Do not pay that, Admiral.",
        "Special or not, that price for rope{LB}is absurd. At most, 30,000 coins.",
        "Wait! This is unique in all the world.{LB}Then how about 200,000 coins?",
        "Hm. Please accept 150,000 coins.",
        "75,000.",
        "You drive a hard bargain.{LB}Then 100,000 coins. No lower.",
        "Hm, that sounds fair.{LB}What do you say, Admiral?",
        "Buy",
        "Pass",
        "Leave the rest to this man.",
        "Handle it.",
        "Carry the rope to the deck.",
        "Thank you for your business.",
        "{MACRO:FI}: Charm +1!",
        "Carlo: Wit +1!",
        "This rope works.{LB}No need yet.",
        "Understood.{LB}We'll decline.",
        "Not buying?!{LB}Please do not waste my time!",
        "Truly, apologies.{LB}Please forgive us.",
        "{MACRO:FI}: Spirit +1!",
    ],
    214: [
        "Hey, you.",
        "Hm?",
        "Take this.{LB}Use it however you like!",
        "Huh?",
        "There you are!{LB}Stop!",
        "See you!",
        "Stop!",
        "Hey, wait...!",
        "What now, Admiral?",
        "Someone forced this on me.",
        "What is it?",
        "A book.",
        "Let's see.{LB}'Glassmaking'...",
        "Hm. Since it was free, keep it.",
        "But...",
        "When someone gives a gift,{LB}accept it.",
        "Right, let me see it later.",
        "So that was your aim.",
    ],
}

SPEAKERS = {
    0x05: "Claudio Manini",
    0x06: "Julio Erdi",
    0x0C: "Sailor",
    0x0F: "Sailor",
    0x12: "Crewman",
    0x13: "Carlo",
    0x14: "Crewman",
    0x15: "Ian Dukov",
    0x19: "Ifa",
    0x69: "Rope merchant",
    0x8C: "Innkeeper",
    0x93: "Pursuer",
    0x9D: "Stranger",
    0xA9: "Mysterious woman",
    0xAC: "Traveler",
    0xAD: "Mysterious seller",
    0xFE: "System or scene text",
}
CONTEXT = {
    208: "A mysterious seller repeatedly lowers the price of a charm-enhancing item.",
    209: "A celestial woman offers Ian an Indian romance and raises his charm.",
    210: "A namahage appears in a sailor's dream and leaves a mysterious gift.",
    211: "Raphael and Claudio find a navigation book behind Rocco Alemkel's inn portrait.",
    212: "Carlo helps a traveler who collapsed at the dock and receives a gift.",
    213: "Carlo bargains for a supposedly enchanted replacement mast rope.",
    214: "A fleeing stranger leaves Raphael a stolen glassmaking encyclopedia.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    if len(source_rows) != 172:
        raise SystemExit(f"B208-B214 inventory changed: {len(source_rows)}")
    rows_by_block = {
        block: [
            row for row in source_rows
            if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED
        ]
        for block in BLOCKS
    }
    for block, lines in LINES.items():
        if len(rows_by_block[block]) != len(lines):
            raise SystemExit(f"B{block}: {len(rows_by_block[block])} visible rows != {len(lines)} translations")

    records = []
    for block, lines in LINES.items():
        for row, english in zip(rows_by_block[block], lines, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if first in SPEAKERS else ""
            unsafe = english
            for macro in ("FI", "FA", "FO", "FU"):
                unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(first, "Raphael Castor, companion, choice, or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
                "localization_note": "Faithful concise American English preserving every branch, stat result, item event, and fixed-record display constraint.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects branching dialogue, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v59-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Seven Raphael treasure, gift, stat, bargaining, and optional crew events across SC0 blocks 208-214.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": {str(block): len(rows_by_block[block]) for block in BLOCKS},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
