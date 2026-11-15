from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v98.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Jam is bored and decides to go out.", "Bored. Time for a walk."),
    9: ("Jam asks an older woman for a nearby diversion.",
        "Ma'am, anything interesting nearby? Need a walk to kill time."),
    13: ("The woman points him toward the lord's castle in the east.",
         "The lord's castle is east of here."),
    16: ("Jam realizes she means a castle and decides to visit it.",
         "A castle? Sounds good. Let's see this country's castle."),
    19: ("Lil asks Jam where he has been.", "Jam! Where have you been?"),
    22: ("Jam apologizes and says his burden is heavy.", "Sorry. This thing's heavy."),
    25: ("Lil asks what he brought and where he got it.", "What is that? Where from?"),
    29: ("Jam calls it an authentic Japanese-made figurehead.",
         "A real figurehead! Made in Japan!"),
    33: ("Jam claims he taught the locals how to use a figurehead and received it as thanks.",
         "They had no idea what a figurehead is for. Showed them. They gave me this as thanks."),
    36: ("Lil hopes he did not steal it and tells him to prepare for departure.",
         "Well, if you didn't steal it... We're leaving soon. Get ready."),
    40: ("Jam agrees and asks for a moment.", "Got it. Just give me a minute."),
    45: ("A retainer frantically reports disaster to the lord.",
         "My lord! My lord! Disaster!"),
    48: ("The lord complains about the noise so early.", "Why so loud at dawn?"),
    52: ("The retainer says the shachihoko vanished and a foreign letter appeared.",
         "The shachihoko is gone! And this foreign letter..."),
    55: ("The lord orders the thief who took the shachihoko caught at any cost.",
         "The shachihoko is gone? Disaster! Catch that thief at any cost!"),
    58: ("The retainer obeys.", "At once!"),
    62: ("Jam's letter addresses the Japanese lord.", "Dear lord of Japan,"),
    66: ("The letter says the statue is a figurehead meant for ships, not castles.",
         "That statue is a figurehead. Put it on a ship, not a castle. Someone got the story mixed up."),
    69: ("Jam says he took a spare instead of payment and one figurehead belongs on each ship.",
         "No reward needed. Took one spare instead. One figurehead per ship, remember?"),
    72: ("Jam signs off using his full name.", "Take care, Jam Jack Ludwyan"),
}
SPEAKERS = {
    0x0B: "Jam Jack Ludwyan", 0x02: "Lil", 0x91: "Older woman",
    0x7C: "Retainer", 0x82: "Japanese lord", 0xFE: "Jam's letter",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B204_")}
    authored = {f"DK4_MES_B204_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B204 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B204_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english or "F" in english:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Jam mistakes a Japanese castle's shachihoko for a ship's figurehead.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B204 Japanese and parallel event context. "
                "Jam's full name follows the established Lil-route spelling. "
                "Preserve 0B/02/91/7C/82/FE states; literal uppercase I/F are unsafe."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v98-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 20 B204 Jam shachihoko, castle pursuit and letter records.",
        "inventory": {"identified_records": 20, "translated_records": 20, "blocks": {"204": 20}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
