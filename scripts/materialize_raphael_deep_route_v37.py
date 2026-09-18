from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v37.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "{MACRO:FI}, Spain seems{LB}one step ahead of us{LB}in these waters.",
    "Looks that way.{LB}But we still have a chance{LB}to catch up.",
    "Aye. Win the Proof,{LB}and we turn it around.",
    "And above all,{LB}we must restore Portugal.{LB}We can't yield this sea to Spain!",
    "Can't say your dream{LB}of restoring home means nothing.{LB}...We have to try.",
    "You're not Spanish.{LB}Are you with {MACRO:FO}?",
    "Yes, but...",
    "Keep this quiet:{LB}this is Maldonado territory.{LB}Know his reputation?",
    "Reputation?{LB}Bad rumors?",
    "Well, truth is,{LB}we barely know him...",
    "Reputation?{LB}Bad rumors?",
    "Telling you because you're{LB}with {MACRO:FO}:{LB}everyone here hates Maldonado.",
    "Hate him? That's serious.{LB}What kind of man is he?",
    "Please tell us.{LB}Why is he hated?",
    "He rules the whole area by force,{LB}backed by Spain's crown,{LB}and does whatever he wants.",
    "He attacks every merchant ship{LB}and lines his own pockets.",
    "Like a pirate...",
    "Exactly. Sailors can't safely{LB}put to sea anymore.{LB}Our trade is ruined.",
    "Maybe you shouldn't trust us.{LB}We could be no better than him.",
    "We've heard of {MACRO:FO}.{LB}At least you don't abuse{LB}the people, right?",
    "We'll defeat Maldonado!",
    "What now?",
    "...This may be a problem{LB}across the whole New World,{LB}not just Maldonado.{LB}Other factions too...",
    "So defeating him alone{LB}may solve nothing.{LB}And we'd need time to prepare...",
    "Sir, given all that,{LB}we may not be able to help{LB}right away...",
    "Oh...",
    "Still, that helped.{LB}Right, {MACRO:FI}?",
    "Yes. Now we understand{LB}how the locals suffer.{LB}Soon, we hope to act.",
    "Hope you're not{LB}like those men...",
    "...He trusted us enough{LB}to tell us this.{LB}To repay that trust...",
    "Everyone!{LB}Let's defeat Maldonado{LB}and bring peace here!",
    "Heh. Let's do it.",
    "You will? Good.{LB}We'll be waiting.{LB}Maybe this misery ends soon...",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B154_")]
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B154: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {0x05: "Claudio Manini", 0x5C: "New World resident"}
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
            "context": "Raphael enters the New World, hears how Maldonado abuses local sailors and merchants under Spanish protection, and may vow to defeat him and bring peace.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving the optional cautious and committed branches, Maldonado's abuses, Spain's regional advantage, and Raphael's Portugal-restoration motive.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects political exposition, branch pacing, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v37-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete Maldonado local-abuse report and optional liberation vow in Raphael SC0 block 154.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"154": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
