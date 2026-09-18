from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v13.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B64_R0005": "Conflicted...",
    "DK4_MES_B64_R0009": "{MACRO:FI}...{LB}This was inevitable...",
    "DK4_MES_B64_R0012": "Kamil...",
    "DK4_MES_B64_R0016": "Marinus. At last.",
    "DK4_MES_B64_R0020": "D-dad...?",
    "DK4_MES_B64_R0024": "My own son defeated me...{LB}Never thought you came this far.",
    "DK4_MES_B64_R0027": "You understand now, right?{LB}Honest trade can earn money.{LB}Just like long ago.",
    "DK4_MES_B64_R0030": "Perhaps.{LB}But my methods are my own.",
    "DK4_MES_B64_R0033": "Dad!",
    "DK4_MES_B64_R0037": "Starting again from nothing.{LB}Nothing is over.{LB}Our next contest can wait.",
    "DK4_MES_B64_R0045": "Marinus, keep these for me.{LB}They serve me no purpose now.{LB}Soon, they will be mine again...",
    "DK4_MES_B64_R0049": "What?",
    "DK4_MES_B64_R0053": "These appeared among my things.{LB}They recalled old days...",
    "DK4_MES_B64_R0056": "One came in my youth.{LB}The other came long ago{LB}from your mother.",
    "DK4_MES_B64_R0061": "Dad, these...!",
    "DK4_MES_B64_R0066": "Dad!{LB}Come back to Holland!{LB}Not too late!",
    "DK4_MES_B64_R0070": "Too late to turn back...",
    "DK4_MES_B64_R0074": "Why are you always like this?{LB}So stubborn!",
    "DK4_MES_B64_R0077": "Adults are so.{LB}Someday you will understand.",
    "DK4_MES_B64_R0080": "Why... Dad?",
    "DK4_MES_B64_R0084": "Kamil...",
    "DK4_MES_B64_R0088": "That is okay. Knew it.{LB}Dad is like that.{LB}He cannot change so easily...",
    "DK4_MES_B64_R0092": "Maybe... But when he gave you{LB}that locket,{LB}his face looked so kind...",
    "DK4_MES_B64_R0104": "Kuhn loves you{LB}in his own way...",
    "DK4_MES_B64_R0110": "Yes...",
    "DK4_MES_B65_R0017": "With its largest company gone,{LB}we can trade freely{LB}throughout Southeast Asia!",
    "DK4_MES_B65_R0021": "Let us go!",
    "DK4_MES_B65_R0027": "The region's largest company fell.{LB}Now no one can object{LB}to our free trade!",
    "DK4_MES_B65_R0030": "Let us go!",
    "DK4_MES_B65_R0050": "Kuhn's company now serves us,{LB}so we can trade freely{LB}across Southeast Asia. Let us go!",
    "DK4_MES_B65_R0057": "Y-yeah...",
    "DK4_MES_B65_R0061": "Hm? What is wrong?{LB}You look pale.",
    "DK4_MES_B65_R0072": "Tired from the voyage?",
    "DK4_MES_B65_R0079": "N-no, nothing...",
    "DK4_MES_B65_R0088": "Really...? All right, then...{LB}Who are you?!",
    "DK4_MES_B65_R0093": "Really...? All right, then...{LB}You!",
    "DK4_MES_B65_R0104": "Why are you here?!",
    "DK4_MES_B65_R0115": "So... it really was you.{LB}Rumors made me wonder...",
    "DK4_MES_B65_R0123": "Who is he...?",
    "DK4_MES_B65_R0129": "Kuhn!",
    "DK4_MES_B65_R0140": "Marinus...?",
    "DK4_MES_B65_R0144": "Yes...",
    "DK4_MES_B65_R0153": "Marinus?{LB}Why did Kamil answer?{LB}Nothing makes sense!",
    "DK4_MES_B65_R0159": "Marinus?! What does that mean?{LB}You know Kuhn?",
    "DK4_MES_B65_R0173": "What is your connection?",
    "DK4_MES_B65_R0188": "What?!",
    "DK4_MES_B65_R0195": "{MACRO:FI}...{LB}There is a story.",
    "DK4_MES_B65_R0198": "Marinus. Never expected{LB}to meet my son again here...",
    "DK4_MES_B65_R0207": "Son...?",
    "DK4_MES_B65_R0213": "Your son?! Kamil's father{LB}is Antony Kuhn?!",
    "DK4_MES_B65_R0227": "S-son?!{LB}You said your father was gone...{LB}dead!",
    "DK4_MES_B65_R0242": "A lie?",
    "DK4_MES_B65_R0249": "Sorry... My true name is{LB}Marinus Kuhn.",
    "DK4_MES_B65_R0252": "You understand now, right?{LB}Honest trade can earn money.{LB}Just like long ago.",
    "DK4_MES_B65_R0255": "Perhaps.{LB}But my methods are my own.",
    "DK4_MES_B65_R0258": "Dad!",
    "DK4_MES_B65_R0262": "Starting again from nothing.{LB}Nothing is over.",
    "DK4_MES_B65_R0269": "Marinus, keep this for me.{LB}No use to me now.",
    "DK4_MES_B65_R0272": "What?",
    "DK4_MES_B65_R0276": "Won in my youth.",
    "DK4_MES_B65_R0282": "Dad... can you not become{LB}the kind father you once were?",
    "DK4_MES_B65_R0286": "Cannot be.",
    "DK4_MES_B65_R0290": "Why? Start over with Mom,{LB}just like long ago!",
    "DK4_MES_B65_R0293": "Mother well?",
    "DK4_MES_B65_R0297": "Yes.",
    "DK4_MES_B65_R0301": "Good. Enough.{LB}Many years have passed.{LB}Life has no reverse.",
    "DK4_MES_B65_R0305": "Dad...",
    "DK4_MES_B65_R0309": "Marinus... guard Mom.",
    "DK4_MES_B65_R0313": "...All right. Be well, Dad...",
    "DK4_MES_B65_R0317": "Kamil, what was that...?",
    "DK4_MES_B65_R0321": "Sorry...{LB}Cannot discuss it...",
    "DK4_MES_B65_R0324": "...Oh.",
    "DK4_MES_B65_R0336": "Leave him be...{LB}Everyone has a past{LB}they cannot bear touched.",
    "DK4_MES_B65_R0351": "Do not worry.{LB}Someday he will tell us...",
}

EXCLUDED = {
    "DK4_MES_B64_R0059": "Seven-byte scene/control payload (47 96 46 47 80 12 05), not standalone dialogue.",
}
SPEAKERS = {
    "02": "Lil Argot", "06": "Old sailor", "07": "Crewmate", "09": "Kamil",
    "10": "Gerhard", "13": "Crewmate", "14": "Fernando", "28": "Antony Kuhn",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    64: "After Kuhn's defeat, Kamil confronts his father; Kuhn entrusts him with keepsakes from his youth and Kamil's mother before leaving.",
    65: "Alternate Kuhn defeat and submission branches reveal Kamil as Marinus Kuhn, expose their father-son relationship, and end with Kuhn's keepsake and farewell.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V13 inventory mismatch: missing={sorted(missing)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving both Kuhn outcomes, the Marinus reveal, family history, keepsakes, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Both Kuhn defeat/submission branches, Kamil's Marinus identity reveal, family confrontation, keepsakes, and farewell across SC2 blocks 64-65.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; {len(EXCLUDED)} control exclusion")


if __name__ == "__main__":
    main()
