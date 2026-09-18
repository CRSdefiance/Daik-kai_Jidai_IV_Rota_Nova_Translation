from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import (
    apply_arm9_fixed_batches,
    apply_pxl_native_label_batch,
    validate_ascii_guard_policy,
    validate_fixed_allocation_policy,
    validate_fixed_text_layout_policy,
)
from scripts.audit_release_text_layout import audit_ilnk

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
ENTITY = Path("translations/entity_ship_names_arm9_v2.json")
UI = Path("translations/shipyard_guild_mystery_ui_arm9_v2.json")
COMMON = [
    Path("translations/common_shipyard_layout_v2.json"),
    Path("translations/guild_item_descriptions_layout_v3.json"),
    Path("translations/common_mystery_items_v1.json"),
]
RUNTIME = Path("translations/common_runtime_layout_v4.json")
GLOBAL_LAYOUT = Path("translations/common_global_layout_v1.json")
PERSON_ARM9 = Path("translations/person_info_arm9_v1.json")
PERSON_GRAPHICS = Path("translations/person_info_graphics_v1.json")
ASSIGN_GRAPHICS = Path("translations/assign_sailors_graphics_v3.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _c_string(data: bytes, offset: int) -> bytes:
    return data[offset : data.index(0, offset)]


def _has_japanese(text: str) -> bool:
    return any("\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff" for char in text)


def test_live_entity_and_ship_name_pointers_are_complete_english_c_strings() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, _ = apply_arm9_fixed_batches([ENTITY, UI], source)

    assert _c_string(rebuilt, struct.unpack_from("<I", rebuilt, 0x11E0B0)[0] - 0x02000000) == b"Arnhem"
    assert _c_string(rebuilt, struct.unpack_from("<I", rebuilt, 0x121920)[0] - 0x02000000) == b"Shipwright"
    assert _c_string(rebuilt, struct.unpack_from("<I", rebuilt, 0x121600)[0] - 0x02000000) == b"Shopkeeper"

    for pointer_offset, expected in {
        0x120D44: "Ｆerog",
        0x120DA8: "Ｆerid",
        0x120E00: "Ｆernando",
        0x120FC8: "Ｆazul",
        0x120FE0: "Ｆernan",
        0x121088: "Ｆong",
        0x121264: "Ｆlahven",
        0x1221C0: "Ｆollower",
        0x1222C0: "Ｆrancisca",
        0x1223C0: "Ｆaticia",
    }.items():
        target = struct.unpack_from("<I", rebuilt, pointer_offset)[0] - 0x02000000
        raw = _c_string(rebuilt, target)
        assert not raw.startswith(b"F")
        assert raw.decode("cp932") == expected

    for pointer_offset in range(0x121600, 0x122501, 4):
        target = struct.unpack_from("<I", rebuilt, pointer_offset)[0] - 0x02000000
        if not (0x15B000 <= target < 0x15E400 or 0x1720A8 <= target < 0x172464):
            continue
        raw = _c_string(rebuilt, target)
        text = raw.decode("cp932")
        assert not _has_japanese(text), (hex(pointer_offset), text)


def test_shipyard_guild_and_mystery_ui_fit_declared_windows() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, _ = apply_arm9_fixed_batches([ENTITY, UI], source)

    assert _c_string(rebuilt, 0x11B5EC) == b"Undo"
    assert _c_string(rebuilt, 0x133154) == b"Refit"
    pitch = _c_string(rebuilt, 0x143D20).decode("ascii")
    assert pitch.splitlines() == [
        "You're in luck!",
        " This old map may lead",
        " to legendary treasure.",
    ]
    assert max(len(line.lstrip(" ")) for line in pitch.splitlines()) <= 31
    assert _c_string(rebuilt, 0x13C2C8) == b"Ruin Map"
    assert _c_string(rebuilt, 0x13C2D4) == b"Old Map"
    assert _c_string(rebuilt, 0x1484CC) == b"%s %s"
    assert _c_string(rebuilt, 0x14FBBC) == b"%s %s"
    assert _c_string(rebuilt, 0x1484DC) == b" "
    assert _c_string(rebuilt, 0x1484E0) == b" "
    assert _c_string(rebuilt, 0x16BD88) == b"Ancient Map"
    assert _c_string(rebuilt, 0x16BE00) == b"%s Map 1"
    assert _c_string(rebuilt, 0x16BEA4) == b"Eerie Mask"
    assert _c_string(rebuilt, 0x133F28) == b"Assigned to flagship first."
    assert _c_string(rebuilt, 0x133F48) == b"Sailors assigned evenly."
    assert _c_string(rebuilt, 0x133F68) == b"Minimum sailors assigned."


def test_common_layout_repairs_remove_visible_guards_and_translate_map_family() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows: list[dict[str, object]] = []
    for path in COMMON:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = IlnkContainer.parse(rebuild_mesfile(source, rows)).blocks

    b15 = rebuilt[15].split(b"\0")[63]
    assert b15.rstrip() == b"Lateen sails favor\nheadwinds.\nNo square sail behind."
    assert all(len(line) <= 24 for line in b15.rstrip().splitlines())

    b32 = rebuilt[32].split(b"\0")
    assert b32[12][89:181].startswith(b"Rainbow-colored")
    assert b32[13][77:177].startswith(b"A graceful watercolor")
    assert b32[12][89:181].rstrip().splitlines() == [
        b"Rainbow-colored glass marbles,",
        b"  crafted by a secret process",
        b"  known only to their makers.",
    ]
    assert b32[19].startswith(b"  A light silk robe")

    b33 = rebuilt[33].split(b"\0")
    assert b33[7].startswith(b"  South England map with a")
    assert b33[24][69:].startswith(b"  Map fragment. Collect all four.")
    for row in range(25, 44):
        assert b33[row].startswith(b"  Map fragment. Collect all four.")
    for row in range(44):
        assert not _has_japanese(b33[row].decode("cp932")), row

    b40 = rebuilt[40].split(b"\0")
    assert b40[25][:69].startswith(b" A priest's stone mask")
    assert b40[25][69:].startswith(b" A crimson crystal")
    assert b40[30].startswith(b" A gigantic red spear.")
    assert b40[23].rstrip().splitlines() == [
        b" A strange gem colored like",
        b"  a living flame.",
    ]
    for row in range(31):
        assert not _has_japanese(b40[row].decode("cp932")), row


def test_runtime_layout_repairs_preserve_entries_and_remove_reported_failures() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rebuilt = IlnkContainer.parse(
        rebuild_mesfile(source, materialize_translation_batch(_load(RUNTIME), source))
    ).blocks

    b0 = rebuilt[0].split(b"\0")
    assert b0[54].startswith(b"  Sailors still unassigned.")
    assert b"%s sailors" not in b0[54]

    b4 = rebuilt[4].split(b"\0")[59]
    assert b4[20:].startswith(b"  %s joined\n  your crew")

    b13 = rebuilt[13].split(b"\0")
    assert b"  Sold out." in b13[26]
    assert b13[30].startswith(b"  Thank you!")
    assert b13[38].find(b"  You have nothing to sell.") > 0
    assert b13[40].startswith(b"  I'll pay %s coins.\n  Deal?")
    assert b13[49].startswith(b"  Thank you!")
    assert b"We still nee" not in b13[49]
    for row in range(58):
        assert not _has_japanese(b13[row].decode("cp932")), row


def test_fixed_text_policy_rejects_future_termination_wrap_and_indent_regressions() -> None:
    bad_c_string = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "fixed_text_policy": {"require_c_string_termination": True},
        "records": [
            {"id": "FULL", "source_hex": "00000000", "english": "Four", "string_kind": "c-string"}
        ],
    }
    with pytest.raises(ValueError, match="terminator"):
        validate_fixed_text_layout_policy(Path("bad.json"), bad_c_string)

    bad_layout = {
        "fixed_text_policy": {"maximum_prose_line_characters": 8, "forbid_visible_leading_space": True},
        "records": [{"id": "WRAP", "english": " too long"}],
    }
    with pytest.raises(ValueError, match="exceeds|indent"):
        validate_fixed_text_layout_policy(Path("bad.json"), bad_layout)

    missing_guard = {
        "fixed_allocation_policy": "screen-entry-layout-v1",
        "records": [{
            "id": "NO_GUARD",
            "replacement_hex": b"Text\n next".hex(),
            "translated_ranges": [[0, 10]],
            "entry_offsets": [0],
            "entry_guard_bytes": 1,
            "linebreak_guard_bytes": 1,
        }],
    }
    with pytest.raises(ValueError, match="guard"):
        validate_fixed_allocation_policy(Path("bad.json"), missing_guard)

    one_space_standard = {
        "format": "dk4-ilnk-translation-batch-v1",
        "ascii_guard_policy": "two-byte-entry-and-line-v1",
        "records": [{
            "id": "ONE_SPACE",
            "replacement_hex": b" Text\n next".hex(),
            "entry_offsets": [0],
        }],
    }
    with pytest.raises(ValueError, match="two-byte"):
        validate_ascii_guard_policy(Path("bad.json"), one_space_standard)


def test_current_fixed_allocations_never_declare_a_one_byte_line_guard() -> None:
    for path in [*COMMON, RUNTIME, GLOBAL_LAYOUT]:
        batch = _load(path)
        validate_fixed_allocation_policy(path, batch)
        if "ascii_guard_policy" in batch:
            validate_ascii_guard_policy(path, batch)
        for record in batch["records"]:
            assert record["linebreak_guard_bytes"] in {0, 2}, record["id"]


def test_release_wide_text_layout_audit_passes_every_renderer_family() -> None:
    base = NdsImage.open(BASE)
    clean = NdsImage.open("work/clean.nds")
    source = base.read_file("/COMMON/MESFILE.DK4")
    rows: list[dict[str, object]] = []
    for path in [*COMMON, RUNTIME, GLOBAL_LAYOUT]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    assert not audit_ilnk(
        "/COMMON/MESFILE.DK4",
        rebuilt,
        clean.read_file("/COMMON/MESFILE.DK4"),
    )["issues"]
    for path in [
        "/COMMON/HELP.DK4",
        "/data/SC0.DK4",
        "/data/SC1.DK4",
        "/data/SC2.DK4",
        "/data/SC3.DK4",
    ]:
        assert not audit_ilnk(path, base.read_file(path), clean.read_file(path))["issues"]


def test_person_info_runtime_and_graphics_are_complete_and_source_locked() -> None:
    base = NdsImage.open(BASE)
    source_arm9 = base.read_file("/__arm9__.bin")
    rebuilt_arm9, ids = apply_arm9_fixed_batches([PERSON_ARM9], source_arm9)
    assert len(ids) == 18
    expected = {
        0x14827C: b"Healthy",
        0x14828C: b"Stamina",
        0x14829C: b"Agility",
        0x1482C4: b"Spirit",
        0x148368: b"Relaxed",
        0x148498: b"Admiral",
        0x14852C: b"Sailor Info",
        0x148CC8: b"Equipped Items",
        0x148CD8: b"Weapon",
        0x148CE4: b"Armor",
    }
    for offset, text in expected.items():
        assert _c_string(rebuilt_arm9, offset) == text

    source_pxl = base.read_file("/_pxl/personinfo.pxl")
    rebuilt_pxl, graphic_ids = apply_pxl_native_label_batch(
        PERSON_GRAPHICS, source_pxl, source_arm9
    )
    assert len(graphic_ids) == 4
    before = PxlImage.from_bytes(source_pxl)
    after = PxlImage.from_bytes(rebuilt_pxl)
    boxes = [tuple(record["box"]) for record in _load(PERSON_GRAPHICS)["records"]]
    for y in range(before.height):
        for x in range(before.width):
            if not any(l <= x < r and t <= y < b for l, t, r, b in boxes):
                pos = y * before.width + x
                assert after.indices[pos] == before.indices[pos]


def test_assign_sailors_v3_uses_compact_aligned_native_labels() -> None:
    base = NdsImage.open(BASE)
    source = base.read_file("/_pxl/dividecrewinfo.pxl")
    arm9 = base.read_file("/__arm9__.bin")
    rebuilt, ids = apply_pxl_native_label_batch(ASSIGN_GRAPHICS, source, arm9)
    assert len(ids) == 7
    assert rebuilt != source
    batch = _load(ASSIGN_GRAPHICS)
    assert [record["text"] for record in batch["records"]] == [
        "Assigned",
        "Reserve",
        "Range",
        "Marines",
        "Guns",
        "Lateen",
        "Square",
    ]


def test_polish_profile_contains_every_new_source_locked_layer() -> None:
    profile = _load(STACK)["profiles"]["lil-guild-shipyard-polish-v2"]
    assert profile["status"] == "experimental"
    assert profile["require_screen_entry_layout"] is True
    assert profile["batches"] == [
        ENTITY.as_posix(),
        UI.as_posix(),
        *(path.as_posix() for path in COMMON),
        RUNTIME.as_posix(),
        GLOBAL_LAYOUT.as_posix(),
        PERSON_ARM9.as_posix(),
        PERSON_GRAPHICS.as_posix(),
        ASSIGN_GRAPHICS.as_posix(),
    ]
