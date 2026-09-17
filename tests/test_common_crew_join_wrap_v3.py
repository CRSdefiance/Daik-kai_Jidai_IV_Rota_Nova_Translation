from __future__ import annotations

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
BATCH = Path("translations/common_crew_join_wrap_v3.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _record(data: bytes) -> bytes:
    return IlnkContainer.parse(data).blocks[4].split(b"\0")[59]


def test_crew_join_wrap_preserves_both_packed_entry_points() -> None:
    source_file = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    source = _record(source_file)
    rows = materialize_translation_batch(_load(BATCH), source_file)
    rebuilt = _record(rebuild_mesfile(source_file, rows))

    assert len(source) == len(rebuilt) == 43
    assert rebuilt[:20] == source[:20]
    assert rebuilt[20:24] == b"  %s"
    assert rebuilt[20:].rstrip() == b"  %s joined\n  your crew"
    assert rebuilt[20] == 0x20
    assert b"\n  " in rebuilt[20:]


def test_long_bergstrom_recruit_names_have_identical_controlled_wrap() -> None:
    source_file = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows = materialize_translation_batch(_load(BATCH), source_file)
    template = _record(rebuild_mesfile(source_file, rows))[20:].rstrip()

    for name in (b"Gerhard Ardelknatts", b"Charles Jean Rochefort"):
        expanded = template.replace(b"%s", name, 1)
        lines = expanded.split(b"\n")
        assert lines == [b"  " + name + b" joined", b"  your crew"]
        assert len(lines[0]) <= 31
        assert len(lines[1]) == 11


def test_v2_profile_layers_character_editor_and_shared_wrap() -> None:
    profile = _load(STACK)["profiles"]["main-menu-character-crew-wrap-v2"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/main_menu_birthday_popup_v1.json",
        "translations/main_menu_birth_label_graphics_v1.json",
        BATCH.as_posix(),
    ]
