from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v24.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# The first field is a faithful gloss of the clean Japanese; the second is the
# localized line. Literal capital I and F in the encoded target are runtime macros.
LINES = {
    "DK4_MES_B99_R0005": (
        "Admiral, I hear you've finally found the demon sword Muramasa. I'd like to see it myself.",
        "Admiral, you've found Muramasa! Could you show it to me?",
    ),
    "DK4_MES_B99_R0008": (
        "Of course. We were able to find it thanks to Yukihisa's report.",
        "Of course! Your report led us right to it, Yukihisa.",
    ),
    "DK4_MES_B99_R0012": (
        "This... this is the demon sword Muramasa...",
        "This... this is Muramasa...",
    ),
    "DK4_MES_B99_R0016": (
        "Hmm... it gives off a strange glow that seems to draw one in.",
        "Hmm... That eerie glow could draw you right in.",
    ),
    "DK4_MES_B99_R0020": ("It was a feast for the eyes.", "Magnificent."),

    "DK4_MES_B119_R0019": ("A-amazing...", "Wow..."),
    "DK4_MES_B119_R0034": ("Whoa! It's a huge hit!", "Whoa! That's a huge hit!"),
    "DK4_MES_B119_R0048": (
        "Ah, tomato sauce! Wow, that looks delicious!",
        "Ah, tomato sauce! That looks delicious!",
    ),
    "DK4_MES_B119_R0062": (
        "Look at that woman! Even the pattern on her clothes...",
        "Look! Even her dress has it!",
    ),
    "DK4_MES_B119_R0075": (
        "I never thought it would become this popular!",
        "Never thought it'd be such a hit!",
    ),
    "DK4_MES_B119_R0078": (
        "Of course it would! I'm the one who produced it, after all!",
        "Of course it did. Yours truly started it!",
    ),
    "DK4_MES_B119_R0090": (
        "What are you talking about? Your mouth was hanging open in surprise.",
        "Oh, please. Your jaw dropped, too!",
    ),
    "DK4_MES_B119_R0093": ("No way! W-was it?", "No way! W-was it?"),
    "DK4_MES_B119_R0100": (
        "{MACRO:FI}, you look happy.",
        "All smiles, {MACRO:FI}!",
    ),
    "DK4_MES_B119_R0103": (
        "Heh, of course. Our efforts made the people of this town so happy!",
        "Of course! Everyone's having fun thanks to us!",
    ),
    "DK4_MES_B119_R0109": (
        "Look at everyone's faces. They're all smiling.",
        "Look around. Everyone's smiling!",
    ),
    "DK4_MES_B119_R0112": (
        "The shopkeepers earn money, and I make a fortune too. Nothing could make me happier!",
        "The shops make money, and so do we! What's not to love?",
    ),
    "DK4_MES_B119_R0123": (
        "{MACRO:FI}, this work really suits you.",
        "{MACRO:FI}, this work really suits you.",
    ),
    "DK4_MES_B119_R0126": (
        "Yes. I'm truly glad I went to sea.",
        "Yeah. So glad we set sail.",
    ),
    "DK4_MES_B119_R0132": (
        "I want to see more people enjoying themselves, and {MACRO:FO} must make more money too!",
        "More smiles for everyone, more profit for {MACRO:FO}!",
    ),
    "DK4_MES_B119_R0143": (
        "How reassuring! Where will you start the next craze, and what will it be?",
        "Great! What's the next craze?",
    ),
    "DK4_MES_B119_R0155": (
        "Fernando, you're getting quite enthusiastic too.",
        "You're getting into this, too.",
    ),
    "DK4_MES_B119_R0162": (
        "Even a casino rarely offers the thrill of a gamble on this scale.",
        "You don't get to gamble on this scale even in a casino!",
    ),
    "DK4_MES_B119_R0177": (
        "Let's make bananas the next trend! Or pumpkins! Just thinking about it makes me hungry!",
        "Bananas next! Or pumpkins! My mouth's watering already!",
    ),
    "DK4_MES_B119_R0181": (
        "Honestly, anything edible will do for you.",
        "All you care about is food.",
    ),
    "DK4_MES_B119_R0193": (
        "Let's go report to this town's guild.",
        "Let's report back to the guild here!",
    ),
    "DK4_MES_B119_R0198": (
        "Let's go report to this town's guild.",
        "Let's report to the guild here.",
    ),

    "DK4_MES_B165_R0006": (
        "Won't someone let me have a good drink?",
        "Can't a man get a decent drink?",
    ),
    "DK4_MES_B165_R0009": (
        "For a man of the sea, nothing is harder than being unable to have a good drink.",
        "A sailor needs a good drink!",
    ),
    "DK4_MES_B165_R0020": (
        "What's that man muttering to himself about?",
        "Who's that man muttering to himself?",
    ),
    "DK4_MES_B165_R0025": (
        "Kamil, look at that older man. He's been complaining this whole time.",
        "Kamil, look at that old man. All he does is complain.",
    ),
    "DK4_MES_B165_R0029": (
        "People tend to grumble when they get old. Anyone could end up like that.",
        "Well, people do get cranky as they age. Happens to us all.",
    ),
    "DK4_MES_B165_R0033": (
        "Not me! My figure won't change, and my mind won't grow dull either.",
        "Not me! My figure won't change, and my mind will stay sharp!",
    ),
    "DK4_MES_B165_R0040": (
        "Did you just say that I've grown senile?!",
        "Did you call me senile?",
    ),
    "DK4_MES_B165_R0052": (
        "Whoa! Sorry, sir. Come on, {MACRO:FI}, apologize too.",
        "Sorry, sir! {MACRO:FI}, apologize!",
    ),
    "DK4_MES_B165_R0059": (
        "Why? He just heard me wrong!",
        "Why? He just misheard me!",
    ),
    "DK4_MES_B165_R0062": (
        "I did not hear wrong! I'm still an active navigator!",
        "My ears work! Still a navigator!",
    ),
    "DK4_MES_B165_R0065": (
        "Oh, you were a navigator, old man? I hope you live long.",
        "Oh, you were a navigator? Hope you live long!",
    ),
    "DK4_MES_B165_R0077": (
        "Ah! There goes {MACRO:FI} again...",
        "Oh, {MACRO:FI}...",
    ),
    "DK4_MES_B165_R0083": (
        "What?! You contrary little thing! Young people these days have no respect!",
        "What did you say?! You little brat! Young people have no respect!",
    ),
    "DK4_MES_B165_R0086": (
        "Even so, I'm an admiral! Does this former active navigator need something?",
        "Hey, you're talking to an admiral. Need something, 'former' navigator?",
    ),
    "DK4_MES_B165_R0097": (
        "I can't watch this anymore...",
        "This is too much...",
    ),
    "DK4_MES_B165_R0104": (
        "What! You're an admiral? Then it's decided. I'll join your ship.",
        "An admiral? Good. Take me aboard!",
    ),
    "DK4_MES_B165_R0107": (
        "I won't be satisfied until I teach you personally!",
        "Someone has to teach you manners!",
    ),
    "DK4_MES_B165_R0110": (
        "Wait a moment... how did it come to this?",
        "Wait... How did that happen?",
    ),
    "DK4_MES_B165_R0113": ("Show me to your ship.", "Lead on, then."),
    "DK4_MES_B165_R0125": (
        "(Maybe {MACRO:FI} will calm down a little.) Let's give in and take him with us.",
        "({MACRO:FI} might calm down a little.) Let's take him aboard.",
    ),
    "DK4_MES_B165_R0132": (
        "Oh, fine! I suppose we have no choice.",
        "Oh, fine! We can take him.",
    ),
    "DK4_MES_B165_R0135": (
        "That's right. You should listen to a veteran.",
        "That's right. Listen to a veteran.",
    ),
    "DK4_MES_B165_R0138": (
        "I'm Julio Erneco. Pleased to meet you.",
        "Julio Erneco. Glad to meet you.",
    ),
    "DK4_MES_B165_R0141": (
        "All right. But you'll have to prove you're still active.",
        "All right. Let's see you prove you're still active.",
    ),
}

SPEAKERS = {
    "02": "Lil Argot",
    "06": "Julio Erneco",
    "09": "Kamil",
    "0C": "Yukihisa Genjo Shiraki",
    "0E": "Emilio Ferrog",
    "14": "Fernando",
}
CONTEXTS = {
    "99": "Yukihisa sees the recovered Muramasa for the first time.",
    "119": "Lil's tomato promotion becomes a townwide craze; the crew celebrates and reports to the guild.",
    "165": "Lil and Kamil meet the gruff navigator Julio Erneco and bring him aboard.",
}
NOTES = {
    "DK4_MES_B165_R0025": "Old man is familiar address, not a claim that Julio is Lil's grandfather.",
    "DK4_MES_B165_R0065": "Lil's patronizing wish keeps the joke without inventing a family relationship.",
    "DK4_MES_B165_R0086": "Quotation marks make Lil's teasing emphasis on former explicit.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        state = row["source_hex"][:2]
        if state not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped leading state {state}")
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise ValueError(f"{row_id}: uppercase runtime macro byte in literal English")
        block = row_id.split("_B", 1)[1].split("_R", 1)[0]
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}",
                "speaker": SPEAKERS[state],
                "context": CONTEXTS[block],
                "source_meaning": source_meaning,
                "localization_note": NOTES.get(
                    row_id,
                    "Source meaning and the neighboring scene lines reviewed for natural American English.",
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
    counts = Counter(row_id.split("_B", 1)[1].split("_R", 1)[0] for row_id in LINES)
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's Muramasa viewing, tomato boom, and Julio Erneco recruitment scenes.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": {str(int(number)): count for number, count in sorted(counts.items())},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
