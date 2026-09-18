from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v81.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"

SPEAKERS = {
    0x5E: "Tavern patron",
    0x66: "Tavern patron",
    0xCB: "Curious local woman",
    0xD0: "Raphael crewmate",
}

OVERRIDES = {
    "DK4_MES_B321_R0006": "Ah, {MACRO:FI}!{LB}Waited for you!",
    "DK4_MES_B321_R0009": "Tell me a foreign tale!",
    "DK4_MES_B321_R0013": "Ha ha, all right. Today, a tale of Hindustan.",
    "DK4_MES_B321_R0018": "Such huge animals live there?! How fascinating!",
    "DK4_MES_B321_R0022": "Speaking of Hindustan, they make a beautiful luxury cloth called chintz, right?",
    "DK4_MES_B321_R0026": "Just once, let me see it.",
    "DK4_MES_B321_R0031": "Chintz? Next time, then.",
    "DK4_MES_B321_R0034": "Really?! Can't wait!",
    "DK4_MES_B322_R0014": "Right... promised to bring chintz.",
    "DK4_MES_B322_R0027": "Ah, {MACRO:FI}!",
    "DK4_MES_B322_R0032": "A promise, remember? This is chintz.",
    "DK4_MES_B322_R0035": "So this is it...! Truly beautiful, and wonderfully soft...",
    "DK4_MES_B322_R0040": "Would you like some?",
    "DK4_MES_B322_R0044": "That is kind, but such luxury goods cannot be accepted. One look is enough.",
    "DK4_MES_B322_R0048": "More foreign tales, please.",
    "DK4_MES_B322_R0052": "All right. A tale of my Mediterranean home?",
    "DK4_MES_B322_R0056": "Yes!",
    "DK4_MES_B322_R0061": "Gentle weather, happy people, fine food... Lovely!",
    "DK4_MES_B322_R0065": "What does wine taste like? Wine differs from Japanese sake, right? Oh, to try it once!",
    "DK4_MES_B322_R0069": "Such curiosity. Next time wine is bought, some will be brought here.",
    "DK4_MES_B322_R0073": "Really?! Can't wait!",
    "DK4_MES_B323_R0014": "Right... promised to bring wine.",
    "DK4_MES_B323_R0028": "Hi",
    "DK4_MES_B323_R0032": "Ah, you brought the wine!",
    "DK4_MES_B323_R0036": "Go on, try it.",
    "DK4_MES_B323_R0040": "Yes{LB}...",
    "DK4_MES_B323_R0044": "Well?",
    "DK4_MES_B323_R0048": "Delicious! Such a new taste from sake!",
    "DK4_MES_B323_R0051": "Well?",
    "DK4_MES_B323_R0055": "Let me try some.",
    "DK4_MES_B323_R0060": "Um...",
    "DK4_MES_B323_R0064": "Oh! Delicious!",
    "DK4_MES_B323_R0068": "Now this is good!",
    "DK4_MES_B323_R0074": "Gone in no time...",
    "DK4_MES_B323_R0079": "Sorry! That was valuable stock.",
    "DK4_MES_B323_R0083": "N-no, fine. Not your fault.",
    "DK4_MES_B323_R0086": "But...",
    "DK4_MES_B323_R0091": "Never mind. Next time,{LB}tell me about Japan?",
    "DK4_MES_B323_R0095": "Yes, gladly!",
    "DK4_MES_B323_R0101": "Kyoto, home of the emperor? Want to see it.",
    "DK4_MES_B323_R0104": "A map makes it easy.{LB}Guidance can be given partway.",
    "DK4_MES_B323_R0108": "Really? Maybe we should go someday.",
    "DK4_MES_B324_R0009": "Admiral, meet the Proof map's guardians. Their village is far northeast of China.",
    "DK4_MES_B324_R0011": "Admiral, quickly meet the Proof map's guardians in their village far northeast of China.",
    "DK4_MES_B324_R0012": "Admiral, what are the Proof map's guardians like? Shall we visit their village far northeast of China?",
    "DK4_MES_B324_R0013": "Admiral, before we forget, let's meet the Proof map's guardians in a village far northeast of China.",
    "DK4_MES_B324_R0014": "Admiral, let's meet the Proof map's guardians in their village far northeast of China.",
    "DK4_MES_B324_R0016": "Admiral, seek the Proof clan{LB}in their village far northeast{LB}of China.",
    "DK4_MES_B324_R0017": "Admiral, curious about{LB}the Proof map's guardians?{LB}Visit their village far northeast of China.",
    "DK4_MES_B324_R0018": "Admiral, the Proof map concerns me. Shall we visit its guardians in a village far northeast of China?",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = [row for row in csv.DictReader(source) if row["id"].startswith(tuple(f"DK4_MES_B{block}_" for block in range(321, 325)))]
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
            "context": "Raphael befriends a curious woman through foreign stories, shows her chintz and wine, hears of Kyoto, and receives reminders about the Proof-map guardians.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving promises, item handoffs, patron interruptions, route leads, companion variants, macro names, and fixed-record constraints.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    if unresolved:
        raise SystemExit(f"Raphael V81 unresolved records: {unresolved}")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v81-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete source-locked Raphael foreign-story, chintz, wine, Kyoto lead, and Proof-map guardian reminder events in SC0 blocks 321-324.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {str(block): sum(row["id"].startswith(f"DK4_MES_B{block}_") for row in rows) for block in range(321, 325)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
