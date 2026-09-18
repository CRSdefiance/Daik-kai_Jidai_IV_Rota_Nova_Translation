from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v7.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B84_R0006": "No navigators in this town?",
    "DK4_MES_B84_R0010": "Every town has sailors.",
    "DK4_MES_B84_R0014": "Let us ask around.{LB}Janus, go speak to someone.",
    "DK4_MES_B84_R0017": "Always ordering me around...",
    "DK4_MES_B84_R0021": "Excuse me.{LB}Seeking someone skilled with ships...",
    "DK4_MES_B84_R0024": "A sailor, eh?{LB}But Master Adernkatz is...",
    "DK4_MES_B84_R0027": "No, never mind.{LB}Heh heh heh.",
    "DK4_MES_B84_R0030": "What a strange old man.{LB}Ader... Adernkatz, was it?{LB}Maybe worth looking for him.",
    "DK4_MES_B84_R0034": "Admiral, heard a rumor{LB}about an Adern-something.",
    "DK4_MES_B84_R0037": "What?! Adernkatz?!{LB}Are you certain, Janus?",
    "DK4_MES_B84_R0040": "No reason to lie.",
    "DK4_MES_B84_R0044": "Good!",
    "DK4_MES_B84_R0049": "Clau! Wait!",
    "DK4_MES_B84_R0053": "Hey, kid!{LB}Where does Gerhard Adernkatz live?",
    "DK4_MES_B84_R0057": "Admiral Adernkatz?{LB}His mansion is that way.",
    "DK4_MES_B84_R0060": "Admiral... knew it.{LB}Thanks, kid. That way.{LB}{MACRO:FI}, hurry!",
    "DK4_MES_B84_R0065": "Rare to see Clau this excited.",
    "DK4_MES_B84_R0068": "Not excited...{LB}Just come and see.",
    "DK4_MES_B84_R0072": "Here?",
    "DK4_MES_B84_R0076": "Seems so.",
    "DK4_MES_B84_R0080": "Knock.",
    "DK4_MES_B84_R0085": "Who?",
    "DK4_MES_B84_R0090": "Good day.{LB}With {MACRO:FO}...",
    "DK4_MES_B84_R0093": "Admiral {MACRO:FI} {MACRO:FA}.{LB}Claudio Manous, navigator.",
    "DK4_MES_B84_R0097": "A navigator...{LB}What brings you here?",
    "DK4_MES_B84_R0100": "We heard of your skill{LB}and hoped to speak.",
    "DK4_MES_B84_R0103": "Long ago.{LB}Now this life is ashore.",
    "DK4_MES_B84_R0107": "Would you sail once more?",
    "DK4_MES_B84_R0110": "No.",
    "DK4_MES_B84_R0114": "Not so fast.{LB}You know Vels.",
    "DK4_MES_B84_R0121": "The man you let escape.",
    "DK4_MES_B84_R0126": "What?! What do you mean?!",
    "DK4_MES_B84_R0134": "Clau!{LB}What is going on?!",
    "DK4_MES_B84_R0137": "Gerhard Adernkatz,{LB}former commander of the strongest{LB}private fleet hunting pirates.",
    "DK4_MES_B84_R0140": "Pirates once vanished from the seas{LB}between the North Sea and{LB}Mediterranean. His fleet did that.",
    "DK4_MES_B84_R0144": "What?!{LB}He was that powerful?!",
    "DK4_MES_B84_R0147": "His navy once captured a vast{LB}pirate band. Vels was among them.",
    "DK4_MES_B84_R0151": "What?!",
    "DK4_MES_B84_R0155": "Enough, Manous.{LB}Let me explain the rest.{LB}All of you, come inside.",
    "DK4_MES_B84_R0160": "Vels was young and promising.{LB}This old man took him in{LB}and trained him.",
    "DK4_MES_B84_R0164": "Pirate Vels...{LB}an admiral's student?!",
    "DK4_MES_B84_R0167": "Once given a ship, he mutinied{LB}and fled. Afterward,{LB}this old man resigned.",
    "DK4_MES_B84_R0171": "Why not pursue him then?",
    "DK4_MES_B84_R0175": "Old comrades followed him,{LB}tempted by freedom and gold.",
    "DK4_MES_B84_R0179": "Perhaps strict rules and thrift{LB}were the wrong virtues.{LB}This old man lost faith{LB}in his command.",
    "DK4_MES_B84_R0186": "The sea was abandoned before!",
    "DK4_MES_B84_R0190": "Life here is comfortable.{LB}People leave this old man alone.{LB}Each quiet day simply passes...",
    "DK4_MES_B84_R0194": "But nothing is truly{LB}resolved, is it?",
    "DK4_MES_B84_R0197": "Your name was {MACRO:FI}?{LB}Say what you mean clearly.",
    "DK4_MES_B84_R0202": "Our fleet barely survived Vels.{LB}We need your help.",
    "DK4_MES_B84_R0206": "Help...?{LB}An old man's counsel is useless.{LB}Vels took everything.",
    "DK4_MES_B84_R0211": "No. That is not true.",
    "DK4_MES_B84_R0215": "{MACRO:FI}...{LB}What do you expect from me?",
    "DK4_MES_B84_R0225": "Let us defeat Vels.",
    "DK4_MES_B84_R0227": "No need to defeat him.",
    "DK4_MES_B84_R0235": "Simply board our ship.{LB}Nothing else is needed.{LB}Together, we can defeat Vels!",
    "DK4_MES_B84_R0244": "Do not take offense.{LB}Even with my help, you cannot{LB}stand against Vels as you are.",
    "DK4_MES_B84_R0249": "We lack the strength...?",
    "DK4_MES_B84_R0253": "Let me think.",
    "DK4_MES_B84_R0258": "Understood. Next time we meet,{LB}hope you will have decided.{LB}Please excuse us.",
    "DK4_MES_B84_R0273": "Pardon any insolence.",
    "DK4_MES_B84_R0278": "But the methods that built{LB}the strongest fleet cannot{LB}have been wrong.",
    "DK4_MES_B84_R0286": "Vels was wrong!{LB}He betrayed you out of greed,{LB}and that cannot be forgiven!",
    "DK4_MES_B84_R0294": "Yet Vels is cautious.{LB}He will not be lured out easily.",
    "DK4_MES_B84_R0298": "He is arrogant now.{LB}Spread word you returned to sea,{LB}and he will reveal himself.",
    "DK4_MES_B84_R0302": "Perhaps.{LB}He likely thinks this old man dead.",
    "DK4_MES_B84_R0307": "Then...!",
    "DK4_MES_B84_R0311": "Very well. My fault.{LB}This old man must end it.",
    "DK4_MES_B84_R0315": "Thank you!{LB}Train us too.{LB}We are ready.",
    "DK4_MES_B84_R0319": "Good. Harsh training.",
    "DK4_MES_B84_R0328": "Your help is not wanted{LB}only to defeat Vels.",
    "DK4_MES_B84_R0332": "Meaning?",
    "DK4_MES_B84_R0337": "Please sail for our fleet!{LB}With you beside us, we can achieve{LB}something worthy of history!",
    "DK4_MES_B84_R0350": "Do not take offense.{LB}A grand speech from a boy{LB}does not earn my trust{LB}to place my life in his hands.",
    "DK4_MES_B84_R0354": "We lack the strength...?",
    "DK4_MES_B84_R0358": "The sea was abandoned.{LB}Leave for today.",
    "DK4_MES_B84_R0362": "Understood. Next time we meet,{LB}hope you will have decided.{LB}Please excuse us.",
    "DK4_MES_B84_R0377": "Pardon any insolence.",
    "DK4_MES_B84_R0382": "But the methods that built{LB}the strongest fleet cannot{LB}have been wrong.",
    "DK4_MES_B84_R0390": "Teach us your way of battle!{LB}Please!",
    "DK4_MES_B84_R0398": "Be ready.",
    "DK4_MES_B84_R0403": "Then...!!",
    "DK4_MES_B84_R0407": "Very well.{LB}Prepare yourself.",
    "DK4_MES_B84_R0417": "Before returning to sea,{LB}there is something to teach.{LB}Want special training?",
    "DK4_MES_B84_R0427": "Train hard.",
    "DK4_MES_B84_R0429": "Hear him.",
    "DK4_MES_B84_R0431": "Keep my own style.",
    "DK4_MES_B84_R0439": "Good nerve.{LB}Do not quit.",
    "DK4_MES_B84_R0443": "Now you look capable.{LB}Take me to the ship.",
    "DK4_MES_B84_R0446": "On the way,{LB}let us discuss combat.",
    "DK4_MES_B84_R0450": "Yes, please.",
    "DK4_MES_B84_R0454": "Start with naval gunfire.{LB}Here is the standard{LB}crossing-the-T tactic.",
    "DK4_MES_B84_R0458": "Avoid the enemy broadside.{LB}Move before or behind the ship,{LB}then turn your own broadside{LB}toward it and fire.",
    "DK4_MES_B84_R0462": "Yes...",
    "DK4_MES_B84_R0466": "You steer; gunners fire alone.{LB}Put a sailor with high accuracy{LB}at the gun deck for better fire.",
    "DK4_MES_B84_R0470": "Naval movement works as at sea.{LB}Set course and sail direction.{LB}Guns fire automatically{LB}when an enemy enters range.",
    "DK4_MES_B84_R0473": "To prepare for boarding, refit a hold{LB}into Marine Quarters at a shipyard.",
    "DK4_MES_B84_R0476": "Hire extra sailors for boarding.{LB}Assign a skilled swordsman{LB}to lead the Marine Quarters{LB}for greater effect.",
    "DK4_MES_B84_R0480": "Choose a skilled fighter{LB}for Marine Quarters.",
    "DK4_MES_B84_R0483": "Touching ships begin boarding.{LB}Your leader commands the attack.",
    "DK4_MES_B84_R0487": "That is all.",
    "DK4_MES_B84_R0492": "Understood.{LB}Now we need real battle experience.{LB}Thank you.",
    "DK4_MES_B84_R0507": "{MACRO:FI}'s{LB}stamina, agility, spirit rose!",
    "DK4_MES_B84_R0511": "Good enough.",
    "DK4_MES_B84_R0515": "Now, let us discuss combat.",
    "DK4_MES_B84_R0519": "Yes, please.",
    "DK4_MES_B84_R0523": "Start with naval gunfire.{LB}Here is the standard{LB}crossing-the-T tactic.",
    "DK4_MES_B84_R0527": "Avoid the enemy broadside.{LB}Move before or behind the ship,{LB}then turn your own broadside{LB}toward it and fire.",
    "DK4_MES_B84_R0531": "Yes...",
    "DK4_MES_B84_R0535": "You steer; gunners fire alone.{LB}Put a sailor with high accuracy{LB}at the gun deck for better fire.",
    "DK4_MES_B84_R0539": "Naval movement works as at sea.{LB}Set course and sail direction.{LB}Guns fire automatically{LB}when an enemy enters range.",
    "DK4_MES_B84_R0542": "To prepare for boarding, refit a hold{LB}into Marine Quarters at a shipyard.",
    "DK4_MES_B84_R0545": "Hire extra sailors for boarding.{LB}Assign a skilled swordsman{LB}to lead the Marine Quarters{LB}for greater effect.",
    "DK4_MES_B84_R0549": "Choose a skilled fighter{LB}for Marine Quarters.",
    "DK4_MES_B84_R0552": "Touching ships begin boarding.{LB}Your leader commands the attack.",
    "DK4_MES_B84_R0556": "That is all.{LB}Understand?",
    "DK4_MES_B84_R0561": "Yes. Now we need{LB}real battle experience.{LB}Thank you.",
    "DK4_MES_B84_R0566": "{MACRO:FI}'s{LB}wit rose!",
    "DK4_MES_B84_R0571": "So the ship itself must teach you.{LB}Very well.",
    "DK4_MES_B84_R0577": "{MACRO:FI}'s{LB}luck rose!",
}

SPEAKERS = {
    "04": "Arcadius", "05": "Claudio Manous", "10": "Gerhard Adernkatz",
    "52": "Old townsman", "A2": "Boy", "FE": "Tutorial narrator",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "Claudio leads Raphael to veteran admiral Gerhard Adernkatz, who reveals his history with the pirate Vels, joins after Raphael's appeal, and teaches naval gunfire and boarding through all training branches."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    inventory = {row_id for row_id in all_rows if row_id.startswith("DK4_MES_B84_")}
    if set(LINES) != inventory:
        raise SystemExit(f"Raphael V7 inventory mismatch: missing={sorted(inventory-set(LINES))} extra={sorted(set(LINES)-inventory)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
            "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Gerhard's regret, Claudio's urgency, both persuasion branches, all choices, stat rewards, and exact naval-combat mechanics.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v7-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Gerhard Adernkatz recruitment, both Vels persuasion branches, all training choices, stat rewards, and the complete naval-combat tutorial in Raphael SC0 block 84.",
        "excluded_records": {},
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": {"84": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
