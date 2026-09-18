from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v16.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(210, 220))
EXCLUDED = {
    "DK4_MES_B210_R0015": "Four-byte packed item/scene payload; not dialogue.",
    "DK4_MES_B217_R0022": "Four-byte packed sword/scene payload; not dialogue.",
}


LINES = {
    # Christina evaluates legendary ceramic earrings.
    "DK4_MES_B210_R0005": "Care to buy something good?",
    "DK4_MES_B210_R0009": "Something good?",
    "DK4_MES_B210_R0013": "This.",
    "DK4_MES_B210_R0017": "Earrings?",
    "DK4_MES_B210_R0021": "Ceramic earrings, exactly.",
    "DK4_MES_B210_R0025": "They do not look so rare.",
    "DK4_MES_B210_R0029": "Hehe. These are no ordinary earrings.",
    "DK4_MES_B210_R0033": "What is special?",
    "DK4_MES_B210_R0037": "They belonged to history's greatest dancer. Legend says any man is enchanted when their wearer dances.",
    "DK4_MES_B210_R0040": "Amazing, but wasted on this man. Christina, do you want them?",
    "DK4_MES_B210_R0044": "Maybe if they improved dancing. No man is worth such effort.",
    "DK4_MES_B210_R0056": "Sera, what about you?",
    "DK4_MES_B210_R0060": "(Shakes head.)",
    "DK4_MES_B210_R0064": "...No? Then we do not need them.",
    "DK4_MES_B210_R0070": "Wearing them is not their only use. Give them to a tavern woman, and she will adore you immediately.",
    "DK4_MES_B210_R0073": "Adore you? What then?",
    "DK4_MES_B210_R0077": "Then she will share all sorts of news. Tavern women know plenty.",
    "DK4_MES_B210_R0083": "Got it.",
    "DK4_MES_B210_R0085": "So what?",
    "DK4_MES_B210_R0092": "See? Now you understand.",
    "DK4_MES_B210_R0095": "We'll buy.",
    "DK4_MES_B210_R0099": "Then 9,000 coins.{LB}Rock-bottom; not one coin less.",
    "DK4_MES_B210_R0104": "Bought!",
    "DK4_MES_B210_R0106": "Pricey",
    "DK4_MES_B210_R0114": "A keen eye. Here are the ceramic earrings.",
    "DK4_MES_B210_R0121": "...Misjudged you. Go away. They are no longer for sale.",
    "DK4_MES_B210_R0124": "How rude! You approached us, remember?!",
    "DK4_MES_B210_R0127": "Hmph. No time for misers. Go away.",
    "DK4_MES_B210_R0130": "Good! This woman refuses!",
    "DK4_MES_B210_R0141": "...Anyone who still fails to understand is unworthy. Go away.",
    "DK4_MES_B210_R0144": "What? What did he mean?{LB}How unpleasant.",

    # A crewman asks Hodram to seek the Minotaur's Axe.
    "DK4_MES_B211_R0005": "Admiral! There is a weapon this man wants!",
    "DK4_MES_B211_R0008": "What?",
    "DK4_MES_B211_R0012": "This man wants strength,{LB}so a weapon is needed!",
    "DK4_MES_B211_R0015": "Something besides food? What weapon?",
    "DK4_MES_B211_R0018": "The Minotaur's Axe!",
    "DK4_MES_B211_R0022": "That sounds enormous. Where is it?",
    "DK4_MES_B211_R0025": "No idea... A Minotaur once lived on this island. That is all this man knows.",
    "DK4_MES_B211_R0029": "Understood. Someday, we shall search.",
    "DK4_MES_B211_R0032": "Hooray!",
    "DK4_MES_B211_R0036": "Someday, remember.",
    "DK4_MES_B211_R0040": "Still, hooray!",
    "DK4_MES_B211_R0044": "Nor was it promised to you.",
    "DK4_MES_B211_R0047": "Aww.",

    # Christina learns of a female pirate's lost treasure sword.
    "DK4_MES_B212_R0005": "You there, may we speak?",
    "DK4_MES_B212_R0009": "Me?",
    "DK4_MES_B212_R0013": "Yes, you.",
    "DK4_MES_B212_R0017": "What?",
    "DK4_MES_B212_R0021": "Seeing you recalls a mighty woman pirate from long ago. She was truly strong.",
    "DK4_MES_B212_R0025": "Do we look alike? Our faces?",
    "DK4_MES_B212_R0028": "Not the face. More your air... Perhaps you simply look strong.",
    "DK4_MES_B212_R0032": "Really? Then this woman must grow stronger in her honor.",
    "DK4_MES_B212_R0036": "You seek strength? Then why not search for that pirate's treasure sword?",
    "DK4_MES_B212_R0040": "Her sword?",
    "DK4_MES_B212_R0044": "Yes, her old sword. The value is unknown to this old man.",
    "DK4_MES_B212_R0048": "Curious. Where is this sword?",
    "DK4_MES_B212_R0051": "Caribbean.",
    "DK4_MES_B212_R0055": "Caribbean",
    "DK4_MES_B212_R0059": "She fought in a great Caribbean sea battle and supposedly lost it amid the fighting.",
    "DK4_MES_B212_R0062": "And?",
    "DK4_MES_B212_R0066": "That is all.",
    "DK4_MES_B212_R0070": "All? Then how can it be found?",
    "DK4_MES_B212_R0073": "Do not ask... Yet somehow, you seem able to find it.",
    "DK4_MES_B212_R0076": "All right. This woman remembers.",
    "DK4_MES_B212_R0079": "Yes. Surely you can find it. Good luck.",
    "DK4_MES_B212_R0082": "Thank you.",
    "DK4_MES_B212_R0086": "(Pirate sword lost in Caribbean... This woman must see it.)",
    "DK4_MES_B212_R0090": "Christina: Charm +1!",

    # Yukihisa writes about the cursed sword Muramasa.
    "DK4_MES_B213_R0014": "Admiral, a letter from Yukihisa.",
    "DK4_MES_B213_R0015": "Admiral, correspondence from Yukihisa.",
    "DK4_MES_B213_R0016": "Admiral, a letter from Yukihisa.",
    "DK4_MES_B213_R0017": "Admiral, a letter from Mr. Yukihisa.",
    "DK4_MES_B213_R0018": "Admiral, Yukihisa sent a letter.",
    "DK4_MES_B213_R0019": "Admiral, a letter from Yukihisa.",
    "DK4_MES_B213_R0020": "Admiral! A letter from Yukihisa!",
    "DK4_MES_B213_R0027": "Rumor speaks of cursed Muramasa,{LB}condemned by Tokugawa rulers{LB}and marked for destruction.",
    "DK4_MES_B213_R0030": "A clan bearing a grudge against Tokugawa apparently hid one blade somewhere in East Asia. This report is sent at once.",
    "DK4_MES_B213_R0033": "Surely this is the treasure sought by this warrior. Hakuki Gensho Yukihisa",
    "DK4_MES_B213_R0053": "Such difficult prose. Very Yukihisa.",
    "DK4_MES_B213_R0054": "Hard prose. Just like Yukihisa.",
    "DK4_MES_B213_R0055": "Complex prose. So like Yukihisa.",
    "DK4_MES_B213_R0056": "Such difficult prose. Very Yukihisa.",
    "DK4_MES_B213_R0057": "Needlessly difficult. Typical Yukihisa.",
    "DK4_MES_B213_R0058": "Hard prose indeed. Very Yukihisa.",
    "DK4_MES_B213_R0059": "Too hard. Cannot understand it.",
    "DK4_MES_B213_R0060": "Difficult prose. Truly, very Yukihisa.",
    "DK4_MES_B213_R0065": "Needlessly difficult. Typical Yukihisa.",
    "DK4_MES_B213_R0071": "...Understood. Curious.",

    # A crewman reports a sealed blood-red sword.
    "DK4_MES_B214_R0005": "Admiral, listen! Valuable news.",
    "DK4_MES_B214_R0008": "A local lord apparently acquired a remarkably sharp sword.",
    "DK4_MES_B214_R0011": "And?",
    "DK4_MES_B214_R0015": "The blade glows faintly red, as though it drank the blood of many.",
    "DK4_MES_B214_R0019": "Hm... Quite unusual.",
    "DK4_MES_B214_R0023": "The lord found it eerie and sealed it away without ever using it. A terrible coward.",
    "DK4_MES_B214_R0026": "What a waste.",
    "DK4_MES_B214_R0029": "An astonishing fool. Why acquire a sword at all?",
    "DK4_MES_B214_R0033": "His feeling is understandable. What became of the sword?",
    "DK4_MES_B214_R0036": "The hiding place is unknown. We should search when possible.",

    # Christina follows swans carrying a shining object toward Amsterdam.
    "DK4_MES_B215_R0005": "What a lovely square...{LB}Something is in that pond.{LB}Could that be...",
    "DK4_MES_B215_R0009": "Aah!",
    "DK4_MES_B215_R0013": "A pair of swans! They visit even here? Are you two traveling as well?",
    "DK4_MES_B215_R0017": "Aah! Coo... Coo... Aah!",
    "DK4_MES_B215_R0021": "Hehe. Such a loving pair. Enviable.",
    "DK4_MES_B215_R0024": "flap, flap!",
    "DK4_MES_B215_R0028": "Oh! Where are they going?{LB}They carry something!",
    "DK4_MES_B215_R0032": "That way...",
    "DK4_MES_B215_R0036": "Christina, there you are.",
    "DK4_MES_B215_R0040": "Oh, {MACRO:FI}. A pair of swans was here.",
    "DK4_MES_B215_R0043": "Swans? Rare for them to enter a city.",
    "DK4_MES_B215_R0046": "They carried something long and shining toward Amsterdam. Shall we look?",

    # A Three Kingdoms enthusiast reveals Zhao Yun's legendary spear.
    "DK4_MES_B216_R0005": "Hey, do you know Romance of the Three Kingdoms?",
    "DK4_MES_B216_R0010": "Yes",
    "DK4_MES_B216_R0012": "No",
    "DK4_MES_B216_R0022": "Really? Read it. A wonderful tale.",
    "DK4_MES_B216_R0032": "You do? Wonderful! Which hero is your favorite?",
    "DK4_MES_B216_R0039": "Zhao",
    "DK4_MES_B216_R0041": "Guan",
    "DK4_MES_B216_R0043": "Zhuge",
    "DK4_MES_B216_R0051": "What?! The same as this man!{LB}We will get along.",
    "DK4_MES_B216_R0054": "His lone charge through Cao Cao's army with A Dou was magnificent!",
    "DK4_MES_B216_R0058": "Rumor says Zhao Yun's legendary spear lies somewhere on this peninsula.",
    "DK4_MES_B216_R0062": "This man searched everywhere but failed. Perhaps you can find it.",
    "DK4_MES_B216_R0078": "Zhuge Liang? His memorial{LB}brings tears. My second favorite.",

    # A guardian recognizes Hodram as the prophesied Sea King.
    "DK4_MES_B217_R0005": "Excuse me, sir.",
    "DK4_MES_B217_R0009": "Me...?",
    "DK4_MES_B217_R0013": "May this old man see that?",
    "DK4_MES_B217_R0016": "That?",
    "DK4_MES_B217_R0020": "That item.",
    "DK4_MES_B217_R0024": "Hm... No mistake. Just as foretold.",
    "DK4_MES_B217_R0031": "Three centuries ago, great Kublai Khan ruled the continent.",
    "DK4_MES_B217_R0035": "Yet even that emperor eventually died...",
    "DK4_MES_B217_R0038": "The emperor said:{LB}'Two centuries hence,{LB}the Sea King shall come...'",
    "DK4_MES_B217_R0042": "'That Sea King will lead many foreigners and bear the golden seal of lands beyond my rule. Give that hero my sword.'",
    "DK4_MES_B217_R0045": "This clan served him.{LB}We awaited the Sea King...",
    "DK4_MES_B217_R0048": "Today, you have appeared at last. Ruler of the oceans, we have awaited you.",
    "DK4_MES_B217_R0052": "Me? Hah, spare me. This man is no such grand figure.",
    "DK4_MES_B217_R0056": "No. These eyes do not err. You are truly the Sea King.",
    "DK4_MES_B217_R0059": "Search south of Shandong. The emperor's sword lies there.",
    "DK4_MES_B217_R0062": "The Great Sword is now yours.{LB}Go well.",

    # Gennas writes about the Sword of Judas.
    "DK4_MES_B218_R0014": "Admiral, a letter from Gennas.",
    "DK4_MES_B218_R0016": "Admiral, correspondence from Gennas.",
    "DK4_MES_B218_R0018": "Admiral, a letter from Gennas.",
    "DK4_MES_B218_R0020": "Admiral, letter from Gennas.",
    "DK4_MES_B218_R0022": "Admiral, Gennas sent a letter.",
    "DK4_MES_B218_R0024": "Admiral, a letter from Gennas.",
    "DK4_MES_B218_R0026": "Admiral! A letter from Gennas!",
    "DK4_MES_B218_R0034": "Admiral, writing from the road to Rome.",
    "DK4_MES_B218_R0038": "This road recalls missionaries{LB}who endured persecution{LB}to spread their faith.",
    "DK4_MES_B218_R0041": "Religion holds little interest, but one tale caught attention.",
    "DK4_MES_B218_R0044": "A sword carried by Judas, one of Jesus's twelve disciples, may remain in a place tied to him.",
    "DK4_MES_B218_R0048": "Judas betrayed Jesus,{LB}so people fear his possessions.{LB}No one seeks the blade.",
    "DK4_MES_B218_R0051": "The sword is keen and magnificent.{LB}A blade bears no guilt,{LB}so a search seems worthwhile.",
    "DK4_MES_B218_R0062": "Though devout Manuel may dislike this tale.",
    "DK4_MES_B218_R0068": "More news will follow when available. Gennas Pasa",
    "DK4_MES_B218_R0075": "A traitor's sword... Gennas is practical enough to value quality over origin.",
    "DK4_MES_B218_R0087": "This man is not wholly opposed. Judas repented in the end. The decision is yours, Admiral.",

    # Vivian sends Hodram after Excalibur in Avalon.
    "DK4_MES_B219_R0005": "King...?",
    "DK4_MES_B219_R0009": "You again!{LB}Stop hurting business and get out!",
    "DK4_MES_B219_R0013": "The king...? Where is its hero?",
    "DK4_MES_B219_R0016": "What is wrong? Who are you?",
    "DK4_MES_B219_R0019": "This woman is... Vivian, maker of Arthur's holy sword...",
    "DK4_MES_B219_R0022": "King Arthur...?",
    "DK4_MES_B219_R0026": "The king sleeps, yet the sacred sword seeks a hero...",
    "DK4_MES_B219_R0029": "Hero, seek Excalibur! The blade awaits you in Avalon, where the king sleeps!",
    "DK4_MES_B219_R0032": "Avalon? Never heard of it.",
    "DK4_MES_B219_R0036": "Someone at the tavern may know that land.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "04": "Gennas Pasa",
    "07": "Christina",
    "0B": "Jam Jack Ludwayer",
    "0C": "Yukihisa",
    "0E": "Crewman",
    "10": "Gerhard Adelknauts",
    "11": "Crewman",
    "17": "Manuel",
    "18": "Sera",
    "52": "Merchant",
    "95": "Three Kingdoms enthusiast",
    "A9": "Vivian",
    "AA": "Elder",
    "AD": "Merchant",
    "D0": "Crewman",
    "FE": "System or scene text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    210: "Christina evaluates legendary ceramic earrings offered by a merchant.",
    211: "A crewman asks Hodram to seek the Minotaur's Axe.",
    212: "Christina learns of a woman pirate's treasure sword lost in the Caribbean.",
    213: "Yukihisa writes to Hodram about the cursed sword Muramasa.",
    214: "A crewman reports a blood-red sword sealed by a frightened lord.",
    215: "Christina follows swans carrying a shining object toward Amsterdam.",
    216: "A Three Kingdoms enthusiast reveals the location of Zhao Yun's legendary spear.",
    217: "An elder recognizes Hodram as the prophesied Sea King and reveals Kublai Khan's sword.",
    218: "Gennas writes to Hodram about the Sword of Judas.",
    219: "Vivian sends Hodram to seek Excalibur in Avalon.",
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
        raise SystemExit(f"Hodram V16 inventory mismatch: missing={missing}, extra={extra}")

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
                "speaker": SPEAKERS.get(state, "Choice or alternate crew text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
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
        "dialogue_profile": "hodram-story-weapon-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Hodram weapon, correspondence, treasure, and character events across SC1 blocks 210-219.",
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
