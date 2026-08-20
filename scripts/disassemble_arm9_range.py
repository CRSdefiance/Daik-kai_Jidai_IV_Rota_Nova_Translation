from __future__ import annotations

import argparse
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN, Cs

ARM9_LOAD_ADDRESS = 0x02000000


def parse_int(value: str) -> int:
    return int(value, 0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Disassemble an ARM instruction range from an extracted DS ARM9 image."
    )
    parser.add_argument("image", type=Path)
    parser.add_argument("start", type=parse_int)
    parser.add_argument("end", type=parse_int)
    parser.add_argument("--load-address", type=parse_int, default=ARM9_LOAD_ADDRESS)
    args = parser.parse_args()

    if args.start < args.load_address or args.end <= args.start:
        raise SystemExit("invalid virtual address range")
    data = args.image.read_bytes()
    start_offset = args.start - args.load_address
    end_offset = args.end - args.load_address
    if end_offset > len(data):
        raise SystemExit("range lies outside the ARM9 image")

    disassembler = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
    for instruction in disassembler.disasm(data[start_offset:end_offset], args.start):
        print(
            f"{instruction.address:08X}  {instruction.bytes.hex().upper():<8}  "
            f"{instruction.mnemonic:<8} {instruction.op_str}"
        )


if __name__ == "__main__":
    main()
