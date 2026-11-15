"""Archive source-bound V585 evidence and preserve all inherited audit scope."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/resource_owners_v585")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V585 Resource owners")
DOC = Path("docs/resource_owner_tables_v585_checkpoint.md")


def main():
    proof = ROOT / "owner_table_proof.json"
    addresses = ROOT / "address_derivation_candidates.json"
    p, a = (json.loads(path.read_text(encoding="utf-8")) for path in (proof, addresses))
    assert p["candidate_sha256"] == a["candidate_sha256"]
    assert p["initialized_PXL_owners"] == 315 and p["no_external_stored_absolute_owner_pointer_count"] == 35
    assert len(a["candidates"]) == 7
    scripts = [Path("scripts/trace_resource_owner_tables_v585.py"),
               Path("scripts/scan_owner_address_derivations_v585.py")]
    assert [sha(path.read_bytes()) for path in scripts] == [p["script_sha256"], a["script_sha256"]]
    rom = Path("out/all_routes_combined_v581_candidate.nds")
    patch = rom.with_suffix(".xdelta")
    assert sha(rom.read_bytes()) == p["candidate_sha256"]
    assert sha(patch.read_bytes()) == "e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415"
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [proof, addresses, DOC, *scripts]
    receipt = {}
    for path in files:
        target = ARCHIVE / path.name
        shutil.copyfile(path, target)
        receipt[path.name] = sha(path.read_bytes())
        assert sha(target.read_bytes()) == receipt[path.name]
    (ARCHIVE / "provenance.json").write_text(json.dumps({
        "kind": "original ARM initializer/cache-list and static owner-pointer evidence",
        "candidate_sha256": p["candidate_sha256"], "files": receipt,
        "ordinary_gameplay_screenshots": 0, "guide_or_publication_approval": False,
        "not_global_non_use_or_actual_parent_context_proof": True}, indent=2) + "\n", encoding="utf-8")
    entry = {
        "documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
        "address_candidate_proof": str(addresses), "address_candidate_proof_sha256": sha(addresses.read_bytes()),
        "scripts": {str(path): sha(path.read_bytes()) for path in scripts},
        "candidate": str(rom), "candidate_sha256": p["candidate_sha256"],
        "original_current_initializer_objects_exact": 315, "initializer_nonstack_writes": 1898,
        "initializer_unique_instructions": 2864,
        "objects_without_external_stored_base_owner_pointers": 35,
        "old_Online_literal_paths_missing_same_basename_elsewhere_not_assumed_aliases": 15,
        "positive_portrait_mysterymap_Extras_pointer_table_controls": True,
        "original_cache_list_admission_and_unlink_ABI_exact_current_clean": True,
        "cache_header_lookup_explicitly_bridged_not_actual_file_load_or_display": True,
        "bounded_address_candidates": 7,
        "all_candidates_are_initializer_or_already_bound_frame_row216": True,
        "computed_indexed_relative_Thumb_runtime_and_copy_paths_remain_open": True,
        "no_global_non_use_or_new_ordinary_parent_claim": True,
        "ordinary_miniature_Confirm_marker_logo_and_legacy_contexts_remain_open": True,
        "archive": str(ARCHIVE), "ordinary_gameplay_screenshots": 0,
        "production_ROM_and_patch_changed": False, "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False,
    }
    snapshot = json.loads(Path("work/analysis/confirm_material_v572/audit_scope_before.json").read_text(encoding="utf-8"))
    for filename, saved in snapshot.items():
        path = Path("translations") / filename
        d = json.loads(path.read_text(encoding="utf-8-sig"))
        assert d.get("historical_pending_items_retained") == saved["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == saved["ongoing_plaque_inventory"]
        d["original_resource_tables_and_address_candidates_v585"] = entry
        d["current_goal_turn_classification"] = "progress-original-resource-pointer-tables-cache-admission-and-calculated-address-reconciliation"
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reread = json.loads(path.read_text(encoding="utf-8"))
        assert reread.get("historical_pending_items_retained") == saved["historical_pending_items_retained"]
        assert reread.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == saved["ongoing_plaque_inventory"]
    paragraph = """

## V585: original resource tables and calculated owner addresses

Original/current initialization matches315 PXL owners,2,864 unique instructions
and1,898 nonstack writes. Frame/Confirm are self-linked rather than published to
a selection table; original cached getter/unlink cases prove later list admission
with an explicit supplied cache header, not file-load/display credit. All-byte
stored-pointer scans distinguish real table-selected controls from35 objects
without external base-owner pointers. Fifteen old Online filename paths are
absent while same basenames exist in the newer subdirectory; no alias is assumed
or changed. Seven bounded ARM address candidates reconcile to six initializer
stores and an already-bound row216 view. Computed/indexed/relative/Thumb/runtime
and embedded-copy paths remain open; no unused-art or ordinary-parent conclusion.
Proofs/provenance are on E under Test fixtures/V585 Resource owners. No new ROM,
patch or screenshot. All18 plaques remain incomplete and all22 historical objects
retain exact scope. See [V585 source-bound evidence](resource_owner_tables_v585_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        path = Path("docs") / name
        text = path.read_text(encoding="utf-8-sig")
        if "## V585: original resource tables and calculated owner addresses" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    print("V585 recorded in all audits/progress docs and E proof archive;18/22 exact;V581 ROM/patch unchanged.")


if __name__ == "__main__":
    main()
