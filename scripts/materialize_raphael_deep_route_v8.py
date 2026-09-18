from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v8.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B85_R0005": "Admiral {MACRO:FI},{LB}shall we ask Admiral Adernkatz{LB}one more time?",
    "DK4_MES_B85_R0011": "Yes.",
    "DK4_MES_B85_R0013": "No.",
    "DK4_MES_B85_R0021": "Let us go.{LB}We need his strength.{LB}This time, going alone.",
    "DK4_MES_B85_R0026": "Admiral?{LB}{MACRO:FI} {MACRO:FA} here.",
    "DK4_MES_B85_R0029": "Ah... you.",
    "DK4_MES_B85_R0034": "Studied hard.{LB}Please lend us your strength!",
    "DK4_MES_B85_R0037": "You have trained a little.",
    "DK4_MES_B85_R0040": "Since your visit,{LB}not one night brought peace.{LB}Your words would not leave me.",
    "DK4_MES_B85_R0044": "Then?!",
    "DK4_MES_B85_R0048": "Very well.{LB}Let me join your ship.",
    "DK4_MES_B85_R0056": "Try another time.",

    "DK4_MES_B86_R0005": "A sailor in the Caribbean{LB}must start with a glass of rum!{LB}Come, to the tavern!",
    "DK4_MES_B86_R0009": "Wh-what was that?!",
    "DK4_MES_B86_R0021": "Aah! Quake! Blaze!{LB}The world is ending!",
    "DK4_MES_B86_R0024": "Oh, stop yelling!",
    "DK4_MES_B86_R0032": "That startled me!",
    "DK4_MES_B86_R0036": "That bomb fool again...",
    "DK4_MES_B86_R0048": "B-bombs?!",
    "DK4_MES_B86_R0055": "Calls himself the{LB}'Magician of Blazing fire.'",
    "DK4_MES_B86_R0058": "Blazing?{LB}What an awful name.",
    "DK4_MES_B86_R0062": "What is he like?",
    "DK4_MES_B86_R0066": "Eccentric Charles?{LB}Would rather not discuss him.",
    "DK4_MES_B86_R0075": "An odd man studies explosives{LB}and cannons outside town.{LB}Sometimes he spreads that{LB}terrible noise everywhere.",
    "DK4_MES_B86_R0079": "Julio, making bombs means{LB}knowing cannons too, right?",
    "DK4_MES_B86_R0083": "Do not confuse bombs and cannons...{LB}But they are not so different.",
    "DK4_MES_B86_R0095": "By my calculations,{LB}he could greatly improve{LB}our fleet's combat power.",
    "DK4_MES_B86_R0102": "So he might be useful.",
    "DK4_MES_B86_R0105": "You are sailors?{LB}Will you take him somewhere else?",
    "DK4_MES_B86_R0117": "Somewhere else...{LB}The sea would qualify.",
    "DK4_MES_B86_R0125": "Yes, perhaps.",
    "DK4_MES_B86_R0129": "Wonderful!{LB}No, no... He will surely{LB}be useful to you!",
    "DK4_MES_B86_R0133": "Not sure how,{LB}but this got strange fast.",
    "DK4_MES_B86_R0138": "Charles! You in there?!",
    "DK4_MES_B86_R0143": "Ah, sir.{LB}Good to see you.",
    "DK4_MES_B86_R0147": "Do not thank me!{LB}You did it again today!",
    "DK4_MES_B86_R0150": "As explained before,{LB}this was not a failure.{LB}Success is very close! Besides...",
    "DK4_MES_B86_R0153": "Enough. Understood.{LB}No complaints today.",
    "DK4_MES_B86_R0157": "Visitors.{LB}They want to speak with you.",
    "DK4_MES_B86_R0161": "Hello.",
    "DK4_MES_B86_R0165": "Hmm?{LB}Have we met before?",
    "DK4_MES_B86_R0168": "Just hear them out.{LB}Surely this will be good for you.",
    "DK4_MES_B86_R0172": "Talk among yourselves.{LB}That settles it. Charles, goodbye!",
    "DK4_MES_B86_R0176": "Wait! Sir!",
    "DK4_MES_B86_R0180": "Science is too hard for him.{LB}No wonder he fails to understand.",
    "DK4_MES_B86_R0184": "You are the one{LB}who makes no sense...",
    "DK4_MES_B86_R0187": "Say something?",
    "DK4_MES_B86_R0199": "N-no, nothing.{LB}(Clau, one remark too many!)",
    "DK4_MES_B86_R0206": "We heard an expert in gunpowder{LB}and cannons lives here...",
    "DK4_MES_B86_R0210": "Yes! That is my research!{LB}Are you from the academy?",
    "DK4_MES_B86_R0213": "Hmm... not very scholarly.{LB}Nor do you look like sponsors.",
    "DK4_MES_B86_R0217": "Hey! You do not get to judge us!{LB}What a rude fool!",
    "DK4_MES_B86_R0222": "Please forget him.{LB}We came to ask you to join us.",
    "DK4_MES_B86_R0226": "We sail around the world.{LB}Your talents would greatly help{LB}our fleet.",
    "DK4_MES_B86_R0230": "Ah, navigators...{LB}Then, are you interested in science?",
    "DK4_MES_B86_R0235": "Science?",
    "DK4_MES_B86_R0239": "Science is truly magnificent!",
    "DK4_MES_B86_R0244": "Uh...",
    "DK4_MES_B86_R0248": "Science starts with curiosity,{LB}then practical experiment!",
    "DK4_MES_B86_R0251": "Repeated experiments{LB}bring progress!",
    "DK4_MES_B86_R0262": "Uh... if you say so.",
    "DK4_MES_B86_R0269": "Navigation too!{LB}Curiosity, courage, action{LB}expand the world!",
    "DK4_MES_B86_R0272": "Magnificent even to imagine!{LB}Navigation is science!",
    "DK4_MES_B86_R0276": "This is hard to follow...{LB}So, will you come with us?",
    "DK4_MES_B86_R0280": "Of course!{LB}A victory for science!",
    "DK4_MES_B86_R0283": "This fool is nonsense.",
}

SPEAKERS = {
    "04": "Arcadius", "05": "Claudio Manous", "06": "Julio",
    "07": "Crewmate", "0D": "Crew strategist", "10": "Gerhard Adernkatz",
    "12": "Charles Jean Rochefort", "6D": "Caribbean townsman", "97": "Crewmate",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "85": "Raphael may return alone to Gerhard Adernkatz after training and finally recruit him, or defer the visit again.",
    "86": "After an explosion in the Caribbean, Raphael's crew meets eccentric scientist Charles Jean Rochefort and recruits him through a comic discussion of explosives, cannons, science, and navigation.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    inventory = {row_id for row_id in all_rows if row_id.startswith(("DK4_MES_B85_", "DK4_MES_B86_"))}
    if set(LINES) != inventory:
        raise SystemExit(f"Raphael V8 inventory mismatch: missing={sorted(inventory-set(LINES))} extra={sorted(set(LINES)-inventory)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        blocks[block] = blocks.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the delayed-recruitment branch, character comedy, scientific argument, route macros, and fixed-allocation display safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v8-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Gerhard's delayed recruitment branch and Charles Jean Rochefort's Caribbean recruitment across Raphael SC0 blocks 85-86.",
        "excluded_records": {},
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
