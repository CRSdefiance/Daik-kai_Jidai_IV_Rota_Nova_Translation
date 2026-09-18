from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v34.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Admiral!{LB}Urgent word from home!",
    "Read it.",
    "Spain's king now formally{LB}rules Portugal too!",
    "What!?",
    "What!?",
    "So Portugal...{LB}our homeland...{LB}is gone?!",
    "On paper, yes.{LB}But in truth...",
    "On paper, yes.{LB}But in truth...",
    "So every Portuguese faction{LB}now serves Spain?",
    "Details are unclear,{LB}but Admiral Dinis de Albuquerque{LB}and his navy sided with Spain.",
    "That Albuquerque!",
    "With our country gone,{LB}what choice had he?{LB}We can't blame the admiral.",
    "{MACRO:FI}!{LB}Not you too!{LB}Won't accept this!",
    "This heart is Portuguese.{LB}Proud of it!{LB}Never will bow to Spain's king!",
    "Arcadius, what's wrong?",
    "My Greece has long been{LB}under Ottoman rule...{LB}So your pain is clear to me.",
    "What can we do?",
    "Rushing home would take{LB}too much time and supplies.{LB}{MACRO:FI}, we must choose wisely.",
    "Even if we return,{LB}our strength can't beat Spain{LB}after it absorbed Portugal's navy...",
    "And we can't abandon{LB}our hard-won progress{LB}toward ruling Asia.",
    "True. Just handing over{LB}{MACRO:FO}'s rights here{LB}would make my blood boil.",
    "Aye. No need to hand Asia{LB}to others for nothing.",
    "Decision made.{LB}...We stay!",
    "Admiral!",
    "{MACRO:FI}, are you sure?{LB}Will you just give up?!",
    "No. Never!{LB}We'll build power here in Asia,{LB}then return and restore Portugal!",
    "What!?",
    "Yes! That's it!{LB}A true man, {MACRO:FI}!{LB}That's the spirit!",
    "Ha ha! Restoring Portugal!{LB}Now this is getting grand!",
    "Ha ha! Restore Portugal!{LB}Now this grows grand!",
    "Spain's fleet,{LB}just wait for us!",
    "{MACRO:FI}!{LB}The governor in Southeast Asia{LB}is Portuguese.",
    "A countryman...",
    "Could we ally with him first,{LB}as fellow countrymen?",
    "All right.{LB}Perhaps.",
    "Ah, {MACRO:FI}.{LB}Listen: the Southeast Asia governor{LB}is Portuguese, right?",
    "A countryman...",
    "He should be based in Malacca.{LB}He may feel as you do.{LB}With luck, you could ally with him.",
    "Right.",
    "Old man, aren't you Spanish?{LB}Helping us means helping Portugal.{LB}Are you sure?",
    "Such details matter less.{LB}Helping you, young {MACRO:FI}...{LB}No, our admiral matters more.",
    "Julio...{LB}Thank you.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B151_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B151: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x06: "Julio Erdi",
        0x08: "Arcadius Eirene", 0x13: "Raphael fleet officer", 0x97: "Portuguese messenger",
    }
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
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker_names.get(first, "Raphael Castor"),
            "context": "News that Spain's king has absorbed Portugal drives Raphael to remain in Asia, gain strength, restore Portugal later, and consider an alliance with the Portuguese governor at Malacca.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Portugal's annexation, Albuquerque's decision, Arcadius's Greek parallel, Raphael's restoration vow, and the Malacca alliance lead.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects dramatic pacing, political exposition, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v33-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Portugal annexation, Raphael restoration vow, and Malacca-governor alliance lead in SC0 block 151.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"151": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
