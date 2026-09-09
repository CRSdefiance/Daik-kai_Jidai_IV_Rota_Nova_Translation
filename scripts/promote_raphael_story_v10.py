from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STACK_PATH = ROOT / "translations/release_stack.json"
ACCEPTED_PATH = ROOT / "translations/accepted_baseline.json"
BASELINE = ROOT / "out/raphael_natural_v2_accepted_base.nds"
CANDIDATE = ROOT / "out/raphael_story_push_v10_candidate.nds"
MANIFEST = ROOT / "out/raphael_story_push_v10_candidate.manifest.json"
ROLLBACK = ROOT / "out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds"

OLD_SHA256 = "d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf"
NEW_SHA256 = "0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2"
PROFILE = "raphael-story-push-v1"
PROMOTED_PROFILES = (
    "ships-submenu-v2",
    "ships-route-forces-v1",
    "opening-movie-v1",
    PROFILE,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if digest(BASELINE) != OLD_SHA256:
        raise SystemExit("canonical pre-promotion baseline hash mismatch")
    if digest(CANDIDATE) != NEW_SHA256:
        raise SystemExit("V10 candidate hash mismatch")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if (
        manifest.get("candidate_sha256") != NEW_SHA256
        or manifest.get("base_sha256") != OLD_SHA256
        or manifest.get("profile") != PROFILE
        or not manifest.get("checks", {}).get("saved_rom_roundtrip")
    ):
        raise SystemExit("V10 manifest does not authorize promotion")

    if ROLLBACK.exists():
        if digest(ROLLBACK) != OLD_SHA256:
            raise SystemExit("existing V10 rollback path has unexpected bytes")
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
                "name": f"story-v10-promotion-{Path(batch).stem}",
                "batch": batch,
                "status": "accepted",
                "baked_into_baseline": True,
                "note": "Explicitly accepted by the user on 2026-09-09 and baked into the Raphael Story V10 baseline.",
            }
        )
        accepted_batches.add(batch)
    stack["canonical_baseline"] = {
        "path": "out/raphael_natural_v2_accepted_base.nds",
        "sha256": NEW_SHA256,
        "accepted_on": "2026-09-09",
        "previous_baseline": {
            "path": "out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds",
            "sha256": OLD_SHA256,
        },
    }
    for name in PROMOTED_PROFILES:
        stack["profiles"][name]["status"] = "accepted-baked"
    write_json(STACK_PATH, stack)

    accepted = {
        "format": "dk4-accepted-baseline-v1",
        "accepted_on": "2026-09-09",
        "user_acceptance": "Promote this and push to github",
        "rom": "out/raphael_natural_v2_accepted_base.nds",
        "sha256": NEW_SHA256,
        "promoted_from": "out/raphael_story_push_v10_candidate.nds",
        "promoted_from_manifest": "out/raphael_story_push_v10_candidate.manifest.json",
        "previous_baseline": {
            "rom": "out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds",
            "sha256": OLD_SHA256,
            "status": "rollback-only",
        },
        "accepted_layers": [layer["name"] for layer in stack["accepted_layers"]],
        "runtime_evidence": {
            "explicit_promotion": True,
            "automated_regression_tests": 282,
            "baseline_invariant_check": True,
            "candidate_manifest_verified": True,
            "sound_selector_verified": "38 BGM and 57 SFX titles",
            "cold_boot_scope": "The user reviewed the evolving integrated V1-V10 builds through supplied cold-boot screenshots, confirmed the latest Deck fixes, and explicitly approved V10 promotion.",
        },
    }
    write_json(ACCEPTED_PATH, accepted)
    print(f"promoted {PROFILE}: {NEW_SHA256}")
    print(f"rollback: {ROLLBACK.name} ({OLD_SHA256})")


if __name__ == "__main__":
    main()
