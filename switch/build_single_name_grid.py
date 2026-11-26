"""Place the Switch 1.0.2 name keyboard layouts in one shared inset."""

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
from struct import pack

from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN

from .build_name_keyboard import STOCK_SHA256, TEXT_OFFSET
from .export_catalogs import apply_literal_ips


V94_SHA256 = "f2e1f79ab5339b40464da1cca2a9c0f92fab4abff91fc7fc7b59e73b22b751d4"


def single_grid_edits(assemble):
    edits = {}

    def code(address, source):
        edits[address + TEXT_OFFSET] = assemble(source, address)

    # Position the active subpanel at the main editor's inset. Offsets
    # are measured from the editor origin supplied by its caller.
    code(0x13DCD0, """
        ldr x11, [sp, #0x30]
        ldp x8, x9, [x11]
        add x8, x8, #44
        add x9, x9, #160
        stp x8, x9, [sp, #0x38]
        b #0x13dd04
    """)
    # Do not activate an empty subpanel during initialization.
    code(0x13DD18, "nop")
    # Use the subpanel's new inset size directly when constructing it.
    code(0x13DD7C, """
        mov x20, x5
        mov x21, x4
        mov x19, x0
        add x2, sp, #0x30
        ldp x8, x10, [x3]
        ldp x11, x9, [x19, #0xd8]
        add x11, x11, x8
        add x9, x9, x10
        stp x8, x10, [sp, #0x30]
        stp x11, x9, [sp, #0x40]
        mov x3, x21
        mov x4, x20
        b #0x13ddc8
    """)
    def adr_x3(address, target):
        displacement = target - address
        return 0x10000003 | ((displacement & 3) << 29) | ((displacement >> 2 & 0x7ffff) << 5)

    # Use the exact inset of the original name-editor sprite as the
    # subpanel background. Neither the name field nor OK is overdrawn.
    edits[0x13E0C8 + TEXT_OFFSET] = pack("<8q", 0, 0, 548, 284, 44, 160, 592, 444)
    code(0x13DDE8, f"""
        mov w2, #0x1e
        .word {adr_x3(0x13DDEC, 0x13E0C8):#x}
        add x4, x3, #0x20
        mov w5, wzr
        mov w6, wzr
    """)
    code(0x13DE48, f"""
        mov w2, #0x1e
        .word {adr_x3(0x13DE4C, 0x13E0C8):#x}
        add x4, x3, #0x20
        mov w5, wzr
        mov w6, wzr
    """)
    # Center the 11-column, five-row keyboard and fit the native
    # scrollbar used by longer kanji and symbol pages inside the frame.
    edits[0x41D7E8 + TEXT_OFFSET] = pack("<2q", 1120, 671)
    edits[0x41D7F8 + TEXT_OFFSET] = pack("<2q", 1477, 665)
    edits[0x41D808 + TEXT_OFFSET] = pack("<2q", 548, 284)
    edits[0x41D828 + TEXT_OFFSET] = pack("<2q", 44, 216)

    # Hide the empty subpanel before restoring native kana focus.
    code(0x13DCE8, """
        str w8, [x0, #0x124]
        ldr x8, [x19]
        ldur x8, [x8, #-0x20]
        add x0, x19, x8
        bl #0x16c110
        mov x2, xzr
        b #0x13f24c
    """)
    code(0x13F244, "b #0x13dce8")
    code(0x13F250, "add x0, x19, #0x18")
    return edits


def patch_ips(stock: bytes, base: bytes) -> bytes:
    if sha256(stock).hexdigest() != STOCK_SHA256 or sha256(base).hexdigest() != V94_SHA256:
        raise ValueError("Expected the Japanese Switch 1.0.2 uncompressed main NSO and v94 IPS")
    asm = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    edits = single_grid_edits(lambda source, addr: asm.asm(source, addr, as_bytes=True)[0])
    records = {}
    cursor = 5
    while cursor < len(base) - 3:
        offset = int.from_bytes(base[cursor:cursor + 3], "big")
        count = int.from_bytes(base[cursor + 3:cursor + 5], "big")
        cursor += 5
        records[offset] = base[cursor:cursor + count]
        cursor += count
    result = bytearray(b"PATCH")
    for address, content in sorted((records | edits).items()):
        result.extend(address.to_bytes(3, "big"))
        result.extend(len(content).to_bytes(2, "big"))
        result.extend(content)
    result.extend(b"EOF")
    image = bytearray(apply_literal_ips(stock, base))
    for address, content in edits.items():
        image[address:address + len(content)] = content
    if apply_literal_ips(stock, result) != image:
        raise ValueError("Rebuilt IPS differs from the intended executable")
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stock_nso", type=Path)
    parser.add_argument("v94_ips", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = patch_ips(args.stock_nso.read_bytes(), args.v94_ips.read_bytes())
    with args.output.open("xb") as stream:
        stream.write(result)
    print(f"{sha256(result).hexdigest()}  {args.output}")


if __name__ == "__main__":
    main()
