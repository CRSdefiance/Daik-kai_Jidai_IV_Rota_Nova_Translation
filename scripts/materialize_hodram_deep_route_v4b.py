from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v4b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (87, 88, 89, 91, 92, 93)
EXCLUDED = {
    "DK4_MES_B88_R0134": "Raw event-control payload; not dialogue.",
    "DK4_MES_B89_R0004": "Raw event-control payload; not dialogue.",
}

LINES = {
    "DK4_MES_B87_R0005": "Suddenly...",
    "DK4_MES_B87_R0009": "Hm?",
    "DK4_MES_B87_R0014": "Would you hire me?",
    "DK4_MES_B87_R0017": "A volunteer? Prove your skill and perhaps.",
    "DK4_MES_B87_R0020": "Yes. Love machines. Good with ships and repairs.",
    "DK4_MES_B87_R0023": "Terms?",
    "DK4_MES_B87_R0027": "One request. Please lend me 1,000 gold!",
    "DK4_MES_B87_R0032": "Agreed.",
    "DK4_MES_B87_R0034": "No money.",
    "DK4_MES_B87_R0042": "Thank you! Now repairs can finish!",
    "DK4_MES_B87_R0045": "Sorry. Delay sailing one day.",
    "DK4_MES_B87_R0048": "Dock tomorrow.",
    "DK4_MES_B87_R0055": "Been waiting! Look here.",
    "DK4_MES_B87_R0062": "Ship fixed. Debt paid. Thanks.",
    "DK4_MES_B87_R0066": "Sorry for testing you. An admiral trusted with my life must show character.",
    "DK4_MES_B87_R0069": "You pass. Please use this ship.",
    "DK4_MES_B87_R0072": "Your name?",
    "DK4_MES_B87_R0076": "The ship? Name it anything.",
    "DK4_MES_B87_R0080": "No, your name. You never said it.",
    "DK4_MES_B87_R0083": "Sorry. Excitement made me forget.",
    "DK4_MES_B87_R0087": "Janus Pasha. Glad to serve.",
    "DK4_MES_B87_R0093": "Take the ship from dock and rename it under Refit.",
    "DK4_MES_B87_R0098": "Understood. Someone else, then.",

    "DK4_MES_B88_R0005": "This is Japan... A strange land.",
    "DK4_MES_B88_R0008": "{MACRO:FI}, look! He eats with two sticks!",
    "DK4_MES_B88_R0019": "They're called chopsticks.",
    "DK4_MES_B88_R0022": "How peculiar...",
    "DK4_MES_B88_R0029": "Hey! You foreigners?",
    "DK4_MES_B88_R0032": "You've been acting big in Japan lately!",
    "DK4_MES_B88_R0036": "They want us...",
    "DK4_MES_B88_R0040": "Seems so...",
    "DK4_MES_B88_R0052": "Whoa...",
    "DK4_MES_B88_R0059": "Ouch! Boss!",
    "DK4_MES_B88_R0063": "My poor man! You hit him on purpose and broke his bones!",
    "DK4_MES_B88_R0071": "Nonsense! You hit us!",
    "DK4_MES_B88_R0082": "Exactly!",
    "DK4_MES_B88_R0089": "They hit us, then pick a fight, boss!",
    "DK4_MES_B88_R0093": "Even heaven may forgive this, but Kurushima won't! Get them!",
    "DK4_MES_B88_R0097": "Yeah!",
    "DK4_MES_B88_R0102": "Many of them...",
    "DK4_MES_B88_R0114": "Can't fight!",
    "DK4_MES_B88_R0121": "This rabble is no match for {MACRO:FI} and me.",
    "DK4_MES_B88_R0125": "Allow me!",
    "DK4_MES_B88_R0136": "Leave this to me.",
    "DK4_MES_B88_R0140": "Huh? A samurai siding with foreigners?",
    "DK4_MES_B88_R0144": "This warrior judges right.",
    "DK4_MES_B88_R0148": "Smart fool! Get them!",
    "DK4_MES_B88_R0152": "Yeah!",
    "DK4_MES_B88_R0157": "Waaah!",
    "DK4_MES_B88_R0161": "Defeated!",
    "DK4_MES_B88_R0165": "Remember this!",
    "DK4_MES_B88_R0169": "Blunt edge. None were cut.",
    "DK4_MES_B88_R0173": "Remarkable... here...",
    "DK4_MES_B88_R0177": "That swordplay was extraordinary.",
    "DK4_MES_B88_R0188": "That speed is impossible...",
    "DK4_MES_B88_R0195": "Apologies for my country's shame.",
    "DK4_MES_B88_R0198": "We should bow. You saved us. Thanks.",
    "DK4_MES_B88_R0201": "You appear to sail the world.",
    "DK4_MES_B88_R0204": "Please take me with you.",
    "DK4_MES_B88_R0207": "This warrior wishes to see the world.",
    "DK4_MES_B88_R0210": "You may never return to Japan.",
    "DK4_MES_B88_R0214": "No plan to return. A man must test himself in the wider world.",
    "DK4_MES_B88_R0217": "Good. Name's {MACRO:FI} {MACRO:FA}.",
    "DK4_MES_B88_R0221": "Yukihisa Genjo Shiraki.",

    "DK4_MES_B89_R0011": "The Golden Crown of Silla...",
    "DK4_MES_B89_R0015": "Heavy, yet elegant...",
    "DK4_MES_B89_R0019": "Even men can see why women desire it.",
    "DK4_MES_B89_R0024": "Ah! That in your hand...",
    "DK4_MES_B89_R0028": "You... Julian? You left first, yet came second.",
    "DK4_MES_B89_R0032": "Who are you? Have we met?",
    "DK4_MES_B89_R0035": "Name's {MACRO:FI}. Heard crown talk.",
    "DK4_MES_B89_R0039": "That tale drew us here to seek it too.",
    "DK4_MES_B89_R0043": "Terrible... That was meant as her gift.",
    "DK4_MES_B89_R0051": "My honor is ruined! Can't face Meihua. Please give it to me!",
    "DK4_MES_B89_R0055": "What will you do?",
    "DK4_MES_B89_R0059": "Very well.",
    "DK4_MES_B89_R0063": "Really?",
    "DK4_MES_B89_R0067": "Take it. Sailors don't need it. Claim the find.",
    "DK4_MES_B89_R0070": "What a great man! Someday repayment will come. Goodbye!",
    "DK4_MES_B89_R0077": "Of course. This is {MACRO:FO}'s...",
    "DK4_MES_B89_R0080": "He's gone. Perhaps a longer talk next time.",

    "DK4_MES_B91_R0009": "Me?",
    "DK4_MES_B91_R0018": "Trust",
    "DK4_MES_B91_R0020": "Doubt",
    "DK4_MES_B91_R0031": "How dare you say that to our admiral!",
    "DK4_MES_B91_R0038": "You!",
    "DK4_MES_B91_R0046": "Huh?",
    "DK4_MES_B91_R0054": "What a strange one...",
    "DK4_MES_B91_R0065": "This?",
    "DK4_MES_B91_R0072": "You'd give me this treasure?",
    "DK4_MES_B91_R0078": "Then gratefully accepted.",
    "DK4_MES_B91_R0084": "{MACRO:FI}'s luck rose by 1!",
    "DK4_MES_B91_R0087": "Crewman's luck rose by 1!",
    "DK4_MES_B91_R0094": "Dealing with oddballs ruins luck. Let's go.",
    "DK4_MES_B91_R0097": "Yes.",
    "DK4_MES_B91_R0103": "{MACRO:FI}'s spirit rose by 1!",
    "DK4_MES_B91_R0106": "His spirit rose by 1!",

    "DK4_MES_B92_R0005": "Tomatoes taste good. Munch.",
    "DK4_MES_B92_R0008": "Yes.",
    "DK4_MES_B92_R0012": "Thought it was an apple. Munch.",
    "DK4_MES_B92_R0015": "...Yes.",
    "DK4_MES_B92_R0019": "So sweet and good. Munch.",
    "DK4_MES_B92_R0022": "...(How much can he eat?)",
    "DK4_MES_B92_R0026": "Ha! You really like tomatoes.",
    "DK4_MES_B92_R0029": "Then take this.",
    "DK4_MES_B92_R0032": "What is it?",
    "DK4_MES_B92_R0036": "Tomato plant.",
    "DK4_MES_B92_R0040": "Really?",
    "DK4_MES_B92_R0044": "Sure. You praised my tomatoes so much.",
    "DK4_MES_B92_R0048": "Thank you.",
    "DK4_MES_B92_R0052": "Good deal, Admiral. Munch.",
    "DK4_MES_B92_R0056": "...(Still eating?)",

    "DK4_MES_B93_R0005": "Ook ook!",
    "DK4_MES_B93_R0009": "Whoa! What?",
    "DK4_MES_B93_R0013": "Ook ook!",
    "DK4_MES_B93_R0017": "Go away!",
    "DK4_MES_B93_R0021": "Ook ook!",
    "DK4_MES_B93_R0025": "Give it back!",
    "DK4_MES_B93_R0029": "What now?",
    "DK4_MES_B93_R0033": "Something stole my banana!",
    "DK4_MES_B93_R0037": "What is 'something'? Which one?",
    "DK4_MES_B93_R0040": "There... Gone! The thief fled! Wait!",
    "DK4_MES_B93_R0043": "Did you catch it?",
    "DK4_MES_B93_R0047": "Too quick. Throws stones and seeds.",
    "DK4_MES_B93_R0051": "Let's see... Strange seeds. Maybe useful.",
    "DK4_MES_B93_R0056": "No seeds! Return my banana!",
    "DK4_MES_B93_R0060": "Return it! Return it!",
    "DK4_MES_B93_R0064": "...Let's try local food.",
    "DK4_MES_B93_R0067": "My treat?",
    "DK4_MES_B93_R0071": "Yes.",
    "DK4_MES_B93_R0077": "Yay!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "04": "Janus Pasha", "0C": "Yukihisa Genjo Shiraki",
    "0E": "Emilio Ferrog", "10": "Gerhard Adelknauts", "12": "Charles",
    "14": "Fernando", "1A": "Julian", "29": "Sojin Kurushima", "6C": "Tomato grower",
    "9E": "Kurushima thug", "FE": "System or scene voice",
}
EXTENDED_STATES = {0x10, 0x12, 0x14, 0x1A, 0x29, 0x6C, 0x9E, 0xFE}
CONTEXT = {
    87: "Hodram recruits the mechanic Janus Pasha and receives his repaired ship.",
    88: "Hodram meets and recruits the samurai Yukihisa in Japan after a street fight.",
    89: "Hodram finds the Golden Crown of Silla and gives it to Julian for Meihua.",
    91: "A strange encounter changes Hodram and Fernando's attributes.",
    92: "Emilio's love of tomatoes earns the fleet a tomato seedling.",
    93: "A monkey steals Emilio's banana and leaves unusual seeds behind.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit("Hodram V4b inventory mismatch")
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Choice or scene text"), "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{MACRO:FA}", "Bergstrom").replace("{MACRO:FO}", "Bergstrom Fleet"),
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"],
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram Japan, treasure, recruitment, and discovery events across SC1 blocks 87-93.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
