from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STACK_PATH = ROOT / "translations/release_stack.json"
ACCEPTED_PATH = ROOT / "translations/accepted_baseline.json"
BASELINE = ROOT / "out/raphael_natural_v2_accepted_base.nds"
CANDIDATE = ROOT / "out/common_gameplay_natural_v2_candidate.nds"
ROLLBACK = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
MANIFEST = ROOT / "out/common_gameplay_natural_v2_candidate.manifest.json"

NEW_SHA256 = "c94e1fd7221c5e929c851a39f1e722c8b127992bea743dd9992ca1ff027afcdf"
OLD_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
PROFILE = "common-gameplay-natural-v2"
PROMOTED_PROFILES = {
    "hodram-intro-english-probe",
    "hodram-stockholm-tavern-complete",
    "hodram-trading-complete",
    "interface-polish-v1",
    PROFILE,
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if digest(BASELINE) != NEW_SHA256 or digest(CANDIDATE) != NEW_SHA256:
        raise SystemExit("promoted baseline and candidate are not byte-identical")
    if digest(ROLLBACK) != OLD_SHA256:
        raise SystemExit("pre-COMMON rollback hash mismatch")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("candidate_sha256") != NEW_SHA256 or manifest.get("profile") != PROFILE:
        raise SystemExit("candidate manifest does not authorize this promotion")

    stack = json.loads(STACK_PATH.read_text(encoding="utf-8"))
    profile = stack["profiles"][PROFILE]
    accepted_batches = {layer["batch"] for layer in stack["accepted_layers"]}
    for batch in profile["batches"]:
        if batch in accepted_batches:
            continue
        stack["accepted_layers"].append(
            {
                "name": f"common-promotion-{Path(batch).stem}",
                "batch": batch,
                "status": "accepted",
                "baked_into_baseline": True,
                "note": "Explicitly accepted by the user on 2026-08-31 and baked into the promoted COMMON gameplay baseline.",
            }
        )
        accepted_batches.add(batch)
    stack["canonical_baseline"] = {
        "path": "out/raphael_natural_v2_accepted_base.nds",
        "sha256": NEW_SHA256,
        "accepted_on": "2026-08-31",
        "previous_baseline": {
            "path": "out/raphael_natural_v2_pre_common_accepted_rollback.nds",
            "sha256": OLD_SHA256,
        },
    }
    for name in PROMOTED_PROFILES:
        stack["profiles"][name]["status"] = "accepted-baked"
    write_json(STACK_PATH, stack)

    accepted = {
        "format": "dk4-accepted-baseline-v1",
        "accepted_on": "2026-08-31",
        "user_acceptance": "First, promote your current build.",
        "rom": "out/raphael_natural_v2_accepted_base.nds",
        "sha256": NEW_SHA256,
        "promoted_from": "out/common_gameplay_natural_v2_candidate.nds",
        "promoted_from_manifest": "out/common_gameplay_natural_v2_candidate.manifest.json",
        "previous_baseline": {
            "rom": "out/raphael_natural_v2_pre_common_accepted_rollback.nds",
            "sha256": OLD_SHA256,
            "status": "rollback-only",
        },
        "accepted_layers": [layer["name"] for layer in stack["accepted_layers"]],
        "runtime_evidence": {
            "explicit_promotion": True,
            "automated_regression_tests": 242,
            "baseline_invariant_check": True,
            "candidate_manifest_verified": True,
            "cold_boot_scope": "User promoted the current build; exact screens tested were not restated in the promotion message.",
        },
    }
    write_json(ACCEPTED_PATH, accepted)
    print(f"promoted {PROFILE}: {NEW_SHA256}")


if __name__ == "__main__":
    main()
