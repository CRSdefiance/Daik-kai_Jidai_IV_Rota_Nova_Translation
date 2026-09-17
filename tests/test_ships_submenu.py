from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_pxl_native_label_batch,
    resolve_release_batches,
)

BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
GRAPHICS_BATCH = Path("translations/ships_submenu_graphics_v2.json")
ARM9_BATCH = Path("translations/ships_submenu_arm9_v1.json")


def test_ships_submenu_profile_is_complete() -> None:
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("ships-submenu-v2", [])


def test_ships_graphics_use_native_font_and_preserve_unclaimed_pixels() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/_pxl/shipinfo.pxl")
    arm9 = image.read_file("/__arm9__.bin")
    batch = json.loads(GRAPHICS_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_pxl_native_label_batch(GRAPHICS_BATCH, source, arm9)
    assert len(ids) == 11
    assert len(rebuilt) == len(source)
    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    boxes = [tuple(record["box"]) for record in batch["records"]]
    for y in range(before.height):
        for x in range(before.width):
            if not any(
                left <= x < right and top <= y < bottom
                for left, top, right, bottom in boxes
            ):
                position = y * before.width + x
                assert after.indices[position] == before.indices[position]

    # The first Cargo sprite begins at x=166 and the cannon sprite at x=43.
    # Neither native-font caption may leak into those runtime-owned fields.
    assert all(
        after.indices[y * after.width + x] != 1
        for y in range(57, 81)
        for x in range(166, 182)
    )
    assert all(
        after.indices[y * after.width + x] != 1
        for y in range(117, 141)
        for x in range(43, 68)
    )


def test_ships_runtime_text_is_source_locked_and_terminated() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    batch = json.loads(ARM9_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 4
    assert rebuilt[0x13C1A7 : 0x13C1B8] == b"Culverin ".ljust(17, b"\0")
    for offset in (0x1484AC, 0x1514FC, 0x152BE4):
        assert rebuilt[offset : offset + 8] == b"%s Cpt.\0"
