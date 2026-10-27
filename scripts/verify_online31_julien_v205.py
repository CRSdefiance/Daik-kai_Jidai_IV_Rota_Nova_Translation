"""Verify complete native screenshot, six glyph cells and release inheritance."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files, verify_golden_content
from scripts.prepare_online31_julien_v205 import BOX, NAME_GLYPHS, RESOURCE
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/online31_julien_v205")
PRIOR = Path("out/all_routes_combined_v204_candidate.nds")
CANDIDATE = Path("out/all_routes_combined_v205_candidate.nds")
CAPTURE = Path("work/emulation_v193/online31_julien_v205")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    old, new = NdsImage.open(PRIOR), NdsImage.open(CANDIDATE)
    before, after = rom_files(old), rom_files(new)
    assert [p for p in before if before[p] != after[p]] == [RESOURCE]
    previous, manifest = read(PRIOR.with_suffix(".manifest.json")), read(CANDIDATE.with_suffix(".manifest.json"))
    assert manifest["candidate_sha256"] == sha(CANDIDATE.read_bytes())
    assert manifest["profile"] == "all-routes-unified-v205" and len(manifest["batches"]) == 466
    assert manifest["batches"][:-1] == previous["batches"]
    assert manifest["batches"][-1].replace("\\", "/") == "translations/online31_julien_name_art_v1.json"
    assert manifest["relocations"] == previous["relocations"]
    assert all(manifest["changed_records"][p] == rows for p, rows in previous["changed_records"].items())
    assert manifest["changed_records"][RESOURCE] == ["DK4_ONLINE31_JULIEN_NAME_V1"]
    preparation = read(ROOT / "preparation.json")
    assert sha(after[RESOURCE]) == preparation["target_sha256"]
    a, b = PxlImage.from_bytes(before[RESOURCE]), PxlImage.from_bytes(after[RESOURCE])
    assert (a.width, a.height, a.palette, a.bits_per_pixel) == (b.width, b.height, b.palette, b.bits_per_pixel)
    assert before[RESOURCE][:a.pixels_offset] == after[RESOURCE][:b.pixels_offset]
    x0, y0, x1, y1 = BOX
    assert all(x == y for k, (x, y) in enumerate(zip(a.indices, b.indices, strict=True))
               if not x0 <= k % a.width < x1 or not y0 <= k // a.width < y1)
    capture = read(CAPTURE / "capture_report.json")
    assert capture["ROM_sha256"] == manifest["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    frame = next(row for row in capture["frames_captured"] if row["frame"] == 11300)
    assert sha(Path(frame["path"]).read_bytes()) == frame["PNG_sha256"]
    with Image.open(frame["path"]) as im:
        actual = im.convert("RGB")
    expected = b.render()
    assert all(native5(expected.getpixel((x, y))) == native5(actual.getpixel((x, y)))
               for y in range(192) for x in range(256))
    foreground = native5(tuple(preparation["foreground_from_original_name_palette"]))
    glyph_cases = []
    for origin in preparation["glyph_origins"]:
        rows = NAME_GLYPHS[origin["letter"]]
        count = 0
        for y, row in enumerate(rows):
            for x, ink in enumerate(row):
                assert (native5(actual.getpixel((origin["x"] + x, origin["y"] + y))) == foreground) == (ink == "1")
                count += ink == "1"
        glyph_cases.append({**origin, "complete_exact_ink_pixels": count, "all_glyph_ink_and_blank_cells_exact": True})
    assert (ROOT / "patch_reconstruction.nds").read_bytes() == CANDIDATE.read_bytes()
    verify_golden_content(NdsImage.open("out/raphael_natural_v2_accepted_base.nds"), new)
    town_path = CAPTURE / "town_regression/capture_report.json"
    town = read(town_path)
    assert town["ROM_sha256"] == manifest["candidate_sha256"] and town["cold_boot"]
    assert not town["savestate_loaded"] and not town["callback_errors"]
    town_frame = next(row for row in town["frames_captured"] if row["frame"] == 14900)
    assert sha(Path(town_frame["path"]).read_bytes()) == town_frame["PNG_sha256"]
    proof = {"format": "dk4-Online31-Julien-integrated-proof-v1", "candidate": CANDIDATE.as_posix(),
             "candidate_sha256": manifest["candidate_sha256"], "profile": manifest["profile"],
             "full_prior_465_batches_terminal_stages_and_record_ids_retained": True,
             "changed_paths_vs_V204": [RESOURCE], "all_headers_palettes_dimensions_unowned_pixels_exact": True,
             "complete_native_screenshot_pixels": 49152, "native_frame": frame,
             "six_complete_native_glyph_cells": glyph_cases,
             "first_and_last_name_letters_included": True,
             "estimated_background_inside_owned_name_box": True,
             "patch": CANDIDATE.with_suffix(".xdelta").as_posix(),
             "patch_sha256": sha(CANDIDATE.with_suffix(".xdelta").read_bytes()), "exact_patch_reconstruction": True,
             "town_UI_frame": town_frame, "visual_review": "pending-recording",
             "source_dialogue_chat_and_all_four_screenshots_still_unfinished": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_native_screenshot_pixels": 49152, "complete_glyphs": len(glyph_cases),
                      "exact_ink_pixels": sum(g["complete_exact_ink_pixels"] for g in glyph_cases),
                      "full_inheritance_and_patch_reconstruction": True}))


if __name__ == "__main__":
    main()
