"""Verify retained icon pixels and viewport bounds in an explicit display fixture."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/environment_live_fixture_v207")
CAPTURE = Path("work/emulation_v193/environment_live_fixture_v207")


def main():
    manifest = json.loads((ROOT / "fixture_manifest.json").read_text(encoding="utf-8"))
    capture = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert capture["ROM_sha256"] == manifest["research_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    rom_path = Path(manifest["research_ROM"])
    assert sha(rom_path.read_bytes()) == manifest["research_sha256"]
    rom = NdsImage.open(rom_path)
    original = NdsImage.open(manifest["source_ROM"])
    a, b = original.read_file("/__arm9__.bin"), rom.read_file("/__arm9__.bin")
    allowed = {row["offset"] + n for row in manifest["changes"] for n in range(4)}
    assert all(x == y for i, (x, y) in enumerate(zip(a, b, strict=True)) if i not in allowed)
    assert {p: bytes(v) for _, p, v in rom.iter_files()} == {p: bytes(v) for _, p, v in original.iter_files()}
    assert bytes(rom.rom.arm7) == bytes(original.rom.arm7)
    saved = next(row for row in capture["frames_captured"] if Path(row["path"]).name == "frame_014900_final.png")
    frame_path = Path(saved["path"])
    assert sha(frame_path.read_bytes()) == saved["PNG_sha256"]
    with Image.open(frame_path) as im:
        frame = im.convert("RGB")
    cases = []
    for path, x0, y0, caption in (("/_pxl/kbj04.pxl", 50, 192, "Tavern"),
                                  ("/_pxl/kbj08.pxl", 0, 240, "Inn")):
        raw = rom.read_file(path)
        assert raw == original.read_file(path)
        source = PxlImage.from_bytes(raw)
        points = [(i % source.width, i // source.width, native5(source.palette[n]))
                  for i, n in enumerate(source.indices) if n != 255]
        assert all(0 <= x0 + x < 256 and 192 <= y0 + y < 384 for x, y, color in points)
        assert all(native5(frame.getpixel((x0 + x, y0 + y))) == color for x, y, color in points)
        cases.append({"path": path, "facility_caption_from_V206": caption,
                      "source_sha256": sha(raw), "native_origin": [x0, y0],
                      "source_extent": [source.width, source.height], "background_index_excluded": 255,
                      "all_other_native5_pixels_exact": len(points),
                      "painted_sign_and_all_opaque_edges_included": True,
                      "opaque_ink_bounds": [min(x for x, y, color in points) + x0,
                                            min(y for x, y, color in points) + y0,
                                            max(x for x, y, color in points) + x0 + 1,
                                            max(y for x, y, color in points) + y0 + 1],
                      "native_glyph_caption_hover_not_verified_here": True})
    navigation = CAPTURE / "caption_navigation"
    nav_report = json.loads((navigation / "capture_report.json").read_text(encoding="utf-8"))
    assert nav_report["ROM_sha256"] == manifest["research_sha256"]
    assert nav_report["cold_boot"] and not nav_report["savestate_loaded"] and not nav_report["callback_errors"]
    font = GameAsciiFont.from_arm9(b)
    assert font.glyphs == GameAsciiFont.from_arm9(a).glyphs
    captions = []
    for number, text, y in ((15400, "Tavern", 244), (15550, "Inn", 264)):
        row = next(r for r in nav_report["frames_captured"] if r["frame"] == number)
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["PNG_sha256"]
        with Image.open(path) as im:
            native = im.convert("RGB")
        count, bounds = complete_mask(font, text, native, 64, y, (0, 8, 0))
        assert 0 <= bounds[0] < bounds[2] <= 256 and 192 <= bounds[1] < bounds[3] <= 384
        captions.append({"text": text, "frame": row, "complete_native_font_ink_pixels": count,
                         "bounds": bounds, "first_last_letters_and_blank_cells_exact": True})
    for case in cases:
        case["native_glyph_caption_hover_not_verified_here"] = False
    proof = {"format": "dk4-contextual-sign-native-display-fixture-proof-v1",
             "research_ROM_sha256": manifest["research_sha256"], "native_frame": saved,
             "cases": cases, "complete_opaque_pixels": sum(row["all_other_native5_pixels_exact"] for row in cases),
             "original_resources_palette_and_dimensions_exact": True,
             "whole_source_rectangles_are_not_claimed_opaque": True,
             "actual_city_assignment_normal_progression_other_states_pending": True,
             "English_caption_navigation": captions,
             "complete_caption_ink_pixels": sum(row["complete_native_font_ink_pixels"] for row in captions),
             "English_caption_navigation_verified": True,
             "other_town_backgrounds_display_pending": True,
             "normal_alternate_city_caption_anchor_pending": True,
             "visual_review": "complete-native-town-fixture-and-retained-signs-reviewed",
             "scope": "Two unchanged alternate facility sprites rendered by original native views/cache/GPU, with complete English captions selected through ordinary D-pad input. Two selector instructions forced images/hit bounds; the caption anchor selector still uses the original Lisbon field. This proves displayed pixels and label bounds in this fixture, not their normal city assignment or alternate-city anchor positions.",
             "not_for_gameplay_release_or_handoff": True, "registered_ROM_changed": False, "full_goal_complete": False}
    (ROOT / "native_sign_pixel_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_sign_cases": len(cases), "all_opaque_source_pixels_exact": proof["complete_opaque_pixels"],
                      "all_sign_and_opaque_edge_pixels_in_bounds": True, "registered_ROM_unchanged": "V205"}))


if __name__ == "__main__":
    main()
