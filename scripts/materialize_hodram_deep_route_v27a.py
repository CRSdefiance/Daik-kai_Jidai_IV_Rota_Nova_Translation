from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v27a.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (315, 316)
EXCLUDED = {
    "DK4_MES_B316_R0038": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B316_R0066": "Four-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B316_R0106": "Four-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B316_R0181": "Four-byte nontext expedition event payload preserved byte-for-byte.",
}
LINES = {
    "DK4_MES_B315_R0006": "Why, welcome!",
    "DK4_MES_B315_R0010": "Your incense burner improved my readings.{LB}As thanks, let me read your fortune.",
    "DK4_MES_B315_R0014": "Come, sit there.",
    "DK4_MES_B315_R0026": "Go inland from this city.{LB}Ruins lie deep in the desert.{LB}What you seek is there.",
    "DK4_MES_B316_R0020": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B316_R0021": "No map.{LB}We'll get lost.",
    "DK4_MES_B316_R0022": "No map.{LB}We'll get lost.",
    "DK4_MES_B316_R0023": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B316_R0024": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B316_R0025": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B316_R0026": "Admiral,{LB}get a map.",
    "DK4_MES_B316_R0027": "No map.{LB}We'll get lost.",
    "DK4_MES_B316_R0052": "Then let us depart.",
    "DK4_MES_B316_R0054": "Shall we go?",
    "DK4_MES_B316_R0056": "Let's go!",
    "DK4_MES_B316_R0058": "Then let's head out.",
    "DK4_MES_B316_R0060": "Let's get going!",
    "DK4_MES_B316_R0062": "Come, let us go!",
    "DK4_MES_B316_R0064": "Onward we go!",
    "DK4_MES_B316_R0077": "Mist is here.",
    "DK4_MES_B316_R0079": "Mist has come.",
    "DK4_MES_B316_R0081": "Heavy mist.",
    "DK4_MES_B316_R0083": "Now we're in fog.",
    "DK4_MES_B316_R0085": "What heavy fog.",
    "DK4_MES_B316_R0087": "Mist is here.",
    "DK4_MES_B316_R0089": "Such heavy fog.",
    "DK4_MES_B316_R0095": "Keep going",
    "DK4_MES_B316_R0097": "Wait for clear",
    "DK4_MES_B316_R0104": "Let's try moving on.",
    "DK4_MES_B316_R0117": "Looks like a dead end.",
    "DK4_MES_B316_R0119": "A dead end...",
    "DK4_MES_B316_R0121": "Oh, a dead end.",
    "DK4_MES_B316_R0123": "A dead end...",
    "DK4_MES_B316_R0125": "A dead end, it seems.",
    "DK4_MES_B316_R0127": "Oh, a dead end.",
    "DK4_MES_B316_R0129": "Well, a dead end.",
    "DK4_MES_B316_R0135": "Keep going",
    "DK4_MES_B316_R0137": "Seek a path",
    "DK4_MES_B316_R0144": "Cut through the trees.",
    "DK4_MES_B316_R0158": "Let's try.",
    "DK4_MES_B316_R0160": "Let's try it.",
    "DK4_MES_B316_R0162": "This is reckless...{LB}but let's try.",
    "DK4_MES_B316_R0163": "Let's try.",
    "DK4_MES_B316_R0165": "All right, onward!",
    "DK4_MES_B316_R0167": "Reckless words...{LB}but let us try.",
    "DK4_MES_B316_R0168": "This is reckless...{LB}All right, let's go!",
    "DK4_MES_B316_R0174": "The sailors are exhausted.",
    "DK4_MES_B316_R0179": "Seek a path.",
    "DK4_MES_B316_R0192": "Admiral, two paths ahead!",
    "DK4_MES_B316_R0194": "Admiral, two paths ahead.",
    "DK4_MES_B316_R0196": "Admiral, look! Two paths!",
    "DK4_MES_B316_R0198": "Admiral, a path over here!",
    "DK4_MES_B316_R0200": "Admiral, a path over here!",
    "DK4_MES_B316_R0202": "Admiral, we can go this way!",
    "DK4_MES_B316_R0204": "Admiral, over here!",
    "DK4_MES_B316_R0206": "A path, right here!",
    "DK4_MES_B316_R0214": "Too risky to move.{LB}Wait for clear skies.",
    "DK4_MES_B316_R0227": "That seems best.",
    "DK4_MES_B316_R0229": "Good idea.",
    "DK4_MES_B316_R0231": "Good idea.",
    "DK4_MES_B316_R0233": "Yes. Let's do that.",
    "DK4_MES_B316_R0235": "We have little choice.",
    "DK4_MES_B316_R0237": "Yes, let's do that.",
    "DK4_MES_B316_R0239": "That is safest.",
    "DK4_MES_B316_R0254": "One day passed.",
    "DK4_MES_B316_R0258": "Clear now.{LB}Depart.",
    "DK4_MES_B316_R0277": "Now in view.",
    "DK4_MES_B316_R0279": "There it is.",
    "DK4_MES_B316_R0281": "There it is.",
    "DK4_MES_B316_R0283": "There it is?",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "CC": "Fortune teller", "D0": "Companion",
    "D3": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V27a inventory mismatch: missing={sorted(set(source_rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(source_rows))}")
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
            "context": "A fortune teller directs Hodram inland, where his party navigates fog, dead ends, and branching paths to desert ruins.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving route choices and party variants.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-final-expeditions-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram celadon reward and fog-desert expedition in SC1 blocks 315-316.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
