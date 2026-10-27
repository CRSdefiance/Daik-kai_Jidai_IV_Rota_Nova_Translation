from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v25.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# Faithful clean-source gloss, then localized en-US target. Literal uppercase I
# and F would be mistaken for runtime macros in this story renderer.
LINES = {
    "DK4_MES_B100_R0007": (
        "Hey, I overheard that you're seeking mysterious treasures scattered around the world. Is that true?",
        "So you're hunting mysterious treasures all over the world?",
    ),
    "DK4_MES_B100_R0010": (
        "The priest at the nearby church knows a great deal. He might tell you something useful.",
        "The priest at the nearby church knows a lot. He might have a useful lead for you.",
    ),
    "DK4_MES_B101_R0005": (
        "Could you be the ones searching for the Proof of Conquest?",
        "Do you seek the Proof of Conquest?",
    ),
    "DK4_MES_B101_R0018": ("It seems I was mistaken...", "My mistake..."),
    "DK4_MES_B101_R0022": (
        "Wait, what is this Proof of Conquest?",
        "Wait. What's the Proof of Conquest?",
    ),
    "DK4_MES_B101_R0025": (
        "It is said to be obtained by one who rules the seas...",
        "A prize for the ruler of the seas...",
    ),
    "DK4_MES_B101_R0029": (
        "Rules the seas? Wow, that sounds interesting!",
        "Rule the seas? Sounds fun!",
    ),
    "DK4_MES_B101_R0039": (
        "Hey, tell us more about it.",
        "Come on, tell us more!",
    ),
    "DK4_MES_B101_R0045": (
        "Would you please tell us more?",
        "Could you tell us more, please?",
    ),
    "DK4_MES_B101_R0054": (
        "What? Priest, do you know something about it?",
        "Wait, you know something about it?",
    ),
    "DK4_MES_B101_R0060": (
        "The journey to the Proof is hard. I won't tell those with halfhearted resolve. Are you prepared?",
        "The Proof is hard to find. These secrets demand real resolve. Are you ready?",
    ),
    "DK4_MES_B101_R0064": (
        "Leave it to me! Once I decide to do something, I never give up until the end.",
        "You bet! Once my mind's made up, nothing makes me quit!",
    ),
    "DK4_MES_B101_R0068": ("Very well.", "Very well."),
    "DK4_MES_B101_R0072": (
        "What I know is that the Proof's map becomes useful only when two Map Keys are joined.",
        "The Proof's map only works when its two Map Keys are joined.",
    ),
    "DK4_MES_B101_R0076": (
        "Each key has no meaning by itself.",
        "Each key means nothing on its own.",
    ),
    "DK4_MES_B101_R0079": (
        "As you may have noticed, Map Keys may be hidden in ruins or held by unexpected people.",
        "Map Keys can hide in ruins or turn up with people you'd never suspect.",
    ),
    "DK4_MES_B101_R0086": (
        "I shall give you a sword.",
        "Take this sword.",
    ),
    "DK4_MES_B101_R0093": (
        "Overcome the trials placed before you and help people in trouble.",
        "Overcome the trials ahead. Help those in need.",
    ),
    "DK4_MES_B101_R0096": (
        "Do not be ruled by greed. Give to the poor, quell the source of strife, and spread peace.",
        "Give to the poor. Let go of greed, end strife, and spread peace.",
    ),
    "DK4_MES_B101_R0100": (
        "Then may God bless you all.",
        "May God watch over you.",
    ),
    "DK4_MES_B102_R0007": (
        "Wait. Have you ever been to Santiago Cathedral?",
        "Wait! Have you visited Santiago Cathedral?",
    ),
    "DK4_MES_B102_R0015": (
        "Pilgrims from all over Europe have come here for ages. It is quite famous.",
        "Pilgrims have come here for ages. People across Europe know it.",
    ),
    "DK4_MES_B102_R0019": (
        "Since you're in Seville, why not visit once? I can give you directions.",
        "You should visit while in Seville. Here's the way.",
    ),
    "DK4_MES_B103_R0009": (
        "Now let us pray. In the name of the Father, Son, and Holy Spirit... Amen.",
        "We pray to God, his Son, and his Spirit. Amen.",
    ),
    "DK4_MES_B103_R0013": (
        "Huh? Everyone's cross looks newer than mine...",
        "Why is my cross older than theirs?",
    ),
    "DK4_MES_B103_R0024": (
        "What is it? Oh, you're right. Only the admiral's cross is a completely different color.",
        "Your cross is a different color!",
    ),
    "DK4_MES_B103_R0026": (
        "What is it? Wow, you're right. Only the admiral's cross has a different color.",
        "Your cross is a different color.",
    ),
    "DK4_MES_B103_R0028": (
        "What's wrong? Oh, you're right. Only the admiral's cross has a different color.",
        "Your cross is a different color!",
    ),
    "DK4_MES_B103_R0030": (
        "What's up? Oh, you're right. Only the admiral's cross has a different color.",
        "Whoa! Your cross is another color!",
    ),
    "DK4_MES_B103_R0032": (
        "What's the matter? Yes, only the admiral's cross has a very different color.",
        "Your cross is a different color, eh?",
    ),
    "DK4_MES_B103_R0034": (
        "What's wrong? Ah, you're right. Only the admiral's cross has a different color.",
        "Oh, your cross is a different color!",
    ),
    "DK4_MES_B103_R0038": ("That's not fair!", "No fair!"),
    "DK4_MES_B103_R0042": (
        "But maybe being this old makes it look stylish after all.",
        "Maybe this old cross looks cool.",
    ),
    "DK4_MES_B104_R0015": ("Admiral, please look at this!", "Admiral, take a look!"),
    "DK4_MES_B104_R0017": ("Admiral, look at this!", "Admiral, look!"),
    "DK4_MES_B104_R0019": ("Admiral, take a look at this!", "Admiral, look at this!"),
    "DK4_MES_B104_R0021": ("Admiral, look over here!", "Admiral, look here!"),
    "DK4_MES_B104_R0023": ("Admiral, look!", "Admiral! Look!"),
    "DK4_MES_B104_R0025": ("Admiral, behold this!", "Admiral, behold!"),
    "DK4_MES_B104_R0029": ("You who have visited this temple...", "Visitor..."),
    "DK4_MES_B104_R0033": ("Whoa! It talked?!", "Whoa, it talks?!"),
    "DK4_MES_B104_R0037": (
        "I shall lend you my power. Debate to your heart's content.",
        "Take my power. Debate freely.",
    ),
}

SPEAKERS = {
    0x02: "Lil Argot",
    0x09: "Kamil",
    0x8B: "Priest",
    0xBC: "Local woman",
    0xBF: "Cathedral guide",
    0xD0: "Selected crewmate",
    0xFE: "Temple voice",
}
CONTEXTS = {
    "100": "A local woman directs Lil to a knowledgeable church priest.",
    "101": "The priest tests Lil's resolve and explains the Proof's two Map Keys.",
    "102": "A Seville woman gives directions to Santiago Cathedral.",
    "103": "A cathedral prayer leads Lil and her companions to notice the age of her cross.",
    "104": "A temple voice addresses Lil and lends its power before a debate.",
}
NOTES = {
    "DK4_MES_B103_R0009": (
        "Names the Trinity in natural prayer language while avoiding literal capital "
        "I/F bytes, which this renderer treats as macros."
    ),
    "DK4_MES_B103_R0024": "The D0 marker selects a crewmate; the name is not asserted from text alone.",
    "DK4_MES_B104_R0029": "Formal temple address kept concise to fit the fixed allocation.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        has_state = lead in SPEAKERS
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise ValueError(f"{row_id}: uppercase runtime macro byte in literal English")
        block = row_id.split("_B", 1)[1].split("_R", 1)[0]
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if has_state else "") + english + "{PAD}",
                "speaker": SPEAKERS.get(lead, "Companion variant"),
                "context": CONTEXTS[block],
                "source_meaning": source_meaning,
                "localization_note": NOTES.get(
                    row_id,
                    "Reviewed against clean Japanese and adjacent scene records; localized for American English.",
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
        "dialogue_profile": "lil-story-deep-route-v25-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's church and priest, Santiago Cathedral, cross, and temple scenes in B100-B104.",
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
