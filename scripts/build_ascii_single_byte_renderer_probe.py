from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

SOURCE_SHA256 = "baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce"
ARM9_LOAD_ADDRESS = 0x02000000
FILE_PATH = "/data/SC0.DK4"
BLOCK_INDEX = 44
SPEAKER_CONTROL = 0x05  # Claudio Manaus in all three test records.
TARGET_SEGMENTS = (25, 67, 74)
ARM9_PATCHES = (
    # The original narrow branch groups two bytes into one draw call. Make its
    # second buffer byte NUL and advance its source/column cursors by one.
    (0x0207CFE0, bytes.fromhex("0160DAE5"), bytes.fromhex("0060A0E3")),
    (0x0207D000, bytes.fromhex("02A08AE2"), bytes.fromhex("01A08AE2")),
    (0x0207D008, bytes.fromhex("029089E2"), bytes.fromhex("019089E2")),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a disposable standard-dialogue renderer experiment that consumes "
            "narrow ASCII one byte at a time and tests bare line feeds."
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
            "REJECTED PROBE: runtime testing proved that 0x0207CFD0 is not the "
            "live progressive-story renderer. Use --reproduce-rejected-research "
            "only to reproduce the documented failure."
        )

    source_rom = args.base.read_bytes()
    if sha256(source_rom) != SOURCE_SHA256:
        raise SystemExit("refusing source other than the verified live-safe v3 candidate")
    if args.base.resolve() == args.out.resolve():
        raise SystemExit("refusing to overwrite the verified live-safe candidate")

    baseline = NdsImage.open(args.base)
    image = NdsImage.open(args.base)

    arm9 = bytearray(image.read_file("/__arm9__.bin"))
    patched_addresses: list[str] = []
    for address, expected, replacement in ARM9_PATCHES:
        offset = address - ARM9_LOAD_ADDRESS
        actual = bytes(arm9[offset : offset + len(expected)])
        if actual != expected:
            raise SystemExit(
                f"ARM9 mismatch at 0x{address:08X}: "
                f"expected {expected.hex().upper()}, got {actual.hex().upper()}"
            )
        arm9[offset : offset + len(expected)] = replacement
        patched_addresses.append(f"0x{address:08X}")
    image.replace_file("/__arm9__.bin", bytes(arm9))

    source_sc0 = image.read_file(FILE_PATH)
    container = IlnkContainer.parse(source_sc0)
    segments = container.blocks[BLOCK_INDEX].split(b"\0")
    changed_segments: list[int] = []
    for index in TARGET_SEGMENTS:
        original = segments[index]
        if not original.startswith(bytes([SPEAKER_CONTROL])):
            raise SystemExit(f"segment {index} is not a Claudio record")
        count = original.count(b"\x0A\x20")
        if count != 1:
            raise SystemExit(f"segment {index} has {count} protected line breaks, expected 1")
        # Retain the fixed segment size by moving the former guard space to the
        # end, where these short test records cannot cross a page boundary.
        segments[index] = original.replace(b"\x0A\x20", b"\x0A", 1) + b" "
        if len(segments[index]) != len(original):
            raise SystemExit(f"segment {index} changed size")
        changed_segments.append(index)

    original_block_lengths = [len(block) for block in container.blocks]
    container.blocks[BLOCK_INDEX] = b"\0".join(segments)
    rebuilt_sc0 = container.to_bytes()
    if len(rebuilt_sc0) != len(source_sc0):
        raise SystemExit("probe changed SC0 size")
    if [len(block) for block in container.blocks] != original_block_lengths:
        raise SystemExit("probe changed an ILNK block size")
    image.replace_file(FILE_PATH, rebuilt_sc0)

    image.save(args.out)
    saved = NdsImage.open(args.out)
    if saved.read_file(FILE_PATH) != rebuilt_sc0:
        raise SystemExit("saved SC0 probe did not round-trip")
    if saved.read_file("/__arm9__.bin") != bytes(arm9):
        raise SystemExit("saved ARM9 probe did not round-trip")

    before_files = {path: data for _, path, data in baseline.iter_files()}
    after_files = {path: data for _, path, data in saved.iter_files()}
    changed_paths = [path for path in before_files if before_files[path] != after_files[path]]
    if changed_paths != [FILE_PATH]:
        raise SystemExit(f"unexpected changed NitroFS files: {changed_paths}")
    for address, _, replacement in ARM9_PATCHES:
        offset = address - ARM9_LOAD_ADDRESS
        actual = saved.read_file("/__arm9__.bin")[offset : offset + len(replacement)]
        if actual != replacement:
            raise SystemExit(f"saved ARM9 patch mismatch at 0x{address:08X}")

    manifest = {
        "format": "dk4-research-probe-v1",
        "status": "REJECTED_DO_NOT_USE",
        "hypothesis": (
            "The standard-dialogue path groups narrow ASCII into two-byte draw calls. "
            "Processing one byte per call should make bare LF safe and remove guard indentation."
        ),
        "source": str(args.base),
        "source_sha256": SOURCE_SHA256,
        "candidate": str(args.out),
        "candidate_sha256": sha256(args.out.read_bytes()),
        "changed_components": ["/__arm9__.bin", FILE_PATH],
        "arm9_patches": patched_addresses,
        "changed_block": BLOCK_INDEX,
        "changed_segments": changed_segments,
        "record_replacement": "0A20 -> 0A (space moved to record tail)",
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
