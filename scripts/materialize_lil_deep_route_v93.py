from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v93.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Samwell asks who the man in the portrait is.", "Who's that old man in the portrait?"),
    9: ("Kamil identifies Rocco Alemkel.", "That's Rocco Alemkel."),
    12: ("Samwell asks whether he is famous.", "Huh. Was he famous?"),
    16: ("Kamil says navigators know him well.", "Among navigators, he sure is."),
    19: ("Lil asks why they whisper by the portrait and threatens to go ahead.",
         "Why whisper by that portrait? Hurry up, or you're getting left behind!"),
    23: ("Kamil apologizes and says he is coming.", "Sorry! Coming!"),
    27: ("Samwell says he is coming and teases Lil as fat.", "Right behind you, fatty!"),
    31: ("Lil threatens to hit Samwell.", "Samwell! You're dead!"),
    34: ("The scene depicts repeated crashes as Lil throws objects.", "Bang! Crash! Thud! Clunk!"),
    37: ("Kamil calls the admiral by name and begs her to stop throwing things.",
         "{MACRO:FI}! Stop throwing things! Ow!"),
    40: ("Samwell taunts Lil for missing him.", "Wrong way! Over here!"),
    43: ("Lil shouts after Samwell.", "Wait right there!"),
    47: ("Kamil sighs that he always has to clean up.", "Sigh... Always left to clean up."),
    50: ("Kamil notices something amid the mess.", "Hm? What's this?"),
    54: ("Kamil recognizes an old book.", "An old book..."),
    58: ("Lil calls Kamil to come with her.", "Kamil! Come on, let's go!"),
    62: ("Kamil asks where Samwell went.", "Where's Samwell?"),
    66: ("Lil says she does not care about Samwell.", "Who cares about him?"),
    70: ("Kamil privately notes Samwell escaped because he is quick.",
         "(Got away again. Samwell's quick on his feet.)"),
    73: ("Lil challenges Kamil's private amusement.", "What?!"),
    77: ("Kamil denies saying anything.", "N-nothing."),
    81: ("Lil tells him to stop grinning.", "Hmph! Stop grinning!"),
    84: ("Kamil apologizes and presents the book.", "S-sorry. Oh, here."),
    88: ("Lil asks if the book is a gift.", "What's this? A gift?"),
    91: ("Kamil tries to correct her.", "N-no, that's not..."),
    95: ("Lil says the book looks old and a gift from Kamil is rare.",
         "An old book... a gift from you? Wow!"),
    99: ("Kamil again tries to explain.", "Not that..."),
    103: ("Lil thanks Kamil.", "Thanks!"),
    107: ("Kamil gives in to the misunderstanding.", "Ah... yes."),
    111: ("Lil urges him to go.", "Go!"),
    115: ("Kamil privately wonders whether he should let her keep the book.", "(Was that okay?)"),
}
EXCLUDED = {
    "DK4_MES_B199_R0086": (
        "Four-byte 95 48 53 A8 packed item/scene event between Kamil's book "
        "handoff and Lil's gift question; no Japanese text; leave unchanged."
    ),
}
SPEAKERS = {0x16: "Samwell", 0x09: "Kamil", 0x02: "Lil", 0xFE: "Scene effects"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B199_")}
    authored = {f"DK4_MES_B199_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B199 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B199_R0086"]["source_hex"].upper() != "954853A8":
        raise ValueError("B199 packed event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B199_R{number:04d}"
        raw = bytes.fromhex(source_rows[row_id]["source_hex"])
        lead = raw[0]
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        if "I" in english.replace("{MACRO:FI}", "") or "F" in english.replace("{MACRO:FI}", ""):
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        if raw.count(b"FI") != english.count("{MACRO:FI}"):
            raise ValueError(f"{row_id}: name macro count changed")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Samwell, Kamil, and Lil find Rocco Alemkel's portrait and an old book.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B199 Japanese. Preserve 16/09/02/FE "
                "states and the FI admiral-name macro; packed event stays unchanged. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v91-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "31 B199 portrait, book, and gift text records; one packed event excluded unchanged.",
        "inventory": {"identified_records": 32, "translated_records": 31, "blocks": {"199": 31}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} exclusion")


if __name__ == "__main__":
    main()
