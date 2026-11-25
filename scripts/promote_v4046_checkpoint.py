"""Promote the user's current verified build, retaining frozen construction inputs."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "releases/all_routes_unified_v4046"
AUDIT = ROOT / "work/analysis/promotion_v4083"
PROFILE = "all-routes-unified-v4046"
ROM_SHA = "6b991313e0f31e72b2548b7fd024ca406b710f61d56ddc35c06e147a443e4913"
PATCH_SHA = "56f13528927f23cd5c72f45fde79fbed58ab6d463d0ad2c916e149fc4b66c971"
MANIFEST_SHA = "bcdfb3b40dbd156214d92b6fed3c30e80f9be94ae02e455d3f6091eba37db4eb"
CLEAN_SHA = "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
BASE_SHA = "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
REGISTRY_SHA = "ce97bb65d41c0feb19246b5b8418551a2f25345d3aba2e3dbc28e6640c5f40ab"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    assert Path.cwd() == ROOT
    assert not RELEASE.exists() and not AUDIT.exists(), "Preserve existing promotion artifacts"
    rom = ROOT / "out/all_routes_combined_v4046_candidate.nds"
    patch = rom.with_suffix(".xdelta")
    manifest = rom.with_suffix(".manifest.json")
    registry_path = ROOT / "translations/release_stack.json"
    ledger_path = ROOT / "translations/editorial_review_current_v1.json"
    clean = ROOT / "work/clean.nds"
    baseline = ROOT / "out/raphael_natural_v2_accepted_base.nds"
    for path, expected in [(rom, ROM_SHA), (patch, PATCH_SHA), (manifest, MANIFEST_SHA),
                           (clean, CLEAN_SHA), (baseline, BASE_SHA), (registry_path, REGISTRY_SHA)]:
        assert sha(path.read_bytes()) == expected, str(path)
    build, registry, ledger = map(read, [manifest, registry_path, ledger_path])
    assert build["profile"] == PROFILE and build["release_stack_sha256"] == REGISTRY_SHA
    assert len(build["batches"]) == 539 and len(registry["accepted_layers"]) == 114
    assert all(build["checks"].values()) and registry["canonical_baseline"]["sha256"] == BASE_SHA
    assert registry["latest_promoted_build"]["profile"] == "all-routes-unified-v1492"
    prior = ROOT / "work/analysis/editorial_handoff_verification_v4073/verified_handoff.json"
    assert sha(ledger_path.read_bytes()) == read(prior)["ledger_sha256"]
    assert ledger["records_editorially_completed"] == 5529 and not ledger["full_goal_complete"]
    assert ledger["goal_status"] == "active"
    release_proof = ROOT / "work/analysis/lil_B165_release_v4047/registered_release_verification.json"
    startup = ROOT / "work/analysis/lil_B165_startup_v4049/cold_boot_Lil_startup_town_verification.json"
    visual = ROOT / "work/analysis/lil_B165_startup_v4049/current_six_frame_visual_review.json"
    completion = ROOT / "work/analysis/lil_B165_completion_v4050/completion_receipt.json"
    approval = ROOT / "work/analysis/lil_B166_native_approval_v4082/approval_receipt.json"
    proof, boot, view, complete, native = map(read, [release_proof, startup, visual, completion, approval])
    assert proof["whole_ROM_reconstruction_byte_exact"] and proof["candidate_sha256"] == ROM_SHA
    assert proof["patch_sha256"] == PATCH_SHA and proof["manifest_sha256"] == MANIFEST_SHA
    assert boot["candidate_sha256"] == ROM_SHA and boot["paired_frame_count"] == 31
    assert boot["all_current_requested_and_final_framebuffers_equal_V4002"]
    assert boot["all_five_postload_actor_model_and_captain_checks_equal"]
    assert view["viewed"] and view["no_new_display_finding"]
    for path, expected in complete["evidence"].items():
        assert sha(Path(path).read_bytes()) == expected, path
    for path, expected in native["manuscripts"].items():
        assert sha(Path(path).read_bytes()) == expected, path
        assert all(all(r["review"].values()) for r in read(Path(path))["records"])
    assert native["new_source_prose_reviews"] == native["new_completed_records"] == 0
    assert native["revised"] == 24 and native["retained"] == 20
    assert native["actual_menu_only_cold_boot_runs"] == 3
    assert native["actual_B166_speech_or_choice_return_coverage_added"] == 0
    assert native["relocation_references_story_representative_registered_release_pending"]
    assert sha(Path(native["merged_native_proof"]).read_bytes()) == native["merged_native_proof_sha256"]
    for sheet in [*native["review_sheets"], native["choice_review_sheet"], native["actual_menu_review_sheet"]]:
        assert sha(Path(sheet["path"]).read_bytes()) == sheet["sha256"]

    AUDIT.mkdir(parents=True)
    docs = [ROOT / "docs" / name for name in ["editorial_handoff_current.md", "translation_progress.md",
            "editorial_review_goal.md", "todo.md", "known_issues.md", "release_build.md"]]
    for path in [ledger_path, registry_path, ROOT / "translations/promoted_build.json", ROOT / "README.md", *docs]:
        shutil.copyfile(path, AUDIT / (path.name + ".before"))
    reconstruction = AUDIT / "promoted_patch_reconstruction_RESEARCH_ONLY.nds"
    apply_xdelta(clean, patch, reconstruction)
    assert reconstruction.read_bytes() == rom.read_bytes()
    RELEASE.mkdir(parents=True)
    shutil.copyfile(patch, RELEASE / "translation.xdelta")
    (RELEASE / "build_manifest.json.gz").write_bytes(gzip.compress(manifest.read_bytes(), mtime=0))
    (RELEASE / "build_release_stack.json.gz").write_bytes(gzip.compress(registry_path.read_bytes(), mtime=0))
    verification = RELEASE / "verification"
    verification.mkdir()
    evidence_files = [(release_proof, "registered_release_verification.json"),
                      (startup, "cold_boot_Lil_startup_town_verification.json"),
                      (visual, "current_six_frame_visual_review.json"),
                      (completion, "B165_completion_receipt.json"),
                      (prior, "historical_V4072_handoff_verification.json"),
                      (ROOT / "work/analysis/editorial_handoff_verification_v4051/verified_handoff.json", "B165_verified_handoff.json"),
                      (approval, "UNINTEGRATED_B166_native_approval.json"),
                      (Path(native["merged_native_proof"]), "UNINTEGRATED_B166_native_reconciliation.json")]
    for source, name in evidence_files:
        shutil.copyfile(source, verification / name)
    shutil.copyfile(Path(view["sheet"]), verification / "current_Lil_startup_and_town_review.png")
    save(verification / "promotion_reconstruction.json", {
        "clean_input_sha256": CLEAN_SHA, "patch_sha256": PATCH_SHA, "candidate_sha256": ROM_SHA,
        "reconstructed_sha256": sha(reconstruction.read_bytes()), "whole_ROM_byte_exact": True,
        "new_emulator_runs_at_promotion": 0, "original_build_registry_sha256": REGISTRY_SHA,
        "producer": "scripts/promote_v4046_checkpoint.py", "producer_sha256": sha(Path(__file__).read_bytes()),
    })
    open_scope = ("Full contextual editorial review remains active across remaining storylines, shared shop/town "
                  "dialogue, random scenes and other player-facing prose. B166's 44 native-approved objects are "
                  "unintegrated and uncredited. COMMON 750-752, canonical Maria SC3 B97, wider prose leads, "
                  "the separate graphics/all 18 plaques work and later older-record technical re-audit remain open.")
    promotion = {
        "format": "dk4-promoted-checkpoint-v1", "status": "promoted", "main_build": True,
        "promoted_on": "2026-10-26",
        "user_request": "lets promote our current build as our new main build and then commit/push to github",
        "profile": PROFILE, "rom": "out/all_routes_combined_v4046_candidate.nds", "rom_sha256": ROM_SHA,
        "release_directory": "releases/all_routes_unified_v4046", "git_tag": "promoted-v4046",
        "patch_sha256": PATCH_SHA, "source_rom_sha256": CLEAN_SHA, "build_manifest_sha256": MANIFEST_SHA,
        "build_registry_sha256": REGISTRY_SHA, "immutable_construction_baseline": registry["canonical_baseline"],
        "previous_promoted_build": "releases/all_routes_unified_v1492/promotion.json",
        "promotion_scope": "User-designated main cumulative build checkpoint; preserve the immutable construction baseline, frozen builders and source/hash contracts. Buildable profile status remains experimental under the registry schema; this promotion record designates the main build.",
        "known_open_scope": open_scope, "complete_entries": 5529, "source_prose_reviewed_entries": 5532,
        "reviewed_incomplete_COMMON_entries": 3, "unintegrated_uncredited_B166_objects": 44,
        "full_editorial_goal_complete": False, "full_graphics_goal_complete": False,
        "new_user_cold_boot_test_claimed": False, "new_emulator_runs_at_promotion": 0,
        "construction_baseline_rebased": False,
    }
    save(RELEASE / "promotion.json", promotion)
    save(ROOT / "translations/promoted_build.json", promotion)
    registry["latest_promoted_build"] = {
        "status": "promoted", "main_build": True, "profile": PROFILE, "rom_sha256": ROM_SHA,
        "record": "translations/promoted_build.json", "git_tag": "promoted-v4046",
        "construction_baseline_rebased": False,
    }
    save(registry_path, registry)
    save(RELEASE / "release_manifest.json", {
        "game": "Daikoukai Jidai IV / Rota Nova DS", "patch_version": "unified-v4046",
        "status": "promoted", "main_build": True, "profile": PROFILE, "source_rom_sha256": CLEAN_SHA,
        "modified_rom_sha256": ROM_SHA, "patch_sha256": PATCH_SHA, "full_graphics_goal_complete": False,
        "full_editorial_goal_complete": False, "promotion_record": "promotion.json", "notes": open_scope,
    })
    next_work = ("B166 native approval V4082b is complete. Reconcile pending ledger credit, then complete "
                 "relocation/stored references, representative source/English speech, accepted menu choices and "
                 "transitions, a registered cumulative build, exact clean-input patch and startup checks. "
                 "The three menu-only cold boots establish complete captions/highlights and backing ownership; "
                 "they do not establish B166 speech, actual choice return, recruitment or natural eligibility. "
                 "Continue B167-B180 and the complete wider editorial objective.")
    pending = {
        "status": "44-native-approved;unintegrated;uncredited;pending-relocation-story-references-release",
        "native_approval": str(approval.relative_to(ROOT)), "native_approval_sha256": sha(approval.read_bytes()),
        "manuscripts": native["manuscripts"], "proposed_revisions": 24, "justified_retentions": 20,
        "speech_objects": 42, "typed_choice_labels": 2, "source_prose_or_completion_credit_added": 0,
        "progressive_planes": 42, "macro_alignment_cases": 336, "actual_menu_only_cold_boot_runs": 3,
        "actual_B166_speech_or_choice_return_coverage_added": 0, "menu_storage_ownership_resolved": True,
        "synthetic_mismatch_was_probe_backing_geometry": True, "phrase_flow_findings_resolved": True,
        "next": next_work, "full_goal_complete": False,
    }
    ledger["lil_B166_native_preintegration_review_v4083"] = pending
    ledger["formatting_watchlist"]["lil_B166_v4083"] = pending
    ledger["promoted_main_build_v4083"] = promotion
    for unit in ledger["coverage_units"]:
        if unit["id"] == "all-route-scenes":
            unit["next"] = next_work
    summary = ("V4083 promotes verified V4046 as the user's new main cumulative build and preserves V1492 "
               "as an earlier checkpoint. The canonical construction baseline and all frozen source contracts "
               "remain unchanged. 539 manuscript batches/114 accepted layers; clean-input patch reconstructs "
               "the entire ROM byte for byte. Existing registered opening/town and representative B165 evidence "
               "are retained; promotion adds no gameplay claim. B166's 42 speeches and two labels have native "
               "approval V4082b, with 24 revisions and 20 justified retentions, but remain unintegrated and "
               "uncredited. The earlier phrase-flow and synthetic menu-backing findings are resolved by the "
               "final native proof and three focused menu-only boots. Actual B166 speech/choice return and "
               "relocation/release checks remain pending. Counters remain 5529 fresh rereads/integrated, zero "
               "credited route records pending; source/prose 5532, historical 3527 revised/2002 retained. "
               "The separate 44 B166 objects await pending-credit reconciliation. Remaining B167-B180:348 "
               "physical speeches and one choice-command lead; neither is a full project denominator. " + open_scope)
    ledger["latest_checkpoint"] = summary
    save(ledger_path, ledger)
    section = ("## V4083: V4046 promoted as the main build; B166 native review preserved\n\n" + summary +
               "\n\nROM SHA-256: `" + ROM_SHA + "`. Clean-input patch SHA-256: `" + PATCH_SHA +
               "`. Main build: [Unified V4046](../releases/all_routes_unified_v4046/README.md). "
               "The original build-time registry is packaged byte-exactly; the current registry differs only "
               "in its promotion pointer. Earlier sections are historical checkpoints.\n\nNext: " + next_work + "\n\n")
    for index, path in enumerate(docs):
        first, rest = path.read_text(encoding="utf-8").split("\n", 1)
        path.write_text(("# Current editorial handoff - V4083" if index == 0 else first) +
                        "\n\n" + section + rest, encoding="utf-8", newline="\n")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace(text.splitlines()[0], "> Main promoted build: [Unified V4046](releases/all_routes_unified_v4046/README.md) (2026-10-26). Full editorial and graphics reviews remain active.", 1)
    text = text.replace("The latest experimental combined patch is [Unified V245](releases/all_routes_unified_v245/README.md).",
                        "The current main combined patch is [Unified V4046](releases/all_routes_unified_v4046/README.md).\nEarlier [V1492](releases/all_routes_unified_v1492/README.md) and [V245](releases/all_routes_unified_v245/README.md) checkpoints remain available.")
    readme.write_text(text, encoding="utf-8", newline="\n")
    ignore = ROOT / ".gitignore"
    text = ignore.read_text(encoding="utf-8")
    assert "!releases/all_routes_unified_v4046/*.xdelta" not in text
    text = text.replace("!releases/all_routes_unified_v1492/*.xdelta", "!releases/all_routes_unified_v1492/*.xdelta\n!releases/all_routes_unified_v4046/*.xdelta")
    ignore.write_text(text, encoding="utf-8", newline="\n")
    save(AUDIT / "promotion_receipt.json", {
        "checkpoint": "V4083", "profile": PROFILE, "candidate_sha256": ROM_SHA,
        "patch_sha256": PATCH_SHA, "before_ledger_sha256": read(prior)["ledger_sha256"],
        "updated_files": {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in [ledger_path, registry_path, *docs]},
        "B166": pending, "source_prose_credit_added": 0, "completion_credit_added": 0,
        "canonical_baseline_unchanged": sha(baseline.read_bytes()) == BASE_SHA,
        "whole_clean_input_patch_reconstruction_exact": True, "full_goal_active": True,
    })
    print(json.dumps({"promoted": PROFILE, "main_build": True, "rom_sha256": ROM_SHA,
                      "patch_sha256": PATCH_SHA, "whole_ROM_reconstruction_byte_exact": True,
                      "construction_baseline_rebased": False, "B166_unintegrated_uncredited": 44}))


if __name__ == "__main__":
    main()
