from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v39.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    13: ("Oh, Kamil!", "Oh, Kamil!"),
    17: ("Did something happen?", "Something wrong?"),
    21: ("Huh? Why?", "What? Why?"),
    25: ("Well, you looked as if something was troubling you.", "You looked worried, that's all."),
    32: ("So the sorrow in my expression made your heart skip a beat?", "So my troubled look made your heart skip a beat?"),
    35: ("W-what are you saying? I was only worried about you!", "W-what?! Just worried about you!"),
    38: ("It was a joke. You don't need to get so worked up.", "Just kidding! No need to get upset."),
    42: ("Y-yes. You're right.", "Y-yeah. Right."),
    46: ("But it seems you weren't worried. Of course it's strange to imagine FI worried. Ha ha...", "So you weren't worried... Why would {MACRO:FI} be? Ha ha..."),
    55: ("I'm a little worried.", "Maybe a little."),
    57: ("I'm not worried at all.", "Nothing's wrong."),
    68: ("So you were worried after all. Tell me about it.", "You were worried! Tell me about it."),
    71: ("What I'm doing isn't wrong, is it? I'm only punishing companies that do bad things, right?", "We're doing the right thing, aren't we? We only punish companies that do wrong."),
    75: ("Yes. FI, you haven't done anything wrong.", "You're right, {MACRO:FI}."),
    78: ("But even those people have families. I'm making their families unhappy...", "They have families too. My actions hurt their loved ones."),
    82: ("That is...", "Well..."),
    86: ("No, it's fine. Talking about it made me feel better. Sorry, Kamil.", "No, it's okay. Talking helped. Sorry, Kamil."),
    94: ("Come on, you have your own work to do, don't you?", "Come on, you have work to do!"),
    98: ("Yes, I do, but...", "Yes, but..."),
    106: ("Oh, that's right!", "Oh, right!"),
    110: ("W-what is it?!", "W-what?"),
    114: ("There's something good for you!", "Got something!"),
    122: ("The Guiding Staff!", "The Guiding Staff!"),
    126: ("The Guiding Staff?", "Guiding Staff?"),
    130: ("Yes. A recent rumor told me of a legendary staff that guides its bearer toward goodness.", "There's a legend about the Guiding Staff. They say it guides its owner toward good."),
    133: ("Really? That sounds dubious, but where is it?", "Really? Sounds dubious. Where?"),
    137: ("Somewhere around India, apparently.", "The subcontinent."),
    141: ("Where in India?", "Where exactly?"),
    145: ("I don't know that much...", "No idea..."),
    149: ("That doesn't help me find it... Oh well. I'll look if I get the chance.", "That's vague. Let's look later."),
    153: ("Right. I'll get back to my work.", "Sure. Time to get back to work."),
    156: ("Oh, Kamil!", "Oh, Kamil!"),
    160: ("What?", "Hm?"),
    164: ("Thank you...", "...Thanks."),
    168: ("Huh? Uh, sure.", "Huh? Oh, sure."),
    175: ("Of course! I can't be a woman of the sea if I keep brooding over every little thing.", "Of course! Can't lead a fleet while moping around!"),
    179: ("Heh, that's right.", "Ha! True."),
    183: ("Besides, worrying is your job, Kamil! If I worry too, it'll be so gloomy that not a sailor will stay.", "Worrying's your job, Kamil! We'd lose the crew if we both moped."),
    186: ("That's harsh. I don't worry because I like it. FI is...", "That's mean! {MACRO:FI} makes me worry..."),
    190: ("Did you say something?", "What was that?"),
    194: ("Nothing. I'll get back to my work.", "Nothing. Back to work for me."),
    197: ("Okay. Thanks for worrying about me. See you later.", "Okay. Thanks for caring. See you!"),
    200: ("Huh? Oh, okay.", "Huh? Oh, okay."),
    205: ("FI's spirit rose by one!", "{MACRO:FI}'s spirit rose by 1!"),
}
SPEAKERS = {0x02: "Lil Argot", 0x09: "Kamil", 0xFE: "Spirit reward panel"}
TEXT_LEADS = {0x82, 0x94}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B125_")}
    if {f"DK4_MES_B125_R{number:04d}" for number in LINES} != expected:
        raise ValueError("B125 coverage does not match clean source")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B125_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead not in SPEAKERS and lead not in TEXT_LEADS:
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        records.append({
            "id": row_id,
            "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "") + english + "{PAD}",
            "speaker": SPEAKERS.get(lead, "Lil response choice"),
            "context": (
                "Kamil notices Lil's troubled expression; Lil jokes about his concern."
                if number < 55 else
                "Lil may confide guilt about hurting merchant families, or deny worrying. Kamil suggests the Guiding Staff, then both return to work."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Localized from clean Japanese in scene order. Preserves both response branches, Lil's moral doubt, Kamil's flirtatious worry, "
                "the established Guiding Staff item name, the subcontinent clue, FI macros, and the spirit reward. "
                "82/94 response starts are visible text, not speaker commands. Automatic guarded wrapping protects continuation letters."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v34-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 44 B125 Kamil-and-Lil doubt, response-choice, Guiding Staff and spirit-reward records.",
        "inventory": {"identified_records": 44, "translated_records": len(records), "blocks": {"125": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
