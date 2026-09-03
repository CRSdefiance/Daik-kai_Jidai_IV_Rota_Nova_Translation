from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_ilnk_pxl_sync_batch

BASE = Path("out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds")
BATCH = Path("translations/common_radial_runtime_graphics_v1.json")


def test_runtime_common_atlas_sync_is_source_locked_and_surgical() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/GRP/CMMNIMG.DK4")
    marker_bytes = image.read_file("/_pxl/__marker.pxl")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]
    assert hashlib.sha256(marker_bytes).hexdigest() == batch["source_image_sha256"]

    rebuilt, ids = apply_ilnk_pxl_sync_batch(BATCH, source, marker_bytes)
    assert ids == ["DK4_COMMON_RUNTIME_MARKER_ATLAS"]
    assert len(rebuilt) == len(source)

    before = IlnkContainer.parse(source)
    after = IlnkContainer.parse(rebuilt)
    assert len(before.blocks) == len(after.blocks)
    assert before.blocks[:5] == after.blocks[:5]
    assert before.blocks[6:] == after.blocks[6:]
    assert before.blocks[5][:20] == after.blocks[5][:20]

    marker = PxlImage.from_bytes(marker_bytes)
    payload = after.blocks[5][20:]
    for y in range(256):
        for x in range(256):
            packed = payload[y * 256 + x // 2]
            actual = packed & 0x0F if x % 2 == 0 else packed >> 4
            assert actual == marker.indices[y * 256 + x]

    for y in range(256):
        row = 20 + y * 256
        assert before.blocks[5][row + 128 : row + 256] == after.blocks[5][
            row + 128 : row + 256
        ]
