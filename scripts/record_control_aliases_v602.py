"""Archive decoded-copy evidence without granting unvisited native-context credit."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/graphics_aliases_v602")
DOC = Path("docs/control_aliases_v602_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Audit comparisons/V602 Control aliases")
KEY = "decoded_control_alias_search_and_current_embedded_index_sync_v602"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof = ROOT / "current_control_copy_proof.json"
    p = read(proof)
    assert p["script_sha256"] == sha(Path("scripts/verify_control_aliases_v602.py").read_bytes())
    assert sha(Path(p["candidate"]).read_bytes()) == p["candidate_sha256"]
    assert sha(Path(p["candidate"]).with_suffix(".xdelta").read_bytes()) == "2aa5a523cfef3165db2eae31643b2d66e3e08a75aa709c025066958a144ffc9f"
    assert all(sha(Path(path).read_bytes()) == digest for path, digest in p["source_alias_proofs"].items())
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof, ROOT / "decoded_template_alias_proof.json", ROOT / "embedded_control_alias_proof.json",
             Path(p["comparison_sheet"]), Path("scripts/scan_graphic_template_aliases_v602.py"),
             Path("scripts/scan_embedded_control_aliases_v602.py"), Path("scripts/verify_control_aliases_v602.py"), Path(__file__)]
    for source in files:
        copy_checked(source, ARCHIVE / source.name)
    save(ARCHIVE / "provenance.json", {"candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
        "analysis_sheet_not_native_screenshot_or_guide": True,
        "embedded_index_mask_not_native_color_claim": True, "publication_approved": False,
        "files": {f.name: sha(f.read_bytes()) for f in ARCHIVE.iterdir() if f.is_file() and f.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
        "candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"], "production_ROM_or_patch_changed": False,
        "PXL_files": 660, "FLS_textures": 261, "decoded_color_domains": 1313, "indexed_shapes": 879,
        "all57_embedded_blocks_visited": True, "bounded_legacy_packets": 31, "legacy_palette_domains": 128,
        "external_palette_storage_pairs": 3, "external_palette_domains": 104,
        "five_known_embedded_controls_automatically_located_and_current_index_crops_exact": True,
        "complete_current_miniature_ink_pixels": 307, "complete_Confirm_ink_pixels": 86,
        "no_additional_exact_Confirm_alias_in_declared_decoders": True,
        "Confirm_initialized_filename_verified_original_owner_was_correct": True,
        "both_control_atlases_byte_identical_to_prior_native_V573": True,
        "odd_nibble_unequal_stride_reordered_palette_and_changed_ink_controls_pass": True,
        "rescaled_recolored_partial_or_raw_block_aliases_not_excluded": True,
        "native_embedded_palette_alpha_and_ordinary_parents_still_unresolved": True,
        "archive": str(ARCHIVE), "new_native_screenshots": 0, "new_guide_candidates": 0,
        "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-decoded-control-copy-search-with-seven-self-controls-and-five-current-embedded-index-aliases"
        save(target, d)
        check = read(target)
        assert check.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert check.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V602: decoded control-copy search and embedded English synchronization

All660 PXL/261 FLS entries receive decoded-row template checks over1313 color
domains and879 indexed shapes. Seven original controls are recovered; no other
exact PXL/FLS Confirm or miniature copy appears in these bounded comparisons.
Unequal-stride, odd-nibble, reordered-palette/bank and changed-ink controls pass.
All57 embedded blocks are visited;31 legacy packets/128 palette domains and
three external-palette storage pairs/104 domains receive separate checks. An
index-shape pass automatically recovers the five known CMMNIMG block5 aliases.
All current embedded crops match the English loose atlas, including307 complete
miniature ink points. Confirm's86-point face and actual initialized filename
pass;both full control atlases remain byte-identical to prior native V573.
An index alias does not establish color/alpha or a shared native consumer.
Confirm and five miniature ordinary parents, raw/unparsed/partial/rescaled copy
classes and the wider audit remain open. Source/current/index analysis sheet
and hashed proofs are on E;no new emulator screenshots or guide credit. V599,
patch, art and registry remain unchanged. All18 plaques remain incomplete and
all22 historical objects retain exact scope;goal active. See
[V602 decoded alias evidence](control_aliases_v602_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V602: decoded control-copy search and embedded English synchronization" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V602:921-entry decoded search;5 embedded English copies/307 ink points;86 Confirm;analysis archive on E;18/22 exact;ordinary parents open;V599 unchanged.")


if __name__ == "__main__":
    main()
