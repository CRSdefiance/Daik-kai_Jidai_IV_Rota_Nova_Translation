"""Check live source icons and quantity glyphs; leave tiny indicator provenance open."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/common_atlas_consumers_v210")
CAPTURE = Path("work/emulation_v193/common_atlas_consumers_v210/trade_extended")


def main():
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    row = next(r for r in report["frames_captured"] if r["frame"] == 19700)
    path = Path(row["path"])
    assert sha(path.read_bytes()) == row["PNG_sha256"]
    with Image.open(path) as im:
        image = im.convert("RGB")
    rom = NdsImage.open("out/all_routes_combined_v205_candidate.nds")
    source = rom.read_file("/_pxl/itemtrade.pxl")
    assert source == NdsImage.open("work/clean.nds").read_file("/_pxl/itemtrade.pxl")
    atlas = PxlImage.from_bytes(source)
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    a = [(21, 0), (22, 0), (21, 1), (22, 1), (23, 1)]
    b = [(21, 1), (22, 1), (21, 2), (22, 3), (23, 3)]
    cases = []
    y0 = 286
    for index, x0, text, indicator in ((13, 84, "3", a), (14, 116, "5", a),
                                       (27, 148, "8", b), (78, 180, "7", b), (86, 212, "5", a)):
        expected = [native5(atlas.palette[v]) for v in atlas.indices[index * 576:(index + 1) * 576]]
        original = expected[:]
        mask = Image.new("1", (len(text) * 6, 11))
        for n, c in enumerate(text):
            mask.paste(font.decode(c), (n * 6, 0))
        # Observed native colors/positions; mask shape is independently from the ROM font.
        for y in range(11):
            for x in range(mask.width):
                if mask.getpixel((x, y)):
                    expected[(y + 13) * 24 + x + 3] = (0, 1, 0)
        for y in range(11):
            for x in range(mask.width):
                if mask.getpixel((x, y)):
                    expected[(y + 12) * 24 + x + 2] = (28, 28, 28)
        actual = [native5(image.getpixel((x0 + x, 286 + y))) for y in range(24) for x in range(24)]
        differences = [(n % 24, n // 24) for n, (x, y) in enumerate(zip(expected, actual, strict=True)) if x != y]
        assert differences == indicator
        assert all(actual[y * 24 + x] == (31, 31, 31) for x, y in indicator)
        assert all(expected[y * 24 + x] == actual[y * 24 + x]
                   for y in range(12, 24) for x in range(2, 3 + mask.width))
        assert 0 <= x0 < x0 + 24 <= image.width and image.height // 2 <= y0 < y0 + 24 <= image.height
        cases.append({"atlas_index": index, "native_bounds": [x0, 286, x0 + 24, 310],
                      "visible_quantity_text": text, "quantity_bounds_with_shadow": [x0 + 2, 298, x0 + 3 + mask.width, 310],
                      "complete_native_font_and_underlying_source_quantity_area_exact": True,
                      "first_last_digit_and_blank_cells_included": True,
                      "original_source_pixels_equal_before_quantity_overlay": sum(x == y for x, y in zip(original, actual, strict=True)),
                      "source_plus_quantity_pixels_exact": 576 - len(differences),
                      "remaining_unmapped_white_indicator_pixels": [list(p) for p in differences],
                      "indicator_coordinates_observed_not_independently_predicted": True,
                      "entire_composition_proved": False})
    proof = {"format": "dk4-live-market-icon-and-quantity-proof-v1", "ROM_sha256": report["ROM_sha256"],
             "capture": row, "atlas_path": "/_pxl/itemtrade.pxl", "atlas_sha256": sha(source),
             "cases": cases, "source_plus_quantity_exact_pixels": sum(c["source_plus_quantity_pixels_exact"] for c in cases),
             "unmapped_indicator_pixels": sum(len(c["remaining_unmapped_white_indicator_pixels"]) for c in cases),
             "all_five_icon_rectangles_and_quantity_bounds_in_viewport": True,
             "market_and_quantity_visual_review": "complete",
             "quantity_numeric_values_not_checked_against_inventory_RAM": True,
             "tiny_indicator_asset_draw_path_and_full_composition_pending": True,
             "all_icons_globally_or_hardware_verified": False, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "live_market_icon_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_market_icons": len(cases), "exact_source_plus_quantity_pixels": proof["source_plus_quantity_exact_pixels"],
                      "unmapped_indicator_pixels": proof["unmapped_indicator_pixels"]}))


if __name__ == "__main__":
    main()
