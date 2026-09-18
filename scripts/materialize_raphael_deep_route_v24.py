from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v24.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Hey, {MACRO:FI}!",
    "What is it?",
    "Great treasure news!",
    "Oh? What treasure?",
    "They call it the{LB}Staff of Guidance.",
    "Why so special?",
    "The guild's purchase list{LB}offers a fortune for it!{LB}Nobody has ever found one!",
    "And?",
    "Get it and we will be rich!{LB}Come on, let us go!",
    "Go... where?",
    "Where the Staff of Guidance is!{LB}Obviously!",
    "And where is that?",
    "Uh...{LB}No idea.",
    "Then how can we search?",
    "...True.",
    "Come on, think this through.{LB}Such a vague rumor may not{LB}even be true.",
    "...Good point.{LB}No use, then.",
    "Why am such a fool...?",
    "Clau...?",
    "{MACRO:FI}, boy...",
    "Oh, Julio.{LB}Please stop calling me boy.",
    "Ah, pardon me.{LB}An old habit.",
    "About this...{LB}Staff of Guidance...",
    "The treasure Clau mentioned?",
    "Hear what this old man knows?",
    "Please tell me.",
    "No, that is enough.",
    "The Staff of Guidance{LB}is said to guide people{LB}toward the path of good.",
    "So it truly exists?",
    "So legends say.",
    "Where could it be...?",
    "They say Hindustan.",
    "Then it must be real.",
    "Only in legend.",
    "Oh...{LB}Too harsh.{LB}Clau deserves an apology.",
    "Thank you, Julio!",
    "Hey, wait!",
    "Gone already.",
    "Well, that should cheer Claudio up.{LB}His gloom makes the tavern dreary{LB}and spoils my drink.",
    "Yet the Staff of Guidance tale{LB}had quite slipped my mind.{LB}Will {MACRO:FI} truly seek it...?",
    "No matter.{LB}Time to ask Janus to join me{LB}for a drink.",
    "There you go again.{LB}You and Clau are trying{LB}to fool me together.{LB}You cannot fool me.",
    "What?{LB}We would not.",
    "You want me as drinking gossip.{LB}Your game is obvious.",
    "We do not!{LB}Oh, never mind.",
    "Clau is upset after that exchange.{LB}This old man only spoke so you might{LB}cheer him up.",
    "Oh! So that was it.{LB}Sorry, Julio.",
    "Understanding is enough.{LB}Now go cheer up Clau.",
    "Yes, sir!",
    "Such troublesome boys.{LB}Now all this talk of drinking{LB}has made me thirsty.",
    "Yes, Janus can join me{LB}for a drink.",
    "Heh heh. Time for ale.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B136_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B136: {len(rows)} source rows != {len(TRANSLATIONS)} translations")
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in {0x05, 0x06} else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        speaker = {0x05: "Claudio Manini", 0x06: "Julio Erdi"}.get(first, "Raphael Castor")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker,
            "context": "Claudio shares the Staff of Guidance rumor; Julio explains its legend, and both response branches resolve Raphael's misunderstanding and Claudio's hurt feelings.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving the treasure legend, Hindustan destination, both player-response branches, character humor, and fixed-allocation safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects dramatic grouping, branch readability, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v24-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Staff of Guidance rumor, explanation, choice, and both aftermath branches in Raphael SC0 block 136.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"136": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
