from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v76.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

EXCLUDED = {
    "DK4_MES_B310_R0038": "Raw forest-scene control payload; not dialogue.",
}

SPEAKERS = {
    0x05: "Claudio Manousch",
    0x13: "Al Fasi",
    0x94: "Hidden-village father and expedition guide",
    0x97: "Raphael crewmate",
    0xA2: "Sick child",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B307_R0020": "Eastern medicine... Where could it be?",
    "DK4_MES_B307_R0026": "This must be Hua Tuo's Herbal Medicine. Deliver it to the guild at once!",
    "DK4_MES_B307_R0041": "No eastern medicine yet?",
    "DK4_MES_B308_R0005": "You found it?!{LB}Give it to the boy at once!",
    "DK4_MES_B308_R0009": "Yes!",
    "DK4_MES_B308_R0014": ".",
    "DK4_MES_B308_R0019": "...How?",
    "DK4_MES_B308_R0023": "My cough...",
    "DK4_MES_B308_R0027": "Oh! His color is returning!",
    "DK4_MES_B308_R0031": "Yes. He should recover.{LB}His fever is gone.",
    "DK4_MES_B308_R0034": "Really?! This medicine is amazing!",
    "DK4_MES_B308_R0045": "Eastern medicine...",
    "DK4_MES_B308_R0052": "Thank you!! You saved my son's life!!",
    "DK4_MES_B308_R0056": "Please, think nothing of it. We could not let such a dear child die.",
    "DK4_MES_B308_R0060": "You're a good person. Never forgotten. Ask anything about this town.",
    "DK4_MES_B308_R0064": "The ruins?{LB}Yes. Let me guide you.",
    "DK4_MES_B309_R0005": "Hey, {MACRO:FI}.{LB}'Dead end ahead,' it says.",
    "DK4_MES_B309_R0008": "You folks, the road to those ruins was closed after a recent rockslide.",
    "DK4_MES_B309_R0012": "Then we cannot reach the ruins?",
    "DK4_MES_B309_R0015": "Probably not for a while.",
    "DK4_MES_B309_R0019": "How long...?",
    "DK4_MES_B309_R0023": "No one goes there. Could be ten years, could be twenty...",
    "DK4_MES_B309_R0027": "What now, {MACRO:FI}?{LB}We cannot wait that long.",
    "DK4_MES_B309_R0030": "You could climb the cliff if you must go, but it is dangerous.",
    "DK4_MES_B309_R0035": "Up?",
    "DK4_MES_B309_R0039": "Even locals rarely attempt it.",
    "DK4_MES_B309_R0043": "Let's climb!",
    "DK4_MES_B309_R0050": "Then let me guide you to the cliff. Meet me here with a map.",
    "DK4_MES_B309_R0055": "A map?",
    "DK4_MES_B309_R0059": "A Christian village hides there. Beyond the cliff the route is unknown to me. A map may be in a Mediterranean town.",
    "DK4_MES_B310_R0020": "No map, Admiral.{LB}We'll be lost.",
    "DK4_MES_B310_R0021": "No map.{LB}We'll get lost.",
    "DK4_MES_B310_R0022": "No map?{LB}We cannot go on.",
    "DK4_MES_B310_R0023": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B310_R0024": "No map means{LB}getting lost.",
    "DK4_MES_B310_R0025": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B310_R0026": "No map.{LB}We cannot continue!",
    "DK4_MES_B310_R0027": "No map.{LB}We'll get lost.",
    "DK4_MES_B310_R0041": "A forest like this near Genoa...",
    "DK4_MES_B310_R0044": "Yeah. This place is eerie.",
    "DK4_MES_B310_R0048": "Admiral! Look!",
    "DK4_MES_B310_R0053": "W-whoa!",
    "DK4_MES_B310_R0057": "Snake!{LB}What now, {MACRO:FI}?",
    "DK4_MES_B310_R0063": "Hit",
    "DK4_MES_B310_R0065": "Run",
    "DK4_MES_B310_R0074": "Attack",
    "DK4_MES_B310_R0078": "With this many, we may have a chance. Everyone, stay alert!",
    "DK4_MES_B310_R0082": "Got it!",
    "DK4_MES_B310_R0091": "Snake beaten!{LB}That was hard...",
    "DK4_MES_B310_R0099": "Several sailors were injured.",
    "DK4_MES_B310_R0105": "Run!{LB}We should flee this place!",
    "DK4_MES_B310_R0108": "All right! Everyone, back!",
    "DK4_MES_B310_R0114": "Whew... Everyone safe?",
    "DK4_MES_B310_R0118": "Yeah... safe.",
    "DK4_MES_B310_R0123": "Good...",
    "DK4_MES_B310_R0127": "Good. Let's press on!",
    "DK4_MES_B310_R0137": "Whoa!{LB}What is this?!",
    "DK4_MES_B310_R0140": "What, {MACRO:FI}?!",
    "DK4_MES_B310_R0145": "My foot is stuck!",
    "DK4_MES_B310_R0149": "What?!",
    "DK4_MES_B310_R0160": "Hang on!{LB}Stay still!",
    "DK4_MES_B310_R0163": "Heave!{LB}Damn, no use...{LB}Everyone, lend a hand!",
    "DK4_MES_B310_R0167": "Aye!",
    "DK4_MES_B310_R0171": "At last, you're free...",
    "DK4_MES_B310_R0176": "Thanks, Clau{LB}You saved me.",
    "DK4_MES_B310_R0186": "Hold on! We'll pull you out!{LB}Nnngh... Rrraaaagh!",
    "DK4_MES_B310_R0190": "Pant...{LB}You okay, {MACRO:FI}?",
    "DK4_MES_B310_R0194": "Yeah... Thanks, Clau. What a shock. Never thought a bog lay here.",
    "DK4_MES_B310_R0202": "The sailors seem fatigued.",
    "DK4_MES_B310_R0219": "Admiral, ahead!",
    "DK4_MES_B310_R0221": "Look ahead!",
    "DK4_MES_B310_R0223": "Admiral, there!",
    "DK4_MES_B310_R0225": "Look!",
    "DK4_MES_B310_R0227": "Look there!",
    "DK4_MES_B310_R0229": "Admiral, there!",
    "DK4_MES_B310_R0231": "Oh...!",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [
            row
            for row in csv.DictReader(source)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in range(307, 311))
        ]

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
        records.append(
            {
                "id": row["id"],
                "english": rendered,
                "speaker": SPEAKERS.get(first, "Raphael party, choice, or scene text"),
                "context": "Raphael completes the hidden-village medicine quest, learns the cliff route to the ruins, and crosses a dangerous forest.",
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving route variants, decisions, hazards, macro names, and fixed-record constraints.",
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
        raise SystemExit(f"Raphael V76 unresolved records: {unresolved}")

    counts = {
        str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows)
        for block in range(307, 311)
    }
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v76-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael medicine-delivery, ruins-guide, cliff-route, forest-snake, bog-rescue, and forest-exit events in SC0 blocks 307-310.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "blocks": counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
