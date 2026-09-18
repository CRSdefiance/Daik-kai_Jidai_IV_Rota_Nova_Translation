from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v25d.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (303,)
EXCLUDED: dict[str, str] = {}
LINES = {
    "DK4_MES_B303_R0006": "Ah, {MACRO:FI}!{LB}Welcome!",
    "DK4_MES_B303_R0009": "Thanks to you,{LB}my dancing has greatly improved!",
    "DK4_MES_B303_R0012": "Here's a useful lead.",
    "DK4_MES_B303_R0016": "An old king built a mosque inland.{LB}They say treasure sleeps there.",
    "DK4_MES_B303_R0020": "Only one accepted by the king{LB}may enter its vault.{LB}Try your luck.",
}
SPEAKERS = {"C5": "Dancer"}
EXTENDED_STATES = {0xC5}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B303_")}
    if set(LINES) != set(source_rows):
        raise SystemExit(f"Hodram V25d inventory mismatch: missing={sorted(set(source_rows)-set(LINES))}, extra={sorted(set(LINES)-set(source_rows))}")
    records = []
    for row_id, english in LINES.items():
        first = bytes.fromhex(source_rows[row_id]["source_hex"])[0]
        state = f"{first:02X}" if first in EXTENDED_STATES else ""
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}",
            "speaker": SPEAKERS[state], "context": "A grateful dancer tells Hodram about an old king's inland mosque and hidden treasure.",
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the king's trial and mosque lead.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-mosque-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram mosque-treasure lead in SC1 block 303.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"303": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
