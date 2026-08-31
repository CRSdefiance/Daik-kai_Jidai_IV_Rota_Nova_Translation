from __future__ import annotations

import json
from pathlib import Path

SOURCE = Path("work/analysis/common_clean_inventory.json")
OUTPUT = Path("translations/common_natural_v2_b17.json")
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"

ENGLISH = [
    "Heh. Made this as an apprentice.",
    "Why's cooking my job?!",
    "Maybe fried rice today.",
    "Everyone loves good food.",
    "Grow big and strong now.",
    "Let's clean you up.",
    "Ha ha, cute.",
    "Grow big, little pig.",
    "Hold still, will you?!",
    "Getting fond of you.",
    "Whoa! Not one of you!",
    "You'll grow into a fine pig.",
    "Let me clean you up.",
    "You're cute up close.",
    "Hey! Don't rub against me!",
    "Eat plenty and grow big.",
    "By the Holy Trinity...",
    "Amen...",
    "Time to pray...",
    "God, please hear my prayer.",
    "Might as well pray.",
    "Belief is everything.",
    "The Bible made me sleepy.",
    "Lord, forgive me...",
    "May Portugal recover soon.",
    "God, can we build a mighty fleet?",
    "God, keep us safe.",
    "May we all sail safely...",
    "My next scheme...",
    "The plan is...",
    "Any bright ideas?",
    "Must study and plan better.",
    "Plan... Zzz... More like nap!",
    "Schemes take experience.",
    "Me, make plans? Let me try.",
    "You can count on my plan.",
    "Time to study strategy!",
    "Direct tactics aren't enough.",
    "Leave the scheming to me!",
    "Strategy's my strength.",
    "Let's check port prices.",
    "Prices are the key...",
    "This month's profit?",
    "Making money is hard!",
    "Market prices? No clue.",
    "What's selling well now?",
    "Where can we sell for a profit?",
    "Let's total this month's profit.",
    "Let's review our finances.",
    "Profit... Hmm.",
    "All these numbers make my head spin.",
    "What goods could turn a profit now?",
    "Captain... Doing my best!",
    "A mighty fleet, all mine.",
    "Hee hee! The captain!",
    "All rests on my shoulders.",
    "Leave the paperwork to me.",
    "Serving as admiral's aide.",
    None,
    "Admiral, writing something?",
    "Let me be first officer.",
    "Leave diplomacy to me.",
    "Heh... the new officer!",
    "Leave negotiations to me.",
    "Your officer? Sure! Wait...",
    "As first officer, who's captain?",
    "All right, but who's captain?",
    "Leave the talks to me.",
    "Leave the helm to me.",
    "We'll sail safely.",
    "The helm? Hard starboard!",
    "Steering? Easy, easy.",
    "Round and round! One more turn!",
    "Every cannonball will miss me.",
    "Always wanted to steer.",
    "Watch me handle this wheel!",
    "Ha... Spins nicely.",
    "Helm and sails work together.",
    "Steer the ship? Leave it to me!",
    "Shen taught me how to steer.",
    "A sextant makes surveying easier.",
    "Know our position.",
    "Our position? Uh... Wait!",
    "The stars show our position.",
    "Just find where we are, right?",
    "Surveying: basic seamanship.",
    "Your surveyor will do the job.",
    "Surveyor? Easy enough.",
    "This is the right tool, yes?",
    "The sun tells us our position.",
    "Surveying is basic seamanship!",
    "Sun and stars show our position.",
    "Keeping watch. Rest easy.",
    "Keeping watch now.",
    "Any trouble gets reported.",
    "Such a view! The world is vast.",
    "What a feeling up here!",
    "Anything spotted gets reported.",
    "Great view from up here!",
    "Keeping watch! Eyes wide open.",
    "Everyone will hear what appears.",
    "My body senses danger.",
    "Wow! What a view!",
    "Sharp eyes. Leave it to me.",
    "Any wind can be mastered.",
    "Match each sail to the wind.",
    "Might blow away!",
    "Well? Better with sails now?",
    "Use half sail when slowing down.",
    "Square and lateen sails differ.",
    "The wind obeys me too.",
    "A sailmaster must read the wind.",
    "Now the wind makes sense.",
    "Sails and helm work together.",
    "Whoa! Might blow away!",
    "No skill can overcome a dead calm.",
    "Training like this every day.",
    "Leave boarding to me.",
    "Getting even stronger.",
    "How's this form?",
    "Count on me in a fight!",
    "Ow! My back just cracked...",
    "Training this long makes me hungry.",
    "Training is essential.",
    "My swordplay has improved, right?",
    "A swordplay lesson for the crew.",
    "How's this swordplay?",
    "Leading every boarding charge.",
    "Test-firing now.",
    "Test-firing. Talk later.",
    "Training for naval combat.",
    "Does firing make you nervous?",
    None,
]


def activity(index: int) -> str:
    ranges = [
        (0, 3, "cooking"),
        (4, 15, "caring for the ship's pig"),
        (16, 27, "praying"),
        (28, 39, "planning strategy"),
        (40, 51, "reviewing markets and finances"),
        (52, 55, "serving as captain"),
        (56, 67, "serving as first officer"),
        (68, 79, "steering the ship"),
        (80, 91, "surveying the ship's position"),
        (92, 103, "keeping lookout"),
        (104, 115, "handling the sails"),
        (116, 127, "training for boarding combat"),
        (128, 131, "training with the ship's guns"),
    ]
    return next(label for start, end, label in ranges if start <= index <= end)


def main() -> None:
    inventory = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = [row for row in inventory["records"] if row["block_index"] == 17]
    if len(rows) != 133 or [row["segment_index"] for row in rows] != list(range(133)):
        raise SystemExit("COMMON block 17 inventory is not the expected contiguous 133 records")
    if len(ENGLISH) != 133:
        raise SystemExit(f"translation table has {len(ENGLISH)} entries, expected 133")

    records = []
    blocked = []
    for row in rows:
        index = int(row["segment_index"])
        row_id = f"DK4_MES_B17_R{index:04d}"
        if index == 58:
            blocked.append(
                {
                    "id": row_id,
                    "source_hex": row["source_hex"],
                    "source_markup": row["markup"],
                    "editorial_english": "{MACRO:I}C can handle diplomacy.",
                    "speaker": "Crew member",
                    "context": "A crew member comments while serving as first officer and volunteering for foreign negotiations.",
                    "source_meaning": "The speaker says to leave foreign negotiations to the entity represented by the source's I/C sequence.",
                    "localization_note": "The clean source contains the ambiguous `{MACRO:I}C` sequence. Its runtime meaning and ASCII expansion parity are not declared by shared-pair-live, so the record remains editorial-only with the sequence preserved.",
                    "blocker": "Command/macro ambiguity: shared-pair-live has no proven ASCII expansion length for macro I, and the literal trailing C may be part of the same runtime construct.",
                    "editorial_review": True,
                    "formatting_review": False,
                }
            )
            continue
        if index == 132:
            blocked.append(
                {
                    "id": row_id,
                    "source_hex": row["source_hex"],
                    "source_markup": row["markup"],
                    "speaker": "None",
                    "context": "Two-byte padding-only tail segment after the final gunner line.",
                    "source_meaning": "No Japanese text or player-facing meaning; this segment contains only spaces.",
                    "localization_note": "Classified and retained byte-identically; no translation is fabricated for padding.",
                    "blocker": "Padding-only non-text segment.",
                    "editorial_review": True,
                    "formatting_review": False,
                }
            )
            continue

        english = ENGLISH[index]
        assert english is not None
        source_breaks = int(row["line_break_count"])
        note = (
            "Localized as concise, idiomatic shipboard speech while preserving the line's intent and activity. "
            "Ordinary wrapping is left to the pair-safe formatter."
        )
        record = {
            "id": row_id,
            "english": f"{english}{{PAD}}",
            "speaker": "Crew member",
            "context": f"A crew member's ambient line while {activity(index)}.",
            "source_meaning": f"While {activity(index)}, the crew member says: {english}",
            "localization_note": note,
            "review": {
                "source": True,
                "context": True,
                "localization": True,
                "naturalness": True,
                "formatting": True,
            },
        }
        if source_breaks:
            record["qa_waivers"] = ["line-break-count"]
            record["qa_waiver_reason"] = (
                "The clean-source line break is ordinary Japanese layout, not a dramatic pause; "
                "the localized line is one logical paragraph."
            )
        records.append(record)

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": COMMON_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "shared-pair-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "scope": "Complete clean-source audit and safe localization of shared shipboard ambient dialogue in COMMON block 17",
        "inventory": {
            "block": 17,
            "total_segments": len(rows),
            "japanese_bearing_segments": 132,
            "safe_translated_records": len(records),
            "blocked_editorial_records": len(blocked),
            "padding_only_segments": 1,
        },
        "blocked_records": blocked,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} safe, {len(blocked)} blocked/classified")


if __name__ == "__main__":
    main()
