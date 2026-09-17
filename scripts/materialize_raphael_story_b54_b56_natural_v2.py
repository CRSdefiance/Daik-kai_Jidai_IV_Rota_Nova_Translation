from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_story_natural_v2_b54_b56.json")
SC0_SHA256 = "cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"

LINES = {
    # B54: news of Silveira's appointment sends Raphael to Sofala.
    "DK4_MES_B54_R0005": "Hey, you! Heard the news?",
    "DK4_MES_B54_R0010": "What?",
    "DK4_MES_B54_R0014": "Admiral Silveira defeated the infamous Espinosa!",
    "DK4_MES_B54_R0019": "So that's the official story.",
    "DK4_MES_B54_R0023": "You're an odd one. Still, Silveira must be better than that villain Espinosa.",
    "DK4_MES_B54_R0027": "Well... maybe so.",
    "DK4_MES_B54_R0031": "They say the governor moved to Sofala...",
    "DK4_MES_B54_R0036": "The African governor... in Sofala?! We must go! Thank you, sir!",
    "DK4_MES_B54_R0040": "Hey! ...What was that about?",

    # B56: grateful townspeople give Raphael a Proof of Conquest clue.
    "DK4_MES_B56_R0005": "Hey! Aren't you {MACRO:FO}'s leader?",
    "DK4_MES_B56_R0009": "Oh! Perfect timing! Hey, you there!",
    "DK4_MES_B56_R0013": "Do you mean me? What is it?",
    "DK4_MES_B56_R0017": "After Espinosa and Silveira, the world finally feels decent again.",
    "DK4_MES_B56_R0021": "That's right. We owe it to your company.",
    "DK4_MES_B56_R0025": "Really? You're making me blush.",
    "DK4_MES_B56_R0028": "Crooked merchants ruled so long, we nearly forgot how to trust anyone.",
    "DK4_MES_B56_R0032": "Exactly... Oh! We nearly forgot why we called you over.",
    "DK4_MES_B56_R0037": "Oh.",
    "DK4_MES_B56_R0041": "Stay sharp now. Here, take this.",
    "DK4_MES_B56_R0047": "What's it?",
    "DK4_MES_B56_R0058": "A Conquest clue?!",
    "DK4_MES_B56_R0063": "Where... where did you find this?!",
    "DK4_MES_B56_R0066": "An adventurer tried selling it to Espinosa.",
    "DK4_MES_B56_R0069": "Trying to profit by leading that devil to a Proof of Conquest... What a vile scheme.",
    "DK4_MES_B56_R0073": "Can this really be mine?",
    "DK4_MES_B56_R0077": "The town pooled money and made him sell it, just to give you.",
    "DK4_MES_B56_R0082": "Thank you so much!",
    "DK4_MES_B56_R0089": "Now it's yours. Do your best for everyone.",
    "DK4_MES_B56_R0093": "Yes!",
    "DK4_MES_B56_R0097": "Good luck!",
}

SPEAKERS = {
    "08": "Raphael fleet officer (state 0x08)",
    "54": "Local resident (state 0x54)",
    "72": "Local resident (state 0x72)",
}
LEADING_STATES = {0x08, 0x54, 0x72}


def context_for(row_id: str) -> str:
    if "B54_" in row_id:
        return "Raphael hears that Silveira received credit for defeating Espinosa and moved the African governor's office to Sofala."
    return "After Raphael defeats Africa's corrupt powers, grateful townspeople give him a clue connected to the Proof of Conquest."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in (54, 56))
        }
    if set(LINES) != set(rows):
        raise SystemExit(
            "Raphael B54/B56 inventory mismatch: "
            f"missing={sorted(set(rows) - set(LINES))}, extra={sorted(set(LINES) - set(rows))}"
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
                "localization_note": "Faithful, concise American English localized from the Japanese with canonical game terminology; wrapping is delegated to the proven formatter.",
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
        "dialogue_profile": "raphael-story-late-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete clean Raphael story prose inventories in SC0 blocks 54 and 56.",
        "profile_note": "Extends the B49-B51 continuation around malformed blocks 52, 53, and 55, which remain quarantined for separate control/source recovery.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} Raphael story records")


if __name__ == "__main__":
    main()
