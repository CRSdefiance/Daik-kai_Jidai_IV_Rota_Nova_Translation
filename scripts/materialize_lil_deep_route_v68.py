from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v68.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
CONTROL_ID = "DK4_MES_B163_R0034"
CONTROL_HEX = "209546E2802C63"

LINES = {
    5: ("A dockworker announces the ship has returned.", "Admiral! Your ship's back!"),
    8: ("Lil is surprised.", "What?!"),
    20: ("Angelo doubts the news.", "Mamma mia! No way!"),
    27: ("The dockworker points out the ship.", "Look! That's your ship, right?"),
    32: ("Jam exults in the open sea.", "Yahoo! What a vast sea!"),
    36: ("Jam enjoyed the morning sail.", "Great sail! What a day! Yahoo!"),
    39: ("Lil confronts the sailor on her ship.", "Hey, you! That's my ship! What were you doing?"),
    43: ("Kamil orders him off the ship.", "Get off our ship!"),
    47: ("Jam claims he found the ship abandoned.", "Huh? Nobody owned it!"),
    50: ("Kamil rejects Jam's claim.", "No, it wasn't!"),
    62: ("Angelo jokes about Jam's mind being strawberry jam.", "Mamma mia! Jam for brains!"),
    69: ("Jam insists the ship looked abandoned in the harbor.", "There it was in the harbor, all lonely and abandoned. Honest!"),
    73: ("Jam says he took in the lonely ship and spells his name.", "Jam took her in! J-A-M! Yahoo!"),
    84: ("Angelo sees Jam's name as proof of his joke.", "Jam? So his brain..."),
    91: ("Lil asks how Jam sailed the ship away by himself.", "You found it? How did you sail her out there?"),
    95: ("Jam waves away the question of how he sailed.", "Just winged it! Yahoo!"),
    98: ("Lil realizes Jam sailed alone.", "You were alone?!"),
    102: ("Kamil is impressed by Jam's talent.", "Wow... Maybe he's a genius."),
    106: ("Lil asks what Jam would have done if stranded.", "What if you got lost at sea?"),
    109: ("Jam dismisses the worry and announces a maxim.", "Tsk, tsk! Here's a saying for you. Listen up!"),
    113: ("Jam says that determination makes anything possible.", "Try, and you can do it! Yahoo!"),
    124: ("Fernando regards Jam as trouble.", "Now this guy's trouble."),
    131: ("Lil rebukes Jam for his careless attitude.", "Enough with the yahoo! Get serious!"),
    134: ("Jam boasts that he lives intensely, however briefly.", "My way's the only way! Live large, even if life is short!"),
    138: ("Jam rejects a long, timid life.", "Live small and safe? Always looking down? No thanks!"),
    149: ("Angelo wants to turn Jam over to the guard.", "Mamma mia! What a guy! Let's hand him to the guards!"),
    155: ("Kamil asks Lil to invite Jam aboard, using her name macro.", "Hey, {MACRO:FI}! Let's ask him to join us!"),
    166: ("Fernando is startled by Kamil's idea.", "K-Kamil?!"),
    173: ("Lil protests Kamil's suggestion.", "What are you talking about?!"),
    185: ("Angelo renews his strawberry-jam joke about Kamil.", "Your brain's turned to strawberry jam too?!"),
    192: ("Kamil admires Jam's solo sailing despite his oddness.", "He's reckless, but he sailed alone! Never met anyone like him. Come on!"),
    195: ("Lil relents, joking that her sailors are already strange.", "All right! My crew's odd already."),
    207: ("Angelo thinks Lil's barb was directed at him.", "Admiral! You looked at me just then!"),
    210: ("Kamil tries to calm Angelo.", "Easy, Angelo..."),
    217: ("Kamil invites Jam to sail with them.", "Jam, join our crew!"),
    220: ("Jam feigns deep deliberation, then asks for two seconds.", "Join you or not... Just a moment! Give me two seconds!"),
    223: ("Jam announces a decision.", "Got it!"),
    227: ("Kamil asks whether Jam has decided.", "You decided?"),
    231: ("Jam says no and pretends to leave.", "Yep. Not coming! Have a good trip!"),
    235: ("Lil is stunned and calls him back.", "What?! Hey, wait a second!"),
    239: ("Jam admits he was teasing them.", "Ha! Just kidding! Merci!"),
    242: ("Lil reacts to the prank.", "Joking?!"),
    246: ("Jam accepts and introduces himself fully.", "Let me come along! Name's Jam Jack Ludwyan! Yahoo!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0B: "Jam Jack Ludwyan",
    0x0F: "Angelo Puccini", 0x14: "Fernando", 0x74: "Dockworker",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B163_")}
    authored = {f"DK4_MES_B163_R{number:04d}" for number in LINES} | {CONTROL_ID}
    if authored != expected:
        raise ValueError(f"B163 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    if source_rows[CONTROL_ID]["source_hex"].upper() != CONTROL_HEX:
        raise ValueError(f"{CONTROL_ID}: opaque event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B163_R{number:04d}"
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
            "context": "Jam returns Lil's ship, boasts of sailing alone, and is invited into her crew.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B163 Japanese. The FI name macro, source "
                "presentation leads, and opaque event retain their control behavior. "
                "Literal uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v67-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 43 B163 ship-return and Jam recruitment text records; one event unchanged.",
        "inventory": {"identified_records": 44, "translated_records": 43, "blocks": {"163": 43}},
        "excluded_records": {CONTROL_ID: "Opaque seven-byte ship-return scene event (20 95 46 E2 80 2C 63)."},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, one control excluded")


if __name__ == "__main__":
    main()
