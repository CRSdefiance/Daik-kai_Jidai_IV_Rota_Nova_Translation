from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_sc2_b22_first_screen_probe_v1.json"
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"
ROW_ID = "DK4_MES_B22_R0019"
ENGLISH = (
    "{SPEAKER:02}Hee hee! The trade permit is mine!{LB}"
    "Just watch me--time to make{LB}a fortune!{PAD}"
)


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}
    if ROW_ID not in rows:
        raise SystemExit(f"missing SC2 row: {ROW_ID}")

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-b22-first-screen-probe",
        "translation_policy": "source-locked-runtime-control-probe",
        "target_locale": "en-US",
        "research_only": True,
        "scope": "Lil's first visible Amsterdam dialogue screen only.",
        "records": [
            {
                "id": ROW_ID,
                "english": ENGLISH,
                "source_hex_guard": rows[ROW_ID]["source_hex"],
                "context": (
                    "Lil celebrates receiving her trade permit on the first visible "
                    "screen of her route."
                ),
                "qa_waivers": ["manual-break"],
                "qa_waiver_reason": (
                    "Three source-matching lines keep the boast readable in the fixed "
                    "85-byte opening record."
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        ],
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
