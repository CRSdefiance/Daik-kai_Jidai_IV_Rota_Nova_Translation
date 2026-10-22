"""Independent asset checks and an explicitly unsuccessful native display experiment."""

import argparse
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_fleet_plaques import DONOR, FILE, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, report, save

ROOT = Path("work/analysis/regional_plaques_v611")
ROM = Path("out/all_routes_combined_v611_candidate.nds")
PARENT = Path("out/all_routes_combined_v610_candidate.nds")
CAP = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def static():
    parent, rom, clean = [NdsImage.open(p) for p in (PARENT, ROM, "work/clean.nds")]
    before = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    after = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == [FILE]
    replacements, transform = apply_release(parent, clean, "translations/regional_fleet_plaques_v1.json")
    assert replacements[FILE] == after[FILE] and len(transform["records"]) == 5
    manifest, previous, stack = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json")), read("translations/release_stack.json")
    assert manifest["profile"] == "all-routes-unified-v611" and manifest["candidate_sha256"] == sha(ROM.read_bytes())
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["base_sha256"] == stack["canonical_baseline"]["sha256"] == sha(Path(manifest["base_rom"]).read_bytes())
    assert manifest["batches"] == previous["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == previous["required_batches"] and len(stack["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    atlas, source, donor = [PxlImage.from_bytes(d) for d in (after[FILE], clean.read_file(FILE), clean.read_file(DONOR))]
    assert atlas.source[:atlas.pixels_offset] == source.source[:source.pixels_offset]
    font = GameAsciiFont.from_arm9(after["/__arm9__.bin"])
    masks, points = [], set()
    for row in transform["records"]:
        left, top, right, bottom = row["plaque_box"]
        sl, st, sr, sb = row["original_plaque_box"]
        assert sr - sl == 40 and sb - st == 16
        text = row["English"]
        x0, y0 = left + (right - left - 5 * len(text)) // 2, top + 2
        expected = {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(text)
                    for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        actual = {(x, y) for y in range(top + 2, bottom - 2) for x in range(left + 2, right - 2)
                  if atlas.indices[y * 256 + x] == 1}
        assert expected == actual and len(expected) == row["full_native_font_ink"]
        # Both end-letter erasure controls must fail the entire mask.
        negative = []
        for index in (0, len(text) - 1):
            end_ink = {(x0 + index * 5 + x, y0 + y) for y in range(11) for x in range(6)
                       if font.decode(text[index]).getpixel((x, y))}
            assert end_ink and actual - end_ink != expected
            negative.append(len(end_ink))
        for y in range(top, bottom):
            for x in range(left, right):
                if left + 2 <= x < right - 2 and top + 2 <= y < bottom - 2:
                    if (x, y) not in expected:
                        sx, sy = 3 + (x - left - 2) % 40, 62 + y - top - 2
                        rgb = donor.palette[donor.indices[sy * 256 + sx]]
                        candidates = [i for i in range(256) if i != 1]
                        nearest = min(candidates, key=lambda i: sum((atlas.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
                        assert atlas.indices[y * 256 + x] == nearest
                    continue
                xx = x - left
                sx = sl + (xx if xx < 2 else 40 - (right - x) if x >= right - 2 else 2 + (xx - 2) % 36)
                assert atlas.indices[y * 256 + x] == source.indices[(st + y - top) * 256 + sx]
        l, t, r, b = row["restore_box"]
        for y in range(t, b):
            for x in range(l, r):
                points.add(y * 256 + x)
                if not (left <= x < right and top <= y < bottom):
                    assert atlas.indices[y * 256 + x] == source.indices[y * 256 + x]
        masks.append({"English": text, "Japanese": row["Japanese"], "origin": [x0, y0],
                      "complete_ink_points": len(expected), "first_final_letter_erasure_controls": negative,
                      "complete_font_and_blank_cells_exact": True})
    old = PxlImage.from_bytes(before[FILE])
    assert all(a == b for i, (a, b) in enumerate(zip(old.indices, atlas.indices, strict=True)) if i not in points)
    make_xdelta(Path("work/clean.nds"), ROM, ROM.with_suffix(".xdelta"))
    apply_xdelta(Path("work/clean.nds"), ROM.with_suffix(".xdelta"), ROOT / "patch_reconstructed.nds")
    assert (ROOT / "patch_reconstructed.nds").read_bytes() == ROM.read_bytes()
    return {"candidate": str(ROM), "candidate_sha256": sha(ROM.read_bytes()), "profile": manifest["profile"],
            "base": manifest["base_rom"], "base_sha256": manifest["base_sha256"],
            "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()), "exact_clean_patch_reconstruction": True,
            "only_changed_file_from_V610": FILE, "all_code_startup_pool_layout_and_other_translations_exact_V610": True,
            "all470_batches114_accepted_layers_retained": True, "transform": transform, "independent_complete_masks": masks,
            "script_sha256": sha(Path(__file__).read_bytes()), "experimental": True, "canonical_promoted": False,
            "all18_original_plaques_remain_incomplete": True, "full_goal_complete": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    proof = static()
    if args.static_only:
        save(ROOT / "static_proof.json", proof)
        print("V611 static: five full native masks, ten end-letter negatives, own source rims/wallpaper, full integration and exact patch pass.")
        return
    rom = NdsImage.open(ROM)
    data = rom.read_file(FILE)
    fixtures, reports, shots = {}, {}, {}
    for version, name in ((610, "control_r2"), (611, "current")):
        path = ROOT / f"V{version}_regional_background_RESEARCH_ONLY.nds"
        receipt = read(path.with_suffix(".fixture.json"))
        assert sha(path.read_bytes()) == receipt["research_ROM_sha256"]
        parent_path = PARENT if version == 610 else ROM
        assert sha(parent_path.read_bytes()) == receipt["parent_sha256"]
        parent = NdsImage.open(parent_path)
        research = NdsImage.open(path)
        a = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
        b = {p: d for _, p, d in research.iter_files()} | dict(research.iter_components())
        assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ["/__arm9__.bin"]
        offset = receipt["one_original_backdrop_branch_address"] - 0x02000000
        assert a["/__arm9__.bin"][:offset] == b["/__arm9__.bin"][:offset]
        assert a["/__arm9__.bin"][offset + 4:] == b["/__arm9__.bin"][offset + 4:]
        r, s, binding = report("regional_plaques_v611_" + name, 17200, receipt["research_ROM_sha256"])
        assert r["battery_save_preloaded"]["source_sha256"] == "f22ff2cd301c306813e9a1f5c0633d78c75d1d5a9acdf668bcd89a117d1ad087"
        assert sha(Path(r["battery_save_preloaded"]["source"]).read_bytes()) == r["battery_save_preloaded"]["source_sha256"]
        assert not any(v for k, v in r.items() if k.startswith("synthetic_"))
        fixtures[version], reports[version], shots[version] = receipt, r, s
        proof.setdefault("reports", {})[str(version)] = binding
    assert reports[610]["scripted_input_schedule"] == reports[611]["scripted_input_schedule"]
    assert reports[610]["core_options"] == reports[611]["core_options"]
    diagnostics = []
    for frame in (16900, 17000, 17200):
        old_shot, new_shot = [Image.open(shots[v][frame]["path"]).convert("RGB") for v in (610, 611)]
        assert old_shot.tobytes() == new_shot.tobytes()
        snapshots = [r for r in reports[611]["read_only_capture_RAM_snapshots"] if r["frame"] == frame]
        assert len(snapshots) == 1
        raw = Path(snapshots[0]["path"]).read_bytes()
        assert len(raw) == 0x400000 and sha(raw) == snapshots[0]["sha256"]
        candidates = []
        for offset in range(0x170000, len(raw) - 48, 4):
            words = struct.unpack_from("<12I", raw, offset)
            if words[3] == 0x02313380 and words[7:12] == (0, 0, 0, 256, 192):
                candidates.append(offset + 0x02000000)
        assert not candidates and raw.find(data) == -1
        assert struct.unpack_from("<I", raw, 0x8E140)[0] == 0xEA000029
        diagnostics.append({"frame": frame, "entire_original_current_screenshot_identical": True,
                            "pixels_compared": 98304, "whole_regional_PXL_not_resident_in_captured_RAM": True,
                            "no_live_full_regional_view_under_declared_descriptor_contract": True,
                            "branch_patch_present_in_live_RAM": True,
                            "regional_plaque_display_verification_credit": False})
    market, market_shots, binding = report("regional_plaques_v611_market", 24100, proof["candidate_sha256"])
    prior, prior_shots, prior_binding = report("village_ui_v610_market", 24100, sha(PARENT.read_bytes()))
    assert market["scripted_input_schedule"] == prior["scripted_input_schedule"] and market["core_options"] == prior["core_options"]
    assert not market.get("battery_save_preloaded") and not any(v for k, v in market.items() if k.startswith("synthetic_"))
    assert market_shots.keys() == prior_shots.keys() and len(market_shots) == 19
    assert all(market_shots[f]["PNG_sha256"] == prior_shots[f]["PNG_sha256"] for f in market_shots)
    preservation = read(ROOT / "preservation_proof.json")
    assert preservation["candidate_sha256"] == proof["candidate_sha256"]
    assert preservation["current921_format_palette_extent_checks"] and preservation["all57_embedded_block_extents_exact"]
    proof.update(rejected_background_selector_display_diagnostics=diagnostics,
                 ordinary_19_whole_screen_regression_frames_exact=True,
                 preservation_proof_sha256=sha((ROOT / "preservation_proof.json").read_bytes()),
                 ordinary_regional_fleet_formation_financial_and_policy_contexts_still_open=True,
                 actual_native_plaque_loading_crops_palette_and_readability_still_open=True,
                 source_branch_disassembly_not_assumed_actual_active_consumer=True,
                 V610_remains_latest_verified_candidate=True,
                 status="experimental_asset_repair_native_display_unverified")
    proof["reports"].update(market=binding, market_parent=prior_binding)
    save(ROOT / "pending_native_proof.json", proof)
    print("V611: five complete source-framed asset repairs; 19 ordinary frames and exact patch pass. Selector test does not display plaques; native context OPEN, latest verified V610.")


if __name__ == "__main__":
    main()
