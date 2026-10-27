"""Record complete ordinary Price Info names without closing other graphics gates."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/marker_consumers_v605")
DOC = Path("docs/price_catalog_v605_checkpoint.md")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V605 Price Info")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Audit comparisons/V605 Price Info")
KEY = "actual_Price_Info_parent_all113_normal_names_and124_canvas_replays_v605"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof_path = ROOT / "native_price_catalog_proof.json"
    p = read(proof_path)
    assert p["script_sha256"] == sha(Path("scripts/verify_price_catalog_v605.py").read_bytes())
    assert sha(Path(p["candidate"]).read_bytes()) == p["candidate_sha256"]
    assert sha(Path(p["candidate"]).with_suffix(".xdelta").read_bytes()) == "5fa980cd6995606989375b69e6be7083cfcb6fbe90c122e96e2a30d7bc20cc7a"
    assert sha(Path(p["report"]).read_bytes()) == p["report_sha256"]
    assert sha(Path(p["marker_census"]).read_bytes()) == p["marker_census_sha256"]
    assert len(p["native_unique_name_cases"]) == 113 and len(p["all124_actual_parent_CPU_replay"]) == 124
    assert len(p["excluded_by_original_view_filter"]) == 11
    GUIDE.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    selected = {}
    for case in p["native_unique_name_cases"]:
        selected.setdefault(case["category"], case)
    chosen = list(selected.values())
    long_ids = (102, 103, 104, 108, 115, 117)
    chosen.extend(case for case in p["native_unique_name_cases"] if case["index"] in long_ids)
    assert len(chosen) == 24 and len({c["index"] for c in chosen}) == 24
    guide = []
    for case in chosen:
        source = Path(case["screenshot"])
        assert sha(source.read_bytes()) == case["screenshot_sha256"]
        target = GUIDE / f"V605_{case['index']:03d}_{case['frame']:06d}_Price_Info.png"
        copy_checked(source, target)
        guide.append({"path": str(target), "sha256": case["screenshot_sha256"], "frame": case["frame"],
                      "commodity_index": case["index"], "English": case["English"], "category": case["category"],
                      "unmodified_native_screenshot": True})
    files = [DOC, proof_path, Path(p["marker_census"]), Path(p["report"]), ROOT / "final_recorded_inputs.json",
             ROOT / "footer_4x.png", ROOT / "price_panel_3x.png", Path(__file__),
             Path("scripts/trace_marker_consumers_v605.py"), Path("scripts/verify_price_catalog_v605.py")]
    for source in files:
        copy_checked(source, ARCHIVE / source.name)
    for source in (DOC, proof_path, Path(p["report"]), ROOT / "final_recorded_inputs.json"):
        copy_checked(source, GUIDE / source.name)
    for folder, shots in ((GUIDE, guide), (ARCHIVE, [])):
        save(folder / "provenance.json", {"candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
            "ordinary_New_Game_no_battery_save_savestate_or_synthetic_fixture": True,
            "publication_approved": False, "hardware_device_verification": False, "screenshots": shots,
            "analysis_enlargements_are_not_unmodified_native_screenshots": True,
            "files": {f.name: sha(f.read_bytes()) for f in folder.iterdir() if f.is_file() and f.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
        "candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"], "production_ROM_patch_registry_art_changed": False,
        "ordinary_frames": p["frames"], "actual_parent_RTTI": p["parent_RTTI"], "actual_name_canvas": [256, 128],
        "all113_originally_listed_names_and18_categories_observed": True, "native_name_appearances": p["native_name_appearances"],
        "unique_native_name_foreground_positions": 130176, "unique_complete_ink_points": p["unique_complete_ink_points"],
        "all124_real_parent_CPU_canvas_replays": True, "whole_canvas_replay_bytes": 2031616,
        "11_originally_filtered_names_no_global_nonuse_or_normal_display_claim": True,
        "earlier_supplied_anchor_kept_as_bounded_research_not_historical_parent_proof": True,
        "88_marker_PC_loads_and_three_actual_Sold_Local_Cargo_selector_calls_bound": True,
        "five_marker_header_ordinary_parents_still_open": True, "existing_abbreviations_not_new_editorial_review": True,
        "guide_archive": str(GUIDE), "unmodified_ordinary_guide_screenshots": len(guide), "audit_archive": str(ARCHIVE),
        "publication_approved": False, "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-ordinary-all113-Price-Info-names-real-parent-and124-entire-canvas-replays"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V605: actual Price Info parent and all normally listed commodity names

A47,580-frame ordinary New Game run opens Market Info's free Lisbon report and
traverses all18 categories. All113 entries passing the original byte14-bit0 filter
appear, with186 name appearances and130,176 complete native foreground positions.
Captured CPriceInformationView RTTI binds the real parent/member256x128 canvas,
source[48,12,144,24] and native[160,208,256,220]. All first/final letters, spaces
and blank tails pass. The original updater also executes all124 IDs against that
real canvas, comparing2,031,616 complete bytes with unchanged header/palette.
Eleven originally filtered entries receive only CPU evidence, not ordinary display
or global nonuse credit. Earlier V357's supplied different anchor remains bounded
font research. The initial Y Price lead was a small-caption misread; enlarged
native pixels show Y Sell and Y left the whole frame unchanged. An88-load marker
census binds the existing Cargo/Local/Sold selectors; the five other marker
header contexts remain open.24 unmodified ordinary guide screenshots and provenance
are on E, publication unapproved. V604 ROM/patch/art/registry unchanged;all18
plaques incomplete/all22 objects exact;goal active. See
[V605 native Price Info catalog](price_catalog_v605_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V605: actual Price Info parent and all normally listed commodity names" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V605:113 ordinary Price Info names/18 categories;124 real-parent canvas cases;24 guide screenshots on E;18/22 exact;V604 unchanged.")


if __name__ == "__main__":
    main()
