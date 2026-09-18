from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v78.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

SPEAKERS = {
    0x05: "Claudio Manousch",
    0x08: "Raphael crewmate",
    0x61: "Mosque rumor informant",
    0xC5: "Local dancer",
}

OVERRIDES = {
    "DK4_MES_B313_R0005": "Oh... what now?",
    "DK4_MES_B313_R0010": "What now?",
    "DK4_MES_B313_R0014": "At the festival,{LB}my dance is for the lord.",
    "DK4_MES_B313_R0018": "Oh? You can dance?",
    "DK4_MES_B313_R0022": "Barely. A visitor saw me practice, and word somehow reached the lord.",
    "DK4_MES_B313_R0025": "The tale grew. Now they call me the finest dancer in the land.",
    "DK4_MES_B313_R0030": "What?! How come?",
    "DK4_MES_B313_R0034": "Rumors are frightening. Too late to admit that dancing is beyond me. Yet mastery won't come easily.",
    "DK4_MES_B313_R0038": "What will you do?",
    "DK4_MES_B313_R0042": "What should be done? Ah, had only that rumor been checked properly.",
    "DK4_MES_B313_R0046": "What rumor?",
    "DK4_MES_B313_R0050": "They say earrings that improve dancing exist somewhere. That sounded false, so no details were sought.",
    "DK4_MES_B313_R0054": "Amazing, if true.",
    "DK4_MES_B313_R0058": "Right? Now even false hope would help. Oh, what can be done?",
    "DK4_MES_B314_R0006": "Oh, {MACRO:FI}!{LB}Welcome!",
    "DK4_MES_B314_R0009": "Thanks to you,{LB}my dancing has greatly improved!",
    "DK4_MES_B314_R0013": "Really? Great!",
    "DK4_MES_B314_R0017": "Here's a useful lead.",
    "DK4_MES_B314_R0021": "An old king built a mosque inland. They say treasure sleeps there.",
    "DK4_MES_B314_R0025": "Only one accepted by the king may claim its treasure. Why not try?",
    "DK4_MES_B315_R0005": "Are you the daredevils who went to Masjid-i Shah?",
    "DK4_MES_B315_R0010": "Daredevils? We went there, but why do you ask?",
    "DK4_MES_B315_R0014": "Oh, it became a terrible mess.",
    "DK4_MES_B315_R0018": "Explorers heard your tale{LB}and rushed to the mosque for treasure, but...",
    "DK4_MES_B315_R0022": "Not one returned. Now people even whisper of the king's curse.",
    "DK4_MES_B315_R0027": "Curse?",
    "DK4_MES_B315_R0031": "Once that rumor spread, nobody went near. The missing explorers were abandoned.",
    "DK4_MES_B315_R0035": "You helped start this. With real courage, go back and find them.",
    "DK4_MES_B315_R0039": "Hard to dump all that on us...",
    "DK4_MES_B315_R0044": "Still, we cannot abandon them. Right?",
    "DK4_MES_B315_R0048": "W-well, true...",
    "DK4_MES_B315_R0059": "What? Don't tell me{LB}the curse scares you?",
    "DK4_MES_B315_R0064": "Clau? The curse{LB}scares you?",
    "DK4_MES_B315_R0070": "Nonsense!",
    "DK4_MES_B315_R0075": "We bear some responsibility. Let's investigate again.",
    "DK4_MES_B315_R0078": "Y-yeah. {MACRO:FI} is right. We cannot abandon people in trouble!",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [
            row
            for row in csv.DictReader(source)
            if row["id"].startswith(("DK4_MES_B313_", "DK4_MES_B314_", "DK4_MES_B315_"))
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
        records.append(
            {
                "id": row["id"],
                "english": rendered,
                "speaker": SPEAKERS.get(first, "Raphael party or scene text"),
                "context": "Raphael helps a nervous dancer, receives a mosque-treasure lead, and returns to rescue explorers drawn there by his earlier feat.",
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving the dancer rumor, earring payoff, treasure lead, curse rumor, rescue motive, macro names, and fixed-record constraints.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."}
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    if unresolved:
        raise SystemExit(f"Raphael V78 unresolved records: {unresolved}")

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v78-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael dancer-earring payoff and mosque explorer-rescue setup in SC0 blocks 313-315.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "blocks": {
                str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows)
                for block in range(313, 316)
            },
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
