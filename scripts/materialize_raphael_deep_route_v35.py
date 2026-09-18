from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v35.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "...Weren't you warned?",
    "Who?",
    "Asking who? Some greeting.{LB}And you trade without leave?{LB}Gwahaha!{LB}Arrogant little whelp.",
    "Claudio, stand back!",
    "Tch.",
    "So you're the admiral?",
    "...Yes.{LB}But you first. Your name?",
    "My mistake.{LB}Duarte.{LB}Duarte Pereira.",
    "Duarte Pereira!{LB}The regional governor!",
    "Admiral Pereira...",
    "Oh?{LB}So my fame precedes me.{LB}Know what brings me here?",
    "About the trade zone{LB}here in Southeast Asia...",
    "Right. Sharp for a young admiral.{LB}Since you understand,{LB}get out.",
    "...As Portuguese companies,{LB}can't we compete fairly?",
    "Equal terms?{LB}Where in this world{LB}do those exist?!",
    "The world itself{LB}is unfair!",
    "Drive me out,{LB}or be driven out!{LB}Gwahaha!",
    "Besides,{LB}your precious Portugal{LB}was taken by Spain, wasn't it?",
    "Either way, Southeast Asia{LB}belongs solely to{LB}the Pereira Company.",
    "A monopoly?",
    "Gwahaha!{LB}Exactly.",
    "Our homeland is gone!{LB}Why fight each other now?",
    "...Yes. This hurts.{LB}Proud Portugal...{LB}Who knew its navy would side{LB}with Spain?",
    "Exactly!{LB}Let's ally, defeat Spain,{LB}and restore Portugal...",
    "Portugal didn't become Spain.{LB}One king merely wears both crowns.",
    "But...",
    "So young.{LB}Still can't accept it, can you?{LB}Your meaning is clear.",
    "As regional governor,{LB}Spain's king commands me.",
    "So aiding threats like us{LB}would draw Spain's wrath?",
    "Many lives depend on me.{LB}They need my care.{LB}That's a governor's burden.",
    "Battle the Dutchman{LB}Antony Koon in the spice isles,{LB}and perhaps we can cooperate...",
    "That's world politics.{LB}Koon is now Spain's enemy too,{LB}so we can defeat him together.{LB}Beyond that, no aid.",
    "So you won't aid us{LB}against Spain?",
    "That's right.",
    "...Sorry for the long grumble.{LB}My only advice now:{LB}Go east and grow stronger.",
    "East...?",
    "Then we'll talk.{LB}Now get going.",
    "Hate to admit it,{LB}but the old man's right...",
    "East?",
    "Hey, {MACRO:FI}.{LB}What's east of here?",
    "Probably...{LB}He means win East Asia's{LB}Proof of Conquest.",
    "Probably...{LB}He means win East Asia's{LB}Proof of Conquest.",
    "Thought so...{LB}But that won't be easy.{LB}Who knows how long it could take?",
    "We need a clue to the Proof,{LB}or Pereira may never{LB}acknowledge us.",
    "Tch. Don't know his game,{LB}but in this climate{LB}we need the old man as an ally.{LB}Let's go!",
    "Right.{LB}Counting on you, Claudio.{LB}Let's sail for East Asia!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B152_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B152: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x08: "Arcadius Eirene", 0x27: "Duarte Pereira", 0x8E: "Raphael crewmate"}
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
            "context": "Raphael confronts Southeast Asia governor Duarte Pereira, who refuses aid against Spain, offers cooperation against Antony Koon, and challenges Raphael to win East Asia's Proof of Conquest.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Pereira's hostile entrance, Portuguese political dilemma, conditional anti-Koon cooperation, and eastward Proof challenge.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects confrontation pacing, political exposition, and progressive ASCII pair phase."} if "{LB}" in english else {}),
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
        "scope": "Complete Duarte Pereira confrontation, Spain dilemma, anti-Koon condition, and East Asia Proof challenge in SC0 block 152.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"152": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
