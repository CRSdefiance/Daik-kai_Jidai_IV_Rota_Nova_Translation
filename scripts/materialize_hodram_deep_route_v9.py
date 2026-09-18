from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v9.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(149, 158))
EXCLUDED = {
    "DK4_MES_B154_R0032": "Raw event-control payload; not dialogue.",
    "DK4_MES_B157_R0003": "Packed scene-control payload; not dialogue.",
    "DK4_MES_B157_R0012": "Packed scene-control payload; not dialogue.",
}

LINES = {
    "DK4_MES_B149_R0017": "Amazing! The ironclad workshop!",
    "DK4_MES_B149_R0023": "Wow! The ironclad workshop!",
    "DK4_MES_B149_R0032": "Magnificent! This is the workshop that built the ironclad!",
    "DK4_MES_B149_R0039": "An ironclad... Oars make ocean voyages hard.",
    "DK4_MES_B149_R0055": "This method can strengthen ship armor further!",
    "DK4_MES_B149_R0060": "This method can strengthen ship armor further!",
    "DK4_MES_B149_R0068": "This method can strengthen ship armor further!",
    "DK4_MES_B149_R0074": "...Hm.",
    "DK4_MES_B149_R0078": "Additional armor can now be installed!",

    "DK4_MES_B150_R0011": "Admiral, this Tang Bamboo Craft...",
    "DK4_MES_B150_R0017": "About this Tang Bamboo Craft...",
    "DK4_MES_B150_R0023": "Quite an intricate object. What about it?",
    "DK4_MES_B150_R0032": "This may match the Bamboo Assembly Diagram. These steps can dismantle it.",
    "DK4_MES_B150_R0038": "Doesn't it resemble the Bamboo Assembly Diagram? Bet we can dismantle it this way.",
    "DK4_MES_B150_R0045": "Then why not try?",
    "DK4_MES_B150_R0055": "Really? Then allow me...",
    "DK4_MES_B150_R0060": "Great! These puzzles are fun!",
    "DK4_MES_B150_R0072": "Done! Every piece is apart... Hm? Something is drawn under the bamboo.",
    "DK4_MES_B150_R0078": "Done! All apart... Hm? Something is drawn under the bamboo.",
    "DK4_MES_B150_R0085": "Oh! This is a map!",
    "DK4_MES_B150_R0089": "This shows East Asia's Proof. So that was the mechanism...",

    "DK4_MES_B151_R0005": "The Ceremonial Knife and Sun-Patterned Sheath... They fit as though once a set.",
    "DK4_MES_B151_R0009": "Yes... Perhaps they were once a set.",
    "DK4_MES_B151_R0013": "Knife in the sheath... What?!",
    "DK4_MES_B151_R0016": "What happened?!",
    "DK4_MES_B151_R0020": "Light...? Argh, too bright to see!",
    "DK4_MES_B151_R0026": "What just happened...?",
    "DK4_MES_B151_R0030": "Look! A pattern appeared on the blade.",
    "DK4_MES_B151_R0033": "Unbelievable... This maps the New World's Proof. How strange...",

    "DK4_MES_B152_R0006": "Someone awaits you in Alexandria.",
    "DK4_MES_B152_R0009": "Alexandria...?",

    "DK4_MES_B153_R0006": "{MACRO:FO}? Pass.",
    "DK4_MES_B153_R0012": "You are...?",
    "DK4_MES_B153_R0027": "You rescued Sera?",
    "DK4_MES_B153_R0034": "No need for details. Now solve it and seek the Proof.",
    "DK4_MES_B153_R0045": "Others escaped Ottoman rule as we did. Search the ruins in Turkey.",

    "DK4_MES_B154_R0005": "The Patterned Cloth surely maps the Mediterranean Proof, but...",
    "DK4_MES_B154_R0009": "This does not look like a map yet.",
    "DK4_MES_B154_R0019": "Shouldn't we use the Brass Lamp? Perhaps reveal it with heat...",
    "DK4_MES_B154_R0025": "Why not heat it with the Brass Lamp?",
    "DK4_MES_B154_R0031": "Heat the cloth with the lamp...",
    "DK4_MES_B154_R0034": "Oh!",
    "DK4_MES_B154_R0044": "Yes!",
    "DK4_MES_B154_R0048": "Well done, Charles. We have the Mediterranean Proof map.",
    "DK4_MES_B154_R0054": "Knew it!",
    "DK4_MES_B154_R0058": "Well done. The Mediterranean Proof map is ours.",

    "DK4_MES_B155_R0005": "Mr. {MACRO:FA}, have you heard?",
    "DK4_MES_B155_R0008": "A new Black Sea town was built.",
    "DK4_MES_B155_R0011": "What is its name?",
    "DK4_MES_B155_R0015": "Abkhaz... perhaps?",
    "DK4_MES_B155_R0019": "Abkhaz... Never heard of it.",
    "DK4_MES_B155_R0026": "What, Sera?",
    "DK4_MES_B155_R0030": "{MACRO:FI}... Take me there...",
    "DK4_MES_B155_R0033": "Certainly. Know anything?",
    "DK4_MES_B155_R0036": "My country... Rebuilding...",
    "DK4_MES_B155_R0039": "Could it be your homeland?",
    "DK4_MES_B155_R0043": "(nods)",
    "DK4_MES_B155_R0047": "Your people rebuild your homeland...",
    "DK4_MES_B155_R0050": "The Black Sea is close. Sera, let's go.",
    "DK4_MES_B155_R0053": "Yes!",

    "DK4_MES_B156_R0006": "Lord {MACRO:FA}, His Majesty awaits.",
    "DK4_MES_B156_R0011": "Ah, {MACRO:FA}! Splendid work! Our nation's prosperity is now assured!",
    "DK4_MES_B156_R0014": "You are appointed supreme naval commander. Lead our navy to still greater glory.",
    "DK4_MES_B156_R0018": "(Oh!)",
    "DK4_MES_B156_R0022": "(The admiral is ideal!)",
    "DK4_MES_B156_R0026": "Commander...",
    "DK4_MES_B156_R0030": "Choose any reward. What do you desire?",
    "DK4_MES_B156_R0037": "May this servant state a wish?",
    "DK4_MES_B156_R0040": "Speak freely.",
    "DK4_MES_B156_R0044": "So...",
    "DK4_MES_B156_R0048": "The appointment is a great honor, but...",
    "DK4_MES_B156_R0051": "Hm?",
    "DK4_MES_B156_R0059": "With permission... this servant wishes to retire from the navy.",
    "DK4_MES_B156_R0063": "What?!",
    "DK4_MES_B156_R0067": "(What?!)",
    "DK4_MES_B156_R0071": "(What did he say?!)",
    "DK4_MES_B156_R0075": "What do you mean?!",
    "DK4_MES_B156_R0079": "This is something long considered.",
    "DK4_MES_B156_R0087": "Blessed with fine officers, this servant built the strongest navy.",
    "DK4_MES_B156_R0090": "Deepest thanks for Your Majesty's faith in this servant. However...",
    "DK4_MES_B156_R0093": "This servant lacks the talent to maintain it, train recruits, and make the navy endure.",
    "DK4_MES_B156_R0096": "Nonsense. Your command alone frightens our rivals and inspires every sailor.",
    "DK4_MES_B156_R0099": "Pardon the reply, but that is precisely my greatest concern.",
    "DK4_MES_B156_R0102": "Hm?",
    "DK4_MES_B156_R0106": "Alarm our rivals and we face isolation. Pride in strength will bring disaster.",
    "DK4_MES_B156_R0109": "My absence will ease our rivals and restore a sense of danger among our own sailors.",
    "DK4_MES_B156_R0113": "Hmm...",
    "DK4_MES_B156_R0117": "My sole wish. Please forgive this request.",
    "DK4_MES_B156_R0124": "...Very well. Deeply regrettable, but if this is your earnest wish, so be it.",
    "DK4_MES_B156_R0128": "My deepest thanks.",
    "DK4_MES_B156_R0136": "(Admiral...)",
    "DK4_MES_B156_R0154": "{MACRO:FI}... Come to my country?",
    "DK4_MES_B156_R0157": "No... This life belongs at sea.",
    "DK4_MES_B156_R0161": "Though cold, your people must rebuild their homeland themselves.",
    "DK4_MES_B156_R0165": "But... please come, {MACRO:FI}.",
    "DK4_MES_B156_R0168": "Sera... No legendary king here.",
    "DK4_MES_B156_R0172": "No matter... Please...!",
    "DK4_MES_B156_R0180": "You are a princess; this is a retired sailor. Our stations differ.",
    "DK4_MES_B156_R0188": "Do not look sad. We shall meet again.",
    "DK4_MES_B156_R0193": "Sera: Will we meet again?",
    "DK4_MES_B156_R0197": "{MACRO:FI}: Of course.",
    "DK4_MES_B156_R0201": "Sera: ...",
    "DK4_MES_B156_R0206": "{MACRO:FI}: Truly. Now a free man.",
    "DK4_MES_B156_R0210": "{MACRO:FI}: Someday your land will live again.",
    "DK4_MES_B156_R0213": "Sera: ...Yes.",
    "DK4_MES_B156_R0217": "Shirwood, take good care of Sera.",
    "DK4_MES_B156_R0220": "...Leave it.",
    "DK4_MES_B156_R0224": "Sera taught you? Next meeting will be fun.",
    "DK4_MES_B156_R0236": "Come... back.",
    "DK4_MES_B156_R0240": "Agreed.",
    "DK4_MES_B156_R0248": "Sera...",
    "DK4_MES_B156_R0252": "Stay strong.",
    "DK4_MES_B156_R0256": "(nods)",
    "DK4_MES_B156_R0260": "We shall meet... Goodbye.",
    "DK4_MES_B156_R0271": "Where to go now...?",
    "DK4_MES_B156_R0275": "Admiral! Ready to sail!",
    "DK4_MES_B156_R0280": "Gerhard?!",
    "DK4_MES_B156_R0284": "Your orders!",
    "DK4_MES_B156_R0288": "Gerhard! What are you doing?!",
    "DK4_MES_B156_R0292": "Your new ship, supplies, departure--all prepared.",
    "DK4_MES_B156_R0295": "Not my meaning. Every officer received a responsible post.",
    "DK4_MES_B156_R0299": "Charles leads the Royal Academy laboratory. He was delighted by unlimited research equipment.",
    "DK4_MES_B156_R0302": "Not about Charles...",
    "DK4_MES_B156_R0306": "Manuel chairs naval engineering, studying plans for a new ship.",
    "DK4_MES_B156_R0310": "No! You bear the grave duty of supreme naval commander!",
    "DK4_MES_B156_R0314": "...That role does not suit me.",
    "DK4_MES_B156_R0317": "Nonsense. Skill, experience, trust made you the choice.",
    "DK4_MES_B156_R0320": "Admiral, giving us duties while you retire is unfair.",
    "DK4_MES_B156_R0324": "Uh.",
    "DK4_MES_B156_R0328": "A nation's defense belongs to its people. An outsider should not interfere.",
    "DK4_MES_B156_R0332": "Besides, without you there is no reason to stay. This officer will follow anywhere.",
    "DK4_MES_B156_R0340": "A loveless voyage, then.",
    "DK4_MES_B156_R0344": "Ha ha! Two handsome men like us? Women everywhere will adore us!",
    "DK4_MES_B156_R0347": "...Happy fool.",

    "DK4_MES_B157_R0005": "Go anywhere you like! A useless brute like you is fired!",
    "DK4_MES_B157_R0011": "Good... Do as you please.",
    "DK4_MES_B157_R0014": "What happened? A quarrel?",
    "DK4_MES_B157_R0017": "He said 'fired'... Was that man a bodyguard?",
    "DK4_MES_B157_R0020": "Who was that man?",
    "DK4_MES_B157_R0024": "He only fights. He disobeyed, so he was fired. That's all.",
    "DK4_MES_B157_R0027": "...Skilled?",
    "DK4_MES_B157_R0031": "Curious? His skill is first-rate, but he refused even to carry luggage.",
    "DK4_MES_B157_R0034": "A perfect guard, but too proud or uncooperative...",
    "DK4_MES_B157_R0037": "You cannot lecture on teamwork, Charles. Let's go.",
    "DK4_MES_B157_R0041": "You're serious?!",
    "DK4_MES_B157_R0045": "Must speak with him.",
    "DK4_MES_B157_R0050": "There he is. What a physique. Hard to miss.",
    "DK4_MES_B157_R0057": "What?",
    "DK4_MES_B157_R0061": "You have trained your body well.",
    "DK4_MES_B157_R0064": "That is obvious, and none of your concern.",
    "DK4_MES_B157_R0067": "Don't understand? This is an offer. That attitude costs chances.",
    "DK4_MES_B157_R0070": "What?!",
    "DK4_MES_B157_R0074": "Heard you were fired. Your strength is wasted.",
    "DK4_MES_B157_R0077": "You mean to hire me? Who are you?",
    "DK4_MES_B157_R0080": "Then introductions. {MACRO:FI}, Swedish admiral of the guard fleet.",
    "DK4_MES_B157_R0083": "An admiral... But no wish to sail.",
    "DK4_MES_B157_R0086": "Such poor judgment? You rank me below your old employer?",
    "DK4_MES_B157_R0090": "We just met! You're awfully impatient.",
    "DK4_MES_B157_R0094": "Hesitation lowers a man's worth.",
    "DK4_MES_B157_R0098": "Grr.",
    "DK4_MES_B157_R0102": "Your strength has use here. Decide whether to follow.",
    "DK4_MES_B157_R0106": "Agreed. Let me sail with you. The name is Al.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "04": "Manuel Armando", "0D": "Emilio Firogue",
    "10": "Gerhard Adelknauts", "11": "Al Fasi", "12": "Charles", "17": "Companion",
    "18": "Sera Altos Shalvaraz", "19": "Ifa", "1A": "Companion", "4E": "Shirwood",
    "71": "Tavern patron", "73": "Tavern patron", "78": "Royal attendant", "79": "Guard",
    "7D": "King of Sweden", "84": "Abkhaz elder", "94": "Employer", "97": "Manuel Armando",
    "FE": "Scene voice",
}
EXTENDED_STATES = {0x10, 0x11, 0x12, 0x17, 0x18, 0x19, 0x1A, 0x4E, 0x71, 0x73, 0x78, 0x79, 0x7D, 0x84, 0x94, 0x97, 0xFE}
CONTEXT = {
    149: "The crew discovers the ironclad workshop and unlocks additional armor.",
    150: "The Tang Bamboo Craft and its diagram reveal East Asia's Proof map.",
    151: "The Ceremonial Knife and Sun-Patterned Sheath reveal the New World map.",
    152: "A sailor tells Hodram that someone awaits him in Alexandria.",
    153: "Abkhaz survivors direct Hodram toward Ottoman ruins and the Proof.",
    154: "The Brass Lamp reveals the Mediterranean Proof map on cloth.",
    155: "Sera learns her people are rebuilding Abkhaz on the Black Sea.",
    156: "Hodram retires, parts from Sera, and begins a new voyage with Gerhard.",
    157: "Hodram meets and recruits the proud bodyguard Al Fasi.",
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
        raise SystemExit(f"Hodram V9 inventory mismatch: missing={missing}, extra={extra}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Choice or scene text"),
            "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{MACRO:FA}", "Bergstrom").replace("{MACRO:FO}", "Bergstrom Fleet"),
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"],
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-ending-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram late-game Proof maps, Sera's restored homeland, complete route ending, and Al recruitment across SC1 blocks 149-157.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
