from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import apply_arm9_fixed_batch, changed_segments
from scripts.materialize_trader_tutorial_repair import PACKED_RECORDS, build_record

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
NATURAL = Path("translations/trader_tutorial_natural_v2.json")
PACKED = Path("translations/trader_tutorial_interior_fixed_v1.json")
ARM9 = Path("translations/trader_market_map_arm9_v1.json")
TAVERN = Path("translations/tutorial_tavern_recruit_natural_v2.json")
STACK = Path("translations/release_stack.json")
BASE_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"
ARM9_SHA256 = "ba0d426b975280a51d503f38b62baeda0a7cf21fc18f962dd0ddeb2f36450dd1"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _source_files() -> tuple[bytes, bytes]:
    image = NdsImage.open(BASE)
    return image.read_file("/COMMON/MESFILE.DK4"), image.read_file("/__arm9__.bin")


def test_batches_are_locked_to_the_accepted_parent() -> None:
    assert _sha256(BASE.read_bytes()) == BASE_SHA256
    common, arm9 = _source_files()
    assert _sha256(common) == COMMON_SHA256
    assert _sha256(arm9) == ARM9_SHA256
    assert _load(NATURAL)["source_file_sha256"] == COMMON_SHA256
    assert _load(PACKED)["source_file_sha256"] == COMMON_SHA256
    assert _load(ARM9)["source_file_sha256"] == ARM9_SHA256


def test_packed_records_preserve_every_interior_entry_offset() -> None:
    common, _ = _source_files()
    blocks = IlnkContainer.parse(common).blocks
    batch = _load(PACKED)
    authored = {str(row["id"]): row for row in batch["records"]}
    assert set(authored) == set(PACKED_RECORDS)

    for row_id, spec in PACKED_RECORDS.items():
        block_index = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        record_index = int(row_id.rsplit("R", 1)[1])
        source = blocks[block_index].split(b"\0")[record_index]
        size = int(spec["size"])
        entries = list(spec["entries"])
        replacement = bytes.fromhex(str(authored[row_id]["replacement_hex"]))
        assert len(source) == len(replacement) == size
        assert replacement == build_record(size, entries)
        assert authored[row_id]["interior_entries"] == [
            {"offset": offset, "english": text} for offset, text in entries
        ]
        for offset, text in entries:
            assert replacement[offset : offset + len(text)] == text.encode("ascii")


def test_natural_records_are_pair_safe_and_qa_clean() -> None:
    common, _ = _source_files()
    batch = _load(NATURAL)
    assert batch["translation_policy"] == "natural-dialogue-v2"
    assert batch["dialogue_profile"] == "shared-pair-live"
    profile = get_dialogue_profile("shared-pair-live")
    rows = materialize_translation_batch(batch, common)
    assert len(rows) == 2
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        assert not [
            issue for issue in audit["issues"] if issue["severity"] in {"warning", "error"}
        ], row["id"]


def test_tavern_recruitment_records_are_pair_safe_and_qa_clean() -> None:
    common, _ = _source_files()
    batch = _load(TAVERN)
    rows = materialize_translation_batch(batch, common)
    assert len(rows) == 13
    blocked_ids = {
        "DK4_MES_B00_R0037",
        "DK4_MES_B00_R0039",
        "DK4_MES_B11_R0024",
        "DK4_MES_B13_R0001",
        "DK4_MES_B13_R0004",
        "DK4_MES_B13_R0007",
    }
    assert set(batch["blocked_packed_records"]) == blocked_ids
    assert {str(record["id"]) for record in batch["blocked_records"]} == blocked_ids
    assert all(record["editorial_review"] is True for record in batch["blocked_records"])
    assert all(record["formatting_review"] is False for record in batch["blocked_records"])
    profile = get_dialogue_profile("shared-pair-live")
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        assert not [
            issue
            for issue in audit["issues"]
            if issue["severity"] in {"warning", "error"}
        ], row["id"]


def test_common_rebuild_changes_only_declared_records() -> None:
    common, _ = _source_files()
    batches = [_load(NATURAL), _load(PACKED)]
    rows = [row for batch in batches for row in materialize_translation_batch(batch, common)]
    rebuilt = rebuild_mesfile(common, rows)
    expected = {
        (
            int(str(row["id"]).split("_B", 1)[1].split("_", 1)[0]),
            int(str(row["id"]).rsplit("R", 1)[1]),
        )
        for batch in batches
        for row in batch["records"]
    }
    assert changed_segments(common, rebuilt) == expected


def test_market_fee_patch_is_exact_single_line_and_keeps_placeholders() -> None:
    _, arm9 = _source_files()
    rebuilt, ids = apply_arm9_fixed_batch(ARM9, arm9)
    batch = _load(ARM9)
    record = batch["records"][0]
    offset = int(record["offset"])
    size = len(bytes.fromhex(str(record["source_hex"])))
    replacement = rebuilt[offset : offset + size]
    assert ids == ["DK4_MARKET_MAP_FEE_SINGLE_LINE"]
    assert replacement.rstrip(b"\0") == b"%s: %s coins"
    assert replacement.count(b"%s") == 2
    assert b"\n" not in replacement
    assert arm9[:offset] == rebuilt[:offset]
    assert arm9[offset + size :] == rebuilt[offset + size :]


def test_release_profile_contains_the_complete_feature() -> None:
    profile = _load(STACK)["profiles"]["raphael-tutorial-trader"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        NATURAL.as_posix(),
        PACKED.as_posix(),
        ARM9.as_posix(),
        TAVERN.as_posix(),
    ]
