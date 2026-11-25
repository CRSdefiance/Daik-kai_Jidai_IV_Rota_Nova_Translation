"""Archive source-bound ending photo usage evidence without closing full scope."""

import json
import shutil
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/ending_photo_markers_v594")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V594 Ending photos")
DOC = Path("docs/ending_photo_markers_v594_checkpoint.md")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof_path = ROOT / "native_photo_usage_proof.json"
    p = read(proof_path)
    scripts = [Path("scripts") / name for name in (
        "prepare_ending_photo_markers_v594.py", "verify_ending_photo_markers_v594.py",
        "record_ending_photo_markers_v594.py", "native_ending_fixture_v537.py")]
    assert p["script_sha256"] == sha(scripts[1].read_bytes())
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == "e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7"
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    screenshots = []
    for case in p["cases"]:
        reports = {name: read(binding["path"]) for name, binding in case["reports"].items()}
        shots = {name: {s["frame"]: s for s in r["frames_captured"]} for name, r in reports.items()}
        positives = [r["frame"] for r in case["native_snapshot_projection_cases"] if r["changed_native_pixels"]]
        negatives = [r["frame"] for r in case["all_paired_frame_cases"] if r["full_two_screen_exact"]]
        selected = sorted(set(positives + [max(f for f in negatives if f < positives[0]), min(f for f in negatives if f > positives[-1])]))
        for frame in selected:
            for mode in ("control", "markers"):
                shot = shots[mode][frame]
                target = ARCHIVE / f"{case['label']}_{frame:06d}_{mode}_TEST.png"
                copy_checked(shot["path"], target)
                screenshots.append({"path": str(target), "sha256": shot["PNG_sha256"],
                                    "frame": frame, "mode": mode, "label": case["label"],
                                    "synthetic_ending_setup_not_earned_or_guide": True})
        for mode, binding in case["reports"].items():
            copy_checked(binding["path"], ARCHIVE / f"{case['label']}_{mode}_capture_report.json")
    rom = NdsImage.open(candidate)
    manifest = read(ROOT / "fixture_manifest.json")
    for config in manifest["cases"]:
        texture = FlsArchive(rom.read_file(config["only_internal_file_changed"])).texture(config["texture"])
        width, height = config["native_dimensions"]
        source_path = Path("work/analysis/endings_current_v583") / ("M30_texture5_native_view.png" if config["label"] == "hodram" else "M32_texture4_native_view.png")
        assert Image.open(source_path).convert("RGB").tobytes() == texture.render().crop((0, 0, width, height)).convert("RGB").tobytes()
        copy_checked(source_path, ARCHIVE / source_path.name)
        copy_checked(config["inputs"], ARCHIVE / Path(config["inputs"]).name)
        copy_checked(Path(config["research_ROM"]).with_suffix(".fixture.json"), ARCHIVE / f"{config['label']}_fixture.json")
    for path in (proof_path, ROOT / "fixture_manifest.json", DOC, *scripts):
        copy_checked(path, ARCHIVE / path.name)
    save(ARCHIVE / "provenance.json", {
        "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
        "test_setup_and_marker_controls_not_normal_guide_scenes": True,
        "publication_approved": False, "screenshots": screenshots,
        "files": {path.name: sha(path.read_bytes()) for path in ARCHIVE.iterdir()
                  if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
             "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
             "actual_original_ending_photo_consumers": ["M30 texture5", "M32 texture4"],
             "source_art_exact_clean_and_no_readable_Japanese_caption_original_retained": True,
             "paired_frame_cases": 331, "full_two_screen_exact_pairs": 291,
             "marker_effect_frame_pairs": 40, "all_lower_screens_exact": True,
             "actual_live_prefix_and_controller_full_bytes_verified": True,
             "original_selector_and_quad_calls_from_real_captured_state": True,
             "independent_projected_marker_bounds_states": 11,
             "changed_native_RGB_pixels_inside_expected_bounds": 13158,
             "source_crop_raster_edge_margin_pixels": 2,
             "observed_source_tags": {c["label"]: c["visible_source_tags"] for c in p["cases"]},
             "bounded_native_source_usage_zoom_and_cropping_verified": True,
             "full_alpha_compositor_all_source_rows_all_frames_or_earned_endings_not_claimed": True,
             "four_authorized_ending_state_fixtures_two_marked_research_ROMs": True,
             "archive": str(ARCHIVE), "source_control_marker_screenshot_files": len(screenshots),
             "guide_or_publication_approved": False, "production_ROM_or_patch_changed": False,
             "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True,
             "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d["actual_original_ending_photo_usage_and_crops_v594"] = entry
        d["current_goal_turn_classification"] = "progress-paired-native-original-ending-photo-usage-with-live-controller-selector-and-projected-source-tag-bounds"
        save(target, d)
        verified = read(target)
        assert verified.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert verified.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V594: actual original ending-photo source and crop checks

Paired V593/original-photo marker tests positively bind M30 texture5 and M32
texture4 to their actual original ending displays. Four authorized one-byte
ending fixtures complete:331 paired frame cases,291 entire pairs identical,
40 marker-effect pairs and every lower screen exact. Eleven real captured
controller states remain byte-identical between pairs; original selector/quad
calls independently project all13,158 changed RGB pixels into declared source-tag
bounds with an explicit2-pixel raster margin. This proves bounded native usage,
zoom and crops, not a full alpha compositor/all rows/all frames or earned endings.
Both source illustrations are reviewed again: no readable Japanese caption;
original art retained. Thirty full test PNGs plus two source views/provenance
are on E under Test fixtures/V594 Ending photos, with no guide approval. V593
ROM/patch/artwork remain unchanged. All18 plaque entries remain incomplete and
all22 historical objects remain exact. Other graphics gates and the full goal
remain open. See [V594 photo checkpoint](ending_photo_markers_v594_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V594: actual original ending-photo source and crop checks" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print(f"Recorded V594 in3 audits/4 docs;{len(screenshots)} full test screenshots and2 source views on E;18/22 exact;V593 unchanged.")


if __name__ == "__main__":
    main()
