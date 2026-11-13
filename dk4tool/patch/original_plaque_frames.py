"""Restore clean source frames and visible grain around retained English ink."""

import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-original-plaque-frames-release-v1":
        raise ValueError("Unknown original plaque frame release")
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    if sha(donor.source) != config["donor_file_sha256"]:
        raise ValueError("Original blank wood donor differs")
    replacements, reports = {}, []
    for group in config["files"]:
        source = candidate.read_file(group["file_path"])
        original_data = clean.read_file(group["file_path"])
        if sha(source) != group["source_sha256"] or sha(original_data) != group["japanese_source_sha256"]:
            raise ValueError("Original or inherited plaque source differs")
        original, old = PxlImage.from_bytes(original_data), PxlImage.from_bytes(source)
        result = PxlImage.from_bytes(source)
        if original.palette != old.palette:
            raise ValueError("Original plaque palette differs")
        mapping = {rgb: min(range(len(result.palette)), key=lambda i: sum(
            (result.palette[i][k] - rgb[k]) ** 2 for k in range(3))) for rgb in donor.palette}
        owned, records = set(), []
        for row in group["records"]:
            l, t, r, b = row["restore_box"]
            el, et, er, eb = row["japanese_stroke_box"]
            if not (0 <= l <= el < er <= r <= old.width and
                    0 <= t <= et < eb <= b <= old.height):
                raise ValueError("Plaque frame or stroke mask escapes its atlas")
            ink = row["ink_palette_index"]
            for y in range(t, b):
                for x in range(l, r):
                    at = y * old.width + x
                    index = original.indices[at]
                    if old.indices[at] == ink:
                        result.indices[at] = ink
                    elif el <= x < er and et <= y < eb and original.palette[index][0] < 140:
                        dx, dy = 2 + (x - el) % 40, 62 + (y - et) % 12
                        result.indices[at] = mapping[donor.palette[donor.indices[dy * donor.width + dx]]]
                    else:
                        result.indices[at] = index
                    owned.add(at)
            records.append(row["id"] + "_ORIGINAL_FRAME_TEXTURE")
        if any(a != b for i, (a, b) in enumerate(zip(old.indices, result.indices, strict=True))
               if i not in owned):
            raise ValueError("Original plaque frames changed unowned pixels")
        data = result.to_bytes()
        if data[:old.pixels_offset] != source[:old.pixels_offset] or sha(data) != group["target_sha256"]:
            raise ValueError("Original frame palette/header or reviewed target differs")
        replacements[group["file_path"]] = data
        reports.append({"file_path": group["file_path"], "changed_records": records,
                        "source_sha256": sha(source), "target_sha256": sha(data),
                        "original_visible_source_pixels_retained": sum(
                            row["visible_source_pixels_preserved"] for row in group["records"]),
                        "source_frames_restored_current_letters_preserved": True,
                        "unowned_pixels_palette_dimensions_preserved": True})
    return replacements, reports
