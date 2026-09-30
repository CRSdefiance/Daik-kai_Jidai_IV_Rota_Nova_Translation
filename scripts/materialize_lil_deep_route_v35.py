from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v35.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
EXISTING = "DK4_MES_B120_R0012"
REMINDER = (
    "(Will she be all right?) Bruges is southwest of Amsterdam. Do your best.",
    "(Will she be all right?) Bruges is southwest of Amsterdam. Good luck!",
)
LINES = {
    "DK4_MES_B120_R0005": (
        "At last, we're at sea. I love the sound of the sea breeze and gulls. Kamil, hurry and give everyone orders.",
        "At sea at last! Love the breeze and gulls! Kamil, give the crew orders!",
    ),
    "DK4_MES_B120_R0009": (
        "Before that, FI, I'll teach you how to handle the ship too.",
        "{MACRO:FI}, first let's learn to sail.",
    ),
    "DK4_MES_B120_R0015": (
        "Even if you're bad at it, you need to learn. We don't know what will happen; be ready for an emergency.",
        "You need to learn, even so. Who knows what's ahead? Be ready when trouble strikes.",
    ),
    "DK4_MES_B120_R0019": ("Oh, fine, I understand.", "Ugh... All right!"),
    "DK4_MES_B120_R0023": (
        "Let's begin. First, check which way the ship is facing.",
        "Let's begin! Start by checking your ship's heading.",
    ),
    "DK4_MES_B120_R0027": (
        "FI, you tell everyone the fleet's course.",
        "{MACRO:FI}, tell everyone our course.",
    ),
    "DK4_MES_B120_R0031": (
        "A ship won't move where you want unless you point it that way.",
        "A ship won't sail where you want unless you point it that way.",
    ),
    "DK4_MES_B120_R0036": (
        "Set the direction the ship travels using the directional pad or stylus.",
        "Use the D-pad or stylus to steer.",
    ),
    "DK4_MES_B120_R0039": (
        "Press the directional pad or touch the screen in the direction you want to travel.",
        "Press a direction on the D-pad or tap it on the screen.",
    ),
    "DK4_MES_B120_R0042": ("How is it? Think you can do it?", "Think you can do it?"),
    "DK4_MES_B120_R0062": REMINDER,
    "DK4_MES_B120_R0080": REMINDER,
    "DK4_MES_B120_R0109": REMINDER,
    "DK4_MES_B120_R0124": ("Leave it to me!", "Count on me!"),
    "DK4_MES_B120_R0126": (
        "Don't we need to consider the wind?",
        "What about the wind?",
    ),
    "DK4_MES_B120_R0134": (
        "You're doing well! I'm counting on you, Admiral!",
        "Nice work! Counting on you, Admiral!",
    ),
    "DK4_MES_B120_R0137": (
        "Don't talk to me right now! The wind is coming from here, so I need to adjust the sails to match, right?",
        "Don't distract me! The sails match the wind's direction, right?",
    ),
    "DK4_MES_B120_R0142": (
        "I understand how to set our heading, but I want to catch the wind and really race ahead.",
        "Now steering makes sense, but let's catch the wind and pick up speed!",
    ),
    "DK4_MES_B120_R0146": (
        "For that, the sails must catch the wind properly. Next, give orders for the sails' direction.",
        "To gain speed, the sails must catch the wind. Next, adjust their angle.",
    ),
    "DK4_MES_B120_R0150": ("It's such a hassle...", "What a hassle..."),
    "DK4_MES_B120_R0155": (
        "Set the sails' direction with L and R. Adjusting the sails increases the ship's speed.",
        "Turn the sails with L and R. Adjust them to increase your speed.",
    ),
    "DK4_MES_B120_R0159": (
        "Press L to turn the sails left, and R to turn them right.",
        "Use L to turn the sails left, and R to turn them right.",
    ),
    "DK4_MES_B120_R0163": (
        "When using the stylus, the sails turn to the best angle automatically. Touch the flagship to stop.",
        "Using the stylus sets the best sail angle. Tap your flagship to stop.",
    ),
    "DK4_MES_B120_R0167": (
        "Watch the wind's direction. Relative to the ship's heading, let the wind strike the back of the sails.",
        "Watch the wind and heading. Catch wind on the back of each sail.",
    ),
    "DK4_MES_B120_R0171": ("Huh? I don't really understand...", "Huh? Don't get it..."),
    "DK4_MES_B120_R0174": (
        "You'll be fine once you get used to it. Now, practice!",
        "You'll get used to it. Practice!",
    ),
    "DK4_MES_B120_R0177": (
        "Check speed with the onscreen speed meter. To increase it, adjust the sails so the bar is as long as possible.",
        "Check the speed meter onscreen. Adjust the sails for the longest bar to gain speed.",
    ),
    "DK4_MES_B120_R0186": REMINDER,
}
SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0xFE: "Tutorial panel"}
TEXT_LEADS = {0x82, 0x95}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B120_")}
    if set(LINES) | {EXISTING} != expected:
        raise ValueError("B120 coverage does not match clean source")
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Bare Lil response"),
            "context": "Lil's first sailing tutorial: Kamil teaches heading, sail adjustment, wind, and the voyage from Amsterdam to Bruges.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese with adjacent tutorial dialogue reviewed. "
                "Preserves directions, button labels, automatic stylus sail adjustment, and flagship stop action. "
                "FI remains a runtime given-name macro; 82/95 starts are text, not speaker states."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "The 28 untranslated B120 sailing-tutorial records; V21's R0012 remains inherited.",
        "inventory": {"identified_records": 29, "translated_records": 28, "inherited_records": [EXISTING], "blocks": {"120": 28}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
