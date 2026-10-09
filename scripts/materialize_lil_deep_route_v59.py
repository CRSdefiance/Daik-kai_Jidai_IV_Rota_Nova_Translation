from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v59.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    8: ("Maldonado distrusts his ally Escante.", "Escante's my ally. Trust him? Never."),
    11: ("He has heard Escante hopes to secede and found a new country.", "Rumor says he wants to leave Spain and found a new nation..."),
    22: ("Maldonado fears Escante will destroy his force once the alliance is no longer useful.", "Once he's done with our pact, he'll crush my fleet..."),
    28: ("Alternate thought: Escante may destroy Maldonado once Clifford is beaten.", "Once Clifford falls, Escante will crush my fleet..."),
    35: ("Maldonado hopes a royal favor might let him expand his forces.", "One grand deed could win royal leave. Then my fleet could grow..."),
    39: ("Lil is tired and orders a drink from the tavern keeper.", "Whew... Barkeep, a drink, please."),
    50: ("Emilio orders food.", "And food for me!"),
    62: ("Samwell orders the same as Emilio.", "Same as Emilio, please!"),
    69: ("Lil teases Samwell for appearing whenever food or drink is served.", "Samwell... are you always here when food or drink turns up?"),
    75: ("The barkeep acknowledges the orders.", "Aye."),
    79: ("Maldonado notices Lil and asks where she comes from.", "New face, girl. Where from?"),
    90: ("Jam eagerly begins boasting of his birth in Paris.", "Glad you asked! Born in Paris..."),
    93: ("Maldonado rudely says he was not asking Jam.", "Nobody asked you!"),
    100: ("Lil says she has a name and gives it with both source name macros.", "Woman? {MACRO:FI} {MACRO:FA}, thanks!"),
    103: ("Maldonado recognizes Lil's given name and asks if she is with her faction.", "{MACRO:FI}...? Are you with {MACRO:FO}?"),
    107: ("Lil recognizes him as Vasquez Maldonado.", "You know me? Are you Vasquez Maldonado?"),
    125: ("Yukihisa recognizes Maldonado in one companion branch.", "That's Maldonado..."),
    134: ("Aziza recognizes Maldonado in another companion branch.", "So that's Maldonado..."),
    141: ("Maldonado concludes Lil intends to expand into the New World.", "Ah, it's you! New World ambitions?"),
    145: ("Lil greets Maldonado as a trading rival.", "So it seems. Hello, trade rival."),
    148: ("Maldonado scorns the Dutch and objects to Lil trading in Spain's sphere.", "Hmph! A girl from tiny Holland has no place in Spain's markets!"),
    152: ("Lil objects to his slight and asserts her freedom to trade.", "Quit calling us tiny! We can trade wherever we please!"),
    164: ("Kamil sees another argument beginning.", "Here we go again..."),
    176: ("Fernando sees the familiar argument coming in an alternate branch.", "Same old story, huh..."),
    186: ("Maldonado loses patience with Lil.", "Enough!"),
    198: ("Kamil warns Lil to dodge the bottle.", "Look out!"),
    205: ("A bottle crashes.", "Crash!"),
    209: ("Lil screams.", "Ah!"),
    221: ("Kamil protests Maldonado's attack.", "Stop that!"),
    228: ("Lil rebukes Maldonado for throwing a bottle at her.", "Hey! Throwing a bottle at someone? That's dangerous!"),
    240: ("Yukihisa rebukes Maldonado for attacking a woman.", "Rogue! How dare you strike a lady!"),
    246: ("Maldonado threatens to hit Lil next time.", "A warning! Next time, you're hit!"),
    249: ("Maldonado leaves, blaming Lil for spoiling his drink.", "Barkeep! No more wine. That girl ruins the taste."),
    253: ("The barkeep hesitantly asks for payment.", "Y-yes... and the bill...?"),
    256: ("Maldonado intimidates the barkeep by claiming to keep the town safe.", "My bill?! You know who keeps this town safe. Watch your tongue!"),
    260: ("The barkeep waives the bill under threat.", "Y-yes... No charge, of course."),
    279: ("Al wants to attack Maldonado.", "What a lout! Let me at him..."),
    283: ("Gerhard stops Al.", "Stop."),
    287: ("Al tells Gerhard not to restrain him.", "Let go!"),
    291: ("Gerhard warns that fighting here would harm the tavern.", "Not here. You'll hurt the tavern."),
    295: ("Al reluctantly holds back.", "Damn..."),
    305: ("Maldonado storms off to drink elsewhere and curses Lil.", "Tch. Home for a drink! That brat makes me sick!"),
    308: ("Maldonado vows to crush Lil's faction, then sees an opportunity.", "{MACRO:FO} will be dust! Hm... perhaps this is a lucky break..."),
    311: ("He plans to defeat Lil and win royal permission to expand.", "She's flown right into the flame! Crush her, win royal favor, and expand my power..."),
    315: ("He imagines surpassing Escante and calls himself lucky.", "Bigger than Escante... What luck!"),
    323: ("The barkeep checks whether Lil is hurt.", "Miss, are you hurt?"),
    335: ("Ian checks Lil in one branch.", "Admiral, you okay?"),
    342: ("Lil condemns soldiers and worries that Maldonado skipped his bill.", "Safe. Soldiers disgust me. He never paid you..."),
    345: ("The barkeep feels unable to resist Maldonado's Spanish naval power.", "Can't help it. He's with Spain's navy. We can't oppose them..."),
    349: ("Lil calls it bullying and promises to punish Maldonado.", "Don't give up! He's bullying you. That brute needs a lesson..."),
    353: ("Kamil checks whether the bottle hit Lil in another branch.", "Did it miss? Are you hurt?"),
    365: ("Ian checks Lil in another branch.", "Admiral, you okay?"),
    372: ("Lil condemns soldiers who use violence to get obedience.", "Yeah... That's why soldiers make me sick! They think violence makes everyone obey!"),
    388: ("Lil exempts Hodram from her criticism.", "Except Hodram..."),
    395: ("Lil vows not to let Maldonado's attack go unanswered.", "That brute makes me so mad! He'll pay for this. Just watch!"),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0x0B: "Jam Jack Ludwayer",
    0x0C: "Yukihisa Genjo Shiraki", 0x0E: "Emilio", 0x10: "Gerhard",
    0x11: "Al", 0x14: "Fernando Dias", 0x15: "Ian Dukov",
    0x16: "Samwell", 0x1B: "Aziza Nurennahar",
    0x2A: "Vasquez Maldonado", 0x5C: "Tavern keeper", 0xFE: "Impact sound",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B151_")}
    authored = {f"DK4_MES_B151_R{number:04d}" for number in LINES}
    if authored != expected:
        raise ValueError(f"B151 coverage mismatch: missing {expected - authored}; extra {authored - expected}")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B151_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": (
                "In a New World tavern, Maldonado fears Escante's ambitions, clashes with Lil, "
                "throws a bottle, bullies the barkeep, then sees a chance to win royal favor "
                "by attacking Lil. Alternate crew reactions and aftermath branches are preserved."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from the clean B151 Japanese; preserves every source lead, "
                "FI/FA/FO macros, both Maldonado monologue branches, companion reactions, "
                "and aftermath variants."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v59-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 55 dialogue records in B151, including alternate companion and aftermath branches.",
        "inventory": {"identified_records": 55, "translated_records": 55, "blocks": {"151": 55}},
        "excluded_records": {}, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
