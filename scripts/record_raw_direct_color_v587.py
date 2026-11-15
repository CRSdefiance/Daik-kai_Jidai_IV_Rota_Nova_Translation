"""Record bounded raw-art evidence without promoting incompatible scene controls."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/raw_direct_color_v587")
DOC = Path("docs/raw_direct_color_v587_checkpoint.md")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    proofs = [ROOT / name for name in ("native_cache_proof.json", "connected_raw_read_copy_proof.json", "event_still_contract_proof.json")]
    cache, copies, event = [read(p) for p in proofs]
    assert len(cache["cases"]) == 8 and copies["original_partial_frame_reads"] == 21
    assert copies["native_direct16_software_copy_cases"] == 84
    assert len(event["native_loader_cases"]) == 8 and len(event["screenshots"]) == 24
    scripts = [Path("scripts") / (name + "_v587.py") for name in (
        "prepare_raw_direct_color", "probe_raw_resource_cache", "verify_raw_archive_blit", "verify_event_still_contract")]
    for proof, source in zip((cache, copies, event), scripts[1:], strict=True):
        assert proof["script_sha256"] == sha(source.read_bytes())
    candidate = Path("out/all_routes_combined_v581_candidate.nds")
    assert sha(candidate.read_bytes()) == event["candidate_sha256"] == copies["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == "e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415"
    archive = Path(event["archive"])
    for path in [DOC, *proofs, *scripts, ROOT / "fixture_manifest.json", ROOT / "opening_inputs.json"]:
        target = archive / path.name
        shutil.copyfile(path, target)
        assert sha(path.read_bytes()) == sha(target.read_bytes())
    for mode, report in event["reports"].items():
        source = Path(report["path"])
        assert sha(source.read_bytes()) == report["sha256"]
        shutil.copyfile(source, archive / f"{mode}_capture_report.json")
    fixtures = read(ROOT / "fixture_manifest.json")
    for row in fixtures:
        source = Path(row["research_ROM"]).with_suffix(".fixture.json")
        shutil.copyfile(source, archive / source.name)
    assert len(list(archive.glob("*.png"))) == 24
    receipt = {p.name: sha(p.read_bytes()) for p in archive.iterdir() if p.is_file() and p.name != "provenance.json"}
    (archive / "provenance.json").write_text(json.dumps({
        "candidate_sha256": event["candidate_sha256"], "files": receipt,
        "unmodified_fullscreen_research_controls": 24, "actual_comic_GPU_display_claimed": False,
        "header_rejected_controls_are_not_graphics_clearance": True,
        "guide_or_publication_approval": False}, indent=2) + "\n", encoding="utf-8")
    entry = {
        "documentation": str(DOC), "candidate": str(candidate), "candidate_sha256": event["candidate_sha256"],
        "proofs": {str(p): sha(p.read_bytes()) for p in proofs},
        "scripts": {str(p): sha(p.read_bytes()) for p in scripts},
        "connected_original_partial_raw_frame_reads": 21,
        "native_direct16_software_copies": 84, "source_words_covered": 1612800,
        "two_screen_framebuffer_bytes_compared": 16515072,
        "raw_high_bits_preserved_without_opacity_conversion": True,
        "independent_exact_cached_PXL_API_cases": 8,
        "actual_fixed_canvas_loader": "020B7158", "actual_canvas_header": "02276D74",
        "actual_header_format_word_width_height": [8, 128, 192],
        "complete_native_fixed_canvas_loader_calls": 8,
        "six_format_and_one_geometry_rejections_preserve_destination": True,
        "one_accepted_complete_indexed_logo": True, "observed_composite_frames": 3,
        "all24_native_fullscreens_bound_to_reports": True,
        "absence_of_resident_file_is_not_no_read_proof": True,
        "raw_opacity_defect_and_original_comic_readability_not_established": True,
        "do_not_force_raw16_into_header_mismatched_event_still_test": True,
        "actual_raw_comic_descriptor_consumer_and_other_graphics_gates_open": True,
        "archive": str(archive), "full_screenshots": 24,
        "production_ROM_and_patch_changed": False, "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False,
    }
    snapshot = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for name, old in snapshot.items():
        target = Path("translations") / name
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d["raw_archive_copy_and_actual_canvas_contract_v587"] = entry
        d["current_goal_turn_classification"] = "progress-connected21-raw-frame-reads84-copies-and-native-fixed-canvas-header-gate-calibration"
        target.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reread = read(target)
        assert reread.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert reread.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V587: raw comic read/copy and actual event-still header contract

All21 current comic frames pass connected original partial reads and84 native
direct16 software copies covering1,612,800 source words/16,515,072 full framebuffer
bytes. These controlled descriptors are not GPU/ordinary-comic evidence. Eight
real cold-boot controls and complete original020B7158 calls bind the live canvas
at02276D74: files are read to scratch first, then rejected unless format/word
width/height match8/128/192. Six raw16 and one small indexed controls are rejected;
the original logo passes its whole positive composite at three frames. No raw
opacity defect or high-bit/artwork fix is inferred. Separate cached-file loading
does not establish this canvas contract. Twenty-four fullscreens/proofs/provenance
are on E under Test fixtures/V587 Raw format controls. Actual comic/legacy parents
remain open; stop repeating incompatible filename substitutions. V581 ROM/patch
unchanged;all18 plaque entries remain incomplete and all22 historical objects
retain exact scope. See [V587 checkpoint](raw_direct_color_v587_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V587: raw comic read/copy and actual event-still header contract" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V587 native raw read/copy and fixed-canvas contract in3 audits/4 docs;24 research screenshots archived;18/22 retained;V581 unchanged.")


if __name__ == "__main__":
    main()
