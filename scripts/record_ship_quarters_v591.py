"""Archive verified ordinary Quarters screens and update retained graphics scope."""

import copy
import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/ship_quarters_v591")
DOC = Path("docs/ship_quarters_v591_checkpoint.md")
AUDIT = Path("E:/Rota Nova translations/Screenshots/Audit comparisons/V591 Quarters")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V591 Quarters")
SCRIPTS = [Path("scripts") / name for name in (
    "prepare_ship_quarters_v591.py", "verify_ship_quarters_v591.py", "record_ship_quarters_v591.py")]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof_path = ROOT / "release_proof.json"
    p = read(proof_path)
    assert p["script_sha256"] == sha(SCRIPTS[1].read_bytes())
    assert p["only_shipinfo_changes_from_V581"] and p["exact_clean_patch_reconstruction"]
    assert len(p["native_view_bindings"]) == 3 and len(p["captured_frame_cases"]) == 12
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == p["patch_sha256"]
    previous_path = Path(p["parent_preservation_proof"])
    assert sha(previous_path.read_bytes()) == p["parent_preservation_proof_sha256"]
    previous = read(previous_path)
    preservation = copy.deepcopy(previous)
    preservation.update(candidate=str(candidate), candidate_sha256=p["candidate_sha256"],
                        parent_proof=str(previous_path), parent_proof_sha256=p["parent_preservation_proof_sha256"],
                        continuity_proof=str(proof_path), continuity_proof_sha256=sha(proof_path.read_bytes()),
                        only_different_graphics_file="/_pxl/shipinfo.pxl",
                        changed_atlas_complete_header_all_palette_banks_and_extent_exact=True,
                        all_other_graphics_and_all_embedded_containers_exact_parent=True)
    preservation.pop("all_graphics_files_and_embedded_containers_exact_parent", None)
    preservation_path = ROOT / "preservation_proof.json"
    save(preservation_path, preservation)
    AUDIT.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    control, actual = [read(p[k]["path"]) for k in ("control_report", "actual_report")]
    shots = [{s["frame"]: s for s in report["frames_captured"]} for report in (control, actual)]
    guide_shots = []
    for frame, name in ((5360, "Sailing_Ship_Info_Quarters"), (5840, "Assign_Sailors_Quarters")):
        for label, frames in zip(("V581_control", "V591_verified"), shots, strict=True):
            copy_checked(frames[frame]["path"], AUDIT / f"{label}_{frame}_{name}.png")
        shot = shots[1][frame]
        target = GUIDE / f"{name}.png"
        copy_checked(shot["path"], target)
        guide_shots.append({"path": str(target), "sha256": shot["PNG_sha256"], "frame": frame,
                            "ordinary_gameplay_no_RAM_or_inventory_fixtures": True})
    for path in (DOC, proof_path, preservation_path, ROOT / "plan.json", ROOT / "source_current_proposed_4x.png",
                 ROOT / "replay_inputs.json", Path("dk4tool/patch/ship_quarters_label.py"),
                 Path("translations/ship_quarters_label_v1.json"), *SCRIPTS):
        copy_checked(path, AUDIT / path.name)
    for key in ("control_report", "actual_report"):
        copy_checked(p[key]["path"], AUDIT / f"{key}.json")
    provenance = {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
                  "source_save_sha256": actual["battery_save_preloaded"]["source_sha256"],
                  "source_save_history_not_claimed": True, "cold_boot": True, "savestate_loaded": False,
                  "ordinary_input_schedule": str(ROOT / "replay_inputs.json"),
                  "ordinary_input_schedule_sha256": sha((ROOT / "replay_inputs.json").read_bytes()),
                  "capture_report": p["actual_report"], "guide_candidates": guide_shots,
                  "publication_approved": False, "full_route_or_hardware_verified": False}
    save(GUIDE / "provenance.json", provenance)
    save(AUDIT / "provenance.json", provenance | {
        "files": {path.name: sha(path.read_bytes()) for path in AUDIT.iterdir()
                  if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
             "profile": p["profile"], "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
             "preservation_proof": str(preservation_path), "preservation_proof_sha256": sha(preservation_path.read_bytes()),
             "patch_sha256": p["patch_sha256"], "exact_clean_patch_reconstruction": True,
             "only_different_file_from_V581": "/_pxl/shipinfo.pxl", "glyph_only_changed_pixels": 144,
             "Japanese": "海兵詰所", "old_English": "Marines", "English": "Quarters",
             "source_review_and_same_ship_room_count_not_number_of_marines": True,
             "matched_ordinary_frames": 12, "whole_screen_pixels_checked": 12 * 98304,
             "complete_native_Quarters_faces": 3, "complete_native_word_ink": 100,
             "actual_original_resource_resolver_and_whole_resident_file_verified": True,
             "source_save_unchanged_no_synthetic_fixtures": True,
             "all470_batches114_layers921_preservation_entries57_embedded_blocks_retained": True,
             "ordinary_miniature_Confirm_Admiral_and_other_remaining_contexts_still_open": True,
             "guide_screenshots": guide_shots, "audit_archive": str(AUDIT), "guide_publication_approved": False,
             "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True,
             "experimental_not_human_accepted": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    latest = {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
              "proof": str(preservation_path), "proof_sha256": sha(preservation_path.read_bytes()),
              "PXL_files": 660, "FLS_textures": 261, "embedded_blocks": 57,
              "all_original_headers_all_indexed_palette_banks_and_extents_exact": True,
              "pixel_fidelity_translation_and_native_usage_are_separate": True}
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        if "release_pointers_before_v591" not in d:
            d["release_pointers_before_v591"] = {key: d[key] for key in (
                "candidate", "candidate_sha256", "source_preservation_proof", "preservation_proof_sha256", "latest_graphics_preservation") if key in d}
        d["ordinary_sailing_Quarters_terminology_release_v591"] = entry
        d["latest_graphics_preservation"] = latest
        if "historical_pending_items_retained" in d:
            d.update(candidate=str(candidate), candidate_sha256=p["candidate_sha256"],
                     source_preservation_proof=str(preservation_path), preservation_proof_sha256=sha(preservation_path.read_bytes()))
        d["current_goal_turn_classification"] = "progress-observed-and-corrected-marine-quarters-graphic-with-registered-combined-ROM-and-matched-ordinary-native-tests"
        save(target, d)
        verified = read(target)
        assert verified.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert verified.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V590-V591: ordinary inspection and consistent Quarters plaque

The same Vestaros brigantine displayed Marines1 in Ship Info and Quarters1 in
Assign Sailors. Original 海兵詰所 denotes marine quarters, not the number of
marines. Registered V591 changes that one Ship Info label to Quarters:144 glyph
indices, with all other texture/frame/palette/geometry and ROM files exact to
V581. All470 batches/114 layers and921/57 preservation scope carry forward.
Twelve complete paired ordinary cold-boot frames check1,179,648 pixels; three
full1,008-pixel faces and complete100-point words pass, with original cache/view
bindings and first/final erasure controls. The clean patch reconstructs V591
exactly. Two unmodified final guide candidates and control comparisons are on E,
with publication unapproved. Donor save remains exact; no synthetic fixtures.
Admiral wording, miniature/Confirm parents and other graphics gates stay open.
All18 plaques remain incomplete and all22 historical objects remain exact.
The graphics goal remains active. See [V591 checkpoint](ship_quarters_v591_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md", "plaque_background_texture_defect.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V590-V591: ordinary inspection and consistent Quarters plaque" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V591 current candidate/preservation in3 audits/5 docs;two ordinary guide candidates on E;18/22 exact;goal remains active.")


if __name__ == "__main__":
    main()
