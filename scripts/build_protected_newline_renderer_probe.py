from __future__ import annotations

import argparse
import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path

SOURCE_SHA256 = "baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce"
RETIRED_REASON = (
    "retired unsafe probe: 0x02172300 is live structured ARM9 data in the "
    "known-good Raphael savestate, not a code cave"
)


@dataclass(frozen=True)
class Arm9Patch:
    address: int
    expected: bytes
    replacement: bytes
    purpose: str


# Historical, revoked implementation. The apparent ROM zero padding at
# 0x02172300 is populated with structured data in the known-good Raphael
# savestate. apply_patches() intentionally hard-fails before any write.
CODE_CAVE_ADDRESS = 0x02172300
CODE_CAVE = bytes.fromhex(
    "01C0DAE5"  # ldrb r12, [r10, #1]
    "20005CE3"  # cmp  r12, #0x20
    "02A08A02"  # addeq r10, r10, #2
    "01A08A12"  # addne r10, r10, #1
    "1EFF2FE1"  # bx   lr
)


def arm_bl(source: int, target: int, *, condition: int = 0xE) -> bytes:
    displacement = target - (source + 8)
    if displacement % 4:
        raise ValueError("ARM branch target is not word aligned")
    word_offset = displacement // 4
    if not -(1 << 23) <= word_offset < (1 << 23):
        raise ValueError("ARM branch target is out of range")
    instruction = (condition << 28) | 0x0B000000 | (word_offset & 0x00FFFFFF)
    return struct.pack("<I", instruction)


PATCHES = (
    Arm9Patch(
        0x0207CFC4,
        bytes.fromhex("01A08AE2"),
        arm_bl(0x0207CFC4, CODE_CAVE_ADDRESS),
        "call the guard-aware advance from the explicit-newline path",
    ),
    Arm9Patch(
        0x0207D038,
        bytes.fromhex("01A08A02"),
        arm_bl(0x0207D038, CODE_CAVE_ADDRESS, condition=0x0),
        "call the guard-aware advance at the width-boundary LF path",
    ),
    Arm9Patch(
        CODE_CAVE_ADDRESS,
        bytes(len(CODE_CAVE)),
        CODE_CAVE,
        "install LF+SPACE-aware source advance in verified ARM9 zero padding",
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def apply_patches(rom: bytes, *, require_source_lock: bool = True) -> bytes:
    raise ValueError(RETIRED_REASON)
    # Historical implementation retained below so its exact writes remain auditable.
    if require_source_lock and sha256(rom) != SOURCE_SHA256:
        raise ValueError("source ROM does not match dialogue_live_safe_v3.nds")

    rebuilt = bytearray(rom)
    arm9_offset, _entry, arm9_ram, arm9_size = struct.unpack_from("<IIII", rebuilt, 0x20)
    arm9_end = arm9_offset + arm9_size

    for patch in PATCHES:
        relative = patch.address - arm9_ram
        if relative < 0:
            raise ValueError(f"patch address {patch.address:08X} precedes ARM9 load address")
        offset = arm9_offset + relative
        end = offset + len(patch.expected)
        if end > arm9_end:
            raise ValueError(f"patch address {patch.address:08X} lies outside ARM9")
        actual = bytes(rebuilt[offset:end])
        if actual != patch.expected:
            raise ValueError(
                f"ARM9 mismatch at {patch.address:08X}: "
                f"expected {patch.expected.hex()}, found {actual.hex()}"
            )
        rebuilt[offset:end] = patch.replacement

    return bytes(rebuilt)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a disposable renderer probe that hides the protected "
            "LF+SPACE guard without changing dialogue data or generic ASCII rendering."
        )
    )
    parser.add_argument("--base", type=Path, default=Path("out/dialogue_live_safe_v3.nds"))
    parser.add_argument(
        "--out", type=Path, default=Path("out/dialogue_protected_newline_probe.nds")
    )
    args = parser.parse_args()

    source = args.base.read_bytes()
    rebuilt = apply_patches(source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(rebuilt)

    print(f"wrote {args.out}")
    print(f"base_sha256={sha256(source)}")
    print(f"probe_sha256={sha256(rebuilt)}")
    for patch in PATCHES:
        print(f"patched {patch.address:08X}: {patch.purpose}")


if __name__ == "__main__":
    main()
