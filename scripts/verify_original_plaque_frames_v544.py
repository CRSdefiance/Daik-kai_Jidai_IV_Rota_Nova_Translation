"""Whole native town/faction plaques, source frames, full English and patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/town_force_texture_v544")
ROM = Path("out/all_routes_combined_v544_candidate.nds")
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
    current = NdsImage.open(ROM)
    parent = NdsImage.open("out/all_routes_combined_v543_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix(".manifest.json"))
    previous = read("out/all_routes_combined_v543_candidate.manifest.json")
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v544"
    assert manifest["batches"] == previous["batches"] and len(manifest["batches"]) == 470
    assert len(read("translations/release_stack.json")["accepted_layers"]) == 114
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys()
    assert sorted(p for p in old if old[p] != new[p]) == ["/_pxl/forceinfo.pxl", "/_pxl/towninfo.pxl"]
    font = GameAsciiFont.from_arm9(new["/__arm9__.bin"])
    config = read("translations/original_plaque_frames_v1.json")
    masks, known, owned = [], 0, set()
    for group, batch_name in zip(config["files"], ("trading_towninfo_graphics_v2", "force_info_graphics_v2"), strict=True):
        path = group["file_path"]
        asset, source, prior = [PxlImage.from_bytes(data) for data in (new[path], clean.read_file(path), old[path])]
        assert sha(asset.source) == group["target_sha256"]
        assert asset.source[:asset.pixels_offset] == prior.source[:prior.pixels_offset]
        assert asset.palette == source.palette
        batch = read(f"translations/{batch_name}.json")
        local_owned = set()
        for row, legacy in zip(group["records"], batch["records"], strict=True):
            l, t, r, b = row["restore_box"]
            el, et, er, eb = row["japanese_stroke_box"]
            bl, bt, br, bb = legacy["box"]
            tx = bl + (br - bl - len(row["english"]) * 5) // 2
            ty = bt + (bb - bt - 11) // 2
            expected = set()
            for n, char in enumerate(row["english"]):
                glyph = font.decode(char)
                assert not glyph.crop((5, 0, 6, 11)).getbbox()
                expected.update((tx + n * 5 + x, ty + y)
                                for y in range(11) for x in range(6) if glyph.getpixel((x, y)))
            actual = {(x, y) for y in range(ty, ty + 11) for x in range(bl, br)
                      if asset.indices[y * asset.width + x] == row["ink_palette_index"]}
            assert actual == expected, row["english"]
            for y in range(t, b):
                for x in range(l, r):
                    at = y * asset.width + x
                    if prior.indices[at] != row["ink_palette_index"] and not (
                            el <= x < er and et <= y < eb and source.palette[source.indices[at]][0] < 140):
                        assert asset.indices[at] == source.indices[at], (path, x, y)
                        known += 1
                    local_owned.add(at)
                    owned.add((x, y))
            masks.append({"english": row["english"], "complete_font_ink_pixels": len(expected),
                          "first_and_final_letters_exact": True, "source_frame_and_visible_grain_exact": True})
        assert all(a == b for p, (a, b) in enumerate(zip(prior.indices, asset.indices)) if p not in local_owned)
    run = report(CAPTURES / "original_frames_v544_map", digest)
    frames = {s["frame"]: s for s in run["frames_captured"]}
    native = []
    for group, selections in zip(config["files"], ((33600,), (34800, 35200)), strict=True):
        asset = PxlImage.from_bytes(new[group["file_path"]])
        for frame in selections:
            image = Image.open(frames[frame]["path"]).convert("RGB")
            for row in group["records"]:
                l, t, r, b = row["restore_box"]
                assert all(native5(image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
                           for y in range(t, b) for x in range(l, r)), (row["english"], frame)
                native.append({"english": row["english"], "frame": frame,
                               "whole_source_frame_grain_and_complete_letters_exact": (r - l) * (b - t),
                               "capture": frames[frame]["path"]})
    fresh = report(CAPTURES / "original_frames_v544_fresh", digest)
    before = report(CAPTURES / "equipment_texture_v543_fresh", sha(parent.source.read_bytes()))
    assert fresh["scripted_input_schedule"] == before["scripted_input_schedule"]
    assert fresh["core_options"] == before["core_options"]
    a, b = [{s["frame"]: s for s in r["frames_captured"]} for r in (fresh, before)]
    assert a.keys() == b.keys() and len(a) == 56
    changed_frames, changed_pixels = 0, 0
    for frame in a:
        aa, bb = [Image.open(row[frame]["path"]).convert("RGB") for row in (a, b)]
        delta = {(x, y) for y in range(384) for x in range(256) if aa.getpixel((x, y)) != bb.getpixel((x, y))}
        assert delta <= owned, (frame, len(delta - owned))
        changed_frames += bool(delta)
        changed_pixels += len(delta)
    preservation = read("work/analysis/equipment_texture_v543/preservation_proof.json")
    assert len(preservation["entries"]) == 921
    for path in ("/_pxl/forceinfo.pxl", "/_pxl/towninfo.pxl"):
        source, target = PxlImage.from_bytes(clean.read_file(path)), PxlImage.from_bytes(new[path])
        assert source.source[:source.pixels_offset] == target.source[:target.pixels_offset]
        assert len(source.indices) == len(target.indices)
    assert all(old[row["path"]] == new[row["path"]] for row in preservation["entries"]
               if row["path"] not in ("/_pxl/forceinfo.pxl", "/_pxl/towninfo.pxl"))
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        parent_proof="work/analysis/equipment_texture_v543/preservation_proof.json")
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
             "all11_complete_English_masks": masks, "native_crops": native,
             "visible_source_pixels_exact": known, "all_unowned_pixels_palette_dimensions_exact": True,
             "all56_regression_frames_only_intended_upper_plaque_differences": True,
             "regression_changed_frames": changed_frames, "regression_changed_pixels": changed_pixels,
             "all56_regression_frames_pixel_exact_V543": changed_frames == 0,
             "all_470_batches114_layers921_preservation_entries_retained": True,
             "all_code_and_equipment_fix_exact_V543": True, "ordinary_New_Game_no_fixture_or_savestate": True,
             "concealed_texture_reconstructed_not_exact_recovery": True,
             "all18_entries_remain_incomplete": True, "experimental": True,
             "canonical_promoted": False, "full_goal_complete": False}
    (ROOT / "release_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"V544: 11 full masks, {len(native)} native source-frame crops, {known} original visible pixels, 56 scoped regression frames, exact patch.")


if __name__ == "__main__":
    main()
