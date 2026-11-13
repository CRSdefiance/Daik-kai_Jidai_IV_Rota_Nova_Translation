from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v67.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    (160, 5): ("A messenger reports Lil's ship missing.", "Admiral! The ship is gone!"),
    (160, 8): ("Lil wonders whether the messenger mistook another ship for hers.", "Gone? Did you check the wrong ship?"),
    (160, 11): ("Kamil thinks the news is a cruel morning joke.", "Bad joke this early."),
    (160, 23): ("Angelo protests that lost sleep harms his skin.", "Quit joking! My skin needs sleep!"),
    (160, 29): ("The messenger insists and summons them to the harbor.", "No joke! Come to the harbor now!"),
    (160, 32): ("Lil sees that the ship has vanished.", "Gone! The ship really vanished!"),
    (160, 43): ("Lil jokes that Emilio might have eaten the ship.", "Did Emilio eat it?"),
    (160, 46): ("Emilio protests that he would not eat something unappetizing.", "Honest, not me! Ships taste awful."),
    (160, 50): ("Lil retracts the joke and demands an explanation.", "Kidding! But this is serious. What happened?"),
    (160, 61): ("The messenger panics.", "What do we do?!"),
    (160, 73): ("Angelo is jolted fully awake.", "Mamma mia! Wide awake now!"),
    (160, 79): ("Kamil asks what happened.", "What's going on?"),
    (160, 83): ("A dockworker calls to Lil.", "Admiral! Wait!"),
    (160, 87): ("The dockworker saw a lanky man handling the ship in the morning.", "A thin man was working on your ship this morning..."),
    (160, 91): ("The dockworker says the man sailed away.", "Then he sailed off!"),
    (160, 103): ("Angelo asks why the dockworker did not stop the man.", "Why didn't you stop him?"),
    (160, 110): ("Kamil asks Lil what to do, using her name macro.", "What do we do, {MACRO:FI}?"),
    (160, 113): ("The dockworker mistook the lone man for someone inspecting the ship.", "He was alone. Looked like a ship check. Then he sailed."),
    (160, 117): ("Lil agrees that one man sailing away was hard to predict.", "True. Who'd expect that?"),
    (160, 121): ("Kamil suggests searching town for the ship thief.", "Ask around town for the thief."),
    (160, 132): ("Angelo laments their bad luck.", "Mamma mia! What rotten luck!"),
    (161, 6): ("The dockworker says the stolen ship has not returned.", "Still hasn't come back."),
    (162, 6): ("The dockworker repeats that the stolen ship has not returned.", "Still hasn't come back."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio",
    0x0F: "Angelo Puccini", 0x74: "Dockworker", 0x97: "Crew messenger",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {
        row_id for row_id in source_rows
        if row_id.startswith(("DK4_MES_B160_", "DK4_MES_B161_", "DK4_MES_B162_"))
    }
    authored = {f"DK4_MES_B{block}_R{number:04d}" for block, number in LINES}
    if authored != expected:
        raise ValueError(f"B160-B162 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
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
                "Lil's ship vanishes from the harbor; a dockworker describes the man "
                "who sailed it away and later reports it still has not returned."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B160-B162 Japanese. The FI name macro "
                "and source speaker leads retain their control behavior. Literal "
                "uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v67-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 23 B160-B162 stolen-ship and dockworker text records.",
        "inventory": {
            "identified_records": 23, "translated_records": 23,
            "blocks": {"160": 21, "161": 1, "162": 1},
        },
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
