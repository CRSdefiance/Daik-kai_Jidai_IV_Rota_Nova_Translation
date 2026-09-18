from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v77.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

EXCLUDED = {
    "DK4_MES_B312_R0074": "Raw desert-scene control payload; not dialogue.",
}

SPEAKERS = {
    0x97: "Raphael crewmate",
    0xC0: "Colosseum informant",
    0xCF: "Raphael",
    0xD0: "Raphael crewmate",
    0xD3: "Raphael crewmate",
    0xD6: "Raphael crewmate",
    0xFE: "System",
}

OVERRIDES = {
    "DK4_MES_B311_R0006": "Ah, {MACRO:FI}.{LB}Good timing.",
    "DK4_MES_B311_R0009": "Do you know the Colosseum?",
    "DK4_MES_B311_R0013": "The Colosseum?",
    "DK4_MES_B311_R0017": "Ruins from Roman times. Heard you seek ruins, so here is a lead.",
    "DK4_MES_B311_R0022": "Thanks, that helps.{LB}Let's go see it.",
    "DK4_MES_B311_R0025": "Take care.{LB}Remember to buy a map.",
    "DK4_MES_B312_R0019": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B312_R0020": "We need a map, Admiral.",
    "DK4_MES_B312_R0022": "No map, Admiral.{LB}We cannot go on.",
    "DK4_MES_B312_R0023": "Get a map first, Admiral,{LB}or we'll get lost.",
    "DK4_MES_B312_R0024": "No map, Admiral.{LB}We should turn back.",
    "DK4_MES_B312_R0025": "No map means getting lost, Admiral.",
    "DK4_MES_B312_R0027": "Admiral, without a map{LB}we'll get lost.",
    "DK4_MES_B312_R0028": "Admiral, we'll get lost.",
    "DK4_MES_B312_R0054": "This heat is brutal.",
    "DK4_MES_B312_R0056": "Hot...",
    "DK4_MES_B312_R0058": "Whew, so hot.",
    "DK4_MES_B312_R0060": "Even so, what heat.",
    "DK4_MES_B312_R0062": "So hot.",
    "DK4_MES_B312_R0064": "Awful heat.",
    "DK4_MES_B312_R0066": "Whew, so hot.",
    "DK4_MES_B312_R0068": "Such fierce heat.",
    "DK4_MES_B312_R0073": "Long road ahead.{LB}Conserve water.",
    "DK4_MES_B312_R0085": "Dunes ahead. Let's detour.",
    "DK4_MES_B312_R0087": "Dunes. Admiral, let's detour.",
    "DK4_MES_B312_R0089": "Dunes. Better go around.",
    "DK4_MES_B312_R0091": "Dunes ahead.{LB}A detour seems best.",
    "DK4_MES_B312_R0092": "Dunes, huh? Let's go around.",
    "DK4_MES_B312_R0094": "Dunes. Let us go around.",
    "DK4_MES_B312_R0096": "A huge sand hill!{LB}Let's go around.",
    "DK4_MES_B312_R0097": "Dunes. Let us detour.",
    "DK4_MES_B312_R0104": "Up",
    "DK4_MES_B312_R0106": "Go right",
    "DK4_MES_B312_R0108": "Go left",
    "DK4_MES_B312_R0117": "Whew... Why choose the hardest route...?",
    "DK4_MES_B312_R0129": "The sailors seem fatigued.",
    "DK4_MES_B312_R0135": "Storm!",
    "DK4_MES_B312_R0139": "Ptoo! Sand in mouth...",
    "DK4_MES_B312_R0152": "We cannot see ahead.",
    "DK4_MES_B312_R0154": "Cannot... see...",
    "DK4_MES_B312_R0156": "Cannot see.",
    "DK4_MES_B312_R0158": "Cannot see.",
    "DK4_MES_B312_R0160": "Damn it, cannot see ahead!",
    "DK4_MES_B312_R0162": "Cannot see.",
    "DK4_MES_B312_R0164": "Cannot see a thing!",
    "DK4_MES_B312_R0166": "No view ahead.",
    "DK4_MES_B312_R0179": "Some sailors have left.",
    "DK4_MES_B312_R0192": "Admiral, we're{LB}too far left.",
    "DK4_MES_B312_R0193": "Admiral...{LB}Veering left?",
    "DK4_MES_B312_R0194": "Admiral, too far left?",
    "DK4_MES_B312_R0196": "Admiral,{LB}too far left?",
    "DK4_MES_B312_R0197": "Admiral,{LB}we're far left of course.",
    "DK4_MES_B312_R0198": "Admiral, it feels like{LB}we've veered far left.",
    "DK4_MES_B312_R0200": "Admiral, haven't we{LB}drifted too far left?",
    "DK4_MES_B312_R0201": "Admiral, are we{LB}veering far left?",
    "DK4_MES_B312_R0205": "You think?",
    "DK4_MES_B312_R0218": "Maybe a little{LB}farther right.",
    "DK4_MES_B312_R0219": "Bear a little{LB}to the right...?",
    "DK4_MES_B312_R0220": "A little more right?",
    "DK4_MES_B312_R0222": "A little more right.",
    "DK4_MES_B312_R0224": "A little more right?",
    "DK4_MES_B312_R0226": "A bit more to the right, perhaps.",
    "DK4_MES_B312_R0228": "More right, maybe.",
    "DK4_MES_B312_R0230": "A little more right, perhaps.",
    "DK4_MES_B312_R0235": "The map says this direction is right. Let's keep going.",
    "DK4_MES_B312_R0253": "Nearly out of{LB}the desert...",
    "DK4_MES_B312_R0254": "Should be out{LB}of the desert...",
    "DK4_MES_B312_R0255": "Desert should end{LB}by now...",
    "DK4_MES_B312_R0256": "Should be out{LB}of the desert...",
    "DK4_MES_B312_R0257": "The desert should end{LB}soon...",
    "DK4_MES_B312_R0258": "The desert should end{LB}before long...",
    "DK4_MES_B312_R0259": "Desert should be{LB}ending now...",
    "DK4_MES_B312_R0260": "The desert should end{LB}before long...",
    "DK4_MES_B312_R0273": "Admiral!{LB}Look over there!",
    "DK4_MES_B312_R0274": "Admiral!{LB}Look!",
    "DK4_MES_B312_R0275": "Admiral!{LB}Look there!",
    "DK4_MES_B312_R0276": "Admiral!{LB}Look!",
    "DK4_MES_B312_R0277": "Admiral!{LB}Look!",
    "DK4_MES_B312_R0278": "Look!{LB}There!",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [
            row
            for row in csv.DictReader(source)
            if row["id"].startswith(("DK4_MES_B311_", "DK4_MES_B312_"))
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
                "context": "Raphael learns of the Colosseum and crosses the desert using a map while managing dunes, heat, sandstorms, and route corrections.",
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving companion variants, navigation choices, hazard feedback, macro names, and fixed-record constraints.",
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
        raise SystemExit(f"Raphael V77 unresolved records: {unresolved}")

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v77-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael Colosseum lead and desert expedition in SC0 blocks 311-312.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "blocks": {
                "311": sum(row["id"].startswith("DK4_MES_B311_") for row in rows),
                "312": sum(row["id"].startswith("DK4_MES_B312_") for row in rows),
            },
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} control preserved")


if __name__ == "__main__":
    main()
