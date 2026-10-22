"""Record the completed actual equipment catalogue while retaining all audit scope."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/equipment_catalogue_v586")
DOC = Path("docs/equipment_catalogue_v586_checkpoint.md")


def main():
    path = ROOT / "native_catalogue_proof.json"
    p = json.loads(path.read_text(encoding="utf-8"))
    assert len(p["all103_native_equipment_items"]) == 103 and len(p["empty_slot_cases"]) == 37
    assert p["whole_paper_pixels"] == 205088 and p["fixture_replays"] == 28
    for script, digest in p["scripts"].items():
        assert sha(Path(script).read_bytes()) == digest
    sets = json.loads((ROOT / "equipment_sets.json").read_text(encoding="utf-8"))
    commands = [{"until": 5480, "buttons": ["B"], "duration": 8}]
    for n, items in enumerate(sets):
        first = 5560 + n * 320
        commands.append({"until": first, "equipment_items": items, "buttons": ["A"], "duration": 8})
        commands.extend({"until": first + offset, "buttons": ["LEFT"], "duration": 8}
                        for offset in (40, 80, 120, 160))
        if n < 27:
            commands.append({"until": first + 240, "buttons": ["B"], "duration": 8})
    commands.append({"stop": True})
    journal = ROOT / "interactive_commands.jsonl"
    journal.write_text("\n".join(json.dumps(row) for row in commands) + "\n", encoding="utf-8")
    archive = Path(p["archive"])
    for source in (DOC, journal, *(Path(script) for script in p["scripts"])):
        target = archive / source.name
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    receipt = {f.name: sha(f.read_bytes()) for f in archive.iterdir() if f.is_file() and f.name != "provenance.json"}
    (archive / "provenance.json").write_text(json.dumps({
        "candidate_sha256": p["candidate_sha256"], "files": receipt,
        "full_unmodified_native_screenshots": 140, "synthetic_equipment_display_fixture": True,
        "normal_acquisition_or_eligibility_verified": False, "guide_or_publication_approval": False}, indent=2) + "\n", encoding="utf-8")
    visual_ids = [92, 98, 126, 40, 71, 197]
    visual = [r for r in p["all103_native_equipment_items"] if r["item_id"] in visual_ids]
    visual.append(p["empty_slot_cases"][-1])
    entry = {
        "documentation": str(DOC), "proof": str(path), "proof_sha256": sha(path.read_bytes()),
        "candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
        "scripts": p["scripts"], "native_unique_equipment_names": 103,
        "native_category_counts_weapon_armor_accessory": [28, 26, 49],
        "actual_hint_appearances": 140, "empty_appearances": 37,
        "empty_slots_this_run": [1, 2, 3, 4], "new_empty_Weapon_claimed": False,
        "whole_paper_pixels": 205088, "complete_original_icon_pixels": 105472,
        "original_transfer_fixture_replays_with_exact_bounded_writes": 28,
        "all_complete_names_blank_cells_source_wood_frames_and_icons_exact": True,
        "seven_visually_reviewed_fullscreens": [{"frame": r["frame"], "item_id": r["item_id"],
                                                   "name": r["display"]["name"]} for r in visual],
        "all_other_characters_conditions_acquisition_and_eligibility_not_proven": True,
        "no_other_global_or_ordinary_marker_parent_claim": True,
        "original_and_test_source_saves_unchanged": True,
        "archive": str(archive), "full_screenshots": 140,
        "production_ROM_and_patch_changed": False, "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False,
    }
    snapshot = json.loads(Path("work/analysis/confirm_material_v572/audit_scope_before.json").read_text(encoding="utf-8"))
    for filename, old in snapshot.items():
        target = Path("translations") / filename
        d = json.loads(target.read_text(encoding="utf-8-sig"))
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d["all103_equipment_native_hints_v586"] = entry
        d["current_goal_turn_classification"] = "progress-all103-native-equipment-names-icons-and37-empty-hints-with-source-wood-and-captured-owner-binding"
        target.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reread = json.loads(target.read_text(encoding="utf-8"))
        assert reread.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert reread.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V586: every equipment name in native Sailor Info

A14,360-frame V581 cold boot with28 bounded original-transfer equipment fixtures
now verifies all103 native equipment names:28 weapons,26 armor and49 accessories.
All140 actual hint appearances (103 occupied/37 empty) pass205,088 complete paper
pixels, full first/final letters/spaces and105,472 original icon pixels. Captured
slots/categories/names/owners and every fixture replay match; source saves and
ROM/patch remain unchanged. Seven fullscreens were visually reviewed. All140
unmodified selected screenshots/proofs/provenance are on E under Test fixtures/
V586 All equipment hints. This is Maria display coverage with explicit slots,
not normal acquisition/eligibility, every character/condition, guide approval or
global graphics completion. No new empty-Weapon case is claimed; the earlier
V581 case remains separate. All18 plaque entries remain incomplete and all22
historical objects retain exact scope. See
[V586 complete catalogue evidence](equipment_catalogue_v586_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md", "plaque_background_texture_defect.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V586: every equipment name in native Sailor Info" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V586 in all three audits/five documents;140 full screenshots and provenance archived;18/22 exact;goal incomplete.")


if __name__ == "__main__":
    main()
