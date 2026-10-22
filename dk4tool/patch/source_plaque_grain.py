"""Replace only plaque interior background pixels with clean-ROM grain."""

import hashlib
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage


def sha(data):
    return hashlib.sha256(data).hexdigest()


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-source-plaque-grain-release-v1":
        raise ValueError("Unknown original plaque grain release")
    for path, digest in config["dependencies"].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError("Plaque grain dependency differs: " + path)
    donor_data = clean.read_file(config["donor_file"])
    if sha(donor_data) != config["donor_file_sha256"]:
        raise ValueError("Original Japanese grain donor differs")
    donor = PxlImage.from_bytes(donor_data)
    columns = list(range(2, 43)) + list(range(85, 124))
    colors = [[donor.palette[donor.indices[y * donor.width + x]][:3]
               for x in columns] for y in range(62, 74)]
    if any(sum(c) < 300 for row in colors for c in row):
        raise ValueError("Blank donor strips contain unexpected dark pixels")
    replacements, reports = {}, []
    for group in config["files"]:
        path = group["file_path"]
        source = candidate.read_file(path)
        if sha(source) != group["source_sha256"]:
            raise ValueError("Complete inherited plaque atlas differs: " + path)
        image = PxlImage.from_bytes(source)
        before = bytes(image.indices)
        mapping = {rgb: min(range(len(image.palette)), key=lambda i: sum(
            (image.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
            for row in colors for rgb in row}
        allowed, records = set(), []
        for row in group["records"]:
            left, top, right, bottom = row["plaque_box"]
            if not (0 <= left < right <= image.width and
                    0 <= top < bottom <= image.height and
                    4 < right - left <= 84 and 4 < bottom - top <= 16):
                raise ValueError("Plaque grain interior exceeds verified donor")
            ink = int(row["ink_palette_index"])
            for y in range(top + 2, bottom - 2):
                for x in range(left + 2, right - 2):
                    position = y * image.width + x
                    if before[position] != ink:
                        image.indices[position] = mapping[colors[y - top - 2][x - left - 2]]
                        allowed.add(position)
            records.append(row["id"] + "_ORIGINAL_GRAIN")
        if any(a != b and i not in allowed for i, (a, b) in enumerate(
                zip(before, image.indices, strict=True))):
            raise ValueError("Plaque grain changed letters, bevels or unowned pixels")
        result = image.to_bytes()
        if result[:image.pixels_offset] != source[:image.pixels_offset]:
            raise ValueError("Plaque grain changed header or palette")
        if sha(result) != group["target_sha256"]:
            raise ValueError("Plaque grain target differs from reviewed prototype")
        replacements[path] = result
        reports.append({"file_path": path, "source_sha256": sha(source),
                        "target_sha256": sha(result), "changed_records": records,
                        "changed_pixels": sum(a != b for a, b in zip(before, image.indices)),
                        "letters_bevels_palette_dimensions_and_unowned_pixels_preserved": True})
    return replacements, {"files": reports, "donor_file": config["donor_file"],
                          "source_blank_bounds": [[2, 62, 43, 74], [85, 62, 124, 74]],
                          "source_strips_joined_at_column": 41,
                          "all18_entries_remain_incomplete": True}
