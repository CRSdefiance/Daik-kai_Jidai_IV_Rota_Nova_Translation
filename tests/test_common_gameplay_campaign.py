from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

LEGACY_BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
CLEAN = Path("work/clean.nds")
BATCH = Path("translations/common_source_restored_b15_single_entry_v1.json")
STACK = Path("translations/release_stack.json")
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_b15_campaign_accounts_for_every_nonblank_record() -> None:
    batch = load(BATCH)
    records = batch["records"]
    authored = {str(record["id"]) for record in records}
    blocked = {str(value) for value in batch["blocked_packed_records"]}
    expected = {f"DK4_MES_B15_R{index:04d}" for index in range(67)}

    assert len(records) == len(authored) == 46
    assert len(blocked) == 21
    assert not authored & blocked
    assert authored | blocked == expected
    assert "DK4_MES_B15_R0067" not in authored | blocked


def test_b15_safe_replacements_are_exact_size_source_reviewed_and_not_filler() -> None:
    baseline_common = NdsImage.open(LEGACY_BASE).read_file("/COMMON/MESFILE.DK4")
    clean_common = NdsImage.open(CLEAN).read_file("/COMMON/MESFILE.DK4")
    assert hashlib.sha256(baseline_common).hexdigest() == COMMON_SHA256
    baseline_records = IlnkContainer.parse(baseline_common).blocks[15].split(b"\0")
    clean_records = IlnkContainer.parse(clean_common).blocks[15].split(b"\0")
    batch = load(BATCH)
    unchanged = {str(value) for value in batch["unchanged_records"]}

    forbidden = ("see below", "another strategy", "the scheme is ready", "ok")
    for record in batch["records"]:
        row_id = str(record["id"])
        record_index = int(row_id.rsplit("R", 1)[1])
        replacement = bytes.fromhex(str(record["replacement_hex"]))
        assert len(replacement) == len(baseline_records[record_index])
        assert len(replacement) == len(clean_records[record_index])
        if row_id in unchanged:
            assert replacement == baseline_records[record_index]
        else:
            assert replacement != baseline_records[record_index]
        english = str(record["english"]).lower()
        assert not any(value in english for value in forbidden)
        assert str(record["source_meaning"]).strip()
        assert str(record["localization_note"]).strip()
        assert all(record["review"].values())


def test_common_campaign_profile_extends_interface_polish() -> None:
    profiles = load(STACK)["profiles"]
    interface = profiles["interface-polish-v1"]["batches"]
    campaign = profiles["common-gameplay-natural-v2"]
    assert campaign["status"] == "accepted-baked"
    assert campaign["batches"][: len(interface)] == interface
    assert campaign["batches"][len(interface) :] == [
        BATCH.as_posix(),
        "translations/common_natural_v2_b16_safe.json",
        "translations/common_natural_v2_b17.json",
        "translations/common_natural_v2_b18.json",
        "translations/common_natural_v2_b19.json",
        "translations/common_natural_v2_b20.json",
        "translations/common_natural_v2_b21_safe.json",
        "translations/common_natural_v2_b22_safe.json",
        "translations/common_natural_v2_b23_safe.json",
        "translations/common_natural_v2_b24_safe.json",
        "translations/common_natural_v2_b25_safe.json",
        "translations/common_natural_v2_b26_safe.json",
        "translations/common_natural_v2_b27_safe.json",
        "translations/common_natural_v2_b28_b29_b34_safe_qa.json",
        "translations/common_natural_v2_b30_b33_safe.json",
        "translations/common_natural_v2_b35_safe.json",
        "translations/common_natural_v2_b36_safe.json",
        "translations/common_natural_v2_b38_safe.json",
        "translations/common_natural_v2_b39_safe.json",
    ]
