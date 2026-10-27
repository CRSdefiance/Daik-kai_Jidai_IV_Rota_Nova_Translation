"""Record native keyboard-control evidence while preserving historical audit scope."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/keyboard_labels_v599")
DOC = Path("docs/keyboard_page_labels_v599_checkpoint.md")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V599 Name keyboard")
AUDIT = Path("E:/Rota Nova translations/Screenshots/Audit comparisons/V599 Keyboard controls")
KEY = "ordinary_keyboard_EN_Symbol_controls_display_only_release_v599"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof = ROOT / "release_proof.json"
    p = read(proof)
    assert p["script_sha256"] == sha(Path("scripts/verify_keyboard_labels_v599.py").read_bytes())
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    preservation = ROOT / "preservation_proof.json"
    assert read(preservation)["candidate_sha256"] == p["candidate_sha256"]
    GUIDE.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    reports = {}
    for label, binding in p["reports"].items():
        assert sha(Path(binding["path"]).read_bytes()) == binding["sha256"]
        reports[label] = read(binding["path"])
        copy_checked(binding["path"], AUDIT / (label + "_capture_report.json"))
    shots = {s["frame"]: s for s in reports["keyboard"]["frames_captured"]}
    guide = []
    for frame, label in ((4400, "name_edit"), (4800, "EN_and_Symbol_controls"),
                         (5500, "Latin_alphabet"), (5700, "Latin_character_inserted"),
                         (7000, "Symbols_page"), (7300, "Symbol_character_inserted"),
                         (7700, "unchanged_name_confirmation"), (7900, "returned_to_edit")):
        shot = shots[frame]
        target = GUIDE / f"V599_{frame:06d}_{label}.png"
        copy_checked(shot["path"], target)
        guide.append({"path": str(target), "sha256": shot["PNG_sha256"], "frame": frame,
                      "ordinary_cold_boot_controls_no_save_or_synthetic_fixture": True})
    old = {s["frame"]: s for s in reports["historical_keyboard"]["frames_captured"]}
    copy_checked(old[4800]["path"], AUDIT / "V581_original_Japanese_controls.png")
    copy_checked(shots[4800]["path"], AUDIT / "V599_EN_and_Symbol_controls.png")
    files = [DOC, proof, preservation, ROOT / "display_and_provider_contract.json",
             ROOT / "final_recorded_inputs.json", Path("translations/keyboard_page_labels_v1.json"),
             Path("dk4tool/patch/keyboard_page_labels.py"), Path("scripts/probe_keyboard_labels_v599.py"),
             Path("scripts/verify_keyboard_labels_v599.py"), Path(__file__)]
    for source in files:
        copy_checked(source, AUDIT / source.name)
    for source in (DOC, proof, ROOT / "final_recorded_inputs.json", Path(p["reports"]["keyboard"]["path"])):
        copy_checked(source, GUIDE / source.name)
    for folder in (GUIDE, AUDIT):
        save(folder / "provenance.json", {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
            "ordinary_cold_boot_no_existing_save_savestate_or_synthetic_fixture": True,
            "publication_approved": False, "hardware_device_verification": False,
            "screenshots": guide if folder == GUIDE else [],
            "files": {path.name: sha(path.read_bytes()) for path in folder.iterdir()
                      if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
        "profile": p["profile"], "status": "experimental", "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
        "preservation_proof": str(preservation), "preservation_proof_sha256": sha(preservation.read_bytes()),
        "patch_sha256": p["patch_sha256"], "exact_clean_patch_reconstruction": True,
        "changed_components_from_V593": p["changed_components_from_V593"],
        "only_visible_functional_labels_changed_original_identifiers_and_character_choices_exact": True,
        "earlier_visible_label_retention_superseded_original_lookup_retention_preserved": True,
        "all49_display_routes_two_only_substitutions": True, "complete_control_label_masks": 12,
        "Latin_choices": 52, "Symbol_choices": 26,
        "whole_page_foreground_positions": sum(q["native_glyph_page"]["whole_foreground_positions"]
                                                for q in p["native_provider_queries_and_complete_pages"]),
        "ordinary_character_insertion_deletion_Finish_and_Back_verified": True,
        "whole_edit_screen_returned_exact_twice": True,
        "whole_market_regression_frames_exact": p["whole_market_regression_frames_exact"],
        "all470_batches114_layers921_graphics57_embedded_blocks_retained": True,
        "guide_candidates": str(GUIDE), "full_unmodified_screenshots": len(guide), "audit_archive": str(AUDIT),
        "publication_approved": False, "human_accepted": False, "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False}
    latest = {"candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
        "proof": str(preservation), "proof_sha256": sha(preservation.read_bytes()),
        "PXL_files": 660, "FLS_textures": 261, "embedded_blocks": 57,
        "all_original_headers_all_indexed_palette_banks_and_extents_exact": True,
        "all_graphics_and_embedded_containers_exact_V593": True,
        "pixel_fidelity_translation_and_native_usage_are_separate": True}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        if "release_pointers_before_v599" not in d:
            d["release_pointers_before_v599"] = {k: d[k] for k in (
                "candidate", "candidate_sha256", "source_preservation_proof", "preservation_proof_sha256",
                "latest_graphics_preservation") if k in d}
        d[KEY] = entry
        d["latest_graphics_preservation"] = latest
        if "historical_pending_items_retained" in d:
            d.update(candidate=str(candidate), candidate_sha256=p["candidate_sha256"],
                     source_preservation_proof=str(preservation), preservation_proof_sha256=sha(preservation.read_bytes()))
        d["current_goal_turn_classification"] = "progress-display-only-keyboard-controls-native-pages-navigation-and-whole-Market-regression"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V599: display-only English/Symbol keyboard controls

The functional 英/記 keys now display EN/#+ through one guarded category-paint
call; all original lookup identifiers, 49-entry category data, fonts and character
choices remain intact. All 49 routing cases pass. A fresh ordinary 7,900-frame
New Game verifies 12 complete control masks, all 52 Latin/26 Symbol choices,
insertion/deletion on both pages and Finish/Back with unchanged Rafael. Two whole
edit-screen returns are exact. Historical comparison confines 178 changed pixels
to the two control cells; the complete Latin popup is exact. A separate ordinary
24,100-frame Market replay matches all 19 sampled whole frames. Registered V599
changes only ARM9 from V593, preserves all 470/114 layers and 921/57 graphics
checks, and reconstructs exactly from its clean patch. Earlier visible-label
retention is superseded; original identifier retention still applies. Eight
ordinary guide candidates/provenance are on E, publication unapproved. V599 is
experimental; canonical baseline unchanged. All 18 plaques remain incomplete,
all 22 historical objects remain exact, and the wider graphics goal stays active.
See [V599 keyboard checkpoint](keyboard_page_labels_v599_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / name
        text = target.read_text(encoding="utf-8-sig")
        if "## V599: display-only English/Symbol keyboard controls" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V599 in3 audits/4 progress docs;8 ordinary guide screenshots on E;18/22 exact;goal active.")


if __name__ == "__main__":
    main()
