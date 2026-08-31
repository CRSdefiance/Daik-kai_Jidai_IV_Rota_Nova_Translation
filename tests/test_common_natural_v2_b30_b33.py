from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
BATCH = Path("translations/common_natural_v2_b30_b33_safe.json")
BLOCKED = Path("translations/common_natural_v2_b30_b33_blocked.json")
AUDIT = Path("work/analysis/common_b30_b33_entry_audit.json")
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"
COUNTS = {30: 22, 31: 24, 32: 23, 33: 50}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _common() -> bytes:
    data = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    assert hashlib.sha256(data).hexdigest() == COMMON_SHA256
    return data


def test_block30_33_inventory_is_complete_and_nonoverlapping() -> None:
    batch, blocked, audit = _load(BATCH), _load(BLOCKED), _load(AUDIT)
    safe_ids = {str(record["id"]) for record in batch["records"]}
    blocked_ids = {str(record["id"]) for record in blocked["records"]}
    expected = {
        f"DK4_MES_B{block:02d}_R{index:04d}"
        for block, count in COUNTS.items()
        for index in range(count)
    }
    assert safe_ids.isdisjoint(blocked_ids)
    assert safe_ids | blocked_ids == expected
    assert len(safe_ids) == 17
    assert len(blocked_ids) == 102
    assert len(audit["records"]) == 119
    assert batch["source_file_sha256"] == COMMON_SHA256
    assert blocked["source_file_sha256"] == COMMON_SHA256


def test_safe_block30_33_records_materialize_and_are_qa_clean() -> None:
    batch = _load(BATCH)
    rows = materialize_translation_batch(batch, _common())
    authored = {str(record["id"]): record for record in batch["records"]}
    profile = get_dialogue_profile("shared-pair-live")
    assert len(rows) == 17
    for row in rows:
        record = authored[str(row["id"])]
        result = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        assert not [
            issue
            for issue in result["issues"]
            if issue["severity"] in {"warning", "error"}
        ], row["id"]
        assert all(record["review"].values())


def test_blocked_inventory_keeps_sources_and_reviewed_drafts() -> None:
    records = {str(record["id"]): record for record in _load(BLOCKED)["records"]}
    assert records["DK4_MES_B31_R0023"]["classification"] == "padding-only"
    assert records["DK4_MES_B33_R0049"]["classification"] == "padding-only"
    assert records["DK4_MES_B33_R0025"]["classification"] == "fixed-allocation-overflow"
    assert records["DK4_MES_B33_R0025"]["editorial_english"].startswith("A fragment")
    assert records["DK4_MES_B30_R0005"]["classification"] == "single-message-layout-blocked"
    assert records["DK4_MES_B30_R0005"]["editorial_english"].startswith("A magic lime")
    for record in records.values():
        assert record["source_hex"]
        assert record["japanese_markup"] is not None
