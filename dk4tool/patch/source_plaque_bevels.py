"""Use genuine clean native frame edges at the existing localized geometry."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL

ARM_SOURCE = "441e0e20c75f39261febac20078a319263fb76533229705cbb6f2c74a18ea960"


def source_point(x, y, width, height):
    def coordinate(i, length, original):
        if i < 2:
            return i
        if i >= length - 2:
            return original - (length - i)
        return 2 + (i - 2) % (original - 4)
    return 8 + coordinate(x, width, 40), 20 + coordinate(y, height, 16)


def transform_files(candidate, clean, groups):
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    replacements, reports = {}, []
    for group in groups:
        source = candidate.read_file(group["file_path"])
        if sha(source) != group["source_sha256"]:
            raise ValueError("Inherited localized plaque atlas differs")
        image = PxlImage.from_bytes(source)
        before = bytes(image.indices)
        mapping = {rgb: min(range(len(image.palette)), key=lambda n: sum(
            (image.palette[n][k] - rgb[k]) ** 2 for k in range(3))) for rgb in donor.palette}
        allowed, records = set(), []
        for row in group["records"]:
            l, t, r, b = row["plaque_box"]
            width, height = r - l, b - t
            if not (4 < width <= 84 and 4 < height <= 16):
                raise ValueError("Unreviewed localized bevel geometry")
            for y in range(height):
                for x in range(width):
                    if 2 <= x < width - 2 and 2 <= y < height - 2:
                        continue
                    at = (t + y) * image.width + l + x
                    if before[at] == row["ink_palette_index"]:
                        raise ValueError("A source bevel would overlap English lettering")
                    sx, sy = source_point(x, y, width, height)
                    image.indices[at] = mapping[donor.palette[donor.indices[sy * 256 + sx]]]
                    allowed.add(at)
            records.append(row["id"] + "_CLEAN_NATIVE_BEVEL")
        if any(a != b for i, (a, b) in enumerate(zip(before, image.indices)) if i not in allowed):
            raise ValueError("Bevel correction changed ink/interiors/unowned pixels")
        result = image.to_bytes()
        assert result[:image.pixels_offset] == source[:image.pixels_offset]
        replacements[group["file_path"]] = result
        reports.append({"file_path": group["file_path"], "source_sha256": sha(source),
                        "target_sha256": sha(result), "changed_records": records,
                        "changed_edge_pixels": sum(a != b for a, b in zip(before, image.indices)),
                        "English_interiors_dimensions_palette_and_layout_preserved": True})
    return replacements, reports


def transform_arm(source, clean):
    if sha(source) != ARM_SOURCE:
        raise ValueError("Clean bevel requires complete V545 ARM9")
    plan = json.loads(Path("work/analysis/direct_equipment_v270/runtime_plan.json").read_text(encoding="utf-8"))
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    at = plan["tile_pointer"] - POOL
    tile = bytearray(before[3][at:at + 1408])
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    for y in range(16):
        for x in range(44):
            if 2 <= x < 42 and 2 <= y < 14:
                continue
            sx, sy = source_point(x, y, 44, 16)
            r, g, b = [(v * 31 + 127) // 255 for v in donor.palette[donor.indices[sy * 256 + sx]][:3]]
            struct.pack_into("<H", tile, (y * 44 + x) * 2, 0x8000 | r | (g << 5) | (b << 10))
    code.sections[3].data[at:at + 1408] = tile
    result = bytes(code.save())
    saved = MainCodeFile(result, BASE)
    restored = bytearray(saved.sections[3].data)
    restored[at:at + 1408] = before[3][at:at + 1408]
    assert bytes(restored) == before[3]
    assert all(bytes(saved.sections[n].data) == before[n] for n in (0, 1, 2, 4))
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in saved.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    return result, {"source_arm9_sha256": ARM_SOURCE, "target_arm9_sha256": sha(result),
                    "tile_pointer": plan["tile_pointer"], "tile_bytes": 1408,
                    "source_frame_bounds": [8, 20, 48, 36],
                    "all_instructions_heap_startup_cache_and_section_geometry_unchanged": True,
                    "existing_fine_grain_interior_preserved": True}


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-source-plaque-bevel-release-v1":
        raise ValueError("Unknown native bevel release")
    if sha(clean.read_file("/_pxl/towninfo.pxl")) != config["donor_sha256"]:
        raise ValueError("Original frame source differs")
    replacements, reports = transform_files(candidate, clean, config["files"])
    for report, group in zip(reports, config["files"], strict=True):
        if report["target_sha256"] != group["target_sha256"]:
            raise ValueError("Reviewed localized bevel target differs")
    arm, plan = transform_arm(candidate.read_file("/__arm9__.bin"), clean)
    if sha(arm) != config["target_arm9_sha256"]:
        raise ValueError("Reviewed equipment bevel target differs")
    replacements["/__arm9__.bin"] = arm
    reports.append({"file_path": "/__arm9__.bin", **plan,
                    "changed_records": ["DK4_EQUIPMENT_ALL_WIDTHS_CLEAN_NATIVE_BEVEL"]})
    return replacements, reports
