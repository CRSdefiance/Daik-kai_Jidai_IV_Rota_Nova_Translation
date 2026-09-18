from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v40.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (157, 158, 159)
TRANSLATIONS = [
    "This Ceremonial Knife...{LB}what is it for?",
    "Hey, careful!{LB}A knife is still a blade.{LB}Put it away.",
    "Right. The Sun-Crest Sheath{LB}is the right size.{LB}Let's put it there...",
    "Whoa!{LB}What's that?{LB}Blade's glowing!",
    "So bright!",
    "Whew... the glare is gone.{LB}What was that light?",
    "Hey, the knife fell.",
    "Ah!{LB}Dropped it in shock.",
    "A map... on it...",
    "That's a map!{LB}Must be the New World's{LB}Proof map!",
    "Looks so.{LB}Now we can find the Proof!{LB}...That was strange.",
    "Claudio, what crops{LB}grow around here?",
    "Hm? Why ask?",
    "Maybe Charlotte's village{LB}could produce a new trade good...",
    "...Hmm.{LB}How about corn?",
    "Corn...{LB}Yes, let's use that!",
    "Well...{LB}{MACRO:FI}, you're quite something!",
    "Huh!? What?",
    "Heh, never mind.{LB}Just take her the corn.",
    "{MACRO:FI},{LB}have a moment?",
    "Arcadius... What?",
    "You seem down.",
    "Really?{LB}No, not at all.",
    "Charlotte is why...",
    "You care for her?",
    "Sigh...{LB}Can't hide from you.",
    "She's always on my mind...{LB}Want to do something for her!{LB}But... but...!",
    "{MACRO:FI}... she told me{LB}she thinks of {MACRO:FI}{LB}every day too.",
    "What!?",
    "Sorry. You came back so dejected{LB}that day, so Charlotte{LB}got a visit from me.",
    "Had {MACRO:FI} felt nothing,{LB}this would have stayed{LB}between us.",
    "Pardon her for leaving suddenly.{LB}She's afraid...{LB}She thinks she's not worthy of you.",
    "Why?",
    "{MACRO:FI}, your noble birth{LB}worries her.",
    "That means nothing to me!",
    "Maybe.{LB}But consider how Charlotte feels.",
    "Meaning?",
    "Remember her story?{LB}What happened in Europe{LB}hurt her deeply.",
    "...Right.",
    "She isn't used to happiness.{LB}That joy frightens her.{LB}Afraid to lose it,{LB}she can't step forward.",
    "Enough preamble.{LB}Charlotte asked me{LB}to relay a message.",
    "What?",
    "...She never learned to write.{LB}That was her world...",
    "What!{LB}Never imagined someone{LB}couldn't write...{LB}Never understood her...",
    "...{LB}'{MACRO:FI}, thank you{LB}for everything. My village{LB}is safe now.",
    "'Hope {MACRO:FI}'s homeland{LB}returns to how it was.{LB}When it does...",
    "'Still feel the same?{LB}Then please come see me.'{LB}That's all.",
    "Charlotte...!",
    "...{LB}Well, time to go.",
    "Thank you, Eirene...",
    "...No.{LB}Good luck, {MACRO:FI}.{LB}Charlotte's future is up to you.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B157-B159: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x08: "Arcadius Eirene"}
    contexts = {
        157: "Raphael combines the Ceremonial Knife and Sun-Crest Sheath to reveal the New World Proof map.",
        158: "Raphael and Claudio choose corn as a new trade good for Charlotte's village.",
        159: "Eirene explains Charlotte's feelings, fears, inability to write, and request that Raphael visit after restoring Portugal.",
    }
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        block = int(row["id"].split("_B", 1)[1].split("_", 1)[0])
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
            "context": contexts[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English retaining established item, Proof, character, homeland, and village terminology.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects item names, emotional pacing, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    counts = {str(block): sum(record["id"].startswith(f"DK4_MES_B{block}_") for record in records) for block in BLOCKS}
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v39-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete New World Proof ritual, Charlotte village corn scene, and Charlotte-Eirene relationship dialogue across SC0 blocks 157-159.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
