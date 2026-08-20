from __future__ import annotations

import argparse
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN, Cs

ARM9_LOAD_ADDRESS = 0x02000000


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List ARM9 instruction windows that compare a value with LF (0x0A)."
    )
    parser.add_argument("image", type=Path)
    parser.add_argument("--load-address", type=lambda value: int(value, 0), default=ARM9_LOAD_ADDRESS)
    parser.add_argument("--context", type=int, default=6)
    args = parser.parse_args()

    disassembler = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
    disassembler.skipdata = True
    instructions = list(disassembler.disasm(args.image.read_bytes(), args.load_address))
    matches = [
        index
        for index, instruction in enumerate(instructions)
        if instruction.mnemonic == "cmp" and instruction.op_str.endswith(", #0xa")
    ]
    print(f"matches={len(matches)}")
    for match in matches:
        print("\n---")
        start = max(0, match - args.context)
        end = min(len(instructions), match + args.context + 1)
        for index in range(start, end):
            instruction = instructions[index]
            marker = ">" if index == match else " "
            print(
                f"{marker} {instruction.address:08X}  {instruction.bytes.hex().upper():<8}  "
                f"{instruction.mnemonic:<8} {instruction.op_str}"
            )


if __name__ == "__main__":
    main()
