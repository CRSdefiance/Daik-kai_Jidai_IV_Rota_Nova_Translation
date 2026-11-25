"""Regress the exact Guild header overwrite and native right-edge pixels/ABI."""
import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_glyph_right_bounds import propose
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine, call, STACK

OUT = Path('../tmp/lisbon_office_fix/native_bounds')
HEADER = 0x02450000


def verify(source, target):
    font = GameAsciiFont.from_arm9(target)
    assert font.glyphs == GameAsciiFont.from_arm9(source).glyphs
    color_table = struct.unpack_from('<I', target, 0xD181C)[0] - 0x02000000
    color = struct.unpack_from('<H', target, color_table + 2)[0]
    rows = []
    u = machine(target)
    for mode in [4, 16]:
        width, pitch, stride = 36, 9 if mode == 4 else 36, 18 if mode == 4 else 72
        for height in [2, 11, 12, 14]:
            for x0 in [0, 1, 3, 8, 30, 33, 35, 36, 40]:
                for y0 in [0, 1, 10, 12]:
                    for char in 'Gd gyp':
                        size = stride * height
                        header = struct.pack('<5I', mode, pitch, height, 0x2000, 20)
                        initial = bytes([0x99]) * size
                        u.mem_write(HEADER - 16, b'\xA5' * (size + 52))
                        u.mem_write(HEADER, header + initial)
                        u.mem_write(STACK, struct.pack('<2I', ord(char), 1))
                        call(u, 0xD16B4, (0, HEADER, x0, y0))
                        expected = bytearray(initial)
                        glyph = font.decode(char)
                        for y in range(max(0, min(11, height - y0 - 1))):
                            for x in range(max(0, min(6, width - x0))):
                                ink = bool(glyph.getpixel((x, y)))
                                px, py = x0 + x, y0 + 1 + y
                                if mode == 16:
                                    if ink:
                                        struct.pack_into('<H', expected, py * stride + px * 2, color)
                                else:
                                    at, shift = py * stride + px // 2, px % 2 * 4
                                    expected[at] = expected[at] & ~(15 << shift) | ((1 if ink else 0) << shift)
                        assert bytes(u.mem_read(HEADER + 20, size)) == expected, (mode, height, x0, y0, char)
                        assert bytes(u.mem_read(HEADER, 20)) == header
                        assert bytes(u.mem_read(HEADER - 16, 16)) == b'\xA5' * 16
                        assert bytes(u.mem_read(HEADER + 20 + size, 16)) == b'\xA5' * 16
                        rows.append(dict(mode=mode, height=height, x=x0, y=y0, char=char))
    # Match the actual layout: pixels precede their own 4-bit image header.
    # The padded sixth cell at x33 used to clear that header's mode byte.
    regression = []
    for name, arm in [('before', source), ('fixed', target)]:
        cpu = machine(arm)
        pixels = HEADER - 216
        header = struct.pack('<5I', 4, 9, 12, 0x2000, (-216) & 0xFFFFFFFF)
        cpu.mem_write(pixels - 16, b'\xA5' * (216 + 20 + 32))
        cpu.mem_write(pixels, bytes(216))
        cpu.mem_write(HEADER, header)
        point, text = 0x02460000, 0x02460100
        cpu.mem_write(point, struct.pack('<2I', 3, 0))
        cpu.mem_write(text, b'Guild \0')
        cpu.mem_write(STACK, struct.pack('<I', 15))
        call(cpu, 0xD1604, (0, HEADER, point, text))
        after = bytes(cpu.mem_read(HEADER, 20))
        assert (after == header) == (name == 'fixed')
        assert struct.unpack_from('<I', after)[0] == (4 if name == 'fixed' else 0)
        if name == 'fixed':
            expected = bytearray(216)
            for i, char in enumerate('Guild '):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        px = 3 + i * 6 + x
                        if px < 36 and glyph.getpixel((x, y)):
                            at, shift = (y + 1) * 18 + px // 2, px % 2 * 4
                            expected[at] |= 15 << shift
            assert bytes(cpu.mem_read(pixels, 216)) == expected
        regression.append(dict(version=name, image_header_before=header.hex(), image_header_after=after.hex()))
    return dict(native_pixel_ABI_canary_cases=len(rows), cases=rows,
        exact_padded_Guild_header_regression=regression,
        font_text_layout_and_Y_plus_one_unchanged=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open('out/all_routes_combined_v8865_candidate.nds').read_file('/__arm9__.bin')
    target, transform = propose(source)
    result = verify(source, target)
    result['transform'] = transform
    (OUT / 'proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    (OUT / 'target_arm9.bin').write_bytes(target)
    print(result['native_pixel_ABI_canary_cases'], 'native cases; original Guild header becomes0; fixed header remains4; complete clipped pixels pass.')


if __name__ == '__main__':
    main()
