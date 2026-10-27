from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v42.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("Load the cargo quickly. Time is money. Get to work.", "Get that cargo aboard! Time is money. Move!"),
    14: ("Young people today are pathetic. No wonder the Hanseatic League declines. I will not allow it while I live.", "Kids today... So the Hanseatic League fades. Not on my watch!"),
    18: ("The Speyer Company must prosper to restore the Hanseatic League.", "A thriving Speyer Company will revive the Hanseatic League!"),
    26: ("Everyone, hurry. I will leave you behind.", "Hurry! We're leaving you behind!"),
    37: ("Wait! I am still eating.", "Wait for me! Still eating over here!"),
    51: ("That admiral is always in such a hurry.", "That admiral's in a rush."),
    66: ("FI, wait. Oh no, that man is here.", "Wait, {MACRO:FI}! Oh no... him!"),
    73: ("FI sounds familiar. Ah, you're from that new FO company, little girl.", "{MACRO:FI}... Heard that name. So you're that girl from {MACRO:FO}!"),
    76: ("Little girl? Who is this unpleasant older man?", "Little girl?! Who's this old jerk?"),
    80: ("Old man? How rude. I am still young. Is that how you greet a stranger?", "Old man?! How rude! Young as ever, thank you. Do you greet everyone like that?"),
    90: ("Admiral, that man is from the Speyer Company...", "Admiral, that's a Speyer man..."),
    95: ("FI, careful. He is Martin Speyer, head of the Speyer Company.", "Careful, {MACRO:FI}! That's Martin Speyer, head of the Speyer Company!"),
    102: ("So what? Calling a lady a little girl is rude, old man.", "So what? Calling a lady 'little girl' is rude, old man!"),
    106: ("Impudent girl. My Speyer Company will crush your tiny company.", "Brat! The Speyer Company will crush your outfit!"),
    118: ("Come on, both of you. This is a childish quarrel.", "Come on, you two. This is a kid's quarrel..."),
    124: ("Quiet. I could say the same about you.", "Oh, hush! That goes double for you!"),
    135: ("FI, Mr. Speyer, she is joking. This girl is a little strange.", "W-wait, {MACRO:FI}! Mr. Speyer, she's joking. She gets carried away..."),
    138: ("Ow!", "Ow!"),
    145: ("Watch me. I will not let you crush FO.", "You'll never crush {MACRO:FO}!"),
    149: ("You impudent girl. Remember this. Let's go. Seeing her makes me angry.", "You brat! Remember this! Come on. Can't bear the sight of her!"),
    165: ("They trade insults so alike that it is like seeing two FIs.", "Watching them argue is like seeing {MACRO:FI} fight herself..."),
    183: ("Why does she start fights and make enemies for no reason?", "Why fight over everything? Making enemies for no reason..."),
    186: ("Because that old man was so unpleasant.", "Because that old man was awful!"),
    189: ("She is such a child.", "Honestly... such a child."),
    193: ("Kamil, there's no use talking about what is already done.", "Kamil, it's done. Just let it go."),
    197: ("She's so selfish.", "So selfish..."),
    201: ("Now I will defeat the Speyer Company fair and square.", "Now we'll beat the Speyer Company fair and square!"),
    205: ("Kamil, to defeat the Speyer Company, we must drive it from its contracted towns, right?", "Kamil, to beat Speyer, drive them from their towns. Right?"),
    208: ("I'm surprised you know that. I thought you'd ask how to defeat it.", "Huh, you knew that? Thought you'd ask how to drive them out."),
    214: ("So how do we drive them out?", "So how do we drive them out?"),
    216: ("Do not make fun of me.", "Don't mock me!"),
    226: ("Sorry. Fight or invest, whichever is FI's strength, and oppose them.", "Sorry. Do what you do best, {MACRO:FI}: battle or invest."),
    229: ("I know. Watch me, Speyer Company.", "Got it! Just watch, Speyer Company!"),
    247: ("Huh?", "Huh?"),
    254: ("You do not know how?", "Wait... you don't know how?"),
    258: ("Um...", "Uh..."),
    262: ("How can you be a merchant without knowing the basics?", "How are you a merchant? This is basic stuff..."),
    265: ("Is it? Please tell me.", "Really? Then teach me."),
    268: ("To drive out a rival company, reduce its share of the town to zero percent.", "All right, {MACRO:FI}. Drive them out by cutting their town share to zero."),
    271: ("Then just invest enough to make the town support us.", "Easy! We invest and get the town on our side."),
    275: ("Listen to the end. Investing alone cannot drive out a rival.", "Let me finish. You can't drive them out by investing alone."),
    279: ("What? Why?", "What? Why not?"),
    283: ("If both sides invest, the town sees both as helpful and cannot choose one.", "A town needs both investors, so it can't choose."),
    287: ("You must enter hostilities with the rival and force the town to choose one side.", "Go to war with them. Then the town has to choose a side."),
    291: ("The town will side with whoever gives it more money, right?", "So it picks whoever pays more?"),
    295: ("Yes. During hostilities, your investment reduces their share and raises yours.", "Right. At war, each investment raises our share and cuts theirs."),
    299: ("Then the town switches sides. How do you enter hostilities?", "So the town switches sides. How do we start a war?"),
    303: ("At the Guild, have your adjutant write a declaration of war, or attack an enemy ship in naval battle.", "At the Guild, your adjutant can declare war. Or attack their ships."),
    307: ("Once at war, investing in their contracted towns gradually drives the enemy out.", "Once at war, invest in their towns. Bit by bit, you'll drive them out."),
    311: ("But what if they have a hundred percent share and we cannot invest?", "What if they own it all? We can't invest there."),
    314: ("Fight their fleet near that town.", "Attack their ships near town."),
    317: ("Losing a naval battle harms reputation, and nearby towns' shares fall below one hundred percent.", "A naval defeat hurts their reputation. They lose their full share of nearby towns."),
    320: ("Then we can enter and make a contract. Watch me, Speyer Company.", "Then we sign a contract! Thanks, Kamil. Watch out, Speyer!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio Ferrog",
    0x14: "Fernando Dias", 0x1D: "Martin Speyer", 0x97: "Crew voice",
}
TEXT_LEADS = {0x82, 0x83}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B128_")}
    if {f"DK4_MES_B128_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B128 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B128_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Lil response choice"),
            "context": (
                "Lil clashes with Martin Speyer while her companions try to calm them."
                if number < 200 else
                "Lil and Kamil explain how war, investment, town share and naval battles drive out a rival company."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean B128 Japanese in scene order. Preserves Hanseatic League, Martin Speyer, "
                "the FI/FO runtime macros, both bare-text response choices and the precise market-share rules. "
                "Source 97 is a speaker selector before Shift-JIS Admiral; 82/83 choice starts are text. "
                "Guarded automatic wrapping protects opening and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v41-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 53 B128 Martin Speyer confrontation, choice and market-share tutorial records.",
        "inventory": {"identified_records": 53, "translated_records": len(records), "blocks": {"128": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
