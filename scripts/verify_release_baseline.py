from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from dk4tool.rom.nds import NdsImage

BASELINE_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
REQUIRED_MENU_TEXT = (b"Continue", b"New Game", b"Opts", b"Grand Race", b"Extras", b"Gallery")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def files(image: NdsImage) -> dict[str, bytes]:
    result = {path: data for _, path, data in image.iter_files()}
    result.update(dict(image.iter_components()))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Reject release builds that regress the known-good UI/graphics baseline.")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--allow-path", action="append", default=[])
    args = parser.parse_args()

    actual_baseline_hash = sha256(args.baseline.read_bytes())
    if actual_baseline_hash != BASELINE_SHA256:
        raise SystemExit(f"wrong baseline ROM: expected {BASELINE_SHA256}, got {actual_baseline_hash}")

    baseline = NdsImage.open(args.baseline)
    candidate = NdsImage.open(args.candidate)
    baseline_files = files(baseline)
    candidate_files = files(candidate)
    changed = {
        path
        for path in baseline_files.keys() | candidate_files.keys()
        if baseline_files.get(path) != candidate_files.get(path)
    }
    unexpected = sorted(changed - set(args.allow_path))
    if unexpected:
        raise SystemExit("unexpected files changed from baseline: " + ", ".join(unexpected))

    arm9 = candidate.read_file("/__arm9__.bin")
    missing_menu = [item.decode("ascii") for item in REQUIRED_MENU_TEXT if item not in arm9]
    if missing_menu:
        raise SystemExit("required English menu text missing: " + ", ".join(missing_menu))

    print("baseline invariant check passed")
    print("changed paths: " + ", ".join(sorted(changed)))
    print(f"candidate sha256: {sha256(args.candidate.read_bytes())}")


if __name__ == "__main__":
    main()
