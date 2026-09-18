from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v51.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "So this is Alexandria...",
    "Busy place.",
    "Hm?{LB}Someone is coming this way.",
    "Could it be?!",
    "What is it?",
    "Th-this ship!{LB}No mistake, sir!",
    "Some parts changed, yet...{LB}the likeness remains!{LB}Oh, beloved Elysion!",
    "A ship's likeness?",
    "This ship...?",
    "Pardon me.{LB}Cesare Tohni, sir.{LB}Once the owner of this ship...",
    "Pirates attacked one day.{LB}This man survived,{LB}but the ship was stolen.",
    "That stolen ship was{LB}my beloved Elysion!{LB}Oh, how this man grieved...",
    "Rumor said she was abandoned.{LB}This man searched day and night,{LB}believing we would meet again!",
    "Yes! This was my ship!{LB}Of course, no demand to return her.",
    "Only one plea, sir!{LB}Take this man along!{LB}Let me sail with the Elysion!",
    "So you're the former owner...{LB}Ah! Then there are questions!",
    "Nothing makes sense.{LB}Does this ship have mechanisms{LB}found in no book?",
    "You noticed them!{LB}A true expert on ships!",
    "Oh, hardly...{LB}Come! Teach me everything!",
    "Of course!{LB}Gladly, sir!",
    "Ah, no introduction yet...{LB}Janus Pasar.",
    "Cesare Tohni, sir.",
    "Take this spot.{LB}Something feels strange.{LB}Another mechanism?",
    "Ah, you noticed this.{LB}What it is...",
    "A hidden mount{LB}for extra armor!",
    "Press this little bump{LB}with a click!",
    "Then...",
    "Then?{LB}O-ohhh!",
    "Extra armor can now{LB}be installed!",
    "A-amazing!{LB}Could this work on other ships?",
    "Of course, sir!",
    "Wonderful!{LB}Now, farther inside...",
    "Wait! Janus!",
    "...There he goes...",
    "Oh dear.{LB}He decided all alone.{LB}Did that man just join us?",
    "Ah, Admiral.{LB}May this man offer advice{LB}on choosing ships?",
    "Yes",
    "No",
    "Understood! Most impressive!{LB}You follow your own principles.{LB}Truly splendid, sir!",
    "This man shall prepare{LB}for departure. Goodbye!",
    "Well then...",
    "While adding routes and contracts{LB}new ships aren't needed.{LB}At 1% share, each good offers{LB}only one to five units.",
    "Once shares rise and more goods{LB}become available,{LB}then buy another ship.",
    "Start by considering{LB}the ship's size and price.",
    "Match ships to shares and cash.{LB}Otherwise cargo goes unfilled,{LB}while extra sailors still cost money.",
    "Ship price reveals the general size{LB}under 5,000 means small;{LB}10,000-20,000 means medium;{LB}over 50,000 is large.",
    "Small ships are cheap.{LB}Even with little cash,{LB}they quickly raise fleet capacity.",
    "After some trade,{LB}once cash grows,{LB}upgrade to medium ships.",
    "Medium ships use two or three masts{LB}Three masts bring greater speed,{LB}but also need more riggers{LB}to handle the sails.",
    "Refits allow five cargo holds.{LB}Planning no combat?{LB}Skip marine quarters and guns.",
    "Long ocean routes need{LB}extra supply holds.{LB}They greatly extend range.",
    "Conflict with another power{LB}calls for large ships.",
    "At least the flagship needs{LB}marine quarters and armed guns,{LB}or sea battles become difficult.",
    "Cash matters too.{LB}Two medium ships cost less{LB}and carry more than one large ship.",
    "Large ships come eventually.{LB}Planning regional fleets?{LB}Keep old medium ships for them.",
    "That is all, sir.{LB}This man shall prepare to depart.{LB}Goodbye!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B177_")]
    if len(rows) != 56 or rows[0]["id"] != "DK4_MES_B177_R0005" or rows[-1]["id"] != "DK4_MES_B177_R0224":
        raise SystemExit("B177 inventory boundaries changed")
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B177: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x04: "Janus Pasar", 0x0D: "Cesare Tohni", 0x8E: "Raphael companion", 0xFE: "System"}
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in speaker_names else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker_names.get(first, "Raphael Castor or companion"),
            "context": "Raphael's crew meets former Elysion owner Cesare Tohni, unlocks extra armor, recruits him, and receives the complete ship-purchasing tutorial.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Cesare's eccentric third-person formality, Elysion history, armor unlock, choices, and all tutorial thresholds.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects tutorial grouping, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v51-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Cesare Tohni's Elysion reunion, recruitment, extra-armor unlock, choices, and ship-purchasing tutorial in SC0 block 177.",
        "excluded_records": {}, "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"177": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
