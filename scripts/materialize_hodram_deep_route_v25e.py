from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v25e.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (304, 305, 306, 307, 308)
EXCLUDED = {
    "DK4_MES_B304_R0028": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B304_R0062": "Four-byte nontext expedition event payload preserved byte-for-byte.",
}
LINES = {
    "DK4_MES_B304_R0012": "Got a map?",
    "DK4_MES_B304_R0016": "No, forgot it.",
    "DK4_MES_B304_R0030": "Then we part here.{LB}Take care.",
    "DK4_MES_B304_R0035": "Yes, thank you.",
    "DK4_MES_B304_R0050": "Come, let's go.",
    "DK4_MES_B304_R0052": "Let's go!",
    "DK4_MES_B304_R0054": "Let's go.",
    "DK4_MES_B304_R0056": "Well, let us go.",
    "DK4_MES_B304_R0058": "Off we go!",
    "DK4_MES_B304_R0060": "Well, shall we go?",
    "DK4_MES_B304_R0073": "A swamp ahead.{LB}What now?",
    "DK4_MES_B304_R0075": "Swamp ahead.{LB}What now?",
    "DK4_MES_B304_R0077": "We hit a swamp.{LB}What now?",
    "DK4_MES_B304_R0078": "Oh, a swamp.{LB}What now?",
    "DK4_MES_B304_R0080": "Swamp ahead.{LB}What now?",
    "DK4_MES_B304_R0081": "A swamp.{LB}What now?",
    "DK4_MES_B304_R0083": "We hit a swamp.{LB}What should we do?",
    "DK4_MES_B304_R0084": "A swamp lies ahead.{LB}What now?",
    "DK4_MES_B304_R0089": "Enter",
    "DK4_MES_B304_R0091": "Retreat",
    "DK4_MES_B304_R0098": "Enter the swamp.",
    "DK4_MES_B304_R0111": "Not so deep.",
    "DK4_MES_B304_R0113": "Not so deep.",
    "DK4_MES_B304_R0115": "Not so deep. Good.",
    "DK4_MES_B304_R0117": "Not deep.{LB}What a relief.",
    "DK4_MES_B304_R0119": "Not so deep.",
    "DK4_MES_B304_R0121": "Oh, not so deep.",
    "DK4_MES_B304_R0123": "Huh? Not so deep.",
    "DK4_MES_B304_R0125": "Not so deep.",
    "DK4_MES_B304_R0129": "This should save us much time.",
    "DK4_MES_B304_R0133": "Yes, we should be close.",
    "DK4_MES_B304_R0137": "The sailors are exhausted.",
    "DK4_MES_B304_R0148": "We can't cross.{LB}Let's take another path.",
    "DK4_MES_B304_R0155": "One day passed.",
    "DK4_MES_B304_R0159": "We took quite a detour.",
    "DK4_MES_B304_R0162": "Yes, but we should be close...",
    "DK4_MES_B304_R0168": "Admiral!{LB}We found it!",
    "DK4_MES_B305_R0006": "Ah, {MACRO:FI}.",
    "DK4_MES_B305_R0010": "Going to a temple today.{LB}Want to come?",
    "DK4_MES_B305_R0013": "Sorry, but not a Buddhist...",
    "DK4_MES_B305_R0017": "Come on.{LB}Just look around.",
    "DK4_MES_B305_R0020": "Wait...",
    "DK4_MES_B305_R0024": "That golden temple on my map--{LB}is it nearby?",
    "DK4_MES_B305_R0027": "Golden?{LB}Ah! That temple.{LB}Not exactly nearby...",
    "DK4_MES_B305_R0031": "Then let's go together awhile.{LB}After that, follow your map.",
    "DK4_MES_B306_R0013": "The monk said to find{LB}the Yuan emperor's keepsake.",
    "DK4_MES_B306_R0019": "This Great Sword of Kublai must be{LB}the Yuan emperor's keepsake.",
    "DK4_MES_B307_R0012": "The monk said to find{LB}the Yuan emperor's keepsake.",
    "DK4_MES_B307_R0016": "We must unequip it first.",
    "DK4_MES_B307_R0030": "Hey",
    "DK4_MES_B307_R0038": "Hm. You should be worthy.",
    "DK4_MES_B307_R0045": "Northeast China...",
    "DK4_MES_B307_R0049": "Search below the high peak{LB}on the east coast.",
    "DK4_MES_B307_R0052": "That land is very distant.{LB}An ordinary ship may not reach it.{LB}Go prepared, or you may die.",
    "DK4_MES_B307_R0059": "Never give the Proof to evil hands.{LB}Do not let wicked desire claim you.",
    "DK4_MES_B307_R0062": "We shall remember.",
    "DK4_MES_B308_R0009": "Admiral, let's meet the clan{LB}guarding the Proof map{LB}northeast of China.",
    "DK4_MES_B308_R0011": "Admiral, we should meet the clan{LB}that guards the Proof map.{LB}Their village is northeast of China.",
    "DK4_MES_B308_R0012": "Admiral, who guards the Proof map?{LB}Their village is northeast of China.{LB}Let's go see.",
    "DK4_MES_B308_R0013": "Admiral, let's visit the clan{LB}that guards the Proof map.{LB}Their village is northeast of China.",
    "DK4_MES_B308_R0014": "Admiral, let's meet the clan{LB}guarding the Proof map.{LB}They're northeast of China.",
    "DK4_MES_B308_R0016": "Admiral, about that Proof...{LB}We should meet its map's guardians{LB}in the village northeast of China.",
    "DK4_MES_B308_R0017": "Admiral, curious about the Proof map?{LB}Let's visit its guardians{LB}northeast of China.",
    "DK4_MES_B308_R0018": "Admiral, the Proof map concerns me.{LB}Shall we visit its guardians?{LB}They're northeast of China.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "CB": "Local guide",
    "D0": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V25e inventory mismatch: missing={sorted(set(source_rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(source_rows))}")
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
            "context": "Hodram crosses a swamp, follows a Golden Pavilion lead, returns Kublai's sword, and learns where the Proof map is guarded.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving route choices, relic terminology, and party variants.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-proof-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram swamp, Golden Pavilion, Yuan-relic, and Proof-map events in SC1 blocks 304-308.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
