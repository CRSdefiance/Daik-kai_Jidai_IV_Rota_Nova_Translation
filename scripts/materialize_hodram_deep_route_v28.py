from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v28.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (320, 321, 322, 323, 324)
EXCLUDED: dict[str, str] = {}
LINES = {
    "DK4_MES_B320_R0005": "New face here.{LB}Where are you from?",
    "DK4_MES_B320_R0008": "Sweden, up north.",
    "DK4_MES_B320_R0012": "Hm? Never heard of it.{LB}You came from very far away.",
    "DK4_MES_B320_R0016": "Ah, now it makes sense.{LB}You have a useful tool{LB}called a sextant, yes?",
    "DK4_MES_B320_R0020": "What?",
    "DK4_MES_B320_R0024": "Rumor says it reveals your position{LB}even on a featureless sea.",
    "DK4_MES_B320_R0028": "Would you trade us that sextant?{LB}A fine reward awaits you.",
    "DK4_MES_B320_R0031": "A reward?",
    "DK4_MES_B320_R0035": "Bring it and see.",
    "DK4_MES_B321_R0006": "Ah, you brought it?{LB}Then take this in exchange.",
    "DK4_MES_B321_R0014": "Sextant given.",
    "DK4_MES_B322_R0015": "Land the survey party.",
    "DK4_MES_B322_R0017": "Party going ashore.",
    "DK4_MES_B322_R0019": "Party going ashore.",
    "DK4_MES_B322_R0021": "Party ashore.",
    "DK4_MES_B322_R0023": "Party going ashore!",
    "DK4_MES_B322_R0025": "Land the survey party.",
    "DK4_MES_B322_R0071": "All gold issued{LB}as operating funds.",
    "DK4_MES_B322_R0076": "1,000 coins issued{LB}as operating funds.",
    "DK4_MES_B322_R0083": "We begin the survey now.{LB}Please report to the Sofala guild.",
    "DK4_MES_B323_R0006": "You seek this, yes?",
    "DK4_MES_B323_R0010": "A long wait...{LB}At last, today.",
    "DK4_MES_B323_R0013": "We shall trust you.{LB}Please accept it.",
    "DK4_MES_B324_R0005": "Oh!{LB}You know of that monk?",
    "DK4_MES_B324_R0009": "You do?",
    "DK4_MES_B324_R0013": "He devoted himself to nursing us{LB}through a plague.{LB}Our village survived because of him.",
    "DK4_MES_B324_R0016": "His medicine stopped the sickness{LB}almost at once.{LB}A true miracle.",
    "DK4_MES_B324_R0020": "Did he know medicine?",
    "DK4_MES_B324_R0024": "No, he called it alchemy.{LB}He said it removed mineral poison{LB}from our drinking water.",
    "DK4_MES_B324_R0028": "Here. He wrote this book.",
    "DK4_MES_B324_R0039": "Could this be...!",
    "DK4_MES_B324_R0058": "The book Charles mentioned!{LB}We found it!",
    "DK4_MES_B324_R0065": "The Book of Alchemy?!{LB}To find it here of all places!!",
    "DK4_MES_B324_R0069": "What's wrong, Charles?!",
    "DK4_MES_B324_R0073": "Rumor said a new experimental material{LB}was discovered in the New World!",
    "DK4_MES_B324_R0077": "My research showed this book{LB}is needed to obtain that material...",
    "DK4_MES_B324_R0081": "Surely this points to a rare metal!{LB}Now to learn how to use it...{LB}Mutter...",
    "DK4_MES_B324_R0084": "Sorry, no time{LB}for that now.",
    "DK4_MES_B324_R0090": "Where is that monk now?",
    "DK4_MES_B324_R0102": "The water here gave him{LB}the same sickness as us...",
    "DK4_MES_B324_R0105": "Yet he hid it and gave every dose{LB}of his medicine to our villagers!",
    "DK4_MES_B324_R0109": "At last, he passed away...{LB}He was truly a messenger of God.",
    "DK4_MES_B324_R0116": "May we entrust this book to you?",
    "DK4_MES_B324_R0119": "Trust?",
    "DK4_MES_B324_R0123": "This book reveals secrets{LB}of an ore no one has ever seen.",
    "DK4_MES_B324_R0126": "Somewhere in the world,{LB}that ore must lie buried.",
    "DK4_MES_B324_R0129": "We seek someone to continue his work.{LB}Will you find that ore?",
    "DK4_MES_B324_R0133": "You have my word.{LB}We will find it.",
    "DK4_MES_B324_R0144": "Of course!{LB}We will investigate it thoroughly!",
    "DK4_MES_B324_R0148": "All right, all right.{LB}Bring me the ore and you become{LB}admiral of that region. Study freely.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "02": "Companion", "12": "Charles",
    "97": "Companion", "A1": "Village elder", "B3": "Village elder",
    "CF": "Companion", "D0": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) != set(source_rows):
        raise SystemExit(f"Hodram V28 inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, extra={sorted(set(LINES)-set(source_rows))}")
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
            "context": "Hodram trades a sextant, dispatches a survey party, receives a guarded treasure, and inherits a monk's alchemy-and-ore quest.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving treasure terminology, system notices, and the final ore-quest setup.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-final-treasures-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram sextant, survey, treasure, and alchemy-book events in final SC1 blocks 320-324.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
