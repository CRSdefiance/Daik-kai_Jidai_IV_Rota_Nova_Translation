"""Reproduce both duel actors on real captured RAM, including source origins."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.compact_bitmap_origin import FIELD, WRAPPER, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ROOT = Path('work/analysis/compact_origin_v621')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_contexts_v620_actual')


def main():
    arm = NdsImage.open('out/all_routes_combined_v617_candidate.nds').read_file('/__arm9__.bin')
    _, proof = transform(arm)
    raw = (CAP / 'frame_021200_arm9_ram.bin').read_bytes()
    itcm = (CAP / 'native_state_021200/arm9_itcm.bin').read_bytes()
    font = GameAsciiFont.from_arm9(arm)
    asset, pixels, width, height = 0x022BD83C, 0x022BFDD0, 464, 96
    cases = []
    for patched in (False, True):
        for index, supplied_origin in [(i, o) for i in (0, 1) for o in (None, (0, 0), (20, 48), (300, 72))]:
            u = machine(arm)
            u.mem_write(BASE, raw)
            u.mem_write(0x01FF8000, itcm)
            if patched:
                u.mem_write(BASE + FIELD, struct.pack('<I', WRAPPER))
            origin = supplied_origin or (0, 24 + index * 12)
            if supplied_origin is not None:
                view = 0x0218D4D8 + 0x3C + index * 0xA4 + 0x14
                u.mem_write(view + 0x1C, struct.pack('<2I', *origin))
            # Leave every other source row unchanged; a view-local clear must
            # not clear the title/name rows or the other actor's stat row.
            before = bytes(u.mem_read(pixels, width * height // 2))
            glyphs = []

            def trace(uc, address, size, data, glyphs=glyphs):
                if address == BASE + 0xD16B4:
                    code, color = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
                    glyphs.append((code, color, uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3)))

            handle = u.hook_add(UC_HOOK_CODE, trace)
            executed = call(u, 0xD54C, (0x0218D4D8, index), instruction_limit=1000000)
            u.hook_del(handle)
            assert all(code < 128 and color == 1 for code, color, _, _ in glyphs)
            expected_x, expected_y = origin if patched else (0, 0)
            assert [x for _, _, x, _ in glyphs] == list(range(expected_x, expected_x + 5 * len(glyphs), 5))
            assert {y for _, _, _, y in glyphs} == {expected_y}
            assert {BASE + x for x in (0xD54C, 0xE290, 0xD393C, 0xD5160, 0xD5404, 0xD5140)} <= executed
            if patched:
                assert WRAPPER in executed
                expected = bytearray(before)
                for y in range(expected_y, expected_y + 12):
                    start = (y * width + expected_x) // 2
                    expected[start:start + 78] = bytes(78)
                for code, color, x, y in glyphs:
                    mask = font.decode(chr(code))
                    for yy in range(11):
                        for xx in range(6):
                            if mask.getpixel((xx, yy)):
                                pos = (y + yy) * width + x + xx
                                expected[pos // 2] |= color << (4 * (pos % 2))
                assert bytes(u.mem_read(pixels, len(before))) == expected
                assert bytes(u.mem_read(asset, 20)) == raw[asset - BASE:asset - BASE + 20]
            cases.append({'patched': patched, 'actor_index': index,
                          'complete_text': ''.join(chr(g[0]) for g in glyphs),
                          'source_origin': list(origin), 'controlled_origin': supplied_origin is not None,
                          'native_origin': [expected_x, expected_y], 'plane_sha256': sha(bytes(u.mem_read(pixels, len(before)))), 'glyph_count': len(glyphs),
                          'real_parent_source_view_and_original_getters_executed': True,
                          'full_plane_independent_font_and_untouched_rows_exact': patched,
                          'not_actual_emulator_display_or_earned_outcome': True})
    zero_cases = [c for c in cases if c['controlled_origin'] and c['source_origin'] == [0, 0]]
    for index in (0, 1):
        pair = [c for c in zero_cases if c['actor_index'] == index]
        assert len(pair) == 2 and pair[0]['plane_sha256'] == pair[1]['plane_sha256']
    ROOT.mkdir(exist_ok=True)
    result = {'transform': proof, 'RAM_sha256': sha(raw), 'ITCM_sha256': sha(itcm),
              'script_sha256': sha(Path(__file__).read_bytes()), 'cases': cases,
              'old_callback_reproduces_name_row_overwrite': True,
              'new_callback_preserves_both_original_stat_row_origins': True,
              'full_goal_complete': False}
    (ROOT / 'actual_parent_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(cases, indent=2))


if __name__ == '__main__':
    main()
