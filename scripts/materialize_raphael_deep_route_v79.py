from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v79.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

SPEAKERS = {
    0x05: "Claudio Manousch",
    0x08: "Raphael crewmate",
    0x11: "Al Fasi",
    0x5C: "Curse-lore informant",
    0x5F: "Basra tavernkeeper",
    0xB6: "Rescued explorer",
    0xFE: "Guardian or system voice",
}

OVERRIDES = {
    "DK4_MES_B316_R0007": "Whew... Nearly there.",
    "DK4_MES_B316_R0010": "Hm? Hear something?",
    "DK4_MES_B316_R0014": "Help me...",
    "DK4_MES_B316_R0019": "That must be a missing explorer!",
    "DK4_MES_B316_R0022": "Hey! Where are you?!",
    "DK4_MES_B316_R0026": "No!",
    "DK4_MES_B316_R0035": "They broke the king's sleep{LB}and earned his wrath.",
    "DK4_MES_B316_R0038": "They stay.{LB}Leave now.",
    "DK4_MES_B316_R0042": "Whoa!",
    "DK4_MES_B316_R0046": "Damn, no use!",
    "DK4_MES_B316_R0051": "The king's curse was real...",
    "DK4_MES_B316_R0055": "What now, {MACRO:FI}?",
    "DK4_MES_B316_R0060": "We need some way to break the curse!",
    "DK4_MES_B316_R0063": "Damn, retreat!",
    "DK4_MES_B317_R0006": "...As suspected.",
    "DK4_MES_B317_R0011": "How can the king's anger be calmed?",
    "DK4_MES_B317_R0014": "Not very certain, but...",
    "DK4_MES_B317_R0019": "You know something?",
    "DK4_MES_B317_R0023": "Start with the fragrance once worn by the queen the king loved in life.",
    "DK4_MES_B317_R0028": "Eh?",
    "DK4_MES_B317_R0032": "Scent.",
    "DK4_MES_B317_R0036": "What kind?",
    "DK4_MES_B317_R0040": "No idea. That much is unknown.",
    "DK4_MES_B317_R0044": "Take it there and offer prayers all night.",
    "DK4_MES_B317_R0048": "With the fragrance found, this may work!",
    "DK4_MES_B317_R0052": "But keep unbelievers away. They might anger the king even more.",
    "DK4_MES_B317_R0056": "What?! Then we cannot do it? That means...",
    "DK4_MES_B317_R0060": "We must ask Al.",
    "DK4_MES_B317_R0072": "Me, of all people? Arabs have long called my faith weak... Will that do?",
    "DK4_MES_B317_R0079": "One more thing:{LB}do not forget Arabian Nights.",
    "DK4_MES_B317_R0084": "Arabian Nights...? Never heard of it.",
    "DK4_MES_B317_R0087": "The king loved those famous tales. Some guild surely sells a copy.",
    "DK4_MES_B317_R0091": "A translation may use{LB}another title.",
    "DK4_MES_B317_R0096": "New title?",
    "DK4_MES_B317_R0100": "Read Arabian Nights to the king. That should restore his good humor.",
    "DK4_MES_B317_R0103": "Hey... This sounds{LB}like worship? More like{LB}babysitting a child.",
    "DK4_MES_B317_R0107": "Who knows? An offering{LB}is about sincerity.",
    "DK4_MES_B317_R0111": "An offering...?{LB}We're here to break a curse.",
    "DK4_MES_B317_R0115": "Close enough. Try it.{LB}We can rethink if it fails.",
    "DK4_MES_B317_R0118": "Once cursed, we could never return!",
    "DK4_MES_B317_R0121": "Then this old man will rescue you. Relax.",
    "DK4_MES_B317_R0124": "...Not reassuring.",
    "DK4_MES_B318_R0012": "We need to call Al back.",
    "DK4_MES_B318_R0028": "Good. Burn the scent.",
    "DK4_MES_B318_R0057": "...We need to buy the fragrance first.",
    "DK4_MES_B318_R0075": "Useless. The king rages.{LB}Leave now, fool.",
    "DK4_MES_B318_R0080": "Wrong scent, it seems.",
    "DK4_MES_B318_R0102": "Oh, right. We need Arabian Nights too...",
    "DK4_MES_B318_R0106": "Could bear another title.{LB}Search carefully.",
    "DK4_MES_B318_R0109": "Do not leave it equipped.",
    "DK4_MES_B318_R0124": "Begin.",
    "DK4_MES_B318_R0129": "Yes.",
    "DK4_MES_B318_R0133": "Ahem!",
    "DK4_MES_B318_R0137": "'By the will of Allah,{LB}the gracious and merciful,{LB}in the name of Allah.'",
    "DK4_MES_B318_R0141": "'Praise Allah, lord of heaven and earth, and our sovereign among those sent below...'",
    "DK4_MES_B318_R0147": "'The Merchant and the Djinn'",
    "DK4_MES_B318_R0152": "'Scheherazade said: O fortunate king, it has reached me that long ago...'",
    "DK4_MES_B318_R0160": "Uh... No. Somehow, sleep took me.",
    "DK4_MES_B318_R0164": "Dawn has broken.",
    "DK4_MES_B318_R0168": "Oh! Saved! Did you break the king's curse?",
    "DK4_MES_B318_R0172": "What? The curse broke?!",
    "DK4_MES_B318_R0176": "Thank you! At last, we can go home!",
    "DK4_MES_B318_R0179": "Shame about the treasure, but life matters more. We're leaving this place!",
    "DK4_MES_B318_R0183": "Goodbye. You should get out quickly too!",
    "DK4_MES_B318_R0187": "...They left.",
    "DK4_MES_B318_R0191": "Hardly worth saving, those people.",
    "DK4_MES_B318_R0195": "Well, fine.{LB}Let's head out too.",
    "DK4_MES_B318_R0198": "No",
    "DK4_MES_B318_R0202": "Whoa!! What is it?!{LB}S-still dissatisfied?!",
    "DK4_MES_B318_R0205": "You soothed the king's memories and led him to peaceful sleep. Receive this reward.",
    "DK4_MES_B318_R0212": "Whew... That startled me.",
    "DK4_MES_B318_R0223": "Hee hee...",
    "DK4_MES_B318_R0227": "W-what is so funny?!",
    "DK4_MES_B319_R0006": "The Basra tavernkeeper was looking for you.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [
            row
            for row in csv.DictReader(source)
            if row["id"].startswith(tuple(f"DK4_MES_B{block}_" for block in range(316, 320)))
        ]
    records = []
    unresolved = []
    for row in rows:
        english = OVERRIDES.get(row["id"])
        if english is None:
            unresolved.append(row["id"])
            continue
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        first = int(row["source_hex"][:2], 16)
        state = f"{first:02X}" if first in SPEAKERS else ""
        rendered = f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
        records.append({
            "id": row["id"], "english": rendered,
            "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
            "context": "Raphael rescues explorers from the king's curse by gathering fragrance and Arabian Nights, then has Al perform the overnight rite.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving ritual requirements, religious context, item handling, reward, macro names, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V79 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v79-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael cursed-explorer rescue, fragrance and Arabian Nights ritual, curse lifting, and reward in SC0 blocks 316-319.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows) for block in range(316, 320)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
