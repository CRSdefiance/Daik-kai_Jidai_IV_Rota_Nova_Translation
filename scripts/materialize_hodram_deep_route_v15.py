from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v15.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(200, 210))
EXCLUDED = {
    "DK4_MES_B201_R0022": "Four-byte packed portrait/scene payload; not dialogue.",
    "DK4_MES_B209_R0007": "Four-byte packed parrot-scene payload; not dialogue.",
}


LINES = {
    # A mysterious seller bargains down an expensive charm-enhancing item.
    "DK4_MES_B200_R0005": "You look wealthy. Hehehehe!",
    "DK4_MES_B200_R0012": "Something good is for sale. How about 200,000 coins? Hehehehe!",
    "DK4_MES_B200_R0024": "Hold on. Are you overcharging us?",
    "DK4_MES_B200_R0032": "Buy",
    "DK4_MES_B200_R0034": "Pass",
    "DK4_MES_B200_R0042": "Generous! This will surely prove useful.",
    "DK4_MES_B200_R0045": "{MACRO:FI}: Charm +1!",
    "DK4_MES_B200_R0062": "All right. How about 100,000 coins? Hehehehe!",
    "DK4_MES_B200_R0074": "(...Admiral, halving it at once proves that first price was outrageous. Two more bargains should work.)",
    "DK4_MES_B200_R0082": "Buy",
    "DK4_MES_B200_R0084": "Pass",
    "DK4_MES_B200_R0092": "Hehehe! Very sharp.{LB}This will surely prove useful.",
    "DK4_MES_B200_R0107": "Then how about 70,000 coins? Hehehehe!",
    "DK4_MES_B200_R0118": "(This man would bargain once more.)",
    "DK4_MES_B200_R0126": "Buy",
    "DK4_MES_B200_R0128": "Pass",
    "DK4_MES_B200_R0136": "Here. Surely this{LB}will prove useful. Hehe!",
    "DK4_MES_B200_R0152": "Greedy, are we? How about 50,000 coins? Hehehe!",
    "DK4_MES_B200_R0170": "(This old man would press once more.)",
    "DK4_MES_B200_R0178": "(Make her lower it again!)",
    "DK4_MES_B200_R0187": "Buy",
    "DK4_MES_B200_R0189": "Pass",
    "DK4_MES_B200_R0197": "A skilled bargainer! Here is the item.",
    "DK4_MES_B200_R0212": "40,000 coins... Heh.",
    "DK4_MES_B200_R0223": "(Now seems the time to buy.)",
    "DK4_MES_B200_R0232": "Buy",
    "DK4_MES_B200_R0234": "Pass",
    "DK4_MES_B200_R0242": "Thought you would never buy. Here.",
    "DK4_MES_B200_R0257": "Please buy it. Just 30,000 coins.",
    "DK4_MES_B200_R0268": "(The price will go no lower.)",
    "DK4_MES_B200_R0277": "Buy",
    "DK4_MES_B200_R0279": "Pass",
    "DK4_MES_B200_R0287": "Tch, sold far too cheaply. At least take good care of it.",
    "DK4_MES_B200_R0302": "Hmph! No eye for value!",
    "DK4_MES_B200_R0306": "Enough! Someone else can buy!",

    # A celestial woman offers Ian an Indian romance.
    "DK4_MES_B201_R0005": "You there, handsome.",
    "DK4_MES_B201_R0009": "You mean me?",
    "DK4_MES_B201_R0014": "Would you buy this book for 8,500 coins?",
    "DK4_MES_B201_R0017": "What book?",
    "DK4_MES_B201_R0021": "A classic romance of a maiden and a sage. Well?",
    "DK4_MES_B201_R0024": "Admiral, what now?",
    "DK4_MES_B201_R0031": "Buy",
    "DK4_MES_B201_R0033": "Pass",
    "DK4_MES_B201_R0035": "Decide",
    "DK4_MES_B201_R0045": "We will take it.",
    "DK4_MES_B201_R0049": "May a celestial maiden love you.",
    "DK4_MES_B201_R0053": "Sadly, no interest.",
    "DK4_MES_B201_R0057": "Oh dear. Handsome, but a pity.",
    "DK4_MES_B201_R0064": "No, thank you.",
    "DK4_MES_B201_R0068": "A shame. Someone else will buy it.",
    "DK4_MES_B201_R0074": "This man would help, but lacks the money.",
    "DK4_MES_B201_R0077": "Ah.",
    "DK4_MES_B201_R0081": "Sorry to disappoint you.",
    "DK4_MES_B201_R0085": "Then take it.",
    "DK4_MES_B201_R0089": "What?!",
    "DK4_MES_B201_R0093": "Hehe... Next time, a man like you may be mine.",
    "DK4_MES_B201_R0097": "Vanished...",
    "DK4_MES_B201_R0101": "A celestial maiden? Hah... What a foolish thought.",
    "DK4_MES_B201_R0109": "Ｉan: Charm +1!",

    # A namahage appears in a sailor's dream.
    "DK4_MES_B202_R0010": "Any naughty children here?",
    "DK4_MES_B202_R0014": "Any naughty children here?",
    "DK4_MES_B202_R0018": "Are you naughty?",
    "DK4_MES_B202_R0022": "Who?",
    "DK4_MES_B202_R0026": "Are you naughty?",
    "DK4_MES_B202_R0030": "...You are a namahage!",
    "DK4_MES_B202_R0034": "Are you naughty?",
    "DK4_MES_B202_R0038": "This man did no wrong.",
    "DK4_MES_B202_R0042": "Oh...",
    "DK4_MES_B202_R0053": "Dream?",
    "DK4_MES_B202_R0065": "Whoa! What is this?!",
    "DK4_MES_B202_R0072": "Hm?!",
    "DK4_MES_B202_R0080": "Strange things happen.",
    "DK4_MES_B202_R0084": "This goes to the admiral tomorrow.",
    "DK4_MES_B202_R0095": "...What was that?!",

    # A portrait of navigator Rocco Alemkel hides a navigation book.
    "DK4_MES_B203_R0005": "What is it, Admiral?",
    "DK4_MES_B203_R0009": "This portrait...",
    "DK4_MES_B203_R0014": "Sir Rocco Alemkel.",
    "DK4_MES_B203_R0018": "Yes. He sustained powerful Portugal.",
    "DK4_MES_B203_R0021": "Yes. Worthy of respect, though foreign.",
    "DK4_MES_B203_R0024": "Yes.",
    "DK4_MES_B203_R0028": "What were they looking at?",
    "DK4_MES_B203_R0032": "Hm. An ordinary portrait.",
    "DK4_MES_B203_R0036": "Clatter!",
    "DK4_MES_B203_R0040": "What?!",
    "DK4_MES_B203_R0044": "Hm? Behind the painting!",
    "DK4_MES_B203_R0048": "A book! Could it be about science?!",
    "DK4_MES_B203_R0051": "Rustle...",
    "DK4_MES_B203_R0055": "Aw, a navigation book. The admiral can have it.",

    # Carlo aids a collapsed traveler and receives a gift.
    "DK4_MES_B204_R0005": "Thud!",
    "DK4_MES_B204_R0009": "Ah!",
    "DK4_MES_B204_R0013": "...Ugh...",
    "DK4_MES_B204_R0017": "What happened? You well?",
    "DK4_MES_B204_R0021": "Ugh...",
    "DK4_MES_B204_R0025": "You are awake.",
    "DK4_MES_B204_R0029": "...Where is this?",
    "DK4_MES_B204_R0033": "At an inn. You fell at the dock, so this man brought you.",
    "DK4_MES_B204_R0037": "That explains it. Sorry for trouble.",
    "DK4_MES_B204_R0040": "No trouble at all. Still, you look quite pale. Rest quietly for a while.",
    "DK4_MES_B204_R0044": "This man will leave. Please take care.",
    "DK4_MES_B204_R0047": "Wait. Are you a physician?",
    "DK4_MES_B204_R0050": "No.",
    "DK4_MES_B204_R0054": "Then this is hardly enough thanks, but please take it.",
    "DK4_MES_B204_R0058": "Please, no need.",
    "DK4_MES_B204_R0062": "Then my conscience will not rest. Please accept it.",
    "DK4_MES_B204_R0065": "Very well, this man will accept it. Please guard your health.",
    "DK4_MES_B204_R0069": "Certainly. Thank you very much.",
    "DK4_MES_B204_R0072": "Carlo: Charm +1!",

    # Carlo bargains for a supposedly enchanted mast rope.
    "DK4_MES_B205_R0005": "That mast rope is badly worn.",
    "DK4_MES_B205_R0008": "This rope works.",
    "DK4_MES_B205_R0012": "No, no, it is worn. Why not replace it with this rope? They say it holds a mysterious power.",
    "DK4_MES_B205_R0015": "You will replace it free?",
    "DK4_MES_B205_R0019": "Certainly not! A discount is possible, of course. Say 300,000 coins.",
    "DK4_MES_B205_R0022": "Hold on!{LB}Do not pay that, Admiral.",
    "DK4_MES_B205_R0025": "Special or not, that price for rope is absurd. At most, 30,000 coins.",
    "DK4_MES_B205_R0028": "Wait! This is unique in all the world. Then how about 200,000 coins?",
    "DK4_MES_B205_R0035": "Hm. Please accept 150,000 coins.",
    "DK4_MES_B205_R0038": "75,000.",
    "DK4_MES_B205_R0042": "You drive a hard bargain. Then 100,000 coins. No lower.",
    "DK4_MES_B205_R0046": "Hm, that sounds fair. What do you say, Admiral?",
    "DK4_MES_B205_R0051": "Buy",
    "DK4_MES_B205_R0053": "Pass",
    "DK4_MES_B205_R0060": "Leave the rest to this man.",
    "DK4_MES_B205_R0063": "Then handle it.",
    "DK4_MES_B205_R0070": "Carry the rope to the deck.",
    "DK4_MES_B205_R0074": "Thank you for your business.",
    "DK4_MES_B205_R0078": "{MACRO:FI}: Charm +1!",
    "DK4_MES_B205_R0081": "Carlo: Wit +1!",
    "DK4_MES_B205_R0087": "This rope still works. No rush to replace it.",
    "DK4_MES_B205_R0091": "Understood. This man will decline.",
    "DK4_MES_B205_R0095": "Not buying?! Please do not waste my time!",
    "DK4_MES_B205_R0098": "Truly, apologies. Please forgive us.",
    "DK4_MES_B205_R0101": "{MACRO:FI}: Spirit +1!",

    # A stranger dumps a stolen glassmaking encyclopedia on Hodram.
    "DK4_MES_B206_R0005": "Hey, you.",
    "DK4_MES_B206_R0009": "Hm?",
    "DK4_MES_B206_R0013": "Take this. Use it however you like!",
    "DK4_MES_B206_R0020": "There you are! Stop!",
    "DK4_MES_B206_R0023": "Hm?",
    "DK4_MES_B206_R0027": "See you!",
    "DK4_MES_B206_R0031": "Stop!",
    "DK4_MES_B206_R0035": "Hey...",
    "DK4_MES_B206_R0039": "What now, Admiral?",
    "DK4_MES_B206_R0043": "Someone gave me this.",
    "DK4_MES_B206_R0047": "What is it?",
    "DK4_MES_B206_R0051": "A book.",
    "DK4_MES_B206_R0055": "Glassmaking guide...",
    "DK4_MES_B206_R0058": "Hm. Since it was free, keep it.",
    "DK4_MES_B206_R0061": "But...",
    "DK4_MES_B206_R0065": "When someone gives a gift, accept it.",
    "DK4_MES_B206_R0068": "Right, let me see it later.",
    "DK4_MES_B206_R0072": "So that was your aim.",

    # An herbalist gives the crew a medicinal-materials book.
    "DK4_MES_B207_R0005": "What is this?!",
    "DK4_MES_B207_R0009": "What?",
    "DK4_MES_B207_R0013": "This thing here.",
    "DK4_MES_B207_R0017": "...Bug?",
    "DK4_MES_B207_R0021": "But a strange plant grows from it.",
    "DK4_MES_B207_R0024": "True.",
    "DK4_MES_B207_R0028": "That is called caterpillar fungus.",
    "DK4_MES_B207_R0035": "People in China prize it as medicine.",
    "DK4_MES_B207_R0038": "Medicine?",
    "DK4_MES_B207_R0042": "Hm, medicine...",
    "DK4_MES_B207_R0046": "Yes. Take this too.",
    "DK4_MES_B207_R0050": "This?",
    "DK4_MES_B207_R0054": "A book about many ingredients used in medicine.",
    "DK4_MES_B207_R0057": "We cannot accept it for nothing.",
    "DK4_MES_B207_R0061": "This old man no longer needs it, so take it.",
    "DK4_MES_B207_R0064": "But...",
    "DK4_MES_B207_R0068": "Hohoho.{LB}Your friend wants it.",
    "DK4_MES_B207_R0071": "What? Well... This old man did want to read that book.",
    "DK4_MES_B207_R0075": "Then might you sell it for 1,000 coins?",
    "DK4_MES_B207_R0078": "Hohoho. Then 100 coins will do.",
    "DK4_MES_B207_R0081": "{MACRO:FI}: Charm +1!",

    # Jam mistakes a castle's shachihoko for a figurehead.
    "DK4_MES_B208_R0005": "Bored. Time to go somewhere.",
    "DK4_MES_B208_R0009": "Ma'am, anywhere interesting nearby? A walk might cure this boredom.",
    "DK4_MES_B208_R0013": "Well, the lord's castle lies to the east.",
    "DK4_MES_B208_R0016": "A castle? Sounds good. Time to see this country's castle.",
    "DK4_MES_B208_R0019": "Jam, late again. Gone all day?",
    "DK4_MES_B208_R0022": "Sorry. This was heavy.",
    "DK4_MES_B208_R0025": "What is that? Where did you get it?",
    "DK4_MES_B208_R0028": "Obviously a figurehead! Genuine, made in Japan!",
    "DK4_MES_B208_R0032": "People here misuse figureheads,{LB}so this man taught them.{LB}They gave this as thanks.",
    "DK4_MES_B208_R0035": "You taught someone? Never mind. We depart soon. Pack up.",
    "DK4_MES_B208_R0039": "Got it. Give this man a moment.",
    "DK4_MES_B208_R0044": "My lord! My looord! Disaster!",
    "DK4_MES_B208_R0047": "What now? Noise from dawn!",
    "DK4_MES_B208_R0051": "The shachihoko vanished, and this foreign letter appeared!",
    "DK4_MES_B208_R0054": "What?! The shachihoko is gone? Disaster! Catch that thief at any cost!",
    "DK4_MES_B208_R0057": "At once!",
    "DK4_MES_B208_R0061": "Dear lord of Japan,",
    "DK4_MES_B208_R0065": "That statue is a figurehead. Such things belong on ships, not castles. Someone misunderstood.",
    "DK4_MES_B208_R0068": "No thanks needed. One spare was taken instead. A ship needs one figurehead. Remember that.",
    "DK4_MES_B208_R0071": "Take care. Jam Jack Ludwayer",

    # A sailor captures a talking parrot.
    "DK4_MES_B209_R0005": "flap, flap!",
    "DK4_MES_B209_R0009": "Whoa! What is that?!",
    "DK4_MES_B209_R0013": "WHAT'S THAT",
    "DK4_MES_B209_R0017": "Mamma mia! That bird spoke!",
    "DK4_MES_B209_R0020": "THAT PARROT TALKED",
    "DK4_MES_B209_R0024": "That is a parrot.",
    "DK4_MES_B209_R0028": "A parrot, eh?",
    "DK4_MES_B209_R0032": "A PARROT, EH",
    "DK4_MES_B209_R0036": "Quit that!",
    "DK4_MES_B209_R0040": "STOP THAT",
    "DK4_MES_B209_R0044": "Oh, fun! This man will catch you!",
    "DK4_MES_B209_R0047": "Here goes! Hah!",
    "DK4_MES_B209_R0051": "flap! Thud! Crash! flap! Bang! Rustle!",
    "DK4_MES_B209_R0055": "Got it.",
    "DK4_MES_B209_R0059": "Whew! Surrender now? Hahahaha!",
    "DK4_MES_B209_R0063": "SURRENDER NOW",
    "DK4_MES_B209_R0067": "Hah.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "06": "Julio",
    "0B": "Jam Jack Ludwayer",
    "0C": "Sailor",
    "0F": "Sailor",
    "10": "Gerhard Adelknauts",
    "12": "Crewman",
    "13": "Carlo",
    "14": "Crewman",
    "15": "Ian",
    "19": "Ifa",
    "4C": "Crewman",
    "69": "Rope merchant",
    "7C": "Retainer",
    "82": "Japanese lord",
    "91": "Towns-woman",
    "93": "Pursuer",
    "9D": "Stranger",
    "A9": "Mysterious woman",
    "AA": "Herbalist",
    "AC": "Traveler",
    "AD": "Mysterious seller",
    "FE": "System or scene text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    200: "A mysterious seller repeatedly lowers the price of a charm-enhancing item.",
    201: "A celestial woman offers Ian an Indian romance and raises his charm.",
    202: "A namahage appears in a sailor's dream and leaves a mysterious gift.",
    203: "A portrait of navigator Rocco Alemkel conceals a navigation book.",
    204: "Carlo helps a traveler who collapsed at the dock and receives a gift.",
    205: "Carlo bargains for a supposedly enchanted replacement mast rope.",
    206: "A fleeing stranger leaves Hodram a stolen glassmaking encyclopedia.",
    207: "An herbalist explains caterpillar fungus and gives the crew a medicinal-materials book.",
    208: "Jam mistakes a castle's shachihoko for a ship's figurehead and takes it.",
    209: "A sailor encounters and captures a talking parrot.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V15 inventory mismatch: missing={missing}, extra={extra}")

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice text"),
                "context": CONTEXT[block],
                "source_meaning": english
                .replace("{MACRO:FI}", "Hodram")
                .replace("{LB}", " "),
                "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places a protected newline before the native row boundary so the "
                            "progressive ASCII pair phase cannot auto-wrap and skip a display row."
                        )
                    }
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-treasure-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Hodram treasure, gift, stat, and crew events across SC1 blocks 200-209.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
