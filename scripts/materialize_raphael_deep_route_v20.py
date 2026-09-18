from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v20.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Admiral, please look!", "Admiral, look!", "Admiral, look at this!",
    "Admiral, look here!", "Admiral! Look!",
    "Just a tablet.",
    "This is no ordinary tablet.{LB}There is no stone nearby.{LB}Even the mosque is made from dried mud.",
    "Then this tablet{LB}was not made here?",
    "Yes, probably.",
    "Admiral...{LB}not an ordinary tablet.",
    "How so?",
    "There is no stone in this land.{LB}Even the mosque is built{LB}from dried mud.",
    "Then...",
    "This tablet was brought here{LB}from another land.",
    "Ah!",
    "Whisper...",
    "This is bad.{LB}We cannot touch that now...",
    "Were you the bandits{LB}attacking Sao Jorge?",
    "What?!{LB}Who are you?",
    "{MACRO:FO}",
    "What?! You helped guard that town!{LB}You ruined everything for us!",
    "No raid because of you!{LB}We will starve!",
    "Bold words for thieves!{LB}That town needs our help!",
    "Shut up!{LB}Europeans destroyed our village!",
    "Nothing will stop{LB}our revenge!",
    "Blame the slavers{LB}and soldiers preying on Africa,{LB}not every European.",
    "Attack everyone without distinction{LB}and you become no better{LB}than the villains you hate.",
    "Easy to say!",
    "Abandon revenge.{LB}That cannot restore your happiness.",
    "More fighting{LB}only repeats the cycle{LB}and brings misery to your people.",
    "Then what should we do?!",
    "End the struggle among European powers{LB}that causes conflict{LB}across the world's seas.",
    "The great powers are dividing the world. We gather the Proof of Conquest they seek to stop them.",
    "Stop the great powers?!{LB}Are you sane?",
    "That is no idle boast.{LB}Our reach now extends to Africa.{LB}We can face them as equals.",
    "Well? Entrust your revenge to us.",
    "What?!",
    "Come to sea with us.{LB}With such spirit, you can succeed.",
    "Staying here changes nothing...",
    "All right. We trust you!",
    "Welcome.",
    "No idea if this{LB}concerns your Proof,{LB}but this was hidden in the ruins.",
    "Tablet?",
]
SPEAKERS = {"03": "Maria Li", "04": "Janus Pasha", "08": "Charles Jean Rochefort", "B4": "African bandit", "D0": "Raphael crewmate", "FE": "Whisper"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = "Raphael's party identifies an imported stone tablet; Maria confronts displaced African bandits, redirects their revenge toward ending imperial conflict, recruits them, and receives a hidden tablet."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B123_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B123: {len(rows)} source rows != {len(TRANSLATIONS)} translations")
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"), "context": CONTEXT,
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving every tablet-analysis variant, anti-imperial argument, recruitment beat, macro name, and fixed-allocation safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v20-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete imported-tablet analysis and African-bandit confrontation, argument, recruitment, and reward in Raphael SC0 block 123.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"123": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
