from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
RECOVERY_ROM = ROOT / "out/common_gameplay_natural_v2_b21_backup.nds"
OUT = ROOT / "translations/common_natural_v2_b20.json"
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"
RECOVERY_SHA256 = "ee42147105f2b872c93b5f73cf5576d6ead1c06b7b2efe4b9c4e0cd4247c0c94"


def rows(rom_path: Path) -> dict[int, object]:
    common = NdsImage.open(rom_path).read_file("/COMMON/MESFILE.DK4")
    return {
        row.segment_index: row
        for row in iter_mesfile_records(common, include_non_japanese=True)
        if row.block_index == 20
    }


def main() -> None:
    base_common = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    if sha256(base_common).hexdigest() != COMMON_SHA256:
        raise SystemExit("canonical COMMON source lock mismatch")
    if sha256(RECOVERY_ROM.read_bytes()).hexdigest() != RECOVERY_SHA256:
        raise SystemExit("B20/B21 recovery ROM hash mismatch")

    base_rows = rows(BASE)
    recovered_rows = rows(RECOVERY_ROM)
    if set(base_rows) != set(recovered_rows) or len(base_rows) != 102:
        raise SystemExit("unexpected block 20 record inventory")

    records: list[dict[str, object]] = []
    blocked: list[str] = []
    for index in sorted(base_rows):
        before = base_rows[index]
        after = recovered_rows[index]
        row_id = f"DK4_MES_B20_R{index:04d}"
        if before.raw_bytes == after.raw_bytes:
            blocked.append(row_id)
            continue
        if len(before.raw_bytes) != len(after.raw_bytes):
            raise SystemExit(f"{row_id}: recovered allocation changed")
        records.append(
            {
                "id": row_id,
                "english": after.text.rstrip().replace("{LB} ", "{LB}") + "{PAD}",
                "speaker": "Context-dependent crew member or shared system voice",
                "context": "Shared block 20: health, morale, battle readiness, and allied-fleet reports.",
                "source_meaning": "Recovered from the previously audited block 20 editorial build.",
                "localization_note": "Exact-size recovery from the hash-locked integrated candidate built before the source batch was lost.",
                "qa_waivers": ["manual-break"] if "{LB}" in after.text else [],
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
        "content_type": "ilnk-recovered-fixed-text-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": COMMON_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "shared-pair-live",
        "translation_policy": "natural-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Recovered, previously audited safe records from shared gameplay block 20",
        "recovery_rom_sha256": RECOVERY_SHA256,
        "blocked_packed_records": blocked,
        "blocked_reason": "These records were deliberately unchanged in the audited candidate because they contain packed entries or unresolved structure.",
        "records": records,
    }
    if len(records) != 90 or len(blocked) != 12:
        raise SystemExit(f"unexpected recovery counts: {len(records)} translated, {len(blocked)} blocked")
    OUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(records)} recovered safe records, {len(blocked)} blocked")


if __name__ == "__main__":
    main()
