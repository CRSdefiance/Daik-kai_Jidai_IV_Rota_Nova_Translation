"""Source-framed Golden Route labels and complete natural financial headings."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha

FILES = ("/_pxl/goldsearoutediscovery.pxl", "/_pxl/goldsearoutelog.pxl", "/_pxl/goldsearoutelog2.pxl")


def blank_goods(original):
    """Coherent own-header source patch, with visible neighbouring controls."""
    result = PxlImage.from_bytes(original.source)
    left, right = 60, 108
    candidates = []
    for source_x in (*range(4, 15), *range(110, 117)):
        if any(sum(original.palette[original.indices[y * 256 + source_x + x]][:3]) < 260
               for y in range(2, 14) for x in range(right - left)):
            continue
        controls = [(x, y) for x in (-2, -1, right - left, right - left + 1) for y in range(2, 14)]
        score = sum(sum(abs(original.palette[original.indices[y * 256 + left + x]][k] // 8
                            - original.palette[original.indices[y * 256 + source_x + x]][k] // 8)
                        for k in range(3)) for x, y in controls)
        candidates.append((score, source_x))
    if not candidates:
        raise ValueError("No reviewed unlettered Golden Route header donor")
    score, sx = min(candidates)
    for y in range(2, 14):
        for x in range(left, right):
            result.indices[y * 256 + x] = original.indices[y * 256 + sx + x - left]
    return result, {"original_Goods_header_concealed_patch": [left, 2, right, 14],
                    "own_unlettered_source_patch": [sx, 2, sx + right - left, 14],
                    "neighbour_control_RGB5_absolute_error": score,
                    "concealed_texture_inferred_not_recovered": True}


def glyphs(font, text, face):
    l, t, r, b = face
    x0, y0 = l + (r - l - len(text) * 5) // 2, t + (b - t - 11) // 2
    return {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(text)
            for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}, (x0, y0)


def transform(inherited, originals, arm):
    font = GameAsciiFont.from_arm9(arm)
    outputs, reports = {}, []
    for path in FILES:
        old, source = PxlImage.from_bytes(inherited[path]), PxlImage.from_bytes(originals[path])
        assert old.source[:old.pixels_offset] == source.source[:source.pixels_offset]
        result = PxlImage.from_bytes(source.source)
        blank_source = PxlImage.from_bytes(originals[FILES[1]])
        blank, donor_proof = blank_goods(blank_source)
        mapping = {rgb: min((i for i in range(256) if i != 1),
                           key=lambda i: sum((result.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
                   for rgb in blank.palette}
        if path == FILES[0]:
            rows = (("GOODS", "交易品", "Goods", (8, 16, 48, 32), (8, 16, 48, 32), (7, 16, 49, 35)),
                    ("PROFIT_RATE", "利益率", "Profit %", (5, 52, 49, 68), (8, 52, 48, 68), (5, 48, 49, 68)),
                    ("REWARD", "報奨金", "Reward", (8, 80, 48, 96), (8, 80, 48, 96), (7, 80, 49, 99)))
        elif path == FILES[1]:
            rows = (("GOODS", "交易品", "Goods", (0, 0, 168, 16), (0, 0, 168, 16), (0, 0, 168, 18)),
                    ("PROFIT_RATE", "利益率", "Profit %", (168, 0, 212, 16), (168, 0, 212, 16), (168, 0, 212, 18)),
                    ("REWARD", "報奨金", "Reward", (212, 0, 256, 16), (212, 0, 256, 16), (212, 0, 256, 18)))
        else:
            rows = (("GOODS", "交易品", "Goods", (0, 0, 168, 16), (0, 0, 168, 16), (0, 0, 168, 18)),
                    ("TOTAL_REWARDS", "報奨金 合計", "Total Rewards", (168, 0, 256, 16), (168, 0, 256, 16), (168, 0, 256, 18)))
        records, owned = [], set()
        for ident, japanese, text, face, original_face, restore in rows:
            l, t, r, b = face
            sl, st, sr, sb = original_face
            assert b - t == sb - st == 16
            rl, rt, rr, rb = restore
            owned.update(y * 256 + x for y in range(rt, rb) for x in range(rl, rr))
            if r - l == 168:
                # Preserve every visible source rim and all source material
                # outside the contiguous Japanese-letter reconstruction band.
                for y in range(2, 14):
                    for x in range(60, 108):
                        result.indices[y * 256 + x] = blank.indices[y * 256 + x]
                font_box = (60, 2, 108, 14)
            else:
                width = r - l
                for dy in range(16):
                    for dx in range(width):
                        if 2 <= dx < width - 2 and 2 <= dy < 14:
                            # A contiguous source region. Wider cumulative
                            # heading also includes the explicitly inferred
                            # Goods-letter patch; no periodic tiling is added.
                            sx, sy = 4 + dx - 2, 2 + dy - 2
                            value = mapping[blank.palette[blank.indices[sy * 256 + sx]]]
                        else:
                            original_width = sr - sl
                            sx = sl + (dx if dx < 2 else original_width - (width - dx) if dx >= width - 2
                                       else 2 + (dx - 2) % (original_width - 4))
                            value = source.indices[(st + dy) * 256 + sx]
                        result.indices[(t + dy) * 256 + l + dx] = value
                font_box = (l + 2, t + 2, r - 2, b - 2)
            points, origin = glyphs(font, text, face)
            assert all(font_box[0] <= x < font_box[2] and font_box[1] <= y < font_box[3] for x, y in points)
            for x, y in points:
                result.indices[y * 256 + x] = 1
            fl, ft, fr, fb = font_box
            actual = {(x, y) for y in range(ft, fb) for x in range(fl, fr) if result.indices[y * 256 + x] == 1}
            assert actual == points, (path, text)
            records.append({"id": "DK4_GOLDEN_" + Path(path).stem.upper() + "_" + ident + "_SOURCE_MATERIAL",
                            "Japanese": japanese, "English": text, "original_plaque_box": list(original_face),
                            "plaque_box": list(face), "restore_box": list(restore), "font_box": list(font_box),
                            "font_origin": list(origin), "complete_font_ink": len(points), "fully_completed": False})
        assert all(a == b for i, (a, b) in enumerate(zip(old.indices, result.indices, strict=True)) if i not in owned), path
        output = result.to_bytes()
        assert output[:old.pixels_offset] == old.source[:old.pixels_offset]
        outputs[path] = output
        reports.append({"file_path": path, "source_sha256": sha(old.source), "clean_sha256": sha(source.source),
                        "target_sha256": sha(output), "records": records, "donor": donor_proof,
                        "base_donor_file": FILES[1], "base_donor_sha256": sha(blank_source.source),
                        "material_has_no_added_periodic_repeat_or_stretch": True,
                        "changed_pixels": sum(a != b for a, b in zip(old.indices, result.indices, strict=True)),
                        "unowned_pixels_header_palettes_and_dimensions_exact": True})
    return outputs, reports


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-golden-route-plaques-v1":
        raise ValueError("Unknown Golden Route plaque repair")
    inherited, originals = ({p: r.read_file(p) for p in FILES} for r in (candidate, clean))
    for row in config["files"]:
        p = row["file_path"]
        if sha(inherited[p]) != row["source_sha256"] or sha(originals[p]) != row["clean_sha256"]:
            raise ValueError("Original or inherited Golden Route material source differs")
    output, reports = transform(inherited, originals, candidate.read_file("/__arm9__.bin"))
    if reports != config["files"]:
        raise ValueError("Reviewed Golden Route material/wording target differs")
    return output, reports
