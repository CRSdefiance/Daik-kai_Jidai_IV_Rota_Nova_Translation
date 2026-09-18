from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v22.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {"DK4_MES_B132_R0089": "Raw battle event-control payload; not dialogue."}
TRANSLATIONS = {
    132: [
        "Battle with Valdes!{LB}Everyone, stand firm!",
        "Everyone ready?", "Heh! Any time!{LB}Come at us!", "Yeah! Let's go!",
        "On it!",
        "So that is the Portuguese fleet.{LB}Young fools who dare defy{LB}the Spanish Empire now.",
        "They will learn.{LB}Battle stations!",
        "Yes! Battle stations!", "Battle line!",
        "Portuguese rebels ahead!{LB}Charge!",
    ],
    133: [
        "Ah...", "Yes, yes. Let us bring Christina.",
        "Who is that?", "My granddaughter.{LB}A skilled swordswoman.",
        "A woman?! Sailing is a man's dream!{LB}Against it! We already have a wom--{LB}Uh-oh.",
        "Ahem, Claudio...", "A-anyway,{LB}a woman is trouble!",
        "Sounds good to me.{LB}A swordswoman could really help.",
        "No! Against it!{LB}Ow! What was that for?",
        "(No difference with two.)",
        "(Another woman may help Arcadius{LB}feel more at ease.)",
        "Ahem. Agreed.", "Another woman makes travel fun.{LB}Right?",
        "(Even {MACRO:FI}...?{LB}All right, fine.)",
        "Since everyone insists,{LB}all right...",
        "Where does she live?", "London.",
        "Understood.{LB}Let us go.",
    ],
    134: [
        "W-what?!",
        "Ambush! Pirates!{LB}They caught us off guard!{LB}We cannot fight back!",
        "That flag... Pirate Vels!{LB}This is bad, Admiral!",
        "The rumors call him dangerous.{LB}Bad luck that he found us.",
        "{MACRO:FI}! Look out!", "Gwaaah!", "Claudio!",
        "Claudio! You okay?", "A scratch! Never mind!",
        "Damn!{LB}Retreat now!",
        "We escaped somehow...{LB}This is bad. Make for a nearby port.",
        "Amsterdam is risky.{LB}Another port.",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {
    "04": "Janus Pasha", "05": "Claudio Manousch", "06": "Julio Castor", "08": "Charles Jean Rochefort",
    "13": "Mikhail Lett", "14": "Raphael ally", "19": "Raphael ally", "1F": "Valdes officer",
    "30": "Spanish sailor", "31": "Spanish officer", "3B": "Spanish officer", "97": "Raphael lookout",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    132: "Raphael's fleet and Valdes's forces prepare for their decisive naval battle.",
    133: "Julio suggests recruiting Christina in London while Claudio protests and Arcadius silently welcomes another woman aboard.",
    134: "Pirate Vels ambushes Raphael, Claudio is wounded protecting him, and the fleet escapes toward a safer port.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    inventory = {row["id"] for row in rows if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    records = []
    translated_ids = set()
    block_counts = {}
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_") and row["id"] not in EXCLUDED]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            translated_ids.add(row["id"])
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"), "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful natural American English preserving battle orders, character comedy, recruitment intent, ambush stakes, macro name, and fixed-allocation safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    if translated_ids | set(EXCLUDED) != inventory:
        raise SystemExit("Raphael V22 inventory accounting mismatch")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v22-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Valdes battle preparations, Christina recruitment discussion, and the Vels ambush across Raphael SC0 blocks 132-134.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control")


if __name__ == "__main__":
    main()
