"""Verify the complete native treasure header, original grain and exact patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.treasure_source_grain import BOX, PATH, STROKES, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path("out/all_routes_combined_v545_candidate.nds")
ROOT = Path("work/analysis/treasure_texture_v545")
CAPTURES = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def report(folder, digest):
    result = read(folder / "capture_report.json")
    assert result["ROM_sha256"] == digest and result["cold_boot"]
    assert not result["savestate_loaded"] and not result["callback_errors"]
    for row in result["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    return result


def main():
    current, parent, clean = [NdsImage.open(p) for p in
                              (ROM, "out/all_routes_combined_v544_candidate.nds", "work/clean.nds")]
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix(".manifest.json"))
    old_manifest = read("out/all_routes_combined_v544_candidate.manifest.json")
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v545"
    assert manifest["batches"] == old_manifest["batches"] and len(manifest["batches"]) == 470
    assert len(read("translations/release_stack.json")["accepted_layers"]) == 114
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys() and [p for p in old if old[p] != new[p]] == [PATH]
    expected, plan = apply_release(parent, clean, "translations/treasure_source_grain_v1.json")
    assert new[PATH] == expected
    asset, original, prior = [PxlImage.from_bytes(d) for d in (new[PATH], clean.read_file(PATH), old[PATH])]
    assert asset.source[:asset.pixels_offset] == original.source[:original.pixels_offset]
    font = GameAsciiFont.from_arm9(new["/__arm9__.bin"])
    mask = {(90 + n * 6 + x, 2 + y) for n, char in enumerate("Treasure Name")
            for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
    actual = {(x, y) for y in range(15) for x in range(84, 174) if asset.indices[y * 256 + x] == 7}
    assert actual == mask
    visible = 0
    for y in range(asset.height):
        for x in range(asset.width):
            at = y * asset.width + x
            if not (BOX[0] <= x < BOX[2] and BOX[1] <= y < BOX[3]):
                assert asset.indices[at] == prior.indices[at]
            elif (x, y) not in mask and not any(l <= x < r and t <= y < b
                    and original.palette[original.indices[at]][0] < 140 for l, t, r, b in STROKES):
                assert asset.indices[at] == original.indices[at]
                visible += 1
    assert visible == plan["visible_source_pixels_preserved"] == 1046
    run = report(CAPTURES / "treasure_texture_v545_list_confirmed", digest)
    frames = {s["frame"]: s for s in run["frames_captured"]}
    parent_run = report(CAPTURES / "treasure_texture_v545_parent_list", sha(parent.source.read_bytes()))
    assert run["scripted_input_schedule"] == parent_run["scripted_input_schedule"]
    assert run["core_options"] == parent_run["core_options"]
    parent_frames = {s["frame"]: s for s in parent_run["frames_captured"]}
    native = []
    for frame in (5200, 5600, 6000, 6400):
        shot = Image.open(frames[frame]["path"]).convert("RGB")
        assert all(native5(shot.getpixel((x, 192 + y))) == native5(asset.palette[asset.indices[y * 256 + x]])
                   for y in range(13) for x in range(84, 174)), frame
        actual_ink = {(x, y - 192) for y in range(192, 207) for x in range(84, 174)
                      if native5(shot.getpixel((x, y))) == native5(asset.palette[7])}
        assert actual_ink == mask
        before_shot = Image.open(parent_frames[frame]["path"]).convert("RGB")
        delta = {(x, y) for y in range(384) for x in range(256)
                 if shot.getpixel((x, y)) != before_shot.getpixel((x, y))}
        assert all(84 <= x < 174 and 192 <= y < 205 for x, y in delta)
        assert shot.crop((84, 205, 174, 207)).tobytes() == before_shot.crop((84, 205, 174, 207)).tobytes()
        native.append({"frame": frame, "visible_header_pixels_exact": 1170,
                       "full_first_final_and_interior_glyphs_exact": True,
                       "native_visible_bounds": [84, 192, 174, 205],
                       "source_rows13_14_overlaid_by_unchanged_native_divider": True,
                       "all_surrounding_pixels_exact_V544": True,
                       "changed_grain_pixels": len(delta), "capture": frames[frame]["path"]})
    save = read(ROOT / "save_copy_manifest.json")
    assert sha(Path(save["source"]).read_bytes()) == save["source_sha256"]
    assert sha(Path(save["test_copy"]).read_bytes()) == save["test_copy_sha256"]
    fresh = report(CAPTURES / "treasure_texture_v545_fresh", digest)
    before = report(CAPTURES / "original_frames_v544_fresh", sha(parent.source.read_bytes()))
    assert fresh["scripted_input_schedule"] == before["scripted_input_schedule"]
    assert fresh["core_options"] == before["core_options"]
    a, b = [{s["frame"]: s["PNG_sha256"] for s in r["frames_captured"]} for r in (fresh, before)]
    assert a == b and len(a) == 56
    preservation = read("work/analysis/town_force_texture_v544/preservation_proof.json")
    assert len(preservation["entries"]) == 921
    assert all(old[r["path"]] == new[r["path"]] for r in preservation["entries"] if r["path"] != PATH)
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        parent_proof="work/analysis/town_force_texture_v544/preservation_proof.json")
    (ROOT / "preservation_proof.json").write_text(json.dumps(preservation, indent=2) + "\n", encoding="utf-8")
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(Path("work/clean.nds"), ROM, patch)
    apply_xdelta(Path("work/clean.nds"), patch, ROOT / "reconstructed.nds")
    assert (ROOT / "reconstructed.nds").read_bytes() == ROM.read_bytes()
    plaques = read("translations/graphics_completion_campaign_v1.json")["plaque_style_v247"]["ongoing_plaque_inventory"]
    assert len(plaques) == 18 and all(not p["fully_completed"] for p in plaques)
    assert len(read("translations/graphics_completion_requirements_v313.json")["historical_pending_items_retained"]) == 22
    proof = {"candidate": str(ROM), "candidate_sha256": digest, "profile": manifest["profile"],
             "base": manifest["base_rom"], "base_sha256": manifest["base_sha256"],
             "patch_sha256": sha(patch.read_bytes()), "exact_clean_patch_reconstruction": True,
             "source_texture_plan": plan, "native_header_cases": native,
             "all_470_batches114_layers921_preservation_entries_retained": True,
             "all56_fresh_regression_frames_exact_V544": True,
             "all_code_other_art_and_six_list_rows_unchanged": True,
             "separate_historical_save_and_test_copy_unchanged": True,
             "normal_historical_item_acquisition_not_claimed": True,
             "initial_menu_only_attempt_not_native_header_credit": True,
             "all18_entries_remain_incomplete": True, "experimental": True,
             "canonical_promoted": False, "full_goal_complete": False}
    (ROOT / "release_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("V545: four complete native headers, 1046 original pixels, 56 unchanged regression frames and exact patch pass.")


if __name__ == "__main__":
    main()
