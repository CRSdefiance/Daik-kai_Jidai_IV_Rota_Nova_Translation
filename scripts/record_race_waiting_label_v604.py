"""Record a real native clipping repair, latest candidate and unchanged audit scope."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/race_controls_v604")
DOC = Path("docs/race_waiting_label_v604_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V604 Grand Race card status")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V604 Market regression")
KEY = "Grand_Race_shared_empty_player_card_native_fit_release_v604"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof_path, preservation = ROOT / "release_proof.json", ROOT / "preservation_proof.json"
    p = read(proof_path)
    assert p["script_sha256"] == sha(Path("scripts/verify_race_waiting_label_v604.py").read_bytes())
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    assert read(preservation)["candidate_sha256"] == p["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == p["patch_sha256"]
    assert len(p["complete_native_label_masks"]) == 9 and len(p["old_clipped_final_letter_evidence"]) == 3
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    reports = {}
    for label, binding in p["reports"].items():
        assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
        reports[label] = read(binding["path"])
        copy_checked(binding["path"], ARCHIVE / f"{label}_capture_report.json")
    files = [DOC, proof_path, preservation, ROOT / "transform_proof.json", Path(__file__),
             Path("dk4tool/patch/race_waiting_label.py"), Path("scripts/verify_race_waiting_label_v604.py"),
             Path("translations/race_waiting_label_v1.json"), candidate.with_suffix(".manifest.json"),
             ROOT / "host_return_inputs.json", ROOT / "join_inputs.json", ROOT / "candidate_save_manifest.json"]
    for path in files:
        copy_checked(path, ARCHIVE / path.name)
    fixture_shots, guide_shots = [], []
    for label, frames in {"host_baseline": (4400,), "host": (4400, 4800, 5200, 5600), "join": (4400, 5600)}.items():
        shots = {s["frame"]: s for s in reports[label]["frames_captured"]}
        for frame in frames:
            row = shots[frame]
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
            target = ARCHIVE / f"{label}_{frame:06d}_SYSTEM_UNLOCK_FIXTURE.png"
            copy_checked(row["path"], target)
            fixture_shots.append({"path": str(target), "sha256": row["PNG_sha256"], "frame": frame,
                                  "synthetic_system_unlock_not_earned_or_ordinary_guide_credit": True})
    shots = {s["frame"]: s for s in reports["market"]["frames_captured"]}
    for frame in (21500, 23200, 24100):
        row = shots[frame]
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        target = GUIDE / f"V604_{frame:06d}_Market.png"
        copy_checked(row["path"], target)
        guide_shots.append({"path": str(target), "sha256": row["PNG_sha256"], "frame": frame,
                            "ordinary_New_Game_no_existing_save_savestate_or_synthetic_fixture": True})
    for path in (DOC, proof_path, Path(p["reports"]["market"]["path"])):
        copy_checked(path, GUIDE / path.name)
    for folder, shots, fixture in ((ARCHIVE, fixture_shots, True), (GUIDE, guide_shots, False)):
        save(folder / "provenance.json", {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
            "synthetic_system_unlock": fixture, "publication_approved": False, "hardware_device_verification": False,
            "screenshots": shots, "files": {f.name: sha(f.read_bytes()) for f in folder.iterdir()
                                               if f.is_file() and f.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
        "profile": p["profile"], "status": "experimental", "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
        "preservation_proof": str(preservation), "preservation_proof_sha256": sha(preservation.read_bytes()),
        "patch_sha256": p["patch_sha256"], "exact_clean_patch_reconstruction": True,
        "original_Japanese": "-- 参加待ち --", "English": "Awaiting player", "changed_components": p["changed_components"],
        "only_shared_status_span_changes_all_pointers_code_and_art_exact_V599": True,
        "complete_native_label_masks": 9, "complete_ink_points": 1512,
        "old_native_final_r_loss_eight_points_confirmed_three_frames": True,
        "all_other_Host_frame_pixels_exact": True, "Host_and_Join_Back_verified": True,
        "whole_Market_frames_exact": p["whole_Market_frames_exact"],
        "all470_batches114_layers921_graphics57_embedded_blocks_retained": True,
        "Grand_Race_trace_calls": 27582, "ordinary_Confirm_and_miniature_parents_still_open": True,
        "wireless_peers_or_completed_race_not_verified": True,
        "test_fixture_archive": str(ARCHIVE), "fixture_screenshots": len(fixture_shots),
        "guide_candidates": str(GUIDE), "ordinary_guide_screenshots": len(guide_shots),
        "human_accepted": False, "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False}
    latest = {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
        "proof": str(preservation), "proof_sha256": sha(preservation.read_bytes()),
        "PXL_files": 660, "FLS_textures": 261, "embedded_blocks": 57,
        "all_original_headers_all_indexed_palette_banks_and_extents_exact": True,
        "all_graphics_and_embedded_containers_exact_V599": True,
        "pixel_fidelity_translation_and_native_usage_are_separate": True}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    pointer_keys = ("candidate", "candidate_sha256", "latest_candidate", "latest_candidate_sha256",
                    "current_verified_release_candidate", "current_verified_release_candidate_sha256",
                    "source_preservation_proof", "preservation_proof_sha256", "latest_graphics_preservation")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        if "release_pointers_before_v604" not in d:
            d["release_pointers_before_v604"] = {k: d[k] for k in pointer_keys if k in d}
        d[KEY] = entry
        d["latest_graphics_preservation"] = latest
        for key in ("candidate", "latest_candidate", "current_verified_release_candidate"):
            if key in d:
                d[key] = str(candidate)
                d[key + "_sha256"] = p["candidate_sha256"]
        if "historical_pending_items_retained" in d:
            d.update(source_preservation_proof=str(preservation), preservation_proof_sha256=sha(preservation.read_bytes()))
        d["current_goal_turn_classification"] = "progress-native-Grand-Race-shared-status-final-letter-repair-and-registered-complete-integration"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V604: Grand Race empty-player status native clipping repair

Unmodified V599 reproduces the final-r loss in the third empty player card;
its eight missing ink points recur at three actual Host frames. Source Japanese
-- 参加待ち -- supports the compact shared status Awaiting player. The registered
V604 terminal transform changes only the owned21-byte text span, with one verified
pointer and no code/layout/section/pool growth. Nine complete native appearances
pass1,512 ink points, all spaces and the entire old-width blank tail. Other Host
pixels, pre-waiting/Back returns and all Join samples remain exact. A separate
ordinary24,100-frame New Game/Market run matches all19 sampled whole frames to
V599. The full470-batch/114-layer candidate and clean-ROM patch reconstruct
exactly; all artwork/embedded files and921/57 preservation checks carry forward.
Grand Race trace adds27,582 calls with both controls/zero overflow/zero targets;
Confirm and five miniature ordinary parents remain open. Seven system-unlock
test screenshots and three ordinary Market guide candidates are on E, with
publication unapproved. Current audit pointers now identify V604, retaining the
older pointers separately. All18 plaques incomplete/all22 objects exact; canonical
acceptance unchanged;goal active. See
[V604 native card status](race_waiting_label_v604_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        path = Path("docs") / filename
        text = path.read_text(encoding="utf-8-sig")
        if "## V604: Grand Race empty-player status native clipping repair" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V604:complete shared card status;9 native masks/1512 ink;Host/Join/Market;registered ROM/patch on E;7 fixture+3 ordinary screenshots;18/22 exact.")


if __name__ == "__main__":
    main()
