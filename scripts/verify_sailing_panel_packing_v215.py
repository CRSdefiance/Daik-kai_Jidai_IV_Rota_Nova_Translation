"""Recover source bank placement from original output and actual Japanese capture."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/sailing_panel_packing_v215")
SOURCE = Path("work/analysis/sailing_panel_overlay_v214")
CAPTURE = Path("work/emulation_v193/generated_modes_v213")


def read_pixel(raw, x, y):
    # Producer word placement recovered from original 01FFB6A4:
    # consecutive 32x16 banks, each containing four by two 8x8 tiles.
    tile = x // 32 * 8 + x % 32 // 8 + y // 8 * 4
    byte = tile * 32 + y % 8 * 4 + x % 8 // 2
    return raw[byte] >> (x % 2 * 4) & 15


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source_proof = json.loads((SOURCE / "calibration.json").read_text(encoding="utf-8"))
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert source_proof["ROM_sha256"] == report["ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    case = next(row for row in source_proof["cases"] if row["name"] == "search")
    raw = Path(case["output"]).read_bytes()
    assert sha(raw) == case["output_sha256"]
    captured = next(row for row in report["frames_captured"] if row["frame"] == 17900)
    assert sha(Path(captured["path"]).read_bytes()) == captured["PNG_sha256"]
    with Image.open(captured["path"]) as im:
        actual = im.convert("RGB")
    placements = [("heading", 0, 192, 56, 2)]
    placements.extend((f"body-{n}", x, width, 8, 32 + n * 16)
                      for n, (x, width) in enumerate(((192, 192), (384, 240), (672, 192),
                                                      (864, 240), (1152, 240), (1440, 240), (1728, 64))))
    rows = []
    for name, source_x, width, x0, y0 in placements:
        glyph = Image.new("1", (width, 16))
        for y in range(16):
            for x in range(width):
                predicted = read_pixel(raw, source_x + x, y) == 15
                observed = native5(actual.getpixel((x0 + x, y0 + y))) == (31, 31, 31)
                assert predicted == observed, (name, x, y)
                glyph.putpixel((x, y), predicted)
        path = ROOT / (name + "_complete_foreground.png")
        glyph.convert("L").save(path)
        rows.append({"region": name, "source_virtual_x": source_x, "native_origin": [x0, y0],
                     "compared_dimensions": [width, 16], "complete_foreground_and_blank_mask_pixels": width * 16,
                     "all_foreground_bits_and_blank_cells_exact": True,
                     "foreground_mask": path.as_posix(), "mask_sha256": sha(path.read_bytes())})
    result = {"format": "dk4-sailing-original-native-bank-screen-match-v1",
              "ROM_sha256": report["ROM_sha256"], "source_producer_output_sha256": sha(raw),
              "capture": captured, "bank_geometry": [32, 16], "tile_geometry": [8, 8],
              "heading_offset": [56, 2], "regions": rows,
              "exact_foreground_and_blank_pixels": sum(r["complete_foreground_and_blank_mask_pixels"] for r in rows),
              "mask_comparison_does_not_prove_all_palette_or_shadow_colors": True,
              "first_and_third_body_rows_have_narrower_source_regions": True,
              "last_body_width_is_complete_known_source_region_not_all_blank_viewport": 64,
              "all_other_panels_and_English_packing_callback_still_pending": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "screen_mapping.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exact_source_screen_regions": len(rows),
                      "exact_foreground_and_blank_pixels": result["exact_foreground_and_blank_pixels"],
                      "English_integration_pending": True}))


if __name__ == "__main__":
    main()
