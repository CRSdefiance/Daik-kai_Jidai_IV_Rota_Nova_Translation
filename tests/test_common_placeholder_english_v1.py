from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
CLEAN = Path("work/files/COMMON/MESFILE.DK4")
ENGLISH = Path("translations/common_placeholder_english_v1.json")
CREW = Path("translations/common_crew_join_wrap_v3.json")
SQUARE = Path("translations/common_square_shipyard_repair_v1.json")
STACK = Path("translations/release_stack.json")
MATERIALIZER = Path("scripts/materialize_common_placeholder_english_v1.py")

PRINTF = re.compile(rb"%[-+0-9.*]*[sd]")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _records(data: bytes) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for block, payload in enumerate(IlnkContainer.parse(data).blocks):
        for index, record in enumerate(payload.split(b"\0")):
            result[f"DK4_MES_B{block:02d}_R{index:04d}"] = record
    return result


def _materializer_module():
    spec = importlib.util.spec_from_file_location("common_placeholder_english_v1", MATERIALIZER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_298_restored_records_are_now_fixed_size_english() -> None:
    batch = _load(ENGLISH)
    clean = _records(CLEAN.read_bytes())
    module = _materializer_module()
    records = batch["records"]
    assert isinstance(records, list)
    assert len(records) == 298
    assert {str(record["status"]) for record in records} == {"translated"}

    for record in records:
        record_id = str(record["id"])
        source = clean[record_id]
        replacement = bytes.fromhex(str(record["replacement_hex"]))
        assert len(replacement) == len(source)
        assert not contains_japanese(replacement.decode("cp932"))
        if "ascii_guard_exemption" not in record:
            assert replacement.startswith(b"  ")
            assert b"\n" not in replacement or all(
                part.startswith(b"  ") for part in replacement.split(b"\n")[1:]
            )
        key = (int(record_id[9:11]), int(record_id[13:17]))
        segment_starts = [0]
        cursor = 1
        for marker in module.PACKED_MARKERS.get(key, []):
            offset = source.find(marker.encode("cp932"), cursor)
            assert offset > 0
            segment_starts.append(offset)
            cursor = offset + 1
        for segment_index, start in enumerate(segment_starts):
            end = (
                segment_starts[segment_index + 1]
                if segment_index + 1 < len(segment_starts)
                else len(replacement)
            )
            assert all(
                len(line.rstrip()) <= 31
                for line in replacement[start:end].split(b"\n")
            )
        assert PRINTF.findall(replacement) == PRINTF.findall(source)
        assert replacement.count(b"IC") == source.count(b"IC")


def test_materializer_is_deterministic_and_packed_offsets_stay_addressable() -> None:
    module = _materializer_module()
    generated = module.materialize(BASE, CLEAN)
    checked_in = _load(ENGLISH)
    assert generated == checked_in

    clean = _records(CLEAN.read_bytes())
    translated = {
        str(record["id"]): bytes.fromhex(str(record["replacement_hex"]))
        for record in checked_in["records"]
    }
    for (block, index), markers in module.PACKED_MARKERS.items():
        record_id = f"DK4_MES_B{block:02d}_R{index:04d}"
        source = clean[record_id]
        cursor = 1
        for marker in markers:
            offset = source.find(marker.encode("cp932"), cursor)
            assert offset > 0
            record = next(row for row in checked_in["records"] if row["id"] == record_id)
            if "ascii_guard_exemption" not in record:
                assert translated[record_id][offset : offset + 2] == b"  "
            cursor = offset + 1


def test_v5_combined_common_contains_no_restored_japanese_or_generic_filler() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows: list[dict[str, object]] = []
    for path in (ENGLISH, CREW, SQUARE):
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    lowered = rebuilt.lower()
    assert b"see below" not in lowered
    assert b"give the order from the captain's cabin." not in lowered
    assert re.search(rb"(?<![a-z])ok(?![a-z])", lowered) is None

    rebuilt_records = _records(rebuilt)
    for record in _load(ENGLISH)["records"]:
        assert not contains_japanese(rebuilt_records[str(record["id"])].decode("cp932"))


def test_v5_profile_replaces_source_restoration_with_complete_english() -> None:
    profile = _load(STACK)["profiles"]["main-menu-character-placeholder-english-v5"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/main_menu_birthday_popup_v1.json",
        "translations/main_menu_birth_label_graphics_v1.json",
        ENGLISH.as_posix(),
        CREW.as_posix(),
        SQUARE.as_posix(),
    ]
