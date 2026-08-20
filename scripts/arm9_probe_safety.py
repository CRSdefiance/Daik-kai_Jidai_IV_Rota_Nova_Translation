from __future__ import annotations

import struct
from dataclasses import dataclass

# This whole file-zeroed tail is runtime-owned. A known-good Raphael savestate
# contains structured values at 0x02172300, and the cold-boot New Game trace
# contains structured values at 0x021723FC through 0x02172463. Zero bytes in the
# ROM image are therefore not evidence that any part of this range is a cave.
RUNTIME_OWNED_TAIL = (0x02171E48, 0x02172464)
PROVEN_RAPHAEL_DATA = (0x02172300, 0x02172320)
PROVEN_NEW_GAME_DATA = (0x021723FC, 0x02172464)


@dataclass(frozen=True)
class Arm9Layout:
    file_offset: int
    entry_address: int
    load_address: int
    size: int

    @property
    def end_address(self) -> int:
        return self.load_address + self.size


def read_arm9_layout(rom: bytes) -> Arm9Layout:
    if len(rom) < 0x30:
        raise ValueError("ROM is too small to contain an NDS ARM9 header")
    file_offset, entry_address, load_address, size = struct.unpack_from("<IIII", rom, 0x20)
    if file_offset + size > len(rom):
        raise ValueError("ARM9 range extends beyond the ROM")
    return Arm9Layout(file_offset, entry_address, load_address, size)


def runtime_to_file_offset(rom: bytes, address: int, length: int) -> int:
    if length < 0:
        raise ValueError("length must not be negative")
    layout = read_arm9_layout(rom)
    if address < layout.load_address or address + length > layout.end_address:
        raise ValueError(
            f"runtime range 0x{address:08X}-0x{address + length:08X} lies outside ARM9"
        )
    return layout.file_offset + address - layout.load_address


def ranges_overlap(start: int, end: int, blocked_start: int, blocked_end: int) -> bool:
    return start < blocked_end and blocked_start < end


def reject_runtime_owned_tail(address: int, length: int) -> None:
    end = address + length
    blocked_start, blocked_end = RUNTIME_OWNED_TAIL
    if ranges_overlap(address, end, blocked_start, blocked_end):
        raise ValueError(
            f"runtime range 0x{address:08X}-0x{end:08X} overlaps runtime-owned ARM9 "
            f"data 0x{blocked_start:08X}-0x{blocked_end:08X}; ROM zero padding is not a cave"
        )


def require_exact_bytes(rom: bytes, address: int, expected: bytes) -> int:
    reject_runtime_owned_tail(address, len(expected))
    offset = runtime_to_file_offset(rom, address, len(expected))
    actual = rom[offset : offset + len(expected)]
    if actual != expected:
        raise ValueError(
            f"ARM9 mismatch at 0x{address:08X}: expected {expected.hex()}, found {actual.hex()}"
        )
    return offset
