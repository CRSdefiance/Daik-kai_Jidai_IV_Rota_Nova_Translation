"""Retain corrected score ownership, successful composites and unresolved frames."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/material_review_v600")
DOC = Path("docs/score_parent_v600_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V600 Score parent")
KEY = "corrected_score_owner_and_original_native_result_parent_v600"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    path = ROOT / "native_score_parent_proof.json"
    p = read(path)
    assert p["script_sha256"] == sha(Path("scripts/verify_score_parent_v600.py").read_bytes())
    assert sha(Path(p["production_ROM"]).read_bytes()) == p["production_ROM_sha256"]
    candidate = Path(p["production_ROM"])
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == "2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f"
    assert sha(Path("out/raphael_natural_v2_accepted_base.nds").read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    screenshots = []
    for kind, binding in p["reports"].items():
        assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
        r = read(binding["path"])
        shots = {s["frame"]: s for s in r["frames_captured"]}
        for frame in (4300, 4400, 4500, 4550):
            shot = shots[frame]
            target = ARCHIVE / f"{kind}_{frame:06d}.png"
            copy_checked(shot["path"], target)
            screenshots.append({"path": str(target), "sha256": shot["PNG_sha256"], "frame": frame,
                                "kind": kind, "unmodified_native_frame": True,
                                "research_result_not_earned_battle_outcome": True})
        copy_checked(binding["path"], ARCHIVE / (kind + "_capture_report.json"))
    for source in (DOC, path, ROOT / "native_score_fixture_manifest.json", ROOT / "original_result_animation_states.json",
                   ROOT / "actual_score_parent.txt", Path("scripts/prepare_score_parent_v600.py"),
                   Path("scripts/verify_score_parent_v600.py"), Path("scripts/native_ship_type_fixture_v600.py"), Path(__file__)):
        copy_checked(source, ARCHIVE / source.name)
    diagnostic_reports = []
    for kind in ("current", "original"):
        source = Path(f"E:/Rota Nova translations/Generated/work/emulation_v193/score_parent_v600_{kind}/capture_report.json")
        r = read(source)
        assert len(r["synthetic_ship_type_fixtures"]) == 1
        assert r["synthetic_ship_type_fixtures"][0]["one_type_byte_only"]
        assert r["synthetic_ship_type_fixtures"][0]["helper_sha256"] == sha(Path("scripts/native_ship_type_fixture_v600.py").read_bytes())
        copy_checked(source, ARCHIVE / ("wrong_owner_diagnostic_" + kind + "_report.json"))
        diagnostic_reports.append({"path": str(source), "sha256": sha(source.read_bytes()),
            "not_score_rendering_credit": True, "original_did_not_reach_same_Deck_context": kind == "original"})
    save(ARCHIVE / "provenance.json", {"production_ROM": str(candidate), "production_ROM_sha256": p["production_ROM_sha256"],
        "research_only": True, "ordinary_guide_or_earned_battle_credit": False, "publication_approved": False,
        "screenshots": screenshots, "wrong_owner_diagnostic_reports": diagnostic_reports,
        "files": {f.name: sha(f.read_bytes()) for f in ARCHIVE.iterdir() if f.is_file() and f.name != "provenance.json"}})
    results = p["native_three_way_frame_results"]
    entry = {"documentation": str(DOC), "proof": str(path), "proof_sha256": sha(path.read_bytes()),
        "candidate": str(candidate), "candidate_sha256": p["production_ROM_sha256"],
        "production_ROM_or_patch_changed": False, "old_V164_resource_selection_claim_superseded": True,
        "actual_score_owner": 0x02313A38, "old_wrong_owner_is_deckchip15": 0x023139FC,
        "full_original_initializer_and_real_cached_payload_names_verified": True,
        "original_source_parent_and_complete_24x24_label_crops_mapped": True,
        "native_original_result_renderer_with_explicit10_2_12_counters": True,
        "source_font_complete_English_ink_points": 94, "whole_source_blank_current_frames_exact": len(results["whole_composites_exact"]),
        "whole_native5_composites": p["whole_native5_composites_checked"],
        "native5_composite_pixel_positions": p["whole_native5_composite_positions"],
        "whole_triples_unchanged": len(results["unchanged"]), "unanchored_frames_remaining": results["no_digit_anchor"],
        "whole_composite_mismatches_remaining": results["whole_composite_mismatch"],
        "all_original_current_pair_comparisons": p["all_same_frame_original_current_comparisons"],
        "whole_pairs_identical": len(p["whole_identical_pairs"]), "no_adaptive_frame_retiming": True,
        "all_animation_frames_or_earned_results_verified": False,
        "research_archive": str(ARCHIVE), "full_unmodified_research_screenshots": len(screenshots),
        "guide_publication_or_human_acceptance_approved": False,
        "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-corrected-score-owner-mapped-real-parent-and-native-three-way-composites-with-failures-retained"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V600: corrected score owner and original result-parent evidence

The old V164 selector test mispaired adjacent initializer literals. Executing
the full original initializer proves owner023139FC is deckchip15, whereas the
real deck04 score owner is02313A38. The old score-selection interpretation is
superseded; historical font/generator evidence remains separate. Original
score setup0200C14C/painter0200C054 now bind both complete24x24 label cells.
Three explicit research cold boots run the unmodified original result selector
and animation with10 Won/2 Lost/12 total, preserving real owner/crops/getters.
All three complete resident score files and native one-shot guards/counters
pass. All94 English ink points and a separate live centered-controller snapshot
pass. Across the451-frame triple window,323 frames pass both entire native5
composites (63,504,384 positions);99 are wholly unchanged. Twelve unanchored and
17 failed whole comparisons retain exact diagnostics and remain unresolved.
Across2905 original/current pairs,2552 are wholly identical. No adaptive frame
shift, earned result, normal guide or every-animation-frame claim is made.
Twelve full research screenshots/proofs/provenance are on E. Production V599,
its patch, artwork and registry remain unchanged. All18 plaques remain incomplete,
all22 historical objects remain exact;the wider goal stays active. The build
protocol now requires actual initialized filenames/resident payloads rather than
adjacent-pool pairing. See [V600 score evidence](score_parent_v600_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md", "plaque_background_texture_defect.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V600: corrected score owner and original result-parent evidence" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V600:corrected binding/native real parent;323 whole triple frames;12 unanchored/17 failures retained;12 research images on E;18/22 exact;V599 unchanged.")


if __name__ == "__main__":
    main()
