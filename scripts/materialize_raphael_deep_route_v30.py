from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v30.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "W-wow... Amazing...!",
    "Pardon the surprise,{LB}{MACRO:FI}... no,{LB}leader of {MACRO:FO}.",
    "Uddin...{LB}No, Commander...",
    "Let us get to the matter.",
    "Y-yes.",
    "An alliance with us?",
    "Pact?",
    "Your suspicion is fair.{LB}This request is sudden and rude.{LB}That much is understood.",
    "An alliance is a serious matter.{LB}No easy choice, surely...",
    "Your suspicion is fair.{LB}This man knows what happened{LB}to you in Africa.",
    "Your caution is understood.{LB}Yet this man still asks.",
    "No answer is needed tonight.{LB}Think it over. Rooms are ready.{LB}That is all. Go and rest.",
    "This way.",
    "Thanks...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B147_")]
    controls = {"DK4_MES_B147_R0078": "Raw overnight-scene transition control; preserved byte-for-byte."}
    visible = [row for row in rows if row["id"] not in controls]
    if len(visible) != len(TRANSLATIONS):
        raise SystemExit(f"B147: {len(visible)} visible rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x25: "Abraham ibn Uddin", 0x36: "Uddin guild attendant"}
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
            "context": "At Basra's guild, Uddin formally proposes an alliance, acknowledges Raphael's justified caution after Africa, and gives him a night to decide.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Uddin's formal third-person voice, the complete alliance proposal, Africa reference, overnight delay, and FI/FO runtime identity commands.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects formal pacing and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v30-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Uddin alliance proposal and overnight deliberation setup in Raphael SC0 block 147.",
        "excluded_records": controls,
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"147": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(controls)} control excluded")


if __name__ == "__main__":
    main()
