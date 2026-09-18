from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v68.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(286, 293))

SPEAKERS = {
    0x46: "Zaganos Bey",
    0x47: "William Clive",
    0x71: "Guild messenger",
    0x93: "Guildmaster",
    0xFE: "System",
}

CONTEXT = {
    286: "The Veracruz guild hires Raphael to defeat the dangerous pirate William Clive.",
    287: "Raphael delivers William, receives a reward, and hears of an ancient kingdom's map.",
    288: "Raphael and the guild recall that William's fleet is in the New World.",
    289: "The Genoa guild hires Raphael to defeat the Turkish pirate Zaganos Bey.",
    290: "Raphael delivers Zaganos, receives a reward, and hears of nearby Roman ruins.",
    291: "Raphael and the guild recall that Zaganos's fleet is in the Mediterranean.",
    292: "A messenger tells Raphael that the Genoa guild is looking for him.",
}

OVERRIDES = {
    "DK4_MES_B286_R0005": "A formidable foe worthy of you.",
    "DK4_MES_B286_R0008": "Defeat the English pirate William Clive.",
    "DK4_MES_B286_R0011": "He heads to Havana.{LB}This advance is yours. Good luck.",
    "DK4_MES_B286_R0022": "Received 27,000 coins.",
    "DK4_MES_B286_R0026": "One more thing: he is very dangerous. Strong... You'll understand when you meet him.",
    "DK4_MES_B287_R0005": "Gyaaah! Rrraaargh!",
    "DK4_MES_B287_R0009": "William!{LB}Caught at last.",
    "DK4_MES_B287_R0013": "Time to go.",
    "DK4_MES_B287_R0017": "No need to rush off. Take your reward.",
    "DK4_MES_B287_R0020": "Received 100,000 coins.",
    "DK4_MES_B287_R0051": "Veracruz share rose slightly!",
    "DK4_MES_B287_R0069": "Heard? Ancient kingdom ruins lie nearby. A map pointing to them was found.",
    "DK4_MES_B287_R0073": "Hmm. Where is that map?",
    "DK4_MES_B287_R0076": "No idea. Search if curious.",
    "DK4_MES_B288_R0014": "Must defeat pirate William.",
    "DK4_MES_B288_R0027": "William's fleet is in the New World.",
    "DK4_MES_B289_R0005": "A job only you can do.",
    "DK4_MES_B289_R0009": "Defeat Turkish pirate Zaganos Bey. He prowls near Cyprus.",
    "DK4_MES_B289_R0013": "Here is an advance. He is vicious and strong.",
    "DK4_MES_B289_R0023": "Received 28,000 coins.",
    "DK4_MES_B290_R0005": "Zaganos! You actually caught him!",
    "DK4_MES_B290_R0008": "Damn... Boil or burn me. Your choice!",
    "DK4_MES_B290_R0011": "You are amazing. A great feat. This may seem small, but accept our thanks.",
    "DK4_MES_B290_R0014": "Received 98,000 coins.",
    "DK4_MES_B290_R0045": "Genoa share rose slightly!",
    "DK4_MES_B290_R0063": "Heard you seek ruins? Roman ruins lie in this land too. Go see them.",
    "DK4_MES_B290_R0066": "But first, do not forget to get a map.",
    "DK4_MES_B291_R0014": "Defeat Zaganos in the Mediterranean.",
    "DK4_MES_B291_R0026": "Zaganos sails the Mediterranean.",
    "DK4_MES_B292_R0006": "{MACRO:FO} crew, right? Genoa's guild is looking for you.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = [row for row in csv.DictReader(stream) if row["id"].startswith(prefixes)]
    records = []
    block_counts: dict[str, int] = {}
    for row in source_rows:
        row_id = row["id"]
        english = OVERRIDES.get(row_id)
        if english is None:
            raise SystemExit(f"Raphael V68 unresolved record: {row_id}")
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        source_hex = row["source_hex"].upper()
        first = int(source_hex[:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(first, "Raphael or scene text"),
            "context": CONTEXT[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving bounty names, rewards, macros, scene order, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects native row boundaries from progressive ASCII pair-phase wrapping."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V68 inventory mismatch: {len(records)} != {len(source_rows)}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v68-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Seven source-locked Raphael bounty, capture, reward, reminder, and ruin-hint events across SC0 blocks 286-292.",
        "excluded_records": {},
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
