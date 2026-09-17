from __future__ import annotations

import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batch, apply_pxl_label_batches

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
BATCH = Path("translations/main_menu_birthday_popup_v1.json")
STACK = Path("translations/release_stack.json")
GRAPHICS_BATCH = Path("translations/main_menu_birth_label_graphics_v1.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_birthday_popup_uses_complete_compact_heading() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(BATCH, source)
    assert ids == [
        "DK4_CHARACTER_EDIT_NAME_HEADING",
        "DK4_CHARACTER_EDIT_MIDDLE_HEADING",
        "DK4_CHARACTER_EDIT_LAST_HEADING",
        "DK4_CHARACTER_EDIT_COMPANY_HEADING",
        "DK4_CHARACTER_EDITOR_POPUP_LABELS",
        "DK4_BIRTHDAY_POPUP_COMPACT_HEADING",
        "DK4_BIRTHDAY_POPUP_HEADING_POINTER",
    ]
    assert rebuilt[0x15037C:0x150384] == b"Date\0\0\0\0"
    pointer = struct.unpack_from("<I", rebuilt, 0xA0678)[0]
    assert pointer == 0x02000000 + 0x15037C
    assert rebuilt[pointer - 0x02000000:pointer - 0x02000000 + 5] == b"Date\0"


def test_character_edit_headings_have_consistent_clear_width_and_terminators() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, _ = apply_arm9_fixed_batch(BATCH, source)
    assert rebuilt[0x14FC28:0x14FC28 + 20].split(b"\0", 1)[0] == b"Name: Edit    "
    assert rebuilt[0x14FC3C:0x14FC3C + 20].split(b"\0", 1)[0] == b"Middle: Edit  "
    assert rebuilt[0x14FC50:0x14FC50 + 20].split(b"\0", 1)[0] == b"Last: Edit    "
    assert rebuilt[0x14FC64:0x14FC64 + 20].split(b"\0", 1)[0] == b"Company: Edit "
    assert rebuilt[0x14FC78:0x14FC78 + 20].split(b"\0", 1)[0] == b"Birthday: Edit"


def test_main_menu_birthday_profile_is_minimal() -> None:
    profile = _load(STACK)["profiles"]["main-menu-birthday-v1"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        BATCH.as_posix(),
        "translations/main_menu_birth_label_graphics_v1.json",
    ]


def test_birth_field_graphic_is_source_locked_and_rebuilt() -> None:
    source = NdsImage.open(BASE).read_file("/_pxl/charselect.pxl")
    rebuilt, ids = apply_pxl_label_batches([GRAPHICS_BATCH], source)
    assert ids == ["DK4_CHARACTER_BIRTH_FIELD_LABEL"]
    assert rebuilt != source
    assert len(rebuilt) == len(source)
    record = _load(GRAPHICS_BATCH)["records"][0]
    assert record["text"] == "Birth"
    assert record["box"] == [0, 299, 48, 312]
