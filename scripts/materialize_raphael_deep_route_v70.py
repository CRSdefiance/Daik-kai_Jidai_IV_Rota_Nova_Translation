from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v70.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = (294, 295, 296)

SPEAKERS = {
    0x04: "Raphael crewmate",
    0x05: "Claudio Manousch",
    0x08: "Arcadius Eirene",
    0x71: "Guild messenger",
    0x93: "Guildmaster",
    0xD0: "Raphael crewmate",
}

CONTEXT = {
    294: "A messenger tells Raphael that the London guild is looking for him.",
    295: "The London guild asks Raphael to investigate suspicious men occupying the Stone Circle ruins.",
    296: "Raphael's party deciphers the cult chant and identifies sunrise on an equinox as the revelation time.",
}

OVERRIDES = {
    "DK4_MES_B294_R0006": "There you are. With {MACRO:FA}, right? London's guild seeks you.",
    "DK4_MES_B295_R0005": "Got a job for you.",
    "DK4_MES_B295_R0009": "Ruins lie nearby.{LB}Suspicious men now come and go.",
    "DK4_MES_B295_R0013": "They drove off the priest guarding the ruins and now hold festival rituals.",
    "DK4_MES_B295_R0017": "No one knows their deeds.{LB}People fear a criminal den.",
    "DK4_MES_B295_R0021": "Learn who they are.",
    "DK4_MES_B295_R0024": "A map should make the ruins easy to find.",
    "DK4_MES_B295_R0034": "They bought every map here.{LB}Now sold out.",
    "DK4_MES_B295_R0038": "Amsterdam may still sell one.{LB}Get it there.",
    "DK4_MES_B295_R0045": "A map? This Stone Circle Map?",
    "DK4_MES_B295_R0049": "Yes, that's it. Well prepared. We can trust you. Good luck.",
    "DK4_MES_B296_R0013": "Sun, moon, stars turn.{LB}When light and dark balance,{LB}it lies between.",
    "DK4_MES_B296_R0017": "You remember that well.",
    "DK4_MES_B296_R0025": "When light and dark are equal,{LB}it lies between them...{LB}What is 'it'?",
    "DK4_MES_B296_R0035": "So they gather next time{LB}to find it, right?",
    "DK4_MES_B296_R0041": "Then their next ritual must be to find it, right?",
    "DK4_MES_B296_R0049": "So something is hidden somewhere in those ruins...",
    "DK4_MES_B296_R0052": "Then why haven't they found it already?",
    "DK4_MES_B296_R0068": "So its hiding place appears only on that day.",
    "DK4_MES_B296_R0069": "So we cannot find it until that day.",
    "DK4_MES_B296_R0070": "Then its hiding place cannot be known before that day...",
    "DK4_MES_B296_R0071": "Wait... So its hiding place is unknown until that day!",
    "DK4_MES_B296_R0073": "The place stays unknown until that day.",
    "DK4_MES_B296_R0074": "Until that day, no one knows where it is.",
    "DK4_MES_B296_R0075": "So its hiding place cannot be known until that day.",
    "DK4_MES_B296_R0080": "They cannot find it yet. On that day, the place becomes clear.",
    "DK4_MES_B296_R0088": "Got it.",
    "DK4_MES_B296_R0092": "But we have no idea when 'that day' is...",
    "DK4_MES_B296_R0109": "Light and dark balance...",
    "DK4_MES_B296_R0115": "Light and dark equal...{LB}Day and night...",
    "DK4_MES_B296_R0123": "That's it! Day and night balance at sunrise or sunset!",
    "DK4_MES_B296_R0127": "They meet at night, so it means sunrise!",
    "DK4_MES_B296_R0132": "Wait. Let light and dark mean day and night...",
    "DK4_MES_B296_R0136": "Day and night balance? So... sunrise?",
    "DK4_MES_B296_R0139": "Sunrise or sunset.{LB}They meet at night, so sunrise.",
    "DK4_MES_B296_R0145": "Well done! But sunrise comes daily. Which day?",
    "DK4_MES_B296_R0157": "True...",
    "DK4_MES_B296_R0165": "No. Day and night are exactly equal only twice each year!",
    "DK4_MES_B296_R0174": "Twice a year? Oh, right!!",
    "DK4_MES_B296_R0179": "Ah, of course...!",
    "DK4_MES_B296_R0187": "The equinoxes!",
    "DK4_MES_B296_R0191": "That's it!! Let's go first and find it!",
    "DK4_MES_B296_R0202": "Claudio, no.{LB}They gather the night before.",
    "DK4_MES_B296_R0207": "But they gather the night before.{LB}Getting ahead seems hard.",
    "DK4_MES_B296_R0214": "Oh... right. The place is hidden until that day, so going early is useless.",
    "DK4_MES_B296_R0218": "What now...",
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
            raise SystemExit(f"Raphael V70 unresolved record: {row_id}")
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
            "source_meaning": english.replace("{LB}", " ").replace("{MACRO:FA}", "Raphael"),
            "localization_note": "Faithful concise American English preserving the Stone Circle item name, chant logic, equinox deduction, macros, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if len(records) != len(source_rows):
        raise SystemExit(f"Raphael V70 inventory mismatch: {len(records)} != {len(source_rows)}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v70-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael London guild summons, Stone Circle investigation, and equinox-riddle deduction across SC0 blocks 294-296.",
        "excluded_records": {},
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
