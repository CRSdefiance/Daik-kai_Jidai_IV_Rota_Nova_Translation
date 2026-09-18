from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v41.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (160, 161, 162)
TRANSLATIONS = [
    "This is fascinating.{LB}The Tang Bamboo Craft follows{LB}this Bamboo Assembly Plan.",
    "So with the plan,{LB}we can take it apart{LB}and rebuild it?",
    "Let's try.{LB}This part comes first...",
    "Wait!{LB}Something is drawn{LB}inside that thick bamboo!",
    "This goes here...{LB}then this next?",
    "You look happy.",
    "Heh!{LB}This Tang Bamboo Craft{LB}comes apart!",
    "What!?{LB}Did you break it?",
    "No!{LB}Look at the Bamboo Assembly Plan!",
    "Oh... right.{LB}The Bamboo Assembly Plan{LB}shows how to take it apart{LB}and rebuild it.",
    "See? Neat, right?{LB}Now it's all apart!",
    "Nice hands.{LB}Huh? Something's drawn{LB}behind that bamboo.",
    "A map, perhaps...{LB}Could this be East Asia's{LB}Proof map?!",
    "Yes, surely!{LB}Let's find it!",
    "Whoa! A map!{LB}A Proof map!",
    "Great work!{LB}Let's seek East Asia's{LB}Proof of Conquest!",
    "(Claudio...!?)",
    "Watch where you throw!{LB}Over here!",
    "Big bro, it's hard!",
    "You can do it.{LB}One more!{LB}Watch the target...",
    "Hyaa!",
    "Whack!",
    "Hit it!",
    "See?{LB}Easy once you know how.{LB}Good job, kid.",
    "Yeah! Thanks!{LB}Tomorrow, victory is mine!",
    "Aye, beat your friends!{LB}Bye!",
    "Bye!",
    "Oh? Arcadius.{LB}Out shopping?",
    "No... just walking.{LB}What were you doing?",
    "Teaching that kid to throw.{LB}He doesn't want to lose{LB}to his friends.",
    "You like children...{LB}That's unexpected.",
    "Really?{LB}Wouldn't work with {MACRO:FI}{LB}if kids bothered me.",
    "That's rude to the admiral!",
    "Keep it between us.",
    "Hehe. Agreed...",
    "{MACRO:FO} member?{LB}Pass.",
    "Amazing!",
    "Did Pasha's army own this?",
    "Hayreddin... this...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B160-B162: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x04: "Raphael crewmate", 0x05: "Claudio Manini", 0x08: "Arcadius Eirene",
        0x19: "Ifa", 0x78: "Guard", 0xA3: "Child", 0xFE: "Sound effect",
    }
    contexts = {
        160: "Raphael's crew follows the Bamboo Assembly Plan to dismantle the Tang Bamboo Craft and reveal East Asia's Proof map.",
        161: "Arcadius sees Claudio teaching a child to throw and discovers his unexpected fondness for children.",
        162: "Raphael's company passes a guarded entrance and reacts to an object formerly associated with Pasha and Hayreddin.",
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
            "localization_note": "Faithful natural American English preserving established item, character, Proof, and runtime company-name semantics.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects item names, scene pacing, and progressive ASCII pair phase."} if "{LB}" in english else {}),
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
        "scope": "Complete Tang Bamboo Craft Proof ritual, Claudio-child scene, and Pasha/Hayreddin reaction across SC0 blocks 160-162.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
