"""Record the complete native battery/quarters terminology repair and scope."""

import copy
import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/ship_batteries_v593")
DOC = Path("docs/ship_batteries_v593_checkpoint.md")
BASE = Path("E:/Rota Nova translations/Screenshots")
AUDIT = BASE / "Audit comparisons/V593 Ship room terms"
GUIDE = BASE / "Guide candidates/V593 Ship room terms"
RESEARCH = BASE / "Test fixtures/V593 Empty room labels"


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
    assert p["script_sha256"] == sha(Path("scripts/verify_ship_batteries_v593.py").read_bytes())
    assert len(p["deck_native_frame_cases"]) == 18 and len(p["ship_native_frame_cases"]) == 12
    assert p["image_changed_pixels"] == 139 and p["ARM9_changed_byte_count"] == 15
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == p["patch_sha256"]
    parent_path = Path(p["parent_preservation_proof"])
    assert sha(parent_path.read_bytes()) == p["parent_preservation_proof_sha256"]
    preservation = copy.deepcopy(read(parent_path))
    preservation.update(candidate=str(candidate), candidate_sha256=p["candidate_sha256"],
                        parent_proof=str(parent_path), parent_proof_sha256=p["parent_preservation_proof_sha256"],
                        continuity_proof=str(proof_path), continuity_proof_sha256=sha(proof_path.read_bytes()),
                        only_different_graphics_file="/_pxl/shipinfo.pxl",
                        changed_atlas_complete_header_all_palette_banks_and_extent_exact=True,
                        all_other_graphics_and_all_embedded_containers_exact_parent=True,
                        ARM9_only_two12_byte_room_text_slots_change_fonts_and_code_exact=True)
    preservation_path = ROOT / "preservation_proof.json"
    save(preservation_path, preservation)
    for folder in (AUDIT, GUIDE, RESEARCH):
        folder.mkdir(parents=True, exist_ok=True)
    reports = {name: read(binding["path"]) for name, binding in p["reports"].items()}
    shots = {name: {s["frame"]: s for s in r["frames_captured"]} for name, r in reports.items()}
    guide = []
    for frame, name, kind in ((6760, "Deck_Battery", "deck"), (6920, "Deck_Quarters", "deck"),
                              (5360, "Ship_Info_Batteries_and_Quarters", "ship")):
        for label in ("control", "actual"):
            shot = shots[kind + "_" + label][frame]
            copy_checked(shot["path"], AUDIT / f"{name}_{label}.png")
        shot = shots[kind + "_actual"][frame]
        destination = GUIDE / f"{name}.png"
        copy_checked(shot["path"], destination)
        guide.append({"path": str(destination), "sha256": shot["PNG_sha256"], "frame": frame,
                      "source_report": p["reports"][kind + "_actual"],
                      "ordinary_controls_no_inventory_location_condition_or_RAM_fixture": True})
        if kind == "deck":
            copy_checked(shots["deck_blank"][frame]["path"], RESEARCH / f"{name}_empty_heading_control.png")
    files = [DOC, proof_path, preservation_path, ROOT / "plan.json", ROOT / "deck_replay_inputs.json",
             ROOT / "source_current_proposed_4x.png", Path("translations/ship_battery_labels_v1.json"),
             Path("dk4tool/patch/ship_battery_labels.py"), Path("dk4tool/patch/ship_quarters_label.py")]
    files += [Path("scripts") / name for name in (
        "prepare_ship_batteries_v593.py", "verify_ship_batteries_v593.py", "record_ship_batteries_v593.py")]
    for path in files:
        copy_checked(path, AUDIT / path.name)
    for name, binding in p["reports"].items():
        copy_checked(binding["path"], AUDIT / f"{name}_report.json")
    copy_checked(ROOT / "deck_empty_labels_RESEARCH_ONLY.fixture.json", RESEARCH / "fixture.json")
    copy_checked(p["reports"]["deck_blank"]["path"], RESEARCH / "capture_report.json")
    guide_provenance = {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
                        "source_save_sha256": reports["deck_actual"]["battery_save_preloaded"]["source_sha256"],
                        "cold_boot": True, "savestate_loaded": False, "source_save_history_not_claimed": True,
                        "guide_candidates": guide, "publication_approved": False,
                        "full_route_or_hardware_verified": False, "reports": p["reports"]}
    save(GUIDE / "provenance.json", guide_provenance)
    for folder in (AUDIT, RESEARCH):
        save(folder / "provenance.json", guide_provenance | {
            "research_or_comparison_not_guide_approval": True,
            "files": {path.name: sha(path.read_bytes()) for path in folder.iterdir()
                      if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
             "profile": p["profile"], "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
             "preservation_proof": str(preservation_path), "preservation_proof_sha256": sha(preservation_path.read_bytes()),
             "patch_sha256": p["patch_sha256"], "exact_clean_patch_reconstruction": True,
             "changed_files_from_V591": ["/__arm9__.bin", "/_pxl/shipinfo.pxl"],
             "plaque_indices_changed": 139, "ARM9_text_bytes_changed": 15,
             "English_terms": {"individual_gun_room": "Battery", "ship_position_count": "Batteries", "marine_room": "Quarters"},
             "source_Help_and_native_Deck_context_reviewed": True,
             "Deck_whole_original_blank_final_cases": 18, "complete_native_heading_appearances": 8,
             "Deck_RGB_pixel_positions_checked": 3538944, "ship_frame_pairs": 12,
             "ship_native5_pixel_positions_checked": 1179648, "complete_Batteries_faces": 3,
             "complete_original_resource_resolver_and_resident_file_verified": True,
             "first_final_letter_erasure_controls_rejected": 4,
             "all470_batches114_layers921_entries57_embedded_blocks_retained": True,
             "source_save_unchanged_final_runs_no_synthetic_RAM_fixtures": True,
             "specific_marine_quarters_and_gun_position_terminology_lead_resolved": True,
             "global_material_and_other_unobserved_graphics_contexts_remain_open": True,
             "guide_screenshots": guide, "audit_archive": str(AUDIT), "research_archive": str(RESEARCH),
             "human_acceptance_or_guide_publication_approved": False,
             "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True,
             "full_goal_complete": False}
    latest = {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
              "proof": str(preservation_path), "proof_sha256": sha(preservation_path.read_bytes()),
              "PXL_files": 660, "FLS_textures": 261, "embedded_blocks": 57,
              "all_original_headers_all_indexed_palette_banks_and_extents_exact": True,
              "pixel_fidelity_translation_and_native_usage_are_separate": True}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        if "release_pointers_before_v593" not in d:
            d["release_pointers_before_v593"] = {k: d[k] for k in (
                "candidate", "candidate_sha256", "source_preservation_proof", "preservation_proof_sha256", "latest_graphics_preservation") if k in d}
        d["source_reviewed_Battery_and_Quarters_labels_v593"] = entry
        d["latest_graphics_preservation"] = latest
        if "historical_pending_items_retained" in d:
            d.update(candidate=str(candidate), candidate_sha256=p["candidate_sha256"],
                     source_preservation_proof=str(preservation_path), preservation_proof_sha256=sha(preservation_path.read_bytes()))
        d["current_goal_turn_classification"] = "progress-source-reviewed-ship-room-terminology-with-three-way-native-background-tests-and-registered-combined-ROM"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V592-V593: source-reviewed Battery/Batteries and Quarters labels

Original Help129 and actual Deck selections establish gun positions that accept
a Gunner, separate from individual cannon counts. Ship Info now says Batteries;
the individual Deck room says Battery, and its marine room now says Quarters.
Only139 plaque indices and15 bytes in two existing12-byte ARM9 text slots change
from V591. Original frames/grain/palettes/geometry and all code/fonts remain exact.
Eighteen complete source/empty-control/final Deck cases check3,538,944 RGB pixels
and eight complete labels; four missing-end-letter controls fail as expected.
Twelve ordinary ship frame pairs check1,179,648 native5 pixels, three complete
1,024-pixel Batteries faces and exact resident-file bindings. Full inherited
470/114 stack and921/57 preservation carry forward; the clean patch reconstructs
registered V593 exactly. Three final ordinary guide candidates are on E with
publication unapproved; empty-heading research controls stay in Test fixtures.
This closes the specific V556 gun/marine-room terminology lead, not the broader
graphics audit. All18 plaques remain incomplete and all22 historical objects
remain exact. See [V593 checkpoint](ship_batteries_v593_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md", "plaque_background_texture_defect.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V592-V593: source-reviewed Battery/Batteries and Quarters labels" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V593 in3 audits/5 docs;three ordinary guide candidates and separate research controls on E;18/22 exact;goal active.")


if __name__ == "__main__":
    main()
