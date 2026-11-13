"""Full sort glyphs and exact legacy alias with input/register/flag guards."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/fleet_detail_v374')


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    u = machine(arm)
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    cases = []
    tuples = [('Hodram', 'Joachim', 'Bergstrom'), ('Hodram', 'Joakim', 'Bergstrom'),
              ('Custom', 'Joachim', 'Bergstrom'), ('Hodram', 'Joachim', 'Custom'),
              ('Hodram', 'JoachimX', 'Bergstrom'), ('Hodram', '', 'Bergstrom')]
    owner = 0x02450020
    for first, middle, last in tuples:
        raw = bytearray(b'\xA5' * 96)
        for offset, value in [(0x20, first), (0x31, last), (0x42, middle)]:
            raw[offset:offset + 17] = (value.encode() + b'\0').ljust(17, b'\0')
        u.mem_write(owner - 16, b'\xA5' * 16 + raw + b'\xA5' * 16)
        before = bytes(u.mem_read(owner - 16, 128))
        flags = u.reg_read(UC_ARM_REG_CPSR)
        call(u, 0x01FFCD00 - 0x02000000, (owner,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        result = bytes(u.mem_read(pointer, 17)).split(b'\0')[0].decode()
        expected = 'Joakim' if (first, middle, last) == tuples[0] else middle
        assert result == expected
        assert pointer == (0x0215C3D4 if (first, middle, last) == tuples[0] else owner + 0x42)
        assert bytes(u.mem_read(owner - 16, 128)) == before
        assert u.reg_read(UC_ARM_REG_CPSR) & 0xF0000000 == flags & 0xF0000000
        cases.append({'tuple': [first, middle, last], 'display_middle': result,
                      'all_fields_guards_flags_and_callee_registers_preserved': True})
    font = GameAsciiFont.from_arm9(arm)
    labels = ['Role', 'Level', 'Vigor', 'Command', 'Sailing', 'Survey',
              'Finance', 'Swords', 'Aim', 'Speech', 'Guile', 'Observe']
    header, point, text = 0x02460020, 0x02462000, 0x02462100
    width, height = 144, 36
    original = struct.pack('<5I', 4, width // 4, height, 20, 20)
    u.mem_write(header - 16, b'\xA5' * (20 + width * height // 2 + 32))
    u.mem_write(header, original + bytes(width * height // 2))
    mask = bytearray(width * height)
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    u.mem_write(metrics + 4, struct.pack('<2I', 6, 16))
    for index, label in enumerate(labels):
        x0, y0 = index % 4 * 36, index // 4 * 12
        position = struct.pack('<2I', x0, y0)
        u.mem_write(point, position)
        raw = label.encode() + b'\0'
        u.mem_write(text - 16, b'\xA5' * 16 + raw + b'\xA5' * 16)
        u.mem_write(STACK, struct.pack('<I', 1))
        call(u, 0x01FFCC00 - 0x02000000, (metrics, header, point, text))
        assert bytes(u.mem_read(point, 8)) == position
        assert bytes(u.mem_read(text - 16, len(raw) + 32)) == b'\xA5' * 16 + raw + b'\xA5' * 16
        for n, ch in enumerate(label):
            glyph = font.decode(ch)
            for y in range(11):
                for x in range(6):
                    assert x0 + n * 5 + x < x0 + 36
                    mask[(y0 + y) * width + x0 + n * 5 + x] = int(bool(glyph.getpixel((x, y))))
    packed = bytes(u.mem_read(header + 20, width * height // 2))
    actual = bytes(n for b in packed for n in (b & 15, b >> 4))
    assert actual == mask
    assert bytes(u.mem_read(header, 20)) == original
    assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + width * height // 2, 16)) == b'\xA5' * 16
    proof = {'legacy_alias_cases': cases, 'all12_sort_labels': labels,
             'full_original_glyphs_and_blank_cells_exact_in_original36_pixel_cells': True,
             'sort_header_input_points_text_buffers_and_guards_unchanged': True,
             'sort_ink_pixels': sum(mask), 'actual_playback_pending': True,
             'full_goal_complete': False}
    (ROOT / 'shim_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Six exact/custom alias cases and all12 complete sort labels pass field/flag/font/buffer guards.')


if __name__ == '__main__':
    main()
