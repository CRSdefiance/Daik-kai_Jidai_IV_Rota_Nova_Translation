"""Stage the explicitly requested main-checkpoint promotion; preserve frozen inputs."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "work/analysis/promotion_v4186"
PACKAGE = ROOT / "releases/all_routes_unified_v4160"
PROFILE = "all-routes-unified-v4160"
ROM_SHA = "22fb73b7067fc9c5f7f59383efdf9fabc233cff3d6a0391092a7a690959f3425"
PATCH_SHA = "854fe3cf7229a829e76c9388807e0cea04ee874ca8a903cb14ebce7c320f7763"
REGISTRY_SHA = "3c0853650a34310a81b0ff02e87a31ed72ab4157fa00c646a2be6f0735fb8b18"
MANIFEST_SHA = "67d7a6bae76be88c10364a31352a0ad2c5ad9f940c84c34c7a437cd16da2a090"
CLEAN_SHA = "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
BASE_SHA = "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
B168_PROOF = "work/analysis/lil_B168_fonts_v4185/all54_native_planes432_macro_cases_and26_consumer_negatives.json"
B168_MANUSCRIPT = "translations/lil_B168_editorial_manuscript_v6.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def save(path: Path, value: object) -> None:
    path.write_bytes(encoded(value))


def main() -> None:
    assert Path.cwd() == ROOT
    assert not AUDIT.exists() and not PACKAGE.exists(), "Preserve prior artifacts"
    rom = ROOT / "out/all_routes_combined_v4160_candidate.nds"
    patch = rom.with_suffix(".xdelta")
    manifest = rom.with_suffix(".manifest.json")
    registry_path = ROOT / "translations/release_stack.json"
    ledger_path = ROOT / "translations/editorial_review_current_v1.json"
    clean = ROOT / "work/clean.nds"
    base = ROOT / "out/raphael_natural_v2_accepted_base.nds"
    for path, digest in [(rom, ROM_SHA), (patch, PATCH_SHA), (manifest, MANIFEST_SHA),
                         (registry_path, REGISTRY_SHA), (clean, CLEAN_SHA), (base, BASE_SHA)]:
        assert sha(path.read_bytes()) == digest, str(path)
    build, registry, ledger = map(read, [manifest, registry_path, ledger_path])
    assert build["profile"] == PROFILE and build["release_stack_sha256"] == REGISTRY_SHA
    assert len(build["batches"]) == 543 and len(registry["accepted_layers"]) == 114
    assert all(build["checks"].values()) and registry["canonical_baseline"]["sha256"] == BASE_SHA
    assert registry["latest_promoted_build"]["profile"] == "all-routes-unified-v4046"
    handoff = ROOT / "work/analysis/editorial_handoff_verification_v4165/verified_handoff.json"
    assert sha(ledger_path.read_bytes()) == read(handoff)["ledger_sha256"]
    assert ledger["records_editorially_completed"] == 5602
    assert ledger["records_with_source_and_prose_pass"] == 5605
    assert ledger["goal_status"] == "active" and not ledger["full_goal_complete"]
    release = ROOT / "work/analysis/lil_B167_release_v4161/registered_release_verification.json"
    startup = ROOT / "work/analysis/lil_B167_startup_v4163/cold_boot_Lil_startup_town_verification.json"
    visual = startup.parent / "current_six_frame_visual_review.json"
    completion = ROOT / "work/analysis/lil_B167_completion_v4164/completion_receipt.json"
    proof, boot, view, completed = map(read, [release, startup, visual, completion])
    assert proof["whole_ROM_reconstruction_byte_exact"] and proof["candidate_sha256"] == ROM_SHA
    assert proof["patch_sha256"] == PATCH_SHA and proof["manifest_sha256"] == MANIFEST_SHA
    assert boot["candidate_sha256"] == ROM_SHA and boot["paired_frame_count"] == 31
    assert boot["all_current_requested_and_final_framebuffers_equal_V4110"]
    assert boot["all_five_postload_actor_model_and_captain_checks_equal"]
    assert view["viewed"] and view["no_new_display_finding"]
    assert sha((ROOT / view["sheet"]).read_bytes()) == view["sha256"]
    for path, digest in completed["evidence"].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    native = read(ROOT / B168_PROOF)
    assert native["all54_complete_native_independent_planes_pass"]
    assert native["visual_review_pending"] and native["new_emulator_runs"] == 0
    assert sha((ROOT / B168_MANUSCRIPT).read_bytes()) == native["manuscript_sha256"]
    assert len(read(ROOT / B168_MANUSCRIPT)["records"]) == 54

    AUDIT.mkdir(parents=True)
    reconstruction = AUDIT / "promoted_patch_reconstruction_RESEARCH_ONLY.nds"
    apply_xdelta(clean, patch, reconstruction)
    assert reconstruction.read_bytes() == rom.read_bytes()
    PACKAGE.mkdir(parents=True)
    verification = PACKAGE / "verification"
    verification.mkdir()
    shutil.copyfile(patch, PACKAGE / "translation.xdelta")
    (PACKAGE / "build_manifest.json.gz").write_bytes(gzip.compress(manifest.read_bytes(), mtime=0))
    (PACKAGE / "build_release_stack.json.gz").write_bytes(gzip.compress(registry_path.read_bytes(), mtime=0))
    (AUDIT / "ledger.before.json.gz").write_bytes(gzip.compress(ledger_path.read_bytes(), mtime=0))
    (AUDIT / "registry.before.json").write_bytes(registry_path.read_bytes())
    for source, name in [(release, "registered_release_verification.json"),
                         (startup, "cold_boot_Lil_startup_town_verification.json"),
                         (visual, "current_six_frame_visual_review.json"),
                         (completion, "B167_completion_receipt.json"),
                         (handoff, "B167_verified_handoff.json")]:
        shutil.copyfile(source, verification / name)
    shutil.copyfile(ROOT / view["sheet"], verification / "current_Lil_startup_and_town_review.png")
    save(verification / "promotion_reconstruction.json", {
        "clean_input_sha256": CLEAN_SHA, "patch_sha256": PATCH_SHA, "candidate_sha256": ROM_SHA,
        "reconstructed_sha256": sha(reconstruction.read_bytes()), "whole_ROM_byte_exact": True,
        "new_emulator_runs_at_promotion": 0, "original_build_registry_sha256": REGISTRY_SHA,
        "producer": "scripts/promote_v4160_checkpoint.py", "producer_sha256": sha(Path(__file__).read_bytes()),
    })
    save(verification / "promotion_test_results.json", {
        "command": "python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q",
        "result": "78 passed in 5.73s", "exit_code": 0, "new_emulator_runs": 0,
    })
    pending = {
        "objects": 54, "proposed_revisions": 28, "justified_retentions": 26,
        "status": "draft-review;native-font-checks-pass;visual-approval-and-integration-pending",
        "manuscript": B168_MANUSCRIPT, "manuscript_sha256": native["manuscript_sha256"],
        "native_proof": B168_PROOF, "native_proof_sha256": sha((ROOT / B168_PROOF).read_bytes()),
        "native_planes": 54, "progressive_planes": 51, "FE_planes": 3,
        "logical_compiled_alignment_cases": 432, "new_gameplay_runs": 0,
        "editorial_ledger_credit_added": 0, "integrated_in_promoted_ROM": False,
        "visual_resume": "Freshly view final V4185 sheets 1,2,3,4,6; the previous multi-image output was truncated. Sheets 5/7 are byte-identical to viewed V4182b originals. Then native approval, ledger reconciliation, relocation/stored references, representative gameplay, registered cumulative release and startup checks remain.",
        "native_approval_next_free_checkpoint": "V4187 or later; V4186 is this promotion",
        "full_goal_complete": False,
    }
    save(verification / "UNINTEGRATED_B168_status.json", pending)
    (verification / "UNINTEGRATED_B168_native_font_proof.json.gz").write_bytes(
        gzip.compress((ROOT / B168_PROOF).read_bytes(), mtime=0))
    open_scope = ("Full contextual editorial review remains active across every remaining storyline, shared shop/town dialogue, random scene, Help and other player-facing prose. B168's 54 draft-reviewed objects remain unintegrated and uncredited. Preserve COMMON 750-752, canonical Maria SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell's full-catalogue middle-field lead, B157 provenance amendment, separate graphics/all 18 plaques and the later older-record technical re-audit/queued 0D gap.")
    promotion = {
        "format": "dk4-promoted-checkpoint-v1", "status": "promoted", "main_build": True,
        "promoted_on": "2026-10-26", "checkpoint": "V4186",
        "user_request": "lets promote our current build as our new main build and then commit/push to github",
        "profile": PROFILE, "rom": "out/all_routes_combined_v4160_candidate.nds", "rom_sha256": ROM_SHA,
        "release_directory": "releases/all_routes_unified_v4160", "git_tag": "promoted-v4160",
        "patch_sha256": PATCH_SHA, "source_rom_sha256": CLEAN_SHA,
        "build_manifest_sha256": MANIFEST_SHA, "build_registry_sha256": REGISTRY_SHA,
        "immutable_construction_baseline": deepcopy(registry["canonical_baseline"]),
        "previous_promoted_build": "releases/all_routes_unified_v4046/promotion.json",
        "promotion_scope": "User-designated main cumulative checkpoint; retain immutable construction baseline, accepted-layer status and frozen source/hash contracts. Buildable profile status stays experimental in the registry schema; this record designates the main build.",
        "known_open_scope": open_scope, "complete_entries": 5602, "source_prose_reviewed_entries": 5605,
        "reviewed_incomplete_COMMON_entries": 3, "unintegrated_uncredited_B168_objects": 54,
        "full_editorial_goal_complete": False, "full_graphics_goal_complete": False,
        "new_user_cold_boot_test_claimed": False, "new_emulator_runs_at_promotion": 0,
        "construction_baseline_rebased": False,
    }
    save(PACKAGE / "promotion.json", promotion)
    save(PACKAGE / "release_manifest.json", {
        "game": "Daikoukai Jidai IV / Rota Nova DS", "patch_version": "unified-v4160",
        "status": "promoted", "main_build": True, "profile": PROFILE,
        "source_rom_sha256": CLEAN_SHA, "modified_rom_sha256": ROM_SHA, "patch_sha256": PATCH_SHA,
        "full_graphics_goal_complete": False, "full_editorial_goal_complete": False,
        "promotion_record": "promotion.json", "notes": open_scope,
    })
    registry["latest_promoted_build"] = {
        "status": "promoted", "main_build": True, "profile": PROFILE, "rom_sha256": ROM_SHA,
        "record": "translations/promoted_build.json", "git_tag": "promoted-v4160",
        "construction_baseline_rebased": False,
    }
    summary = ("V4186 promotes verified V4160 as the user's new main cumulative build. All 543 manuscript batches and 114 accepted layers are preserved; the packaged clean-input patch reconstructs the entire ROM byte for byte. This includes completed B166 and B167. Current completed coverage remains 5602 fresh contextual rereads/integrated, 5605 source/prose reviews, 3567 historically revised and 2035 retained; 4003 reviewed route objects are integrated, with zero credited records pending. B168's 54 draft-reviewed objects (28 proposed revisions/26 justified retentions) remain separately uncredited and absent from the ROM. Offline native checks pass all 54 planes/432 alignment cases; final visual approval, ledger reconciliation, relocation, stored references, representative gameplay, registered integration and startup remain. No new emulator run, user cold-boot test or review credit is claimed by promotion. V4046 and all earlier builds, translations, drafts, executed producers/proofs/failures remain preserved. Immutable construction inputs and accepted-layer status are unchanged. " + open_scope)
    ledger["promoted_main_build_v4186"] = promotion
    ledger["lil_B168_preintegration_review_v4186"] = pending
    ledger["latest_checkpoint"] = summary
    section = "## V4186: V4160 promoted as main; B168 draft review preserved\n\n" + summary + "\n\nMain build: [Unified V4160](../releases/all_routes_unified_v4160/README.md). ROM SHA-256: `" + ROM_SHA + "`. Patch SHA-256: `" + PATCH_SHA + "`. Earlier sections describe their original checkpoints.\n\nNext: " + pending["visual_resume"] + " Continue B169-B180 and the full wider editorial objective. Remaining B168-B180 has 321 physical speeches and zero typed choice-command leads; this is not a full-project denominator. Full goal active.\n\n"
    mutations = {
        "translations/release_stack.json": encoded(registry),
        "translations/promoted_build.json": encoded(promotion),
        "translations/editorial_review_current_v1.json": encoded(ledger),
    }
    docs = ["editorial_handoff_current.md", "translation_progress.md", "editorial_review_goal.md", "todo.md", "known_issues.md", "release_build.md"]
    for index, name in enumerate(docs):
        path = "docs/" + name
        first, rest = (ROOT / path).read_text(encoding="utf-8").split("\n", 1)
        if index == 0:
            first = "# Current editorial handoff - V4186"
        mutations[path] = (first + "\n\n" + section + rest).encode("utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = readme.replace("[Unified V4046](releases/all_routes_unified_v4046/README.md)", "[Unified V4160](releases/all_routes_unified_v4160/README.md)")
    readme = readme.replace("Earlier [V1492]", "Earlier [V4046](releases/all_routes_unified_v4046/README.md), [V1492]")
    mutations["README.md"] = readme.encode("utf-8")
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "!releases/all_routes_unified_v4160/*.xdelta" not in ignore
    mutations[".gitignore"] = ignore.replace("!releases/all_routes_unified_v4046/*.xdelta", "!releases/all_routes_unified_v4046/*.xdelta\n!releases/all_routes_unified_v4160/*.xdelta").encode("utf-8")
    pins = read(ROOT / "translations/rom_retention_pins.json")
    pins.append({"path": str(reconstruction.resolve()), "reason": "V4186 promoted V4160 exact clean-input patch reconstruction. Preserve all ROMs under active user goal; no pruning. SHA-256 " + ROM_SHA})
    mutations["translations/rom_retention_pins.json"] = encoded(pins)
    staged = AUDIT / "staged"
    staged.mkdir()
    plan = []
    for index, (relative, data) in enumerate(mutations.items()):
        destination = ROOT / relative
        before = destination.read_bytes()
        (AUDIT / (str(index) + ".before")).write_bytes(before)
        planned = staged / (str(index) + ".planned")
        planned.write_bytes(data)
        plan.append({"target": str(destination), "before_sha256": sha(before),
                     "planned": str(planned), "planned_sha256": sha(data)})
    save(AUDIT / "mutation_plan.json", plan)
    (PACKAGE / "README.md").write_text(
        "# Main promoted English build: V4160\n\nPromoted on 2026-10-26 at the user's request. Tag: `promoted-v4160`.\n\n"
        "This cumulative build contains 543 manuscript batches and 114 accepted layers, including the completed Lil B166 and B167 reviews. Earlier releases and all local ROMs/translations are preserved.\n\n"
        "## Apply the patch\n\nSupply your own unmodified Japanese ROM with SHA-256 `" + CLEAN_SHA + "`:\n\n"
        "```powershell\npython -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4160/translation.xdelta --out out/all_routes_combined_v4160_candidate.nds\n```\n\n"
        "Expected ROM SHA-256: `" + ROM_SHA + "`.\n\nPatch SHA-256: `" + PATCH_SHA + "`.\n\nThe complete clean-input patch reconstruction was rerun byte for byte at promotion. ROMs, saves and raw RAM captures remain local. The retained ROM is `E:/Rota Nova translations/Generated/out/all_routes_combined_v4160_candidate.nds`.\n\n"
        "## Verification and coverage\n\nThe registered profile is `all-routes-unified-v4160`. Against V4110 only SC2 B167 changes; every other file/component, font, graphic, ARM9 and 123040-byte staged payload remains exact. Existing B167 tests include four 14401-frame Japanese/English cold boots covering both menu outcomes, 25 distinct speeches/28 English observations and both normal town returns. Two alternative Cesare remarks have offline native coverage only. Two additional registered opening/town cold boots pass 31 whole-frame comparisons and five actor/captain checks. The inherited town battery is test data, not earned progress. These targeted automated headless emulator tests do not establish natural event eligibility, full route completion or hardware verification. Promotion adds no new emulator or user cold-boot claim.\n\n"
        "At promotion, 78 existing integrated-release, dialogue-review, wrapping, pair-phase, relocation and literal-guard tests passed. The packaged existing release/startup receipts and viewed startup sheet preserve their original scope.\n\n"
        "## Unfinished work\n\nThe ledger retains 5602 completed contextual reviews (3567 historically revised/2035 retained) and 5605 source/prose reviews. B168 has 54 draft-reviewed objects (28 proposed revisions/26 justified retentions). **Those revisions are not in this ROM.** Offline checks pass 54 native planes and 432 alignment cases. Final visual approval and subsequent ledger, relocation, representative gameplay and registered release gates remain pending. The packaged B168 status identifies exact resume references; its native proof is explicitly labelled unintegrated.\n\n"
        + open_scope + "\n\nSee the [current handoff](../../docs/editorial_handoff_current.md).\n\n"
        "## Reproduction records\n\n`build_manifest.json.gz` and `build_release_stack.json.gz` preserve the exact original build-time bytes; decompressed hashes are in `promotion.json`. The current registry changes only its promotion pointer. `checksums.json` covers every other packaged file. `verification/` contains scoped receipts, the promotion reconstruction and final audit.\n\n"
        "The immutable construction baseline is `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `" + BASE_SHA + "`. This checkpoint promotion preserves frozen builders, canonical inputs and accepted-layer status. Buildable profiles retain the registry schema's experimental status; `promoted_build.json` designates the main build.\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({"staged": len(plan), "profile": PROFILE, "patch_reconstruction_byte_exact": True,
                      "canonical_baseline_rebased": False, "B168_unintegrated_uncredited": 54}))


if __name__ == "__main__":
    main()
