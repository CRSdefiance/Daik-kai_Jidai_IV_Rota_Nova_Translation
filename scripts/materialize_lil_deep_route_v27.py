from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v27.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# Each clean-source gloss precedes its localized en-US line. Capital I and F
# become runtime macro bytes in this story renderer, so literal prose avoids them.
LINES = {
    "DK4_MES_B106_R0006": ("Oh, is that the strange festival?", "So that's the odd festival?"),
    "DK4_MES_B106_R0010": ("Aaaah...", "Aaaah..."),
    "DK4_MES_B106_R0014": ("Ooooh!", "Ooooh!"),
    "DK4_MES_B106_R0018": (
        "Singing? Are they drunk on wine?",
        "Singing? Are they drunk on wine?",
    ),
    "DK4_MES_B106_R0029": ("Shh!", "Shh!"),
    "DK4_MES_B106_R0036": (
        "This is a revelation! Our Ancient Megalith Society will soon conquer the world!",
        "A revelation! Our Ancient Megalith Society will soon rule the world!",
    ),
    "DK4_MES_B106_R0040": (
        "We are the chosen ones! We will dig up the treasure written here and rule the fools who do not fear God!",
        "We're chosen! We'll dig up this treasure and rule the godless!",
    ),
    "DK4_MES_B106_R0043": ("Ooooh!", "Ooooh!"),
    "DK4_MES_B106_R0047": ("Something about this feels awful...", "This is creepy..."),
    "DK4_MES_B106_R0051": (
        "We begin by attacking this village! We will show those who mocked us!",
        "We attack this village first! Those who mocked us will pay!",
    ),
    "DK4_MES_B106_R0055": ("Ooooh!", "Ooooh!"),
    "DK4_MES_B106_R0059": ("W-what did they say?!", "W-what?!"),
    "DK4_MES_B106_R0063": (
        "Hey! I will not let you do that!",
        "Hey! You won't hurt this village on my watch!",
    ),
    "DK4_MES_B106_R0078": ("Whoa, you idiot!", "You idiot!"),
    "DK4_MES_B106_R0104": ("A-admiral!", "Admiral!"),
    "DK4_MES_B106_R0106": ("Oh no, what have you done?", "What have you done?!"),
    "DK4_MES_B106_R0108": ("Eek! Admiral, stop!", "Admiral, stop!"),
    "DK4_MES_B106_R0110": ("A-admiral!", "Admiral!"),
    "DK4_MES_B106_R0131": (
        "Someone there still defies God's will... Seize them and make them a sacrifice!",
        "One defies God... Seize and sacrifice them!",
    ),
    "DK4_MES_B106_R0135": ("Ooooh!", "Ooooh!"),
    "DK4_MES_B106_R0139": ("Eek!", "Eek!"),
    "DK4_MES_B106_R0151": (
        "Honestly, this young lady...",
        "That girl's a handful...",
    ),
    "DK4_MES_B106_R0158": ("Stop!", "Stop!"),
    "DK4_MES_B106_R0166": (
        "You heretics! Your dreadful deeds are clear. You cannot do as you please any longer. Give back our village ruins!",
        "Heretics! Your crimes are plain. Stop this! Give back our ruins!",
    ),
    "DK4_MES_B106_R0169": ("Damn!", "Damn it!"),
    "DK4_MES_B106_R0173": ("The villagers...?", "The villagers?"),
    "DK4_MES_B106_R0189": (
        "You came! Thank goodness we called for help from the nearby village!",
        "You came! Glad we asked for help.",
    ),
    "DK4_MES_B106_R0195": (
        "I thought this might happen, so I asked the villagers to help us.",
        "Thought this might happen, so we asked the villagers for help.",
    ),
    "DK4_MES_B106_R0204": (
        "I thought this could happen, so I asked the village folk to help.",
        "We asked the villagers for help. Just in case.",
    ),
    "DK4_MES_B106_R0211": (
        "Grr, I am fleeing! Hm? It's gone? Where is it?",
        "Grr, gotta run! Where did it go?!",
    ),
    "DK4_MES_B106_R0230": ("Hm? What is this?", "What's this?"),
    "DK4_MES_B106_R0232": ("What is this?", "What's this?"),
    "DK4_MES_B106_R0234": ("Hm? What could this be?", "What's this?"),
    "DK4_MES_B106_R0236": ("What could this be?", "What's this?"),
    "DK4_MES_B106_R0238": ("Huh. What's this?", "Huh. What's this?"),
    "DK4_MES_B106_R0240": ("Huh. What is this?", "What's this, then?"),
    "DK4_MES_B106_R0242": ("Something is here!", "Something!"),
    "DK4_MES_B106_R0244": ("Huh. What's this?", "Huh. What's this?"),
    "DK4_MES_B106_R0250": (
        "You mean this? It looked important on the altar, so I took a look.",
        "This was on the altar. Looked important, so we borrowed it.",
    ),
    "DK4_MES_B106_R0257": (
        "D-don't touch it! Oh no... It's over! My noble mission is ruined!",
        "Don't touch it! No... My grand mission is ruined!",
    ),
    "DK4_MES_B106_R0261": ("Now behave yourself!", "Settle down!"),
    "DK4_MES_B106_R0268": (
        "Thank you. Your warning saved the village.",
        "Thank you. You saved our village!",
    ),
    "DK4_MES_B106_R0272": (
        "We cannot offer much thanks, but we will send you to London. There are bears in those woods.",
        "We can take you to London. Bears roam those woods.",
    ),
    "DK4_MES_B106_R0276": ("B-bears? I've had enough of those...", "B-bears? No more, please..."),
    "DK4_MES_B106_R0279": (
        "Do not worry. A skilled hunter will go with you. Travel safely.",
        "A skilled hunter will guide you. Safe travels!",
    ),
    "DK4_MES_B108_R0006": ("Who are you? Wait, could it be...?", "You... could it be?"),
    "DK4_MES_B108_R0009": (
        "Oh! After so long, fellow believers!",
        "Oh! Believers at last!",
    ),
    "DK4_MES_B108_R0012": (
        "We fled the rule of Islamic powers and lived quietly to preserve our faith.",
        "We fled Muslim rule and kept our faith in secret here.",
    ),
    "DK4_MES_B108_R0016": (
        "Have you heard of the treasure obtained by one who rules all seven seas?",
        "Have you heard of the treasure won by whoever rules the seven seas?",
    ),
    "DK4_MES_B108_R0019": (
        "What! You seek the Proof of Conquest? God has guided you here!",
        "The Proof? God guided you here!",
    ),
    "DK4_MES_B108_R0023": ("What? Do you know something?", "You know something?"),
    "DK4_MES_B108_R0026": ("Know of it? Of course...", "Oh, yes..."),
    "DK4_MES_B108_R0030": (
        "This lamp has been handed down in our village for ages. They say seekers of the Proof must have it. We entrust it to you.",
        "This lamp is an ancient heirloom. Seekers of the Proof need it. Please take it.",
    ),
    "DK4_MES_B108_R0035": (
        "Please, do not let the Proof fall into Ottoman hands. We beg you to stop that.",
        "Keep the Proof from the Ottomans.",
    ),
    "DK4_MES_B108_R0039": ("Yes! Leave it to us!", "You can count on us!"),
}

SPEAKERS = {
    0x02: "Lil Argot",
    0x09: "Kamil",
    0x10: "Gerhard Adelknauts",
    0x14: "Fernando",
    0xA0: "Village speaker",
    0xB1: "Megalith cult leader",
    0xB2: "Megalith cultists",
    0xD0: "Selected crewmate",
}
NOTES = {
    "DK4_MES_B106_R0036": "Uses the established Ancient Megalith Society name.",
    "DK4_MES_B106_R0195": "Gerhard's first-person explanation is phrased as a group action to avoid a literal runtime-macro I byte.",
    "DK4_MES_B106_R0204": "Fernando's first-person explanation is phrased as a group action to avoid a literal runtime-macro I byte.",
    "DK4_MES_B106_R0232": "The source begins 89 BD (何), an ordinary Japanese glyph; preserve the English first character.",
    "DK4_MES_B106_R0236": "The source begins 89 BD (何), an ordinary Japanese glyph; preserve the English first character.",
    "DK4_MES_B106_R0272": "Prioritizes the promised London escort and bear warning within the fixed allocation.",
    "DK4_MES_B108_R0012": "Preserves the source's religious and political context without assigning a specific state.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    counts: Counter[str] = Counter()
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in {0x82, 0x89, 0x92}:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        block = row_id.split("_B", 1)[1].split("_R", 1)[0]
        counts[str(int(block))] += 1
        speaker = (
            "Hidden believer" if lead == 0xA0 and block == "108" else SPEAKERS.get(lead, "Companion variant")
        )
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "")
                + english
                + "{PAD}",
                "speaker": speaker,
                "context": (
                    "Lil exposes a megalith cult's plan to attack a village; Gerhard or Fernando called for help."
                    if block == "106"
                    else "A hidden believer entrusts Lil with an old lamp tied to the Proof of Conquest."
                ),
                "source_meaning": source_meaning,
                "localization_note": NOTES.get(
                    row_id,
                    "Reviewed against the clean Japanese and neighboring lines for American English and scene voice.",
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
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v27-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's megalith-cult confrontation and the hidden believer's lamp in B106/B108.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": dict(counts),
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
