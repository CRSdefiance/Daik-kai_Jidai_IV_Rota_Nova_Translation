"""Archive complete original caller-loop evidence without narrowing the goal."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/slack_caller_loop_v588")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V588 Original SLACK caller")
DOC = Path("docs/slack_caller_loop_v588_checkpoint.md")
SCRIPT = Path("scripts/trace_slack_caller_loop_v588.py")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    proof = ROOT / "original_loop_proof.json"
    p = read(proof)
    assert p["script_sha256"] == sha(SCRIPT.read_bytes())
    assert [r[0] for r in p["original_wrapper_calls"]] == [14, 15, 16, 17]
    assert len(p["real_metadata_virtual_calls"]) == len(p["four_persisted_actual_PXL_views"]) == 4
    assert not p["raw_buffer_read_events"] and not p["ARM9_DMA_register_writes_in_loop"]
    assert sha(Path(p["source_snapshot"]["path"]).read_bytes()) == p["source_snapshot"]["sha256"]
    assert sha(Path(p["source_report"]).read_bytes()) == p["source_report_sha256"]
    candidate = Path("out/all_routes_combined_v581_candidate.nds")
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == "e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415"
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for path in (proof, SCRIPT, DOC):
        target = ARCHIVE / path.name
        shutil.copyfile(path, target)
        assert sha(path.read_bytes()) == sha(target.read_bytes())
    receipt = {path.name: sha(path.read_bytes()) for path in ARCHIVE.iterdir()
               if path.is_file() and path.name != "provenance.json"}
    (ARCHIVE / "provenance.json").write_text(json.dumps({
        "candidate_sha256": p["candidate_sha256"], "files": receipt,
        "existing_capture_reused_not_new_emulator_or_screenshot_evidence": True,
        "new_screenshots": 0, "guide_or_publication_approval": False,
        "not_global_nonuse_or_actual_raw_comic_display_proof": True}, indent=2) + "\n", encoding="utf-8")
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
             "scripts": {str(SCRIPT): sha(SCRIPT.read_bytes())},
             "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
             "source_report_sha256": p["source_report_sha256"],
             "original_complete_loop_with_own_counter_and_header_initialization": True,
             "real_metadata_virtual_calls": 4, "source_blocks": [14, 15, 16, 17],
             "complete_raw_bytes_per_block": 14144, "captured_PXL_views_exact44_bytes_each": 4,
             "raw_buffer_ARM_reads_in_entire_replay": 0, "ARM9_DMA_setup_writes": 0,
             "all_main_overlay_ARM_B_BL_and_Thumb_BL_BLX_and_stored_pointer_census": True,
             "sole_direct_wrapper_call": "0209EDE8", "other_Thumb_or_pointer_candidates": 0,
             "current_parent_globals_and_stack_are_replay_contracts": True,
             "not_full_UI_constructor_new_GPU_capture_or_Maria_unlock": True,
             "other_indirect_fileID_reader_later_and_hardware_paths_remain_open": True,
             "no_global_unused_or_comic_display_claim": True,
             "archive": str(ARCHIVE), "new_screenshots": 0,
             "production_ROM_and_patch_changed": False, "all18_plaques_remain_incomplete": True,
             "all22_historical_objects_retained": True, "full_goal_complete": False}
    snapshot = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in snapshot.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d["whole_original_SLACK_caller_loop_v588"] = entry
        d["current_goal_turn_classification"] = "progress-complete-original-SLACK-caller-loop-with-real-metadata-four-PXL-views-and-expanded-target-census"
        target.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reread = read(target)
        assert reread.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert reread.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V588: complete original SLACK portrait caller loop

Original0209ED3C-0209EE94 executes its own counter/header setup, all four real
metadata virtual calls, four14..17 archive reads and four exact44-byte captured
PXL views. The whole replay has zero raw-buffer ARM reads or DMA setup writes;
the synthetic20-byte header is exact. An expanded all-main/overlay ARM B/BL,
Thumb BL/BLX and all-byte stored-pointer census finds only known0209EDE8 for
the wrapper. This closes the earlier skipped-metadata/per-index-fragment gap,
not global non-use, other readers, a full UI constructor or actual comic display.
Reused ordinary V581 source RAM/report remain exact; no new screenshot, ROM,
patch or guide credit. Proofs are on E under Test fixtures/V588 Original SLACK
caller. All18 entries remain incomplete and all22 historical objects retain
exact scope. See [V588 whole-loop evidence](slack_caller_loop_v588_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V588: complete original SLACK portrait caller loop" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V588 full original loop in3 audits/4 docs and E evidence archive;source capture/18/22 exact;V581 unchanged.")


if __name__ == "__main__":
    main()
