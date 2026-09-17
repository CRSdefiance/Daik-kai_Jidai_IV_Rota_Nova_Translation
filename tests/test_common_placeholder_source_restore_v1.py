from __future__ import annotations

import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
CLEAN = Path("work/files/COMMON/MESFILE.DK4")
RESTORE = Path("translations/common_placeholder_source_restore_v1.json")
CREW = Path("translations/common_crew_join_wrap_v3.json")
SQUARE = Path("translations/common_square_shipyard_repair_v1.json")
STACK = Path("translations/release_stack.json")

OK_TOKEN = re.compile(rb"(?<![a-z])ok(?![a-z])", re.IGNORECASE)
CAPTAIN_FALLBACK = b"give the order from the captain's cabin."


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _record_map(data: bytes) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for block_index, block in enumerate(IlnkContainer.parse(data).blocks):
        for record_index, record in enumerate(block.split(b"\0")):
            result[f"DK4_MES_B{block_index:02d}_R{record_index:04d}"] = record
    return result


def test_restore_inventory_is_exact_clean_source_and_disjoint_from_overrides() -> None:
    batch = _load(RESTORE)
    clean = _record_map(CLEAN.read_bytes())
    records = batch["records"]
    assert isinstance(records, list)
    assert len(records) == 298
    assert batch["placeholder_counts"] == {
        "literal ok": 48,
        "see below": 212,
        "unrelated captain-cabin fallback": 38,
    }

    restored_ids = {str(record["id"]) for record in records}
    override_ids = {
        str(record["id"])
        for path in (CREW, SQUARE)
        for record in _load(path)["records"]
    }
    assert restored_ids.isdisjoint(override_ids)
    for record in records:
        record_id = str(record["id"])
        assert bytes.fromhex(str(record["replacement_hex"])) == clean[record_id]


def test_v4_common_has_no_known_generic_fallbacks() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows: list[dict[str, object]] = []
    for path in (RESTORE, CREW, SQUARE):
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)

    assert b"see below" not in rebuilt.lower()
    assert CAPTAIN_FALLBACK not in rebuilt.lower()
    for block in IlnkContainer.parse(rebuilt).blocks:
        for record in block.split(b"\0"):
            assert OK_TOKEN.search(record) is None


def test_v4_profile_layers_source_restoration_before_english_overrides() -> None:
    profile = _load(STACK)["profiles"]["main-menu-character-placeholder-cleanup-v4"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/main_menu_birthday_popup_v1.json",
        "translations/main_menu_birth_label_graphics_v1.json",
        RESTORE.as_posix(),
        CREW.as_posix(),
        SQUARE.as_posix(),
    ]
