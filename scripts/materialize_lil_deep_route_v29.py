from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v29.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
NON_PROSE_ID = "DK4_MES_B109_R0281"
NON_PROSE_HEX = "9647214851A8"

LINES = {
    "DK4_MES_B109_R0007": (
        "Visitor to the Colosseum, answer my question!",
        "Colosseum visitor, answer my question!",
    ),
    "DK4_MES_B109_R0010": ("Huh? What does that mean?", "Huh? What's going on?"),
    "DK4_MES_B109_R0013": ("Then I shall ask.", "Question!"),
    "DK4_MES_B109_R0017": (
        "I have a strange bean. It splits in two after one second, four after two, and eight after three.",
        "A magic bean doubles each second: two after one, four after two, eight after three.",
    ),
    "DK4_MES_B109_R0021": (
        "If one bean fills a bag after sixty seconds, how long does it take if two beans go in at the start?",
        "One bean fills a bag in 60 seconds. How long would two beans take?",
    ),
    "DK4_MES_B109_R0024": ("Now choose an answer from the following!", "Choose your answer!"),
    "DK4_MES_B109_R0031": ("One second.", "1s"),
    "DK4_MES_B109_R0033": ("Thirty seconds.", "30s"),
    "DK4_MES_B109_R0035": ("Fifty-nine seconds.", "59s"),
    "DK4_MES_B109_R0058": (
        "Admiral, what do you think? I have no idea...",
        "Admiral, any idea? No clue.",
    ),
    "DK4_MES_B109_R0059": ("This is hard. I do not know.", "That's hard. No idea."),
    "DK4_MES_B109_R0060": ("I give up. I have no idea.", "No clue. No idea at all."),
    "DK4_MES_B109_R0062": ("This is no good. I have no idea.", "No good. No clue at all."),
    "DK4_MES_B109_R0064": ("Hmm, what does this mean...?", "What does it mean?"),
    "DK4_MES_B109_R0066": ("Hmm, what could it mean?", "What does this mean?"),
    "DK4_MES_B109_R0070": ("Hmm, a difficult one.", "Hmm, a hard one."),
    "DK4_MES_B109_R0076": (
        "This is a hard question, Lil. What do you think?",
        "Tough one, {MACRO:FI}. Thoughts?",
    ),
    "DK4_MES_B109_R0082": (
        "Leave it to me! The answer is one second!",
        "Leave it to me! One second!",
    ),
    "DK4_MES_B109_R0093": (
        "You are so confident. You must be sure!",
        "Wow, you're sure of yourself!",
    ),
    "DK4_MES_B109_R0096": ("I have both beauty and brains!", "Brains and beauty!"),
    "DK4_MES_B109_R0103": ("You fool!", "You fool!"),
    "DK4_MES_B109_R0115": (
        "What was that confidence based on?",
        "So... what made you so sure?",
    ),
    "DK4_MES_B109_R0118": ("It was only a hunch.", "Just a hunch."),
    "DK4_MES_B109_R0146": (
        "Admiral, what do you think? I have no idea...",
        "Admiral, any idea? No clue.",
    ),
    "DK4_MES_B109_R0147": ("This is hard. I do not know.", "That's hard. No idea."),
    "DK4_MES_B109_R0149": ("I give up. I have no idea.", "No clue. No idea at all."),
    "DK4_MES_B109_R0151": ("This is no good. I have no idea.", "No good. No clue at all."),
    "DK4_MES_B109_R0153": ("Hmm, what does this mean...?", "What does it mean?"),
    "DK4_MES_B109_R0155": ("Hmm, what could it mean?", "What does this mean?"),
    "DK4_MES_B109_R0159": ("Hmm, a difficult one.", "Hmm, a hard one."),
    "DK4_MES_B109_R0165": (
        "This is a hard question, Lil. What do you think?",
        "Tough one, {MACRO:FI}. Thoughts?",
    ),
    "DK4_MES_B109_R0171": (
        "Leave it to me! The answer is thirty seconds!",
        "Leave it to me! Thirty seconds!",
    ),
    "DK4_MES_B109_R0182": (
        "You are so confident. You must be sure!",
        "Wow, you're sure of yourself!",
    ),
    "DK4_MES_B109_R0185": ("I have both beauty and brains!", "Brains and beauty!"),
    "DK4_MES_B109_R0192": ("You fool!", "You fool!"),
    "DK4_MES_B109_R0204": (
        "What was that confidence based on?",
        "So... what made you so sure?",
    ),
    "DK4_MES_B109_R0207": ("It was only a hunch.", "Just a hunch."),
    "DK4_MES_B109_R0225": ("Perhaps fifty-nine seconds...", "Maybe 59 sec..."),
    "DK4_MES_B109_R0238": ("Admiral, did you calculate it?", "Admiral, you solved it?"),
    "DK4_MES_B109_R0240": ("Admiral, did you calculate it?", "Admiral, did you solve it?"),
    "DK4_MES_B109_R0242": ("Admiral, you figured it out?!", "You solved it?!"),
    "DK4_MES_B109_R0244": ("Admiral, you figured it out?", "You solved it?"),
    "DK4_MES_B109_R0246": ("Admiral, did you calculate it?!", "You worked it out?!"),
    "DK4_MES_B109_R0248": ("Oh, you solved it?", "You solved it?"),
    "DK4_MES_B109_R0250": ("Wow! You figured it out!", "Wow, you solved it!"),
    "DK4_MES_B109_R0252": ("Oh, you solved it?", "You solved it?"),
    "DK4_MES_B109_R0256": ("Well, more or less...", "Uh, yeah..."),
    "DK4_MES_B109_R0262": ("Oh, now I see!", "Oh, of course!"),
    "DK4_MES_B109_R0266": ("You figured it out? Amazing, Kamil!", "You got it? Nice work, Kamil!"),
    "DK4_MES_B109_R0269": ("The answer is fifty-nine seconds!", "Answer: 59 seconds!"),
    "DK4_MES_B109_R0273": (
        "I was just about to say that too!",
        "That was my guess too!",
    ),
    "DK4_MES_B109_R0279": (
        "Well done! One with wisdom and courage, take this!",
        "Well done! Take this, clever hero!",
    ),
    "DK4_MES_B109_R0292": ("Thank goodness! Lucky!", "Phew, lucky!"),
    "DK4_MES_B109_R0298": ("Kamil, you are reliable!", "Kamil, you came through!"),
    "DK4_MES_B109_R0302": ("I know!", "You bet!"),
    "DK4_MES_B110_R0015": ("Admiral, it is a dead end.", "Admiral, dead end."),
    "DK4_MES_B110_R0017": ("Admiral, it is a dead end.", "Admiral, dead end."),
    "DK4_MES_B110_R0019": ("Huh, a dead end.", "Huh, a dead end."),
    "DK4_MES_B110_R0021": ("Admiral, it is a dead end.", "Admiral, dead end."),
    "DK4_MES_B110_R0023": ("Oops, a dead end.", "Oops. Dead end."),
    "DK4_MES_B110_R0025": ("Admiral, it is a dead end.", "Admiral, dead end."),
    "DK4_MES_B110_R0027": ("Admiral, it is a dead end!", "Admiral! Dead end!"),
    "DK4_MES_B110_R0029": ("Oh, a dead end.", "Oh my, a dead end."),
    "DK4_MES_B110_R0033": (
        "An urn-shaped stone tablet is embedded in the wall.",
        "An urn-shaped tablet is here.",
    ),
    "DK4_MES_B110_R0036": (
        "Traveler, pour from the sacred urn with your left hand.",
        "Pour this holy urn left-handed.",
    ),
    "DK4_MES_B110_R0039": ("The urn, with the left hand?", "Left hand?"),
    "DK4_MES_B110_R0046": ("Push.", "Push"),
    "DK4_MES_B110_R0048": ("Turn right.", "Right"),
    "DK4_MES_B110_R0050": ("Turn left.", "Left"),
    "DK4_MES_B110_R0066": (
        "Pouring the urn with the left hand should make it tilt right...",
        "Left hand means it tips right...",
    ),
    "DK4_MES_B110_R0089": ("Aaah! Run!", "Ah! Run!"),
    "DK4_MES_B110_R0093": ("Aaah!", "Aaah!"),
    "DK4_MES_B110_R0100": ("A sailor was injured!", "A sailor is hurt!"),
}

SPEAKERS = {
    0x02: "Lil Argot",
    0x09: "Kamil",
    0x97: "Sailor",
    0xCF: "Party",
    0xD0: "Selected crewmate",
    0xFE: "Colosseum voice",
}
TEXT_LEADS = {0x81, 0x82, 0x83, 0x89, 0x8D, 0x92}
NOTES = {
    "DK4_MES_B109_R0013": "Source leading blank lines are staging, not spoken text; starts on the first row.",
    "DK4_MES_B109_R0024": "Source leading blank lines are staging, not spoken text; starts on the first row.",
    "DK4_MES_B109_R0076": "Preserves Lil's three-byte FI runtime name macro.",
    "DK4_MES_B109_R0165": "Preserves Lil's three-byte FI runtime name macro.",
    "DK4_MES_B110_R0046": "Choice label begins ordinary Shift-JIS text, not a selector.",
    "DK4_MES_B110_R0048": "Choice label begins ordinary Shift-JIS text, not a selector.",
    "DK4_MES_B110_R0050": "Choice label begins ordinary Shift-JIS text, not a selector.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    if source_rows[NON_PROSE_ID]["source_hex"] != NON_PROSE_HEX:
        raise ValueError("B109 six-byte event fragment changed; review before excluding")
    counts: Counter[str] = Counter()
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        block = row_id.split("_B", 1)[1].split("_R", 1)[0]
        counts[str(int(block))] += 1
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "")
                + english
                + "{PAD}",
                "speaker": SPEAKERS.get(
                    lead,
                    "Choice" if row_id in {
                        "DK4_MES_B109_R0031", "DK4_MES_B109_R0033", "DK4_MES_B109_R0035",
                        "DK4_MES_B110_R0046", "DK4_MES_B110_R0048", "DK4_MES_B110_R0050",
                    } else "Companion variant",
                ),
                "context": (
                    "Lil and Kamil answer the Colosseum's doubling-bean riddle, including two wrong branches."
                    if block == "109"
                    else "The party reaches an urn tablet and must choose how a left-handed pour tips it."
                ),
                "source_meaning": source_meaning,
                "localization_note": NOTES.get(
                    row_id,
                    "Reviewed against clean Japanese and adjacent Colosseum dialogue for en-US meaning and voice.",
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
        "scope": "Lil's Colosseum doubling-bean riddle and left-handed urn puzzle in B109-B110.",
        "excluded_records": {
            NON_PROSE_ID: (
                "Unmapped six-byte 96 47 21 48 51 A8 event fragment with no "
                "coherent prose; retain byte-identical pending runtime mapping."
            )
        },
        "inventory": {
            "identified_records": len(LINES) + 1,
            "translated_records": len(records),
            "blocks": dict(counts),
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records and one exclusion")


if __name__ == "__main__":
    main()
