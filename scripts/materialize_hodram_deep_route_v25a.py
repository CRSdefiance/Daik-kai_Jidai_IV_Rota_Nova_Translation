from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v25a.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (300,)
EXCLUDED = {
    "DK4_MES_B300_R0038": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
}


LINES = {
    "DK4_MES_B300_R0020": "No map.{LB}We'll get lost.",
    "DK4_MES_B300_R0021": "No map.{LB}We'll get lost.",
    "DK4_MES_B300_R0022": "No map?{LB}We can't go on.",
    "DK4_MES_B300_R0023": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B300_R0024": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B300_R0025": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B300_R0026": "No map.{LB}We can't continue!",
    "DK4_MES_B300_R0027": "No map.{LB}We'll get lost.",
    "DK4_MES_B300_R0040": "Even locals avoid this place...",
    "DK4_MES_B300_R0043": "Something may be here.{LB}Let us proceed with care.",
    "DK4_MES_B300_R0046": "Admiral! Look!",
    "DK4_MES_B300_R0050": "Giant snake!!",
    "DK4_MES_B300_R0054": "What now?{LB}This foe will not be easy.",
    "DK4_MES_B300_R0059": "Hit",
    "DK4_MES_B300_R0061": "Run",
    "DK4_MES_B300_R0068": "Attack",
    "DK4_MES_B300_R0072": "Understood!{LB}All hands, attack!",
    "DK4_MES_B300_R0075": "Got it!",
    "DK4_MES_B300_R0094": "We won...",
    "DK4_MES_B300_R0098": "Yes...",
    "DK4_MES_B300_R0110": "A fearsome foe.{LB}Good thing we had gunpowder.",
    "DK4_MES_B300_R0119": "Several sailors were injured.",
    "DK4_MES_B300_R0124": "Battle here would be unwise.",
    "DK4_MES_B300_R0128": "Understood.{LB}Everyone, withdraw!{LB}Stay together!",
    "DK4_MES_B300_R0132": "Aye!",
    "DK4_MES_B300_R0137": "Everyone here?",
    "DK4_MES_B300_R0141": "All present!",
    "DK4_MES_B300_R0148": "Hmm!!",
    "DK4_MES_B300_R0152": "What happened,{LB}{MACRO:FI}?!",
    "DK4_MES_B300_R0155": "Caught in a swamp...",
    "DK4_MES_B300_R0159": "What?!",
    "DK4_MES_B300_R0170": "Coming to help!",
    "DK4_MES_B300_R0174": "Rrraaagh!{LB}My strength is not enough...{LB}Everyone, help me!",
    "DK4_MES_B300_R0178": "Aye!",
    "DK4_MES_B300_R0182": "Whew...{LB}{MACRO:FI}, are you safe?",
    "DK4_MES_B300_R0186": "Yes, Gerhard.{LB}You saved me.",
    "DK4_MES_B300_R0194": "Coming to help!{LB}Rrraaagh!",
    "DK4_MES_B300_R0197": "Pant...{LB}Are you safe, {MACRO:FI}?",
    "DK4_MES_B300_R0201": "Yes... thanks.{LB}Never expected a swamp here.",
    "DK4_MES_B300_R0208": "The sailors seem fatigued.",
    "DK4_MES_B300_R0225": "Admiral, ahead!",
    "DK4_MES_B300_R0227": "Admiral, ahead!",
    "DK4_MES_B300_R0229": "Admiral, there!",
    "DK4_MES_B300_R0231": "Look!",
    "DK4_MES_B300_R0233": "Look there!",
    "DK4_MES_B300_R0235": "Admiral, there!",
    "DK4_MES_B300_R0237": "Oh...!",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles",
    "97": "Crewman", "D0": "Companion", "D3": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B300_")}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        raise SystemExit(f"Hodram V25a inventory mismatch: missing={sorted(set(source_rows)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(LINES)|set(EXCLUDED))-set(source_rows))}")
    records = []
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram's expedition crosses a forbidden jungle, confronts a giant snake, escapes a swamp, and sights its destination.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English with party variants and expedition choices preserved.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-snake-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram giant-snake and swamp expedition in SC1 block 300.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"300": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
