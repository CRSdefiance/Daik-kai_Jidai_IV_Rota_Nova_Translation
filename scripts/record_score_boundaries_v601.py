"""Record all29 resolved label cases and retain nine foreground-image differences."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/score_boundaries_v601")
DOC = Path("docs/score_boundaries_v601_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V601 Score boundaries")
KEY = "original_score_clipping_and_native_bitmap_plane_followup_v601"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof = ROOT / "boundary_proof.json"
    p = read(proof)
    assert p["script_sha256"] == sha(Path("scripts/verify_score_boundaries_v601.py").read_bytes())
    assert p["headless_script_sha256"] == sha(Path("scripts/headless_desmume_v193.py").read_bytes())
    assert sha(Path(p["production_ROM"]).read_bytes()) == p["production_ROM_sha256"]
    assert sha(Path(p["production_ROM"]).with_suffix(".xdelta").read_bytes()) == "2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f"
    assert p["all29_visible_score_label_cases_native_exact"] and len(p["whole_bitmap_plane_word_cases"]) == 18
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    screenshots = []
    for name, binding in p["reports"].items():
        assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
        r = read(binding["path"])
        copy_checked(binding["path"], ARCHIVE / (name + "_report.json"))
        if name.startswith("score_boundaries_v601_"):
            shots = {s["frame"]: s for s in r["frames_captured"]}
            for frame in (4303, 4311, 4407, 4603):
                shot = shots[frame]
                target = ARCHIVE / f"{name}_{frame:06d}.png"
                copy_checked(shot["path"], target)
                screenshots.append({"path": str(target), "sha256": shot["PNG_sha256"], "frame": frame,
                    "unmodified_native_screenshot": True, "research_only_not_earned_result_or_guide": True})
    for source in (DOC, proof, ROOT / "frames.json", Path("scripts/verify_score_boundaries_v601.py"),
                   Path("scripts/headless_desmume_v193.py"), Path(__file__)):
        copy_checked(source, ARCHIVE / source.name)
    save(ARCHIVE / "provenance.json", {"production_ROM": p["production_ROM"],
        "production_ROM_sha256": p["production_ROM_sha256"], "research_only": True,
        "ordinary_gameplay_or_earned_result_verified": False, "publication_approved": False,
        "screenshots": screenshots, "files": {f.name: sha(f.read_bytes()) for f in ARCHIVE.iterdir()
                                               if f.is_file() and f.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
        "candidate": p["production_ROM"], "candidate_sha256": p["production_ROM_sha256"],
        "production_ROM_patch_or_graphics_changed": False,
        "all29_prior_score_label_gaps_addressed_by_original_native_parent": True,
        "three33_frame_entire_live_controller_comparisons": True,
        "all_observed_replay_images_exact_V600": True, "no_capture_frame_retiming": True,
        "independent_positions_from_only_complete_unchanged_digit_cells": True,
        "original_painter_resource_getters_and_blitter_execute_without_bridges": True,
        "whole_native5_composite_frames": p["whole_native5_frames_exact"],
        "whole_two_bitmap_plane_cases": len(p["whole_bitmap_plane_word_cases"]),
        "full16_bit_bitmap_bytes_checked": p["bitmap_plane_bytes_checked"],
        "nine_foreground_only_composed_image_differences_retained": p["nine_background_only_full_frame_disagreements"],
        "foreground_timing_or_raster_cause_proven": False, "all_final_composed_frames_exact": False,
        "research_archive": str(ARCHIVE), "full_unmodified_research_screenshots": len(screenshots),
        "guide_publication_or_human_acceptance_approved": False, "earned_result_or_normal_activation_verified": False,
        "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for name, old in scope.items():
        path = Path("translations") / name
        d = read(path)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-all29-score-label-cases-native-exact-with-nine-foreground-only-image-differences-retained"
        save(path, d)
        after = read(path)
        assert after.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert after.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V601: original score clipping and native bitmap-plane follow-up

Six fresh research cold boots reproduce all observed V600 screenshots exactly.
Both entire200-byte live score objects match across three variants at all33
primary frames. Complete unclipped unchanged digits provide unique positions;
the original parent/adapters/getter/blitter replace the incorrect generic host
crop model. All29 prior score-label cases now match native rendering.48 entire
native5 composites pass. Nine final-image cases still differ over the existing
crew figure, but all18 source/current cases pass both complete49152-pixel bitmap
planes byte for byte, including bit15 (3,538,944 bytes). OAM and non-bitmap texture/
palette banks are exact. The precise foreground timing/raster cause remains
unproved and full final-frame equality is not claimed. No frame is silently
retimed. Twelve full research screenshots/reports/provenance are on E, with no
ordinary guide or earned-result credit. Production V599, patch, assets and registry
remain unchanged. All18 plaques remain incomplete;all22 historical objects retain
exact scope;the wider graphics goal remains active. See
[V601 native clipping and planes](score_boundaries_v601_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md", "plaque_background_texture_defect.md"):
        path = Path("docs") / name
        text = path.read_text(encoding="utf-8-sig")
        if "## V601: original score clipping and native bitmap-plane follow-up" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V601:all29 label cases native-exact;9 foreground-only final-image gaps retained;12 research screenshots on E;18/22 exact;V599 unchanged.")


if __name__ == "__main__":
    main()
