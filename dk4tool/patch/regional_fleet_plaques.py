"""Source-framed regional-fleet plaques; no runtime or memory-layout changes."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha

FILE = "/_pxl/chihofleetinfo.pxl"
DONOR = "/_pxl/towninfo.pxl"
RECORDS = (
    ("LEVEL", "Level", "レベル", (83, 72, 125, 92), (83, 76, 125, 92), (84, 76, 124, 92)),
    ("INCOME", "Income", "収入額", (3, 100, 49, 118), (3, 100, 49, 116), (8, 100, 48, 116)),
    ("EXPENSES", "Expenses", "支出額", (3, 120, 49, 138), (3, 120, 49, 136), (8, 120, 48, 136)),
    ("INVESTED", "Invested", "投資額", (3, 140, 49, 158), (3, 140, 49, 156), (8, 140, 48, 156)),
    ("MISSION", "Mission", "任務", (3, 160, 49, 178), (3, 160, 49, 176), (8, 160, 48, 176)),
)


def full_ink(font, text, face):
    left, top, right, bottom = face
    x0 = left + (right - left - len(text) * 5) // 2
    y0 = top + (bottom - top - 11) // 2
    return {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(text)
            for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}


def render(inherited, japanese, donor_data, arm):
    old, original, donor = [PxlImage.from_bytes(d) for d in (inherited, japanese, donor_data)]
    if old.source[:old.pixels_offset] != original.source[:original.pixels_offset]:
        raise ValueError("Regional-fleet source header/palette/geometry differs")
    result = PxlImage.from_bytes(inherited)
    font = GameAsciiFont.from_arm9(arm)
    # Same reviewed 40-column source sample as the V581 repeat-join correction.
    # Hidden text pixels are reconstructed, not claimed recovered.
    mapping = {rgb: min((i for i in range(len(old.palette)) if i != 1),
                       key=lambda i: sum((old.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
               for rgb in donor.palette}
    owned, reports = set(), []
    for key, text, source_text, erase, face, source_face in RECORDS:
        left, top, right, bottom = erase
        fl, ft, fr, fb = face
        sl, st, sr, sb = source_face
        assert fb - ft == sb - st == 16 and sr - sl == 40
        for y in range(top, bottom):
            for x in range(left, right):
                at = y * old.width + x
                result.indices[at] = original.indices[at]
                owned.add(at)
        ink = full_ink(font, text, face)
        assert all(fl + 2 <= x < fr - 2 and ft + 2 <= y < fb - 2 for x, y in ink)
        frame_points, reconstructed = 0, 0
        for y in range(ft, fb):
            for x in range(fl, fr):
                dx, dy = x - fl, y - ft
                if 2 <= dx < fr - fl - 2 and 2 <= dy < 14:
                    sx, sy = 3 + (dx - 2) % 40, 62 + dy - 2
                    value = mapping[donor.palette[donor.indices[sy * donor.width + sx]]]
                    assert sum(result.palette[value][:3]) > 260
                    reconstructed += 1
                else:
                    # Original plaque's own two-pixel rim, not a generic frame.
                    sx = sl + (dx if dx < 2 else 40 - (fr - x) if x >= fr - 2 else 2 + (dx - 2) % 36)
                    value = original.indices[(st + dy) * original.width + sx]
                    frame_points += 1
                result.indices[y * result.width + x] = value
        for x, y in ink:
            result.indices[y * result.width + x] = 1
        actual = {(x, y) for y in range(ft + 2, fb - 2) for x in range(fl + 2, fr - 2)
                  if result.indices[y * result.width + x] == 1}
        assert actual == ink, text
        wallpaper = {(x, y) for y in range(top, bottom) for x in range(left, right)
                     if not (fl <= x < fr and ft <= y < fb)}
        assert all(result.indices[y * result.width + x] == original.indices[y * result.width + x]
                   for x, y in wallpaper)
        reports.append({"id": "DK4_REGIONAL_" + key + "_SOURCE_MATERIAL", "English": text,
                        "Japanese": source_text, "restore_box": list(erase), "plaque_box": list(face),
                        "original_plaque_box": list(source_face), "full_native_font_ink": len(ink),
                        "own_source_frame_pixels": frame_points, "reconstructed_interior_pixels": reconstructed,
                        "original_wallpaper_pixels_restored": sum(old.indices[y * old.width + x] != original.indices[y * old.width + x]
                                                                   for x, y in wallpaper),
                        "fully_completed": False})
    assert all(a == b for i, (a, b) in enumerate(zip(old.indices, result.indices, strict=True)) if i not in owned)
    output = result.to_bytes()
    assert output[:old.pixels_offset] == inherited[:old.pixels_offset]
    return output, {"file_path": FILE, "source_sha256": sha(inherited), "clean_sha256": sha(japanese),
                    "target_sha256": sha(output), "donor_sha256": sha(donor_data), "records": reports,
                    "changed_pixels": sum(a != b for a, b in zip(old.indices, result.indices, strict=True)),
                    "grain_source_half_open_bounds": [3, 62, 43, 74], "grain_horizontal_period": 40,
                    "concealed_texture_is_inferred": True, "all_unowned_pixels_header_palettes_and_dimensions_exact": True}


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-regional-fleet-plaques-v1":
        raise ValueError("Unknown regional-fleet plaque repair")
    inherited, original, donor = candidate.read_file(FILE), clean.read_file(FILE), clean.read_file(DONOR)
    if (sha(inherited) != config["source_sha256"] or sha(original) != config["clean_sha256"]
            or sha(donor) != config["donor_sha256"]):
        raise ValueError("Original or inherited regional-fleet texture source differs")
    result, report = render(inherited, original, donor, candidate.read_file("/__arm9__.bin"))
    if sha(result) != config["target_sha256"] or report["records"] != config["records"]:
        raise ValueError("Regional-fleet plaque reviewed target or ownership differs")
    return {FILE: result}, report
