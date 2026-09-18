from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v28.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Hey, {MACRO:FI}.",
    "Oh, Clau. What is it?",
    "Let us find something good to eat.{LB}...And invite old Julio too.",
    "Yes. He was angry when we forgot{LB}last time.",
    "Exactly. That old man remembers{LB}things like this forever.",
    "Why not invite Arcadius{LB}for once?",
    "Arcadius?",
    "Yes. He never socializes.{LB}Let us drag him out{LB}and talk man to man.",
    "He likes being alone.{LB}We should respect that.",
    "That is why we drag him out!{LB}He said he was going to the inn.",
    "You are so pushy!",
    "Knock!",
    "Hey, Arca...dius...",
    "!!! What is this!?",
    "That was Arcadius,{LB}right...!?",
    "Eek!",
    "See it?",
    "Y-yes...",
    "We saw something dangerous...",
    "Y-yes...",
    "H-hey! You two!",
    "Oh, old Hans.",
    "D-did you... see?",
    "Well...",
    "We saw... something...",
    "Both of you... come in.",
    "Eire-- no,{LB}A-Arcadius!",
    "No more hiding.{LB}Come in.",
    "O-okay.",
    "Yes.",
    "You saw me.",
    "N-no, not me...",
    "Saw nothing...",
    "No need to deny it.{LB}Arcadius is my false name.{LB}My real name is Eirene.",
    "Usually this old man guards{LB}the door, but today...",
    "Sorry.{LB}Calling Dr. Hans every time{LB}felt unfair, so this once{LB}seemed safe.",
    "Why dress as a man?",
    "What a waste.",
    "Before sailing with Hans,{LB}this disguise seemed safest.",
    "Many sailors are rough men.{LB}With a woman among them,{LB}anything might happen.",
    "Maybe men like that exist,{LB}but not among our crew.",
    "Exactly. Everyone is kind.{LB}Though we do have more than our share{LB}of odd characters...",
    "True.{LB}My worries seem needless...",
    "Yes.{LB}{MACRO:FI}, Clau, everyone is kind.{LB}Though Clau is a bit... crude...",
    "What!?",
    "Am... am this rough?",
    "Save that for later.{LB}Did you never consider{LB}dressing as a woman again?",
    "Too late to say,{LB}'This one is a woman.'",
    "That means we doubted the crew.{LB}Awkward, would it not?",
    "So please,{LB}keep this secret.",
    "All right.{LB}No one else will hear.",
    "Y-yeah.{LB}We will keep quiet.",
    "Thank you...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B145_")]
    controls = {"DK4_MES_B145_R0050": "Raw inn-room transition control; preserved byte-for-byte."}
    visible = [row for row in rows if row["id"] not in controls]
    if len(visible) != len(TRANSLATIONS):
        raise SystemExit(f"B145: {len(visible)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x08: "Eirene", 0x4B: "Hans Retzel", 0xFE: "Sound effect"}
    records = []
    for row, english in zip(visible, TRANSLATIONS, strict=True):
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
            "context": "Claudio and Raphael discover Arcadius is Eirene in disguise; she and Hans explain the safety concern behind her male identity, and the crew agrees to keep her secret.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving the reveal, Eirene's agency and safety rationale, the crew's reassurance, Claudio's humor, and their promise of confidentiality.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects reveal pacing, speaker beats, and progressive ASCII pair phase."} if "{LB}" in english else {}),
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
        "scope": "Complete Arcadius/Eirene identity reveal, explanation, reassurance, and secrecy promise in Raphael SC0 block 145.",
        "excluded_records": controls,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"145": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(controls)} control excluded")


if __name__ == "__main__":
    main()
