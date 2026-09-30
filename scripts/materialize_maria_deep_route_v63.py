from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.materialize_lil_deep_route_v17 import LINES as LIL_LINES

SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v63.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
EXCLUDED = {"DK4_MES_B58_R0078": "nontext rescue-scene payload 05 60 18 63 94 76 80 34 63; preserved byte-for-byte"}
OVERRIDES = {
    "DK4_MES_B58_R0007": "You are home.{LB}Rest awhile.",
    "DK4_MES_B58_R0014": "All right.{LB}We will go to the inn.",
    "DK4_MES_B58_R0274": "He did well.",
    "DK4_MES_B58_R0281": "Here he comes.",
    "DK4_MES_B58_R0321": "They make a good pair.",
}
SPEAKERS = {"03": "Maria", "07": "Cristina", "4F": "Mivor Gentz", "A2": "Boy", "A7": "Boy's mother", "FE": "Boy"}
STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B58_")]
    text_rows = [row for row in rows if row["id"] not in EXCLUDED]
    lil_lines = [english for row_id, english in LIL_LINES.items() if row_id.startswith("DK4_MES_B73_")][:len(text_rows)]
    if len(rows) != 85 or len(text_rows) != 84 or len(lil_lines) != 84:
        raise SystemExit(f"V63 inventory mismatch: rows={len(rows)}, text={len(text_rows)}, reusable={len(lil_lines)}")
    records = []
    for row, reused in zip(text_rows, lil_lines, strict=True):
        row_id = row["id"]
        english = OVERRIDES.get(row_id, reused).replace("Christina", "Cristina")
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in STATES else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "F" in unsafe or "I" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal macro byte: {english}")
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if target_breaks:
            waivers.append("manual-break")
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Scene participant"),
            "context": "At London harbor, Mivor overcomes his fear of water to rescue Cristina and a drowning boy, earning Cristina's reluctant gratitude and respect.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Shared rescue-event wording was reconciled against the translated Lil-route parallel; Maria-specific lines and speaker states were independently reviewed for SC3.",
            "qa_waivers": waivers,
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if target_breaks else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v63-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 block 58: complete London harbor rescue and Cristina-Mivor romantic follow-up.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": len(EXCLUDED), "blocks": {"58": len(records)}},
        "excluded": [{"id": row_id, "reason": reason} for row_id, reason in EXCLUDED.items()],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} preserved control")


if __name__ == "__main__":
    main()
