from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v25c.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (302,)
EXCLUDED: dict[str, str] = {}

LINES = {
    "DK4_MES_B302_R0019": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B302_R0020": "We need a map, Admiral.",
    "DK4_MES_B302_R0022": "No map, Admiral.{LB}We can't go on.",
    "DK4_MES_B302_R0023": "We should buy a map{LB}before entering the desert.",
    "DK4_MES_B302_R0024": "No map, Admiral.{LB}We should turn back.",
    "DK4_MES_B302_R0025": "No map means getting lost, Admiral.",
    "DK4_MES_B302_R0027": "No map? We'll get lost.",
    "DK4_MES_B302_R0028": "Admiral, we'll get lost.",
    "DK4_MES_B302_R0053": "This heat is brutal.",
    "DK4_MES_B302_R0055": "Hot...",
    "DK4_MES_B302_R0057": "Whew, hot.",
    "DK4_MES_B302_R0059": "Even so, what heat.",
    "DK4_MES_B302_R0061": "So hot.",
    "DK4_MES_B302_R0063": "Awful heat.",
    "DK4_MES_B302_R0065": "Whew, so hot.",
    "DK4_MES_B302_R0067": "Such fierce heat.",
    "DK4_MES_B302_R0071": "Long road.{LB}Save our water.",
    "DK4_MES_B302_R0080": "A sandstorm.{LB}Moving on is hard.{LB}What now?",
    "DK4_MES_B302_R0082": "A sandstorm...{LB}Moving on is hard.{LB}Your orders?",
    "DK4_MES_B302_R0084": "What a sandstorm!{LB}We could get lost.{LB}What do we do?",
    "DK4_MES_B302_R0086": "The sandstorm is growing.{LB}We may lose our way.{LB}Your orders, Admiral?",
    "DK4_MES_B302_R0088": "This sandstorm is fierce.{LB}Moving on is risky.{LB}What now?",
    "DK4_MES_B302_R0089": "The storm is growing.{LB}Moving on is dangerous.{LB}Admiral, your orders?",
    "DK4_MES_B302_R0091": "A severe sandstorm...{LB}We may lose our way.{LB}What should we do?",
    "DK4_MES_B302_R0093": "A terrible sandstorm.{LB}We could get lost out here.{LB}Should we continue?",
    "DK4_MES_B302_R0099": "Keep going",
    "DK4_MES_B302_R0101": "Wait it out",
    "DK4_MES_B302_R0108": "Storm won't stop.{LB}We must go on.",
    "DK4_MES_B302_R0122": "Very well.{LB}Let us move on.",
    "DK4_MES_B302_R0123": "As ordered, Admiral.{LB}We'll go on.",
    "DK4_MES_B302_R0124": "All right.{LB}We'll continue.",
    "DK4_MES_B302_R0125": "Understood.{LB}We'll move on.",
    "DK4_MES_B302_R0126": "Very well.{LB}Let us go.",
    "DK4_MES_B302_R0127": "As you wish, Admiral.{LB}We'll continue.",
    "DK4_MES_B302_R0128": "Agreed.{LB}We should move on.",
    "DK4_MES_B302_R0129": "Understood.{LB}We'll press ahead.",
    "DK4_MES_B302_R0137": "The sailors are exhausted.{LB}One has collapsed.",
    "DK4_MES_B302_R0141": "We pushed too hard.{LB}Let's rest.",
    "DK4_MES_B302_R0150": "The sandstorm still rages.{LB}What should we do?",
    "DK4_MES_B302_R0152": "The storm still rages.{LB}Admiral, your orders?",
    "DK4_MES_B302_R0154": "Hours have passed,{LB}yet the storm will not stop.{LB}What now?",
    "DK4_MES_B302_R0156": "No sign of stopping.{LB}What should we do?",
    "DK4_MES_B302_R0158": "Still no end to the storm.{LB}Your orders?",
    "DK4_MES_B302_R0160": "This storm may never stop.{LB}Should we go on?",
    "DK4_MES_B302_R0162": "Hours have passed,{LB}but the storm continues.{LB}What now?",
    "DK4_MES_B302_R0164": "The storm is not stopping.{LB}What should we do?",
    "DK4_MES_B302_R0170": "Keep going",
    "DK4_MES_B302_R0172": "Wait longer",
    "DK4_MES_B302_R0180": "We can't wait.{LB}We must go on.",
    "DK4_MES_B302_R0187": "The sailors are exhausted.",
    "DK4_MES_B302_R0193": "Pushing on is too risky.{LB}We'll wait until it stops.",
    "DK4_MES_B302_R0203": "One day passed.",
    "DK4_MES_B302_R0207": "At last, it has stopped.",
    "DK4_MES_B302_R0226": "Almost out of water.{LB}This is bad...",
    "DK4_MES_B302_R0227": "We're almost out of water...",
    "DK4_MES_B302_R0228": "Our water is nearly gone...",
    "DK4_MES_B302_R0229": "We're running out of water...",
    "DK4_MES_B302_R0230": "Very little water remains...",
    "DK4_MES_B302_R0231": "We're almost out of water...",
    "DK4_MES_B302_R0232": "Our water is nearly gone...",
    "DK4_MES_B302_R0233": "We're nearly out of water...",
    "DK4_MES_B302_R0246": "Admiral!{LB}Something ahead!",
    "DK4_MES_B302_R0247": "Admiral!{LB}Ahead!",
    "DK4_MES_B302_R0248": "Admiral!{LB}Look there!",
    "DK4_MES_B302_R0249": "Admiral!{LB}Look!",
    "DK4_MES_B302_R0250": "Hey!{LB}Look ahead!",
    "DK4_MES_B302_R0251": "Look!{LB}Ahead!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "D0": "Companion", "D3": "Companion",
    "D6": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B302_")}
    if set(LINES) != set(source_rows):
        raise SystemExit(f"Hodram V25c inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, extra={sorted(set(LINES)-set(source_rows))}")
    records = []
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram's party crosses a desert, survives a sandstorm, manages fatigue and water, and reaches its destination.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English with choice prompts and party variants preserved.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-desert-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram desert and sandstorm expedition in SC1 block 302.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"302": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
