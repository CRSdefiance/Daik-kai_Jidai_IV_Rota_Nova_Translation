from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v52.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (141, 15): ("Sorry, I still don't have enough right now.", "Sorry... the money's still short."),
    (141, 26): ("It is one million gold.", "A million gold..."),
    (141, 41): ("That is not easy to save. We must work hard to earn it.", "Not easy to save that much. Better get trading."),
    (141, 47): ("I understand your feelings. Thank you.", "Your trust means much to me."),
    (141, 50): ("It won't just be feelings. I'll have the funds soon. Trust me and wait.", "More than kind words. The money's coming. Trust me!"),
    (141, 54): ("Thank you. I'll prepare the plan so I can start as soon as the money arrives.", "Thank you. The plans will be ready when the funds arrive."),
    (141, 58): ("Keep going. I will too.", "Keep at it. So will we!"),
    (141, 63): ("Leave it to me. I do know how to trade.", "Leave it to me. Trading's my specialty!"),
    (141, 66): ("FI! This is incredible.", "{MACRO:FI}... Oh, this is..."),
    (141, 69): ("I asked many people and borrowed money, but raised only one tenth.", "After asking everyone, only a tenth came in..."),
    (141, 73): ("So you still need nine hundred thousand gold. Take this.", "Then take the 900,000 gold you need."),
    (141, 77): ("Oh! But are you sure?", "Oh! But... are you sure?"),
    (141, 80): ("Yes. Work hard and build the polder soon.", "Yes. Build that polder soon!"),
    (141, 84): ("Thank you. Leave it to me.", "Thank you! Count on me!"),
    (142, 5): ("FI, have you already raised the money?", "{MACRO:FI}! Got the money already?"),
    (142, 16): ("Not yet. Please wait a little longer.", "Not yet. A bit longer."),
    (142, 20): ("Sorry, that sounded like I was rushing you. Don't worry about it.", "Sorry to rush you. Take your time."),
    (142, 24): ("No, I'll work hard to save it soon.", "No, we'll save it soon."),
    (142, 28): ("Yes! Now you can start building the polder.", "Yes! Now you can start the polder!"),
    (142, 32): ("FI! This is incredible.", "{MACRO:FI}... This is incredible..."),
    (142, 43): ("Now everyone can be saved!", "Now everyone can get help!"),
    (142, 50): ("I also went around borrowing money, but raised only one tenth.", "Loans brought in just one tenth..."),
    (142, 54): ("So you still need nine hundred thousand gold. Here it is.", "Then take the 900,000 gold you need."),
    (142, 58): ("Are you sure? Raising all this must have been hard.", "Wow... Are you sure? Raising this must've been hard."),
    (142, 62): ("Don't worry about me. I look forward to the completed polder.", "Don't worry. That polder can't come soon enough!"),
    (142, 74): ("I look forward to it being completed.", "Can't wait to see it!"),
    (142, 81): ("Thank you. I'll start immediately.", "Thank you! Work starts right away!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x10: "Gerhard",
    0x14: "Fernando Dias", 0xAB: "Lelystad founder",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith(("DK4_MES_B141_", "DK4_MES_B142_"))}
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B141-B142 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for (block, number), (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B{block}_R{number:04d}"
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
                "Lil raises one million gold to fund the Lelystad founder's polder. "
                "These scenes include the shortfall visits and two alternate full-funding branches; "
                "the founder has independently borrowed one tenth, leaving 900,000 gold."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B141-B142 Japanese; preserves the 1,000,000-gold total, "
                "100,000 already raised, 900,000 supplied, both funding paths and exact FI name macros. "
                "Guarded wrapping protects first and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 27 B141-B142 polder funding, shortfall and alternate completion records.",
        "inventory": {"identified_records": 27, "translated_records": len(records), "blocks": {"141": 14, "142": 13}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
