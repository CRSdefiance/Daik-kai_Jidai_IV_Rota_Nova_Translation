"""Exclude a source bevel-adjacent column from repeating equipment wood."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL

SOURCE_ARM = "1f94c9c084552fa93cefd80ad195dda054cf9fdaa06a488d2a3943b37822aa5f"
DONOR_SHA = "7d69036562e1589fe70f044fa2b268e564bc5fe2aec6486f42341712219b3431"


def transform(source, clean):
    if sha(source) != SOURCE_ARM:
        raise ValueError("Equipment join repair requires the complete V573 ARM9")
    raw = clean.read_file("/_pxl/towninfo.pxl")
    if sha(raw) != DONOR_SHA:
        raise ValueError("Original equipment wood donor differs")
    donor = PxlImage.from_bytes(raw)
    plan = json.loads(Path("work/analysis/direct_equipment_v270/runtime_plan.json").read_text(encoding="utf-8"))
    if plan["period"] != 40:
        raise ValueError("Existing equipment repeat period differs")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    offset = plan["tile_pointer"] - POOL
    tile = bytearray(before[3][offset:offset + 1408])

    def color(x, y):
        rgb = donor.palette[donor.indices[y * donor.width + x]][:3]
        r, g, b = [(v * 31 + 127) // 255 for v in rgb]
        return 0x8000 | r | (g << 5) | (b << 10)

    for y in range(2, 14):
        for x in range(2, 42):
            at = (y * 44 + x) * 2
            if struct.unpack_from("<H", tile, at)[0] != color(x, y + 60):
                raise ValueError("Inherited source wood interior differs")
            struct.pack_into("<H", tile, at, color(x + 1, y + 60))
    code.sections[3].data[offset:offset + 1408] = tile
    result = bytes(code.save())
    saved = MainCodeFile(result, BASE)
    restored = bytearray(saved.sections[3].data)
    restored[offset:offset + 1408] = before[3][offset:offset + 1408]
    assert bytes(restored) == before[3]
    assert all(bytes(saved.sections[n].data) == before[n] for n in (0, 1, 2, 4))
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in saved.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    assert all(tile[(y * 44 + x) * 2:(y * 44 + x + 1) * 2] ==
               before[3][offset + (y * 44 + x) * 2:offset + (y * 44 + x + 1) * 2]
               for y in range(16) for x in range(44)
               if not (2 <= x < 42 and 2 <= y < 14))
    return result, {"source_arm9_sha256": SOURCE_ARM, "target_arm9_sha256": sha(result),
                    "source_blank_bounds": [3, 62, 43, 74], "previous_blank_bounds": [2, 62, 42, 74],
                    "period": 40, "tile_pointer": plan["tile_pointer"], "tile_bytes": 1408,
                    "changed_interior_words": sum(tile[i:i + 2] != before[3][offset + i:offset + i + 2]
                                                  for i in range(0, 1408, 2)),
                    "all_code_frames_heap_cache_and_section_extents_preserved": True,
                    "changed_records": ["DK4_EQUIPMENT_ALL_WIDTHS_SOURCE_WOOD_JOIN"]}


def apply_release(source, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-equipment-grain-join-v1":
        raise ValueError("Unknown equipment join release")
    result, proof = transform(source, clean)
    if sha(result) != config["target_arm9_sha256"]:
        raise ValueError("Reviewed equipment join target differs")
    return result, proof
