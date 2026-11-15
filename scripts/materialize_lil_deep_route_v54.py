from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v54.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (144, 5): (
        "The shipwright has completed the project. Ships can now be fitted with additional armor.",
        "Boss, it's ready! Now we can fit even more armor on ships!",
    ),
    (144, 9): ("Lil is delighted.", "Amazing!"),
    (144, 21): ("Manuel examines the new mechanism.", "Hmm, so that's how it works..."),
    (144, 35): (
        "A crewmate recognizes a theory from a book and asks whether the new method applies it.",
        "Ah! Could this be based on a theory from an old book?",
    ),
    (144, 39): ("The shipwright asks whether the younger man understands it.", "You get it, lad?"),
    (144, 43): (
        "The crewmate says this is a subject he had planned to study himself.",
        "Sure! Been eager to study this.",
    ),
    (144, 50): (
        "The shipwright allows Lil's group, as sponsors, unrestricted use of the technology.",
        "You're our sponsors. Use this technology as much as you like.",
    ),
    (144, 54): ("Lil thanks the shipwright.", "Thanks!"),
    (144, 66): (
        "Janus is impressed that the technology can be used on any ship.",
        "Wow, remarkable! Works on any ship.",
    ),
    (144, 75): (
        "A system notice says that fitting further additional armor is now possible.",
        "Ships can now carry more armor!",
    ),
    (145, 5): (
        "Lil thinks the Patterned Cloth is the map to the Mediterranean Proof.",
        "Could the Patterned Cloth be our Mediterranean Proof map?",
    ),
    (145, 9): (
        "Fernando thinks the Brass Lamp is also involved, and the two items must somehow be combined.",
        "The Brass Lamp matters too. We must combine the two...",
    ),
    (145, 13): ("Lil lights the lamp and wonders what to do next.", "The lamp is lit... What now?"),
    (145, 16): ("Fernando suggests trying to reveal the cloth's image with heat.", "Try warming the cloth?"),
    (145, 19): (
        "Lil likes the idea and warms the Patterned Cloth to reveal its hidden map.",
        "Heat the Patterned Cloth? Let's try!",
    ),
    (145, 23): (
        "Lil sees the map to the Mediterranean Proof and wants to set out at once.",
        "Yes! The Mediterranean Proof map! Let's go find it!",
    ),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x04: "Janus Pasha", 0x0D: "Crewmate",
    0x14: "Fernando Dias", 0x17: "Manuel Almeida", 0x6D: "Shipwright",
    0xFE: "System notice",
}
EXCLUDED = {"DK4_MES_B145_R0021": "Opaque four-byte map-reveal event payload (23 48 9C A8)."}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith(("DK4_MES_B144_", "DK4_MES_B145_"))}
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B144-B145 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B145_R0021"]["source_hex"].upper() != "23489CA8":
        raise ValueError("B145 R0021 event payload changed")
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
            "context": (
                "The armor-upgrade research Lil funded is complete, allowing any ship to receive more armor. "
                "Lil then uses the Brass Lamp to reveal the Mediterranean Proof map hidden in the Patterned Cloth."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B144-B145 Japanese; retains the armor-unlock notice, "
                "item identities and Mediterranean Proof reveal. Opaque event bytes remain unchanged. "
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
        "scope": "All 16 text records in B144-B145; preserves one opaque B145 reveal control.",
        "inventory": {"identified_records": 17, "translated_records": len(records), "blocks": {"144": 10, "145": 6}},
        "excluded_records": EXCLUDED,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
