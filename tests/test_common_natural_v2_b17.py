from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
BATCH = Path("translations/common_natural_v2_b17.json")
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


def _load() -> dict[str, object]:
    value = json.loads(BATCH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _common() -> bytes:
    data = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    assert hashlib.sha256(data).hexdigest() == COMMON_SHA256
    return data


def test_block17_inventory_is_complete_and_nonoverlapping() -> None:
    batch = _load()
    safe = {str(record["id"]) for record in batch["records"]}
    blocked = {str(record["id"]) for record in batch["blocked_records"]}
    expected = {f"DK4_MES_B17_R{index:04d}" for index in range(133)}
    assert safe.isdisjoint(blocked)
    assert safe | blocked == expected
    assert len(safe) == 131
    assert blocked == {"DK4_MES_B17_R0058", "DK4_MES_B17_R0132"}
    assert batch["inventory"] == {
        "block": 17,
        "total_segments": 133,
        "japanese_bearing_segments": 132,
        "safe_translated_records": 131,
        "blocked_editorial_records": 2,
        "padding_only_segments": 1,
    }


def test_safe_block17_records_are_source_locked_and_qa_clean() -> None:
    common = _common()
    batch = _load()
    assert batch["source_file_sha256"] == COMMON_SHA256
    assert batch["translation_policy"] == "natural-dialogue-v2"
    assert batch["dialogue_profile"] == "shared-pair-live"
    rows = materialize_translation_batch(batch, common)
    authored = {str(record["id"]): record for record in batch["records"]}
    profile = get_dialogue_profile("shared-pair-live")
    assert len(rows) == 131

    for row in rows:
        record = authored[str(row["id"])]
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        waivers = set(record.get("qa_waivers", []))
        assert not [
            issue
            for issue in audit["issues"]
            if issue["severity"] in {"warning", "error"}
            and issue["code"] not in waivers
        ], row["id"]
        assert all(record["review"].values())


def test_blocked_entries_are_exhaustive_editorial_classifications() -> None:
    blocked = {str(record["id"]): record for record in _load()["blocked_records"]}
    macro = blocked["DK4_MES_B17_R0058"]
    assert macro["editorial_english"] == "{MACRO:I}C can handle diplomacy."
    assert macro["editorial_review"] is True
    assert macro["formatting_review"] is False
    assert "macro" in str(macro["blocker"]).lower()

    padding = blocked["DK4_MES_B17_R0132"]
    assert padding["source_hex"] == "2020"
    assert "padding" in str(padding["blocker"]).lower()
