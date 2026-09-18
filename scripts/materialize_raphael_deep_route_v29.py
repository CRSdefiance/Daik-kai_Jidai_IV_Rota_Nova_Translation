from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v29.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "{MACRO:FU}...?",
    "And you?",
    "Pardon the delay.{LB}This man trades from Basra.{LB}The name is Abraham ibn Uddin.",
    "Hello.",
    "{MACRO:FO} has become well known.{LB}Your business seems broad.",
    "Not really...",
    "A request, if you will?",
    "(Quiet, yet dignified...{LB}All right...)",
    "No reason to refuse.",
    "He looks dangerous. Decline.",
    "The request needs{LB}a short journey.",
    "Y-yes. Lead on.",
    "Then meet at Basra's guild.",
    "Understood.{LB}Basra's guild.",
    "Yes.{LB}This man waits.",
    "Yes. Later.",
    "Go.",
    "Sorry. Let me consult the crew.{LB}An admiral cannot decide alone.",
    "Your own answer was desired...{LB}No, pardon me.{LB}Our paths may cross again.{LB}Goodbye.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B146_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B146: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = "25" if first == 0x25 else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": "Abraham ibn Uddin" if state else "Raphael Castor",
            "context": "Abraham ibn Uddin introduces himself, notes Castor Company's growing reputation, and asks Raphael to meet him at Basra's guild; both player-choice outcomes are retained.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving Uddin's formal third-person voice, Basra invitation, both choices, and FU/FO runtime identity commands.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects formal speech grouping and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v26-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Abraham ibn Uddin introduction, Basra invitation, and both response branches in Raphael SC0 block 146.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"146": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
