from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_sc2_b23_control_probe_v1.json"
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"

LINES = {
    "DK4_MES_B23_R0005": ("{SPEAKER:09}Next...{PAD}", "Kamil speaker state"),
    "DK4_MES_B23_R0009": ("{SPEAKER:02}Done already?{PAD}", "Lil speaker state"),
    "DK4_MES_B23_R0018": ("Need a lesson.{PAD}", "first choice label; no speaker state"),
    "DK4_MES_B23_R0020": ("Already know it.{PAD}", "second choice label; no speaker state"),
    "DK4_MES_B23_R0062": (
        "{SPEAKER:09}{MACRO:FI} is captain.{LB}Stay in the cabin.{PAD}",
        "Kamil state plus Lil-route FI expansion",
    ),
    "DK4_MES_B23_R0091": (
        "{SPEAKER:FE}Set sails with L/R.{LB}Good trim adds speed.{PAD}",
        "system tutorial panel state",
    ),
    "DK4_MES_B23_R0120": (
        "{SPEAKER:14}Let me be lookout!{PAD}",
        "Fernando speaker state",
    ),
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {row["id"]: row for row in csv.DictReader(stream)}
    if set(LINES) - set(rows):
        raise SystemExit(f"missing SC2 rows: {sorted(set(LINES) - set(rows))}")

    records = []
    for row_id, (english, purpose) in LINES.items():
        records.append(
            {
                "id": row_id,
                "english": english,
                "source_hex_guard": rows[row_id]["source_hex"],
                "context": f"Lil SC2 B23 mapping probe: {purpose}.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line"],
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-b23-probe",
        "translation_policy": "source-locked-runtime-control-probe",
        "target_locale": "en-US",
        "research_only": True,
        "scope": (
            "Seven short B23 fixtures covering 02/09/14/FE, both choice labels, "
            "and the default Lil-route FI expansion."
        ),
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(records)} probe records")


if __name__ == "__main__":
    main()
