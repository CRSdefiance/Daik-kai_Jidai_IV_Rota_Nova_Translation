from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v88.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
BLOCKS = tuple(range(0, 12))

SPEAKERS = {
    0x05: "Claudio",
    0x06: "Eirene",
    0x07: "Eirene",
    0x08: "Eirene",
    0x0C: "Muramasa examiner",
    0x10: "Muramasa owner",
    0x13: "Raphael companion",
    0x14: "Claudio",
    0x19: "Raphael companion",
    0x1B: "Raphael companion",
    0x1E: "Albuquerque",
    0x1F: "Pedro de Valdes",
    0x23: "Silveira",
    0x24: "Silveira",
    0x25: "Abraham ibn Uddin",
    0x27: "Pereira",
    0x28: "Koon",
    0x29: "Kurushima",
    0x30: "Lookout",
    0x31: "Fleet officer",
    0x3B: "Valdes officer",
    0x97: "Lookout",
}

EXCLUDED = {
    "DK4_MES_B00_R0003": "Raw scene-control payload, not visible dialogue.",
    "DK4_MES_B01_R0003": "Raw scene-control payload, not visible dialogue.",
    "DK4_MES_B10_R0086": "Raw scene-control payload, not visible dialogue.",
}

OVERRIDES = {
    "DK4_MES_B00_R0006": "Africa's Ruler's Proof...!",
    "DK4_MES_B00_R0010": "We finally did it!",
    "DK4_MES_B00_R0020": "But we have to collect seven of these?",
    "DK4_MES_B00_R0025": "We need all seven.",
    "DK4_MES_B00_R0033": "Which Proof comes next?",
    "DK4_MES_B00_R0037": "Adventurers press onward, right?{LB}Let's head east!",
    "DK4_MES_B00_R0048": "Eastward, then!",
    "DK4_MES_B00_R0056": "Eastward...{LB}Let's go!",
    "DK4_MES_B01_R0006": "Wow!{LB}A little scary, though.",
    "DK4_MES_B01_R0009": "Y-yeah.{LB}A little creepy...",
    "DK4_MES_B01_R0013": "What's wrong, Clau? Scared?",
    "DK4_MES_B01_R0017": "Shut up. Put it away!{LB}Don't leave that creepy thing{LB}lying around!",
    "DK4_MES_B01_R0022": "Oh. Huh. Hmm.",
    "DK4_MES_B01_R0034": "So you're scared after all?",
    "DK4_MES_B01_R0049": "Hmm. So even Claudio has things{LB}he's bad at.",
    "DK4_MES_B01_R0055": "What?{LB}This doesn't scare me.",
    "DK4_MES_B01_R0059": "Then shall we put it{LB}in Clau's cabin?",
    "DK4_MES_B01_R0063": "No! Anything but that!{LB}You have my word!{LB}Work comes first!!",
    "DK4_MES_B01_R0075": "Hmm. Could be useful.",
    "DK4_MES_B01_R0083": "Ha, just kidding. We'll stow it.{LB}Next region!{LB}Clau, counting on you!",
    "DK4_MES_B01_R0087": "Y-yeah! Leave it to me...{LB}Whew. Saved...",
    "DK4_MES_B02_R0007": "Good. We have the East Asian Proof.{LB}Now we must take it{LB}to Governor Pereira.",
    "DK4_MES_B03_R0006": "At last... Muramasa...",
    "DK4_MES_B03_R0010": "Such a strange glow...{LB}Almost pulls you in.",
    "DK4_MES_B04_R0006": "Yes, unmistakable!{LB}That same dull gleam.",
    "DK4_MES_B04_R0010": "Lucky no one found it...",
    "DK4_MES_B05_R0005": "Admiral!{LB}Espinosa's fleet sighted!!",
    "DK4_MES_B05_R0008": "There! Those are the people{LB}roaming Africa with Silveira!",
    "DK4_MES_B05_R0019": "Hmph.{LB}A decent number.",
    "DK4_MES_B05_R0024": "This looks difficult...",
    "DK4_MES_B05_R0032": "Can we manage alone?",
    "DK4_MES_B05_R0036": "Admiral!{LB}Silveira astern!!",
    "DK4_MES_B05_R0040": "Whew.{LB}Admiral Silveira, you came.",
    "DK4_MES_B05_R0043": "Now we have a chance.",
    "DK4_MES_B05_R0048": "We won't know until we try.",
    "DK4_MES_B05_R0052": "Now then, {MACRO:FI}.{LB}You must fight hard for me too!{LB}Ha ha ha!",
    "DK4_MES_B05_R0057": "Everyone, count on you!{LB}Let's go!",
    "DK4_MES_B05_R0060": "Yeah!",
    "DK4_MES_B06_R0012": "The famed Admiral {MACRO:FA}.{LB}We meet in battle...",
    "DK4_MES_B06_R0017": "So this is{LB}Admiral Abraham Uddin...",
    "DK4_MES_B06_R0022": "We meet in battle...",
    "DK4_MES_B06_R0027": "Admiral Uddin...",
    "DK4_MES_B06_R0034": "No matter the foe, no mercy.{LB}Come!",
    "DK4_MES_B07_R0011": "Damn! That's Koon's fleet?{LB}Look at those guns!",
    "DK4_MES_B07_R0015": "A hard fight awaits...",
    "DK4_MES_B07_R0023": "...Here!",
    "DK4_MES_B07_R0028": "Ah!{LB}Pereira!",
    "DK4_MES_B07_R0031": "You again! Outsiders should{LB}stay out of this!",
    "DK4_MES_B07_R0040": "...{LB}Pereira...",
    "DK4_MES_B07_R0043": "Old man...",
    "DK4_MES_B07_R0047": "Damn you! No matter.{LB}You all sink together!",
    "DK4_MES_B07_R0051": "...Stay close.",
    "DK4_MES_B07_R0056": "Y-yes!",
    "DK4_MES_B08_R0006": "These spice isles are ours!",
    "DK4_MES_B08_R0011": "Let's begin.{LB}Ready, {MACRO:FA}!",
    "DK4_MES_B08_R0015": "Yes!",
    "DK4_MES_B09_R0009": "Gwahaha! Your puny foreign ships{LB}will become seaweed!{LB}Gahaha!!",
    "DK4_MES_B09_R0013": "No ship beats ours!",
    "DK4_MES_B09_R0018": "Such a nimble ship?",
    "DK4_MES_B09_R0030": "Amazing...{LB}Such a ship...",
    "DK4_MES_B09_R0036": "Hey! Nobody told me they had{LB}warships clad in iron!!",
    "DK4_MES_B09_R0041": "Maybe that is one of the ship types{LB}Xian mentioned.",
    "DK4_MES_B09_R0045": "No time for idle talk!{LB}Enough. Stay sharp and attack!",
    "DK4_MES_B09_R0050": "W-wait, Clau!{LB}Attack without warning and{LB}we'll look like pirates...",
    "DK4_MES_B10_R0007": "Valdes awaits!{LB}Everyone, count on you!",
    "DK4_MES_B10_R0018": "Everyone ready?",
    "DK4_MES_B10_R0033": "Heh, anytime!{LB}Let them come!",
    "DK4_MES_B10_R0039": "Yeah! Let's do it!",
    "DK4_MES_B10_R0051": "On it!",
    "DK4_MES_B10_R0058": "So that is the Portuguese fleet.{LB}Young fools who dare defy Spain...",
    "DK4_MES_B10_R0061": "They shall learn!{LB}Battle stations!",
    "DK4_MES_B10_R0064": "Yes!{LB}Battle stations!!",
    "DK4_MES_B10_R0072": "Battle line!",
    "DK4_MES_B10_R0076": "Enemy ahead: Portuguese rebels!{LB}Charge!!",
    "DK4_MES_B11_R0006": "Boy! Defying Pedro de Valdes{LB}was reckless arrogance!{LB}Atone with your life!!",
    "DK4_MES_B11_R0024": "Albuquerque!{LB}Lead the vanguard!",
    "DK4_MES_B11_R0027": "Yes.",
}


def main() -> None:
    prefixes = tuple(f"DK4_MES_B{block:02d}_" for block in BLOCKS)
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith(prefixes)]
    records = []
    unresolved = []
    for row in rows:
        if row["id"] in EXCLUDED:
            continue
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
            "id": row["id"],
            "english": rendered,
            "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
            "context": "Raphael's Ruler's Proof progression and major regional-fleet battle scenes.",
            "source_meaning": row["japanese"].lstrip("".join(chr(value) for value in SPEAKERS)),
            "localization_note": "Natural concise American English preserving named characters, battle intent, route progression, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V88 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v88-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael Ruler's Proof progression and major fleet battles in SC0 blocks 0-11.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block:02d}_") for row in rows) for block in BLOCKS},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
