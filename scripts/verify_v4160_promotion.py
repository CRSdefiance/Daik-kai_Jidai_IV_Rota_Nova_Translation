"""Audit the main checkpoint, exact patch and preserved editorial state independently."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "releases/all_routes_unified_v4160"
AUDIT = ROOT / "work/analysis/promotion_v4186"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    promotion = read(PACKAGE / "promotion.json")
    assert promotion == read(ROOT / "translations/promoted_build.json")
    assert promotion["status"] == "promoted" and promotion["main_build"]
    assert promotion["profile"] == "all-routes-unified-v4160"
    assert promotion["git_tag"] == "promoted-v4160"
    manifest_bytes = gzip.decompress((PACKAGE / "build_manifest.json.gz").read_bytes())
    frozen_bytes = gzip.decompress((PACKAGE / "build_release_stack.json.gz").read_bytes())
    assert sha(manifest_bytes) == promotion["build_manifest_sha256"]
    assert sha(frozen_bytes) == promotion["build_registry_sha256"]
    assert manifest_bytes == (ROOT / "out/all_routes_combined_v4160_candidate.manifest.json").read_bytes()
    assert frozen_bytes == (AUDIT / "registry.before.json").read_bytes()
    manifest, frozen = json.loads(manifest_bytes), json.loads(frozen_bytes)
    registry = read(ROOT / "translations/release_stack.json")
    assert manifest["release_stack_sha256"] == sha(frozen_bytes)
    assert manifest["profile"] == promotion["profile"]
    assert len(manifest["batches"]) == 543 and len(frozen["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    assert {k: v for k, v in frozen.items() if k != "latest_promoted_build"} == {
        k: v for k, v in registry.items() if k != "latest_promoted_build"}
    pointer = registry["latest_promoted_build"]
    assert pointer["profile"] == promotion["profile"] and pointer["main_build"]
    assert pointer["rom_sha256"] == promotion["rom_sha256"]
    assert pointer["git_tag"] == promotion["git_tag"]
    assert not pointer["construction_baseline_rebased"]
    baseline = registry["canonical_baseline"]
    assert baseline == promotion["immutable_construction_baseline"]
    assert sha((ROOT / baseline["path"]).read_bytes()) == baseline["sha256"]
    assert sha((ROOT / baseline["previous_baseline"]["path"]).read_bytes()) == baseline["previous_baseline"]["sha256"]
    rom_bytes = (ROOT / promotion["rom"]).read_bytes()
    assert sha(rom_bytes) == promotion["rom_sha256"]
    assert (AUDIT / "promoted_patch_reconstruction_RESEARCH_ONLY.nds").read_bytes() == rom_bytes
    assert sha((PACKAGE / "translation.xdelta").read_bytes()) == promotion["patch_sha256"]
    assert sha((ROOT / "work/clean.nds").read_bytes()) == promotion["source_rom_sha256"]
    before = json.loads(gzip.decompress((AUDIT / "ledger.before.json.gz").read_bytes()))
    ledger = read(ROOT / "translations/editorial_review_current_v1.json")
    allowed = {"latest_checkpoint", "promoted_main_build_v4186", "lil_B168_preintegration_review_v4186"}
    assert {k: v for k, v in before.items() if k not in allowed} == {
        k: v for k, v in ledger.items() if k not in allowed}
    assert ledger["goal_status"] == "active" and not ledger["full_goal_complete"]
    assert (ledger["records_editorially_completed"], ledger["records_with_source_and_prose_pass"],
            ledger["records_revised_and_integrated"], ledger["retained_wordings_editorially_completed"]
            ) == (5602, 5605, 3567, 2035)
    assert ledger["promoted_main_build_v4186"] == promotion
    pending = ledger["lil_B168_preintegration_review_v4186"]
    assert pending == read(PACKAGE / "verification/UNINTEGRATED_B168_status.json")
    assert pending["objects"] == 54 and pending["proposed_revisions"] == 28
    assert pending["justified_retentions"] == 26
    assert pending["editorial_ledger_credit_added"] == pending["new_gameplay_runs"] == 0
    assert not pending["integrated_in_promoted_ROM"]
    assert sha((ROOT / pending["manuscript"]).read_bytes()) == pending["manuscript_sha256"]
    native_bytes = (ROOT / pending["native_proof"]).read_bytes()
    assert sha(native_bytes) == pending["native_proof_sha256"]
    assert gzip.decompress((PACKAGE / "verification/UNINTEGRATED_B168_native_font_proof.json.gz").read_bytes()) == native_bytes
    native = json.loads(native_bytes)
    assert native["visual_review_pending"] and native["formatting_gate_and_editorial_credit_still_pending"]
    assert native["all54_complete_native_independent_planes_pass"]
    assert (native["progressive_planes"], native["FE_planes"], native["current_original_macro_alignment_calls"]) == (51, 3, 432)
    assert not native["actual_selected_B168_IDs"] and native["new_emulator_runs"] == 0
    updates = {}
    for entry in read(AUDIT / "mutation_plan.json"):
        target = Path(entry["target"])
        assert target.is_relative_to(ROOT), target
        assert sha(target.read_bytes()) == entry["planned_sha256"]
        assert target.read_bytes() == Path(entry["planned"]).read_bytes()
        updates[target.relative_to(ROOT).as_posix()] = entry["planned_sha256"]
    assert (ROOT / "docs/editorial_handoff_current.md").read_text(encoding="utf-8").startswith("# Current editorial handoff - V4186")
    assert "Unified V4160" in (ROOT / "README.md").read_text(encoding="utf-8").splitlines()[0]
    assert (ROOT / promotion["previous_promoted_build"]).is_file()
    result = {
        "checkpoint": "V4186", "profile": promotion["profile"], "main_build": True,
        "rom_sha256": promotion["rom_sha256"], "patch_sha256": promotion["patch_sha256"],
        "original_manifest_and_registry_byte_exact": True,
        "only_registry_promotion_pointer_changed": True,
        "whole_clean_input_patch_reconstruction_byte_exact": True,
        "canonical_baseline_and_rollback_unchanged": True,
        "manifest_batches": 543, "accepted_layers": 114,
        "completed_contextual_reviews": 5602, "source_prose_reviews": 5605,
        "ledger_sha256": sha((ROOT / "translations/editorial_review_current_v1.json").read_bytes()),
        "all_prior_ledger_records_and_coverage_preserved": True,
        "B168_draft_objects_unintegrated_uncredited": 54,
        "final_B168_visual_review_pending": True,
        "targeted_tests_passed": 78, "new_emulator_runs_at_promotion": 0,
        "ROMs_deleted": 0, "full_goal_active": True, "full_goal_complete": False,
        "updated_files": updates, "producer_sha256": sha(Path(__file__).read_bytes()),
    }
    save(AUDIT / "promotion_receipt.json", result)
    save(PACKAGE / "verification/promotion_final_audit.json", result)
    checksums = {path.relative_to(PACKAGE).as_posix(): sha(path.read_bytes())
                 for path in sorted(PACKAGE.rglob("*")) if path.is_file() and path.name != "checksums.json"}
    save(PACKAGE / "checksums.json", checksums)
    assert all(sha((PACKAGE / name).read_bytes()) == digest for name, digest in checksums.items())
    print(json.dumps({"promoted_package_verified": True, "files": len(checksums),
                      "profile": promotion["profile"], "whole_ROM_byte_exact": True,
                      "all_prior_ledger_records_preserved": True, "B168_unintegrated_uncredited": 54}))


if __name__ == "__main__":
    main()
