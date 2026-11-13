"""Archive actual normal Save/Load evidence, retaining all inherited open gates."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_save_load_plaques_v612 import ROM, ROOT, read, save

DOC = Path("docs/save_load_plaques_v612_checkpoint.md")
AUDIT = Path("E:/Rota Nova translations/Screenshots/Audit comparisons/V612 Save and Load")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V612 Save and Load")
KEY = "actual_normal_Save_Load_original_plaque_frames_release_v612"


def copy_checked(source, destination):
    source, destination = Path(source), Path(destination)
    shutil.copyfile(source, destination)
    assert sha(source.read_bytes()) == sha(destination.read_bytes())


def main():
    proof_path = ROOT / "release_proof.json"
    proof = read(proof_path)
    assert sha(ROM.read_bytes()) == proof["candidate_sha256"]
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == proof["patch_sha256"]
    assert proof["script_sha256"] == sha(Path("scripts/verify_save_load_plaques_v612.py").read_bytes())
    assert len(proof["all_complete_native_composite_pairs"]) == 32
    assert len(proof["native_original_and_current_getter_bindings"]) == 36
    assert proof["inherited_V611_regional_plaques_native_context_still_open"]
    AUDIT.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    for path in (DOC, proof_path, ROOT / "transform_proof.json", ROOT / "preservation_proof.json",
                 ROOT / "complete_inputs.json", ROOT / "initial_inputs.json", ROOT / "build.log",
                 ROOT / "source_current_repair_5x.png", ROOT / "actual_source_current_repair_5x.png",
                 ROM.with_suffix(".manifest.json"), Path("translations/save_load_plaques_v1.json"),
                 Path("dk4tool/patch/save_load_plaques.py"), Path("scripts/prepare_save_load_plaques_v612.py"),
                 Path("scripts/verify_save_load_plaques_v612.py"), Path(__file__)):
        copy_checked(path, AUDIT / path.name)
    audit_shots, guide_shots = [], []
    for key, receipt in proof["reports"].items():
        source = Path(receipt["path"])
        assert sha(source.read_bytes()) == receipt["sha256"]
        report = read(source)
        copy_checked(source, AUDIT / f"{key}_capture_report.json")
        shots = {r["frame"]: r for r in report["frames_captured"]}
        for frame in (6200, 11000, 11800, 13800, 14200):
            row = shots[frame]
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
            target = AUDIT / f"{key}_{frame:06d}_NATIVE.png"
            copy_checked(row["path"], target)
            audit_shots.append({"path": str(target), "frame": frame, "sha256": row["PNG_sha256"],
                                "source_ROM_sha256": report["ROM_sha256"], "variant": key,
                                "unmodified_ordinary_capture_from_isolated_save_copy": True})
            if key == "new":
                target = GUIDE / f"V612_{frame:06d}_Save_Load.png"
                copy_checked(row["path"], target)
                guide_shots.append({"path": str(target), "frame": frame, "sha256": row["PNG_sha256"],
                                    "source_ROM_sha256": report["ROM_sha256"],
                                    "ordinary_no_code_inventory_location_unlock_or_condition_fixture": True})
    for source in (DOC, proof_path, Path(proof["reports"]["new"]["path"])):
        copy_checked(source, GUIDE / source.name)
    for folder, screenshots in ((AUDIT, audit_shots), (GUIDE, guide_shots)):
        save(folder / "provenance.json", {"candidate": str(ROM), "candidate_sha256": proof["candidate_sha256"],
             "screenshots": screenshots, "source_save_history_not_claimed_newly_earned": True,
             "publication_approved": False, "physical_device_verification": False,
             "inherited_regional_fleet_native_context_still_open": True,
             "files": {p.name: sha(p.read_bytes()) for p in folder.iterdir() if p.is_file() and p.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "candidate": str(ROM), "candidate_sha256": proof["candidate_sha256"],
             "patch_sha256": proof["patch_sha256"], "profile": proof["profile"], "status": "experimental_with_inherited_regional_native_gap",
             "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
             "two_Save_Load_plaques_actual_normal_native_context_verified": True,
             "changed_palette_indices": 1037, "complete_static_English_ink_points": 123,
             "same_coordinate_original_frame_samples": 416, "active_Save_Load_states": 18,
             "whole_screen_control_pairs": 32, "whole_native5_composite_pixel_positions": 3145728,
             "complete_active_restoration_pixels": 26568, "actual_original_and_current_resource_getter_bindings": 36,
             "original_halfword_flag_ABI_and_retained_padding_verified": True,
             "six_actual_stylus_slot_previews_and_original_Yes_load": True,
             "all19_ordinary_New_Game_Market_frames_exact": True,
             "all470_batches114_layers_and_V611_asset_repair_retained": True,
             "only_Save_Load_atlas_changed_code_pool_other_art_and_scripts_exact_V611": True,
             "preservation_proof": str(ROOT / "preservation_proof.json"),
             "preservation_proof_sha256": sha((ROOT / "preservation_proof.json").read_bytes()),
             "all921_PXL_FLS_formats_palettes_and57_embedded_extents_exact": True,
             "inherited_regional_fleet_native_context_and_Golden_Route_material_gates_still_open": True,
             "V610_latest_verified_candidate_pointers_retained": True,
             "audit_archive": str(AUDIT), "unmodified_audit_screenshots": 15,
             "guide_archive": str(GUIDE), "unmodified_ordinary_guide_candidates": 5,
             "all18_original_plaques_incomplete_all22_historical_objects_retained": True,
             "canonical_promoted": False, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for name, old in scope.items():
        path = Path("translations") / name
        d = read(path)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        pointers = {k: v for k, v in d.items() if k in ("candidate", "candidate_sha256", "latest_candidate", "latest_candidate_sha256",
                    "current_verified_release_candidate", "current_verified_release_candidate_sha256", "latest_graphics_preservation")}
        d[KEY] = entry
        d["latest_compiled_experimental_candidate_with_inherited_native_gap"] = {
            "candidate": str(ROM), "sha256": proof["candidate_sha256"], "profile": proof["profile"],
            "Save_Load_native_verified": True, "regional_fleet_native_context_still_open": True}
        save(path, d)
        now = read(path)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert now.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    text = """

## V612: Save/Load source-frame repair and actual normal display/load verification

Both 40x16 Level/Power plaques now retain all 416 original rim samples at their
original coordinates and use contiguous source wood without repetition. All 123
native-font ink points and four end-letter negatives pass; 1,037 indices change
in saveloadinfo.pxl only. Registered V612 retains the complete V611/470-batch/
114-layer stack with all code, pool layout, other art and dialogue exact.

Paired original Japanese/V611/V612 cold boots on the unchanged isolated Syracuse
save exercise normal Save/Load, cancellation, all six actual stylus previews and
Yes loading of the first existing save, returning to Stockholm. All 18 active
states pass 26,568 complete source/final restoration pixels. All 32 sampled whole
current/control pairs pass 3,145,728 native5 positions; 36 original native getters
bind the real views to complete named PXL files. The original flag is a halfword;
source constructor/read opcodes correct the first verifier's zero-word assumption
without a ROM edit. No synthetic fixture, new travel/acquisition or hardware claim.
All 19 ordinary New Game/Market frames, 921/57 preservation, full manifest, exact
clean patch and Ruff pass. Fifteen audit captures and five ordinary guide candidates
are saved on E with provenance; publication remains unapproved.

V612 is the latest compiled combined experimental work. Its inherited regional-
fleet native context remains open, so V610's latest-verified pointers are retained.
Golden Route material/wording and other graphics gates remain open. All 18 original
plaque entries remain incomplete and all 22 historical objects retain exact scope;
goal active. See [V612 checkpoint](save_load_plaques_v612_checkpoint.md).
"""
    heading = "## V612: Save/Load source-frame repair and actual normal display/load verification"
    for name in ("docs/todo.md", "docs/translation_progress.md", "docs/known_issues.md", "docs/plaque_background_texture_defect.md", "docs/release_build.md"):
        path = Path(name)
        current = path.read_text(encoding="utf-8")
        if heading not in current:
            path.write_text(current.rstrip() + "\n" + text, encoding="utf-8")
    print("Recorded V612: two native Save/Load plaques, six previews/load,32 complete pairs,19 market frames;15 audit+5 guide images; inherited regional gap/18/22 scope retained.")


if __name__ == "__main__":
    main()
