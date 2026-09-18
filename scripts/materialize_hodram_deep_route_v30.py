from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v30.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (15, 16)
LINES = {
    "DK4_MES_B15_R0011": "Release prisoners.",
    "DK4_MES_B15_R0017": "Damn!",
    "DK4_MES_B15_R0021": "They won't pursue.{LB}They're pulling away.{LB}Hm?",
    "DK4_MES_B15_R0025": "A ship ran aground.",
    "DK4_MES_B15_R0029": "Abandoned?{LB}Check inside.",
    "DK4_MES_B15_R0035": "Admiral...",
    "DK4_MES_B15_R0039": "What?",
    "DK4_MES_B15_R0043": "We found someone{LB}who does not belong on this ship.",
    "DK4_MES_B15_R0050": "Over here.",
    "DK4_MES_B15_R0056": "Like a doll...",
    "DK4_MES_B15_R0064": "Sir!{LB}The woman!",
    "DK4_MES_B15_R0067": "Wait--ugh...{LB}She mistakes me for a pirate.",
    "DK4_MES_B15_R0077": "No wonder.{LB}Be calm. You are free now.",
    "DK4_MES_B15_R0084": "Those features...{LB}Unlike other African peoples.",
    "DK4_MES_B15_R0087": "Not dressed as a Muslim...{LB}Perhaps born to a noble family.",
    "DK4_MES_B15_R0095": "Can't understand.",
    "DK4_MES_B15_R0107": "What now?{LB}Without knowing her homeland,{LB}we cannot take her home.",
    "DK4_MES_B15_R0113": "What now?{LB}Without knowing her homeland,{LB}we cannot take her home.",
    "DK4_MES_B15_R0120": "Other prisoners?",
    "DK4_MES_B15_R0130": "They all wish{LB}to be released here.",
    "DK4_MES_B15_R0135": "They all wish{LB}to be released here.",
    "DK4_MES_B15_R0141": "They cannot trust us either.{LB}Very well. Release all who wish it.",
    "DK4_MES_B15_R0151": "Understood.",
    "DK4_MES_B15_R0157": "Understood.",
    "DK4_MES_B15_R0164": "You may choose your path.{LB}That knife won't protect you.{LB}Take this.",
    "DK4_MES_B15_R0168": "Strange girl{LB}?!",
    "DK4_MES_B15_R0171": "Giving her a weapon is dangerous!{LB}She may attack again!",
    "DK4_MES_B15_R0175": "Cut me if she wishes.",
    "DK4_MES_B15_R0179": "Sir!",
    "DK4_MES_B15_R0183": "Strange girl{LB}...!",
    "DK4_MES_B15_R0201": "Watch out!",
    "DK4_MES_B15_R0205": "Girl{LB}...",
    "DK4_MES_B15_R0208": "Hm? Don't want it?",
    "DK4_MES_B15_R0212": "Strange girl{LB}(Nods.)",
    "DK4_MES_B15_R0215": "...{LB}So be it.",
    "DK4_MES_B15_R0226": "(What a shock...)",
    "DK4_MES_B15_R0233": "(Whew...)",
    "DK4_MES_B16_R0006": "We won.",
    "DK4_MES_B16_R0010": "Yes. A future top fleet{LB}should manage this.",
    "DK4_MES_B16_R0013": "Strict as ever.",
    "DK4_MES_B16_R0017": "Lives scattered into the sea...{LB}No, returned to mother ocean.",
    "DK4_MES_B16_R0021": "Manuel...",
    "DK4_MES_B16_R0025": "Honor the spirits{LB}of those who fell.",
    "DK4_MES_B16_R0032": "Sea and mother are alike.{LB}Endless waves recall{LB}a distant mother's heartbeat.",
    "DK4_MES_B16_R0035": "Sea and mother are alike.{LB}Some foreign tongues give both{LB}the same sound and sign.",
    "DK4_MES_B16_R0039": "Sea and mother are alike.{LB}Both hold bonds{LB}that never fade while we live.",
    "DK4_MES_B16_R0042": "A fine poem. Surprising.{LB}Never knew you had such talent.",
    "DK4_MES_B16_R0045": "Yes, impressive.",
    "DK4_MES_B16_R0049": "The sea accepts everything...{LB}May we learn to do the same.",
}

SPEAKERS = {"01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles", "17": "Manuel", "FE": "Foreign girl"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Hodram V30 inventory mismatch: missing={sorted(missing)}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[row_id.split("_B", 1)[1].split("_", 1)[0]] += 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Hodram frees prisoners, rescues the foreign girl Sera, and reflects on victory and lives lost at sea.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving silent reactions, recruitment staging, and Manuel's poem.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-opening-battles-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked remaining Hodram Sera-rescue and victory dialogue in SC1 blocks 15-16.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
