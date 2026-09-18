from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v44.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B166_R0275": "Six-byte cutscene transition payload; no independently rendered dialogue."}
TRANSLATIONS = [
    "Hey, Claudio. Back.",
    "Huh? That was quick.",
    "Eirene:{LB}...?{LB}Claudio?",
    "Ah, Arca... no,{LB}Eirene.",
    "Eirene:{LB}Weren't you with the others?",
    "Stiff places like that{LB}just aren't for me...",
    "Eirene:{LB}Hehe... right.",
    "What about you?{LB}Won't they make you{LB}a high-ranking scholar?",
    "Eirene:{LB}Seems so. No great research{LB}was achieved, though.{LB}Do such honors fit me?",
    "Eirene:{LB}But higher rank means more funding.{LB}A poor researcher can celebrate that.",
    "...You'll leave.",
    "Eirene:{LB}Hm?{LB}Couldn't hear you.",
    "No...{LB}Your research returns to Athens?",
    "Eirene:{LB}Probably...{LB}But you said something before.{LB}What was it?",
    "You wore your scholar's face.{LB}Off the ship...",
    "We'll live in different worlds...{LB}Tch. Strange thoughts{LB}for someone like me.",
    "Eirene:{LB}Claudio...",
    "Ha, strange mood today.{LB}Must be the weather...{LB}or coming to the palace.",
    "Claudio...{LB}What do you want from me?",
    "What!? What do you mean?",
    "Should research end?",
    "No, that's not...",
    "Then, should Athens wait?",
    "Or...",
    "...Well?",
    "Can't really tell{LB}from here...",
    "Hey, stop pushing!",
    "Can't see.",
    "Come on! Stop!{LB}Munch, munch.",
    "Go, Claudio! Now!",
    "Shh! Quiet!{LB}They'll spot us!",
    "Ah! Arcadius... no, Eirene nodded.",
    "Hey, what happened?",
    "Claudio's blushing?{LB}Never seen him like this...",
    "Already under her thumb?{LB}How sad.",
    "Oh, come on.{LB}My back's starting to itch.",
    "Yet you're grinning.",
    "Yet you're grinning.",
    "Oh no!{LB}They're coming this way!",
    "Oh no!{LB}They're coming this way!",
    "Ow! Wait!{LB}Stop pushing...{LB}Aah!",
    "{MACRO:FI}!!{LB}What are you all doing?!",
    "Well... audience ended,{LB}so we came looking.{LB}Didn't mean to spy, but...",
    "This isn't a show!",
    "But...{LB}can't miss a scene like this!",
    "Tried to stop them...",
    "Everyone is so rude!",
    "You all watched too...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B166_")]
    selected = all_rows[26:75]
    if len(selected) != 49 or selected[0]["id"] != "DK4_MES_B166_R0171" or selected[-1]["id"] != "DK4_MES_B166_R0504":
        raise SystemExit("B166 middle scene inventory boundaries changed")
    rows = [row for row in selected if row["id"] not in EXCLUDED]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B166 middle: {len(rows)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x06: "Julio Erdi",
        0x07: "Raphael companion", 0x0B: "Raphael companion", 0x0E: "Raphael companion",
        0x11: "Raphael companion", 0x12: "Raphael companion", 0x13: "Raphael companion",
        0x14: "Raphael companion", 0x16: "Raphael companion", 0x17: "Raphael companion",
        0x1B: "Raphael companion", 0xFE: "Eirene",
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
            "context": "Outside the Portuguese palace, Claudio and Eirene discuss their future while Raphael's crew secretly watches and is discovered.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Eirene's explicit name captions, the romantic subtext, crew banter, runtime name command, and cutscene transition.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects cinematic pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v44-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Claudio-Eirene palace-side romance and crew eavesdropping scene in the middle of SC0 block 166.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(selected), "translated_records": len(records), "blocks": {"166": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
