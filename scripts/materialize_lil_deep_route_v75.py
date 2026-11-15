from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v75.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    6: ("Lil recognizes someone nearby.", "Huh? Seen her somewhere..."),
    10: ("Kamil takes a look.", "Let's see..."),
    14: ("Aziza recognizes Lil from their earlier encounter.", "Well, look who it is!"),
    18: ("Lil recognizes the woman pirate.", "You! The pirate from before!"),
    21: ("Aziza did not expect to meet Lil here.", "Never thought we'd meet here."),
    24: ("A pirate threatens Lil and Kamil for coming here alone.", "You two have nerve, coming here alone. Think you'll leave unhurt?"),
    28: ("Kamil realizes pirates have surrounded them and asks Lil what to do.", "Surrounded! {MACRO:FI}, what now?"),
    32: ("Lil condemns the pirates for using superior numbers.", "So this is your trick? Surrounding us with a gang? That's cowardly!"),
    36: ("A pirate calls Lil a brat.", "What was that, brat?!"),
    40: ("Kamil asks Lil why she is picking a fight while trapped.", "{MACRO:FI}, why pick a fight here?"),
    44: ("A pirate tells them to give up.", "Heh! Give up."),
    47: ("Aziza orders the crew to stop.", "Enough!"),
    51: ("A pirate asks Aziza if she is certain.", "You sure, boss?"),
    55: ("Aziza says her crew are proud pirates rather than thugs.", "Told you before! We're pirates, not thugs. Have some pride!"),
    59: ("Lil is impressed by Aziza's code of honor.", "(So that's her way...)"),
    63: ("Aziza says they will settle their fight at sea and warns Lil not to run.", "No plans to kill you here. Pirates settle things at sea. When that day comes, don't run!"),
    66: ("Lil vows she will not run away.", "Run? Never!"),
    69: ("Aziza likes Lil's courage and asks her name.", "Ha! You've got nerve. What name do you go by?"),
    73: ("Lil gives her full name.", "{MACRO:FI} {MACRO:FA}!"),
    77: ("Aziza teases Lil for being a cute admiral, then notices something.", "Such a cute little admiral... Hm?!"),
    81: ("Lil asks whether Aziza has another complaint.", "What now? Another complaint?"),
    84: ("Aziza covets Lil's sword and vows to take it someday.", "Nice sword, girl. Too good for you. One day it'll be mine."),
    88: ("Lil does not know what Aziza means.", "Huh?"),
    92: ("Aziza dismisses Lil's question and orders a retreat.", "Never mind. Men, fall back!"),
    95: ("The pirates answer Aziza's order.", "Aye!"),
    99: ("Kamil is relieved they escaped unharmed.", "Safe at last... That was close."),
    102: ("Lil says boldness is the way to handle pirates like that.", "Stand up to people like that!"),
    105: ("Kamil says Aziza seemed even scarier than Lil.", "She was terrifying! Even {MACRO:FI} seemed tame beside her."),
    109: ("Lil objects to Kamil's comment but admires Aziza's wish for a sea duel.", "Hey, watch it! But settling things at sea... That's pretty cool."),
    113: ("Kamil warns that Aziza will now chase them across the seas.", "Cool? She'll hound us forever now!"),
    117: ("Lil insists she can handle Aziza and will not lose.", "We'll manage! We can't lose!"),
    120: ("Kamil sighs at Lil's stubborn competitiveness.", "Always so stubborn..."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x09: "Kamil", 0xFE: "Aziza",
    0xB7: "Pirate crew", 0xB8: "Pirate", 0xB9: "Pirate",
}
EXCLUDED = {
    "DK4_MES_B175_R0012": (
        "Four-byte 96 46 CA 80 event payload between Kamil looking and "
        "Aziza's entrance; not dialogue. Preserved unchanged."
    ),
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B175_")}
    authored = {f"DK4_MES_B175_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B175 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}; extra {authored - expected}")
    if source_rows["DK4_MES_B175_R0012"]["source_hex"] != "9646CA80":
        raise ValueError("Opaque B175 event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B175_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        source_hex = source_rows[row_id]["source_hex"]
        for macro in ("FI", "FA"):
            if bytes.fromhex(source_hex).count(macro.encode()) != english.count(f"{{MACRO:{macro}}}"):
                raise ValueError(f"{row_id}: {macro} macro count mismatch")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{lead:02X}}}{english}{{PAD}}",
            "speaker": SPEAKERS[lead],
            "context": "Aziza's pirates surround Lil and Kamil, but Aziza chooses a duel at sea and notices Lil's sword.",
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B175 Japanese. Source presentation "
                "leads and FI/FA name macros are preserved. Literal uppercase "
                "I/F are unsafe renderer bytes."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v75-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "32 B175 Aziza pirate confrontation dialogue records; opaque event payload excluded.",
        "inventory": {"identified_records": 33, "translated_records": 32, "blocks": {"175": 32}},
        "excluded_records": EXCLUDED, "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records; {len(EXCLUDED)} excluded")


if __name__ == "__main__":
    main()
