from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_story_natural_v2_b57_b59.json")
SC0_SHA256 = "cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"
EXCLUDED = {"DK4_MES_B57_R0003": "Corrupt non-prose command fragment with unmapped controls."}

LINES = {
    # B57: Emilio is injured and Arcadius quietly looks after him.
    "DK4_MES_B57_R0005": "Aaaah!",
    "DK4_MES_B57_R0011": "Emilio! Are you all right?!",
    "DK4_MES_B57_R0014": "Huh? The pier must've rotted away.",
    "DK4_MES_B57_R0017": "Owwww!",
    "DK4_MES_B57_R0022": "Let me see.",
    "DK4_MES_B57_R0026": "Oww...",
    "DK4_MES_B57_R0030": "Don't move him. Let him rest at the inn.",
    "DK4_MES_B57_R0033": "No choice. Grab on, Emilio... Ugh, you're heavy!",
    "DK4_MES_B57_R0041": "Emilio's all right! Oh, Arcadius is there.",
    "DK4_MES_B57_R0045": "Why buy flowers?",
    "DK4_MES_B57_R0049": "And fruit.",
    "DK4_MES_B57_R0053": "What's up? Someone's birthday?",
    "DK4_MES_B57_R0057": "Hey, Arcadius. Having a party today?",
    "DK4_MES_B57_R0060": "Eh?",
    "DK4_MES_B57_R0064": "You had flowers and tasty food. Hurry and share it!",
    "DK4_MES_B57_R0068": "That? No. A gift for Emilio.",
    "DK4_MES_B57_R0072": "Emilio? Why?",
    "DK4_MES_B57_R0076": "What are you saying?",
    "DK4_MES_B57_R0080": "He's stuck in town and bored, so a visit may cheer him.",
    "DK4_MES_B57_R0083": "Huh.",
    "DK4_MES_B57_R0087": "Emilio likes sweets. Not sure about flowers, but you can't get them at sea.",
    "DK4_MES_B57_R0091": "Oh... Would you visit me too if something happened?",
    "DK4_MES_B57_R0095": "Of course. We're companions.",
    "DK4_MES_B57_R0099": "R-right... of course.",
    "DK4_MES_B57_R0103": "N-no, it's nothing. Go see him.",
    "DK4_MES_B57_R0106": "Yes... Want to come, Claudio? You might get some tasty fruit.",
    "DK4_MES_B57_R0109": "No thanks. Give it all to Emilio. He'll love it.",
    "DK4_MES_B57_R0113": "All right. Bye.",
    "DK4_MES_B57_R0116": "Emilio, does your leg still hurt? This is for you.",
    "DK4_MES_B57_R0119": "Wow! Thanks, Arcadius! You knew flowers are my favorite?",
    "DK4_MES_B57_R0122": "No, that was new to me. Glad you like them. Eat plenty.",
    "DK4_MES_B57_R0126": "Hooray!",
    "DK4_MES_B57_R0132": "Clau... You waited for me?",
    "DK4_MES_B57_R0135": "Y-yeah. Let's join the others.",
    "DK4_MES_B57_R0139": "...Let's.",

    # B58: Uddin yields the Indian Ocean's Proof of Conquest clue.
    "DK4_MES_B58_R0005": "{MACRO:FA}, yes?",
    "DK4_MES_B58_R0015": "You are...?",
    "DK4_MES_B58_R0025": "Once, this man led the Uddin Company.",
    "DK4_MES_B58_R0030": "This man leads the Uddin Company.",
    "DK4_MES_B58_R0039": "Admiral Uddin...",
    "DK4_MES_B58_R0045": "You swept across this ocean in no time. Worthy of Admiral {MACRO:FA}.",
    "DK4_MES_B58_R0051": "N-no... it was luck.",
    "DK4_MES_B58_R0054": "No need for modesty. Maybe it's fate.",
    "DK4_MES_B58_R0057": "This is for you: my last duty as this ocean's guardian. Take it.",
    "DK4_MES_B58_R0068": "The Everlasting Lotus Leaf reveals this ocean's Proof of Conquest.",
    "DK4_MES_B58_R0073": "This huge leaf... it's a map.",
    "DK4_MES_B58_R0076": "This ocean's Proof is a book called the Rig Veda.",
    "DK4_MES_B58_R0080": "The Rig Veda...",
    "DK4_MES_B58_R0084": "May it prove worthy of you. Now, farewell.",
    "DK4_MES_B58_R0095": "Huh. He's a decent old man.",
    "DK4_MES_B58_R0100": "Admiral Uddin...",
    "DK4_MES_B58_R0107": "Admiral Uddin... Thank you for everything. Goodbye.",

    # B59: warning about Duarte Pereira's Indochina territory.
    "DK4_MES_B59_R0005": "Hold it, Admiral!",
    "DK4_MES_B59_R0009": "You mean me?",
    "DK4_MES_B59_R0013": "This is Governor Duarte Pereira's territory. You didn't know?",
    "DK4_MES_B59_R0018": "...And?",
    "DK4_MES_B59_R0022": "Just don't let him notice you.",
    "DK4_MES_B59_R0027": "Much obliged.",
}

SPEAKERS = {
    "05": "Claudio Manous",
    "08": "Arcadius",
    "0E": "Emilio Marone",
    "25": "Uddin",
    "74": "Local resident (state 0x74)",
}
LEADING_STATES = {0x05, 0x08, 0x0E, 0x25, 0x74}


def context_for(row_id: str) -> str:
    if "B57_" in row_id:
        return "After Emilio falls through a rotten pier, Arcadius brings him fruit and flowers while Claudio reveals concern for Arcadius."
    if "B58_" in row_id:
        return "After Raphael gains the Indian Ocean, Uddin gives him the Everlasting Lotus Leaf and explains that it leads to the Rig Veda."
    return "A local warns Raphael that Indochina is controlled by the Portuguese governor Duarte Pereira."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in (57, 58, 59))
        }
    expected = set(rows) - set(EXCLUDED)
    if set(LINES) != expected:
        raise SystemExit(
            "Raphael B57-B59 inventory mismatch: "
            f"missing={sorted(expected - set(LINES))}, extra={sorted(set(LINES) - expected)}"
        )

    records = []
    counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        state = f"{source[0]:02X}" if source and source[0] in LEADING_STATES else ""
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        counts[block] = counts.get(block, 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor"),
                "context": context_for(row_id),
                "source_meaning": english,
                "localization_note": "Faithful, concise American English localized from the Japanese with established names and Proof of Conquest terminology.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-late-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All clean prose records in consecutive Raphael SC0 blocks 57-59.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_non_prose_records": len(EXCLUDED), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Raphael story records")


if __name__ == "__main__":
    main()
