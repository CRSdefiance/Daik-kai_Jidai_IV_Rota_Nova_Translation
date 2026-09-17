from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STACK_PATH = ROOT / "translations/release_stack.json"
ACCEPTED_PATH = ROOT / "translations/accepted_baseline.json"
BASELINE = ROOT / "out/raphael_natural_v2_accepted_base.nds"
CANDIDATE = ROOT / "out/lil_hodram_unified_v1_candidate.nds"
MANIFEST = ROOT / "out/lil_hodram_unified_v1_manifest.json"
ROLLBACK = (
    ROOT / "out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds"
)

OLD_SHA256 = "0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2"
NEW_SHA256 = "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
PROFILE = "lil-hodram-unified-v1"
ABSORBED_PROFILES = (
    "hodram-market-inn-sea-v2",
    "lil-b22-intro-all-items-v5",
    PROFILE,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    if digest(BASELINE) != OLD_SHA256:
        raise SystemExit("canonical pre-promotion baseline hash mismatch")
    if digest(CANDIDATE) != NEW_SHA256:
        raise SystemExit("Lil/Hodram cumulative candidate hash mismatch")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if (
        manifest.get("candidate_sha256") != NEW_SHA256
        or manifest.get("base_sha256") != OLD_SHA256
        or manifest.get("profile") != PROFILE
        or not manifest.get("checks", {}).get("saved_rom_roundtrip")
        or not manifest.get("checks", {}).get("fixed_text_two_byte_guards_enforced")
    ):
        raise SystemExit("candidate manifest does not authorize this promotion")

    if ROLLBACK.exists():
        if digest(ROLLBACK) != OLD_SHA256:
            raise SystemExit("existing rollback path has unexpected bytes")
    else:
        shutil.copy2(BASELINE, ROLLBACK)
    shutil.copy2(CANDIDATE, BASELINE)
    if digest(ROLLBACK) != OLD_SHA256 or digest(BASELINE) != NEW_SHA256:
        raise SystemExit("promotion copy verification failed")

    stack = json.loads(STACK_PATH.read_text(encoding="utf-8"))
    profile = stack["profiles"][PROFILE]
    accepted_batches = {layer["batch"] for layer in stack["accepted_layers"]}
    for batch in profile["batches"]:
        if batch in accepted_batches:
            continue
        stack["accepted_layers"].append(
            {
                "name": f"lil-hodram-v1-promotion-{Path(batch).stem}",
                "batch": batch,
                "status": "accepted",
                "baked_into_baseline": True,
                "note": "Explicitly accepted by the user on 2026-09-17 and baked into the cumulative Lil, Guild, Hodram, market, Inn, shipyard, cargo, and at-sea baseline.",
            }
        )
        accepted_batches.add(batch)

    stack["canonical_baseline"] = {
        "path": "out/raphael_natural_v2_accepted_base.nds",
        "sha256": NEW_SHA256,
        "accepted_on": "2026-09-17",
        "previous_baseline": {
            "path": "out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds",
            "sha256": OLD_SHA256,
        },
    }
    for name in ABSORBED_PROFILES:
        stack["profiles"][name]["status"] = "accepted-baked"
    write_json(STACK_PATH, stack)

    accepted = {
        "format": "dk4-accepted-baseline-v1",
        "accepted_on": "2026-09-17",
        "user_acceptance": "okay, promote this build and push to github",
        "rom": "out/raphael_natural_v2_accepted_base.nds",
        "sha256": NEW_SHA256,
        "promoted_from": "out/lil_hodram_unified_v1_candidate.nds",
        "promoted_from_manifest": "out/lil_hodram_unified_v1_manifest.json",
        "previous_baseline": {
            "rom": "out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds",
            "sha256": OLD_SHA256,
            "status": "rollback-only",
        },
        "accepted_layers": [layer["name"] for layer in stack["accepted_layers"]],
        "runtime_evidence": {
            "explicit_promotion": True,
            "automated_regression_tests": 346,
            "baseline_invariant_check": True,
            "candidate_manifest_verified": True,
            "cold_boot_scope": "The user reviewed the cumulative translation work through supplied runtime screenshots and explicitly requested promotion of the unified Lil/Guild/Hodram build.",
        },
    }
    write_json(ACCEPTED_PATH, accepted)
    print(f"promoted {PROFILE}: {NEW_SHA256}")
    print(f"rollback: {ROLLBACK.name} ({OLD_SHA256})")


if __name__ == "__main__":
    main()
