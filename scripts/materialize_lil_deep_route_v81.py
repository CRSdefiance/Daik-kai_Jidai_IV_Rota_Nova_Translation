from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v81.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("A visitor gives a brief interjection.", "Hm!"),
    10: ("An art collector praises an artist's work.", "Truly marvelous!"),
    14: ("Another collector is unconvinced.", "Really?"),
    18: ("The first collector predicts the artist will be famous.", "He'll be a famous artist one day."),
    21: ("The other collector gives an uncertain acknowledgment.", "Oh."),
    25: ("The first collector urges buying the artist's work early.", "Buy his work now, while you can."),
    28: ("The other collector prefers a different painting.", "This one's better, if you ask me!"),
    32: ("The first collector says his favorite artist is still better.", "Not bad, but his work is better."),
    35: ("A third collector insists another piece is best.", "You're all wrong. That one is best!"),
    39: ("The first collector buys his preferred painting.", "Well, his painting is mine!"),
    42: ("The second collector buys a different artist's painting.", "Then this artist's painting is mine!"),
    45: ("The third collector claims a third painting.", "And this one's mine!"),
    49: ("The shopkeeper thanks the collectors.", "Thanks for your business!"),
    53: ("The shop door slams.", "Slam!"),
    57: ("The shopkeeper is relieved the arguing collectors have gone.", "Gone at last. They argue in my shop every time!"),
    61: ("A visitor asks the shopkeeper what happened.", "What was all that?"),
    65: ("The shopkeeper calls the argument a rich person's pastime.", "Rich folks at play."),
    69: ("The visitor asks about the rich person's pastime.", "The rich?"),
    73: ("The shopkeeper says collecting paintings is fashionable.", "Yes. Everyone's collecting art now."),
    76: ("The visitor calls collecting art a lofty hobby.", "A lofty hobby."),
    80: ("The shopkeeper says few collectors understand art.", "Most of them know nothing about art."),
    83: ("The visitor laughs at the shopkeeper's frankness.", "Ha ha! You said it!"),
    87: ("The shopkeeper asks the visitor to keep the remark private.", "Keep that between us, will you?"),
    91: ("The visitor agrees to keep the secret.", "Of course."),
    95: ("The market notice predicts a Basra painting boom.", "Paintings may boom in Basra."),
}
SPEAKERS = {
    0x99: "Visitor", 0x94: "Art collector", 0x6E: "Art collector",
    0x84: "Art collector", 0x55: "Shopkeeper", 0xFE: "Scene cue or market notice",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B183_")}
    authored = {f"DK4_MES_B183_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B183 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    if source_rows["DK4_MES_B183_R0006"]["source_hex"] != "9982F18148":
        raise ValueError("B183 short visitor interjection changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B183_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Collectors argue over paintings in a Basra shop; a visitor asks the shopkeeper about the craze.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B183 Japanese. Source presentation "
                "leads are preserved. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v81-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 25 B183 Basra painting-craze text and cue records.",
        "inventory": {"identified_records": 25, "translated_records": 25, "blocks": {"183": 25}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
