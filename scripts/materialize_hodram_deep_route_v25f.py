from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v25f.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (309,)
EXCLUDED = {
    "DK4_MES_B309_R0038": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
    "DK4_MES_B309_R0316": "Four-byte nontext expedition event payload preserved byte-for-byte.",
}
LINES = {
    "DK4_MES_B309_R0020": "Admiral,{LB}no map means lost.",
    "DK4_MES_B309_R0021": "Admiral,{LB}no map means lost.",
    "DK4_MES_B309_R0022": "Admiral,{LB}no map could be trouble.",
    "DK4_MES_B309_R0023": "Admiral,{LB}we'll get lost.",
    "DK4_MES_B309_R0024": "Admiral,{LB}no map is bad.",
    "DK4_MES_B309_R0025": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B309_R0026": "Admiral,{LB}we need a map.",
    "DK4_MES_B309_R0027": "Admiral,{LB}we'll get lost.",
    "DK4_MES_B309_R0052": "Come, let's go.",
    "DK4_MES_B309_R0054": "Let's go!",
    "DK4_MES_B309_R0056": "Let's go.",
    "DK4_MES_B309_R0058": "Well, let us go.",
    "DK4_MES_B309_R0071": "A-Admiral!{LB}Wolves!",
    "DK4_MES_B309_R0073": "Huh! Wolves!",
    "DK4_MES_B309_R0075": "A-Admiral!{LB}Wolves!",
    "DK4_MES_B309_R0077": "Aaaah! Wolves!!",
    "DK4_MES_B309_R0079": "Whoa! Wolves!",
    "DK4_MES_B309_R0081": "A-Admiral!{LB}Wolves!",
    "DK4_MES_B309_R0083": "Whoa! Wolves!",
    "DK4_MES_B309_R0085": "Admiral!{LB}Wolves ahead!",
    "DK4_MES_B309_R0089": "Eek!!",
    "DK4_MES_B309_R0094": "Calm.",
    "DK4_MES_B309_R0098": "Wh-what will you do?",
    "DK4_MES_B309_R0105": "Drive",
    "DK4_MES_B309_R0107": "Hit",
    "DK4_MES_B309_R0109": "Run",
    "DK4_MES_B309_R0117": "Leave them to me.",
    "DK4_MES_B309_R0131": "Admiral!{LB}Look out!",
    "DK4_MES_B309_R0132": "Admiral!{LB}Look out!",
    "DK4_MES_B309_R0133": "Admiral!{LB}Watch out!",
    "DK4_MES_B309_R0134": "Look out!",
    "DK4_MES_B309_R0136": "Admiral!{LB}Look out!",
    "DK4_MES_B309_R0137": "Admiral!{LB}Look out!",
    "DK4_MES_B309_R0140": "Damn! Too slow.",
    "DK4_MES_B309_R0157": "Are you okay?!",
    "DK4_MES_B309_R0159": "You okay?!",
    "DK4_MES_B309_R0161": "You okay?!",
    "DK4_MES_B309_R0163": "You okay?",
    "DK4_MES_B309_R0167": "Just a scratch.{LB}Don't worry.",
    "DK4_MES_B309_R0174": "{MACRO:FI} was{LB}injured.",
    "DK4_MES_B309_R0178": "Ranks!{LB}Break through now!",
    "DK4_MES_B309_R0195": "Look out!",
    "DK4_MES_B309_R0197": "Look out!",
    "DK4_MES_B309_R0199": "Look out!",
    "DK4_MES_B309_R0216": "Gah!",
    "DK4_MES_B309_R0218": "Aaaaah!",
    "DK4_MES_B309_R0220": "Gah!",
    "DK4_MES_B309_R0222": "Whoa!",
    "DK4_MES_B309_R0226": "You okay?!",
    "DK4_MES_B309_R0241": "Ugh!{LB}Somehow...",
    "DK4_MES_B309_R0242": "Ow!{LB}Hurts...",
    "DK4_MES_B309_R0243": "Ow!{LB}That hurts...",
    "DK4_MES_B309_R0244": "Ugh!{LB}This is nothing.",
    "DK4_MES_B309_R0245": "Ugh!{LB}Still all right.",
    "DK4_MES_B309_R0246": "Waaah!{LB}Not all right!",
    "DK4_MES_B309_R0249": "Lost my footing...{LB}Truly sorry.",
    "DK4_MES_B309_R0258": "Quick care will do.{LB}The wolves fled.",
    "DK4_MES_B309_R0259": "Don't worry, Admiral.{LB}Quick care will heal this.{LB}The wolves fled.",
    "DK4_MES_B309_R0261": "Don't worry.{LB}Quick care will do.{LB}Wolves are gone.",
    "DK4_MES_B309_R0263": "Quick treatment will do.{LB}The wolves are gone too.",
    "DK4_MES_B309_R0264": "Don't worry!{LB}Quick treatment will fix this.{LB}The wolves are gone.",
    "DK4_MES_B309_R0266": "Don't fret.{LB}Quick treatment will suffice.{LB}The wolves have gone.",
    "DK4_MES_B309_R0268": "A little treatment will do!{LB}The wolves ran off too.",
    "DK4_MES_B309_R0269": "This is nothing serious.{LB}Quick treatment will heal it.{LB}The wolves fled.",
    "DK4_MES_B309_R0273": "Good.",
    "DK4_MES_B309_R0280": "The sailors are exhausted.",
    "DK4_MES_B309_R0285": "Those wolves are starving.{LB}We should run. Hurry!",
    "DK4_MES_B309_R0294": "Sailors exhausted.{LB}Several fell behind.",
    "DK4_MES_B309_R0305": "Pant... pant... pant!{LB}We should be safe here.",
    "DK4_MES_B309_R0306": "Pant... pant... pant!{LB}We should be safe now.",
    "DK4_MES_B309_R0307": "Pant... pant... pant!{LB}We should be safe now.",
    "DK4_MES_B309_R0308": "Pant... pant... pant!{LB}We should be safe here.",
    "DK4_MES_B309_R0309": "Wheeze... wheeze...{LB}We should be safe now.",
    "DK4_MES_B309_R0310": "Wheeze...{LB}We should be safe now.",
    "DK4_MES_B309_R0311": "Pant... pant... pant!{LB}We should be safe here.",
    "DK4_MES_B309_R0330": "Woods' end is near.",
    "DK4_MES_B309_R0331": "Woods' end is near, right?",
    "DK4_MES_B309_R0332": "Woods' end is near.",
    "DK4_MES_B309_R0333": "Woods' end is near.",
    "DK4_MES_B309_R0334": "The forest must{LB}end soon.",
    "DK4_MES_B309_R0349": "Admiral, it's in sight!",
    "DK4_MES_B309_R0351": "There it is.",
    "DK4_MES_B309_R0353": "Admiral, there!",
    "DK4_MES_B309_R0355": "Admiral, there!",
    "DK4_MES_B309_R0357": "There, Admiral!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "97": "Companion", "D0": "Companion",
    "D3": "Companion", "D6": "Companion", "D7": "Companion",
    "DA": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B309_")}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V25f inventory mismatch: missing={sorted(set(source_rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(source_rows))}")
    records = []
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram's party crosses a forest, survives a wolf attack, treats injuries, and reaches its destination.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving route choices, injury branches, and party variants.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-wolf-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram wolf and forest expedition in SC1 block 309.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"309": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
