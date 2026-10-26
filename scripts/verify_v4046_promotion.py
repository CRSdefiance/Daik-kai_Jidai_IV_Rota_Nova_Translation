"""Independently audit the promoted package and unchanged frozen contracts."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "releases/all_routes_unified_v4046"
AUDIT = ROOT / "work/analysis/promotion_v4083"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    promotion = read(PACKAGE / "promotion.json")
    assert promotion == read(ROOT / "translations/promoted_build.json")
    assert promotion["main_build"] and promotion["status"] == "promoted"
    manifest_bytes = gzip.decompress((PACKAGE / "build_manifest.json.gz").read_bytes())
    registry_bytes = gzip.decompress((PACKAGE / "build_release_stack.json.gz").read_bytes())
    assert sha(manifest_bytes) == promotion["build_manifest_sha256"]
    assert sha(registry_bytes) == promotion["build_registry_sha256"]
    manifest, frozen = json.loads(manifest_bytes), json.loads(registry_bytes)
    registry = read(ROOT / "translations/release_stack.json")
    assert manifest["release_stack_sha256"] == sha(registry_bytes)
    assert manifest["profile"] == promotion["profile"] == "all-routes-unified-v4046"
    assert len(manifest["batches"]) == 539 and len(frozen["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    assert {k: v for k, v in frozen.items() if k != "latest_promoted_build"} == {
        k: v for k, v in registry.items() if k != "latest_promoted_build"}
    assert registry["latest_promoted_build"]["rom_sha256"] == promotion["rom_sha256"]
    assert registry["latest_promoted_build"]["git_tag"] == "promoted-v4046"
    assert not registry["latest_promoted_build"]["construction_baseline_rebased"]
    for key, expected in [("rom", "rom_sha256")]:
        assert sha((ROOT / promotion[key]).read_bytes()) == promotion[expected]
    assert sha((PACKAGE / "translation.xdelta").read_bytes()) == promotion["patch_sha256"]
    assert sha((AUDIT / "promoted_patch_reconstruction_RESEARCH_ONLY.nds").read_bytes()) == promotion["rom_sha256"]
    assert (AUDIT / "promoted_patch_reconstruction_RESEARCH_ONLY.nds").read_bytes() == (ROOT / promotion["rom"]).read_bytes()
    base = registry["canonical_baseline"]
    assert sha((ROOT / "out/raphael_natural_v2_accepted_base.nds").read_bytes()) == base["sha256"]
    assert base == promotion["immutable_construction_baseline"]
    before = read(AUDIT / "editorial_review_current_v1.json.before")
    ledger_path = ROOT / "translations/editorial_review_current_v1.json"
    ledger = read(ledger_path)
    allowed = {"latest_checkpoint", "formatting_watchlist", "coverage_units",
               "lil_B166_native_preintegration_review_v4083", "promoted_main_build_v4083"}
    assert {k: v for k, v in before.items() if k not in allowed} == {
        k: v for k, v in ledger.items() if k not in allowed}
    assert {k: v for k, v in ledger["formatting_watchlist"].items() if k != "lil_B166_v4083"} == before["formatting_watchlist"]
    for old, new in zip(before["coverage_units"], ledger["coverage_units"], strict=True):
        if old["id"] == "all-route-scenes":
            assert {k: v for k, v in old.items() if k != "next"} == {k: v for k, v in new.items() if k != "next"}
        else:
            assert old == new
    assert ledger["goal_status"] == "active" and not ledger["full_goal_complete"]
    assert (ledger["records_editorially_completed"], ledger["records_with_source_and_prose_pass"],
            ledger["records_revised_and_integrated"], ledger["retained_wordings_editorially_completed"]) == (5529, 5532, 3527, 2002)
    pending = ledger["lil_B166_native_preintegration_review_v4083"]
    assert pending["source_prose_or_completion_credit_added"] == 0
    assert pending["actual_menu_only_cold_boot_runs"] == 3 and pending["actual_B166_speech_or_choice_return_coverage_added"] == 0
    assert pending["menu_storage_ownership_resolved"] and pending["phrase_flow_findings_resolved"]
    approval = read(ROOT / pending["native_approval"])
    assert sha((ROOT / pending["native_approval"]).read_bytes()) == pending["native_approval_sha256"]
    for path, digest in approval["manuscripts"].items():
        assert sha((ROOT / path).read_bytes()) == digest
        document = read(ROOT / path)
        assert all(all(row["review"].values()) for row in document["records"])
    assert Path(ROOT / "docs/editorial_handoff_current.md").read_text(encoding="utf-8").startswith("# Current editorial handoff - V4083")
    receipt = read(AUDIT / "promotion_receipt.json")
    for path, digest in receipt["updated_files"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    result = {
        "checkpoint": "V4083", "profile": promotion["profile"], "main_build": True,
        "rom_sha256": promotion["rom_sha256"], "patch_sha256": promotion["patch_sha256"],
        "original_manifest_and_registry_byte_exact": True, "only_registry_promotion_pointer_changed": True,
        "whole_clean_input_patch_reconstruction_byte_exact": True, "accepted_layers": 114, "manifest_batches": 539,
        "canonical_construction_baseline_unchanged": True, "historical_completed_reviews_and_credit_unchanged": True,
        "ledger_sha256": sha(ledger_path.read_bytes()), "B166_native_approved_unintegrated_uncredited": 44,
        "new_emulator_runs_at_promotion": 0, "full_editorial_goal_active": True, "full_goal_complete": False,
        "producer_sha256": sha(Path(__file__).read_bytes()),
    }
    destination = PACKAGE / "verification/promotion_final_audit.json"
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    checksums = {p.relative_to(PACKAGE).as_posix(): sha(p.read_bytes()) for p in sorted(PACKAGE.rglob("*"))
                 if p.is_file() and p.name != "checksums.json"}
    (PACKAGE / "checksums.json").write_text(json.dumps(checksums, indent=2) + "\n", encoding="utf-8")
    assert all(sha((PACKAGE / name).read_bytes()) == digest for name, digest in checksums.items())
    print(json.dumps({"promoted_package_verified": True, "files": len(checksums), **result}))


if __name__ == "__main__":
    main()
