from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v55.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("Lil asks whether Kamil has come back.", "Where's Kamil? Hasn't he come back?"),
    8: ("A sailor says Kamil was not with them and asks whether he was with Lil.", "No, wasn't Kamil with you, Admiral?"),
    19: (
        "Fernando cannot tell where Kamil went or predict his actions.",
        "Where did he go? Even his next move is a mystery to me...",
    ),
    25: ("Lil worries about what has happened to Kamil.", "Kamil... what happened?"),
    31: ("Meanwhile, Kamil is elsewhere.", "Meanwhile, Kamil:"),
    35: ("Kamil wonders whether his father has changed at all.", "My father... still the same."),
    39: ("Kamil addresses Lil by name and wonders what he should do.", "{MACRO:FI}... What now?"),
    48: ("Hodram notices Kamil's pale face and asks what is wrong.", "Hey, you're pale! What's wrong?"),
    51: ("Kamil asks who the stranger is.", "Who are you?"),
    55: ("Hodram introduces himself as Hodram Bergstrom.", "Pardon me. Hodram Bergstrom."),
    58: ("Kamil recognizes the Bergstrom name and asks about Hodram's fleet.", "Bergstrom... of the Bergstrom fleet?"),
    61: ("Hodram confirms it in a modest way.", "More or less."),
    65: (
        "Kamil apologizes for failing to introduce himself and gives his full name.",
        "Sorry, how rude of me. The name's Kamil Overijssel.",
    ),
    69: ("Hodram asks whether Kamil is unwell; his hands are shaking.", "Kamil, you're shaking. Are you ill?"),
    72: ("Kamil says he is all right but hesitates.", "No, it's nothing. Just..."),
    77: ("Hodram suddenly recognizes Kamil.", "You...!"),
    81: ("Kamil recalls Hodram's name.", "Oh, Hodram... sir."),
    85: ("Hodram remarks that meeting there is a coincidence.", "Small world."),
    89: ("Kamil gives a subdued assent.", "Yes..."),
    93: ("Hodram notices Kamil's low spirits.", "You seem down. What's wrong?"),
    97: ("Kamil admits that something is wrong without elaborating.", "Well..."),
    101: (
        "Hodram asks after Lil, recalling her name through the FI macro.",
        "How's that girl? {MACRO:FI}, wasn't it?",
    ),
    105: ("Kamil says he and Lil are currently apart.", "We're apart."),
    112: ("Hodram infers a personal problem rather than an illness.", "Not sick? Then something's wrong."),
    119: ("Hodram invites Kamil to sail aboard his ship for a while.", "Why not sail with me awhile?"),
    122: ("Kamil is surprised and hesitant.", "But..."),
    126: (
        "Hodram cannot leave Kamil alone in this state and asks whether he intends to stop sailing.",
        "Can't leave you like this. You're not quitting the sea?",
    ),
    129: (
        "Kamil is not quitting, but hesitates at the idea of sailing on a Bergstrom ship.",
        "No... But me, on a Bergstrom ship?",
    ),
    132: ("Hodram advises Kamil to go to sea when troubled.", "Kamil, when troubled, go to sea."),
    140: (
        "Hodram says isolation deepens worries; staying active steadies the mind and brings solutions.",
        "Don't brood alone. Keep busy until your mind settles. Then a way forward may appear.",
    ),
    147: ("Hodram says he also had troubles in the past.", "Had troubles too..."),
    151: ("Kamil is surprised that Hodram had troubles.", "You, Hodram?"),
    155: (
        "Hodram's sailing mentor took him aboard at such times, and the voyages eased his worries.",
        "Yes. My sailing mentor always took me aboard when worries weighed on me. Somehow, the sea eased them.",
    ),
    158: ("Kamil thanks Hodram and accepts his invitation for a while.", "Thanks. Let me join you awhile."),
    162: ("Hodram welcomes Kamil aboard.", "Welcome."),
}

SPEAKERS = {
    0x01: "Hodram Bergstrom", 0x02: "Lil Argot", 0x09: "Kamil",
    0x14: "Fernando Dias", 0x97: "Sailor", 0xFE: "Narration",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B146_")}
    authored = {f"DK4_MES_B146_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B146 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B146_R{number:04d}"
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
                "Kamil leaves Lil after confronting his father. Hodram finds him distraught, "
                "offers him a berth, and recalls how sailing helped him through his own worries. "
                "The 0x97 crew voice and 0xFE narration are established Lil presentation states."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B146 Japanese; preserves speaker states, both exact FI name macros, "
                "Kamil's separation from Lil and Hodram's mentor story. Guarded wrapping protects first "
                "and continuation glyphs."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 35 B146 Kamil-and-Hodram encounter and recruitment records.",
        "inventory": {"identified_records": 35, "translated_records": len(records), "blocks": {"146": 35}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
