from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v39b.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
RECORD_ID = "DK4_MES_B156_R0080"


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        row = next(row for row in csv.DictReader(stream) if row["id"] == RECORD_ID)
    english = "They come,{LB}we fight."
    record = {
        "id": RECORD_ID,
        "english": f"{english}{{PAD}}",
        "speaker": "Raphael Castor",
        "context": "Raphael accepts that if Maldonado and Escante target the company, the crew will have to fight.",
        "source_meaning": "If they come, we will have no choice but to fight.",
        "localization_note": "The source begins with Shift-JIS 97 88 for 来; 0x97 must not be consumed as the officer state used by other block-156 records.",
        "qa_waivers": ["weak-line-ending", "orphan-final-line", "manual-break"],
        "manual_break_reason": "Protects progressive ASCII pair phase.",
        "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
    }
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v39-plain-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Shift-JIS-safe final Raphael response from SC0 block 156.",
        "excluded_records": {},
        "inventory": {"identified_records": 1, "translated_records": 1, "blocks": {"156": 1}},
        "records": [record],
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: 1 record")


if __name__ == "__main__":
    main()
