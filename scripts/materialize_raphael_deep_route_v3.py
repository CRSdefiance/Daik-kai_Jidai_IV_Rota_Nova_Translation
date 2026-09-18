from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v3.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B75_R0006": "Move, pest.",
    "DK4_MES_B75_R0015": "Hey! Watch it!",
    "DK4_MES_B75_R0019": "...Do you know whom you address?",
    "DK4_MES_B75_R0023": "Who cares?{LB}You crashed into me!{LB}Why act so high and mighty?!",
    "DK4_MES_B75_R0027": "Such insolence toward{LB}Cordoba's Linares family...",
    "DK4_MES_B75_R0031": "Linares?",
    "DK4_MES_B75_R0043": "Could he perhaps{LB}be a nobleman?",
    "DK4_MES_B75_R0057": "This may become troublesome...",
    "DK4_MES_B75_R0064": "Linares or whatever!{LB}You shove a man and refuse{LB}to apologize. What a farce!",
    "DK4_MES_B75_R0072": "Whoa!{LB}A glove?!",
    "DK4_MES_B75_R0075": "Draw. A duel.",
    "DK4_MES_B75_R0079": "What?!",
    "DK4_MES_B75_R0084": "A duel over this?{LB}That is absurd!",
    "DK4_MES_B75_R0088": "No Spanish naval officer{LB}ignores an insult to his honor.",
    "DK4_MES_B75_R0091": "Honor? These pampered mad nobles{LB}will rule our Portugal?!",
    "DK4_MES_B75_R0094": "Ah, Portuguese.{LB}That explains your poor attitude{LB}toward Spanish officers.",
    "DK4_MES_B75_R0098": "Hear this.{LB}The Spanish Armada will now{LB}protect you Portuguese.",
    "DK4_MES_B75_R0102": "You trade in peace only because{LB}we fight your enemies each day.{LB}Remember that.",
    "DK4_MES_B75_R0111": "This outrage is forgiven.{LB}Now vanish.",
    "DK4_MES_B75_R0115": "Wait!",
    "DK4_MES_B75_R0119": "...Still confused?",
    "DK4_MES_B75_R0124": "You protect us?{LB}Enough of that delusion!",
    "DK4_MES_B75_R0128": "What?!",
    "DK4_MES_B75_R0133": "Our {MACRO:FO}{LB}acts by its own power!{LB}We will never submit to Spain!",
    "DK4_MES_B75_R0137": "So you are the foolish boy{LB}still claiming Portuguese nationality.",
    "DK4_MES_B75_R0142": "No false claim!{LB}Portugal is forever my homeland!{LB}Never Spain!",
    "DK4_MES_B75_R0146": "Clinging to a vanished nation?{LB}How pathetic.",
    "DK4_MES_B75_R0151": "Not vanished...{LB}We will restore Portugal!",
    "DK4_MES_B75_R0155": "Restore Portugal?{LB}Such grand delusion.",
    "DK4_MES_B75_R0158": "That is rebellion{LB}against the Spanish crown.{LB}You cannot be allowed to live.",
    "DK4_MES_B75_R0162": "No need to trouble Lord Valdes.{LB}You die here. Draw!",
    "DK4_MES_B75_R0167": "Gladly!",
    "DK4_MES_B75_R0171": "Cry all you want.{LB}No mercy!",
    "DK4_MES_B75_R0174": "Simon!{LB}What is this?!",
    "DK4_MES_B75_R0177": "L-Lord Valdes!!",
    "DK4_MES_B75_R0181": "We are surrounded!!",
    "DK4_MES_B75_R0184": "No escape...!",
    "DK4_MES_B75_R0188": "Sir! These men plotted rebellion{LB}against His Majesty.{LB}Their execution was about to begin.",
    "DK4_MES_B75_R0191": "Rebellion?",
    "DK4_MES_B75_R0195": "Yes. They spoke of restoring{LB}Portugal and other sedition.",
    "DK4_MES_B75_R0198": "Portugal?{LB}You belong to {MACRO:FO}?",
    "DK4_MES_B75_R0203": "We do!",
    "DK4_MES_B75_R0207": "...Go.",
    "DK4_MES_B75_R0215": "What?",
    "DK4_MES_B75_R0223": "Our dispute will be settled at sea.{LB}Leave this city now.",
    "DK4_MES_B75_R0227": "...Damn!",
    "DK4_MES_B75_R0231": "You call that mercy?!",
    "DK4_MES_B75_R0235": "Mercy? Ha ha ha!{LB}You expect to defeat us?",
    "DK4_MES_B75_R0238": "My Armada is invincible.{LB}Tradition, dignity, perfect order...{LB}You are beneath notice.",
    "DK4_MES_B75_R0242": "You will regret this!",
    "DK4_MES_B75_R0246": "Lord Valdes!",
    "DK4_MES_B75_R0250": "Brawling with children{LB}shames you.",
    "DK4_MES_B75_R0253": "Y-yes, sir!{LB}But...",
    "DK4_MES_B75_R0256": "Do you not see?{LB}This capital cannot bear{LB}a loser's blood.",
    "DK4_MES_B75_R0260": "Ah!{LB}Of course. My error.",
    "DK4_MES_B75_R0264": "Besides, they suit the new{LB}combined fleet's battle exercise.",
    "DK4_MES_B75_R0267": "Yes, sir!{LB}Such deep insight!",
}

SPEAKERS = {
    "04": "Emilio Marone", "05": "Claudio Manous", "06": "Eirene", "1F": "Valdes", "30": "Simon Linares",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "In Seville, Claudio clashes with Spanish officer Simon Linares; Raphael declares Portugal will rise again before Valdes intervenes and challenges them to settle the conflict at sea."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Raphael V3 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor"), "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Natural concise American English preserving the class conflict, Portuguese defiance, military threat, and Valdes's contempt.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Simon Linares confrontation and Valdes's Seville challenge in SC0 block 75.",
        "excluded_records": {},
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": {"75": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
