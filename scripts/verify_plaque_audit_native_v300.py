"""Refresh current-ROM conditions, skill formatting and bounded paper writes."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import FRAMEBUFFER, ORIGIN_X, ORIGIN_Y
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_modal_cursor_native_v272 import raster
from scripts.verify_sailor_status_tables_v274 import GROUPS, verify_selectors

ROOT = Path('work/analysis/plaque_audit_v300')
ROM = Path('out/all_routes_combined_v299_candidate.nds')
DIGEST = '9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    image, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = image.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert verify_selectors(arm) == verify_selectors(original)
    font, conditions = GameAsciiFont.from_arm9(arm), []
    for field, table, count, _, _ in GROUPS:
        for state in range(count):
            pointer = struct.unpack_from('<I', arm, table + state * 4)[0]
            raw = arm[pointer - BASE:].split(b'\0', 1)[0]
            source_text = original[pointer - BASE:].split(b'\0', 1)[0].decode('cp932')
            pixels, events, returned = raster(arm, raw, width=48, height=16, wrapping=0)
            assert returned == len(raw)
            assert [e['code'] for e in events if e['code'] != 32] == list(raw)
            expected = bytearray(48 * 16)
            for n, c in enumerate(raw):
                cell = font.decode(chr(c))
                for y in range(11):
                    for x in range(6):
                        if cell.getpixel((x, y)):
                            expected[y * 48 + n * 6 + x] = 1
            assert pixels == expected
            conditions.append({'field': field, 'state': state, 'Japanese': source_text,
                               'English': raw.decode('ascii'), 'complete_ink_pixels': sum(expected),
                               'all_cells_first_final_letters_native_bounds_and_guards_pass': True,
                               'actual_alternate_gameplay_state_not_claimed': True})
    u = machine(arm)
    code = MainCodeFile(arm, BASE)
    u.mem_write(POOL, bytes(code.sections[3].data[:-48]))
    names, formats = [], []
    for index, expected in enumerate(['Vigor', 'Command', 'Sailing', 'Survey', 'Finance', 'Swords', 'Aim', 'Speech', 'Guile', 'Observe']):
        call(u, 0x7EEB0, (index,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        text = bytes(u.mem_read(pointer, 24)).split(b'\0', 1)[0].decode('ascii')
        assert text == expected
        names.append(text)
        for value in (0, 9, 97, 107, 500):
            u.mem_write(0x02410000, text.encode('ascii') + b'\0')
            u.mem_write(0x02411000, struct.pack('<2I', 0x02410000, value))
            u.mem_write(0x02412000, b'\xA5' * 64)
            call(u, 0xCE898, (0x02412000, BASE + 0x148CC0, 0x02411000))
            actual = bytes(u.mem_read(0x02412000, 64)).split(b'\0', 1)[0].decode('ascii')
            assert actual == f'{text:>7}{value:3d}' and len(actual) == 10
            assert bytes(u.mem_read(0x0241200B, 53)) == b'\xA5' * 53
            formats.append([text, value, actual])
    plan = read('work/analysis/direct_equipment_v270/runtime_plan.json')
    inherited = NdsImage.open('out/all_routes_combined_v270_candidate.nds').read_file('/__arm9__.bin')
    old_pool = bytes(MainCodeFile(inherited, BASE).sections[3].data[:-48])
    assert bytes(code.sections[3].data[:len(old_pool)]) == old_pool
    # Both fresh/current and prior native states contain the original ITCM fill.
    capture = read('work/emulation_v193/plaque_audit_v300_person/capture_report.json')
    itcm_info = capture['read_only_native_state']['regions']['ITCM']
    itcm = Path(itcm_info['path']).read_bytes()
    assert sha(itcm) == itcm_info['sha256']
    u.mem_write(0x01FF8000, itcm)
    u.mem_write(ORIGIN_X, bytes(4))
    u.mem_write(ORIGIN_Y, bytes(4))
    palette = PxlImage.from_bytes(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/_pxl/towninfo.pxl')).palette
    manager, seed, cases = 0x02450000, b'\xA5' * 0x30000, []
    for screen in (0, 1):
        for width in range(10, 245):
            u.mem_write(FRAMEBUFFER - 16, b'\xA5' * (0x30000 + 32))
            u.mem_write(plan['state_pointer'], struct.pack('<I', manager))
            u.mem_write(manager + 0x18, struct.pack('<I', screen))
            u.mem_write(manager + 0x20, struct.pack('<4I', 6, 12, 6 + width, 28))
            u.mem_write(STACK, struct.pack('<3I', 255, 0, 0))
            call(u, plan['entry'] - BASE, (manager, 0, 255, 255))
            expected = bytearray(seed)
            tile = paper(width, 16, palette)
            for y in range(16):
                for x in range(width):
                    r, g, b, _ = palette[tile[y * width + x]]
                    color = 0x8000 | (r * 31 + 127) // 255 | ((g * 31 + 127) // 255) << 5 | ((b * 31 + 127) // 255) << 10
                    struct.pack_into('<H', expected, screen * 0x18000 + ((12 + y) * 256 + 6 + x) * 2, color)
            assert bytes(u.mem_read(FRAMEBUFFER, 0x30000)) == expected
            assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == bytes(u.mem_read(FRAMEBUFFER + 0x30000, 16)) == b'\xA5' * 16
            cases.append({'screen': screen, 'width': width, 'all_complete_paper_and_other_framebuffer_bytes_exact': True,
                          'original_ITCM_fill_and_owned_helper_execute_no_GPU_draw_bridge': True})
    result = {'format': 'dk4-current-plaque-native-audit-v300', 'candidate': str(ROM), 'candidate_sha256': DIGEST,
              'all512_current_selectors_exact_clean': True, 'condition_glyph_cases': conditions,
              'native_skill_names': names, 'all50_native_numeric_formatter_cases': formats,
              'all470_native_framebuffer_paper_cases': cases,
              'current_ITCM_source_snapshot': itcm_info, 'all18_plaques_and_variants_remain_incomplete': True,
              'actual_occupied_Armor_Weapon_and_alternate_health_mood_gameplay_pending': True,
              'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Current V299: 512 selectors,13 full condition rasters,50 numeric formats,470 guarded framebuffer papers pass.')


if __name__ == '__main__':
    main()
