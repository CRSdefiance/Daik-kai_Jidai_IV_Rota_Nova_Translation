"""Archive the bounded Lil source-row evidence, preserving all outstanding scope."""

import json
import shutil
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/ending_pan_rows_v596")
DOC = Path("docs/ending_pan_rows_v596_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V596 Lil ending pan rows")
KEY = "actual_Lil_pan_hidden_rows_and_fixed_phase_control_v596"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof = ROOT / "pan_rows_proof.json"
    p = read(proof)
    scripts = [Path("scripts") / name for name in (
        "prepare_ending_pan_rows_v596.py", "verify_ending_pan_rows_v596.py", "record_ending_pan_rows_v596.py")]
    assert p["script_sha256"] == sha(scripts[1].read_bytes())
    assert p["fixed_one_update_alignment_interval"] == [18028, 21000]
    assert len(p["whole_two_screen_control_pairs"]) == 3007
    assert p["one_update_aligned_pair_count"] == 2973
    assert p["same_frame_exact_pair_count"] == 2814 and p["same_frame_different_pair_count"] == 193
    rom = NdsImage.open(p["candidate"])
    assert sha(rom.source.read_bytes()) == p["candidate_sha256"]
    assert sha(rom.source.with_suffix(".xdelta").read_bytes()) == "e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7"
    source_view = ROOT / "M31_texture1_original_full.png"
    assert Image.open(source_view).convert("RGBA").tobytes() == FlsArchive(rom.read_file("/FLS/M31.fls")).texture(1).render().convert("RGBA").tobytes()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    screenshots = []
    for mode, report in zip(("production", "lower_rows_control"), p["reports"], strict=True):
        r = read(report["path"])
        assert sha(Path(report["path"]).read_bytes()) == report["sha256"]
        shots = {s["frame"]: s for s in r["frames_captured"]}
        for frame in (18096, 18400, 19400, 20400, 20540, 26600):
            shot = shots[frame]
            dest = ARCHIVE / f"{mode}_{frame:06d}_TEST.png"
            copy_checked(shot["path"], dest)
            screenshots.append({"path": str(dest), "sha256": shot["PNG_sha256"], "mode": mode,
                                "frame": frame, "synthetic_ending_not_earned_or_guide": True})
        copy_checked(report["path"], ARCHIVE / f"{mode}_capture_report.json")
    manifest = ROOT / "lil_lower_rows_RESEARCH_ONLY.fixture.json"
    inputs = Path(p["research_fixture"]["inputs"])
    for path in (proof, DOC, source_view, manifest, inputs, *scripts):
        copy_checked(path, ARCHIVE / path.name)
    save(ARCHIVE / "provenance.json", {"candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
        "production_ROM_and_patch_changed": False, "test_fixtures_not_normal_guide_or_earned_ending": True,
        "publication_approved": False, "screenshots": screenshots,
        "files": {path.name: sha(path.read_bytes()) for path in ARCHIVE.iterdir()
                  if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
             "candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
             "specific_M31_texture1_lower64_pan_rows_verified_outside_view": True,
             "no_readable_Japanese_source_caption_original_art_retained": True,
             "original_native_update_calls": 2452, "complete_live_controller_anchors": 19,
             "source_pan_order_bound_by_original_selector_and_geometry": [3, 2, 1],
             "whole49152_pixel_source_composites": 2344, "complete_two_screen_frame_pairs": 3007,
             "same_frame_exact_pairs": 2814, "same_frame_different_pairs": 193,
             "fixed_minus_one_control_alignment_interval": [18028, 21000], "fixed_aligned_pairs": 2973,
             "complete32768_byte_original_and_marked_decoded_tiles_verified_at_three_anchors": True,
             "changed_source_indices": 16358, "changed_row64_indices": 256,
             "phase_offset_proved_with_original_one_update_cause_not_established": True,
             "other_movies_effects_full_alpha_compositor_and_earned_completion_not_claimed": True,
             "archive": str(ARCHIVE), "unmodified_full_test_screenshots": len(screenshots),
             "production_ROM_or_patch_changed": False, "all18_plaques_remain_incomplete": True,
             "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-actual-Lil-pan-row-coverage-with-original-controller-replay-and-fixed-phase-native-control"
        save(target, d)
        v = read(target)
        assert v.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert v.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V596: Lil ending pan source-row coverage

Two fresh26,600-frame current/control ending fixtures address M31 texture1's
previously unobserved lower64 rows. Original native selectors/quads bind order3,2,1;
2,344 entire source-window composites pass. A2,452-update original replay matches
19 whole live controllers and reaches inactive pan geometry. All16,358 lower-row
marker changes, including row64, reach complete decoded memory at three anchors.
The first same-frame test fails at193 frames: the control is one original update
ahead. A fixed minus-one comparison throughout18028-21000, not adaptive matching,
passes all3,007 full pairs;2,814 also match at identical frame numbers. The phase
cause remains unproved. The specific lower64-row pan gap is now supported as
outside view; original caption-free art is retained. Other consumer/material/movie
gates stay open. V593 ROM/patch unchanged;all18 plaques incomplete/all22 objects
exact. Twelve full test screenshots, source view and provenance are on E under
Test fixtures/V596 Lil ending pan rows, with no guide or earned-ending credit.
See [V596 row checkpoint](ending_pan_rows_v596_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V596: Lil ending pan source-row coverage" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V596: specific Lil pan row gap addressed;12 full test screenshots+source view;3 audits/4 docs;18/22 exact;V593 unchanged.")


if __name__ == "__main__":
    main()
