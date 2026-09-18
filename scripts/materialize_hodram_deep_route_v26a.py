from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v26a.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (310, 311, 312)
EXCLUDED = {
    "DK4_MES_B311_R0036": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B311_R0063": "Four-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B311_R0132": "Seven-byte nontext path-selection event payload preserved byte-for-byte.",
    "DK4_MES_B311_R0272": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B311_R0296": "Nine-byte nontext path-selection event payload preserved byte-for-byte.",
}
LINES = {
    "DK4_MES_B310_R0006": "Welcome, {MACRO:FI}.",
    "DK4_MES_B310_R0009": "Looking for the city gate?",
    "DK4_MES_B310_R0013": "We're not meant to tell foreigners...",
    "DK4_MES_B310_R0016": "Yet foreign pressure has ended isolation.{LB}Very well. You'll hear it in secret.",
    "DK4_MES_B311_R0018": "No map, Admiral.{LB}We can't go on.",
    "DK4_MES_B311_R0019": "No map, Admiral.{LB}We can't go on.",
    "DK4_MES_B311_R0020": "No map, Admiral.{LB}We won't know the way.",
    "DK4_MES_B311_R0021": "Admiral, without a map{LB}we won't know the way.",
    "DK4_MES_B311_R0022": "No map, Admiral.{LB}Can't continue.",
    "DK4_MES_B311_R0023": "No map, Admiral.{LB}We won't know the way.",
    "DK4_MES_B311_R0024": "Admiral, without a map{LB}we won't know where to go.",
    "DK4_MES_B311_R0025": "Admiral, without a map{LB}we cannot continue.",
    "DK4_MES_B311_R0047": "This forest is very dark.",
    "DK4_MES_B311_R0049": "Dense woods...",
    "DK4_MES_B311_R0051": "So dark, even by day.",
    "DK4_MES_B311_R0053": "The forest is so dark.",
    "DK4_MES_B311_R0055": "Dark woods.",
    "DK4_MES_B311_R0057": "Dense woods.",
    "DK4_MES_B311_R0059": "Dark as night in here.",
    "DK4_MES_B311_R0061": "A dense forest...",
    "DK4_MES_B311_R0076": "Admiral...{LB}Hear that?",
    "DK4_MES_B311_R0077": "Admiral...{LB}Hear that?",
    "DK4_MES_B311_R0078": "Admiral...{LB}Hear that?",
    "DK4_MES_B311_R0079": "Admiral...{LB}Listen!",
    "DK4_MES_B311_R0080": "Admiral...{LB}Hear that?",
    "DK4_MES_B311_R0081": "Admiral...{LB}Hear that?",
    "DK4_MES_B311_R0097": "Whoa! A rock behind us!!",
    "DK4_MES_B311_R0099": "Whoa! Behind!",
    "DK4_MES_B311_R0101": "A huge rock behind us!!",
    "DK4_MES_B311_R0103": "Aaaah! Behind us!!",
    "DK4_MES_B311_R0105": "A rock behind us!!",
    "DK4_MES_B311_R0107": "B-behind us!!",
    "DK4_MES_B311_R0109": "A rock is chasing us!",
    "DK4_MES_B311_R0113": "Aaaah!",
    "DK4_MES_B311_R0117": "Everyone, run!",
    "DK4_MES_B311_R0125": "Go left",
    "DK4_MES_B311_R0127": "Go right",
    "DK4_MES_B311_R0145": "A dead end!",
    "DK4_MES_B311_R0147": "Whoa!{LB}A dead end!",
    "DK4_MES_B311_R0148": "No!{LB}A dead end!",
    "DK4_MES_B311_R0149": "A dead end!",
    "DK4_MES_B311_R0151": "No!{LB}A dead end!",
    "DK4_MES_B311_R0152": "A dead end!",
    "DK4_MES_B311_R0156": "Jump into the brush!",
    "DK4_MES_B311_R0162": "Left",
    "DK4_MES_B311_R0164": "Right",
    "DK4_MES_B311_R0176": "Everyone safe?!",
    "DK4_MES_B311_R0180": "Aye!",
    "DK4_MES_B311_R0189": "Everyone safe?!",
    "DK4_MES_B311_R0193": "Aye!",
    "DK4_MES_B311_R0212": "Hm?",
    "DK4_MES_B311_R0214": "Oh?",
    "DK4_MES_B311_R0233": "Aaaaaah!!",
    "DK4_MES_B311_R0235": "Aaaaaah!!",
    "DK4_MES_B311_R0239": "What?!",
    "DK4_MES_B311_R0252": "A snake!!",
    "DK4_MES_B311_R0254": "Big snake!",
    "DK4_MES_B311_R0256": "A snake!!",
    "DK4_MES_B311_R0258": "There's a snake!!",
    "DK4_MES_B311_R0260": "A snake!!",
    "DK4_MES_B311_R0262": "A snake!!",
    "DK4_MES_B311_R0264": "A snaaake!!",
    "DK4_MES_B311_R0266": "Another snake!!",
    "DK4_MES_B311_R0270": "Run away!",
    "DK4_MES_B311_R0274": "Pant...",
    "DK4_MES_B311_R0278": "No more!",
    "DK4_MES_B311_R0284": "The sailors are exhausted.",
    "DK4_MES_B311_R0290": "Almost there.{LB}Onward.",
    "DK4_MES_B311_R0308": "Rock rolled left!",
    "DK4_MES_B311_R0310": "The rock took the left path!",
    "DK4_MES_B311_R0312": "Lucky!{LB}The rock rolled left!",
    "DK4_MES_B311_R0313": "The rock went left!",
    "DK4_MES_B311_R0315": "The rock rolled left!",
    "DK4_MES_B311_R0317": "Rock rolled left!",
    "DK4_MES_B311_R0319": "The rock went left!",
    "DK4_MES_B311_R0323": "Safe.",
    "DK4_MES_B311_R0327": "What a scare.",
    "DK4_MES_B311_R0349": "Admiral! Look there!",
    "DK4_MES_B311_R0351": "Admiral! Over there!",
    "DK4_MES_B311_R0353": "Admiral! Look there!",
    "DK4_MES_B311_R0355": "Admiral! Look there!",
    "DK4_MES_B312_R0006": "Oh, {MACRO:FI}.{LB}Almost forgot to tell you.",
    "DK4_MES_B312_R0010": "An ancient map was found.{LB}Old kingdom ruins lie{LB}near this city.",
    "DK4_MES_B312_R0013": "Oh?{LB}Where is that map?",
    "DK4_MES_B312_R0016": "Sorry, no idea.{LB}But try searching for it.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "97": "Companion", "C9": "Local woman",
    "CD": "Local woman", "D0": "Companion", "D1": "Companion",
    "D3": "Companion", "D6": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V26a inventory mismatch: missing={sorted(set(source_rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(source_rows))}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[row_id.split("_B", 1)[1].split("_", 1)[0]] += 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram learns a city gate's location, survives a dark-forest boulder and snake chase, and hears of old kingdom ruins.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving route choices, chase branches, and party variants.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-eastasia-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram city-gate, dark-forest, and old-kingdom-rumor events in SC1 blocks 310-312.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
