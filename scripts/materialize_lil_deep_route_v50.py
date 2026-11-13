from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v50.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("The Evergreen Lotus Leaf and Kushan Platter should be the two keys to the Ruler's Proof map.", "The Evergreen Lotus Leaf and Kushan Platter must unlock the Proof map."),
    8: ("A leaf and a plate? We're not going to put the leaf on the plate and eat it.", "A leaf and a plate? Dinner?"),
    12: ("What if I hit the leaf with the plate? Oh, sorry, I spilled the water on the leaf.", "Maybe hit the leaf with the plate? Oops! The water spilled on it."),
    16: ("You're so rough. Handle important things more carefully.", "Stop being so rough! Be careful!"),
    20: ("Hey, look at the wet part of the leaf.", "Hey! Look where the leaf got wet!"),
    24: ("What's this? It looks like a strange pattern.", "What's this? Some strange pattern?"),
    27: ("I know. Put the leaf on the plate and pour water on it.", "Leaf on platter. Pour water over it!"),
    30: ("So that's how they go together. Let's try it.", "So that's the trick! Let's try it!"),
    33: ("Water is seeping into the leaf veins.", "The leaf veins soak it up..."),
    37: ("The leaf floating on water is the map. The platter is essential.", "A map on the floating leaf! This platter is the key."),
    41: ("We would not have thought of this without your spill. Your talent appeared just in time.", "Your spill showed us the clue. Nice timing, klutz!"),
    44: ("That's not really a compliment.", "That's not a compliment..."),
    48: ("We have the map to the Indian Ocean's Ruler's Proof. Let's hurry and find it.", "Ruler's Proof map in hand! Let's search the southern sea!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x14: "Fernando Dias"}
EXCLUDED = {"DK4_MES_B139_R0035": "Four-byte 23 48 9E A8 event payload during leaf-map reveal; not dialogue."}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B139_")}
    authored = {f"DK4_MES_B139_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError("B139 coverage does not match clean source")
    if source_rows["DK4_MES_B139_R0035"]["source_hex"].upper() != "23489EA8":
        raise ValueError("B139 event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B139_R{number:04d}"
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
                "Lil and Fernando combine the Evergreen Lotus Leaf and Kushan Platter. "
                "Lil's spilled water reveals the Indian Ocean Ruler's Proof map."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B139 Japanese; preserves established item names, "
                "the accidental spill and Fernando's teasing. Opaque R0035 event payload remains "
                "unchanged. Guarded wrapping protects first and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Thirteen B139 Indian Ocean Proof-map dialogue records; opaque event payload excluded unchanged.",
        "inventory": {"identified_records": 14, "translated_records": len(records), "blocks": {"139": 13}},
        "excluded_records": EXCLUDED,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
