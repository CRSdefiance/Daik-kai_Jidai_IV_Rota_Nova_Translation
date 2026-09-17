from __future__ import annotations

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
BATCH = Path("translations/common_square_shipyard_repair_v1.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _records(data: bytes, block: int) -> list[bytes]:
    return IlnkContainer.parse(data).blocks[block].split(b"\0")


def _rebuilt_common() -> tuple[bytes, bytes]:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows = materialize_translation_batch(_load(BATCH), source)
    return source, rebuild_mesfile(source, rows)


def test_square_prompt_and_market_lines_are_source_sized_and_pair_safe() -> None:
    source, rebuilt = _rebuilt_common()
    for block, record in ((1, 22), (8, 4), (8, 5), (8, 6), (8, 7), (8, 24)):
        before = _records(source, block)[record]
        after = _records(rebuilt, block)[record]
        assert len(after) == len(before)
        assert b"\n\n" not in after
        assert after.startswith(b"  ")
        assert all(part.startswith(b"  ") for part in after.split(b"\n")[1:])

    prompt = _records(rebuilt, 1)[22].rstrip()
    assert prompt == b"  Choose a sign.\n  Hear market news."

    square = _records(rebuilt, 8)
    assert square[4].rstrip() == b"  %s is selling fast!"
    assert b"trade house" in square[5]
    assert b"captain" not in square[5].lower()
    assert square[7].rstrip() == b"  We only sell retail."
    assert square[24].rstrip() == b"  Free? Then I'll try it!"
    assert square[7].strip().lower() != b"ok"
    assert square[24].strip().lower() != b"ok"


def test_shipyard_repair_preserves_packed_byte_26_entry() -> None:
    source, rebuilt = _rebuilt_common()
    before = _records(source, 10)[20]
    after = _records(rebuilt, 10)[20]

    assert len(before) == len(after) == 52
    assert after[:26].rstrip() == b"  No ships need repairs!"
    assert after[26:].rstrip() == b"  Admiral, I'll help!"
    assert after.strip().lower() != b"ok"


def test_v3_profile_layers_all_reported_repairs() -> None:
    profile = _load(STACK)["profiles"]["main-menu-character-square-repair-v3"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/main_menu_birthday_popup_v1.json",
        "translations/main_menu_birth_label_graphics_v1.json",
        "translations/common_crew_join_wrap_v3.json",
        BATCH.as_posix(),
    ]
