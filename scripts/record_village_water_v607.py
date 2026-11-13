"""Archive real village fixture evidence and retain all original graphics scope."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_water_v607 import CAP, DIGEST, ROM, ROOT, read, save

DOC = Path("docs/village_water_v607_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V607 Village discovery")
KEY = "source_water_fixture_actual_village_UI_and_observed_formatting_gap_v607"


def main():
    proof_path = ROOT / "native_village_proof.json"
    proof = read(proof_path)
    assert proof["script_sha256"] == sha(Path("scripts/verify_village_water_v607.py").read_bytes())
    assert sha(ROM.read_bytes()) == DIGEST == proof["candidate_sha256"]
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == "5fa980cd6995606989375b69e6be7083cfcb6fbe90c122e96e2a30d7bc20cc7a"
    assert sha(Path(proof["report"]).read_bytes()) == proof["report_sha256"]
    assert proof["password_success_not_verified"] and not proof["full_goal_complete"]
    for source, digest in proof["implementation_hashes"].items():
        assert sha(Path(source).read_bytes()) == digest
    report = read(proof["report"])
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    sources = [DOC, proof_path, Path(proof["report"]), ROOT / "start_inputs.json",
               ROOT / "final_recorded_inputs.json", Path(__file__),
               Path("scripts/verify_village_water_v607.py"),
               Path("scripts/native_village_water_v607.py"), Path("scripts/run_village_water_v607.py"),
               Path("scripts/native_village_location_v606.py"), Path("scripts/run_village_location_v606.py")]
    selected = []
    for frame in (5200, 5600, 6000, 6400, 6900, 7800, 8200, 8600, 9000, 9200, 16900, 17800):
        source = CAP / "village_water_v607_inuvik" / f"frame_{frame:06d}_navigation.png"
        receipt = next(r for r in report["frames_captured"] if r["path"] == str(source))
        assert sha(source.read_bytes()) == receipt["PNG_sha256"]
        sources.append(source)
        selected.append({"frame": frame, "filename": source.name,
                         "sha256": receipt["PNG_sha256"], "unmodified_native_capture": True})
    for source in sources:
        destination = ARCHIVE / source.name
        shutil.copyfile(source, destination)
        assert sha(source.read_bytes()) == sha(destination.read_bytes())
    save(ARCHIVE / "provenance.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
        "synthetic_location_fixture": True, "normal_travel_or_earned_unlock_claimed": False,
        "successful_password_claimed": False, "native_wrap_and_Japanese_UI_defects_retained": True,
        "guide_credit": False, "publication_approved": False, "hardware_device_verification": False,
        "screenshots": selected,
        "files": {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof_path),
        "proof_sha256": sha(proof_path.read_bytes()), "candidate_sha256": DIGEST,
        "original_terrain_center_blocked_nearby_water_verified": True,
        "native_discovery_menu_editor_and_failure_after_only_ship_coordinate_fixture": True,
        "normal_village_travel_not_claimed": True, "password_success_not_verified": True,
        "newly_observed_English_wrap_defect_unfixed": True,
        "Japanese_village_menu_and_name_unfixed": True,
        "all8_ordinary_village_card_contexts_still_open": True,
        "global_card_nonuse_not_claimed": True, "two_v606_setups_rejected_not_display_credit": True,
        "archive": str(ARCHIVE), "unmodified_test_screenshots": len(selected),
        "production_ROM_patch_registry_art_or_donor_changed": False,
        "all18_plaques_incomplete_all22_historical_objects_exact": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for name, old in scope.items():
        path = Path("translations") / name
        d = read(path)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-native-village-discovery-and-actual-UI-expose-wrap-and-translation-gaps"
        save(path, d)
        check = read(path)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V607: actual village discovery exposes formatting and UI translation gaps

The original terrain predicate rejects the village center but accepts nearby water
22 map units away. The corrected authorized fixture owns only eight ship-coordinate
bytes; six differ. In a finalized 17,800-frame cold boot from an unchanged isolated
Syracuse donor, original game logic synchronizes the fleet cache, changes discovery
mask 0 to 1 and reaches the village discovery, docking, menu, Promised Words editor
and rejected-answer response. No scene/resource/discovery flags are supplied.
The actual request splits `hear` into `h` and `ear` on separate lines before the
compiled break; all three native line masks and live compiled bytes bind this real
formatting defect. Six village menu strings and the Inuvik name remain Japanese.
These observed gaps require correction; older controlled raster passes do not close
them. The intended Aurora entry was a navigation failure: actual input `auaaaA`
is explicitly retained and receives no successful-password or keyboard-bug claim.
None of nine selected whole top screens is one of the eight village cards; their
ordinary contexts remain open, with no global nonuse claim. Both rejected V606
setups are retained. Twelve unmodified fixture screenshots and provenance are on E;
no guide/earned travel credit. Production V604 and patch unchanged, all18 plaques
incomplete and all22 historical objects exact. Goal active; see
[V607 real village UI and defects](village_water_v607_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        path = Path("docs") / name
        text = path.read_text(encoding="utf-8-sig")
        if "## V607: actual village discovery exposes formatting and UI translation gaps" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V607: native village UI and real defects;12 fixture screenshots on E;18/22 exact;V604 unchanged.")


if __name__ == "__main__":
    main()
