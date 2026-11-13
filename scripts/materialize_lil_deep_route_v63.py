from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v63.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("The tavernkeeper asks Ian to carry something.", "Dukov, carry this."),
    10: ("Ian complies.", "Yes."),
    15: ("A woman admires Ian's beauty.", "Look. So beautiful..."),
    19: ("A man doubts Ian is male.", "Really a man?"),
    23: ("The woman warns that Ian will hear.", "Shh. He'll hear."),
    27: ("Ian resents being treated as a spectacle again.", "(Again... Enough. Not a showpiece.)"),
    30: ("The tavernkeeper asks Ian to bring more wine.", "Dukov, this wine too."),
    34: ("Ian reluctantly agrees.", "Yes."),
    38: ("The woman is delighted Ian served her.", "Oh! Dukov served me himself!"),
    41: ("The man is annoyed at her delight.", "Why so happy? Hmph. Not funny."),
    44: ("The tavernkeeper sends Ian to another table.", "Dukov, take this to that table."),
    47: ("Ian complies.", "Yes."),
    51: ("A drunken thug demands a drink from Ian with a feminine address.", "Hey, sweetheart. Pour me a drink."),
    58: ("The thug leers at Ian's looks.", "You're a real beauty, aren't you?"),
    65: ("The thug questions Ian's sex and comments on his pale skin.", "Really a man? Skin that pale can't be natural. Heh heh!"),
    69: ("Ian tells the thug not to touch him.", "Stop!"),
    73: ("The thug cries out in pain.", "Ow! That hurts!"),
    77: ("The thug curses Ian.", "You bastard!"),
    81: ("Ian realizes he has made a mistake.", "(Damn!)"),
    85: ("The thug sarcastically calls Ian's treatment of a customer fine hospitality.", "So this is how you treat a customer?"),
    89: ("Ian apologizes formally.", "My apologies."),
    93: ("Lil orders a drink from the tavernkeeper.", "A drink, please."),
    105: ("Fernando asks for plenty more drinks.", "Keep them coming!"),
    120: ("Emilio asks for food.", "And food for me!"),
    127: ("The tavernkeeper agrees, then calls Ian aside.", "Coming right up... Dukov, a word."),
    130: ("The tavernkeeper says this work may not suit Ian.", "This job may not suit you."),
    134: ("Ian addresses the tavernkeeper.", "Sir..."),
    138: ("The tavernkeeper says a worker should handle customers without a sword.", "Enough trouble. You can manage customers without drawing a sword."),
    142: ("The tavernkeeper dismisses Ian.", "You can go."),
    146: ("Ian accepts the dismissal.", "...Understood."),
    150: ("Lil notices Ian is not from the city.", "He's not from here, is he?"),
    153: ("Kamil does not know.", "No idea."),
    157: ("Lil wonders why melancholy Ian works at the tavern.", "Those sad eyes... What's his story? Why work here?"),
    160: ("Kamil tells Lil not to ask him.", "Don't ask me."),
    164: ("Lil teases Kamil for being jealous.", "Are you jealous?"),
    168: ("Kamil denies it.", "No way!"),
    172: ("Lil decides to speak with Ian.", "Heh. Let's talk to him."),
    176: ("Unemployed and penniless, Ian wonders what to do.", "(No job... no money. Now what?)"),
    179: ("Seeing a ship offshore, Ian longs to return to sea.", "(A ship... Wish to sail again.)"),
    183: ("The thug calls out to Ian in the street.", "Hey, sweetheart! Seeing you again!"),
    190: ("The thug taunts Ian for being alone and summons his men.", "Alone? Bad luck. Men, get him!"),
    198: ("The thug vows revenge for Ian embarrassing him.", "No escape! You'll pay for that!"),
    201: ("Outnumbered, Ian plans to strike the leader.", "(Too many... Can't beat them all. Aim for the leader!)"),
    206: ("The thug orders his men to hurry against a lone opponent.", "He's alone! Move, you fools!"),
    213: ("Ian is too exhausted to reach the leader alone.", "Hah... (Can't even reach him alone!)"),
    216: ("The thug orders his men to finish Ian.", "He's nearly done. End it!"),
    219: ("The thug is startled by an unexpected rescuer.", "Who are you?"),
    223: ("Lil refuses to abandon such a handsome man.", "A man that handsome? No way!"),
    227: ("The thug retreats and threatens to remember the defeat.", "Damn... Only battle when victory's sure. Remember that!"),
    232: ("Lil says Ian looks even better up close.", "You're even more handsome up close."),
    239: ("Kamil teases that Lil looks masculine next to Ian.", "Next to him, {MACRO:FI} looks like a man."),
    251: ("Fernando laughs and agrees with Kamil.", "Heh! No kidding."),
    258: ("Lil objects to the teasing.", "How rude!"),
    262: ("Ian says appearance does not matter.", "Looks don't matter."),
    265: ("Lil clarifies that she was complimenting Ian.", "Hey, that was a compliment!"),
    268: ("Ian apologizes for muttering and thanks them for saving his life.", "Talking to myself. Sorry. You saved my life. Thank you."),
    272: ("Lil asks Ian for a favor in return.", "Then will you do me a favor?"),
    276: ("Ian agrees if it is within his power.", "Whatever you need."),
    280: ("Lil reveals that they are sailors.", "We're sailors, actually."),
    284: ("Ian is surprised.", "What?"),
    288: ("Lil asks Ian to join their ship as a guard.", "We could use your skill as a guard. Will you sail with us?"),
    296: ("Kamil asks Ian for his answer.", "So... will you?"),
    300: ("Ian welcomes Lil's offer.", "Gladly. Thank you."),
    303: ("Lil playfully claims Ian accepted because of her charm.", "Glad to hear it! My charm, right?"),
    306: ("Kamil doubts Lil's claim given Ian's beauty.", "Come on, {MACRO:FI}. (Next to him? Really?)"),
    310: ("Ian says Lil is attractive but explains that he is an unemployed navigator.", "You're charming. Me? An unemployed navigator."),
    314: ("Ian says his ship sank and a berth would help him greatly.", "My ship sank. A berth would help."),
    318: ("Lil says both sides are lucky and asks Ian's name.", "Lucky us both! Your name?"),
    322: ("Ian Dukov introduces himself.", "Dukov. Glad to meet you."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0E: "Emilio", 0x14: "Fernando Dias",
    0x15: "Ian Dukov", 0x5C: "Tavernkeeper", 0x60: "Drunken thug",
    0xA4: "Male patron", 0xA5: "Female patron",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B156_")}
    authored = {f"DK4_MES_B156_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B156 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B156_R{number:04d}"
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
                "Ian Dukov is dismissed after a tavern confrontation, Lil's crew "
                "saves him from an ambush, and Lil recruits him as a navigator."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B156 Japanese. Source FI name macros and all "
                "presentation leads are preserved. Ian's given name cannot be printed "
                "literally in dialogue because uppercase I is a renderer macro byte, "
                "so his introduction uses Dukov."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v63-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 69 B156 Ian Dukov recruitment dialogue records.",
        "inventory": {"identified_records": 69, "translated_records": 69, "blocks": {"156": 69}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
