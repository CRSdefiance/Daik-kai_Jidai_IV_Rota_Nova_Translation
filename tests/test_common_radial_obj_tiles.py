from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_obj_tile_pxl_sync_batch

BASE = Path("out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds")
BATCH = Path("translations/common_radial_obj_tiles_v2.json")


def _packed_tile(marker: PxlImage, tile_x: int, tile_y: int) -> bytes:
    packed = bytearray()
    for y in range(8):
        row = (tile_y * 8 + y) * marker.width + tile_x * 8
        for x in range(0, 8, 2):
            packed.append(marker.indices[row + x] | marker.indices[row + x + 1] << 4)
    return bytes(packed)


def test_common_radial_obj_tiles_are_source_locked_and_surgical() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/GRP/DSOBJ.DK4")
    marker_bytes = image.read_file("/_pxl/__marker.pxl")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]
    assert hashlib.sha256(marker_bytes).hexdigest() == batch["source_image_sha256"]

    rebuilt, ids = apply_obj_tile_pxl_sync_batch(BATCH, source, marker_bytes)
    assert len(rebuilt) == len(source)
    assert len(ids) == 6
    assert hashlib.sha256(rebuilt).hexdigest() == (
        "93b08c821ec2a356a970e23da4dbe074421ad1ec8dd0a12fe05e32bbaf9fdd6d"
    )

    marker = PxlImage.from_bytes(marker_bytes)
    claimed: set[int] = set()
    for bank in range(6):
        for tile_y in range(3):
            for tile_x in range(8):
                tile_index = bank * 32 + tile_y * 8 + tile_x
                claimed.add(tile_index)
                start = tile_index * 32
                assert rebuilt[start : start + 32] == _packed_tile(
                    marker, tile_x, bank * 3 + tile_y
                )

    for tile_index in range(len(source) // 32):
        if tile_index not in claimed:
            start = tile_index * 32
            assert rebuilt[start : start + 32] == source[start : start + 32]
