"""Record actual Hodram tile-order and star-tag evidence without closing scope."""

import json
import shutil
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/hodram_pan_tags_v597")
DOC = Path("docs/hodram_pan_tags_v597_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V597 Hodram pan tiles")
KEY = "actual_Hodram_pan_order_and_star_tile_transition_v597"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof = ROOT / "pan_tags_proof.json"
    p = read(proof)
    scripts = [Path("scripts") / name for name in (
        "prepare_hodram_pan_tags_v597.py", "verify_hodram_pan_tags_v597.py", "record_hodram_pan_tags_v597.py",
        "native_ending_fixture_v537.py", "probe_button_prompt_native.py", "research_fls_frames_v312.py",
        "verify_ending_photo_markers_v594.py", "verify_ending_pan_rows_v596.py")]
    assert p["script_sha256"] == sha(scripts[1].read_bytes())
    assert p["fixed_native_update_offset"] == 0 and p["observed_source_tags"] == list(range(8))
    assert p["changed_native_pixels_in_projected_states"] == 11981
    assert len(p["native_projection_cases"]) == 15 and len(p["whole_source_pan_composites"]) == 836
    assert len(p["all_paired_frame_cases"]) == 1467
    assert sum(x["same_frame_full_exact"] for x in p["all_paired_frame_cases"]) == 1022
    rom = NdsImage.open(p["candidate"])
    assert sha(rom.source.read_bytes()) == p["candidate_sha256"]
    assert sha(rom.source.with_suffix(".xdelta").read_bytes()) == "e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7"
    source_view = ROOT / "M30_texture3_original_full.png"
    assert Image.open(source_view).convert("RGBA").tobytes() == FlsArchive(rom.read_file("/FLS/M30.fls")).texture(3).render().convert("RGBA").tobytes()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    screenshots = []
    positives = [x["frame"] for x in p["native_projection_cases"] if x["changed_native_pixels"]]
    assert len(positives) == 8
    for mode, binding in zip(("production", "tile3_tags"), p["reports"], strict=True):
        assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
        r = read(binding["path"])
        shots = {x["frame"]: x for x in r["frames_captured"]}
        for frame in (12400, *positives, 13440):
            shot = shots[frame]
            dest = ARCHIVE / f"{mode}_{frame:06d}_TEST.png"
            copy_checked(shot["path"], dest)
            screenshots.append({"path": str(dest), "sha256": shot["PNG_sha256"], "frame": frame, "mode": mode,
                                "synthetic_ending_with_retained_underlying_dialogue_not_normal_guide": True})
        copy_checked(binding["path"], ARCHIVE / f"{mode}_capture_report.json")
    for path in (proof, DOC, source_view, ROOT / "hodram_pan_tile3_tags_RESEARCH_ONLY.fixture.json",
                 Path(p["fixture"]["inputs"]), *scripts):
        copy_checked(path, ARCHIVE / path.name)
    save(ARCHIVE / "provenance.json", {"candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
        "production_ROM_or_patch_changed": False, "test_ending_not_earned_or_normal_guide": True,
        "publication_approved": False, "screenshots": screenshots,
        "files": {path.name: sha(path.read_bytes()) for path in ARCHIVE.iterdir()
                  if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
             "candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
             "source_bound_top_to_bottom_pan_order": [3, 2, 1], "whole_source_upper_composites": 836,
             "actual_native_controller_and_geometry_cases": 15, "eight_positive_tag_states": True,
             "observed_source_tags": list(range(8)), "changed_native_pixels_inside_projection": 11981,
             "explicit_raster_margin_pixels": 2, "all_other_full_frame_pixels_exact_in_projected_cases": True,
             "whole_frame_pairs": 1467, "whole_frame_identical_pairs": 1022, "every_lower_screen_exact": True,
             "same_frame_controllers_exact_no_phase_alignment_needed": True,
             "complete_linear_CPU_tile_not_found_not_assumed_required": True,
             "original_caption_free_star_art_retained": True,
             "other_rows_alpha_compositor_and_earned_completion_not_claimed": True,
             "archive": str(ARCHIVE), "full_unmodified_test_screenshots": len(screenshots),
             "helper_and_script_hashes": {str(path): sha(path.read_bytes()) for path in scripts},
             "production_ROM_or_patch_changed": False, "all18_plaques_remain_incomplete": True,
             "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-actual-Hodram-pan-order-and-positive-star-tile-transition-source-tags"
        save(target, d)
        v = read(target)
        assert v.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert v.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V597: original Hodram pan order and actual star-tile transition

Two current/control14,600-frame ending fixtures resolve the earlier screenshot
permutation ambiguity: original selectors/quads bind top-to-bottom3,2,1, with
the original fractional offsets retained. All836 complete opaque source windows
pass. Fifteen real controller pairs are byte-identical at the same frame; eight
positive states show all eight source tags and11,981 native pixel differences
inside independently projected bounds, with every other full-frame pixel exact.
All1,467 lower screens and1,022 whole frame pairs match. Tile3 enters during the
movement/zoom, rather than being globally unused. Original caption-free stars
are retained. A whole linear CPU copy was not found; that failed initial
assumption is recorded without inventing buffer-lifetime/VRAM evidence. Twenty
full test screenshots plus source extraction/provenance are on E under Test
fixtures/V597 Hodram pan tiles. Underlying Charles dialogue persists in the
synthetic setup; no normal guide or earned-ending credit. V593 ROM/patch unchanged;
all18 plaques incomplete/all22 objects exact;other graphics gates stay open.
See [V597 source-order checkpoint](hodram_pan_tags_v597_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V597: original Hodram pan order and actual star-tile transition" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V597: original order3,2,1;15 native states/8 positive tags;20 full test screenshots;3 audits/4 docs;18/22 exact;V593 unchanged.")


if __name__ == "__main__":
    main()
