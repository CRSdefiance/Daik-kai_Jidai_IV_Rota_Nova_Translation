"""Verify actual plaque crops, full letters, preservation and exact clean patch."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path("out/all_routes_combined_v542_candidate.nds")
ROOT = Path("work/analysis/plaque_texture_v542")
CAPTURES = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def masks(asset, records, font):
    results = []
    for row in records:
        left, top, right, bottom = row["draw_box"]
        text = row["english"]
        tx = left + (right - left - len(text) * 5) // 2
        ty = top + (bottom - top - 11) // 2
        expected = set()
        for n, char in enumerate(text):
            glyph = font.decode(char)
            assert not glyph.crop((5, 0, 6, 11)).getbbox(), char
            expected.update((tx + n * 5 + x, ty + y)
                            for y in range(11) for x in range(6) if glyph.getpixel((x, y)))
        x0, y0, x1, y1 = row["plaque_box"]
        actual = {(x, y) for y in range(y0, y1) for x in range(x0, x1)
                  if asset.indices[y * asset.width + x] == row["ink_palette_index"]}
        assert actual == expected, row["id"]
        assert all(x0 <= x < x1 and y0 <= y < y1 for x, y in expected)
        results.append({"id": row["id"], "english": text,
                        "complete_ink_pixels": len(expected),
                        "complete_first_and_final_letters_and_all_font_pixels": True})
    return results


def capture_report(folder, digest):
    report = read(folder / "capture_report.json")
    assert report["ROM_sha256"] == digest and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    for frame in report["frames_captured"]:
        assert sha(Path(frame["path"]).read_bytes()) == frame["PNG_sha256"]
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    current = NdsImage.open(ROM)
    parent = NdsImage.open("out/all_routes_combined_v540_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix(".manifest.json"))
    stack = read("translations/release_stack.json")
    prior_manifest = read("out/all_routes_combined_v540_candidate.manifest.json")
    assert manifest["candidate_sha256"] == digest
    assert manifest["profile"] == "all-routes-unified-v542"
    assert manifest["base_sha256"] == stack["canonical_baseline"]["sha256"]
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["batches"] == prior_manifest["batches"] and len(manifest["batches"]) == 470
    assert len(stack["accepted_layers"]) == 114
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    paths = ["/_pxl/dividecrewinfo.pxl", "/_pxl/personinfo.pxl"]
    assert old.keys() == new.keys()
    assert sorted(p for p in old if old[p] != new[p]) == paths
    config = read("translations/source_plaque_grain_v1.json")
    font = GameAsciiFont.from_arm9(new["/__arm9__.bin"])
    cases = []
    for group in config["files"]:
        path = group["file_path"]
        a, b = PxlImage.from_bytes(old[path]), PxlImage.from_bytes(new[path])
        assert sha(old[path]) == group["source_sha256"]
        assert sha(new[path]) == group["target_sha256"]
        assert a.source[:a.pixels_offset] == b.source[:b.pixels_offset]
        allowed = {y * a.width + x for row in group["records"]
                   for y in range(row["plaque_box"][1] + 2, row["plaque_box"][3] - 2)
                   for x in range(row["plaque_box"][0] + 2, row["plaque_box"][2] - 2)
                   if a.indices[y * a.width + x] != row["ink_palette_index"]}
        assert all(x == y for n, (x, y) in enumerate(zip(a.indices, b.indices)) if n not in allowed)
        cases.append({"path": path, "full_font_masks": masks(b, group["records"], font),
                      "bevels_palette_dimensions_and_all_unowned_pixels_exact_parent": True})
    preservation = []
    for _, path, source in clean.iter_files():
        saved = new[path]
        if path.lower().endswith(".pxl"):
            a, b = struct.unpack_from("<5I", source), struct.unpack_from("<5I", saved)
            assert a[:3] == b[:3]
            length = 32 if a[0] & 255 == 4 else 512
            assert source[a[3]:a[3] + length] == saved[b[3]:b[3] + length]
            assert len(source) - a[4] == len(saved) - b[4]
            preservation.append({"path": path, "kind": "PXL", "original_metadata_palette_extent_exact": True})
        elif path.lower().endswith(".fls"):
            a, b = FlsArchive(source), FlsArchive(saved)
            assert a.count == b.count and a.compressed_storage == b.compressed_storage
            for index in range(a.count):
                aa, bb = a.texture(index), b.texture(index)
                assert (aa.flags, aa.width, aa.height, aa.palette, len(aa.indices)) == (
                    bb.flags, bb.width, bb.height, bb.palette, len(bb.indices))
                preservation.append({"path": path, "kind": "FLS", "texture": index,
                                     "original_metadata_palette_extent_exact": True})
    assert len(preservation) == 921
    write(ROOT / "preservation_proof.json", {"candidate_sha256": digest, "entries": preservation,
                                            "visual_quality_and_full_translation_not_inferred": True})
    patch = ROM.with_suffix(".xdelta")
    if not patch.exists():
        make_xdelta(Path("work/clean.nds"), ROM, patch)
    reconstructed = ROOT / "reconstructed.nds"
    apply_xdelta(Path("work/clean.nds"), patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    proof = {"candidate": str(ROM), "candidate_sha256": digest,
             "base": manifest["base_rom"], "base_sha256": manifest["base_sha256"],
             "profile": manifest["profile"], "patch_sha256": sha(patch.read_bytes()),
             "exact_clean_patch_reconstruction": True, "inherited_batches": 470,
             "accepted_layers": 114, "preservation_entries": 921,
             "only_two_plaque_atlases_changed_from_V540": True,
             "all_code_and_other_translations_exact_V540": True, "asset_cases": cases,
             "experimental": True, "canonical_promoted": False, "full_goal_complete": False}
    if args.static_only:
        write(ROOT / "static_release_proof.json", proof)
        print("V542 static: 17 full font masks, owned grain pixels, all921 preservation entries, exact patch.")
        return
    live = []
    for name, group, selections in zip(("crew", "person"), config["files"],
                                       ((10000, 10300, 10600), (10500, 12600, 13500, 14400)), strict=True):
        report = capture_report(CAPTURES / f"plaque_texture_v542_{name}", digest)
        frames = {r["frame"]: r for r in report["frames_captured"]}
        asset = PxlImage.from_bytes(new[group["file_path"]])
        for frame in selections:
            shot = Image.open(frames[frame]["path"]).convert("RGB")
            for row in group["records"]:
                l, t, r, b = row["plaque_box"]
                assert all(native5(shot.getpixel((x, y))) == native5(
                    asset.palette[asset.indices[y * asset.width + x]])
                    for y in range(t, b) for x in range(l, r)), (name, frame, row["id"])
                live.append({"screen": name, "frame": frame, "id": row["id"],
                             "complete_plaque_bounds_pixels_exact": (r - l) * (b - t),
                             "all_grain_bevel_and_full_letters_inside_native_display": True,
                             "capture": frames[frame]["path"], "fully_completed": False})
    fresh = capture_report(CAPTURES / "plaque_texture_v542_fresh", digest)
    previous = capture_report(CAPTURES / "coin_game_v540_fresh", sha(parent.source.read_bytes()))
    assert fresh["scripted_input_schedule"] == previous["scripted_input_schedule"]
    assert fresh["core_options"] == previous["core_options"]
    a, b = [{r["frame"]: r["PNG_sha256"] for r in rep["frames_captured"]}
            for rep in (fresh, previous)]
    assert a == b and len(a) == 56
    requirements = read("translations/graphics_completion_requirements_v313.json")
    plaques = read("translations/graphics_completion_campaign_v1.json")["plaque_style_v247"]["ongoing_plaque_inventory"]
    assert len(requirements["historical_pending_items_retained"]) == 22
    assert len(plaques) == 18 and all(not p["fully_completed"] for p in plaques)
    proof.update(native_plaque_cases=live, exact_V540_regression_frames=56,
                 all22_requirements_and18_incomplete_entries_retained=True,
                 remaining="Other plaques, original bevel comparison, equipment hints and global graphics audit remain open.")
    write(ROOT / "release_proof.json", proof)
    print(f"V542 native: {len(live)} complete plaque crops, 17 full masks, 56 exact regression frames, exact patch.")


if __name__ == "__main__":
    main()
