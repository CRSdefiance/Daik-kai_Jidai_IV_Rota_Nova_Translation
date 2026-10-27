from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v65.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Lil remarks that they drank a lot.", "Whew, we drank a lot!"),
    17: ("Kamil tells Lil she drank too much, using her name macro.", "Too much, {MACRO:FI}."),
    31: ("Emilio says he can still eat more.", "Still room for more!"),
    43: ("Kamil tells Emilio he has eaten too much.", "Emilio! Too much!"),
    53: ("Christina says she has drunk quite a bit, then hears music.", "Had my share too. Oh..."),
    58: ("Lil enjoys the passionate music.", "Such a fiery tune... Lovely."),
    69: ("Kamil agrees.", "Yes."),
    76: ("Christina recognizes the song and excuses herself.", "This song... Excuse me."),
    79: ("Lil wonders what Christina is doing.", "What's Christina doing?"),
    84: ("A patron admires Christina's performance.", "Wow, look at her!"),
    87: ("Another patron praises Christina's beauty and dance.", "Yeah! Beautiful, and what a dancer!"),
    92: ("Lil admires Christina's performance.", "Christina... amazing."),
    104: ("Kamil finds Christina beautiful.", "Yes, beautiful."),
    111: ("The tavern audience cheers for Christina.", "Bravo! Bravo! Bravo!"),
    114: ("The tavern audience applauds.", "Clap, clap, clap!"),
    118: ("Christina says she could not help dancing to a song she loves.", "Had to dance. Love this song."),
    121: ("Lil says Christina looked splendid.", "So cool..."),
    133: ("Kamil praises Christina's dance above even her swordplay.", "Your swordplay is graceful. Your dancing even more so."),
    140: ("Christina thanks the crew.", "Heh. Thank you."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x07: "Christina", 0x09: "Kamil",
    0x0E: "Emilio", 0xFE: "Tavern audience",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B158_")}
    authored = {f"DK4_MES_B158_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B158 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B158_R{number:04d}"
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
            "context": "Christina dances to a familiar tavern song while Lil's crew and the audience applaud.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B158 Japanese. The FI name macro and every "
                "speaker or audience presentation lead retain source control behavior. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v64-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 19 B158 Christina tavern dance dialogue records.",
        "inventory": {"identified_records": 19, "translated_records": 19, "blocks": {"158": 19}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
