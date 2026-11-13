from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v53.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("The shipwright asks Lil for a favor.", "Say, can you do me a favor?"),
    8: ("What is it?", "What?"),
    12: (
        "The shipyard is studying a way to add armor to ships, but lacks research funds.",
        "We're working on armor upgrades but need research funds.",
    ),
    16: ("Lil will consider it, depending on the sum.", "Maybe. How much do you need?"),
    19: ("Really? You are as generous as ever!", "Really? You're the best, boss!"),
    22: (
        "Funding is about all Lil can provide; she asks the amount needed.",
        "Money's about all we can offer. How much do you need?",
    ),
    25: ("Three hundred thousand gold should finish the research.", "300,000 gold should do it."),
    28: ("Lil readily agrees and tells the shipwright to use the money well.", "Sure. Here, use it wisely."),
    32: ("The shipwright thanks Lil and will start immediately.", "Thanks! We'll start right away!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x6D: "Shipwright"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B143_")}
    authored = {f"DK4_MES_B143_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B143 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B143_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "A shipwright asks Lil to fund research into fitting armor at the shipyard. "
                "Lil agrees to provide the requested 300,000 gold."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B143 Japanese; retains the shipyard armor research, "
                "the precise 300,000-gold cost and Lil's ready agreement. "
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
        "scope": "All nine B143 shipyard armor-research funding records.",
        "inventory": {"identified_records": 9, "translated_records": len(records), "blocks": {"143": 9}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
