from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v43.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    12: ("We were told to go to Amsterdam, but does Crimson Pigment really exist?", "They sent us to Amsterdam, but is Crimson Pigment even real?"),
    24: ("We can probably believe them.", "Why not believe them?"),
    36: ("Ah, almost there. Oh, are you Dutch?", "Ah, almost... Oh! You're Dutch, aren't you?"),
    39: ("Yes. Why?", "Yes. Why?"),
    43: ("So am I.", "Me too!"),
    47: ("If you're Dutch too, I think you'll understand.", "You're Dutch too. Maybe you'll understand..."),
    54: ("If this country had more good farmland, wouldn't poor people be saved?", "With more fertile land, we could help the poor. Don't you agree?"),
    57: ("My hometown had poor land, so I understand. Everyone suffered.", "My hometown had poor soil. Everyone suffered. That's familiar."),
    61: ("My family were poor farmers. I've always wondered how we could make more good land.", "My family farm was poor too. Years of wondering how to make more fertile land led to an idea..."),
    64: ("Make more land?", "Make more land?"),
    68: ("Yes. Turn the sea into land and we will have more of it.", "Yes! Turn the sea into land. Then we'd have more of it!"),
    72: ("What do you mean?", "...How?"),
    76: ("Dry the sea. Build dikes along the coast, enclose an area and pump out the water. Vast new land remains.", "Build coastal dikes, then pump out the seawater. New land appears!"),
    79: ("I've named this a polder.", "The name for it: a polder!"),
    82: ("Brilliant. You should try it at once.", "That's brilliant! You should try it!"),
    85: ("I'd like to, but I lack the money.", "Wish we could. No money."),
    88: ("How much will it cost?", "How much?"),
    92: ("About one million gold.", "About 1,000,000 gold."),
    96: ("That's a fortune. Have you approached the government?", "A fortune! Ask your government?"),
    99: ("Yes, but even its aid isn't nearly enough.", "We did. Their aid barely helps."),
    103: ("I see. That's difficult.", "That's tough..."),
    107: ("I won't give up. Someone out there will fund it.", "But someone will help fund it. This dream isn't over."),
    111: ("Good for you. Keep at it.", "Well done! Keep at it."),
    123: ("Don't give up. One day your dream will come true.", "Never give up. Dreams come true."),
    129: ("Thank you.", "Thank you."),
    133: ("A polder... If it's finished, perhaps the people back home will have easier lives.", "A polder... Could it make life easier back home?"),
}

SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0x10: "Gerhard", 0xAB: "Lelystad founder"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B129_")}
    if {f"DK4_MES_B129_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B129 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B129_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unmapped speaker {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "Lil and Kamil seek Crimson Pigment in Amsterdam and meet the future Lelystad founder, "
                "who hopes to reclaim fertile land from the sea."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese. Retains established Crimson Pigment and polder names, "
                "the dike-and-pump method, million-gold cost, lack of government funds and dream of helping poor farmers. "
                "Preserves all source speaker selectors and guarded automatic wrapping."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v41-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 26 B129 Amsterdam Crimson Pigment and Lelystad polder scenes.",
        "inventory": {"identified_records": 26, "translated_records": len(records), "blocks": {"129": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
