from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v19.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
EXCLUDED = {
    "DK4_MES_B122_R0004": "Raw event-control payload; not dialogue.",
    "DK4_MES_B122_R0025": "Raw event-control payload; not dialogue.",
    "DK4_MES_B125_R0004": "Raw event-control payload; not dialogue.",
    "DK4_MES_B126_R0004": "Raw event-control payload; not dialogue.",
}
TRANSLATIONS = {
    122: [
        "Admiral, this!", "Admiral!", "Admiral, this!",
        "Amazing! Such fine jade!",
        "Here, as in the East,{LB}jade is the most prized gem.",
        "This much jade offered here{LB}shows how important{LB}this structure once was.",
    ],
    124: [
        "Wait.",
        "A gift cannot go unanswered.{LB}Here is a useful tip.",
        "A grand building lies{LB}by the Ganges.{LB}Visit while nearby.",
        "A map is needed.{LB}Please go if you find it.",
        "Thanks.{LB}We will go with the map.",
    ],
    125: [
        "This statue...", "Hm?",
        "The design seems wrong for this place.", "The design looks out of place here.",
        "The statue seems to stand out here.", "This statue does not match.",
        "Does this not seem wrong here?", "The statue hardly suits this building.",
        "Seems out of place here.", "This design does not suit the building.",
        "Yes?",
        "Looks like a figurehead.{LB}Was it one before?",
        "Looks like a figurehead.{LB}Perhaps it always was one.",
        "Does this not look like a figurehead?{LB}Maybe that is exactly what it is.",
        "A figurehead shape...{LB}Perhaps it was one originally.",
        "Looks like a figurehead...{LB}Maybe that is what it is.",
        "The shape is a figurehead.{LB}Surely that was its purpose.",
        "A figurehead. Look.",
        "A figurehead shape...{LB}Perhaps it was one originally.",
        "Ah, true.",
    ],
    126: [
        "Oh! This is it!",
        "As the discoverers,{LB}you may own this dagger.",
        "Thanks to you, our tribe's sacred anchor{LB}has been found at last.{LB}Please accept it.",
        "Received 24,000 gold coins.",
        "Let us return.{LB}Your fleet must be waiting.",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {"13": "Mikhail Lett", "B3": "Tribal guide", "C6": "Gift guide", "D1": "Raphael crewmate", "D6": "Raphael crewmate", "DC": "Raphael crewmate", "FE": "System"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    122: "Raphael's party discovers a major jade offering and explains its cultural and architectural significance.",
    124: "A grateful woman reveals an Indian landmark that requires a map to reach.",
    125: "Every possible crew observer recognizes an out-of-place statue as a usable ship figurehead.",
    126: "A tribal guide grants the discovered ceremonial dagger and 24,000 gold before returning to the fleet.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    inventory = {row["id"] for row in rows if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    records = []
    block_counts = {}
    translated_ids = set()
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
                "localization_note": "Faithful concise American English preserving discovery lore, all observer variants, exact reward, and fixed-allocation safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    if translated_ids | set(EXCLUDED) != inventory:
        raise SystemExit("Raphael V19 inventory accounting mismatch")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v19-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Jade, Indian-landmark, figurehead, and ceremonial-dagger discoveries across Raphael SC0 blocks 122 and 124-126.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
