"""Restore the original Save/Load plaque rims with contiguous source wood."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha

FILE = "/_pxl/saveloadinfo.pxl"
DONOR = "/_pxl/towninfo.pxl"
ROWS = (("LEVEL", "レベル", "Level", (96, 39, 137, 57), (96, 40, 136, 56)),
        ("POWER", "勢力値", "Power", (96, 63, 137, 81), (96, 64, 136, 80)))


def transform(inherited, japanese, donor_data, arm):
    old, original, donor = [PxlImage.from_bytes(d) for d in (inherited, japanese, donor_data)]
    assert old.width == original.width == 256 and old.height == original.height == 192
    assert old.source[:old.pixels_offset] == original.source[:original.pixels_offset]
    result = PxlImage.from_bytes(inherited)
    font = GameAsciiFont.from_arm9(arm)
    mapping = {rgb: min((i for i in range(256) if i != 1),
                       key=lambda i: sum((result.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
               for rgb in donor.palette}
    owned, records = set(), []
    for key, japanese_text, text, restore, face in ROWS:
        l, t, r, b = restore
        fl, ft, fr, fb = face
        assert fr - fl == 40 and fb - ft == 16
        for y in range(t, b):
            for x in range(l, r):
                result.indices[y * 256 + x] = original.indices[y * 256 + x]
                owned.add(y * 256 + x)
        for y in range(ft + 2, fb - 2):
            for x in range(fl + 2, fr - 2):
                sx, sy = 3 + x - fl - 2, 62 + y - ft - 2
                result.indices[y * 256 + x] = mapping[donor.palette[donor.indices[sy * 256 + sx]]]
        x0, y0 = fl + (40 - len(text) * 5) // 2, ft + 2
        ink = {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(text)
               for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        assert all(fl + 2 <= x < fr - 2 and ft + 2 <= y < fb - 2 for x, y in ink)
        for x, y in ink:
            result.indices[y * 256 + x] = 1
        assert {(x, y) for y in range(ft + 2, fb - 2) for x in range(fl + 2, fr - 2)
                if result.indices[y * 256 + x] == 1} == ink
        rim = {(x, y) for y in range(ft, fb) for x in range(fl, fr)
               if not (fl + 2 <= x < fr - 2 and ft + 2 <= y < fb - 2)}
        assert all(result.indices[y * 256 + x] == original.indices[y * 256 + x] for x, y in rim)
        records.append({"id": "DK4_SAVE_LOAD_" + key + "_SOURCE_PLAQUE", "Japanese": japanese_text, "English": text,
                        "restore_box": list(restore), "original_and_final_plaque_box": list(face), "font_origin": [x0, y0],
                        "complete_native_font_ink": len(ink), "original_rim_pixels_exact_at_original_coordinates": len(rim),
                        "reconstructed_interior_pixels": 432, "fully_completed": False})
    assert all(a == b for i, (a, b) in enumerate(zip(old.indices, result.indices, strict=True)) if i not in owned)
    output = result.to_bytes()
    assert output[:old.pixels_offset] == inherited[:old.pixels_offset]
    report = {"file_path": FILE, "source_sha256": sha(inherited), "clean_sha256": sha(japanese), "donor_sha256": sha(donor_data),
              "target_sha256": sha(output), "records": records,
              "source_grain_contiguous_half_open_bounds": [3, 62, 39, 74], "no_repeat_join_or_stretch": True,
              "concealed_interior_material_is_inferred": True,
              "changed_pixels": sum(a != b for a, b in zip(old.indices, result.indices, strict=True)),
              "source_frames_geometry_palettes_headers_and_unowned_pixels_preserved": True}
    return output, report


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-save-load-plaques-v1":
        raise ValueError("Unknown Save/Load plaque repair")
    old, source, donor = candidate.read_file(FILE), clean.read_file(FILE), clean.read_file(DONOR)
    if any(sha(data) != config[key] for data, key in ((old, "source_sha256"), (source, "clean_sha256"), (donor, "donor_sha256"))):
        raise ValueError("Original or inherited Save/Load plaque source differs")
    output, report = transform(old, source, donor, candidate.read_file("/__arm9__.bin"))
    if sha(output) != config["target_sha256"] or report["records"] != config["records"]:
        raise ValueError("Save/Load reviewed target or ownership differs")
    return {FILE: output}, report
