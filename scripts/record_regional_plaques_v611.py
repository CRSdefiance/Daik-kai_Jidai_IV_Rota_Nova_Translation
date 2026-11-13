"""Save incomplete regional-plaque work without promoting its native status."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_regional_plaques_v611 import CAP, PARENT, ROM, ROOT, read, save

DOC = Path("docs/regional_plaques_v611_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V611 Regional plaque investigation")
KEY = "regional_fleet_source_material_repair_native_context_open_v611"


def copy_checked(source, destination):
    source, destination = Path(source), Path(destination)
    shutil.copyfile(source, destination)
    assert sha(source.read_bytes()) == sha(destination.read_bytes())


def main():
    proof_path = ROOT / "pending_native_proof.json"
    proof = read(proof_path)
    assert proof["script_sha256"] == sha(Path("scripts/verify_regional_plaques_v611.py").read_bytes())
    assert sha(ROM.read_bytes()) == proof["candidate_sha256"]
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == proof["patch_sha256"]
    assert len(proof["independent_complete_masks"]) == 5
    assert proof["actual_native_plaque_loading_crops_palette_and_readability_still_open"]
    assert proof["ordinary_19_whole_screen_regression_frames_exact"]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / "prototype_proof.json", ROOT / "preservation_proof.json",
             ROOT / "regional_source_current_prototype_5x.png", ROOT / "fleet_inputs.json",
             ROOT / "rejected_short_inputs.json", ROOT / "build.log",
             ROOT / "rejected_first_source_binding_build.log", ROOT / "rejected_second_memory_build.log",
             Path("translations/regional_fleet_plaques_v1.json"), ROM.with_suffix(".manifest.json"),
             Path("dk4tool/patch/regional_fleet_plaques.py"), Path("scripts/review_regional_plaques_v611.py"),
             Path("scripts/register_regional_plaques_v611.py"), Path("scripts/prepare_regional_view_v611.py"),
             Path("scripts/verify_regional_plaques_v611.py"), Path(__file__)]
    for path in files:
        copy_checked(path, ARCHIVE / path.name)
    for version in (610, 611):
        path = ROOT / f"V{version}_regional_background_RESEARCH_ONLY.fixture.json"
        copy_checked(path, ARCHIVE / path.name)
    sweep = Path("work/analysis/material_sweep_v611")
    for path in (sweep / "atlas_inventory.json", sweep / "review_findings.json"):
        copy_checked(path, ARCHIVE / path.name)
    for stem in ("chihofleetinfo", "goldsearoutediscovery", "goldsearoutelog", "saveloadinfo", "winframe00"):
        copy_checked(sweep / f"{stem}_source_current.png", ARCHIVE / f"{stem}_source_current.png")
    screenshots = []
    for name, frames, label in (("control_r2", (16900, 17000, 17200), "rejected regional selector: V610 control"),
                                ("current", (16900, 17000, 17200), "rejected regional selector: V611 repair"),
                                ("control", (12000,), "rejected short navigation before Info"),
                                ("market", (21500, 23200, 24100), "ordinary regression, no plaque display claim")):
        source = CAP / ("regional_plaques_v611_" + name) / "capture_report.json"
        r = read(source)
        copy_checked(source, ARCHIVE / f"{name}_capture_report.json")
        shots = {s["frame"]: s for s in r["frames_captured"]}
        for frame in frames:
            row = shots[frame]
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
            target = ARCHIVE / f"{name}_{frame:06d}_TEST_EVIDENCE.png"
            copy_checked(row["path"], target)
            screenshots.append({"path": str(target), "frame": frame, "sha256": row["PNG_sha256"],
                                "source_ROM_sha256": r["ROM_sha256"], "label": label,
                                "unmodified_framebuffer_capture": True, "regional_plaque_display_credit": False})
    provenance = {"candidate": str(ROM), "candidate_sha256": proof["candidate_sha256"],
                  "latest_verified_candidate_unchanged": str(PARENT), "screenshots": screenshots,
                  "guide_publication_or_earned_regional_fleet_progress": False,
                  "five_plaque_source_sheet_is_an_asset_comparison_not_a_game_capture": True,
                  "files": {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                            if p.is_file() and p.name != "provenance.json"}}
    save(ARCHIVE / "provenance.json", provenance)
    entry = {"documentation": str(DOC), "candidate": str(ROM), "candidate_sha256": proof["candidate_sha256"],
             "status": proof["status"], "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
             "five_asset_masks_complete_ink_points": 424, "source_rim_samples": 1144,
             "changed_regional_indices": 3333, "only_changed_file": "/_pxl/chihofleetinfo.pxl",
             "original_code_pool_layout_and_all_other_translations_exact_V610": True,
             "ordinary_19_regression_frames_exact": True, "exact_clean_patch_reconstruction": True,
             "all921_PXL_FLS_formats_palettes_and57_embedded_extents_retained": True,
             "native_regional_context_still_open": True, "rejected_short_and_full_selector_tests_receive_no_plaque_display_credit": True,
             "additional_Golden_Route_and_Save_Load_material_findings": str(sweep / "review_findings.json"),
             "V610_remains_latest_verified_candidate": True, "archive": str(ARCHIVE), "unmodified_test_screenshots": 10,
             "all18_original_plaques_incomplete_all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for name, old in scope.items():
        path = Path("translations") / name
        d = read(path)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        pointers = {k: v for k, v in d.items() if k in ("candidate", "candidate_sha256", "latest_candidate", "latest_candidate_sha256",
                    "current_verified_release_candidate", "current_verified_release_candidate_sha256", "latest_graphics_preservation")}
        d[KEY] = entry
        save(path, d)
        now = read(path)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert now.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    text = """

## V611: additional plaque repairs; native regional context remains open

Original/current atlas review finds retained Japanese upper strokes, row-filled
grain and incomplete rims in the regional-fleet plaques. The compiled complete
V611 asset repair changes only chihofleetinfo.pxl (3,333 indices), with five
complete native-font masks/424 ink points, ten end-letter negatives and 1,144
own-source rim samples. Wording now reads Level/Income/Expenses/Invested/Mission.
All code, memory/pool layout and other translations remain exact V610. The full
470-batch/114-layer builder, exact clean patch, fresh 921/57 preservation and 19
ordinary regression frames pass. The early source-binding guard failure and
subsequent MemoryError are retained; the complete retry succeeded.

Native display remains UNVERIFIED. A short setup stopped before Info; two full
17,200-frame original-backdrop-selector research runs reach Fleet Info but show
no regional atlas: all three whole pairs match, the PXL is not resident and no
declared live backdrop view exists. No plaque-display, regional-formation, guide
or earned-progress credit follows. V610 stays the latest verified candidate;
V611 is experimental pending its actual native context. Golden Route and Save/
Load material defects are newly recorded and remain unfixed. Ten unmodified test
captures, source comparisons and hashed evidence are on E. All 18 original plaques
remain incomplete and all 22 historical objects retain exact scope; full goal
active. See [V611 checkpoint](regional_plaques_v611_checkpoint.md).
"""
    for name in ("docs/todo.md", "docs/translation_progress.md", "docs/known_issues.md", "docs/plaque_background_texture_defect.md", "docs/release_build.md"):
        path = Path(name)
        current = path.read_text(encoding="utf-8")
        if "## V611: additional plaque repairs; native regional context remains open" not in current:
            path.write_text(current.rstrip() + "\n" + text, encoding="utf-8")
    print("Recorded V611 asset repair and failed native selector honestly; V610 latest verified, 18/22 scope exact, ten test screenshots archived.")


if __name__ == "__main__":
    main()
