"""Preserve original treasure-header grain around the retained English mask."""

import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha

PATH = "/_pxl/mysterymap/mys_hunt_d.pxl"
BOX = (84, 0, 174, 15)
STROKES = ((86, 1, 99, 13), (122, 1, 135, 13), (158, 1, 171, 13))


def transform(source, japanese):
    old, original = PxlImage.from_bytes(source), PxlImage.from_bytes(japanese)
    if old.palette != original.palette or (old.width, old.height) != (256, 192):
        raise ValueError("Original treasure header geometry or palette differs")
    result = PxlImage.from_bytes(source)
    preserved, reconstructed, ink = 0, 0, 0
    for y in range(BOX[1], BOX[3]):
        for x in range(BOX[0], BOX[2]):
            at = y * old.width + x
            if old.indices[at] == 7:
                ink += 1
                continue
            cell = next((b for b in STROKES if b[0] <= x < b[2] and b[1] <= y < b[3]), None)
            if cell and original.palette[original.indices[at]][0] < 140:
                # Same asset, same row, original blank wood: no palette remap,
                # no nearest-row stretching, no translated donor.
                result.indices[at] = original.indices[y * old.width + 24 + x - cell[0]]
                reconstructed += 1
            else:
                result.indices[at] = original.indices[at]
                preserved += 1
    data = result.to_bytes()
    if data[:old.pixels_offset] != source[:old.pixels_offset]:
        raise ValueError("Treasure grain changed header/palette")
    return data, {"source_sha256": sha(source), "japanese_source_sha256": sha(japanese),
                  "target_sha256": sha(data), "restore_box": list(BOX),
                  "stroke_boxes": [list(b) for b in STROKES],
                  "local_source_donor_bounds": [24, 1, 37, 13],
                  "same_row_source_pixels_no_palette_remap": True,
                  "visible_source_pixels_preserved": preserved,
                  "concealed_dark_pixels_reconstructed": reconstructed,
                  "complete_current_English_ink_pixels_retained": ink}


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-treasure-source-grain-release-v1":
        raise ValueError("Unknown treasure source grain release")
    source, japanese = candidate.read_file(PATH), clean.read_file(PATH)
    if sha(source) != config["source_sha256"] or sha(japanese) != config["japanese_source_sha256"]:
        raise ValueError("Original/inherited treasure header source differs")
    result, plan = transform(source, japanese)
    if sha(result) != config["target_sha256"]:
        raise ValueError("Reviewed treasure grain target differs")
    plan["changed_records"] = ["DK4_TREASURE_NAME_HEADER_ORIGINAL_SOURCE_GRAIN"]
    return result, plan
