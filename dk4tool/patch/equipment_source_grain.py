"""Correct every equipment hint width inside the existing tile/helper slots."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import paint
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL

SOURCE_ARM = "72b3f84ab3ffc5db8da4d420a343941749baeed44d044bdfb79690339500c36c"
PLAN = Path("work/analysis/direct_equipment_v270/runtime_plan.json")
OLD_TILE = Path("work/analysis/direct_equipment_v270/paper_tile.bin")


def transform(source, clean):
    if sha(source) != SOURCE_ARM:
        raise ValueError("Equipment grain requires the complete V542 ARM9")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    original_tile = OLD_TILE.read_bytes()
    if plan["period"] != 40 or len(original_tile) != 1408:
        raise ValueError("Existing equipment tile geometry differs")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    tile_offset = plan["tile_pointer"] - POOL
    helper_offset = plan["entry"] - POOL
    expected_helper = paint(plan["entry"], plan["state_pointer"],
                            plan["old_dispatcher"], plan["tile_pointer"], 40)
    if before[3][tile_offset:tile_offset + 1408] != original_tile:
        raise ValueError("Original equipment tile slot differs")
    if before[3][helper_offset:helper_offset + len(expected_helper)] != expected_helper:
        raise ValueError("Original bounded equipment painter differs")
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    tile = bytearray(original_tile)
    for y in range(2, 14):
        for x in range(2, 42):
            rgb = donor.palette[donor.indices[(60 + y) * donor.width + x]][:3]
            if sum(rgb) < 300:
                raise ValueError("Original blank wood strip contains a dark stroke")
            r, g, b = [(v * 31 + 127) // 255 for v in rgb]
            struct.pack_into("<H", tile, (y * 44 + x) * 2,
                             0x8000 | r | (g << 5) | (b << 10))
    code.sections[3].data[tile_offset:tile_offset + 1408] = tile
    branches = []
    # These three BEQs delegated heading/short hints to the old coarse painter.
    # The existing direct painter can handle them without new code or storage.
    for offset, width in ((32, 34), (40, 40), (48, 88)):
        at = helper_offset + offset
        old = struct.unpack_from("<I", before[3], at)[0]
        if old >> 24 != 0x0A:
            raise ValueError("Expected original width-specific BEQ")
        struct.pack_into("<I", code.sections[3].data, at, 0xE1A00000)
        branches.append({"resident_address": plan["entry"] + offset,
                         "width": width, "before": old, "after": 0xE1A00000})
    result = bytes(code.save())
    saved = MainCodeFile(result, BASE)
    restored = bytearray(saved.sections[3].data)
    restored[tile_offset:tile_offset + 1408] = original_tile
    for row in branches:
        struct.pack_into("<I", restored, row["resident_address"] - POOL, row["before"])
    if bytes(restored) != before[3] or any(bytes(saved.sections[n].data) != before[n]
                                          for n in (0, 1, 2, 4)):
        raise ValueError("Equipment grain changed unowned code/data")
    geometry = [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    if geometry != [(s.ramAddress, len(s.data), s.bssSize) for s in saved.sections]:
        raise ValueError("Equipment grain changed section geometry")
    return result, {"source_arm9_sha256": SOURCE_ARM, "target_arm9_sha256": sha(result),
                    "tile_pointer": plan["tile_pointer"], "entry": plan["entry"],
                    "old_dispatcher": plan["old_dispatcher"], "state_pointer": plan["state_pointer"],
                    "tile_bytes": 1408, "tile_sha256": sha(tile), "period": 40,
                    "source_blank_bounds": [2, 62, 42, 74], "dispatch_changes": branches,
                    "all_tile_bevel_pixels_preserved": True,
                    "all_other_code_data_heap_startup_cache_and_section_extents_preserved": True,
                    "section_geometry": geometry}


def apply_release(source, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-equipment-source-grain-release-v1":
        raise ValueError("Unknown equipment source grain release")
    for path, digest in config["dependencies"].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError("Equipment grain dependency differs: " + path)
    if sha(clean.read_file("/_pxl/towninfo.pxl")) != config["donor_file_sha256"]:
        raise ValueError("Original grain donor differs")
    result, plan = transform(source, clean)
    if sha(result) != config["target_arm9_sha256"]:
        raise ValueError("Equipment source grain target differs")
    plan["changed_records"] = ["DK4_EQUIPMENT_HEADING_AND_ALL_HINT_WIDTHS_ORIGINAL_GRAIN"]
    return result, plan
