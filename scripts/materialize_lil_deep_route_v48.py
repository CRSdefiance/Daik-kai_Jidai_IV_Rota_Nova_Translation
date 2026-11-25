from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v48.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("Uncle, make us something to eat. I'm starving.", "Hey, cook us something! We're starving!"),
    17: ("I'm starving too. My stomach feels stuck to my back.", "Me too... My stomach's growling!"),
    28: ("Me too.", "Me too!"),
    38: ("I'm out of ingredients. I can make a drinking snack if that will do.", "Sorry, we're low on supplies. Would a snack do?"),
    41: ("Why have you run out of ingredients at this hour?", "Why's the kitchen empty already?"),
    52: ("No, we'll die of hunger!", "N-no! We're gonna starve!"),
    64: ("I don't want to die hungry!", "Don't let me die hungry!"),
    74: ("That gentleman bought almost everything.", "He bought nearly all our food..."),
    77: ("Almost everything?", "Nearly all?!"),
    81: ("Bring more food. I have plenty of money.", "Ho ho ho! Bring more food! There's plenty of money!"),
    85: ("Sorry to keep you waiting.", "Your order's here."),
    89: ("What a cute girl. I want to touch you.", "Ho ho! Pretty girl! Can't keep my hands off!"),
    92: ("Ah, Lord Nagalpur!", "Ah! Lord Nagalpur!"),
    96: ("I'll give you a tip. Here, take it.", "Ho ho! A tip for you. Take it!"),
    99: ("With money, anything is possible. What a wonderful paradise.", "Ho ho ho! Money makes anything possible! What a paradise!"),
    111: ("Paradise? Only inside that head of yours.", "Paradise? Only in your own head!"),
    126: ("I can't stand that man.", "What a creep..."),
    133: ("Hey, you!", "Hey, you!"),
    137: ("A new barmaid? You're not as attractive as the others.", "New barmaid? The others are prettier."),
    141: ("Well, you will do. Come here.", "Still, you'll do. Come here."),
    145: ("Plain? How rude! You have no right to judge me.", "Plain? How rude! You have no right to judge me!"),
    156: ("Plain is too harsh. Call her somewhat below average.", "Yeah! 'Plain' is too harsh! She's just below average!"),
    168: ("That's right.", "Exactly!"),
    175: ("Are you praising me or insulting me?", "Hey! Was that praise or an insult?"),
    181: ("Even your angry face is charming. I'll give you a tip. What's your name?", "Ho ho! A charming scowl! Take this tip. Your name?"),
    192: ("He dares to mock our admiral.", "He dares mock our admiral..."),
    198: ("You've got it wrong. I'm FI. Any merchant should know my name.", "Wrong! My name's {MACRO:FI}. Any merchant knows that name!"),
    201: ("I don't know you, nor do I care. Money is all that interests me.", "Never heard of you. Why care? Only money interests me."),
    205: ("How can you be a merchant while knowing nothing of the world?", "So ignorant! How are you a merchant?"),
    208: ("FI, you said you're a merchant?", "{MACRO:FI}? You call yourself a merchant?"),
    211: ("Yes, I am.", "Yes!"),
    215: ("Then you know the value of money. It lets you do anything.", "Then you know the value of money. With enough, you can do anything."),
    219: ("You're a fool. Some things cannot be bought with money.", "You're a fool! There are things money can't buy!"),
    231: ("FI, you've grown so much.", "(Wow, {MACRO:FI}! You've really grown!)"),
    245: ("What a fine quote, Admiral. I'll note it for my poetry collection.", "Well said, Admiral! One for my poetry notes!"),
    252: ("Money buys power, goods, everything. The world runs on money.", "You fool! Money buys power and goods. This world runs on cash!"),
    255: ("I'm telling you, some things cannot be bought with money.", "Money can't buy everything, remember?"),
    258: ("What if I offered your sailors and officers five times your wages?", "What if your crew got five times your pay? Would they stay?"),
    270: ("He's rotten to the core. There's no saving him.", "Rotten to the core... There's no saving him."),
    280: ("Many people would be tempted by that offer.", "Many would take that offer. Ho ho!"),
    283: ("Some people won't be bought. Money can't buy everything.", "...Some people won't be bought! Money can't buy everything!"),
    287: ("Stubborn girl. I could bring your entire company under mine.", "Stubborn girl! Maybe your whole company should work under me."),
    291: ("I won't let you do that.", "That won't happen!"),
    295: ("You'll learn what happens soon enough.", "Careful what you say. You'll learn soon enough."),
    298: ("You're the one who'll learn.", "You're the one who'll learn!"),
    302: ("When your company becomes mine, I'll make you a servant. There's plenty of work.", "Once your company's mine, you can serve me. There's plenty of work."),
    306: ("Stop fooling around. You'll regret this later.", "Enough of this nonsense! You'll regret it!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio Ferrog", 0x10: "Gerhard",
    0x11: "Al", 0x14: "Fernando Dias", 0x16: "Samwell", 0x17: "Manuel Almeida",
    0x26: "Nagalpur", 0x5C: "Barkeep", 0xC6: "Barmaid",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B137_")}
    authored = {f"DK4_MES_B137_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B137 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B137_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Lil's hungry crew meets the wealthy merchant Nagalpur in a tavern. "
                "He harasses a barmaid and Lil, boasts that money can buy anything, "
                "and threatens to take over Lil's company."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B137 Japanese; preserves Nagalpur's established name, "
                "his predatory behavior, Fernando's teasing, the fivefold-wage challenge, "
                "Lil's reply and all FI name macros. Source 26 and C6 are presentation selectors. "
                "Guarded wrapping protects first and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 47 B137 Lil-versus-Nagalpur tavern confrontation records.",
        "inventory": {"identified_records": 47, "translated_records": len(records), "blocks": {"137": 47}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
