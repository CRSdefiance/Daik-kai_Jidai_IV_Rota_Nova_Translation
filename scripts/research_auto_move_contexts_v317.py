"""Original Auto Move pointer owners and complete proposed Stop footer raster."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import BASE, machine
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/auto_move_contexts_v317')
ROM = Path('out/all_routes_combined_v316_candidate.nds')
FIELDS = (0x11911C, 0x1451EC, 0x1451F8, 0x147A48, 0x14DEF8)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    pool = bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48])
    rows = []
    for offset in FIELDS:
        needle = struct.pack('<I', 0x02000000 + offset)
        refs = []
        for field in range(len(original) - 3):
            if original[field:field + 4] != needle:
                continue
            pointer = struct.unpack_from('<I', arm, field)[0]
            if 0x02387A20 <= pointer < 0x02387A20 + len(pool):
                data = pool[pointer - 0x02387A20:]
            else:
                assert 0x02000000 <= pointer < 0x02000000 + len(arm)
                data = arm[pointer - 0x02000000:]
            text = data.split(b'\0', 1)[0].decode('cp932')
            refs.append({'original_owner_field': field, 'current_pointer': pointer,
                         'current_text': text, 'already_relocated': pointer != 0x02000000 + offset})
        assert len(refs) == 1
        rows.append({'original_offset': offset, 'Japanese': original[offset:].split(b'\0', 1)[0].decode('cp932'),
                     'owners': refs})
    assert sum(r['owners'][0]['already_relocated'] for r in rows) == 4
    target = bytearray(arm)
    assert arm[0x147A48:0x147A58] == ('自動移動停止'.encode('cp932') + b'\0').ljust(16, b'\0')
    target[0x147A48:0x147A58] = b'Stop Auto Move\0\0'
    assert struct.unpack_from('<2I', arm, 0xCA7A8) == (0xE1A010A0, 0xE3A0000C)
    # Byte count times6 retains12-pixel CP932 pairs and includes every odd
    # ASCII character. The previous floor(bytes/2)*12 lost the last cell.
    assert struct.unpack_from('<I', arm, 0xCA7B0)[0] == 0xE0040091
    struct.pack_into('<I', target, 0xCA7A8, 0xE0801080)  # r1 = bytes*3
    struct.pack_into('<I', target, 0xCA7B0, 0xE1A04081)  # r4 = r1*2
    # Preserve r0=12 because it also supplies the native surface height.
    assert len(target) == len(arm)
    (ROOT / 'proposed_arm9.bin').write_bytes(target)
    cases = []
    for mode in (4, 16):
        result = execute(bytes(target), 'unused', footer_table=0x11914C, mode=mode)
        texts = [r['text'] for r in result['footer_draws']]
        consumed = ''.join(texts)
        assert 'Stop Auto Move' in texts, texts
        assert result['pixels'] == expected_pixels(bytes(target), consumed, 0, 0, mode, advance=6)
        placements = []
        for slot in range(6):
            left, width, source_x = result['footer_metadata'][slot * 3:slot * 3 + 3]
            if left != -1:
                assert 0 <= left < left + width <= 256
                placements.append({'slot': slot, 'left': left, 'width': width, 'source_x': source_x})
        ordered = sorted(placements, key=lambda row: row['left'])
        assert all(a['left'] + a['width'] <= b['left'] for a, b in pairwise(ordered))
        cases.append({'mode': mode, 'draws': texts, 'placements': placements,
                      'complete_native_pixels_sha256': sha(result['pixels']),
                      'complete_native_footer_raster_bounds_and_return_pass': True})
    widths = []
    for count in range(129):
        values = []
        for source in (arm, bytes(target)):
            u = machine(source)
            u.reg_write(UC_ARM_REG_R0, count)
            u.emu_start(BASE + 0xCA7A8, BASE + 0xCA7B4, count=3)
            values.append(u.reg_read(UC_ARM_REG_R4))
            assert u.reg_read(UC_ARM_REG_R0) == 12
        assert values == [(count // 2) * 12, count * 6]
        if count % 2 == 0:
            assert values[0] == values[1]
        widths.append({'bytes': count, 'original_width': values[0], 'proposed_width': values[1],
                       'native_surface_height12_preserved': True})
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'original_to_current_label_owners': rows, 'proposed_target_arm9_sha256': sha(target),
             'native_proposed_Stop_Auto_Move_footer_cases': cases,
             'current_ROM_Stop_label_still_Japanese': True,
             'current_ROM_odd_ASCII_footer_width_floors_the_last_cell': True,
             'proposed_measurement_byte_count_times6_CP932_pair_width_retained': True,
             'native_measurement_cases': widths,
             'four_retained_Japanese_literals_already_relocated_to_English': True,
             'physical_Auto_Move_Stop_footer_not_yet_reached': True,
             'proposed_change_research_only_not_integrated': True, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'owners': rows, 'footer_cases': cases}, ensure_ascii=False))


if __name__ == '__main__':
    main()
