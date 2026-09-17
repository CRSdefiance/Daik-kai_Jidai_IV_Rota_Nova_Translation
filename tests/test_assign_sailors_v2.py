from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_pxl_native_label_batch,
)


BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
GRAPHICS_BATCH = Path("translations/assign_sailors_graphics_v2.json")
ARM9_BATCH = Path("translations/assign_sailors_arm9_v2.json")


def test_assign_sailors_v2_restores_full_plaques_and_preserves_everything_else() -> None:
    base = NdsImage.open(BASE)
    source = base.read_file("/_pxl/dividecrewinfo.pxl")
    arm9 = base.read_file("/__arm9__.bin")
    batch = json.loads(GRAPHICS_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_pxl_native_label_batch(GRAPHICS_BATCH, source, arm9)
    assert len(ids) == 7
    assert len(rebuilt) == len(source)
    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    boxes = [tuple(record["box"]) for record in batch["records"]]
    draw_boxes = [tuple(record["draw_box"]) for record in batch["records"]]

    for y in range(before.height):
        for x in range(before.width):
            in_box = any(
                left <= x < right and top <= y < bottom
                for left, top, right, bottom in boxes
            )
            if not in_box:
                position = y * before.width + x
                assert after.indices[position] == before.indices[position]

    # Every complete plaque frame comes from the accepted artwork. Only the
    # inner draw bands may differ because they contain the new native glyphs.
    for box, draw_box in zip(boxes, draw_boxes, strict=True):
        for y in range(box[1], box[3]):
            for x in range(box[0], box[2]):
                if not (
                    draw_box[0] <= x < draw_box[2]
                    and draw_box[1] <= y < draw_box[3]
                ):
                    position = y * before.width + x
                    assert after.indices[position] == before.indices[position]


def test_assign_sailors_range_formatter_is_clear_and_exact_width() -> None:
    arm9 = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, arm9)
    assert ids == ["DK4_ASSIGN_RANGE_FORMAT_V2"]
    assert rebuilt[0x133FF4 : 0x133FFC] == b"%d days\0"
    assert rebuilt[:0x133FF4] == arm9[:0x133FF4]
    assert rebuilt[0x133FFC:] == arm9[0x133FFC:]


def test_assign_sailors_v2_is_part_of_the_current_review_profile() -> None:
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    batches = stack["profiles"]["raphael-story-push-v1"]["batches"]
    assert GRAPHICS_BATCH.as_posix() in batches
    assert ARM9_BATCH.as_posix() in batches
