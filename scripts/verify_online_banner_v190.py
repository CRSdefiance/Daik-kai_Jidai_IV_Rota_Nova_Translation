"""Verify full inheritance, exact patch and complete emulator-rendered Online pixels."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files, verify_golden_content

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
PRIOR = Path("out/all_routes_combined_v189_candidate.nds")
CANDIDATE = Path("out/all_routes_combined_v190_candidate.nds")
OUTPUT = Path("work/analysis/online_banner_v190_saved_proof.json")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(PRIOR.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    old_manifest, manifest = read(PRIOR.with_suffix(".manifest.json")), read(CANDIDATE.with_suffix(".manifest.json"))
    candidate_sha = sha(CANDIDATE.read_bytes())
    assert manifest["candidate_sha256"] == candidate_sha
    assert manifest["batches"] == old_manifest["batches"] and len(manifest["batches"]) == 465
    assert manifest["required_batches"] == old_manifest["required_batches"]
    for path, records in old_manifest["changed_records"].items():
        expected = records + ["ONLINE_TITLE_CANVAS_BOTTOM_LAYER", "ONLINE_TITLE_BORDER_BOTTOM_LAYER"] if path == "/__arm9__.bin" else records
        assert manifest["changed_records"][path] == expected
    for path, stages in old_manifest["relocations"].items():
        assert all(manifest["relocations"][path][key] == value for key, value in stages.items())
    original, previous, current = NdsImage.open(BASE), NdsImage.open(PRIOR), NdsImage.open(CANDIDATE)
    before, after = rom_files(previous), rom_files(current)
    changed = [path for path in before if before[path] != after[path]]
    assert changed == ["/__arm9__.bin"]
    diffs = [index for index, (left, right) in enumerate(zip(before[changed[0]], after[changed[0]])) if left != right]
    assert diffs == [0x1058D4, 0x105904, 0x105906, 0x105907]
    assert sha(Path("work/analysis/v189_online_banner_builder_reproduction.nds").read_bytes()) == old_manifest["candidate_sha256"]
    assert Path("work/analysis/online_banner_v190_patch_reconstruction.nds").read_bytes() == CANDIDATE.read_bytes()
    pixels = read("work/analysis/v190_online_pixel_matches.json")
    captions = read("work/analysis/v190_online_caption_pixel_matches.json")
    capture = read("work/emulation_v193/v190_all_online/capture_report.json")
    story = read("work/emulation_v193/v190_lil_scene/capture_report.json")
    assert pixels["ROM_sha256"] == capture["ROM_sha256"] == story["ROM_sha256"] == candidate_sha
    assert pixels["matched_unique_resources"] == 23 and len(pixels["pages"]) == len(captions["pages"]) == 13
    assert all(set(page["expected"]) == set(page["matched"]) for page in pixels["pages"])
    assert all(page["differing_native_5bit_caption_pixels"] == 0 for page in captions["pages"])
    for report in (capture, story):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        for frame in report["frames_captured"]:
            assert sha(Path(frame["path"]).read_bytes()) == frame["PNG_sha256"]
    verify_golden_content(original, current)
    result = {
        "status": "pass-full-stack-native-emulator-online-banner-correction",
        "candidate": str(CANDIDATE), "candidate_sha256": candidate_sha,
        "canonical_base": str(BASE), "canonical_base_sha256": sha(BASE.read_bytes()),
        "profile": manifest["profile"], "experimental": True,
        "all_465_batches_prior_records_and_terminal_stages_retained": True,
        "full_prior_v189_reproduction_exact": True,
        "changed_paths_vs_v189": changed, "changed_ARM9_offsets": diffs,
        "changed_paths_vs_canonical": manifest["changed_paths"],
        "ARM9_sha256": sha(after["/__arm9__.bin"]),
        "patch": str(CANDIDATE.with_suffix(".xdelta")), "patch_sha256": sha(CANDIDATE.with_suffix(".xdelta").read_bytes()),
        "patch_reconstruction_exact": True,
        "native_emulator": capture["core_name"] + " " + capture["core_version"],
        "core_DLL_sha256": capture["core_DLL_sha256"],
        "actual_input_flow_all_13_online_pages": True,
        "all_23_full_screenshots_match_native_5bit_pixels": True,
        "all_13_caption_cards_complete_nontransparent_pixels_match": True,
        "native_visual_review": "pending",
        "physical_hardware_user_acceptance": False,
        "goal_complete": False,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Pass: full465-batch inheritance, four code bytes, 23 screenshots/13 captions, cold boots and exact patch.")


if __name__ == "__main__":
    main()
