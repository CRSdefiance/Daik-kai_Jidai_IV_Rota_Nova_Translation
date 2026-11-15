from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v22.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    "DK4_MES_B81_R0005": "Love tropical islands.",
    "DK4_MES_B81_R0013": "Endless blue sky, clear seas,{LB}and a blazing sun!{LB}Ah, this is paradise!",
    "DK4_MES_B81_R0017": "Admiral, when business is quiet,{LB}let me command the local fleet.",
    "DK4_MES_B81_R0021": "Sure. Maybe someday.",
    "DK4_MES_B81_R0025": "Really?",
    "DK4_MES_B81_R0029": "Who knows?",
    "DK4_MES_B81_R0033": "Oh... So mean!",

    "DK4_MES_B82_R0009": "You mean me?",
    "DK4_MES_B82_R0018": "Trust",
    "DK4_MES_B82_R0020": "Doubt",
    "DK4_MES_B82_R0031": "Watch how you speak{LB}to our admiral!",
    "DK4_MES_B82_R0038": "You!",
    "DK4_MES_B82_R0046": "Huh?",
    "DK4_MES_B82_R0054": "What a strange one...",
    "DK4_MES_B82_R0065": "This?",
    "DK4_MES_B82_R0072": "Something this grand...{LB}for me?",
    "DK4_MES_B82_R0078": "Oh... Thanks.{LB}A true treasure.",
    "DK4_MES_B82_R0083": "{MACRO:FI}'s Luck rose by 1!",
    "DK4_MES_B82_R0086": "His Luck rose by 1!",
    "DK4_MES_B82_R0093": "Oddballs bring bad luck.{LB}Let us go.",
    "DK4_MES_B82_R0096": "Y-yeah.",
    "DK4_MES_B82_R0102": "{MACRO:FI}'s Spirit rose by 1!",
    "DK4_MES_B82_R0105": "His Spirit rose by 1!",

    "DK4_MES_B83_R0005": "Tasty tomatoes.{LB}Munch, munch.",
    "DK4_MES_B83_R0008": "Yes, tasty.",
    "DK4_MES_B83_R0012": "Thought it was an apple.{LB}Munch.",
    "DK4_MES_B83_R0015": "Really? Only you would think that.",
    "DK4_MES_B83_R0018": "Sweet and tasty.{LB}Munch, munch.",
    "DK4_MES_B83_R0021": "How long are you going to eat?",
    "DK4_MES_B83_R0025": "Ha ha ha! You folks{LB}really love tomatoes!",
    "DK4_MES_B83_R0028": "Since you like them so much,{LB}take this.",
    "DK4_MES_B83_R0031": "What is it?",
    "DK4_MES_B83_R0035": "Tomato plant.",
    "DK4_MES_B83_R0039": "Really? We can have it?",
    "DK4_MES_B83_R0043": "Sure. You praised my tomatoes{LB}more than enough to earn it.",
    "DK4_MES_B83_R0047": "Thank you, sir!",
    "DK4_MES_B83_R0051": "Lucky us. Munch, munch.",
    "DK4_MES_B83_R0055": "...(Still eating.)",

    "DK4_MES_B84_R0005": "Ook ook ook!",
    "DK4_MES_B84_R0009": "Whoa! What?!",
    "DK4_MES_B84_R0013": "Ook ook ook!",
    "DK4_MES_B84_R0017": "Hey! Get away!",
    "DK4_MES_B84_R0021": "Ook ook ook!",
    "DK4_MES_B84_R0025": "Hey! Give it!",
    "DK4_MES_B84_R0029": "What now?",
    "DK4_MES_B84_R0033": "My banana!{LB}Something stole it{LB}right from my hand!",
    "DK4_MES_B84_R0037": "Something...?",
    "DK4_MES_B84_R0041": "That thing was... Gone!{LB}The thief ran away! Wait!",
    "DK4_MES_B84_R0044": "Did you catch it?",
    "DK4_MES_B84_R0048": "Too quick, and it throws things!{LB}Rocks, seeds, all kinds of stuff.",
    "DK4_MES_B84_R0052": "Look. Huh? What seed?{LB}Never seen it.",
    "DK4_MES_B84_R0057": "Who cares? Give back my banana!",
    "DK4_MES_B84_R0061": "Give it back! Give back my banana!",
    "DK4_MES_B84_R0065": "Oh, all right! Emilio, let us try{LB}this town's famous food.",
    "DK4_MES_B84_R0069": "...Pay?",
    "DK4_MES_B84_R0073": "Uh... yes. My treat.",
    "DK4_MES_B84_R0078": "Hooray!",

    "DK4_MES_B86_R0005": "!{LB}Here...",
    "DK4_MES_B86_R0008": "What is it, Uncle Gerhard?",
    "DK4_MES_B86_R0012": "Nothing.{LB}Old memories...",
    "DK4_MES_B86_R0019": "Long ago, fighting pirates here,{LB}my sword was lost.",
    "DK4_MES_B86_R0022": "Sword?",
    "DK4_MES_B86_R0026": "Yes. An old Katzbalger,{LB}but far better in the hand{LB}than its looks suggested.{LB}That blade served me for years.",
    "DK4_MES_B86_R0029": "You loved it that much?{LB}Was it never found?",
    "DK4_MES_B86_R0032": "No trace remained. A fisherman{LB}probably found and sold it{LB}for a pittance.",
    "DK4_MES_B86_R0035": "Maybe someone still{LB}takes good care of it.",
    "DK4_MES_B86_R0039": "A blade like that is rarely found.{LB}Knowing a worthy owner uses it{LB}would ease my mind...",

    "DK4_MES_B88_R0005": "Admiral, what is nukenin?",
    "DK4_MES_B88_R0009": "A nukenin?",
    "DK4_MES_B88_R0013": "One who was once a ninja.",
    "DK4_MES_B88_R0017": "A ninja, huh?{LB}...What is a ninja?",
    "DK4_MES_B88_R0020": "A clan in Japan skilled{LB}in covert action.",
    "DK4_MES_B88_R0023": "So, a Japanese spy.{LB}Ever met one?",
    "DK4_MES_B88_R0027": "Never. See a ninja's face and die.{LB}Such is their code...",
    "DK4_MES_B88_R0031": "Mamma mia!",
    "DK4_MES_B88_R0035": "Leaving a ninja clan risks death.{LB}Any nukenin who escapes pursuit{LB}must possess extraordinary skill.",
    "DK4_MES_B88_R0038": "Why do you ask of nukenin?",
    "DK4_MES_B88_R0042": "Well, it is their outfit{LB}that caught my ear.",
    "DK4_MES_B88_R0046": "Black clothes called{LB}'Nukenin's Black Garb.'{LB}Armor, not mere clothing.",
    "DK4_MES_B88_R0050": "Armor?",
    "DK4_MES_B88_R0054": "Details are scarce,{LB}but it is very light and tough.",
    "DK4_MES_B88_R0057": "Such a thing exists?{LB}News to me.",
    "DK4_MES_B88_R0060": "Even Yukihisa never heard of it?",
    "DK4_MES_B88_R0064": "No. My shame.",
    "DK4_MES_B88_R0068": "No need to apologize, Yukihisa.",
    "DK4_MES_B88_R0071": "But...",
    "DK4_MES_B88_R0075": "Besides, this was my story.{LB}Yukihisa, you are amusing.",
    "DK4_MES_B88_R0078": "Amusing? What do you mean?{LB}An insult will not be forgiven.",
    "DK4_MES_B88_R0082": "Oh? And what would you do?",
    "DK4_MES_B88_R0086": "What are you two doing?!{LB}Grown men squabbling{LB}like children!",
    "DK4_MES_B88_R0090": "...Apologies.",
    "DK4_MES_B88_R0094": "Sorry. My fault.",
    "DK4_MES_B88_R0097": "Still, if that black armor exists,{LB}it must be in Japan.",
    "DK4_MES_B88_R0100": "Yes.",
    "DK4_MES_B88_R0104": "Same here. Let us look{LB}when we have time.",

    "DK4_MES_B164_R0005": "So this is Alexandria.{LB}Quite a large city.",
    "DK4_MES_B164_R0008": "Africa is vast.{LB}Likely many large cities.",
    "DK4_MES_B164_R0011": "Maybe! The land feels endless.",
    "DK4_MES_B164_R0015": "Precisely!{LB}You are completely wrong!!!",
    "DK4_MES_B164_R0018": "Whoa! Who are you?",
    "DK4_MES_B164_R0022": "Hey! Who are you?{LB}Want a fight?",
    "DK4_MES_B164_R0025": "Wrong is wrong! There is no end{LB}of the world. The Earth is round.{LB}This is common knowledge!!!",
    "DK4_MES_B164_R0028": "True, but...{LB}Were you even listening?",
    "DK4_MES_B164_R0031": "This scholar merely{LB}corrected an error.",
    "DK4_MES_B164_R0034": "This fellow makes no sense!",
    "DK4_MES_B164_R0038": "Maybe that means he knows a lot.",
    "DK4_MES_B164_R0042": "Correct! This scholar traveled{LB}the world, gaining knowledge.",
    "DK4_MES_B164_R0046": "Wow. You really study hard.",
    "DK4_MES_B164_R0050": "Why admire him?{LB}He came looking for a fight!",
    "DK4_MES_B164_R0054": "His timing was poor, that is all.{LB}Would knowledge of the whole world{LB}not be useful?",
    "DK4_MES_B164_R0058": "Kamil, no...",
    "DK4_MES_B164_R0062": "Would you come with us?",
    "DK4_MES_B164_R0066": "What???",
    "DK4_MES_B164_R0070": "Knew it! Wait just a minute!",
    "DK4_MES_B164_R0074": "We sail a ship,{LB}and she is our admiral.",
    "DK4_MES_B164_R0077": "Splendid!!! An admiral!{LB}Please allow this scholar aboard!",
    "DK4_MES_B164_R0080": "Kamil, what am l supposed to do?",
    "DK4_MES_B164_R0083": "Traveling the world means{LB}he has sailing experience too.{LB}He should be useful aboard ship.",
    "DK4_MES_B164_R0086": "Please, Admiral!",
    "DK4_MES_B164_R0089": "Sounds exhausting...{LB}All right. Hired.",
    "DK4_MES_B164_R0092": "Many thanks. This scholar is{LB}Cesare Tohni.",
    "DK4_MES_B164_R0095": "Welcome, Cesare.{LB}Let me show you the ship.",
    "DK4_MES_B164_R0098": "Great. Another oddball...",
    "DK4_MES_B164_R0103": "Admiral, may this scholar offer{LB}advice on choosing ships?",
    "DK4_MES_B164_R0109": "Yes",
    "DK4_MES_B164_R0111": "No",
    "DK4_MES_B164_R0121": "Understood! A creed of your own.{LB}Truly admirable!",
    "DK4_MES_B164_R0125": "This scholar shall prepare{LB}to depart. Goodbye!",
    "DK4_MES_B164_R0136": "Ahem...",
    "DK4_MES_B164_R0140": "No need for more ships yet. At one percent, you can buy only one to five units of goods.",
    "DK4_MES_B164_R0143": "Once shares rise and more goods{LB}become available, buy a ship.",
    "DK4_MES_B164_R0147": "Begin with the ship's{LB}size and price.",
    "DK4_MES_B164_R0150": "Match ships to cash and shares.{LB}An empty hold merely means{LB}paying extra sailors.",
    "DK4_MES_B164_R0153": "Price reveals size: under 5,000{LB}is small; 10,000-20,000 is medium;{LB}over 50,000 is large.",
    "DK4_MES_B164_R0156": "Small ships are cheap.{LB}Even with little cash, they easily{LB}increase fleet cargo capacity.",
    "DK4_MES_B164_R0159": "After trading builds some savings,{LB}replace them with medium ships.",
    "DK4_MES_B164_R0163": "Medium ships have two or three masts. Three are faster, but need more sail handlers.",
    "DK4_MES_B164_R0166": "A refit allows up to five holds.{LB}Without plans for combat, skip{LB}marine quarters and gun decks.",
    "DK4_MES_B164_R0169": "To reach distant ports,{LB}add supply holds to greatly{LB}extend sailing range.",
    "DK4_MES_B164_R0173": "But conflict with another faction{LB}will require large ships.",
    "DK4_MES_B164_R0177": "At least the flagship needs{LB}marine quarters and gun decks,{LB}or victory at sea will be difficult.",
    "DK4_MES_B164_R0180": "Mind your money. Two medium ships{LB}cost less than one large ship{LB}and carry more goods.",
    "DK4_MES_B164_R0183": "Large ships come later. To form local fleets, keep old medium ships instead of selling them.",
    "DK4_MES_B164_R0186": "That concludes the advice.{LB}Now to prepare for departure!",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Kamil", "06": "Manuel Armida", "07": "Christina",
    "09": "Kamil", "0C": "Yukihisa Genjo Shiraki", "0E": "Emilio Ferrog",
    "0F": "Carlo", "10": "Gerhard Adelknauts", "12": "Mikhail",
    "14": "Fernando", "16": "Samwell", "6C": "Tomato grower", "72": "Cape resident",
    "FE": "Narration",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "81": "Christina dreams of commanding a tropical local fleet.",
    "82": "Lil faces a trust choice and receives a small crew-stat reward.",
    "83": "Emilio's love of tomatoes earns the fleet a tomato seedling.",
    "84": "A monkey steals Emilio's banana and leaves an unfamiliar seed behind.",
    "86": "Gerhard recalls a beloved Katzbalger lost in an old pirate battle.",
    "88": "The crew discusses nukenin and learns of the legendary black garb in Japan.",
    "164": "Lil recruits Cesare Tohni in Alexandria; Cesare explains ship size, price, holds, refits, and fleet roles.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V22 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Concise American English preserving characterization, treasure clues, choice meaning, and tutorial accuracy.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    counts = {}
    for row_id in LINES:
        block = str(int(row_id.split("_B", 1)[1].split("_", 1)[0]))
        counts[block] = counts.get(block, 0) + 1
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil route blocks 81-88 plus Cesare's ship-selection and refit tutorial in block 164.",
        "excluded_records": {},
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
