from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v69.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("A townsman asks whether Lil's group came to see Mikhail.", "Here to see old Mikhail too?"),
    8: ("Lil asks who Mikhail is.", "Old Mikhail?"),
    20: ("Lil's grandfather urgently warns her away from Mikhail.", "M-Mikhail?! Stay away, {MACRO:FI}!"),
    26: ("The townsman says Mikhail is famous for his knowledge.", "No? He's a famous local scholar."),
    30: ("Lil wants to meet the intriguing scholar.", "Sounds interesting. Let's meet him."),
    33: ("Kamil agrees to go.", "Yeah, let's go."),
    37: ("The townsman advises against taking women to Mikhail.", "With women along, better not..."),
    48: ("Lil's grandfather emphatically agrees.", "Exactly! Stay away!"),
    58: ("Kamil points out the old scholar.", "That must be Mikhail."),
    62: ("A young woman praises Mikhail.", "Wow, Grandpa! Amazing!"),
    66: ("Mikhail preens at the praise.", "Quite so! Ho ho ho!"),
    69: ("Another girl asks him to identify something.", "Then what's this?"),
    73: ("Mikhail identifies a peppercorn and explains its use.", "A peppercorn. Grind this tropical fruit into spice."),
    77: ("Mikhail suggests cultivating pepper near Brunei as a trade good.", "Grow it near Brunei. The crop could make a fine trade good."),
    81: ("Mikhail realizes the object is rabbit droppings.", "Wait... Rabbit droppings! Yuck!"),
    85: ("The girl asks him to throw it away.", "Eww! Throw it away!"),
    89: ("Mikhail tosses it.", "There. Tossed!"),
    93: ("A young woman asks why Mikhail knows so much.", "You know so much, Grandpa! How?"),
    97: ("Mikhail calls himself a genius and makes an improper boast.", "A genius, that's why! Could even guess your bust size!"),
    101: ("The young woman calls Mikhail a dirty old man.", "Eek! You dirty old man!"),
    105: ("Mikhail laughs.", "Ho ho ho!"),
    109: ("Kamil admires his knowledge but finds him strange.", "Odd old man, but he does know a lot."),
    112: ("Lil agrees about his knowledge but is wary of his lechery.", "True... but he's too strange. And lecherous."),
    116: ("Kamil teases that Lil would be safe from Mikhail.", "You're safe, {MACRO:FI}."),
    119: ("Lil objects, then admits the crew needs a scholar.", "What's that mean?! Still, we could use his knowledge..."),
    123: ("Kamil admits the crew lacks scholars and suggests inviting him.", "We need a scholar. Let's ask him."),
    135: ("Fernando takes offense at being called ignorant.", "Does that include me?"),
    142: ("Mikhail asks who they are.", "Huh? Who are you?"),
    146: ("Kamil invites Mikhail to use his knowledge for their fleet.", "Bring your knowledge to {MACRO:FO}."),
    149: ("Kamil asks Mikhail to join them.", "Please join our crew!"),
    152: ("Mikhail does not want to leave town or follow a man.", "Join you? No! Won't leave town, or follow any man!"),
    156: ("Kamil again says they need his knowledge.", "Please! We need your knowledge."),
    159: ("Mikhail hesitates then spots Lil.", "Well, if you insist... Oh!"),
    162: ("Mikhail asks for Lil's name.", "Who's that young lady with you?"),
    165: ("Lil states her full name with two source name macros.", "{MACRO:FI} {MACRO:FA}. Why?"),
    168: ("Mikhail repeats Lil's given name.", "{MACRO:FI}, eh?"),
    172: ("Mikhail admires Lil in a lecherous tone.", "Lovely! Just lovely!"),
    180: ("Mikhail suddenly decides to join the crew.", "Decided! This old man goes with you!"),
    183: ("Mikhail calls to Lil.", "{MACRO:FI}, dear!"),
    187: ("Mikhail says he will follow Lil anywhere.", "Where you go, this man goes!"),
    191: ("Lil tells Mikhail to keep his distance.", "Hey! Stay away from me!"),
    194: ("Kamil tries to withdraw the invitation.", "M-Mikhail! No need to join. Bye!"),
    198: ("Mikhail insists his knowledge will help them.", "No! My mind's made up! My knowledge will help. You'll see!"),
    201: ("Kamil relents but starts warning Mikhail about Lil.", "All right, you can come. But leave {MACRO:FI}... Hey!"),
    204: ("Mikhail calls to Lil and touches her.", "{MACRO:FI}, dear! (touches her)"),
    207: ("Lil angrily rebukes Mikhail for touching her.", "Hands off, you old creep!"),
    210: ("Mikhail yelps after Lil strikes him.", "Oof!"),
    214: ("Kamil sighs at the commotion.", "Oh..."),
    222: ("The system says Mikhail is a scholar, not a deck officer.", "Mikhail is a scholar. He can't take a deck post."),
    226: ("The system says Mikhail unlocks detailed item information.", "Mikhail can now show detailed item information."),
    229: ("The system instructs the player to press X for item information.", "While viewing item details, press the X Button."),
    232: ("Mikhail offers item knowledge despite not working aboard ship.", "No shipwork. Ask me about items!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x06: "Lil's grandfather", 0x09: "Kamil",
    0x14: "Fernando", 0x4C: "Mikhail Lett", 0x57: "Townsman",
    0xA5: "Young woman", 0xA6: "Young woman", 0xFE: "System",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B168_")}
    authored = {f"DK4_MES_B168_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B168 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B168_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english
        for macro in ("FI", "FA", "FO"):
            literal = literal.replace(f"{{MACRO:{macro}}}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Lil's crew meets eccentric scholar Mikhail and recruits him for item knowledge.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B168 Japanese. Source FI, FA, and FO macros "
                "and presentation leads retain their control behavior. Literal "
                "uppercase I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v69-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 52 B168 Mikhail recruitment and item-information records.",
        "inventory": {"identified_records": 52, "translated_records": 52, "blocks": {"168": 52}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
