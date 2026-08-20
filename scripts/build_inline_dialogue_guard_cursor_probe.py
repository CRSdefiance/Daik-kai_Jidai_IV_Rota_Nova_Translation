from __future__ import annotations

import argparse
import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.arm9_probe_safety import require_exact_bytes, runtime_to_file_offset
except ModuleNotFoundError:  # Direct `python scripts/...py` invocation.
    from arm9_probe_safety import require_exact_bytes, runtime_to_file_offset


SOURCE_SHA256 = "baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce"
RETIRED_REASON = (
    "retired failed probe: both zero- and one-pixel cursor targets lose the "
    "uppercase J at the protected Janus break"
)
BYTE_LOOP = 0x020D54F0
BLOCK_ADDRESS = 0x020D5504
BLOCK_SIZE = 0x68
HELPER_ADDRESS = 0x020D5544
CONTINUE_TARGET = 0x020D57FC
EXIT_TARGET = 0x020D5808
LOOP_BRANCH_ADDRESS = 0x020D5804
ORIGINAL_LOOP_BRANCH = bytes.fromhex("39FFFF1A")

ORIGINAL_BLOCK = bytes.fromhex(
    "24309AE5 04009AE5 019089E2 030050E1 0510A0E1 0500A0E1 0580A0E1"
    "020000CA 0C209AE5 020053E1 0480A0B1 000058E3 0300000A 08309AE5"
    "28209AE5 020053E1 0400A0D1 000050E3 0300000A 28209AE5 10009AE5"
    "000052E1 0410A0B1 000051E3 A400001A A60000EA"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def arm_branch(source: int, target: int, *, condition: int = 0xE) -> bytes:
    displacement = target - (source + 8)
    if displacement % 4:
        raise ValueError("ARM branch target is not word aligned")
    word_offset = displacement // 4
    if not -(1 << 23) <= word_offset < (1 << 23):
        raise ValueError("ARM branch target is out of range")
    return struct.pack(
        "<I", (condition << 28) | 0x0A000000 | (word_offset & 0x00FFFFFF)
    )


def decode_arm_branch(address: int, instruction: bytes) -> tuple[int, int, bool]:
    word = struct.unpack("<I", instruction)[0]
    if word & 0x0E000000 != 0x0A000000:
        raise ValueError("instruction is not an ARM B/BL")
    displacement = word & 0x00FFFFFF
    if displacement & 0x00800000:
        displacement -= 1 << 24
    return word >> 28, address + 8 + displacement * 4, bool(word & 0x01000000)


@dataclass(frozen=True)
class BranchExpectation:
    address: int
    condition: int
    target: int


BRANCHES = (
    BranchExpectation(0x020D5514, 0xC, EXIT_TARGET),
    BranchExpectation(0x020D5520, 0xA, EXIT_TARGET),
    BranchExpectation(0x020D5530, 0xC, EXIT_TARGET),
    BranchExpectation(0x020D553C, 0xA, EXIT_TARGET),
    BranchExpectation(0x020D5540, 0xE, CONTINUE_TARGET),
    BranchExpectation(0x020D5560, 0xE, BYTE_LOOP),
)


REPLACEMENT_BLOCK = b"".join(
    (
        bytes.fromhex("24309AE5"),  # ldr r3, [r10, #0x24]   current X
        bytes.fromhex("04009AE5"),  # ldr r0, [r10, #4]      lower X
        bytes.fromhex("019089E2"),  # add r9, r9, #1         retain guard
        bytes.fromhex("030050E1"),  # cmp r0, r3
        arm_branch(0x020D5514, EXIT_TARGET, condition=0xC),
        bytes.fromhex("0C209AE5"),  # ldr r2, [r10, #0x0c]   upper X
        bytes.fromhex("020053E1"),  # cmp r3, r2
        arm_branch(0x020D5520, EXIT_TARGET, condition=0xA),
        bytes.fromhex("08309AE5"),  # ldr r3, [r10, #8]      lower Y
        bytes.fromhex("28209AE5"),  # ldr r2, [r10, #0x28]   current Y
        bytes.fromhex("020053E1"),  # cmp r3, r2
        arm_branch(0x020D5530, EXIT_TARGET, condition=0xC),
        bytes.fromhex("10009AE5"),  # ldr r0, [r10, #0x10]   upper Y
        bytes.fromhex("000052E1"),  # cmp r2, r0
        arm_branch(0x020D553C, EXIT_TARGET, condition=0xA),
        arm_branch(0x020D5540, CONTINUE_TARGET),
        bytes.fromhex("022059E5"),  # ldrb r2, [r9, #-2]
        bytes.fromhex("0A0052E3"),  # cmp r2, #0x0a
        bytes.fromhex("01205905"),  # ldreqb r2, [r9, #-1]
        bytes.fromhex("20005203"),  # cmpeq r2, #0x20
        bytes.fromhex("24309A05"),  # ldreq r3, [r10, #0x24]
        bytes.fromhex("06005303"),  # cmpeq r3, #6
        bytes.fromhex("24408A05"),  # streq r4, [r10, #0x24] (one-pixel inset)
        arm_branch(0x020D5560, BYTE_LOOP),
        bytes.fromhex("0000A0E1") * 2,
    )
)

REPLACEMENT_LOOP_BRANCH = arm_branch(LOOP_BRANCH_ADDRESS, HELPER_ADDRESS, condition=0x1)


def verify_replacement() -> None:
    if len(ORIGINAL_BLOCK) != BLOCK_SIZE or len(REPLACEMENT_BLOCK) != BLOCK_SIZE:
        raise ValueError("cursor probe must retain the exact LF block size")
    for branch in BRANCHES:
        offset = branch.address - BLOCK_ADDRESS
        decoded = decode_arm_branch(branch.address, REPLACEMENT_BLOCK[offset : offset + 4])
        if decoded != (branch.condition, branch.target, False):
            raise ValueError(f"branch mismatch at 0x{branch.address:08X}: {decoded}")
    if decode_arm_branch(LOOP_BRANCH_ADDRESS, REPLACEMENT_LOOP_BRANCH) != (
        0x1,
        HELPER_ADDRESS,
        False,
    ):
        raise ValueError("loop branch does not target the inline guard helper")


def apply_patch(rom: bytes, *, require_source_lock: bool = True) -> bytes:
    raise ValueError(RETIRED_REASON)
    # Historical implementation retained below so its exact rewrite remains auditable.
    verify_replacement()
    if require_source_lock and sha256(rom) != SOURCE_SHA256:
        raise ValueError("source ROM does not match dialogue_live_safe_v3.nds")
    block_offset = require_exact_bytes(rom, BLOCK_ADDRESS, ORIGINAL_BLOCK)
    loop_offset = require_exact_bytes(rom, LOOP_BRANCH_ADDRESS, ORIGINAL_LOOP_BRANCH)
    rebuilt = bytearray(rom)
    rebuilt[block_offset : block_offset + BLOCK_SIZE] = REPLACEMENT_BLOCK
    rebuilt[loop_offset : loop_offset + 4] = REPLACEMENT_LOOP_BRANCH
    changed = {index for index, pair in enumerate(zip(rom, rebuilt)) if pair[0] != pair[1]}
    allowed = set(range(block_offset, block_offset + BLOCK_SIZE)) | set(
        range(loop_offset, loop_offset + 4)
    )
    if not changed or not changed <= allowed or len(rebuilt) != len(rom):
        raise ValueError("probe changed bytes outside its two declared ARM9 ranges")
    return bytes(rebuilt)


def build_manifest(source: bytes, rebuilt: bytes, output: Path) -> dict[str, object]:
    ranges = ((BLOCK_ADDRESS, BLOCK_SIZE), (LOOP_BRANCH_ADDRESS, 4))
    return {
        "format": "dk4-disposable-arm9-probe-v1",
        "status": "experimental-awaiting-cold-boot",
        "output": str(output),
        "base": "out/dialogue_live_safe_v3.nds",
        "base_sha256": sha256(source),
        "probe_sha256": sha256(rebuilt),
        "changed_components": ["/__arm9__.bin"],
        "changed_ranges": [
            {
                "runtime_start": f"0x{address:08X}",
                "runtime_end_exclusive": f"0x{address + length:08X}",
                "rom_file_start": f"0x{runtime_to_file_offset(source, address, length):08X}",
                "rom_file_end_exclusive": (
                    f"0x{runtime_to_file_offset(source, address, length) + length:08X}"
                ),
            }
            for address, length in ranges
        ],
        "external_storage": False,
        "runtime_success_claimed": False,
        "note": "Preserves LF+SPACE timing and reduces the traced six-pixel guard advance to one pixel.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build inline guard cursor probe")
    parser.add_argument("--base", type=Path, default=Path("out/dialogue_live_safe_v3.nds"))
    parser.add_argument(
        "--out", type=Path, default=Path("out/dialogue_guard_cursor_one_pixel_probe.nds")
    )
    args = parser.parse_args()
    source = args.base.read_bytes()
    rebuilt = apply_patch(source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(rebuilt)
    manifest_path = args.out.with_suffix(args.out.suffix + ".manifest.json")
    manifest_path.write_text(
        json.dumps(build_manifest(source, rebuilt, args.out), indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out}")
    print(f"wrote {manifest_path}")
    print(f"base_sha256={sha256(source)}")
    print(f"probe_sha256={sha256(rebuilt)}")


if __name__ == "__main__":
    main()
