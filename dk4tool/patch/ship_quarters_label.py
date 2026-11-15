"""Use the established Quarters term for the same marine-room statistic."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.source_plaque_bevels import source_point

FILE = "/_pxl/shipinfo.pxl"
FACE = (5, 104, 68, 120)


def render_label(candidate, clean, face, previous, replacement, japanese, record_id):
    data = candidate.read_file(FILE)
    image = PxlImage.from_bytes(data)
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    font = GameAsciiFont.from_arm9(candidate.read_file("/__arm9__.bin"))
    mapping = {rgb: min((n for n in range(len(image.palette)) if n != 1),
                       key=lambda n: sum((image.palette[n][k] - rgb[k]) ** 2 for k in range(3)))
               for rgb in donor.palette}
    columns = list(range(2, 43)) + list(range(85, 124))
    left, top, right, bottom = face

    def grain(x, y):
        xx, yy = x - left, y - top
        if 2 <= xx < right - left - 2 and 2 <= yy < bottom - top - 2:
            sx, sy = columns[xx - 2], 62 + yy - 2
        else:
            sx, sy = source_point(xx, yy, right - left, bottom - top)
        return mapping[donor.palette[donor.indices[sy * donor.width + sx]]]

    def ink(text):
        x0 = left + (right - left - len(text) * 5) // 2
        points = {(x0 + n * 5 + x, top - 1 + y) for n, ch in enumerate(text)
                  for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        if not points or not all(left < x < right - 1 and top < y < bottom - 1 for x, y in points):
            raise ValueError("Ship lettering crosses the original outer frame")
        return points

    old, new = ink(previous), ink(replacement)
    # Reconstruct the existing reviewed face, rather than filling old letters
    # from unrelated pixels or flattening the wood. Every visible point must fit.
    for y in range(top, bottom):
        for x in range(left, right):
            expected = 1 if (x, y) in old else grain(x, y)
            if image.indices[y * image.width + x] != expected:
                raise ValueError("Inherited ship plaque differs from the reviewed source grain")
    before = bytes(image.indices)
    for x, y in old:
        image.indices[y * image.width + x] = grain(x, y)
    for x, y in new:
        image.indices[y * image.width + x] = 1
    if {(x, y) for y in range(top, bottom) for x in range(left, right)
            if image.indices[y * image.width + x] == 1} != new:
        raise ValueError("Ship complete glyph mask differs")
    owned = {y * image.width + x for x, y in old | new}
    if any(a != b for n, (a, b) in enumerate(zip(before, image.indices, strict=True)) if n not in owned):
        raise ValueError("Unowned ship plaque pixel changed")
    output = image.to_bytes()
    if output[:image.pixels_offset] != data[:image.pixels_offset]:
        raise ValueError("Ship plaque header or palette changed")
    return output, {"file_path": FILE, "source_sha256": sha(data), "target_sha256": sha(output),
                    "Japanese": japanese, "previous_English": previous, "English": replacement,
                    "original_face": list(face), "old_ink": sorted(old), "new_ink": sorted(new),
                    "changed_pixels": sum(a != b for a, b in zip(before, image.indices, strict=True)),
                    "all_nonlettered_grain_and_outer_frame_exact": True,
                    "header_palette_dimensions_and_all_other_pixels_exact": True,
                    "changed_records": [record_id]}


def render(candidate, clean):
    return render_label(candidate, clean, FACE, "Marines", "Quarters", "海兵詰所",
                        "DK4_SHIPS_MARINES_QUARTERS_TERMINOLOGY")


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-ship-quarters-label-v1":
        raise ValueError("Unknown ship Quarters label format")
    for key, data in (("source_sha256", candidate.read_file(FILE)),
                      ("clean_sha256", clean.read_file(FILE)),
                      ("font_arm9_sha256", candidate.read_file("/__arm9__.bin")),
                      ("donor_sha256", clean.read_file("/_pxl/towninfo.pxl"))):
        if sha(data) != config[key]:
            raise ValueError("Ship Quarters source lock differs: " + key)
    output, report = render(candidate, clean)
    if sha(output) != config["target_sha256"]:
        raise ValueError("Ship Quarters reviewed target differs")
    return FILE, output, report
