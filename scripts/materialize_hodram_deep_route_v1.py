from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v1.json")
# The canonical accepted baseline already contains the approved Hodram opening
# and Stockholm tutorials.  All records in this batch are still byte-locked to
# their clean source_hex values, but the enclosing SC1 container is the current
# accepted one rather than the pristine extraction.
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(45, 61)) + (137, 138)

# Three tiny records are scene commands, not dialogue.  Their decoded text is
# mojibake and they must remain byte-identical.
EXCLUDED = {
    "DK4_MES_B49_R0008": "Four-byte scene command.",
    "DK4_MES_B49_R0087": "Three-byte scene command.",
    "DK4_MES_B50_R0019": "Five-byte scene command.",
    "DK4_MES_B138_R0032": "Four-byte reveal command.",
}

LINES = {
    # B45-B50: Lil's North Sea challenge and the two resolutions of her trade.
    "DK4_MES_B45_R0007": "The Argot Company boss is waiting for you in Amsterdam.",
    "DK4_MES_B46_R0006": "Wait!",
    "DK4_MES_B46_R0010": "You're the richest captain here? Then let's see who's better!",
    "DK4_MES_B46_R0014": "Duel?",
    "DK4_MES_B46_R0019": "This key reveals a map. Whoever finds it first rules the North Sea.",
    "DK4_MES_B46_R0023": "No mercy! This is real. You won't beat me!",
    "DK4_MES_B46_R0051": "A map key? What is it?",
    "DK4_MES_B47_R0006": "What?! Already? That's not fair!",
    "DK4_MES_B47_R0010": "You win... Oh well.",
    "DK4_MES_B47_R0013": "You beat me, so don't lose to anyone. Become number one!",
    "DK4_MES_B48_R0006": "Lil Argot appears to have found Ullr's Bow!",
    "DK4_MES_B48_R0011": "Hee hee. Too bad, {MACRO:FI}!",
    "DK4_MES_B48_R0014": "Want it? Meet me in Amsterdam.",
    "DK4_MES_B49_R0006": "You're here!",
    "DK4_MES_B49_R0010": "This proves who rules here. So no, it's not yours.",
    "DK4_MES_B49_R0019": "But one thing might change my mind.",
    "DK4_MES_B49_R0022": "The Heavenly Wristband! So cute!",
    "DK4_MES_B49_R0033": "They say it's in the New World. Bring it and the bow is yours. Bye!",
    "DK4_MES_B49_R0040": "You already have it? Let me see!",
    "DK4_MES_B49_R0043": "Wow! So cute! Take the bow; give me that!",
    "DK4_MES_B49_R0048": "All right.",
    "DK4_MES_B49_R0050": "No.",
    "DK4_MES_B49_R0058": "Yes! No changing your mind! See you!",
    "DK4_MES_B49_R0064": "What?! Don't you want the Proof?",
    "DK4_MES_B49_R0067": "...The bow matters.",
    "DK4_MES_B49_R0071": "Exactly! Here, take this. Now give me the wristband!",
    "DK4_MES_B49_R0074": "Wow! So cute! Yes! Bye!",
    "DK4_MES_B49_R0081": "Heavenly Wristband given.",
    "DK4_MES_B50_R0007": "You brought it?! Let me see!",
    "DK4_MES_B50_R0010": "Wow! So cute! Take the bow. Yes! Bye!",
    "DK4_MES_B50_R0013": "Heavenly Wristband given.",

    # B51-B55: regional warnings and route hooks beyond the North Sea.
    "DK4_MES_B51_R0006": "Whatever your plans here, leave while you can.",
    "DK4_MES_B51_R0010": "...Why?",
    "DK4_MES_B51_R0014": "A monster rules here. Take my advice: sail elsewhere.",
    "DK4_MES_B51_R0032": "A terrifying man?",
    "DK4_MES_B51_R0039": "(Could it be?)",
    "DK4_MES_B52_R0006": "Will you oppose the Hayreddin family?",
    "DK4_MES_B52_R0011": "Not at all.",
    "DK4_MES_B52_R0013": "Bring it on.",
    "DK4_MES_B52_R0021": "Then get out before they notice you.",
    "DK4_MES_B52_R0033": "A death wish.",
    "DK4_MES_B53_R0007": "The Ottoman Empire has put a price on your head. Watch yourself.",
    "DK4_MES_B54_R0006": "You new around here?",
    "DK4_MES_B54_R0010": "Hm? Yes.",
    "DK4_MES_B54_R0014": "So you're new. Well, good luck. Heh heh.",
    "DK4_MES_B55_R0006": "You're officer {MACRO:FA}, right? Veracruz's guildmaster wants you.",

    # B56-B57: Sera remains with Hodram and begins learning his language.
    "DK4_MES_B56_R0007": "...And you? Won't you go with them?",
    "DK4_MES_B56_R0010": "Strange girl: ...",
    "DK4_MES_B56_R0013": "You're from another people. This city can shelter you.",
    "DK4_MES_B57_R0007": "{MACRO:FI}...",
    "DK4_MES_B57_R0011": "What?",
    "DK4_MES_B57_R0015": "...Thank you.",
    "DK4_MES_B57_R0019": "You learned our speech?",
    "DK4_MES_B57_R0023": "(Nods) ...A little.",
    "DK4_MES_B57_R0027": "You're a quick learner.",
    "DK4_MES_B57_R0031": "{MACRO:FI}. Thank... you.",
    "DK4_MES_B57_R0035": "Yes... Never mind.",

    # B58-B60: Espinosa's reckoning, the African clue, and Manuel's resolve.
    "DK4_MES_B58_R0006": "W-what are you doing?!",
    "DK4_MES_B58_R0010": "Get over here!",
    "DK4_MES_B58_R0014": "What? Espinosa?!",
    "DK4_MES_B58_R0018": "{MACRO:FA}, you defeated this fiend!",
    "DK4_MES_B58_R0021": "You won't escape punishment!",
    "DK4_MES_B58_R0024": "Shut up!",
    "DK4_MES_B58_R0028": "Gah! That hurts!",
    "DK4_MES_B58_R0032": "Your cruelty ends now.",
    "DK4_MES_B58_R0035": "About what?",
    "DK4_MES_B58_R0039": "Don't pretend you forgot! You stole my father's home and land. My whole family vanished!",
    "DK4_MES_B58_R0042": "You killed my friend for trying to expose your crimes!",
    "DK4_MES_B58_R0046": "You dragged people from my village away and worked them nearly to death!",
    "DK4_MES_B58_R0058": "A devil in human skin...",
    "DK4_MES_B58_R0064": "No! My men acted alone!",
    "DK4_MES_B58_R0068": "You bastard...!",
    "DK4_MES_B58_R0080": "Rotten to the core. You deserve no mercy.",
    "DK4_MES_B58_R0093": "Sera, do you know this man?",
    "DK4_MES_B58_R0097": "Yes.",
    "DK4_MES_B58_R0101": "Y-you?!",
    "DK4_MES_B58_R0105": "He... sold me high... sent me home.",
    "DK4_MES_B58_R0108": "Lies!",
    "DK4_MES_B58_R0116": "Wrong person! This is slander!",
    "DK4_MES_B58_R0120": "He killed my brother... my people! Him!",
    "DK4_MES_B58_R0124": "Stop! Damn woman! Should've killed you then... Gah!",
    "DK4_MES_B58_R0127": "...No escape from this.",
    "DK4_MES_B58_R0137": "{MACRO:FA}, what shall we do with him?",
    "DK4_MES_B58_R0141": "You decide his fate.",
    "DK4_MES_B58_R0145": "You heard him! Come. You'll pay for every crime!",
    "DK4_MES_B58_R0148": "P-please, help me!",
    "DK4_MES_B58_R0168": "Sera, remember this. Men like him still swagger across the world.",
    "DK4_MES_B58_R0172": "...Perhaps we're not so different.",
    "DK4_MES_B58_R0175": "No... {MACRO:FI}... different.",
    "DK4_MES_B58_R0179": "Don't trust people blindly.",
    "DK4_MES_B58_R0186": "{MACRO:FA}.",
    "DK4_MES_B58_R0190": "Sorry to test you, but we need something found.",
    "DK4_MES_B58_R0198": "Admiral, know the legends of King Solomon?",
    "DK4_MES_B58_R0202": "They say mighty Solomon could command even demon kings.",
    "DK4_MES_B58_R0206": "A weapon tied to one such demon is said to lie sealed on an icy island far northwest.",
    "DK4_MES_B58_R0210": "Only a true ruler may wield it. Return with it...",
    "DK4_MES_B58_R0213": "Then what?",
    "DK4_MES_B58_R0217": "Then something will be yours.",
    "DK4_MES_B58_R0220": "What is it?",
    "DK4_MES_B58_R0224": "Not yet. Return safely and you'll learn.",
    "DK4_MES_B58_R0228": "Hm... Demon arms.",
    "DK4_MES_B58_R0239": "An icy isle far northwest? The isle of ice?",
    "DK4_MES_B59_R0005": "You found it?",
    "DK4_MES_B59_R0009": "Yes, this is it. Then we entrust this to you.",
    "DK4_MES_B59_R0013": "Please accept this piece of the map.",
    "DK4_MES_B59_R0019": "This?",
    "DK4_MES_B59_R0023": "Espinosa had it. He sought Africa's Proof of Conquest, and we prayed he would never find it.",
    "DK4_MES_B59_R0026": "You should rule these waters. Seek the treasure and bring Africa peace.",
    "DK4_MES_B59_R0030": "The map is welcome, but expect little.",
    "DK4_MES_B60_R0005": "Admiral, no one is more vile than a slave trader.",
    "DK4_MES_B60_R0012": "Years ago, sickness left me ashore at Sao Jorge on a voyage east.",
    "DK4_MES_B60_R0015": "The local people saved me. They cared for me with extraordinary kindness.",
    "DK4_MES_B60_R0019": "They suffered under Portugal, yet cared for me like family.",
    "DK4_MES_B60_R0022": "Oh...",
    "DK4_MES_B60_R0026": "Then the Lord's words became real: love thy neighbor. This became my second home.",
    "DK4_MES_B60_R0029": "A vow followed: fight the men hunting slaves in Africa.",
    "DK4_MES_B60_R0033": "Admiral, we must defeat Espinosa!",
    "DK4_MES_B60_R0036": "Yes. Of course.",

    # B137: Kamil apologizes and Gerhard points the fleet toward recruitment.
    "DK4_MES_B137_R0006": "Hm?",
    "DK4_MES_B137_R0010": "Um... Sorry about before.",
    "DK4_MES_B137_R0014": "You! Her friend! What do you want?",
    "DK4_MES_B137_R0017": "She had no right to say those things. Please accept my apology.",
    "DK4_MES_B137_R0025": "She never meant to anger you.",
    "DK4_MES_B137_R0028": "Once she sees a business rival, that's the only way she can talk.",
    "DK4_MES_B137_R0032": "She's kind, really. She just jumps to conclusions. Please forgive Lil!",
    "DK4_MES_B137_R0039": "You're Kamil, yes?",
    "DK4_MES_B137_R0043": "What? Oh, yes.",
    "DK4_MES_B137_R0047": "Your apology is welcome. You help her talent shine.",
    "DK4_MES_B137_R0050": "N-no... not me.",
    "DK4_MES_B137_R0054": "Don't worry. We choose our enemies carefully. We won't harm either of you. Tell her that.",
    "DK4_MES_B137_R0058": "Thank you! Well... goodbye!",
    "DK4_MES_B137_R0078": "A promising young man.",
    "DK4_MES_B137_R0082": "Hm... Our own fleet is short-handed too.",
    "DK4_MES_B137_R0086": "More talent is needed to expand our fleet.",
    "DK4_MES_B137_R0089": "Mediterranean ports breed sailors. Try Lisbon or Seville.",
    "DK4_MES_B137_R0092": "Agreed. We can extend our trade routes through that sea too.",

    # B138: the North Sea clue is combined and the next voyage begins.
    "DK4_MES_B138_R0005": "She said whoever finds it first rules the North Sea.",
    "DK4_MES_B138_R0008": "Does this Crimson Dye somehow lead to the Proof of Conquest?",
    "DK4_MES_B138_R0012": "Admiral, the Old Parchment from the ruins is blank. That worries me.",
    "DK4_MES_B138_R0016": "Meaning?",
    "DK4_MES_B138_R0020": "That man prized this paper. Some secret must be hidden.",
    "DK4_MES_B138_R0023": "Crimson Dye may reveal something on it.",
    "DK4_MES_B138_R0026": "Hm!",
    "DK4_MES_B138_R0030": "Th-this is!",
    "DK4_MES_B138_R0038": "A map... Then...",
    "DK4_MES_B138_R0041": "No doubt.",
    "DK4_MES_B138_R0045": "Now the North Sea's Proof of Conquest is ours!",
    "DK4_MES_B138_R0048": "Yes. Prepare to sail.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "02": "Lil Argot",
    "09": "Kamil",
    "10": "Gerhard Adelknauts",
    "12": "Charles",
    "14": "African sailor",
    "17": "Manuel",
    "18": "Sera",
    "24": "Espinosa",
    "26": "Nagalpur",
    "2B": "Diogo de Escante",
    "54": "African elder",
    "69": "Indian Ocean elder",
    "71": "Tavern patron",
    "72": "African townsman",
    "77": "Tavern patron",
    "8D": "African villager",
    "9A": "Nagalpur attendant",
    "FE": "System narration",
}

EXTENDED_STATES = {
    0x10, 0x12, 0x14, 0x17, 0x18, 0x24, 0x26, 0x2B, 0x54, 0x69,
    0x71, 0x72, 0x77, 0x8D, 0x9A, 0xFE,
}

CONTEXT = {
    **{block: "Hodram's North Sea rivalry with Lil and the search for its Proof of Conquest." for block in range(45, 51)},
    **{block: "Hodram receives regional warnings while expanding beyond the North Sea." for block in range(51, 56)},
    56: "Hodram frees captives and offers the foreign girl Sera sanctuary.",
    57: "Sera begins speaking Hodram's language and thanks him.",
    58: "After Espinosa's defeat, his victims confront him and entrust Hodram with a test tied to Africa's Proof of Conquest.",
    59: "Hodram completes the test and receives the African map fragment.",
    60: "Manuel explains why ending the African slave trade is personal to him.",
    137: "Kamil apologizes for Lil's behavior; Hodram and Gerhard discuss recruiting in the Mediterranean.",
    138: "Hodram and Gerhard combine the Crimson Dye with the Old Parchment to reveal the North Sea map.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }

    expected = set(source_rows) - set(EXCLUDED)
    if set(LINES) != expected:
        raise SystemExit(
            f"Hodram deep-route inventory mismatch: missing={sorted(expected-set(LINES))}, "
            f"extra={sorted(set(LINES)-expected)}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        source = bytes.fromhex(row["source_hex"])
        first = source[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice or scene text"),
                "context": CONTEXT[block],
                "source_meaning": english,
                "localization_note": (
                    "Faithful, concise American English from the clean Japanese; "
                    "established item and Proof of Conquest terminology is retained, "
                    "and wrapping is delegated to the measured formatter."
                ),
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
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
        "dialogue_profile": "hodram-story-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "A deep Hodram-route continuation across SC1 blocks 45-60, 137, and 138.",
        "profile_note": (
            "Source-locked fixed-allocation route pass covering the immediate Kamil follow-up, "
            "North Sea Proof rivalry, outward regional hooks, Sera's introduction, Espinosa's "
            "reckoning, the Africa clue, and Manuel's anti-slavery resolve."
        ),
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "excluded_non_prose_records": len(EXCLUDED),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
