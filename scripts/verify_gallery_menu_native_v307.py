"""Original submenu flags and complete native English label glyphs."""

import json
import struct

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.gallery_menu_labels import BASE, FIELDS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_gallery_menu_v307 import ROOT
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.verify_modal_cursor_native_v272 import raster


def flags(arm, value):
    u = machine(arm)
    system = 0x02279824
    u.mem_write(system, bytes(0x100))
    u.mem_write(system + 0x38, struct.pack('<H', value))
    before = bytes(u.mem_read(system, 0x100))
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    # Original submenu's two derived flags; stop before its construction loop.
    u.emu_start(BASE + 0x41DDC, BASE + 0x41DF4, count=1000)
    assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x41DF4 and u.reg_read(UC_ARM_REG_SP) == STACK
    result = [struct.unpack('<I', u.mem_read(STACK + offset, 4))[0] for offset in (0x5C, 0x6C)]
    assert bytes(u.mem_read(system, 0x100)) == before
    return result


def main():
    source = NdsImage.open('out/all_routes_combined_v305_candidate.nds').read_file('/__arm9__.bin')
    target = (ROOT / 'research_arm9.bin').read_bytes()
    assert source[0x41DDC:0x41DF4] == target[0x41DDC:0x41DF4]
    cases, glyphs = [], []
    for value in range(16):
        a, b = flags(source, value), flags(target, value)
        assert a == b == [value & 8, int(bool(value & 15))]
        cases.append({'low_four_flags': value, 'Characters_native_enable_value': b[0], 'Event_Scenes_native_enable_value': b[1],
                      'source_gate_code_native_outputs_and_system_memory_preserved': True})
    font = GameAsciiFont.from_arm9(target)
    for ident, offset, _, _, japanese, english in FIELDS:
        raw = target[offset:].split(b'\0', 1)[0]
        assert raw == english.encode('ascii')
        actual, events, returned = raster(target, raw, width=84, height=16, wrapping=0)
        assert returned == len(raw) and [e['code'] for e in events if e['code'] != 32] == [ord(c) for c in english if c != ' ']
        expected = bytearray(84 * 16)
        for n, c in enumerate(english):
            cell = font.decode(c)
            for y in range(11):
                for x in range(6):
                    if cell.getpixel((x, y)):
                        expected[y * 84 + n * 6 + x] = 1
        assert actual == expected
        glyphs.append({'id': ident, 'Japanese': japanese, 'English': english, 'advance_width': len(raw) * 6,
                       'complete_native_glyph_pixels': sum(expected), 'all_first_final_letters_and_space_cells_bounds_guards_pass': True})
    proof = {'format': 'dk4-gallery-menu-native-label-gate-v307', 'target_arm9_sha256': sha(target),
             'native_flag_cases': cases, 'native_label_glyph_cases': glyphs,
             'all_native_unlock_logic_source_pointers_and_nonstack_system_bytes_unchanged': True,
             'flag_conditions_observed_not_claimed_as_legitimate_gameplay_unlocks': True,
             'full_hidden_Characters_Event_Scenes_actual_unlock_and_popup_layout_pending': True,
             'current_registered_release_and_Ruins_actual_popup_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All16 source flag combinations unchanged; three complete English native glyph/guard cases pass.')


if __name__ == '__main__':
    main()
