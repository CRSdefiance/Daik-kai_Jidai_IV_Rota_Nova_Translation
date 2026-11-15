"""Archive the complete village localization and preserve rejected-build evidence."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_ui_v610 import DIGEST, ROM, ROOT, read, save

DOC = Path("docs/village_ui_v610_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V610 Village UI")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V610 Market regression")
KEY = "all24_village_names_six_menu_labels_actual_password_development_release_v610"


def copy_checked(source, destination):
    shutil.copyfile(source, destination)
    assert sha(Path(source).read_bytes()) == sha(Path(destination).read_bytes())


def main():
    proof_path, preservation = ROOT / "release_proof.json", ROOT / "preservation_proof.json"
    p = read(proof_path)
    assert p["script_sha256"] == sha(Path("scripts/verify_village_ui_v610.py").read_bytes())
    assert sha(ROM.read_bytes()) == DIGEST == p["candidate_sha256"]
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == p["patch_sha256"]
    assert len(p["complete_menu_masks"]) == 36 and len(p["all24_actual_name_getters_and_original_discovery_preparations"]) == 24
    assert read(preservation)["candidate_sha256"] == DIGEST
    save(ROOT / "transform_proof.json", p["transform"])
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    reports = {}
    for label, receipt in {**p["reports"], **{f"probe_{k}": v for k, v in p["probes"].items()}}.items():
        source = Path(receipt["path"])
        assert sha(source.read_bytes()) == receipt["sha256"]
        reports[label] = read(source)
        copy_checked(source, ARCHIVE / f"{label}_capture_report.json")
    files = [DOC, Path("docs/village_names_v610_decisions.md"), proof_path, preservation,
             ROOT / "transform_proof.json", ROOT / "keyboard_navigation.json", ROOT / "final_recorded_inputs.json",
             Path("scripts/prepare_village_ui_v609.py"), Path("scripts/register_village_ui_v609.py"),
             Path("scripts/register_village_ui_v610.py"), Path("scripts/run_village_ui_v610.py"),
             Path("scripts/inspect_village_keyboard_v610.py"), Path("scripts/verify_village_ui_v610.py"), Path(__file__),
             Path("dk4tool/patch/village_ui_text.py"), Path("dk4tool/patch/village_ui_compact.py"),
             Path("translations/village_ui_manuscript_v1.json"), Path("translations/village_ui_text_v2.json"),
             Path("work/analysis/village_ui_v609/pointer_census.json"),
             Path("work/analysis/village_ui_v609/initial_inputs.json"), ROM.with_suffix(".manifest.json")]
    for source in files:
        copy_checked(source, ARCHIVE / source.name)
    fixtures, guide = [], []
    for label, frames in (("village", (6000, 6400, 6900, 7400, 7800, 10400, 11300, 11700, 12100, 12900, 13300, 14200)),
                           ("rejected_V609_market", (24100,)), ("probe_growth_only", (5200,)), ("probe_compact", (5200,))):
        shots = {r["frame"]: r for r in reports[label]["frames_captured"]}
        for frame in frames:
            shot = shots[frame]
            assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
            target = ARCHIVE / f"{label}_{frame:06d}_TEST_EVIDENCE.png"
            copy_checked(shot["path"], target)
            fixtures.append({"path": str(target), "frame": frame, "sha256": shot["PNG_sha256"],
                "source_ROM_sha256": reports[label]["ROM_sha256"], "label": label,
                "unmodified_native_capture": True, "ordinary_travel_or_user_save_progress_claimed": False})
    market = {r["frame"]: r for r in reports["market"]["frames_captured"]}
    for frame in (21500, 23200, 24100):
        shot = market[frame]
        target = GUIDE / f"V610_{frame:06d}_Market.png"
        copy_checked(shot["path"], target)
        guide.append({"path": str(target), "frame": frame, "sha256": shot["PNG_sha256"],
                      "ordinary_New_Game_no_existing_save_savestate_or_fixture": True})
    for source in (DOC, proof_path, Path(p["reports"]["market"]["path"])):
        copy_checked(source, GUIDE / source.name)
    for folder, screenshots in ((ARCHIVE, fixtures), (GUIDE, guide)):
        save(folder / "provenance.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
            "screenshots": screenshots, "each_research_rejected_image_keeps_its_own_ROM_identity": True,
            "publication_approved": False, "hardware_device_verification": False,
            "files": {f.name: sha(f.read_bytes()) for f in folder.iterdir()
                      if f.is_file() and f.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "name_decisions": "docs/village_names_v610_decisions.md",
        "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()), "candidate": str(ROM),
        "candidate_sha256": DIGEST, "patch_sha256": p["patch_sha256"], "experimental_not_human_accepted": True,
        "all24_original_village_name_descriptors_English": True, "all6_original_menu_captions_English": True,
        "all24_native_model_getters_and_complete_original_discovery_preparations": True,
        "actual_complete_menu_masks": 36, "actual_menu_ink_points": 4164,
        "all6_whole_menu_foreground_regions_exact": True, "actual_Inuvik_initial_I_and_final_letters_verified": True,
        "ordinary_Aurora_keyboard_entry_and_original_success_development_branch_verified_under_location_fixture": True,
        "actual_developed_Inuvik_port_reached_without_second_location_fixture": True,
        "three_Lil_Leveque_name_only_corrections_same_seven_bytes_controls_and_all_other_prose_preserved": True,
        "V609_rejected_and_growth_only_failure_reproduced": True,
        "V610_all_staged_pool_startup_arena_cache_native_code_bytes_exact_V608": True,
        "deeper_growth_failure_mechanism_unresolved": True,
        "original_name_pool_RTTI_and_zero_padding_ownership_census_checked": True,
        "all470_batches114_layers921_graphics57_embedded_blocks_retained": True,
        "all19_ordinary_24100_frame_regression_screens_exact_V608": True,
        "test_archive": str(ARCHIVE), "current_village_screenshots": 12, "rejected_or_control_screenshots": 3,
        "guide_archive": str(GUIDE), "ordinary_guide_screenshots": 3,
        "all24_village_GPU_contexts_or_eight_village_cards_not_claimed": True,
        "all18_plaques_incomplete_all22_historical_objects_retained": True, "full_goal_complete": False}
    latest = {"candidate": str(ROM), "candidate_sha256": DIGEST, "proof": str(preservation),
        "proof_sha256": sha(preservation.read_bytes()), "PXL_files": 660, "FLS_textures": 261,
        "embedded_blocks": 57, "all_original_headers_all_indexed_palette_banks_and_extents_exact": True,
        "all_graphics_and_embedded_containers_exact_V608": True,
        "pixel_fidelity_translation_and_native_usage_are_separate": True}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    pointer_keys = ("candidate", "candidate_sha256", "latest_candidate", "latest_candidate_sha256",
                    "current_verified_release_candidate", "current_verified_release_candidate_sha256",
                    "source_preservation_proof", "preservation_proof_sha256", "latest_graphics_preservation")
    for name, old in scope.items():
        path = Path("translations") / name
        d = read(path)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        if "release_pointers_before_v610" not in d:
            d["release_pointers_before_v610"] = {k: d[k] for k in pointer_keys if k in d}
        d[KEY] = entry
        d["latest_graphics_preservation"] = latest
        for key in ("candidate", "latest_candidate", "current_verified_release_candidate"):
            if key in d:
                d[key] = str(ROM)
                d[key + "_sha256"] = DIGEST
        if "historical_pending_items_retained" in d:
            d.update(source_preservation_proof=str(preservation), preservation_proof_sha256=sha(preservation.read_bytes()))
        d["current_goal_turn_classification"] = "progress-complete-village-labels-real-password-and-developed-port-zero-growth-V610"
        save(path, d)
        check = read(path)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V610: all village names/menu labels and real password/developed-port path

All 24 village descriptors and six menu labels are now English, with documented
name choices and three seven-byte Lebaque -> Leveque corrections in existing Lil
records. The original controls, other prose, record/block sizes and parity remain
exact. Thirty isolated pointer owners and all source text/zero-padding spans are
checked, preserving interleaved CVillage RTTI. V609's larger-pool build is rejected:
ordinary and late-START runs fail, and a growth-only control reproduces it. V610
keeps the identical full localization in 268 owned source bytes and existing
immutable strings, preserving every staged/startup/arena/cache/native-code byte
to V608. The deeper growth failure mechanism remains unresolved. The real village
run verifies all six captions across 36 complete masks/4,164 ink pixels and six
whole text regions, full Inuvik discovery/docking text, 24 actual initialized name
getters and 24 complete original discovery preparations. Ordinary controller/
stylus input enters Aurora, the original success branch changes town90 development
0 to2, and the next visit reaches developed Inuvik without another location
fixture. It is isolated test progress, not the user's save or ordinary travel.
A separate 24,100-frame ordinary New Game/Market run matches all 19 whole screens
to V608. Complete 470-batch/114-layer integration, exact clean patch and fresh
921/57 preservation pass. Twelve village captures, three rejected/control images
and three ordinary guide candidates are on E. All 18 plaques remain incomplete;
all 22 historical objects exact; eight village cards and broader graphics gates
remain open. Goal active, human acceptance/canonical unchanged. See
[V610 village UI and boot isolation](village_ui_v610_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        path = Path("docs") / name
        text = path.read_text(encoding="utf-8-sig")
        if "## V610: all village names/menu labels and real password/developed-port path" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    glossary = Path("docs/glossary.md")
    text = glossary.read_text(encoding="utf-8-sig")
    if "## V610 village place-name decisions" not in text:
        glossary.write_text(text + "\n\n## V610 village place-name decisions\n\n"
            "Use the 24 spellings in [Village name decisions](village_names_v610_decisions.md). "
            "レバキュー is Leveque, correcting the former Lebaque spelling in three active "
            "Lil records. コルフ is Korf in the source Bering Sea context. Preserve Forel, "
            "Ezo and the game's Wanganui spelling as documented. Character-name locks "
            "remain unchanged.\n", encoding="utf-8")
    print("Recorded V610:24 names/6 labels;real password and developed port;36 masks;19 ordinary frames;15 test+3 guide images;18/22 retained.")


if __name__ == "__main__":
    main()
