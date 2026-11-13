"""Record bounded numeric-file client evidence and retain the complete audit."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/numeric_file_clients_v595")
DOC = Path("docs/numeric_file_clients_v595_checkpoint.md")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V595 Numeric file clients")
KEY = "original_numeric_file_clients_and_overlay_sound_arguments_v595"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    proof_path = ROOT / "numeric_clients_proof.json"
    p = read(proof_path)
    scripts = [Path("scripts/trace_numeric_file_clients_v595.py"), Path(__file__)]
    assert p["script_sha256"] == sha(scripts[0].read_bytes())
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    patch = candidate.with_suffix(".xdelta")
    assert sha(patch.read_bytes()) == "e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7"
    assert p["clean_current_native_semantics_exact_with_repacked_physical_ranges_retained"]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for path in (proof_path, DOC, *scripts):
        target = ARCHIVE / path.name
        shutil.copyfile(path, target)
        assert sha(target.read_bytes()) == sha(path.read_bytes())
    save(ARCHIVE / "provenance.json", {
        "candidate": str(candidate), "candidate_sha256": p["candidate_sha256"],
        "no_screenshots_no_guide_or_normal_comic_display_credit": True,
        "publication_approved": False, "production_ROM_or_patch_changed": False,
        "files": {path.name: sha(path.read_bytes()) for path in ARCHIVE.iterdir()
                  if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof_path),
             "proof_sha256": sha(proof_path.read_bytes()), "candidate": str(candidate),
             "candidate_sha256": p["candidate_sha256"], "source_exact_code_ranges": p["source_exact_code_ranges"],
             "main_and_overlay_target_count": 12, "all_byte_stored_pointers_and_Thumb_checked": True,
             "direct_numeric_open_calls": 6, "direct_range_open_calls": 3,
             "original_overlay_lookup_cases": 12, "complete_original_overlay_loads": 4,
             "each_loaded_overlay_bytes": 6208, "each_cleared_overlay_BSS_bytes": 32,
             "original_sound_open_calls": 6, "observed_overlay_file_id": 0,
             "observed_sound_file_id": 2, "raw_comic_file_id": 619,
             "SDK_IO_path_resolution_and_sound_parse_boundaries_explicitly_supplied": True,
             "raw_comic_GPU_display_or_global_nonuse_not_proved": True,
             "next_action": p["next_action"], "archive": str(ARCHIVE),
             "production_ROM_or_patch_changed": False, "full_goal_complete": False,
             "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-original-numeric-file-client-census-and-source-bound-overlay-sound-arguments"
        save(target, d)
        v = read(target)
        assert v.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert v.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V595: original numeric filesystem client classification

A clean/current12-target ARM9 main/overlay census adds ARM B/BL, Thumb BL/BLX
and all-byte pointer coverage for numeric-ID/direct-range opens and their clients.
Six direct numeric opens reconcile to pathname, overlay or sound inputs; three
direct-range calls belong to archive-table buffering or overlay-record reads.
The sole stored pointer is retained with its original tail-call wrapper. Twelve
complete original overlay lookup cases and four6208-byte overlay loads pass;
six original sound opens select actual sound_data.sdat ID2. Real overlay ID0
and raw SLACK archive ID619 remain distinct. SDK I/O/path/parser outcomes are
explicitly supplied; clean/current payload semantics match despite ROM repacking.
No actual raw-comic display, global nonuse, screenshot or hardware credit.
Next: non-SDK image conversion/compositing and runtime-generated references.
V593 ROM/patch unchanged; all18 plaques incomplete and all22 historical objects
exact. Proofs/scripts/provenance on E under Test fixtures/V595 Numeric file clients.
See [V595 source-bound checkpoint](numeric_file_clients_v595_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V595: original numeric filesystem client classification" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V595 in3 audits/4 docs;12/4/6 native cases;18/22 exact;V593 unchanged;no screenshot credit.")


if __name__ == "__main__":
    main()
