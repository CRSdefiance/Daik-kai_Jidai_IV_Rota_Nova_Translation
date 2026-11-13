"""Record completed V584 evidence without altering retained audit requirements."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/frame_callers_v584")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V584 Frame source contracts")
KEY = "original_frame_source_contracts_and_literal_callers_v584"


def main():
    proof_path = ROOT / "frame_caller_reconciliation.json"
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    assert proof["literal_owner_loads_reconciled"] == 48
    assert proof["native_source_tile_calls"] == 852
    candidate = Path("out/all_routes_combined_v581_candidate.nds")
    assert sha(candidate.read_bytes()) == proof["candidate_sha256"]
    patch = candidate.with_suffix(".xdelta")
    if not patch.exists():
        patch = next(p for p in candidate.parent.glob("*v581*.xdelta*"))
    assert sha(patch.read_bytes()) == "e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415"
    scripts = [Path("scripts") / f"{name}_v584.py" for name in (
        "trace_frame_crop_arguments", "resolve_frame_rows", "trace_frame_styles",
        "verify_frame_blitter_contract", "verify_frame_style_tiles", "verify_frame_caller_census")]
    files = [proof_path, *(ROOT / name for name in proof["proofs"]),
             ROOT / "original_frame_atlas_4x.png", ROOT / "current_frame_atlas_4x.png"]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    receipt = {}
    for path in files:
        target = ARCHIVE / path.name
        shutil.copyfile(path, target)
        assert sha(path.read_bytes()) == sha(target.read_bytes())
        receipt[path.name] = sha(target.read_bytes())
    (ARCHIVE / "provenance.json").write_text(json.dumps({
        "candidate": str(candidate), "candidate_sha256": proof["candidate_sha256"],
        "kind": "source projections and controlled original ARM helper proofs",
        "ordinary_gameplay_screenshots": 0, "guide_or_publication_approval": False,
        "files": receipt}, indent=2) + "\n", encoding="utf-8")
    record = {
        "documentation": "docs/frame_source_contracts_v584_checkpoint.md",
        "proof": str(proof_path), "proof_sha256": sha(proof_path.read_bytes()),
        "scripts": {str(p): sha(p.read_bytes()) for p in scripts},
        "candidate": str(candidate), "candidate_sha256": proof["candidate_sha256"],
        "literal_owner_loads_reconciled": 48, "view_sites": 38,
        "fixed_style_calls": 84, "controlled_native_wrapper_cases": 168,
        "native_tile_argument_traces": 852, "native_pixel_contract_cases": 22,
        "all_fixed_source_tiles_outside_five_miniature_cells": True,
        "source_XYWH_distinguished_from_destination_LTRB": True,
        "zero_size_source_descriptor_can_fill_from_one_pixel": True,
        "computed_aliased_owners_indirect_calls_and_embedded_readers_remain_open": True,
        "ordinary_five_miniature_and_Confirm_contexts_remain_open": True,
        "controlled_binding_and_row_alias_ABI_assumptions_retained": True,
        "wording_lead_percent_s_Admiral_requires_context_review": True,
        "archive": str(ARCHIVE), "ordinary_gameplay_screenshots": 0,
        "production_ROM_and_patch_changed": False,
        "all18_plaques_remain_incomplete": True,
        "all22_historical_objects_retained": True, "full_goal_complete": False,
    }
    snapshot = json.loads(Path("work/analysis/confirm_material_v572/audit_scope_before.json").read_text(encoding="utf-8"))
    for filename, saved in snapshot.items():
        path = Path("translations") / filename
        d = json.loads(path.read_text(encoding="utf-8-sig"))
        assert d.get("historical_pending_items_retained") == saved["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == saved["ongoing_plaque_inventory"]
        d[KEY] = record
        d["current_goal_turn_classification"] = "progress-original-frame-contracts-and-complete-literal-caller-reconciliation"
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reread = json.loads(path.read_text(encoding="utf-8"))
        assert reread.get("historical_pending_items_retained") == saved["historical_pending_items_retained"]
        assert reread.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == saved["ongoing_plaque_inventory"]
    paragraph = """

## V584: original frame drawing contracts and literal caller reconciliation

All48 literal frame-owner references resolve to38 view sites, eight getters and
two initialization sites. All84 fixed style calls resolve;168 original native
wrapper cases trace852 tiles outside Done/Rank/Cancel/Pick Cargo/Pick Ship.
Twenty-two original native pixel cases verify source/destination contracts,
clipping, banks0/9 and zero-size one-pixel fills. Source rows216/224 have checked
dominating stores with explicit no-alias/callee-ABI assumptions. No ordinary
caption parent is established: investigate computed/aliased owners, indirect
calls or embedded-copy readers next. Retain the inherited `%s Admiral` wording
lead for actual-context review. Source projections and hashed proofs are on E
under Test fixtures/V584 Frame source contracts; no new gameplay screenshot or
guide credit. V581 ROM/patch unchanged. All18 plaques remain incomplete and all22
historical objects retain their exact scope. The graphics goal remains active.
See [V584 source-contract checkpoint](frame_source_contracts_v584_checkpoint.md).
"""
    for name in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        path = Path("docs") / name
        text = path.read_text(encoding="utf-8-sig")
        if "## V584: original frame drawing contracts and literal caller reconciliation" not in text:
            path.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V584 in three audits/four progress documents; archived eight proofs/projections;18/22 retained exactly;V581 unchanged.")


if __name__ == "__main__":
    main()
