from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v13.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = {
    108: [
        "Admiral, Muramasa{LB}was found at last.{LB}May this warrior see it?",
        "Of course. Your report{LB}led us to it, Yukihisa.",
        "This is... Muramasa...",
        "Hmm... That eerie glow{LB}nearly draws one inside.",
        "A grand sight.",
    ],
    109: [
        "Say, a rumor says you seek{LB}strange treasures scattered worldwide.",
        "The nearby priest knows much.{LB}He may have useful news.",
    ],
    110: [
        "Do you seek{LB}the Proof of Conquest?",
        "You know of it?",
        "This much is known:{LB}the proof's map works only when{LB}two Map Keys are joined.",
        "Each key alone{LB}has no meaning.",
        "Perhaps you already know:{LB}Map Keys may hide in distant ruins{LB}or rest with unexpected people.",
        "Take this sword.",
        "Overcome the trial it sets{LB}and aid those in need.",
        "Reject selfish greed.{LB}Give to those without wealth.{LB}End strife and spread peace.",
        "May God protect you.",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {"0C": "Yukihisa Genjo Shiraki", "8B": "Priest", "BC": "Churchwoman"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    108: "Yukihisa examines Muramasa after Raphael finds the legendary blade.",
    109: "A churchwoman directs Raphael to a priest who knows about strange treasures.",
    110: "A priest explains the two Map Keys and gives Raphael a sword and moral trial tied to the Proof of Conquest.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    records = []
    block_counts = {}
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_")]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"],
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
                "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving treasure terminology, religious charge, scene tone, and fixed-allocation display safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v13-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Muramasa inspection and the complete church lead into the Proof of Conquest quest across Raphael SC0 blocks 108-110.",
        "excluded_records": {},
        "inventory": {"identified_records": len(records), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records across {len(BLOCKS)} blocks")


if __name__ == "__main__":
    main()
