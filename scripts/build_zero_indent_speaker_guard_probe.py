from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

SOURCE_SHA256 = "baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce"
FILE_PATH = "/data/SC0.DK4"
BLOCK_INDEX = 44
SPEAKER_CONTROL = 0x05  # Claudio Manaus in the tested opening scene.
TARGET_SEGMENTS = (25, 67, 74)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a disposable zero-indent experiment by replacing the visible "
            "post-LF space with the current speaker's zero-width control byte."
        )
    )
    parser.add_argument("--base", type=Path, default=Path("out/dialogue_live_safe_v3.nds"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--reproduce-rejected-research",
        action="store_true",
        help="Allow reproduction of this known-failing historical experiment.",
    )
    args = parser.parse_args()

    if not args.reproduce_rejected_research:
        raise SystemExit(
            "REJECTED PROBE: runtime testing proved that 0x05 is visible and "
            "still consumes a continuation-line cell. Use "
            "--reproduce-rejected-research only to reproduce the documented failure."
        )

    source_rom = args.base.read_bytes()
    if sha256(source_rom) != SOURCE_SHA256:
        raise SystemExit("refusing source other than the verified live-safe v3 candidate")
    if args.base.resolve() == args.out.resolve():
        raise SystemExit("refusing to overwrite the verified live-safe candidate")

    baseline = NdsImage.open(args.base)
    image = NdsImage.open(args.base)
    source = image.read_file(FILE_PATH)
    container = IlnkContainer.parse(source)
    segments = container.blocks[BLOCK_INDEX].split(b"\0")
    changed: list[int] = []
    for index in TARGET_SEGMENTS:
        original = segments[index]
        if not original.startswith(bytes([SPEAKER_CONTROL])):
            raise SystemExit(f"segment {index} is not a Claudio record")
        count = original.count(b"\x0A\x20")
        if count != 1:
            raise SystemExit(f"segment {index} has {count} protected line breaks, expected 1")
        segments[index] = original.replace(
            b"\x0A\x20", b"\x0A" + bytes([SPEAKER_CONTROL]), 1
        )
        changed.append(index)

    original_block_lengths = [len(block) for block in container.blocks]
    container.blocks[BLOCK_INDEX] = b"\0".join(segments)
    rebuilt = container.to_bytes()
    if len(rebuilt) != len(source):
        raise SystemExit("probe changed SC0 size")
    if [len(block) for block in container.blocks] != original_block_lengths:
        raise SystemExit("probe changed an ILNK block size")

    image.replace_file(FILE_PATH, rebuilt)
    image.save(args.out)
    saved = NdsImage.open(args.out)
    if saved.read_file(FILE_PATH) != rebuilt:
        raise SystemExit("saved probe did not round-trip")
    before_files = {path: data for _, path, data in baseline.iter_files()}
    after_files = {path: data for _, path, data in saved.iter_files()}
    changed_paths = [
        path for path in before_files if before_files[path] != after_files[path]
    ]
    if changed_paths != [FILE_PATH]:
        raise SystemExit(f"unexpected changed ROM files: {changed_paths}")
    if saved.read_file("/__arm9__.bin") != baseline.read_file("/__arm9__.bin"):
        raise SystemExit("probe unexpectedly changed ARM9")

    manifest = {
        "format": "dk4-research-probe-v1",
        "status": "REJECTED_DO_NOT_USE",
        "hypothesis": (
            "Repeating the active speaker control after LF may satisfy the delayed "
            "progressive line transition without drawing a visible guard cell."
        ),
        "source": str(args.base),
        "source_sha256": SOURCE_SHA256,
        "candidate": str(args.out),
        "candidate_sha256": sha256(args.out.read_bytes()),
        "changed_file": FILE_PATH,
        "changed_block": BLOCK_INDEX,
        "changed_segments": changed,
        "replacement": "0A20 -> 0A05",
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
