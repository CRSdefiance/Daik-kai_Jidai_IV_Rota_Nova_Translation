"""Record runtime source-rectangle evidence while preserving every open audit item."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/blitter_trace_v603")
DOC = Path("docs/blitter_trace_v603_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V603 Runtime drawing trace")
KEY = "native_bounded_drawing_call_trace_v603"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof_path = ROOT / "native_trace_proof.json"
    p = read(proof_path)
    assert p["script_sha256"] == sha(Path("scripts/verify_blitter_trace_v603.py").read_bytes())
    assert sha(Path(p["production_ROM"]).read_bytes()) == p["production_ROM_sha256"]
    assert sha(Path(p["production_ROM"]).with_suffix(".xdelta").read_bytes()) == "2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f"
    assert sha(Path(p["fixture_manifest"]).read_bytes()) == p["fixture_manifest_sha256"]
    assert sha(Path(p["ABI_proof"]).read_bytes()) == p["ABI_proof_sha256"]
    assert p["whole_capture_pairs_exact"] == 51 and p["unique_frame_pairs_exact"] == 48
    assert p["total_drawing_calls"] == 404767 and p["total_native_frames"] == 36650
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    paths = [DOC, proof_path, Path(p["fixture_manifest"]), Path(p["ABI_proof"]), Path(__file__),
             Path("scripts/prepare_blitter_trace_v603.py"), Path("scripts/verify_blitter_trace_abi_v603.py"),
             Path("scripts/verify_blitter_trace_v603.py")]
    for path in paths:
        copy_checked(path, ARCHIVE / path.name)
    chosen = {"keyboard": (4400, 5700, 7900), "deck": (4650,), "market": (21500, 23200, 24100)}
    archive_shots, bindings = [], {}
    for run in p["runs"]:
        scene = run["scene"]
        report_path = Path(run["report"])
        assert sha(report_path.read_bytes()) == run["report_sha256"]
        report = read(report_path)
        copy_checked(report_path, ARCHIVE / f"{scene}_capture_report.json")
        copy_checked(ROOT / f"{scene}_inputs.json", ARCHIVE / f"{scene}_inputs.json")
        native_path = Path(run["native_state"])
        assert sha(native_path.read_bytes()) == run["native_state_sha256"]
        copy_checked(native_path, ARCHIVE / f"{scene}_native_state.json")
        itcm = Path(read(native_path)["regions"]["ITCM"]["path"])
        copy_checked(itcm, ARCHIVE / f"{scene}_arm9_itcm.bin")
        bindings[scene] = {"report": run["report"], "report_sha256": run["report_sha256"],
                           "baseline_report": run["baseline_report"], "baseline_report_sha256": run["baseline_report_sha256"]}
        shots = {s["frame"]: s for s in report["frames_captured"]}
        for frame in chosen[scene]:
            assert frame in run["unique_compared_frames"]
            shot = shots[frame]
            path = Path(shot["path"])
            assert sha(path.read_bytes()) == shot["PNG_sha256"]
            target = ARCHIVE / f"{scene}_{frame:06d}_RESEARCH_ONLY.png"
            copy_checked(path, target)
            archive_shots.append({"scene": scene, "frame": frame, "source": str(path), "archive": str(target),
                                  "sha256": shot["PNG_sha256"], "unmodified_native_capture": True,
                                  "instrumented_ROM_not_ordinary_guide_credit": True})
    assert len(archive_shots) == 7
    save(ARCHIVE / "provenance.json", {"production_ROM": p["production_ROM"],
        "production_ROM_sha256": p["production_ROM_sha256"], "research_instrumentation": True,
        "no_guide_or_earned_outcome_credit": True, "publication_approved": False, "reports": bindings,
        "screenshots": archive_shots,
        "files": {f.name: sha(f.read_bytes()) for f in ARCHIVE.iterdir() if f.is_file() and f.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
        "production_ROM": p["production_ROM"], "production_ROM_sha256": p["production_ROM_sha256"],
        "production_ROM_patch_or_registry_changed": False, "research_ROM_manifest": p["fixture_manifest"],
        "total_frames": 36650, "drawing_calls": 404767, "exact_capture_pairs": 51, "exact_unique_run_frame_pairs": 48,
        "zero_target_records_in_three_sampled_paths": True, "all_three_runs_both_positive_controls_zero_overflow": True,
        "final_cache_address_reuse_explicitly_checked": True, "ABI_cases": 20,
        "Confirm_and_five_miniature_ordinary_parents_still_open": True, "global_nonuse_not_proven": True,
        "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True,
        "research_screenshots_archived": 7, "new_guide_candidates": 0, "archive": str(ARCHIVE), "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-new-native-source-rectangle-trace-three-paths-positive-controls-zero-overflow"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V603: native drawing-call trace over three input paths

A new research-only observer wraps both original corner/tiled drawing entries,
preserving all registers/flags, executing the original prologues and supplying no
replacement resources or rectangles.20 ABI cases plus dedup/overflow/negative
controls pass.Three cold boots cover36,650 frames and404,767 drawing calls across
name entry, saved-game town/Deck and Market purchase/sale paths. Both routines
provide positive controls in every run; zero target records and zero overflows.
All51 compared captures/48 unique run-frame pairs match V599 exactly, including
4,718,592 whole-frame positions. One additional keyboard frame has no baseline
and gets no comparison credit. Final exports verify intact observer/hooks and
explicitly distinguish reused logged pointers from the current resident atlas.
No Confirm/miniature ordinary parent or global nonuse is established; expand to
other paths/GPU consumers rather than repeat these schedules. Seven full research
screenshots/provenance are on E; no guide or earned-outcome credit. Production
V599, patch, artwork, registry and canonical baseline are unchanged. All18 plaques
remain incomplete/all22 historical objects retain exact scope;goal active. See
[V603 runtime drawing trace](blitter_trace_v603_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V603: native drawing-call trace over three input paths" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V603:404,767 calls/36,650 frames;51 exact captures;7 research screenshots on E;18/22 exact;ordinary parents open;V599 unchanged.")


if __name__ == "__main__":
    main()
