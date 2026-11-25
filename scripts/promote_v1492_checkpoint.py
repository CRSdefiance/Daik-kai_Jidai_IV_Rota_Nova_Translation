"""Package the explicitly requested V1492 checkpoint without rebasing frozen inputs."""
from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "releases/all_routes_unified_v1492"
PROFILE = "all-routes-unified-v1492"
ROM_SHA = "96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd"
PATCH_SHA = "417db2ada9bc4a5ebfd552e6e2f81a8d57ba75369b6c3488eca6284b086867d0"
MANIFEST_SHA = "fdf9f572febb67d4cd6dfbfae2fbec5dc318fcaea1d9792e84955795b2ecc2ba"
CLEAN_SHA = "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    rom = ROOT / "out/all_routes_combined_v1492_candidate.nds"
    patch = rom.with_suffix(".xdelta")
    manifest = rom.with_suffix(".manifest.json")
    for path, expected in [(rom, ROM_SHA), (patch, PATCH_SHA), (manifest, MANIFEST_SHA)]:
        assert digest(path.read_bytes()) == expected, str(path)
    build = json.loads(manifest.read_text(encoding="utf-8"))
    assert build["profile"] == PROFILE
    proof_path = ROOT / "work/analysis/battle_reaction_release_v1491/registered_release_verification.json"
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    assert proof["complete_reconstruction_byte_exact"] is True
    assert proof["candidate_sha256"] == ROM_SHA and proof["patch_sha256"] == PATCH_SHA
    reconstruction = ROOT / proof["reconstruction"]
    assert digest(reconstruction.read_bytes()) == ROM_SHA
    registry_path = ROOT / "translations/release_stack.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert registry["canonical_baseline"]["sha256"] == proof["canonical_sha256"]
    assert len(registry["accepted_layers"]) == 114
    assert len(registry["profiles"][PROFILE]["batches"]) == 470
    RELEASE.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(patch, RELEASE / "translation.xdelta")
    (RELEASE / "build_manifest.json.gz").write_bytes(gzip.compress(manifest.read_bytes(), mtime=0))
    registry_snapshot = RELEASE / "build_release_stack.json.gz"
    if not registry_snapshot.exists():
        raw_registry = registry_path.read_bytes()
        assert digest(raw_registry) == build["release_stack_sha256"]
        registry_snapshot.write_bytes(gzip.compress(raw_registry, mtime=0))
    assert digest(gzip.decompress(registry_snapshot.read_bytes())) == build["release_stack_sha256"]
    verification = RELEASE / "verification"
    verification.mkdir(exist_ok=True)
    for source, name in [
        (proof_path, "registered_release_verification.json"),
        (ROOT / "work/analysis/battle_reaction_integration_v1499/integration_receipt.json", "integration_receipt.json"),
        (ROOT / "work/analysis/stronger_fleet_return_verified_v1505/actual_declaration_defeat_and_transfer_return.json", "original_defeat_transfer_control.json"),
        (ROOT / "work/analysis/retreat_transfer_fonts_v1512/native_font_research.json", "UNINTEGRATED_retreat_font_research.json"),
    ]:
        shutil.copyfile(source, verification / name)
    promotion = {
        "format": "dk4-promoted-checkpoint-v1",
        "status": "promoted",
        "promoted_on": "2026-10-22",
        "user_request": "can you commit and push the work that has been done so far to github, and mark our latest work as a promoted build",
        "profile": PROFILE,
        "rom": "out/all_routes_combined_v1492_candidate.nds",
        "rom_sha256": ROM_SHA,
        "release_directory": "releases/all_routes_unified_v1492",
        "git_tag": "promoted-v1492",
        "patch_sha256": PATCH_SHA,
        "source_rom_sha256": CLEAN_SHA,
        "build_manifest_sha256": MANIFEST_SHA,
        "build_registry_sha256": build["release_stack_sha256"],
        "immutable_construction_baseline": registry["canonical_baseline"],
        "promotion_scope": "User-designated cumulative build checkpoint; preserve the immutable construction baseline and all frozen source/hash contracts. This does not certify every scene or complete the editorial/graphics goals.",
        "known_open_issue": "Retreat notices 2683-2689 can interpret custom ship names such as ICARUS as speech codes. V1509b/V1511b/V1512 contain an unintegrated research repair; visual refinement, copy/cache regressions, registered build and original transfer replay remain pending.",
        "complete_entries": 1323,
        "source_prose_reviewed_entries": 1467,
        "reviewed_incomplete_COMMON_entries": 144,
        "full_editorial_goal_complete": False,
        "full_graphics_goal_complete": False,
        "new_user_cold_boot_test_claimed": False,
    }
    write_json(RELEASE / "promotion.json", promotion)
    write_json(ROOT / "translations/promoted_build.json", promotion)
    registry["latest_promoted_build"] = {
        "status": "promoted", "profile": PROFILE, "rom_sha256": ROM_SHA,
        "record": "translations/promoted_build.json", "git_tag": "promoted-v1492",
        "construction_baseline_rebased": False,
    }
    write_json(registry_path, registry)
    write_json(RELEASE / "release_manifest.json", {
        "game": "Daikoukai Jidai IV / Rota Nova DS", "patch_version": "unified-v1492",
        "status": "promoted", "profile": PROFILE,
        "source_rom_sha256": CLEAN_SHA, "modified_rom_sha256": ROM_SHA,
        "patch_sha256": PATCH_SHA, "full_graphics_goal_complete": False,
        "full_editorial_goal_complete": False, "promotion_record": "promotion.json",
        "notes": promotion["known_open_issue"],
    })
    files = {str(p.relative_to(RELEASE)).replace("\\", "/"): digest(p.read_bytes())
             for p in sorted(RELEASE.rglob("*")) if p.is_file() and p.name != "checksums.json"}
    write_json(RELEASE / "checksums.json", files)
    print(json.dumps({"promoted": PROFILE, "rom_sha256": ROM_SHA, "packaged_files": len(files),
                      "construction_baseline_rebased": False, "exact_reconstruction_rechecked": True}))


if __name__ == "__main__":
    main()
