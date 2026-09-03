from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_pxl_native_label_batch,
    resolve_release_batches,
)

BASE = Path("out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds")
ARM9_BATCH = Path("translations/common_submenus_arm9_v1.json")
CREW_BATCH = Path("translations/dividecrewinfo_native_labels_v1.json")
ITEMS_BATCH = Path("translations/common_items_runtime_v1.json")


def test_common_submenu_profile_is_complete() -> None:
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("common-submenus-v1", [])


def test_common_submenus_and_deck_help_are_source_locked() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/__arm9__.bin")
    batch = json.loads(ARM9_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 37
    assert len(rebuilt) == len(source)
    assert hashlib.sha256(rebuilt).hexdigest() == (
        "d800b54777686d77edbfb834c9b56b7198f8e5084c7e3156ccc82c1a42459685"
    )
    assert rebuilt[0x1385D4 : 0x1385DC] == b"Options\0"
    assert rebuilt[0x1385E4 : 0x1385EC] == b"Sailors\0"
    assert rebuilt[0x1385FC : 0x138608] == b"Ancient Map\0"
    assert rebuilt[0x138608 : 0x138614] == b"Fleet Info\0\0"
    assert rebuilt[0x138614 : 0x138620] == b"Reports".ljust(12, b"\0")
    assert rebuilt[0x138638 : 0x138644] == b"Save".ljust(12, b"\0")
    assert rebuilt[0x138644 : 0x138650] == b"Load".ljust(12, b"\0")
    assert rebuilt[0x13866C : 0x13867C] == b"Quit Game".ljust(16, b"\0")
    assert rebuilt[0x13865C : 0x13866C] == b"Sail Help".ljust(16, b"\0")
    assert rebuilt[0x16A0FC : 0x16A11C] == b"Select a save slot.".ljust(32, b"\0")
    assert rebuilt[0x16A11C : 0x16A13C] == b"Select data to load.".ljust(32, b"\0")
    assert rebuilt[0x16A14C : 0x16A154] == b" Docked\0"
    assert rebuilt[0x16A154 : 0x16A15C] == b"Unused\0\0"
    assert rebuilt[0x131F30 : 0x131F3C] == b"Deck".ljust(12, b"\0")
    assert b"Use Deck View to assign navigator duties." in rebuilt
    assert b"Higher ability makes the assignment more effective." in rebuilt


def test_empty_items_message_is_literal_and_source_locked() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/COMMON/MESFILE.DK4")
    batch = json.loads(ITEMS_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rows = materialize_translation_batch(batch, source)
    assert [row["id"] for row in rows] == ["DK4_MES_B04_R0051"]
    assert "%" not in rows[0]["english"]
    rebuilt = rebuild_mesfile(source, rows)
    assert len(rebuilt) == len(source)
    assert b"You have no items." in rebuilt
    assert rebuilt.count(b"see below") == source.count(b"see below") - 1


def test_assign_sailors_uses_native_font_and_preserves_unclaimed_pixels() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/_pxl/dividecrewinfo.pxl")
    arm9 = image.read_file("/__arm9__.bin")
    batch = json.loads(CREW_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_pxl_native_label_batch(CREW_BATCH, source, arm9)
    assert len(ids) == 7
    assert len(rebuilt) == len(source)
    assert hashlib.sha256(rebuilt).hexdigest() == (
        "a3441a625a853bf05f70d57599f8565535aba0f119147e40ed38fd55c2dc29ef"
    )

    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    boxes = [tuple(record["box"]) for record in batch["records"]]
    for y in range(before.height):
        for x in range(before.width):
            if not any(left <= x < right and top <= y < bottom for left, top, right, bottom in boxes):
                position = y * before.width + x
                assert after.indices[position] == before.indices[position]
