"""Rebuild the Switch 1.0.2 Latin name keyboard IPS from the v91 IPS."""

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path

from .export_catalogs import apply_literal_ips


STOCK_SHA256 = "577b985b2441c3cfe5ee95b544147570b1293c5ddd6d1cbb89eb06172e242b41"
V91_SHA256 = "6100bcd27a8e3f26a59ce6eac90d14f60a2fcbc18aea8b883c7d25e6a247f9aa"
TEXT_OFFSET = 0x100
SELECTOR_START = 0x13EB50
SELECTOR_END = 0x13ED18


def keyboard_edits(assemble):
    edits = {}

    def write(address, code):
        edits[address + TEXT_OFFSET] = assemble(code, address)

    def helper(code):
        address = SELECTOR_START + sum(map(len, edits.values()))
        write(address, code)
        return address

    # Preserve the original button priority and reuse the rest of its body.
    helper("""
        mov w8, #0x83ff
        movk w8, #7, lsl #16
        and w8, w0, w8
        rbit w8, w8
        clz w0, w8
        cmp w0, #32
        mov w8, #20
        csel w0, w8, w0, eq
        ret
    """)

    # Prefix only Latin keyboard grids with a private rendering marker. The
    # draw queue copies this buffer before returning. The marker is stripped
    # by both the drawing and measuring paths before glyphs are processed.
    draw_grid = helper("""
        ldr w8, [x19, #0x124]
        cmp w8, #50
        b.ne draw
        sub sp, sp, #0xa0
        stp x0, x30, [sp]
        mov w8, #0xf7ff
        strh w8, [sp, #0x10]
        add x0, sp, #0x12
        bl #0x2b6c90
        ldr x0, [sp]
        add x1, sp, #0x10
        mov w2, wzr
        mov x3, xzr
        bl #0x10440
        ldr x30, [sp, #8]
        add sp, sp, #0xa0
        ret
    draw:
        b #0x10440
    """)
    convert = helper("""
        ldrb w16, [x2]
        cmp w16, #0xff
        b.ne normal
        ldrb w16, [x2, #1]
        cmp w16, #0xf7
        b.ne normal
        mov x0, x1
        add x1, x2, #2
        b #0x2b6c90
    normal:
        stp x28, x27, [sp, #-0x60]!
        b #0x9bd4
    """)
    # Initialization activates the empty popup. Cycle it as the original
    # Aa handler does so activation selects a key in the populated panel.
    # Pass the existing Aa group label at 0x3f195a.
    open_latin = helper("""
        str x30, [sp, #-0x10]!
        bl #0x16c2c0
        bl #0x72bc0
        tst w0, #0xff
        b.eq done
        ldr x8, [x19, #0x338]
        ldr x9, [x8]
        ldur x9, [x9, #-0x20]
        add x0, x8, x9
        bl #0x16c110
        ldr x0, [x19, #0x338]
        adrp x1, #0x3f1000
        add x1, x1, #0x95a
        bl #0x13e840
        ldr x8, [x19, #0x338]
        ldr x9, [x8]
        ldur x9, [x9, #-0x20]
        add x0, x8, x9
        bl #0x16c2c0
    done:
        ldr x30, [sp], #0x10
        ret
    """)
    # This Japanese-locale group contains 26 lowercase and 26 uppercase
    # CP932 characters. Put the kana panel key in the next free cell.
    append_kana_key = helper("""
        stp x0, x30, [sp, #-0x10]!
        bl #0x2b6ea0
        ldp x8, x30, [sp], #0x10
        mov w9, #0xa082
        strh w9, [x8, #104]
        strb wzr, [x8, #106]
        ret
    """)
    select_key = helper("""
        cmp w1, #50
        b.ne character
        cmp w2, #52
        b.ne character
        mov x0, x19
        bl #0x13f230
        b #0x13fd60
    character:
        ldp x8, x9, [x19, #0x110]
        b #0x13fd0c
    """)
    keep_latin_open = helper("""
        ldr w8, [x0, #0x124]
        cmp w8, #50
        b.ne #0x13f230
        ldr x0, [x0, #0x118]
        mov w1, #2
        b #0x13ed30
    """)

    # Match the name field's centered drawing path (106f0) at its native
    # 13x26 text size. The renderer folds full-width Latin for both calls.
    measure_name = helper("""
        adrp x0, #0x549000
        ldr x0, [x0, #0x710]
        mov w2, #13
        mov w3, #26
        mov w4, wzr
        mov w5, wzr
        b #0xb5a0
    """)
    # The Latin panel takes controller focus. Let the original editor
    # handle X, L, R, and B through its existing buttons and validation.
    latin_shortcuts = helper("""
        ldr w8, [x0, #0x124]
        cmp w8, #50
        b.ne normal_input
        adrp x8, #0x549000
        ldr x8, [x8, #0x6e0]
        ldr w9, [x8, #0x70]
        mov w10, #0x306
        tst w9, w10
        b.ne parent_input
        ldr w9, [x8, #0x74]
        cbz w9, normal_input
    parent_input:
        stp x0, x1, [sp]
        ldr x0, [x0, #0x118]
        bl #0x13ea30
        tbnz w0, #0, #0x13fc60
        ldp x0, x1, [sp]
    normal_input:
        ldr x8, [x0, #0x110]
        b #0x13f9ac
    """)
    # Keep the stock button glyphs on the editor while the Latin child has
    # focus. Leave the original focus flag intact for the UI's dispatch.
    show_editor_shortcuts = helper("""
        b.ne #0x13ed50
        ldr x8, [x20, #0x338]
        cbz x8, unfocused
        ldr w8, [x8, #0x124]
        cmp w8, #50
        b.eq #0x13ed50
    unfocused:
        b #0x13edb0
    """)
    if SELECTOR_START + sum(map(len, edits.values())) > SELECTOR_END:
        raise ValueError("Keyboard helpers exceed the original button selector")

    write(0x9BD0, f"b #{convert:#x}")
    # Conversion runs after the control-token parser. Save data and game
    # logic still see the original two-byte characters.
    write(0x9CD0, """
        cmp w14, #0xff
        b.eq #0x9c6c
        ldrh w1, [x2], #2
        cmp w14, #0x82
        b.ne copy_pair
        lsr w16, w1, #8
        sub w14, w16, #0x60
        cmp w14, #25
        b.ls emit
        sub w14, w16, #0x81
        cmp w14, #25
        b.hi copy_pair
        add w14, w14, #32
    emit:
        add w14, w14, #65
        b #0x9c70
    copy_pair:
        strh w1, [x15], #2
        b #0x9c74
    """)

    # Preserve the caret's stored byte index. Clamp it to an encoded
    # character boundary before temporarily measuring a NUL-ended prefix.
    # The game restores the name before returning to drawing and input.
    write(0x13C6C4, f"""
        ldr x20, [x0, #0xb0]
        mov x19, x0
        mov x21, xzr
    scan:
        cmp w21, w1
        b.ge located
        ldrb w8, [x20, x21]
        cbz w8, located
        sub w9, w8, #0xa1
        cmp w9, #0x3e
        lsr w8, w8, #7
        ccmp w8, #1, #0, hi
        add x9, x21, #1
        cinc x9, x9, hs
        cmp w9, w1
        b.gt located
        mov x21, x9
        b scan
    located:
        str w21, [x19, #0xbc]
        ldr x8, [x19, #0xc0]
        cbz x8, #0x13c7c8
        ldr x8, [x19]
        ldur x8, [x8, #-0x18]
        add x21, x19, x8
        mov x1, x20
        bl #{measure_name:#x}
        ldp x8, x9, [x21, #0x30]
        ldp x10, x11, [x21, #0x40]
        sub x10, x10, x8
        sub x11, x11, x9
        sub x10, x10, x0
        sub x11, x11, x1
        cmp x10, #0
        cinc x10, x10, lt
        cmp x11, #0
        cinc x11, x11, lt
        add x8, x8, x10, asr #1
        add x9, x9, x11, asr #1
        stp x8, x9, [x19, #0xc8]
        ldrsw x21, [x19, #0xbc]
        ldrb w8, [x20, x21]
        str w8, [sp, #8]
        strb wzr, [x20, x21]
        mov x1, x20
        bl #{measure_name:#x}
        ldr w8, [sp, #8]
        strb w8, [x20, x21]
        ldp x8, x1, [x19, #0xc8]
        add x8, x8, x0
        ldr x9, [x19, #0xc0]
        ldr x10, [x9]
        ldur x10, [x10, #-0x18]
        add x0, x9, x10
        stp x8, x1, [sp, #0x30]
        b #0x13c79c
    """)
    if len(edits[0x13C6C4 + TEXT_OFFSET]) > 0x13C79C - 0x13C6C4:
        raise ValueError("Name caret logic exceeds its original function")

    # Stock editing assumes two bytes per letter. Localized preset names
    # can contain both ASCII and CP932, so delete one encoded character.
    write(0x13C960, """
        stp x20, x19, [sp, #-0x20]!
        stp x29, x30, [sp, #0x10]
        add x29, sp, #0x10
        mov x19, x0
        ldr x20, [x19, #0xb0]
        ldrb w8, [x20]
        cbz w8, redraw
        ldr w10, [x19, #0xbc]
        mov w11, wzr
        mov w12, wzr
    scan:
        mov w11, w12
        add x0, x20, w12, uxtw
        bl #0x13c9e0
        cbz w0, redraw
        add w12, w12, w0
        cmp w12, w10
        b.lo scan
        mov w1, w11
    shift:
        ldrb w8, [x20, w12, uxtw]
        strb w8, [x20, w11, uxtw]
        add w12, w12, #1
        add w11, w11, #1
        cbnz w8, shift
        mov x0, x19
        bl #0x13c6b0
    redraw:
        mov x0, x19
        ldp x29, x30, [sp, #0x10]
        ldp x20, x19, [sp], #0x20
        b #0x13c860
    """)
    write(0x13CA30, """
        ldr x0, [x0, #0xb0]
        add x0, x0, w8, uxtw
        bl #0x13c9e0
        add w1, w8, w0
        ldr x0, [x19, #0x330]
        b #0x13e724
    """)
    # Return the length of the character at x0 without changing the
    # caller's index registers. A terminator advances zero bytes.
    write(0x13C9E0, """
        ldrb w9, [x0]
        cbz w9, end
        sub w13, w9, #0x81
        cmp w13, #0x1e
        b.ls lead
        sub w13, w9, #0xe0
        cmp w13, #0x1c
        b.hi single
    lead:
        ldrb w9, [x0, #1]
        cmp w9, #0
        cset w0, ne
        add w0, w0, #1
        ret
    single:
        mov w0, #1
        ret
    end:
        mov w0, wzr
        ret
    """)
    if any(start + len(edits[start + TEXT_OFFSET]) > end for start, end in (
        (0x13C960, 0x13C9E0), (0x13C9E0, 0x13CA30), (0x13CA30, 0x13CA60),
    )):
        raise ValueError("Name editing helpers exceed the original delete routine")
    write(0x13BD88, f"bl #{append_kana_key:#x}")
    write(0x13E704, "sub w1, w8, #1")
    write(0x13E720, "b #0x13ca30")
    write(0x13ED4C, f"b #{show_editor_shortcuts:#x}")
    # A refresh after typing only updates the glyphs. Keep the active
    # grid key selected, including when the name goes from empty to set.
    write(0x13EF20, """
        cmp w1, #2
        b.ne #0x16d040
        ret
    """)
    write(0x13EFBC, f"bl #{open_latin:#x}")
    write(0x13F8B4, f"bl #{draw_grid:#x}")
    write(0x13F9A8, f"b #{latin_shortcuts:#x}")
    write(0x13FD08, f"b #{select_key:#x}")
    write(0x13FD5C, f"bl #{keep_latin_open:#x}")
    return edits


def patch_ips(stock: bytes, base_ips: bytes) -> bytes:
    if sha256(stock).hexdigest() != STOCK_SHA256 or sha256(base_ips).hexdigest() != V91_SHA256:
        raise ValueError("Expected the Japanese Switch 1.0.2 uncompressed main NSO and the v91 IPS")

    from keystone import KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN, Ks

    assembler = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    edits = keyboard_edits(lambda code, address: assembler.asm(code, address, as_bytes=True)[0])
    image = bytearray(apply_literal_ips(stock, base_ips))
    ranges = []
    cursor = 5
    while cursor < len(base_ips) - 3:
        offset = int.from_bytes(base_ips[cursor:cursor + 3], "big")
        length = int.from_bytes(base_ips[cursor + 3:cursor + 5], "big")
        ranges.append((offset, offset + length))
        cursor += 5 + length

    for offset, data in edits.items():
        image[offset:offset + len(data)] = data
        ranges.append((offset, offset + len(data)))

    # Preserve every baseline IPS byte outside the edits, including bytes
    # whose patched value happened to match the original executable.
    merged = []
    for start, end in sorted(ranges):
        if merged and start < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))

    result = bytearray(b"PATCH")
    for start, end in merged:
        result.extend(start.to_bytes(3, "big"))
        result.extend((end - start).to_bytes(2, "big"))
        result.extend(image[start:end])
    result.extend(b"EOF")
    if apply_literal_ips(stock, result) != image:
        raise ValueError("Rebuilt IPS differs from the intended executable")
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stock_nso", type=Path)
    parser.add_argument("v91_ips", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = patch_ips(args.stock_nso.read_bytes(), args.v91_ips.read_bytes())
    with args.output.open("xb") as stream:
        stream.write(result)
    print(f"{sha256(result).hexdigest()}  {args.output}")


if __name__ == "__main__":
    main()
