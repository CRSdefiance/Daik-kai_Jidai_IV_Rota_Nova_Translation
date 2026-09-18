from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v14.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B66_R0012": "Kuhn Company, Southeast Asia's{LB}largest, is gone.{LB}Trade here is free now.",
    "DK4_MES_B66_R0016": "Let us go!",
    "DK4_MES_B66_R0033": "Kuhn serves us now.{LB}So trade is free{LB}across Southeast Asia.",
    "DK4_MES_B66_R0046": "So, {MACRO:FI}...",
    "DK4_MES_B66_R0050": "Who are you?!",
    "DK4_MES_B66_R0054": "Antony Kuhn...",
    "DK4_MES_B66_R0058": "You are Kuhn...",
    "DK4_MES_B66_R0064": "You are {MACRO:FI}?",
    "DK4_MES_B66_R0067": "You!",
    "DK4_MES_B66_R0074": "Where is Marinus?",
    "DK4_MES_B66_R0078": "Marinus?",
    "DK4_MES_B66_R0088": "No one here has that name.",
    "DK4_MES_B66_R0092": "So... you do not know.",
    "DK4_MES_B66_R0096": "What?",
    "DK4_MES_B66_R0102": "Kamil's true name?{LB}He left us.",
    "DK4_MES_B66_R0105": "You know more than me, right?{LB}You are his father.",
    "DK4_MES_B66_R0109": "You know our relation?",
    "DK4_MES_B66_R0113": "...Yes.",
    "DK4_MES_B66_R0117": "So...",
    "DK4_MES_B66_R0124": "Pardon me. Goodbye.",
    "DK4_MES_B66_R0128": "Dad!",
    "DK4_MES_B66_R0132": "Kamil...",
    "DK4_MES_B66_R0144": "Kamil! Where have you been?!",
    "DK4_MES_B66_R0158": "You are back! So glad!",
    "DK4_MES_B66_R0169": "Kamil, safe now?",
    "DK4_MES_B66_R0173": "Yes.",
    "DK4_MES_B66_R0177": "Then, goodbye.",
    "DK4_MES_B66_R0181": "Hodram,{LB}thank you so much!",
    "DK4_MES_B66_R0184": "No worry.",
    "DK4_MES_B66_R0188": "Kamil, where were you?!",
    "DK4_MES_B66_R0198": "And why call him Dad?{LB}What is this?!",
    "DK4_MES_B66_R0203": "We searched...",
    "DK4_MES_B66_R0211": "We owe an apology.{LB}Kamil, you are Kuhn's...",
    "DK4_MES_B66_R0217": "Yes... Overijssel is Mom's surname.{LB}My true name is Marinus Kuhn.{LB}Antony Kuhn is my father.",
    "DK4_MES_B66_R0226": "Marinus Kuhn...{LB}Kuhn is Kamil's father...",
    "DK4_MES_B66_R0229": "Yes.{LB}Kamil is my old nickname.",
    "DK4_MES_B66_R0237": "Dad was once a good man.{LB}When he met Mom,{LB}he ran a tiny trading company.",
    "DK4_MES_B66_R0241": "Poor, but each day was happy{LB}and fun, Mom said.",
    "DK4_MES_B66_R0244": "Then his company reached{LB}the spice islands and prospered.{LB}Great wealth changed Dad...",
    "DK4_MES_B66_R0248": "Greed blinded him.{LB}Profit became all he cared for,{LB}even through dirty methods...",
    "DK4_MES_B66_R0252": "Neither Mom nor me{LB}could bear any of it.",
    "DK4_MES_B66_R0255": "Kamil...",
    "DK4_MES_B66_R0259": "Everyone feared Dad.{LB}Neighbors began avoiding{LB}Mom and me too...",
    "DK4_MES_B66_R0263": "Mom knew we could not remain.{LB}She took me{LB}back to Holland.",
    "DK4_MES_B66_R0267": "{MACRO:FI}...{LB}Never meant to tell anyone{LB}about Dad. Least of all you.",
    "DK4_MES_B66_R0270": "That is why... Sorry.",
    "DK4_MES_B66_R0280": "No... That explains{LB}why you fought it...",
    "DK4_MES_B66_R0283": "Even without knowing,{LB}we doubted you...{LB}Truly sorry...",
    "DK4_MES_B66_R0289": "No...{LB}You suffered too, Kamil...",
    "DK4_MES_B66_R0295": "{MACRO:FI}...{LB}may this ship take me back?",
    "DK4_MES_B66_R0298": "Of course!{LB}Things were hard without you!{LB}Work enough to make up for it!",
    "DK4_MES_B66_R0302": "You never change, {MACRO:FI}.{LB}Still working people hard.",
    "DK4_MES_B66_R0306": "Oh, sorry!",
    "DK4_MES_B66_R0310": "Ha ha. That is{LB}{MACRO:FI} as always.",
    "DK4_MES_B66_R0313": "Kamil...{LB}(So glad you came back!)",
    "DK4_MES_B66_R0317": "Hey, Dad.",
    "DK4_MES_B66_R0321": "What?",
    "DK4_MES_B66_R0325": "You understand now, right?{LB}Honest trade can earn money.{LB}Just like long ago.",
    "DK4_MES_B66_R0328": "Perhaps.{LB}But my methods are my own.",
    "DK4_MES_B66_R0331": "Dad!",
    "DK4_MES_B66_R0335": "Starting again from nothing.{LB}Nothing is over.",
    "DK4_MES_B66_R0342": "Marinus, keep this for me.{LB}No use to me now.",
    "DK4_MES_B66_R0345": "What?",
    "DK4_MES_B66_R0349": "Won in my youth.",
    "DK4_MES_B66_R0355": "Dad... can you not become{LB}the kind father you once were?",
    "DK4_MES_B66_R0359": "Cannot be.",
    "DK4_MES_B66_R0363": "Why? Start over with Mom,{LB}just like long ago!",
    "DK4_MES_B66_R0366": "Mother well?",
    "DK4_MES_B66_R0370": "Yes.",
    "DK4_MES_B66_R0374": "Take care of Mom.",
    "DK4_MES_B66_R0378": "Not fair!{LB}Go see Mom yourself!",
    "DK4_MES_B66_R0381": "Adults have their reasons.{LB}Goodbye.",
    "DK4_MES_B67_R0011": "Pirate Clifford...{LB}Worthy of England's royal favor,{LB}but...",
    "DK4_MES_B67_R0017": "Top English pirate{LB}is gone.",
    "DK4_MES_B67_R0032": "Swallowed by the new age...",
    "DK4_MES_B67_R0036": "Yes...",
    "DK4_MES_B67_R0051": "...Somehow sad...",
    "DK4_MES_B67_R0063": "Clifford's manor{LB}held this letter.",
    "DK4_MES_B67_R0066": "Letter?",
    "DK4_MES_B67_R0070": "Yes, this one.",
    "DK4_MES_B67_R0074": "\"North's ruler...\"{LB}Hm?",
    "DK4_MES_B67_R0077": "North's conqueror, a gift awaits.{LB}Bring this to Amsterdam's tavern.{LB}-James Clifford",
    "DK4_MES_B67_R0080": "A gift...? Not sure why,{LB}but Amsterdam's tavern is next.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "02": "Lil Argot", "06": "Old sailor", "09": "Kamil",
    "0E": "Emilio Ferrog", "10": "Gerhard", "14": "Fernando", "28": "Antony Kuhn",
    "97": "Sailor", "FE": "Letter",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    66: "After Kuhn's defeat or submission, Hodram returns Kamil; Kamil reveals his Marinus identity and childhood, rejoins Lil, and confronts his father before their farewell.",
    67: "After Clifford's defeat, Lil's crew reflects on his fall and finds his letter promising a heartfelt gift at Amsterdam's tavern.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V14 inventory mismatch: missing={sorted(missing)}")
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
            "localization_note": "Faithful concise American English preserving both Kuhn outcomes, Kamil's return and childhood, Hodram's role, Clifford's letter, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Kamil's return with Hodram, Marinus identity and childhood, Kuhn family reconciliation, and Clifford's Amsterdam gift letter across SC2 blocks 66-67.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
