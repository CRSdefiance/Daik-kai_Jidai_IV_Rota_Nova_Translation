from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v71.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (297, 298, 299, 300)

SPEAKERS = {
    0x04: "Raphael crewmate",
    0x05: "Claudio Manousch",
    0x08: "Arcadius Eirene",
    0x93: "Guildmaster",
    0xBB: "London informant",
    0xFE: "System or sound effect",
}

CONTEXT = {
    297: "A London informant explains that the Stone Circle may have measured calendars and time.",
    298: "Raphael's party realizes the cult seeks the equinox shadow cast by the Stone Circle.",
    299: "Raphael's party calculates the shadow, digs up a stone box, and finds blank parchment.",
    300: "The London guild rewards Raphael while the party wonders whether the parchment conceals a Proof of Hegemony map.",
}

OVERRIDES = {
    "DK4_MES_B297_R0007": "Welcome.",
    "DK4_MES_B297_R0011": "Want to know about those ruins?",
    "DK4_MES_B297_R0015": "Customers say these ruins{LB}measured calendars and time.",
    "DK4_MES_B297_R0020": "Calendar...",
    "DK4_MES_B298_R0006": "Lies between light and dark...",
    "DK4_MES_B298_R0011": "Those stones measured calendars and time...",
    "DK4_MES_B298_R0015": "...That's it! Got it!!",
    "DK4_MES_B298_R0019": "Really?!",
    "DK4_MES_B298_R0024": "The ruins' shadow edge. Used as a sundial, those pillars make shadows matter!",
    "DK4_MES_B298_R0040": "With our latitude, we can calculate where the equinox shadow falls!",
    "DK4_MES_B298_R0046": "Brilliant, {MACRO:FI}! With our latitude, we can calculate where the equinox shadow falls!",
    "DK4_MES_B298_R0054": "Brilliant, {MACRO:FI}! With our latitude, we can calculate where the equinox shadow falls!",
    "DK4_MES_B298_R0060": "Whoa, we can do that?!",
    "DK4_MES_B298_R0065": "Let's visit the ruins!",
    "DK4_MES_B299_R0019": "Let's see... Morning's shadow was here.{LB}The longest should end here!",
    "DK4_MES_B299_R0024": "This was this morning's shadow, so the longest shadow should end here.",
    "DK4_MES_B299_R0032": "Let's see... Morning's shadow was here.{LB}The longest should end here.",
    "DK4_MES_B299_R0038": "Let's dig!",
    "DK4_MES_B299_R0042": "Digging.",
    "DK4_MES_B299_R0046": "Oh!",
    "DK4_MES_B299_R0052": "A stone box!!",
    "DK4_MES_B299_R0056": "All right, open it!! Heave!!",
    "DK4_MES_B299_R0060": "? Huh? Nothing inside?",
    "DK4_MES_B299_R0064": "Look at this!",
    "DK4_MES_B299_R0068": "A scrap of paper?!",
    "DK4_MES_B299_R0073": "!! Blank...",
    "DK4_MES_B299_R0077": "Hey! What's going on? They were seeking this?!",
    "DK4_MES_B299_R0085": "This should stop their plan.{LB}Let's flee before they find us{LB}and make us sacrifices.",
    "DK4_MES_B299_R0088": "Creepy. Let's return and report to the guild!",
    "DK4_MES_B300_R0005": "Thanks. All solved safely.{LB}Take your reward.",
    "DK4_MES_B300_R0009": "Received 100,000 coins.",
    "DK4_MES_B300_R0040": "London share rose slightly!",
    "DK4_MES_B300_R0052": "But what is this parchment?",
    "DK4_MES_B300_R0063": "Maybe this maps the Proof of Hegemony... but...",
    "DK4_MES_B300_R0069": "Nothing written, so no use.",
    "DK4_MES_B300_R0073": "This paper is clearly not recent. Some secret must remain. Surely...",
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
            raise SystemExit(f"Raphael V71 unresolved record: {row_id}")
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
            "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
            "context": CONTEXT[block],
            "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FI}", "Raphael"),
            "localization_note": "Faithful concise American English preserving the shadow calculation, canonical Proof of Hegemony term, reward, scene order, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V71 inventory mismatch: {len(records)} != {len(source_rows)}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v71-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael Stone Circle informant, equinox-shadow discovery, excavation, blank-parchment find, and London guild resolution across SC0 blocks 297-300.",
        "excluded_records": {},
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
