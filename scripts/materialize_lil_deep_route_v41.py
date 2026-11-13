from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v41.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# Clean B127, in scene order. The source 5F/5C bytes select the opponent and barkeep.
LINES = {
    5: ("Ten... fifteen... thirty chips!", "10... 15... 30 chips!"),
    9: ("Now what will you do? Raise or fold?", "Well? Raise or fold?"),
    13: ("Ugh! Damn it! I cannot call that bet. I fold!", "Damn! Can't call that! Gotta fold!"),
    17: ("I see. That's too bad.", "Oh... Too bad."),
    21: ("What?! You had no hand at all?", "W-what?! You had nothing?!"),
    24: ("Luck. Make it your ally and even a reckless bluff can be a winning card.", "Luck. Get it on your side, and even a wild bluff can win."),
    28: ("You expected me to bluff, didn't you? But...", "You knew a bluff was coming. But..."),
    32: ("Luck made you misread it as a bluff meant to get you to raise your chips.", "You mistook it for a bluff to make you raise. Luck was on my side."),
    36: ("Ugh... I lost.", "Ugh... Beaten..."),
    39: ("Fernando, that was an amazing match.", "What a game!"),
    42: ("Kamil, you saw that? Barkeep, pour him a drink too. My treat.", "Kamil? You saw that? Barkeep, get him a drink. My treat."),
    46: ("All right.", "Sure!"),
    50: ("Thanks! Was that match what you mean when you say to watch closely?", "Thanks! Was that what you mean by 'watch closely'?"),
    53: ("Heh. You're sharp. Exactly.", "Heh. Sharp! That's right."),
    57: ("Luck and close observation, or insight. You need both to win at gambling.", "Luck and insight. Miss either one, and you won't win at cards."),
    61: ("Kamil, here's a question: how can you make luck your ally?", "Kamil, tell me: how do you get luck on your side?"),
    65: ("Huh? How? Hmm... Can you really do that?", "Huh? Can you really do that?"),
    69: ("Develop a habit of winning.", "Make winning a habit."),
    73: ("A habit of winning?", "Winning?"),
    77: ("Luck does not make people winners. Luck sides with people who win.", "Luck doesn't make winners. Winners make luck work for them."),
    81: ("And to develop that habit of winning...", "And to make winning a habit..."),
    85: ("Insight. Sharpening it raises your chances of winning.", "Hone your insight. Boost your odds!"),
    89: ("You're clever, Kamil. My insight won the early rounds, causing him to misread the last one.", "Smart, Kamil. My early wins came from reading him. That's why he misread the last play."),
    92: ("Fernando, you're amazing.", "You're amazing!"),
    96: ("May I ask why you came aboard FI's ship?", "Why'd you join {MACRO:FI}'s crew?"),
    100: ("Gulp... Cough, cough.", "Ghk... Cough, cough!"),
    103: ("Are you all right?", "Okay?"),
    107: ("I told you before: well, things happened.", "Remember? Things happened..."),
    110: ("That's what I want to know. Did you lose a bet to FI?", "Wait... Did you lose a bet to {MACRO:FI}?"),
    114: ("He flinches.", "...!"),
    118: ("So you did lose.", "Oh... you did lose."),
    122: ("You're really sharp, aren't you?", "Ugh... Too sharp."),
    125: ("That little girl kept pestering me, so I said I'd join if she beat me. That was my mistake.", "She kept nagging. Win one game, get a crewman. Big mistake."),
    129: ("I cannot believe you lost. Why did you?", "You lost? That's hard to believe! What happened?"),
    133: ("She challenged me to cards, and I accepted. But...", "She challenged me to cards, so we played. But..."),
    137: ("She knew neither poker, baccarat, nor blackjack. She could only play Old Maid.", "She didn't know poker, baccarat, or blackjack. Only Old Maid!"),
    141: ("Can a grown man seriously play 'Which card is the old maid?'", "How's a grown man supposed to take 'Pick the old maid' seriously?!"),
    145: ("You were unlucky, Fernando.", "...Just bad luck, then."),
}

SPEAKERS = {0x09: "Kamil", 0x14: "Fernando Dias", 0x5C: "Barkeep", 0x5F: "Fernando's opponent"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B127_")}
    if {f"DK4_MES_B127_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B127 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B127_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped speaker {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Fernando wins a card game by bluffing; Kamil asks how luck and insight work."
                if number < 96 else
                "Kamil discovers Fernando joined Lil after losing to her at Old Maid."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese in scene order; keeps the betting logic, Fernando's embarrassment, "
                "Old Maid as the English name for baba-nuki, the FI name macro, and each source speaker selector. "
                "Natural phrasing avoids unsafe literal uppercase I/F renderer bytes. Guarded wrapping protects initial glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v41-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 38 B127 Fernando gambling, insight and Old Maid recruitment records.",
        "inventory": {"identified_records": 38, "translated_records": len(records), "blocks": {"127": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
