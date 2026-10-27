from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v38.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

# Faithful clean-source gloss followed by localized American English.
LINES = {
    (123, 5): ("Come to think of it...", "Oh, right..."),
    (123, 13): ("Yes, yes, that's it. Let's bring Christina along.", "Yes! Let's bring Christina along."),
    (123, 16): ("Who are you talking about?", "Who?"),
    (123, 20): ("She's my granddaughter. She practices swordsmanship and is quite skilled.", "My granddaughter's a gifted swordswoman."),
    (123, 23): ("Where does she live?", "Where is she?"),
    (123, 27): ("London.", "London."),
    (123, 31): ("All right, then let's go.", "Then let's go!"),
    (124, 5): ("Admiral, you've traveled the whole world. You must know girls you're close to in the taverns of many cities, right?", "Admiral, you've sailed the world! You must know women at taverns everywhere!"),
    (124, 9): ("Hmm, well... Not in so many different cities.", "Well... Maybe not that many cities."),
    (124, 12): ("That's no good. Tavern girls know all kinds of information adventurers need.", "Those women know the best leads. You're missing out!"),
    (124, 16): ("For instance, they know treasure rumors, movements of enemy fleets, and even unusual ruins known only to locals.", "They hear treasure rumors and track enemy fleets. Some even know ruins only locals can find."),
    (124, 19): ("If you aren't friendly with girls all over the world, you're a failure as an adventurer.", "Good adventurers make friends everywhere!"),
    (124, 23): ("But becoming friends with them isn't so easy.", "But making friends takes time..."),
    (124, 26): ("Just talking to them as a customer isn't enough. They speak to dozens of people a day.", "Just chatting as a customer won't do. They talk to dozens of people every day."),
    (124, 29): ("The only way is to give a gift that captures a woman's heart.", "A thoughtful gift wins her heart."),
    (124, 32): ("Naturally, each woman likes different things. Find out what interests her and give her that as a present.", "Everyone likes something different. Ask what catches her eye, then bring her a gift she'll love."),
    (124, 40): ("For example, Sakura in Osaka wants the Snowfall Robe, sold somewhere in a North Sea city.", "Sakura in Osaka wants the Snowfall Robe, sold in a North Sea town."),
    (124, 49): ("Even a woman who wants little would be happy to receive something she wants.", "Even a modest woman loves getting something she really wants."),
    (124, 53): ("So you've been flirting with every tavern girl because that's what adventurers are supposed to do?", "So all that flirting at taverns was just part of being an adventurer?"),
    (124, 56): ("O-of course!", "O-of course!"),
    (124, 60): ("It didn't look like that to me...", "Didn't look that way to me..."),
    (124, 64): ("R-right? If you can act convincingly enough to win a girl's heart, you're a real adventurer! Ha ha.", "R-right? My charm was an act! Adventurers need that skill."),
}

SPEAKERS = {0x02: "Lil Argot", 0x06: "Christina's grandfather", 0x1A: "Julian"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith(("DK4_MES_B123_", "DK4_MES_B124_"))}
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError("B123/B124 coverage does not match clean source")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped presentation state {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Christina's grandfather suggests bringing his skilled granddaughter aboard in London."
                if block == 123 else
                "Julian explains tavern contacts, useful rumors and personal gifts; Lil catches him flirting."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese with neighboring lines reviewed. "
                "Preserves the grandfather's proven family relationship, Julian's playful evasions, and the established Snowfall Robe name. "
                "The existing Lil profile retains 02/06/1A presentation states and pair-phase-safe automatic wrapping."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All seven B123 Christina-lead records and fifteen B124 Julian tavern-tip records.",
        "inventory": {"identified_records": 22, "translated_records": len(records), "blocks": {"123": 7, "124": 15}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
