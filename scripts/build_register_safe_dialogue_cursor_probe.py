from __future__ import annotations

import argparse
import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path

SOURCE_SHA256 = "75f27e78cabbce6d55aba9ad26665271bfe1ee13fbd666d3f8cf34c03abbdd46"
RETIRED_REASON = (
    "retired unsafe probe: 0x021723FC-0x02172463 is live structured ARM9 data "
    "during New Game initialization"
)
STANDARD_DIALOGUE_CALL = 0x02054924
SHARED_RENDERER = 0x020D5404
CURSOR_LOAD = 0x020D5504
FLAG_ADDRESS = 0x021723FC
WRAPPER_ADDRESS = 0x02172400
HELPER_ADDRESS = 0x02172424


@dataclass(frozen=True)
class Arm9Patch:
    address: int
    expected: bytes
    replacement: bytes
    purpose: str


def arm_branch(source: int, target: int, *, link: bool, condition: int = 0xE) -> bytes:
    displacement = target - (source + 8)
    if displacement % 4:
        raise ValueError("ARM branch target is not word aligned")
    word_offset = displacement // 4
    if not -(1 << 23) <= word_offset < (1 << 23):
        raise ValueError("ARM branch target is out of range")
    opcode = 0x0B000000 if link else 0x0A000000
    return struct.pack("<I", (condition << 28) | opcode | (word_offset & 0x00FFFFFF))


def arm_bl(source: int, target: int) -> bytes:
    return arm_branch(source, target, link=True)


# Preserve the incoming r2/r3 even though they are nominally call-clobbered,
# preserve r4/lr, and keep the stack 8-byte aligned across the nested call.
WRAPPER = b"".join(
    (
        bytes.fromhex("1C402DE9"),  # push {r2, r3, r4, lr}
        bytes.fromhex("14409FE5"),  # ldr  r4, [pc, #0x14]
        bytes.fromhex("01C0A0E3"),  # mov  r12, #1
        bytes.fromhex("00C0C4E5"),  # strb r12, [r4]
        arm_bl(WRAPPER_ADDRESS + 0x10, SHARED_RENDERER),
        bytes.fromhex("00C0A0E3"),  # mov  r12, #0
        bytes.fromhex("00C0C4E5"),  # strb r12, [r4]
        bytes.fromhex("1C80BDE8"),  # pop  {r2, r3, r4, pc}
        struct.pack("<I", FLAG_ADDRESS),
    )
)


# The original instruction changes only r3. Preserve r12 around all flag and
# source inspection so the flag-off path is equivalent to the original load.
HELPER = b"".join(
    (
        bytes.fromhex("00102DE9"),  # push {r12}
        bytes.fromhex("24309AE5"),  # ldr  r3, [r10, #0x24] (original)
        bytes.fromhex("2CC09FE5"),  # ldr  r12, [pc, #0x2c]
        bytes.fromhex("00C0DCE5"),  # ldrb r12, [r12]
        bytes.fromhex("00005CE3"),  # cmp  r12, #0
        arm_branch(HELPER_ADDRESS + 0x14, HELPER_ADDRESS + 0x34, link=False, condition=0x0),
        bytes.fromhex("01C0D9E5"),  # ldrb r12, [r9, #1]
        bytes.fromhex("20005CE3"),  # cmp  r12, #0x20
        arm_branch(HELPER_ADDRESS + 0x20, HELPER_ADDRESS + 0x34, link=False, condition=0x1),
        bytes.fromhex("060053E3"),  # cmp  r3, #6
        arm_branch(HELPER_ADDRESS + 0x28, HELPER_ADDRESS + 0x34, link=False, condition=0x3),
        bytes.fromhex("063043E2"),  # sub  r3, r3, #6
        bytes.fromhex("24308AE5"),  # str  r3, [r10, #0x24]
        bytes.fromhex("0010BDE8"),  # pop  {r12}
        arm_branch(HELPER_ADDRESS + 0x38, CURSOR_LOAD + 4, link=False),
        struct.pack("<I", FLAG_ADDRESS),
    )
)


PATCHES = (
    Arm9Patch(FLAG_ADDRESS, b"\x00", b"\x00", "reserve private flag"),
    Arm9Patch(
        STANDARD_DIALOGUE_CALL,
        arm_bl(STANDARD_DIALOGUE_CALL, SHARED_RENDERER),
        arm_bl(STANDARD_DIALOGUE_CALL, WRAPPER_ADDRESS),
        "scope the flag to the proven story call",
    ),
    Arm9Patch(
        CURSOR_LOAD,
        bytes.fromhex("24309AE5"),
        arm_branch(CURSOR_LOAD, HELPER_ADDRESS, link=False),
        "branch to the link-register-safe cursor trampoline",
    ),
    Arm9Patch(WRAPPER_ADDRESS, bytes(len(WRAPPER)), WRAPPER, "install wrapper"),
    Arm9Patch(HELPER_ADDRESS, bytes(len(HELPER)), HELPER, "install helper"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def apply_patches(rom: bytes, *, require_source_lock: bool = True) -> bytes:
    raise ValueError(RETIRED_REASON)
    # Historical implementation retained below so its exact writes remain auditable.
    if require_source_lock and sha256(rom) != SOURCE_SHA256:
        raise ValueError("source ROM does not match dialogue_protected_newline_probe.nds")
    rebuilt = bytearray(rom)
    arm9_offset, _entry, arm9_ram, arm9_size = struct.unpack_from("<IIII", rebuilt, 0x20)
    arm9_end = arm9_offset + arm9_size
    for patch in PATCHES:
        offset = arm9_offset + patch.address - arm9_ram
        end = offset + len(patch.expected)
        if offset < arm9_offset or end > arm9_end:
            raise ValueError(f"patch address {patch.address:08X} lies outside ARM9")
        actual = bytes(rebuilt[offset:end])
        if actual != patch.expected:
            raise ValueError(
                f"ARM9 mismatch at {patch.address:08X}: expected {patch.expected.hex()}, "
                f"found {actual.hex()}"
            )
        rebuilt[offset:end] = patch.replacement
    return bytes(rebuilt)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build register-safe scoped dialogue probe")
    parser.add_argument("--base", type=Path, default=Path("out/dialogue_protected_newline_probe.nds"))
    parser.add_argument("--out", type=Path, default=Path("out/dialogue_link_safe_cursor_probe.nds"))
    args = parser.parse_args()
    source = args.base.read_bytes()
    rebuilt = apply_patches(source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(rebuilt)
    print(f"wrote {args.out}")
    print(f"base_sha256={sha256(source)}")
    print(f"probe_sha256={sha256(rebuilt)}")


if __name__ == "__main__":
    main()
