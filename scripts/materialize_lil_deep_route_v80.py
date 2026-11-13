from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v80.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (180, 5): ("A woman notices another lady's lovely scent.", "What a lovely scent she had!"),
    (180, 9): ("Her friend noticed it too.", "You noticed it too?"),
    (180, 13): ("The woman wonders what scent it was.", "What fragrance was it?"),
    (180, 17): ("Her friend predicts the scent will become fashionable.", "No idea. But it'll surely catch on."),
    (180, 20): ("The woman wants to get some before everyone else.", "We must get some before the rest!"),
    (180, 24): ("Her friend agrees.", "Quite right."),
    (180, 28): ("The woman proposes asking the lady directly next time.", "Let's ask her about it next time."),
    (180, 31): ("Her friend approves of the idea.", "Great idea. Let's do it!"),
    (180, 34): ("The woman bids her friend farewell.", "Good day, then."),
    (180, 38): ("Her friend returns the farewell.", "Good day."),
    (180, 73): ("The market notice predicts a Lisbon spice boom.", "Spices may catch on in Lisbon."),
    (181, 6): ("A woman asks whether her friend saw a bright ruby.", "Did you see that bright red ruby?"),
    (181, 9): ("Her friend praises the gem.", "Yes. Magnificent!"),
    (181, 13): ("A third woman asks what they are discussing.", "Oh? What's this about?"),
    (181, 17): ("The first woman names the lady's necklace.", "The necklace that lady wore."),
    (181, 20): ("The third woman remembers the large ruby.", "Ah, that huge, lovely stone!"),
    (181, 23): ("The second woman dreams of receiving such a gift from a man.", "Such a gift from a man... just once!"),
    (181, 27): ("The first woman agrees and sighs.", "Quite so... Sigh."),
    (181, 31): ("The second woman sighs.", "Sigh."),
    (181, 35): ("The third woman sighs.", "Sigh."),
    (181, 39): ("The market notice predicts an Athens ruby boom.", "Rubies may catch on in Athens."),
    (182, 5): ("A woman reports the princess's engagement.", "The princess got engaged!"),
    (182, 8): ("Her friend says the groom is a duke's son.", "Yes! To a duke's son, correct?"),
    (182, 11): ("The first woman describes the engagement ring's cost.", "Her ring could buy a mountain!"),
    (182, 14): ("Her friend asks when the princess will wear the jewel publicly.", "Such wealth! When can we see that jewel on her?"),
    (182, 17): ("The first woman predicts other ladies will covet that jewel.", "Soon enough. Then every lady will want a jewel like hers."),
    (182, 21): ("Her friend wants to know the gem before it becomes fashionable.", "We must buy it before the craze! What gem is it?"),
    (182, 25): ("The first woman proposes asking about the gem at once.", "No idea. Let's go ask right away!"),
    (182, 62): ("The market notice predicts a London gem boom.", "Gems may catch on in London."),
}
SPEAKERS = {0xA6: "Townswoman", 0xA7: "Townswoman", 0xA8: "Townswoman", 0xFE: "Market notice"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {
        row_id for row_id in source_rows
        if row_id.startswith(("DK4_MES_B180_", "DK4_MES_B181_", "DK4_MES_B182_"))
    }
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B180-B182 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Linked Lisbon spice, Athens ruby, and London gem market-rumor scenes.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B180-B182 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v80-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 29 B180-B182 Lisbon spice, Athens ruby, and London gem rumor records.",
        "inventory": {"identified_records": 29, "translated_records": 29, "blocks": {"180": 11, "181": 10, "182": 8}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
