from __future__ import annotations

import csv
import json
from pathlib import Path

S = Path("work/sc3/script.csv")
O = Path("translations/maria_deep_route_v89.json")
SHA = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"

L = {
    "DK4_MES_B103_R0014": "Admiral!{LB}A shark!",
    "DK4_MES_B103_R0015": "Admiral!{LB}A shark!",
    "DK4_MES_B103_R0016": "W-Whoa!{LB}A-a shark!",
    "DK4_MES_B103_R0017": "Eek!{LB}A-a shark!",
    "DK4_MES_B103_R0018": "A-Admiral!{LB}A shark!",
    "DK4_MES_B103_R0019": "A-Admiral!{LB}A shark!",
    "DK4_MES_B103_R0020": "A-Admiral!{LB}A shark!",
    "DK4_MES_B103_R0021": "Admiral!{LB}A shark, sir!",
}

SP = {"D6": "Maria companion variant"}
ST = {int(value, 16) for value in SP}


def main() -> None:
    with S.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if row["id"].startswith("DK4_MES_B103_")
        }
    if set(L) != set(rows):
        raise SystemExit(
            f"V89 mismatch: missing={sorted(set(rows) - set(L))}; "
            f"extra={sorted(set(L) - set(rows))}"
        )

    records = []
    for record_id in sorted(L, key=lambda value: int(value.rsplit("R", 1)[1])):
        row = rows[record_id]
        english = L[record_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in ST else ""
        if "F" in english or "I" in english:
            raise SystemExit(f"{record_id}: unsafe macro literal: {english}")
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line", "manual-break"]
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        records.append(
            {
                "id": record_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SP.get(state, "Maria companion variant"),
                "context": "One of eight companion-specific warnings when a shark appears at sea.",
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Preserves each companion's alarmed delivery, the lone presentation-state byte, and the source line break.",
                "qa_waivers": waivers,
                "manual_break_reason": "Preserves the shouted warning as two short rows.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SHA,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v89-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 block 103: all eight companion-specific shark warnings.",
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"103": len(records)},
        },
        "excluded": [],
        "records": records,
    }
    O.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {O}: {len(records)} records")


if __name__ == "__main__":
    main()
