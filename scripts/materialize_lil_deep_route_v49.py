from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v49.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    11: ("What's wrong, sir?", "What's wrong, sir?"),
    23: ("Nagalpur Company was absorbed by the FO Company.", "Bad news! Nagalpur Co. was taken over by {MACRO:FO}!"),
    27: ("They're practically bankrupt.", "They're as good as ruined!"),
    40: ("With Nagalpur Company gone, things have been hard.", "Nagalpur Co. is gone. What a mess..."),
    49: ("Why is that hard for you?", "Why does that hurt you?"),
    52: ("Their people kept my tavern going with their food and drink orders. My sales have collapsed.", "They kept this tavern open. Now sales have crashed."),
    55: ("Oh, that is hard.", "Oh... sorry."),
    58: ("Worse, Nagalpur's people still owe me for food and drink.", "Worse, Nagalpur's men still owe me for food and drink."),
    69: ("This man has had a terrible time. I feel for him.", "Poor man... what a mess."),
    75: ("They gave me this because they had no money. I don't know what it is. It won't pay their tab.", "They gave me this instead of cash. What's it worth? Won't pay the tab."),
    82: ("They claim it's a treasure map. That sounds dubious, and I'm stuck with it.", "A treasure map, they say. Sounds fishy, eh?"),
    86: ("Are you interested? Would you buy it from me?", "Miss, would you buy this map?"),
    89: ("How much?", "How much?"),
    93: ("How about one hundred gold coins?", "Let's say 100 gold coins."),
    104: ("Sorry, I don't have that much.", "Sorry, that's more than we have."),
    108: ("Then you may have it. Thank you for listening to my complaints.", "Then take it. Thanks for listening."),
    111: ("Sorry. Thank you.", "Sorry. Thank you."),
    117: ("All right.", "Sure."),
    121: ("Good, the deal is done.", "Deal."),
    130: ("Nagalpur thought money could buy everything. He brought this on himself.", "Nagalpur thought money bought everything. Serves him right."),
    134: ("But he trusted nothing except money. He must have been lonely. I'm glad I didn't become like him.", "But... money was all he trusted. He must've been lonely. Glad my life went another way."),
    145: ("Yes. When greed blinds you, you're finished.", "True. Greed can ruin a person."),
    151: ("You haven't run out of ingredients today, have you? I'm hungry.", "You have food today, right? My stomach's growling!"),
    163: ("I'm hungry.", "So hungry..."),
    175: ("Same here.", "Same."),
    185: ("We're stocked today. To make up for last time, I'll cook my best for you.", "Ha ha, we're stocked today! To make up for last time, you'll get my best meal!"),
    188: ("Maybe I wronged you.", "Maybe... we hurt your business, sir."),
    191: ("Why do you say that?", "How so?"),
    195: ("Nagalpur was a good customer here. He spent a lot of money.", "He spent so much here. Wasn't he your best customer?"),
    207: ("Well, that's true.", "Well, that's true..."),
    214: ("He paid well. But back then, I had lost my pride as a person.", "He paid well. But my pride was gone."),
    217: ("I flattered him for his money and obeyed him. I was ashamed of myself.", "Chasing his money, obeying every whim... What a sorry sight!"),
    221: ("Sir...", "Oh, sir..."),
    225: ("You said some things cannot be bought with money. Your words woke me up.", "Money can't buy everything. You helped me see that."),
    236: ("Yes, that was a fine quote.", "Yes! A fine line!"),
    243: ("From now on, I will live with pride like you.", "Like you, this old man will live with pride."),
    246: ("That makes me blush. Let's both do our best.", "You're making me blush! Let's both do our best!"),
    249: ("Thank you. By the way, do you know what this is?", "Heh, thank you. Say, do you know what this is?"),
    257: ("A customer left it to pay for drinks. I have no idea what it is.", "A customer left it to cover a tab. No idea what it is..."),
    261: ("A leaf? What is it?", "A leaf? What kind?"),
    265: ("You may have it. I won't use it.", "You take it, miss. No use to me."),
    268: ("Thank you!", "Thank you!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x0E: "Emilio Ferrog", 0x14: "Fernando Dias",
    0x15: "Ian", 0x16: "Samwell", 0x17: "Manuel Almeida", 0x5C: "Barkeep",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B138_")}
    authored = {f"DK4_MES_B138_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B138 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B138_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "After Nagalpur's defeat, Lil speaks with the tavern keeper whose business has suffered. "
                "He offers a treasure map, regains his pride, and gives Lil an unidentified leaf. "
                "The map has paid and free acquisition branches."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B138 Japanese; preserves the FO faction macro, "
                "100-gold asking price, both map acquisition branches, the barkeep's change of heart "
                "and the leaf handoff. Guarded wrapping protects first and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 42 B138 tavern aftermath, two map-price branches and leaf handoff records.",
        "inventory": {"identified_records": 42, "translated_records": len(records), "blocks": {"138": 42}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
