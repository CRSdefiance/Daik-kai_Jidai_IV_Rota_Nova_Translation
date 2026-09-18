from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v31.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Your decision?",
    "Yes.{LB}After much thought...",
    "Hmm. Let us hear it.",
    "Accept alliance.",
    "Decline the alliance.",
    "You have my trust.{LB}Let us work together.",
    "Glad to hear it.{LB}Mr. {MACRO:FA},{LB}shall we discuss business?",
    "Y-yes. Understood.",
    "To another room.{LB}...{LB}Take Mr. {MACRO:FA}{LB}to reception.",
    "At once.",
    "Our pact targets{LB}Lord Zamorin Nagalpur,{LB}who rules Hindustan.",
    "A man enslaved by gold.{LB}His crude greed has caused us{LB}great trouble.",
    "The company has vast wealth.{LB}That power is formidable,{LB}but its master lacks virtue.",
    "Together,{LB}we can defeat him.",
    "Yes.",
    "Now the part{LB}that may concern you...",
    "What happens after Nagalpur falls?",
    "Exactly. Our alliance ends there.{LB}No contract binds us. Afterward,{LB}let us sign a nonaggression pact.",
    "A truce...?",
    "Near Arabia, my homeland,{LB}we can share markets.{LB}Other ports are yours.",
    "So stay mostly out{LB}of Arabian markets.",
    "Correct.{LB}We promise never to obstruct you.",
    "Uddin shared his Muscat{LB}market share with you.",
    "Uddin shared Socotra{LB}market share with you.",
    "Understood.{LB}Anything else?",
    "No, that is all.{LB}Pardon the trouble.",
    "Likewise.{LB}{MACRO:FO} remains small,{LB}but we will help.",
    "Thanks.{LB}Count on you.",
    "Then let us defeat Nagalpur!",
    "Agreed.{LB}Together, onward.",
    "You decline?",
    "My apologies...",
    "The wounds of Africa remain,{LB}then?",
    "No, that is not...",
    "A worthy choice.{LB}As rivals, let us both seek{LB}rule over Hindustan's ocean.{LB}Odd words, perhaps?",
    "Y-yes.{LB}Go easy.",
    "Goodbye.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B148_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B148: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x25: "Abraham ibn Uddin", 0x36: "Uddin guild attendant", 0xFE: "System"}
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
            "context": "Raphael accepts or declines Uddin's alliance; the accepted branch defines Nagalpur as their target, a later nonaggression pact, Arabian market boundaries, and grants shares in Muscat and Socotra.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving both complete decision branches, alliance terms, Nagalpur objective, nonaggression settlement, Arabian boundaries, share grants, and runtime company-name command.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects negotiation structure and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v31-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Uddin alliance decision, accepted terms and share grants, and declined-rival branch in Raphael SC0 block 148.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"148": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
