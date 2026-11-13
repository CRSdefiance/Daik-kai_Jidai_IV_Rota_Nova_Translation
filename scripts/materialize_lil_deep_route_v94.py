from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v94.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A traveler collapses.", "Thud!"),
    9: ("Carlo sees the collapse.", "Ah!"),
    13: ("The traveler groans faintly.", "...Ugh..."),
    17: ("Carlo asks what happened and whether the traveler is well.", "Hey! Are you all right?"),
    21: ("The traveler groans again.", "Ugh..."),
    25: ("Carlo sees that the traveler has regained consciousness.", "You're awake."),
    29: ("The traveler asks where they are.", "Where is this place?"),
    33: ("Carlo says he brought the traveler from the harbor to an inn.",
         "At an inn. You fell at the docks. Brought you here."),
    37: ("The traveler apologizes for the trouble.", "Oh. Sorry for the trouble."),
    40: ("Carlo dismisses the trouble but urges the pale traveler to rest.",
         "No trouble. Still, you look pale. Rest here for a while."),
    44: ("Carlo leaves and wishes the traveler well.", "Well then, time to go. Take care."),
    47: ("The traveler stops Carlo and asks if he is a doctor.", "Wait, are you a doctor?"),
    50: ("Carlo says he is not a doctor.", "No, sorry."),
    54: ("The traveler offers Carlo an item as thanks.",
         "Please take this. Not much, but you helped me."),
    58: ("Carlo declines the reward.", "No, really. No need."),
    62: ("The traveler insists that Carlo accept the gift.", "Please take it. Let me thank you."),
    65: ("Carlo accepts and tells the traveler to care for their health.",
         "All right. Take care."),
    69: ("The traveler agrees and thanks Carlo warmly.", "Yes. Thank you so much."),
    72: ("The system raises Carlo's charm by one.", "Carlo's charm rose by 1!"),
}
SPEAKERS = {0xFE: "Scene effect or system notice", 0x13: "Carlo Sinato", 0xAC: "Traveler"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B200_")}
    authored = {f"DK4_MES_B200_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B200 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B200_R{number:04d}"
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
            "context": "Carlo helps a traveler who collapsed at the docks and receives thanks.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B200 Japanese and correlated cross-route event. "
                "Preserve FE/13/AC states; literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v94-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 19 B200 Carlo, collapsed traveler, gift, and charm records.",
        "inventory": {"identified_records": 19, "translated_records": 19, "blocks": {"200": 19}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
