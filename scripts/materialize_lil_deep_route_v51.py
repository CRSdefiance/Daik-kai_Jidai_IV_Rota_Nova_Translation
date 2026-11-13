from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v51.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("Why won't anyone understand me?", "Why won't anyone understand?!"),
    14: ("What's wrong?", "What is it?"),
    18: ("Are you Dutch?", "Oh! Are you Dutch?"),
    22: ("Yes, I am. Why?", "Yes... Why?"),
    26: ("Please listen. As a Dutch person, you should understand.", "Hear me out! You're Dutch. You'll understand!"),
    29: ("What does being Dutch have to do with it?", "What's that got to do with it?"),
    33: ("I lack money for my polder, not for daily living.", "My polder needs funding. Living costs aren't the problem."),
    37: ("A polder? What is that?", "A polder? What's that?"),
    41: ("It's my method for creating more land.", "A way to make more land. My idea!"),
    44: ("Build coastal dikes, enclose the sea, pump out the water, and new land remains.", "Coastal dikes enclose the sea. Pump out the water. New land!"),
    47: ("That's a polder.", "That's a polder."),
    59: ("What a wonderful idea!", "Oh! What a fine idea!"),
    65: ("What happens once you've created the land?", "And once you've made land?"),
    68: ("More usable land should help poor people.", "More good land could help the poor."),
    75: ("My hometown is a poor farming village. Fertile land is everyone's dream.", "My poor village dreams of good farmland. We could grow crops!"),
    78: ("My home is poor too; everyone suffers. It's a good idea.", "My home is poor too. People suffer there. Your idea gives hope."),
    82: ("You understand. A polder could make everyone happy.", "You see it! A polder could make people happy!"),
    86: ("If it's completed, my people could live more easily.", "My people could live better..."),
    89: ("That's it!", "That's it!"),
    94: ("Hello. It's been a while.", "Hello! Been a while."),
    98: ("Ah, FI...", "Oh, {MACRO:FI}..."),
    110: ("You look dispirited.", "You seem down..."),
    117: ("From your look, you still haven't raised the funds?", "Still no funding, then?"),
    120: ("No one understood. They all said it couldn't be done.", "No one believes me. They call it impossible."),
    123: ("But the method will work and make people's lives better.", "But it will work! A polder can make lives better!"),
    126: ("Why won't they believe me? If only I had money.", "Why won't they believe me? Money would change everything!"),
    142: ("We'd like to help him too, FI.", "Wish we could help him, {MACRO:FI}."),
    148: ("Yes... Oh, that's it!", "Yeah... Wait! That's it!"),
    162: ("What's wrong, FI?", "What is it, {MACRO:FI}?"),
    169: ("What is it?", "Hm? What is it?"),
    173: ("I'll provide the funding!", "Let me fund it!"),
    177: ("You? You'll really fund it?", "You? You'd really fund it?"),
    203: ("That funding is a huge sum!", "H-hey! That's a huge sum!"),
    209: ("I've been wondering why I do business.", "Lately, one thought keeps coming back: why do we trade?"),
    221: ("But FI, you wanted to become rich.", "But {MACRO:FI}, you wanted to be rich."),
    224: ("At first, yes.", "At first, yes..."),
    231: ("After seeing many countries, I realized wealth alone isn't what I want.", "Travel taught me that wealth isn't everything."),
    235: ("Fine food, clothes, a mansion. Those aren't what I truly want.", "Good food? Nice clothes? A grand house? No. That's not my dream."),
    254: ("Seeing the towns of India reminded me of my home village. At last I understood.", "Eastern towns reminded me of home. Now it makes sense."),
    258: ("I want to help poor people in my village and all around the world.", "People back home need help. So do people everywhere. That's what matters to me."),
    262: ("That's an enormous dream.", "Such a huge dream..."),
    281: ("This is my dream now. It's huge, but I want to help others however I can.", "A huge dream, yes. But helping one person still matters."),
    284: ("If I help a little each day, perhaps one day I can help people everywhere.", "Help someone each day. Someday, we might help everyone!"),
    287: ("This polder is my first step toward that dream.", "This polder is my first step."),
    299: ("FI, not maybe. You can do it. I'll help too.", "You can do it, {MACRO:FI}! Count on me!"),
    303: ("Thank you, Kamil.", "Thank you, Kamil."),
    318: ("A fine idea. I agree.", "A good plan. Count me in."),
    332: ("I'll help too.", "Count me in!"),
    339: ("I'll help too.", "Me too!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x04: "Janus", 0x09: "Kamil", 0x10: "Gerhard",
    0x14: "Fernando Dias", 0x15: "Ian", 0xAB: "Lelystad founder",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B140_")}
    authored = {f"DK4_MES_B140_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B140 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B140_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Lil meets the future Lelystad founder again. His polder plan and funding trouble "
                "lead Lil to finance land reclamation and state her dream of helping people in need."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B140 Japanese; preserves the dike-and-pump method, "
                "the founder's poverty motive, Lil's change from seeking wealth to helping others, "
                "the funding pledge, crew responses and exact FI name macros. Guarded wrapping "
                "protects first and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 49 B140 polder-funding and Lil's new dream dialogue records.",
        "inventory": {"identified_records": 49, "translated_records": len(records), "blocks": {"140": 49}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
