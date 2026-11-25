"""Native caption selectors, actual leader call block, and complete font pixels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/fleet_detail_v370')


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    u, font = machine(arm), GameAsciiFont.from_arm9(arm)
    # Original startup copies the inherited staging payload to its live pool.
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    u.mem_write(metrics + 4, struct.pack('<2I', 6, 16))
    header, view, ctx = 0x02450000, 0x02454000, STACK + 0x20
    profession_object, company = 0x02456000, 0x02456100
    cases = []

    def surface():
        width, height = 172, 16
        raw = struct.pack('<5I', 4, width // 4, height, 0x02453000 - header, 20)
        u.mem_write(header - 16, b'\xA5' * (20 + width * height // 2 + 32))
        u.mem_write(header, raw + bytes(width * height // 2))
        call(u, 0xD3D80, (view,))
        u.mem_write(STACK, struct.pack('<4I', width, height, 0, 0))
        call(u, 0xD3AFC, (view, header, 0, 0))
        call(u, 0xD5160, (ctx, view, 1))
        return raw

    def verify(expected, original_header):
        packed = bytes(u.mem_read(header + 20, 172 * 16 // 2))
        indices = bytes(n for b in packed for n in (b & 15, b >> 4))
        mask = bytearray(172 * 16)
        for n, ch in enumerate(expected):
            glyph = font.decode(ch)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        assert n * 6 + x < 172
                        mask[y * 172 + n * 6 + x] = 1
        assert indices == mask
        assert bytes(u.mem_read(header, 20)) == original_header
        assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + 172 * 16 // 2, 16)) == b'\xA5' * 16
        return sum(mask)

    for kind, text in enumerate(('Trader', 'Pirate', 'Soldier', 'Conqueror')):
        u.mem_write(profession_object, bytes(16))
        u.mem_write(profession_object + 9, bytes((kind,)))
        call(u, 0x3CF70, (profession_object,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(pointer, 32)).split(b'\0')[0].decode() == text
        original = surface()
        u.mem_write(company, b'Bergstrom Fleet\0')
        u.reg_write(UC_ARM_REG_R0, pointer)
        u.reg_write(UC_ARM_REG_R4, company)
        u.reg_write(UC_ARM_REG_SP, STACK)
        try:
            u.emu_start(0x0203D4F0, 0x0203D504, count=100000)
        except Exception:
            print('Native fault PC', hex(u.reg_read(UC_ARM_REG_PC)),
                  'SP', hex(u.reg_read(UC_ARM_REG_SP)),
                  'context', bytes(u.mem_read(ctx, 72)).hex())
            raise
        assert u.reg_read(UC_ARM_REG_PC) == 0x0203D504 and u.reg_read(UC_ARM_REG_SP) == STACK
        assert u.reg_read(UC_ARM_REG_R4) == company
        assert bytes(u.mem_read(company, 16)) == b'Bergstrom Fleet\0'
        expected = f'Leader ({text})'
        cases.append({'kind': kind, 'caption': expected, 'ink_pixels': verify(expected, original),
                      'actual_3D4F0_call_block_and_original_profession_getter_execute': True})
    for field in (0x37E88, 0x3D90C, 0x9C410):
        pointer = struct.unpack_from('<I', arm, field)[0]
        for value in (0, 1, 18, 19, 99, 255):
            original = surface()
            call(u, 0xD5200, (ctx, pointer, value))
            expected = f'Level {value:4d}'
            cases.append({'field': field, 'value': value, 'caption': expected,
                          'ink_pixels': verify(expected, original), 'original_printf_argument_and_pixels_exact': True})
    selector = []
    for index in (-1, *range(14)):
        call(u, 0x9D7A8, (index & 0xFFFFFFFF,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        text = bytes(u.mem_read(pointer, 48)).split(b'\0')[0].decode('ascii')
        if index == 0:
            assert text == 'Role'
        elif index == 1:
            assert text == 'Level'
        elif not 2 <= index < 12:
            assert text == 'Cancel'
        selector.append({'index': index, 'text': text})
    proof = {'native_raster_cases': cases, 'sort_selector_cases': selector,
             'all_first_final_letters_blank_cells_and_bounds_exact': True,
             'original_name_level_profession_values_and_selectors_preserved': True,
             'faction_name_preservation_in_title_requires_actual_screen_proof': True,
             'supplied_bitmap_geometry_contract': [172, 16], 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'{len(cases)} full native caption rasters and{len(selector)} original selector cases pass.')


if __name__ == '__main__':
    main()
