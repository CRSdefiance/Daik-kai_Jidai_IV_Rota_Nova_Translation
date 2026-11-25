from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v71.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("Yifa bumps into Lil, who cries out.", "Ah!"),
    11: ("Yifa apologizes quickly because she is in a hurry.", "Sorry! Gotta run!"),
    15: ("Lil objects to the abrupt apology.", "Hey! You crash into me and that's all you say?"),
    19: ("Yifa says she already apologized and must hurry.", "Said sorry! Gotta run!"),
    22: ("Lil says Yifa's apology was not sincere.", "That wasn't a real apology."),
    26: ("Yifa calls Lil stubborn.", "Oh, you're so stubborn!"),
    30: ("Lil takes offense.", "What was that?!"),
    34: ("Yifa says she has no time for the argument.", "Look, there's no time to argue!"),
    37: ("Lil bristles and demands Yifa come over.", "Get over here! You've got nerve!"),
    41: ("Yifa yields and apologizes to Lil as an older woman.", "Okay, big sis, my fault. Sorry."),
    45: ("Lil softens when Yifa apologizes.", "Oh! Well, that's better."),
    49: ("Yifa flatters Lil, calling her kind.", "You really are nice, big sis."),
    53: ("Lil accepts the compliment.", "Well, people do say that!"),
    57: ("Yifa asks Lil to hear her serious problem.", "Hear me out. This is serious."),
    61: ("Lil offers help and boasts that she is an admiral.", "Sure! Tell me. An admiral can help."),
    64: ("Yifa is impressed that Lil is an admiral.", "Huh?"),
    68: ("Lil says she commands the named fleet.", "My fleet's called {MACRO:FO}."),
    71: ("Yifa admires Lil's command.", "Wow, big sis! That's amazing!"),
    74: ("Lil decides that the cheeky girl is rather sweet.", "Thought you were a brat, but you're pretty sweet."),
    78: ("Lil asks if Yifa's trouble is money.", "So what's wrong? Need money?"),
    82: ("Yifa says she fled her master to travel the world.", "Ran away from my master. Gonna see the world."),
    86: ("Lil asks why Yifa ran away.", "Wait, why run away from your master?"),
    90: ("Yifa says her master kept scolding her during Taoist training.", "My master kept scolding me during Taoist training. Had enough!"),
    94: ("Yifa refuses to quit before proving herself to her master.", "But quitting now would never prove him wrong!"),
    97: ("Yifa plans to train around the world and grow strong.", "Gonna travel the world, train hard, and get strong!"),
    100: ("Lil is confused by Taoist training.", "Taoist arts? What's that?"),
    104: ("Lil understands the wish to prove a master wrong.", "Still, wanting to prove your master wrong... that makes sense."),
    108: ("Yifa asks to sail with Lil.", "You get it! So can we sail together?"),
    111: ("Lil warns that life at sea is serious and asks Yifa's resolve.", "Sea life's no game. You ready?"),
    114: ("Yifa says she endured tough training already.", "Sure! Training's made me tough!"),
    118: ("Lil sees Yifa is resolved and asks her name.", "You mean it. What's your name?"),
    121: ("Yifa introduces herself and asks Lil's name.", "Yifa! And you, big sis?"),
    125: ("Lil introduces herself and urges Yifa to impress her master.", "Name's {MACRO:FI}. Yifa, show your master what you can do!"),
}

SPEAKERS = {0x02: "Lil Argot", 0x19: "Yifa"}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B170_")}
    authored = {f"DK4_MES_B170_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B170 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B170_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Yifa runs into Lil, describes leaving her Taoist master, and asks to sail with Lil's fleet.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B170 Japanese. The FI and FO name "
                "macros and source presentation leads retain their control "
                "behavior. Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v69-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 33 B170 Yifa recruitment text records.",
        "inventory": {"identified_records": 33, "translated_records": 33, "blocks": {"170": 33}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
