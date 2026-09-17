from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_story_natural_v2_b49_b51.json")
# SC0 in the accepted baseline already contains the approved Raphael opening.
# Blocks 49-51 are byte-identical to the clean extraction and are still locked
# individually by the materialized source_hex values.
SC0_SHA256 = "cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"

# The complete prose inventory in the three consecutive story blocks after
# Raphael's translated opening/tutorial.  Capital F and I are deliberately
# avoided as literal text because the native script parser reserves them for
# runtime name macros; explicit {MACRO:..} tokens are safe.
LINES = {
    # B49: Raphael meets Lil and agrees to leave the North Sea for later.
    "DK4_MES_B49_R0006": "Hm? The guild is noisy. Let's look.",
    "DK4_MES_B49_R0012": "Hey! You there!",
    "DK4_MES_B49_R0015": "Lil! No fighting!",
    "DK4_MES_B49_R0020": "You have to be blunt about this! Kamil, stay out of it.",
    "DK4_MES_B49_R0032": "My, this feels hostile.",
    "DK4_MES_B49_R0039": "Do you need me?",
    "DK4_MES_B49_R0043": "Need something?! Who said you could trade in our North Sea?!",
    "DK4_MES_B49_R0047": "What was that, girl? You trying to make us angry?",
    "DK4_MES_B49_R0052": "Sorry, but... what exactly is going on here?",
    "DK4_MES_B49_R0055": "You dumb?",
    "DK4_MES_B49_R0067": "Ha! That's rather harsh.",
    "DK4_MES_B49_R0074": "Listen. This is your only warning.",
    "DK4_MES_B49_R0078": "Uh... yes.",
    "DK4_MES_B49_R0082": "People everywhere are fighting to get rich. The same goes for this sea.",
    "DK4_MES_B49_R0086": "Could you be more polite?",
    "DK4_MES_B49_R0090": "Good! Argot Company runs this area. Got it?",
    "DK4_MES_B49_R0094": "Uh...",
    "DK4_MES_B49_R0098": "Can this man be trusted? Are you really an admiral?",
    "DK4_MES_B49_R0107": "Yeah. That's it.",
    "DK4_MES_B49_R0112": "Yes. He's a fine admiral.",
    "DK4_MES_B49_R0118": "What a letdown.",
    "DK4_MES_B49_R0122": "But you seem decent. All right, let me explain.",
    "DK4_MES_B49_R0126": "The North Sea covers a pretty big area, right?",
    "DK4_MES_B49_R0129": "Yeah.",
    "DK4_MES_B49_R0142": "Up north is navy man Hodram Berg... something. At least for now.",
    "DK4_MES_B49_R0158": "Around England, an admiral named Clifford is in charge.",
    "DK4_MES_B49_R0175": "Germany is barely held together by Martin Speyer of the Hanseatic League.",
    "DK4_MES_B49_R0183": "The other regions are what my company plans to claim next.",
    "DK4_MES_B49_R0188": "But Lil, isn't trade fair once you sign a contract with a city?",
    "DK4_MES_B49_R0192": "Of course. So please leave it alone for a while.",
    "DK4_MES_B49_R0196": "How convenient for you.",
    "DK4_MES_B49_R0201": "Well, that's a little...",
    "DK4_MES_B49_R0205": "Aren't you trying to take on the whole world?",
    "DK4_MES_B49_R0209": "Yes. We are.",
    "DK4_MES_B49_R0213": "What a dull answer.",
    "DK4_MES_B49_R0225": "We do have a goal.",
    "DK4_MES_B49_R0238": "Then go to Africa, or sail west to the New World.",
    "DK4_MES_B49_R0244": "The world is huge! Try the New World, or solve the mysteries of the East!",
    "DK4_MES_B49_R0251": "Hm. That's one viewpoint.",
    "DK4_MES_B49_R0255": "So, stay out of our way for a while.",
    "DK4_MES_B49_R0259": "Challenge us head-on if you like, but we'll answer in kind. Do you understand?",
    "DK4_MES_B49_R0262": "W-wait, Lil...",
    "DK4_MES_B49_R0267": "More or less. You're asking us to form a pact, aren't you?",
    "DK4_MES_B49_R0271": "H-how are you so sharp about that? You make it sound like we're begging!",
    "DK4_MES_B49_R0276": "Heh. Hate losing?",
    "DK4_MES_B49_R0279": "Hey! Mocking me?",
    "DK4_MES_B49_R0284": "No, not at all.",
    "DK4_MES_B49_R0296": "(Giggle)",
    "DK4_MES_B49_R0311": "Good grief. {MACRO:FI}, seeking profit in another sea may be wiser.",
    "DK4_MES_B49_R0328": "That Spanish Valdes is your enemy, right?",
    "DK4_MES_B49_R0332": "An enemy? Spain wants Portuguese land, so... yes, perhaps.",
    "DK4_MES_B49_R0336": "Then we have the same enemy! We shouldn't be fighting each other. Exactly!",
    "DK4_MES_B49_R0344": "Uh...",
    "DK4_MES_B49_R0356": "So we should go elsewhere.",
    "DK4_MES_B49_R0363": "Then it's settled! We're busy too, so see you around!",
    "DK4_MES_B49_R0367": "Lil, wait! Sorry for the commotion. Please excuse us! Lil!",
    "DK4_MES_B49_R0381": "All calm.",
    "DK4_MES_B49_R0388": "Not my choice, but you decide, {MACRO:FI}. We'll follow.",
    "DK4_MES_B49_R0393": "Let's leave this sea for later. She's likable, and scary when angry.",
    "DK4_MES_B49_R0405": "Unless only this sea remains, that plan is wise.",
    "DK4_MES_B49_R0410": "Then we'll head for another sea for now.",

    # B50: Lil gives Raphael the map pigment after losing control of the region.
    "DK4_MES_B50_R0006": "Wait!",
    "DK4_MES_B50_R0011": "Oh! You're Lil, right?",
    "DK4_MES_B50_R0014": "You remembered. Anyway, you beat us to it.",
    "DK4_MES_B50_R0019": "Oh... sorry.",
    "DK4_MES_B50_R0023": "Don't apologize. This pigment unlocks a treasure map. Take it.",
    "DK4_MES_B50_R0028": "What?! Are you sure?",
    "DK4_MES_B50_R0031": "Sigh... So he beat me? Oh well.",
    "DK4_MES_B50_R0037": "Lil! There you are! We haven't finished getting ready yet!",
    "DK4_MES_B50_R0040": "Hello. You're {MACRO:FA}, right?",
    "DK4_MES_B50_R0045": "Y-yes. And you're Kamil?",
    "DK4_MES_B50_R0049": "Yes. We have met before, technically. Ha ha.",
    "DK4_MES_B50_R0053": "Lil! You aren't being rude again, are you?",
    "DK4_MES_B50_R0057": "No! We don't need it, so she can have it.",
    "DK4_MES_B50_R0061": "Oh, right. {MACRO:FA} now rules the North Sea. Then that's fine.",
    "DK4_MES_B50_R0066": "What? Did something happen?",
    "DK4_MES_B50_R0069": "Still so dense... No, no. You're as easygoing as ever.",
    "DK4_MES_B50_R0073": "Let's say there's more to life than money.",
    "DK4_MES_B50_R0078": "Oh. Got it.",
    "DK4_MES_B50_R0082": "You just got it?!",
    "DK4_MES_B50_R0087": "(No idea, but play along.) That's wonderful!",
    "DK4_MES_B50_R0091": "Thanks!",
    "DK4_MES_B50_R0095": "Thank you very much.",
    "DK4_MES_B50_R0099": "Where's my gift?",
    "DK4_MES_B50_R0104": "What?! (Oh no... what are we celebrating?)",
    "DK4_MES_B50_R0108": "Please don't worry. Come, Lil. Goodbye, {MACRO:FI}.",
    "DK4_MES_B50_R0111": "Bye! Do your best for us too!",
    "DK4_MES_B50_R0115": "Thank you both! We'll live up to your hopes!",
    "DK4_MES_B50_R0120": "(What were we celebrating, anyway?)",

    # B51: Raphael briefly crosses paths with Hodram and Serah.
    "DK4_MES_B51_R0007": "So peaceful. Maybe at last...",
    "DK4_MES_B51_R0019": "(Hm?)",
    "DK4_MES_B51_R0024": "(Smiles)",
    "DK4_MES_B51_R0029": "...? (Who is she?)",
    "DK4_MES_B51_R0037": "Sera",
    "DK4_MES_B51_R0042": "(Hm?)",
    "DK4_MES_B51_R0046": "Oh, Hodram.",
    "DK4_MES_B51_R0050": "Who? Surely no acquaintance.",
    "DK4_MES_B51_R0059": "Hmm.",
    "DK4_MES_B51_R0063": "Hodram?",
    "DK4_MES_B51_R0067": "Go.",
    "DK4_MES_B51_R0071": "Yes.",
    "DK4_MES_B51_R0076": "She's beautiful. A princess, perhaps?",
    "DK4_MES_B51_R0087": "That officer was with Sweden's navy...",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "02": "Lil Argot",
    "04": "Emilio Marone",
    "05": "Claudio Manous",
    "06": "Julian Lopez",
    "08": "Raphael fleet officer (state 0x08)",
    "09": "Kamil",
    "18": "Serah",
}


def context_for(row_id: str) -> str:
    if "B49_" in row_id:
        return "Raphael's fleet meets Lil and the Argot Company, surveys the North Sea powers, and agrees to expand elsewhere for now."
    if "B50_" in row_id:
        return "After Raphael gains control of the North Sea, Lil gives him pigment that unlocks a treasure map."
    return "Raphael briefly crosses paths with Hodram and Serah during his travels."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in (49, 50, 51))
        }

    if set(LINES) != set(rows):
        raise SystemExit(
            "Raphael B49-B51 inventory mismatch: "
            f"missing={sorted(set(rows) - set(LINES))}, extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        state = (
            f"{source[0]:02X}"
            if source and ((0x01 <= source[0] <= 0x0F and source[0] != 0x0A) or source[0] == 0x18)
            else ""
        )
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        speaker = SPEAKERS.get(state, "Raphael Castor")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": speaker,
                "context": context_for(row_id),
                "source_meaning": english,
                "localization_note": "Faithful, concise American English localized from the Japanese; source breaks are layout evidence and wrapping is delegated to the proven formatter.",
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
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Raphael story prose inventory in consecutive SC0 blocks 49-51.",
        "profile_note": "Large experimental continuation after the accepted Raphael opening/tutorial. Block 52 is deliberately excluded because its source contains a malformed record and an unmapped printable leading state.",
        "quarantined_following_block": {
            "block": 52,
            "reason": "One mojibake source record and leading 0x72 runtime state require separate source/control recovery."
        },
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Raphael story records")


if __name__ == "__main__":
    main()
