"""Record the actual village wrapping repair without closing unrelated gates."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import DIGEST, ROM, ROOT, read, save

DOC = Path("docs/village_wrap_v608_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V608 Village wrapping")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V608 Market regression")
KEY = "actual_village_portrait_full_family_wrap_release_v608"


def copy_checked(source, destination):
    shutil.copyfile(source, destination)
    assert sha(Path(source).read_bytes()) == sha(Path(destination).read_bytes())


def main():
    proof_path, preservation_path = ROOT / "release_proof.json", ROOT / "preservation_proof.json"
    p = read(proof_path)
    assert p["script_sha256"] == sha(Path("scripts/verify_village_wrap_v608.py").read_bytes())
    assert sha(ROM.read_bytes()) == DIGEST == p["candidate_sha256"]
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == p["patch_sha256"]
    assert read(preservation_path)["candidate_sha256"] == DIGEST
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    reports = {}
    for label, receipt in p["reports"].items():
        path = Path(receipt["path"])
        assert sha(path.read_bytes()) == receipt["sha256"]
        reports[label] = read(path)
        copy_checked(path, ARCHIVE / f"{label}_capture_report.json")
    files = [DOC, proof_path, preservation_path, ROOT / "transform_proof.json",
             ROOT / "actual_canvas_proof.json", ROOT / "all28_actual_canvas_previews.png",
             ROOT / "village_inputs.json", ROOT / "market_inputs.json", Path(__file__),
             Path("scripts/prepare_village_wrap_v608.py"), Path("scripts/run_village_wrap_v608.py"),
             Path("scripts/probe_village_canvas_v608.py"), Path("scripts/verify_village_wrap_v608.py"),
             Path("dk4tool/patch/village_portrait_wrap.py"), Path("translations/village_portrait_wrap_v1.json"),
             ROM.with_suffix(".manifest.json")]
    for source in files:
        copy_checked(source, ARCHIVE / source.name)
    fixtures, guide = [], []
    for label, frames in (("village", (5600, 6000, 6400, 6900, 7800, 8200, 8600)),
                           ("former_village", (7800,))):
        shots = {s["frame"]: s for s in reports[label]["frames_captured"]}
        for frame in frames:
            row = shots[frame]
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
            target = ARCHIVE / f"{label}_{frame:06d}_LOCATION_FIXTURE.png"
            copy_checked(row["path"], target)
            fixtures.append({"path": str(target), "frame": frame, "sha256": row["PNG_sha256"],
                             "unmodified_native_capture": True, "normal_travel_or_guide_credit": False})
    shots = {s["frame"]: s for s in reports["market"]["frames_captured"]}
    for frame in (21500, 23200, 24100):
        row = shots[frame]
        target = GUIDE / f"V608_{frame:06d}_Market.png"
        copy_checked(row["path"], target)
        guide.append({"path": str(target), "frame": frame, "sha256": row["PNG_sha256"],
                      "ordinary_New_Game_no_battery_save_savestate_or_fixture": True})
    for source in (DOC, proof_path, Path(p["reports"]["market"]["path"])):
        copy_checked(source, GUIDE / source.name)
    for folder, screenshots, fixture in ((ARCHIVE, fixtures, True), (GUIDE, guide, False)):
        save(folder / "provenance.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
            "location_fixture_archive": fixture, "publication_approved": False,
            "hardware_device_verification": False, "screenshots": screenshots,
            "native_raster_sheet_is_analysis_not_replacement_art_or_ordinary_guide": True,
            "files": {s.name: sha(s.read_bytes()) for s in folder.iterdir()
                      if s.is_file() and s.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof_path),
        "proof_sha256": sha(proof_path.read_bytes()), "candidate": str(ROM), "candidate_sha256": DIGEST,
        "patch_sha256": p["patch_sha256"], "experimental_not_human_accepted": True,
        "actual_V607_request_wrap_defect_resolved": True, "all28_native_canvas_layouts_verified": True,
        "actual_sprite": [228, 48], "native_storage": [288, 48, 4], "whole_native_replay_bytes": 193536,
        "captured_6912_byte_request_plane_binding_exact": True,
        "all_words_and_leading_final_letters_preserved": True, "English_answers_and_prose_unchanged": True,
        "stored_rows12_physical_dialog_spacing16": True, "all_current_paragraphs_use_at_most3_rows": True,
        "Japanese_village_menu_and_name_still_open": True, "all8_ordinary_village_card_contexts_still_open": True,
        "successful_password_or_all28_ordinary_events_not_claimed": True,
        "ordinary_24100_frame_regression_all19_whole_screens_exact": True,
        "all470_batches114_layers921_graphics57_embedded_blocks_preserved": True,
        "native_fixture_archive": str(ARCHIVE), "native_fixture_screenshots": len(fixtures),
        "ordinary_guide_archive": str(GUIDE), "ordinary_guide_screenshots": len(guide),
        "all18_plaques_incomplete_all22_historical_objects_retained": True, "full_goal_complete": False}
    latest = {"candidate": str(ROM), "candidate_sha256": DIGEST, "proof": str(preservation_path),
        "proof_sha256": sha(preservation_path.read_bytes()), "PXL_files": 660, "FLS_textures": 261,
        "embedded_blocks": 57, "all_original_headers_all_indexed_palette_banks_and_extents_exact": True,
        "all_graphics_and_embedded_containers_exact_V604": True,
        "pixel_fidelity_translation_and_native_usage_are_separate": True}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    keys = ("candidate", "candidate_sha256", "latest_candidate", "latest_candidate_sha256",
            "current_verified_release_candidate", "current_verified_release_candidate_sha256",
            "source_preservation_proof", "preservation_proof_sha256", "latest_graphics_preservation")
    for name, old in scope.items():
        path = Path("translations") / name
        d = read(path)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        if "release_pointers_before_v608" not in d:
            d["release_pointers_before_v608"] = {k: d[k] for k in keys if k in d}
        d[KEY] = entry
        d["latest_graphics_preservation"] = latest
        for key in ("candidate", "latest_candidate", "current_verified_release_candidate"):
            if key in d:
                d[key] = str(ROM)
                d[key + "_sha256"] = DIGEST
        if "historical_pending_items_retained" in d:
            d.update(source_preservation_proof=str(preservation_path), preservation_proof_sha256=sha(preservation_path.read_bytes()))
        d["current_goal_turn_classification"] = "progress-native-village-wrap-family-fix-and-complete-registered-V608-integration"
        save(path, d)
        check = read(path)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V608: village portrait wrapping repaired across all clues/messages

The registered complete V608 candidate fixes V607's actual split-word request.
All 24 expanded clues and four messages use the portrait width; eleven stored
strings change, with no English wording or answer changes. Only ARM9 differs
from V604. Kamui's clue gets an aligned new copy in 32 additional staged bytes;
other text slots, fonts, native renderers, keyboard, artwork and scripts remain
preserved. The actual 228x48 CMessageSurfaceSprite, 288x48 four-bit VRAM plane
and bank D mapping bind the complete 6,912-byte real request to native replay.
All 28 contexts match 193,536 independently decoded canvas bytes, with complete
words/first/final letters, unchanged header/palette and no overflow. Stored rows
are 12 pixels with 16-pixel screen spacing; all current paragraphs use at most
three of four available rows. The real request's full old-width foreground,
blank tails and cleared third row pass; six other village frames stay exact.
A separate ordinary 24,100-frame New Game/Market run matches all 19 sampled whole
screens to V604. The 470-batch/114-layer manifest, exact clean patch and fresh
921/57 preservation checks pass. Eight fixture screenshots, native analysis
previews and three ordinary guide candidates are on E. Japanese village menu/name,
successful password, all eight village-card contexts and broader graphics gates
remain open. All 18 plaques stay incomplete and all 22 historical objects exact;
human acceptance/canonical unchanged, goal active. See
[V608 village portrait repair](village_wrap_v608_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        path = Path("docs") / name
        text = path.read_text(encoding="utf-8-sig")
        if "## V608: village portrait wrapping repaired across all clues/messages" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V608: complete village wrap fix;28 native canvases;19 ordinary frames;8 fixture+3 guide screenshots on E;18/22 retained.")


if __name__ == "__main__":
    main()
