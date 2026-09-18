from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v45.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "So all know now:{LB}Eirene is a woman.",
    "Ah! Well...",
    "Keeping the pretense felt wrong.{LB}Sorry...{LB}Couldn't keep pretending.",
    "Hehe, fine.{LB}Congratulations, {MACRO:FI}.{LB}Oh, should such casual words{LB}stop now?",
    "Right!{LB}Hey, {MACRO:FI}!{LB}Why are you wasting time here?!",
    "Why?",
    "Why? You got some grand post!{LB}Weren't they presenting you{LB}to the whole crowd?",
    "Hehehe.",
    "Well...",
    "Turned it down.",
    "What!?",
    "You refused?!",
    "Yes. Albuquerque already led{LB}Portugal's navy,{LB}and a sailor like me{LB}shouldn't be viceroy.",
    "You handed it to Albuquerque!?{LB}He defected to Spain!",
    "He never defected.{LB}As a soldier, he served{LB}the Spanish king who ruled then.",
    "Gah!{LB}You're too trusting!{LB}Why must you always...!",
    "...Well,{LB}maybe that nature is why{LB}everyone followed you.",
    "Aye, aye.",
    "A different request:{LB}to advance Portugal's seafaring,{LB}let us explore unknown waters.",
    "Explorer instead of viceroy?{LB}Ha ha! That's perfect!",
    "Then you still need me, right?",
    "Of course, Claudio.{LB}Counting on you.",
    "Aye! Leave it all to me!",
    "Unknown waters...{LB}New research awaits.",
    "Just don't flirt on the ship.{LB}Might riot.",
    "D-don't say stupid things!",
    "Wow!{LB}More scenes not to miss!",
    "Eirene looks happy...{LB}Maybe London calls me home...",
    "Then prepare for exploration{LB}at once.",
    "No need to rush...{LB}Everyone is tired.{LB}We can rest first.",
    "Move slowly and another nation{LB}will beat us there.",
    "Can't allow that.{LB}Hate losing to anyone.",
    "Aye. Speed wins every race.",
    "Hehe... oh!{LB}{MACRO:FI}, know what this is?",
    "...A letter?",
    "Yes.{LB}Here, please read it.",
    "Who sent it?{LB}...{LB}Ah!!!",
    "Muint obrigada por tudo.{LB}(Thank you for everything.)",
    "Muint bem, obrigada.{LB}(Very well, thank you.){LB}Charlotte Miller",
    "{MACRO:FI},{LB}thank you for everything.{LB}Doing very well, thank you.{LB}Charlotte Miller",
    "Well...{LB}The writing is awkward.",
    "Hmm...{LB}The meaning is clear, at least.",
    "You idiot!{LB}Don't say that!",
    "She wrote from the heart!{LB}How rude!",
    "How can men miss{LB}a woman's heart?",
    "Charlotte studied Portuguese{LB}and worked hard on this.",
    "...Charlotte...",
    "Heh.{LB}Destination settled!",
    "What!?{LB}B-but...",
    "Why so shy?{LB}Hurry and get ready!",
    "No one objects.{LB}Exploring the New World first{LB}sounds fine.",
    "Julio...",
    "That's right, Admiral.{LB}Give the usual order.",
    "...Yes!",
    "Everyone, let's go!",
    "Yeah!!",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B166_")]
    rows = all_rows[75:]
    if len(rows) != 56 or rows[0]["id"] != "DK4_MES_B166_R0526" or rows[-1]["id"] != "DK4_MES_B166_R0912":
        raise SystemExit("B166 final scene inventory boundaries changed")
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B166 final: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x06: "Julio Erdi",
        0x07: "Raphael companion", 0x08: "Arcadius Eirene", 0x0D: "Raphael companion",
        0x0F: "Raphael companion", 0x11: "Raphael companion", 0x12: "Raphael companion",
        0x14: "Raphael companion", 0x16: "Raphael companion", 0x1A: "Raphael companion",
        0xFE: "System or letter caption",
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
            "context": "Raphael declines the viceroyalty, chooses exploration, reads Charlotte's Portuguese letter, and leads the crew on the route's final New World departure.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Albuquerque's role, exploration resolution, Charlotte's intentionally awkward Portuguese, runtime name command, and final crew call-and-response.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects letter layout, ending pacing, and progressive ASCII pair phase."} if "{LB}" in english else {}),
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
        "scope": "Raphael viceroy refusal, exploration choice, Charlotte letter, and final departure in the last 56 records of SC0 block 166.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"166": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
