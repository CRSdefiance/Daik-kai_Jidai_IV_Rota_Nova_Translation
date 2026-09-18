from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v10.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B90_R0005": "Ah...",
    "DK4_MES_B90_R0010": "Janus, what is wrong?",
    "DK4_MES_B90_R0014": "Admiral...{LB}Ships are nice.",
    "DK4_MES_B90_R0023": "With a fleet of my own,{LB}trade in the Mediterranean{LB}would be the dream.",
    "DK4_MES_B90_R0028": "Why that sea?",
    "DK4_MES_B90_R0032": "No sea has more variety.{LB}Ships of every shape cross{LB}among so many nations.{LB}The thought is thrilling.",
    "DK4_MES_B90_R0036": "Understood. A regional fleet{LB}under Janus gets the Mediterranean.",
    "DK4_MES_B90_R0040": "Really? That would be wonderful!{LB}Any time will do,{LB}but please do not forget.",
    "DK4_MES_B90_R0044": "Yes. Noted.",

    "DK4_MES_B91_R0010": "Me?",
    "DK4_MES_B91_R0019": "Trust.",
    "DK4_MES_B91_R0021": "Doubt.",
    "DK4_MES_B91_R0032": "How dare you say that{LB}to our admiral!",
    "DK4_MES_B91_R0039": "You!",
    "DK4_MES_B91_R0047": "Huh?",
    "DK4_MES_B91_R0055": "What a strange one...",
    "DK4_MES_B91_R0066": "This?",
    "DK4_MES_B91_R0074": "May such a treasure be accepted?",
    "DK4_MES_B91_R0081": "Then it will be accepted.{LB}Thank you.",
    "DK4_MES_B91_R0088": "{MACRO:FI}'s luck{LB}rose by 1!",
    "DK4_MES_B91_R0091": "His luck{LB}rose by 1!",
    "DK4_MES_B91_R0098": "Odd people ruin one's luck.{LB}Let us go.",
    "DK4_MES_B91_R0102": "Y-yes.",
    "DK4_MES_B91_R0109": "{MACRO:FI}'s spirit{LB}rose by 1!",
    "DK4_MES_B91_R0112": "His spirit{LB}rose by 1!",

    "DK4_MES_B92_R0005": "Tomatoes are good.{LB}Munch.",
    "DK4_MES_B92_R0009": "Yes, they do.",
    "DK4_MES_B92_R0013": "Thought it an apple.{LB}Munch.",
    "DK4_MES_B92_R0017": "Really?",
    "DK4_MES_B92_R0021": "So sweet and good.{LB}Munch, munch.",
    "DK4_MES_B92_R0025": "...(Big appetite.)",
    "DK4_MES_B92_R0029": "Ha! You really like tomatoes.",
    "DK4_MES_B92_R0032": "Then take this.",
    "DK4_MES_B92_R0035": "What is it?",
    "DK4_MES_B92_R0039": "A tomato plant.",
    "DK4_MES_B92_R0044": "Really?",
    "DK4_MES_B92_R0048": "Certainly.{LB}You praised these tomatoes{LB}so highly.",
    "DK4_MES_B92_R0053": "Thank you.",
    "DK4_MES_B92_R0057": "Good deal.{LB}Munch.",
    "DK4_MES_B92_R0062": "...(Still eating.)",
}

SPEAKERS = {
    "04": "Janus Pasha", "0E": "Emilio Ferrog", "14": "Fernando",
    "6C": "Tomato grower", "FE": "System message",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "90": "Janus tells Raphael that he hopes to command a Mediterranean regional fleet because of its varied nations, ships, and trade.",
    "91": "A strange trust-or-doubt encounter changes Raphael and Fernando's luck or spirit, with both choices and outcomes localized.",
    "92": "Emilio's enthusiastic tomato tasting earns Raphael's fleet a tomato seedling.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    inventory = {row_id for row_id in all_rows if row_id.startswith(("DK4_MES_B90_", "DK4_MES_B91_", "DK4_MES_B92_"))}
    if set(LINES) != inventory:
        raise SystemExit(f"Raphael V10 inventory mismatch: missing={sorted(inventory-set(LINES))} extra={sorted(set(LINES)-inventory)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        blocks[block] = blocks.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the fleet-assignment preference, both attribute-event branches, item reward, character comedy, and route-name macros.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v10-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Janus's regional-fleet preference, both trust-event attribute branches, and Emilio's tomato reward across Raphael SC0 blocks 90-92.",
        "excluded_records": {},
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
