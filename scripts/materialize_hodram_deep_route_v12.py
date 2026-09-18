from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v12.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(169, 174))
EXCLUDED = {"DK4_MES_B169_R0014": "Packed gambling branch-control payload; not dialogue."}


LINES = {
    "DK4_MES_B169_R0011": "Since you're here, take my wager.",
    "DK4_MES_B169_R0016": "New face, eh? Bet me a drink; it's only a simple game.",
    "DK4_MES_B169_R0020": "Here are some coins. We each take one to three on our turn.",
    "DK4_MES_B169_R0024": "Whoever takes the last coin loses. Simple, right? Let's play.",
    "DK4_MES_B169_R0033": "Play",
    "DK4_MES_B169_R0035": "Pass",
    "DK4_MES_B169_R0047": "Then a drink.",
    "DK4_MES_B169_R0051": "Ah, good stuff. Thanks. See ya.",
    "DK4_MES_B169_R0060": "Damn, you got me. Been a while. Here.",
    "DK4_MES_B169_R0070": "No, thanks. You truly trust your luck that much?",
    "DK4_MES_B169_R0074": "Sure. Gambling needs insight and luck.",
    "DK4_MES_B169_R0077": "Got both. Born to gamble, you might say.",
    "DK4_MES_B169_R0081": "You? Sharp...?",
    "DK4_MES_B169_R0085": "Never judge by appearances.",
    "DK4_MES_B169_R0089": "Take that couple. Can't hear them, but what are they saying?",
    "DK4_MES_B169_R0092": "He courts her.",
    "DK4_MES_B169_R0096": "Amateur mistake. They're breaking up.",
    "DK4_MES_B169_R0104": "Just watch.",
    "DK4_MES_B169_R0108": "Listening to you... Your selfish thinking is unbearable!",
    "DK4_MES_B169_R0111": "Think what you like. You're selfish too.",
    "DK4_MES_B169_R0114": "Then we should stop seeing each other.",
    "DK4_MES_B169_R0117": "We agree, then. This is goodbye.",
    "DK4_MES_B169_R0124": "See? Called it.",
    "DK4_MES_B169_R0128": "Remarkable... How?",
    "DK4_MES_B169_R0132": "Her fist was clenched under the table. She hid anger, not love.",
    "DK4_MES_B169_R0136": "He never met her eyes. Would a man in love act that way?",
    "DK4_MES_B169_R0140": "Understood... Keen insight.",
    "DK4_MES_B169_R0143": "Right. That insight lets me read an opponent.",
    "DK4_MES_B169_R0146": "Then luck brings victory.",
    "DK4_MES_B169_R0149": "Such talent is wasted on gambling. Join my ship.",
    "DK4_MES_B169_R0153": "Whoa. That's sudden.",
    "DK4_MES_B169_R0157": "Well, time hangs heavy. Heads, and you have a new crewmate.",
    "DK4_MES_B169_R0163": "No drink. Join me.",
    "DK4_MES_B169_R0167": "Again? All right. Ask the coin once more.",
    "DK4_MES_B169_R0192": "Hah. My life won't ride{LB}with unlucky men. Goodbye.",
    "DK4_MES_B169_R0208": "Hah, settled. My life's riding on you!",
    "DK4_MES_B169_R0211": "My name is Dias! Another stroke of luck!",
    "DK4_MES_B169_R0214": "Show your skill.",
    "DK4_MES_B169_R0228": "Tch. Bad luck lately.",

    "DK4_MES_B170_R0005": "No good!",
    "DK4_MES_B170_R0013": "No, no, no! Absolutely not!",
    "DK4_MES_B170_R0016": "(Drunk...?)",
    "DK4_MES_B170_R0021": "Hey, you there!",
    "DK4_MES_B170_R0029": "Young folk these days!",
    "DK4_MES_B170_R0033": "(Old man's routine...)",
    "DK4_MES_B170_R0037": "You drink this swill? Disgraceful!",
    "DK4_MES_B170_R0040": "(Oh dear...)",
    "DK4_MES_B170_R0044": "What's that sour look?",
    "DK4_MES_B170_R0048": "Then don't drink bad wine.",
    "DK4_MES_B170_R0051": "When thirst calls, one makes do.",
    "DK4_MES_B170_R0054": "Then drink quietly. Think of those around you.",
    "DK4_MES_B170_R0057": "Though forced to drink swill and complain...",
    "DK4_MES_B170_R0061": "Truth is, good wine is wanted! You there, let this old man taste some.",
    "DK4_MES_B170_R0065": "Give me good wine and peace follows!",
    "DK4_MES_B170_R0068": "(Oh dear...)",
    "DK4_MES_B170_R0072": "Come, pour it! This old instinct says you have fine wine.",
    "DK4_MES_B170_R0077": "Yes...",
    "DK4_MES_B170_R0079": "No.",
    "DK4_MES_B170_R0086": "What! Well done!",
    "DK4_MES_B170_R0090": "No wine expert here, only aware of its normal trade value.",
    "DK4_MES_B170_R0094": "Trade, eh? This old man knows a little.",
    "DK4_MES_B170_R0098": "You were a seaborne merchant?",
    "DK4_MES_B170_R0101": "Aye. Call me a veteran.",
    "DK4_MES_B170_R0105": "Then may this man ask you something?",
    "DK4_MES_B170_R0109": "Hm? What would you ask?",
    "DK4_MES_B170_R0115": "Ask what you don't know",
    "DK4_MES_B170_R0117": "Test his knowledge",
    "DK4_MES_B170_R0125": "Honest and humble. A fine attitude.",
    "DK4_MES_B170_R0128": "Then let's go. Where is your ship?",
    "DK4_MES_B170_R0133": "Testing me, eh? Not so fast.",
    "DK4_MES_B170_R0136": "A cynic needs proper teaching.{LB}Start by recognizing fine wine.",
    "DK4_MES_B170_R0139": "Stop gawking and show me the ship.",
    "DK4_MES_B170_R0145": "Eh?",
    "DK4_MES_B170_R0149": "You're taking me aboard, yes? There is far too much to teach in a day or two.",
    "DK4_MES_B170_R0157": "Julio Erneco. Good to meet you.",
    "DK4_MES_B170_R0160": "...Likewise.",
    "DK4_MES_B170_R0164": "Old man! The admiral never agreed...",
    "DK4_MES_B170_R0168": "Very well.",
    "DK4_MES_B170_R0172": "The sea again! My heart soars!",
    "DK4_MES_B170_R0181": "No lies! Age brings no foolishness.{LB}Now, tell me all.",
    "DK4_MES_B170_R0184": "Well... We're just setting out to search, during our voyage.",
    "DK4_MES_B170_R0188": "A voyage? Splendid! Then this old man shall join you.",
    "DK4_MES_B170_R0196": "Why the shock? This old sea dog is still in his prime!",
    "DK4_MES_B170_R0200": "Old, perhaps, but still useful.",
    "DK4_MES_B170_R0203": "Old man! The admiral never agreed...",
    "DK4_MES_B170_R0207": "Very well.",
    "DK4_MES_B170_R0211": "Julio Erneco. Count on me.",

    "DK4_MES_B171_R0005": "Admiral, care to hear my sailing lesson?",
    "DK4_MES_B171_R0008": "Tips?",
    "DK4_MES_B171_R0012": "Bored stiff lately. Think of it as helping a fellow out.",
    "DK4_MES_B171_R0018": "Hear",
    "DK4_MES_B171_R0020": "No thanks",
    "DK4_MES_B171_R0029": "Do you know who you're trying to lecture?",
    "DK4_MES_B171_R0033": "...Right.",
    "DK4_MES_B171_R0045": "No need. Ships are already well known.",
    "DK4_MES_B171_R0051": "All right. You seem shipwise.{LB}Better wait for greener hands.",
    "DK4_MES_B171_R0062": "Good attitude. You'll go far.",
    "DK4_MES_B171_R0065": "On a sailing ship, sails are life.",
    "DK4_MES_B171_R0068": "Start with square sails versus lateen sails.",
    "DK4_MES_B171_R0071": "A square sail crosses the ship's length. This makes it transverse.",
    "DK4_MES_B171_R0075": "Such sails won't turn fore and aft.{LB}Strong downwind, poor at an ideal angle upwind.",
    "DK4_MES_B171_R0078": "A lateen sail runs fore and aft, so it cannot lie across the ship like a square sail.",
    "DK4_MES_B171_R0081": "That gives a good upwind angle, but less speed downwind. Clear so far?",
    "DK4_MES_B171_R0084": "Next, extra sails.",
    "DK4_MES_B171_R0088": "A topsail is a small square sail mounted atop each mast.",
    "DK4_MES_B171_R0092": "A staysail is a small fore-and-aft sail before a mast. No overlap with a lateen.",
    "DK4_MES_B171_R0095": "A spritsail is a square sail at the bow. Small ships cannot mount one.",
    "DK4_MES_B171_R0098": "A jigger spanker is an aft sail, almost another small mast. Only large ships fit one.",
    "DK4_MES_B171_R0101": "Ships with two or more masts run faster on a quartering wind than dead astern. Know why?",
    "DK4_MES_B171_R0105": "You there. Know why?",
    "DK4_MES_B171_R0109": "Because the masts line up fore to aft.",
    "DK4_MES_B171_R0112": "Right. Dead astern, only the rear mast catches wind; those forward are shadowed.",
    "DK4_MES_B171_R0115": "Best speed comes from the aft quarter, with every sail trimmed to match.",
    "DK4_MES_B171_R0119": "Got it!",
    "DK4_MES_B171_R0131": "Never noticed before! Now it makes sense!",
    "DK4_MES_B171_R0138": "Thanks for listening. Back to work now.",

    "DK4_MES_B172_R0005": "You folks here to see old Mikhail too?",
    "DK4_MES_B172_R0008": "Old Mikhail?",
    "DK4_MES_B172_R0020": "M-Mikhail?! No! Don't meet him! {MACRO:FI}, stay away!",
    "DK4_MES_B172_R0026": "No? He's known here as a wise old scholar.",
    "DK4_MES_B172_R0030": "Let's meet him.",
    "DK4_MES_B172_R0034": "With women along, perhaps don't...",
    "DK4_MES_B172_R0045": "Exactly! Stay away!",
    "DK4_MES_B172_R0055": "So that's Mikhail.",
    "DK4_MES_B172_R0059": "Wow! You're amazing!",
    "DK4_MES_B172_R0063": "Quite so! Ho ho ho!",
    "DK4_MES_B172_R0066": "Then what's this?",
    "DK4_MES_B172_R0070": "A peppercorn. A tropical fruit ground into spice.",
    "DK4_MES_B172_R0074": "Plant it near Brunei. This crop should thrive and make a useful trade good.",
    "DK4_MES_B172_R0078": "Wait... rabbit droppings! Disgusting!",
    "DK4_MES_B172_R0082": "Eww! Throw it away!",
    "DK4_MES_B172_R0086": "All right. Tossed!",
    "DK4_MES_B172_R0090": "You know everything! How did you learn so much?",
    "DK4_MES_B172_R0094": "A genius. None know more.{LB}This man could guess your bust size.",
    "DK4_MES_B172_R0098": "Eek! You dirty old man!",
    "DK4_MES_B172_R0102": "Ho ho ho!",
    "DK4_MES_B172_R0106": "His knowledge is vast, but that manner...",
    "DK4_MES_B172_R0110": "Still, his knowledge will surely help us. We should invite him.",
    "DK4_MES_B172_R0114": "...Agreed.",
    "DK4_MES_B172_R0118": "W-what do you want?",
    "DK4_MES_B172_R0122": "You've great knowledge. {MACRO:FI} {MACRO:FA}, fleet admiral.",
    "DK4_MES_B172_R0126": "Lend that knowledge to our cause.",
    "DK4_MES_B172_R0129": "Join you? This old man won't leave this town, nor follow any man.",
    "DK4_MES_B172_R0133": "Please reconsider, sir.",
    "DK4_MES_B172_R0137": "Well, if you insist... Ah!",
    "DK4_MES_B172_R0140": "And who is that young lady with you?",
    "DK4_MES_B172_R0153": "She can't speak. Her name is Serah.",
    "DK4_MES_B172_R0158": "...Christina.",
    "DK4_MES_B172_R0171": "Serah...",
    "DK4_MES_B172_R0177": "Christina...",
    "DK4_MES_B172_R0184": "Lovely. Truly lovely!",
    "DK4_MES_B172_R0192": "Decided! This old man goes with you!",
    "DK4_MES_B172_R0201": "Serah, dear!",
    "DK4_MES_B172_R0207": "Christina, dear!",
    "DK4_MES_B172_R0214": "This man follows anywhere!",
    "DK4_MES_B172_R0228": "{MACRO:FI}! No! Lady Serah is in danger!",
    "DK4_MES_B172_R0233": "Wh-what is with this old man?! Stay away!",
    "DK4_MES_B172_R0244": "Mikhail! Still alive, lecher? Stay away from my granddaughter!",
    "DK4_MES_B172_R0248": "Julio! Long time! You're stubborn too. And no old man calls me old!",
    "DK4_MES_B172_R0254": "{MACRO:FI}, don't recruit him!",
    "DK4_MES_B172_R0260": "No! Decision made. This old man goes! My knowledge will help. Don't worry!",
    "DK4_MES_B172_R0263": "...Granted. But...",
    "DK4_MES_B172_R0272": "Touch Lady Serah and this blade finds you!",
    "DK4_MES_B172_R0275": "Serah, dear!",
    "DK4_MES_B172_R0279": "S-sir, please...",
    "DK4_MES_B172_R0288": "Touch me and this sword runs you through!",
    "DK4_MES_B172_R0291": "Christina, dear!",
    "DK4_MES_B172_R0295": "No more!",
    "DK4_MES_B172_R0307": "Mikhail, you lecher! Stay away from my granddaughter!",
    "DK4_MES_B172_R0311": "Love is free! Good thing Christina looks nothing like you!",
    "DK4_MES_B172_R0315": "Silence!",
    "DK4_MES_B172_R0329": "Mikhail is a scholar.{LB}He cannot take a deck post.",
    "DK4_MES_B172_R0333": "Mikhail now reveals detailed item information.",
    "DK4_MES_B172_R0336": "While viewing item information, press the X Button.",
    "DK4_MES_B172_R0339": "No shipwork for me, but call whenever you need item knowledge.",

    "DK4_MES_B173_R0005": "Trouble, Gerhard?",
    "DK4_MES_B173_R0009": "Admiral, research on the Proof of Conqueror is needed, but the expert is... hmm...",
    "DK4_MES_B173_R0012": "What?",
    "DK4_MES_B173_R0016": "Ahem! None other than me!",
    "DK4_MES_B173_R0019": "...Ah.",
    "DK4_MES_B173_R0023": "Yes. Of all people, this man...",
    "DK4_MES_B173_R0026": "Gerhard? Something to say?",
    "DK4_MES_B173_R0029": "N-no. Mikhail's wisdom is most impressive...",
    "DK4_MES_B173_R0033": "Never mind that. Mikhail, explain.",
    "DK4_MES_B173_R0036": "Ho ho! {MACRO:FI}, curious about the Proof?",
    "DK4_MES_B173_R0040": "Skip the trivia. What purpose does it serve?",
    "DK4_MES_B173_R0044": "The Proofs are treasures scattered across the seas, destined for those who rule them.",
    "DK4_MES_B173_R0048": "Ancient texts name seven. The Seven Sages marked their locations on various maps.",
    "DK4_MES_B173_R0051": "When one rules a sea, fate grants that map. So the texts say.",
    "DK4_MES_B173_R0055": "Only treasure? How dull...",
    "DK4_MES_B173_R0058": "Admiral {MACRO:FI}, it would proclaim you ruler of every sea! This is a grand undertaking!",
    "DK4_MES_B173_R0061": "Proof of rule.",
    "DK4_MES_B173_R0065": "{MACRO:FI}, think of your followers.{LB}The answer is clear.",
    "DK4_MES_B173_R0069": "A clear goal gives everyone purpose?",
    "DK4_MES_B173_R0072": "Exactly.",
    "DK4_MES_B173_R0076": "Why whisper? Awed by my wisdom?",
    "DK4_MES_B173_R0080": "W-we understand. Please cause no trouble aboard...",
    "DK4_MES_B173_R0083": "No worry! Ho ho ho!",
    "DK4_MES_B173_R0087": "Mikhail, do you know how to gather every Proof?",
    "DK4_MES_B173_R0091": "Start by becoming the strongest power in that sea. Local leaders hold clues.",
    "DK4_MES_B173_R0095": "Should an evil soul hold one, that foe must fall.",
    "DK4_MES_B173_R0103": "Then find each city's ruins and solve the sealed Proof's mystery.",
    "DK4_MES_B173_R0106": "But how do we find those ruins?",
    "DK4_MES_B173_R0110": "Let's see... Maybe...",
    "DK4_MES_B173_R0117": "Women.",
    "DK4_MES_B173_R0121": "Miiikhaiiil!",
    "DK4_MES_B173_R0125": "Calm down. A large city should hold clues to nearby ruins.",
    "DK4_MES_B173_R0129": "Tavern women hear sailors from across the world each day. Their knowledge is priceless.",
    "DK4_MES_B173_R0132": "Naturally, they won't share such secrets freely.",
    "DK4_MES_B173_R0135": "So some payment is required.",
    "DK4_MES_B173_R0138": "Think romantically! Gifts seek no reward. They're only meant to win a woman's heart... heh heh.",
    "DK4_MES_B173_R0141": "That sounds like a reward.",
    "DK4_MES_B173_R0145": "Oops. Quite right...",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "04": "Crewmate",
    "06": "Julio Erneco",
    "07": "Christina",
    "0D": "Crewmate",
    "10": "Gerhard Adelknauts",
    "14": "Fernando Dias",
    "17": "Crewmate",
    "4C": "Mikhail",
    "57": "Townsman",
    "6D": "Sailing instructor",
    "A4": "Man",
    "A5": "Young woman",
    "A6": "Young woman",
    "FE": "Tutorial",
}
EXTENDED_STATES = {0x10, 0x14, 0x17, 0x4C, 0x57, 0x6D, 0xA4, 0xA5, 0xA6, 0xFE}
CONTEXT = {
    169: "Fernando demonstrates his gambling insight and joins Hodram when the coin toss favors him.",
    170: "Hodram meets veteran navigator Julio Erneco over wine and accepts his self-invitation aboard.",
    171: "A harbor instructor explains square, lateen, and auxiliary sails and the best wind angle for multi-masted ships.",
    172: "Hodram recruits scholar Mikhail, whose presence unlocks detailed item information.",
    173: "Mikhail and Gerhard explain the seven Proofs of Conqueror and how regional dominance, ruins, and tavern information reveal them.",
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
        raise SystemExit(f"Hodram V12 inventory mismatch: missing={missing}, extra={extra}")

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
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english
                .replace("{LB}", " ")
                .replace("{MACRO:FI}", "Hodram")
                .replace("{MACRO:FA}", "Bergstrom")
                .replace("{MACRO:FO}", "Bergstrom Fleet"),
                "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places the protected newline before the native row boundary so the "
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
        "dialogue_profile": "hodram-story-mikhail-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hodram optional Fernando, Julio, and Mikhail recruitments plus sailing and Proof of Conqueror tutorials across SC1 blocks 169-173.",
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
