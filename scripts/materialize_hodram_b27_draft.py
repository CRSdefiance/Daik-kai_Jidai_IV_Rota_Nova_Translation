from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/hodram_natural_v2_sc2_b27_blocked.json")
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"

# Source-first editorial manuscript. Prefixes and formatting are deliberately
# supplied from the clean export below, not copied from the revoked legacy batch.
LINES: dict[str, tuple[str, str, str]] = {
    "DK4_MES_B27_R0005": (
        "Hodram Bergstrom",
        "Never seen that ship before. Let's hope they're not pirates...",
        "Hodram notices an unfamiliar ship and hopes it is not a pirate vessel.",
    ),
    "DK4_MES_B27_R0009": (
        "Lil Argot",
        "Hey, you! What do you want with my ship? Staring at it and calling us pirates... How rude!",
        "Lil confronts the men for staring at her ship and calling its crew pirates.",
    ),
    "DK4_MES_B27_R0012": (
        "Hodram Bergstrom",
        "...This is your ship?",
        "Hodram asks whether the vessel belongs to Lil.",
    ),
    "DK4_MES_B27_R0016": (
        "Lil Argot",
        "Yes, it's mine! And you have no right to call me 'you' like that!",
        "Lil confirms ownership and objects to Hodram's overly familiar address.",
    ),
    "DK4_MES_B27_R0020": (
        "Lil Argot",
        "You're a soldier. Your uniform gives you away.",
        "Lil identifies Hodram as military from his clothes.",
    ),
    "DK4_MES_B27_R0024": (
        "Lil Argot",
        "I hate soldiers. They hide behind their authority and push everyone around!",
        "Lil says she hates soldiers who use authority as cover for bullying.",
    ),
    "DK4_MES_B27_R0035": ("Kamil", "{MACRO:FI}, please calm down.", "Kamil asks Lil to calm down."),
    "DK4_MES_B27_R0041": (
        "Kamil",
        "{MACRO:FI}! You can't talk to someone like that when you've just met!",
        "Kamil scolds Lil for being rude to strangers.",
    ),
    "DK4_MES_B27_R0044": (
        "Lil Argot",
        "Stay out of this, Kamil!",
        "Lil tells Kamil to be quiet and stop interfering.",
    ),
    "DK4_MES_B27_R0048": (
        "Lil Argot",
        "If you're trying to pick a fight with me, you've chosen the wrong woman!",
        "Lil refuses to let Hodram make accusations or provoke her.",
    ),
    "DK4_MES_B27_R0052": (
        "Hodram Bergstrom",
        "...Tch...!",
        "Hodram reacts with restrained frustration.",
    ),
    "DK4_MES_B27_R0056": (
        "Lil Argot",
        "What, violence? Just what I'd expect from a man with nothing but brute strength. Go on, try it!",
        "Lil accuses Hodram of resorting to violence and dares him to try.",
    ),
    "DK4_MES_B27_R0060": (
        "Hodram Bergstrom",
        "Don't misunderstand. I would never strike a woman or a child.",
        "Hodram says he has no intention of hitting women or children.",
    ),
    "DK4_MES_B27_R0063": (
        "Lil Argot",
        "Oh? Playing the gentleman now?",
        "Lil sarcastically asks whether Hodram means to act like a gentleman.",
    ),
    "DK4_MES_B27_R0066": (
        "Lil Argot",
        "That still won't fool me!",
        "Lil insists Hodram's restraint will not deceive her.",
    ),
    "DK4_MES_B27_R0069": (
        "Lil Argot",
        "Come on, Kamil. We're leaving!",
        "Lil orders Kamil to leave with her.",
    ),
    "DK4_MES_B27_R0073": (
        "Kamil",
        "W-wait! {MACRO:FI}! Um... I'm sorry. Excuse us...",
        "Kamil calls after Lil, apologizes to the men, and takes his leave.",
    ),
    "DK4_MES_B27_R0083": (
        "Gerhard Ardelknatts",
        "You are Lord Hodram Bergstrom, I presume...",
        "Gerhard formally confirms Hodram's identity.",
    ),
    "DK4_MES_B27_R0087": ("Hodram Bergstrom", "Yes, I am.", "Hodram confirms his identity."),
    "DK4_MES_B27_R0091": (
        "Gerhard Ardelknatts",
        "I've heard the stories. My name is Gerhard Ardelknatts.",
        "Gerhard says he knows Hodram by reputation and introduces himself.",
    ),
    "DK4_MES_B27_R0094": (
        "Hodram Bergstrom",
        "Admiral Ardelknatts... the famous pirate hunter?",
        "Hodram recognizes Gerhard as the admiral known for hunting pirates.",
    ),
    "DK4_MES_B27_R0097": (
        "Gerhard Ardelknatts",
        "That was a long time ago...",
        "Gerhard says his pirate-hunting exploits belong to the past.",
    ),
    "DK4_MES_B27_R0101": (
        "Gerhard Ardelknatts",
        "Tell me, Lord Hodram. Why did you tolerate that abuse?",
        "Gerhard asks why Hodram accepted Lil's insulting words.",
    ),
    "DK4_MES_B27_R0105": (
        "Hodram Bergstrom",
        "...She wasn't in any state to listen. Forgive me, but dealing with people like that is exhausting.",
        "Hodram says reason would not have worked and that dealing with such people pains him.",
    ),
    "DK4_MES_B27_R0108": (
        "Gerhard Ardelknatts",
        "...I see. I believe I understand.",
        "Gerhard says he understands Hodram's response.",
    ),
    "DK4_MES_B27_R0121": (
        "Hodram Bergstrom",
        "Hm? What is it...?",
        "Hodram notices someone returning and asks what they want.",
    ),
    "DK4_MES_B27_R0127": (
        "Gerhard Ardelknatts",
        "Hm? Kamil...?",
        "Gerhard recognizes Kamil returning.",
    ),
    "DK4_MES_B27_R0134": (
        "Kamil",
        "Huff... huff... Um... I'm sorry about earlier.",
        "Out of breath, Kamil apologizes for the earlier confrontation.",
    ),
    "DK4_MES_B27_R0137": (
        "Hodram Bergstrom",
        "Is there something else?",
        "Hodram asks whether Kamil has more business with them.",
    ),
    "DK4_MES_B27_R0141": (
        "Kamil",
        "I couldn't leave without apologizing... I'm truly sorry!",
        "Kamil says he had to apologize properly and repeats his sincere apology.",
    ),
    "DK4_MES_B27_R0148": (
        "Kamil",
        "Please forgive {MACRO:FI}. She didn't come here looking for a fight.",
        "Kamil asks them to forgive Lil and says she did not intend to start a fight.",
    ),
    "DK4_MES_B27_R0151": (
        "Kamil",
        "A soldier once treated her terribly just because he could. Ever since then, she's been a little sensitive about the military.",
        "Kamil explains that a soldier abused his position in the past, leaving Lil wary of soldiers.",
    ),
    "DK4_MES_B27_R0154": (
        "Kamil",
        "She's really kind at heart. She just jumps to conclusions and gets carried away sometimes... That's {MACRO:FI} for you.",
        "Kamil praises Lil's kindness while admitting she is impulsive and quick to assume the worst.",
    ),
    "DK4_MES_B27_R0157": (
        "Hodram Bergstrom",
        "You're Kamil, correct?",
        "Hodram checks Kamil's name.",
    ),
    "DK4_MES_B27_R0161": ("Kamil", "Huh? Oh, yes.", "Kamil confirms his name in surprise."),
    "DK4_MES_B27_R0165": (
        "Hodram Bergstrom",
        "I appreciate the sincere apology. No offense taken.",
        "Hodram accepts Kamil's courteous apology and says he is not offended.",
    ),
    "DK4_MES_B27_R0168": ("Kamil", "R-really?!", "Kamil is surprised that Hodram forgives them."),
    "DK4_MES_B27_R0172": (
        "Hodram Bergstrom",
        "Yes. With someone like you beside her, she can put her talents to good use.",
        "Hodram says Kamil's presence helps Lil use her abilities well.",
    ),
    "DK4_MES_B27_R0176": (
        "Kamil",
        "N-no, I wouldn't say that...",
        "Kamil modestly denies deserving Hodram's praise.",
    ),
    "DK4_MES_B27_R0180": (
        "Hodram Bergstrom",
        "You needn't worry about me. And not one soldier like the man you described serves in our fleet.",
        "Hodram reassures Kamil and says his fleet has no cruel soldiers of that kind.",
    ),
    "DK4_MES_B27_R0184": (
        "Hodram Bergstrom",
        "My only ambition is to make our navy one of the strongest in the world. I won't harm either of you. You have my word.",
        "Hodram states his naval ambition and promises not to harm Lil or Kamil.",
    ),
    "DK4_MES_B27_R0196": (
        "Kamil",
        "Thank you! And... Gerhard...",
        "Kamil thanks Hodram, then turns to Gerhard with another request.",
    ),
    "DK4_MES_B27_R0200": ("Gerhard Ardelknatts", "What is it?", "Gerhard asks what Kamil wants."),
    "DK4_MES_B27_R0204": (
        "Kamil",
        "About me coming here... {MACRO:FI} doesn't know...",
        "Kamil says Lil does not know he returned to speak with them.",
    ),
    "DK4_MES_B27_R0207": (
        "Gerhard Ardelknatts",
        "Understood. We'll keep it between us.",
        "Gerhard agrees to keep Kamil's visit secret.",
    ),
    "DK4_MES_B27_R0214": (
        "Kamil",
        "Thank you! Then... please excuse me.",
        "Kamil thanks them and politely leaves.",
    ),
    "DK4_MES_B27_R0227": (
        "Hodram Bergstrom",
        "A promising young man...",
        "Hodram remarks that Kamil has a promising future.",
    ),
    "DK4_MES_B27_R0233": (
        "Gerhard Ardelknatts",
        "A fine young man...",
        "Gerhard praises Kamil's character.",
    ),
    "DK4_MES_B27_R0237": (
        "Hodram Bergstrom",
        "Yes... I look forward to seeing what becomes of him.",
        "Hodram agrees that Kamil's future is worth anticipating.",
    ),
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B27_")
        }
    if set(rows) != set(LINES):
        missing = sorted(set(rows) - set(LINES))
        extra = sorted(set(LINES) - set(rows))
        raise SystemExit(f"B27 inventory mismatch: missing={missing}, extra={extra}")

    records = []
    for row_id, (speaker, english, source_meaning) in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        records.append(
            {
                "id": row_id,
                "draft_english": f"{english}{{PAD}}",
                "speaker": speaker,
                "context": "Hodram and Gerhard encounter Lil and Kamil at the harbor; the confrontation gives way to Kamil's private apology.",
                "source_meaning": source_meaning,
                "localization_note": "Localized from the clean Japanese in natural American English while preserving the scene's tone and facts.",
                "source_prefix_hex": f"{source[0]:02X}",
                "source_length": len(source),
                "blocker": "SC2 block 27 speaker/portrait state and FI expansion are not independently mapped; this editorial draft is not encodable.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": False,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "route_owner": "Lil Argot",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "draft_status": "source-first-editorial-draft-blocked-unmapped-sc2-b27-control-state",
        "profile_note": "Non-buildable Lil-route draft retained under a historical Hodram filename. SC2 block 27 control state and runtime FI expansion must be mapped before formatting or insertion.",
        "inventory": {
            "identified_records": 49,
            "translated_drafts": 49,
            "encodable_records": 0,
            "blocked_records": 49,
            "missing_records": 0,
            "blocks": {"27": 49},
        },
        "records": [],
        "blocked_records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} blocked source-first drafts")


if __name__ == "__main__":
    main()
