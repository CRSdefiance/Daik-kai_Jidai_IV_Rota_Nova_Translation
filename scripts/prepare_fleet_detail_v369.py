"""Research-only complete fleet/faction Level and leader captions."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/fleet_detail_v369')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v366_candidate.nds')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm = rom.read_file('/__arm9__.bin')
    code = MainCodeFile(arm, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    rows = []
    for field, offset, jp, en in [(0x37E88, 0x13710C, 'レベル%4d', 'Level %4d'),
                                  (0x3D90C, 0x137904, 'レベル %4d', 'Level %4d'),
                                  (0x9C410, 0x14FBA8, 'レベル%4d', 'Level %4d'),
                                  (0x9D800, 0x14FBCC, 'レベル', 'Level'),
                                  (0x9D7FC, 0x14FBC4, '担　当', 'Role'),
                                  (0x9D804, 0x14FBD4, 'キャンセル', 'Cancel')]:
        raw, replacement = jp.encode('cp932') + b'\0', en.encode() + b'\0'
        assert len(replacement) <= len(raw)
        assert arm[offset:offset + len(raw)] == clean[offset:offset + len(raw)] == raw
        assert struct.unpack_from('<I', arm, field)[0] == 0x02000000 + offset
        code.sections[0].data[offset:offset + len(raw)] = replacement.ljust(len(raw), b'\0')
        rows.append({'field': field, 'offset': offset, 'Japanese': jp, 'English': en,
                     'source_hex': raw.hex(), 'replacement_hex': replacement.ljust(len(raw), b'\0').hex(),
                     'native_arguments_preserved': True})
    field, offset, jp, en = 0x3D908, 0x1378F4, '%s総帥（%s）', 'Leader (%s)'
    raw = jp.encode('cp932') + b'\0'
    assert arm[offset:offset + len(raw)] == clean[offset:offset + len(raw)] == raw
    assert struct.unpack_from('<I', arm, field)[0] == 0x02000000 + offset
    assert code.sections[4].ramAddress == 0x01FFC000
    pointer = code.sections[4].ramAddress + len(before[4])
    code.sections[4].data.extend(en.encode() + b'\0')
    code.sections[4].data.extend(bytes(-len(code.sections[4].data) % 4))
    assert len(code.sections[4].data) <= 0x1000
    struct.pack_into('<I', code.sections[0].data, field, pointer)
    rows.append({'field': field, 'offset': offset, 'Japanese': jp, 'English': en,
                 'pointer': pointer, 'source_hex': raw.hex(), 'faction_name_preserved_in_existing_title_bar': True, 'profession_getter_preserved': True,
                 'localization_note': 'Faction title already displays the organization name. Leader (profession) beneath it retains both fields once and avoids clipping a duplicated name; individual fleet Admiral remains distinct.'})
    argument_field = 0x3D4F8
    assert struct.unpack_from('<I', arm, argument_field)[0] == 0xE1A02004
    struct.pack_into('<I', code.sections[0].data, argument_field, 0xE1A02003)
    target = bytes(code.save())
    loaded = MainCodeFile(target, 0x02000000)
    assert all(bytes(loaded.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(loaded.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(loaded.sections[0].data)
    for row in rows[:-1]:
        o = row['offset']; original = bytes.fromhex(row['source_hex'])
        restored[o:o + len(original)] = original
    restored[field:field + 4] = arm[field:field + 4]
    restored[argument_field:argument_field + 4] = arm[argument_field:argument_field + 4]
    o = code.codeSettingsOffs
    restored[o:o + 12] = before[0][o:o + 12]
    assert bytes(restored) == before[0]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    rom.replace_file('/__arm9__.bin', target)
    rom.save(ROOT / 'research_only_fleet_detail.nds')
    (ROOT / 'plan.json').write_text(json.dumps({'source_arm9_sha256': sha(arm), 'target_arm9_sha256': sha(target),
        'records': rows, 'profession_argument_field': argument_field, 'argument_before': 0xE1A02004, 'argument_after': 0xE1A02003, 'all_inherited_components_and_heap_bounds_preserved': True,
        'native_and_actual_caption_fit_pending': True, 'not_for_handoff': True,
        'full_goal_complete': False}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = json.loads(Path('work/emulation_v193/equipment_search_v367/capture_report.json').read_text())
    (ROOT / 'replay_inputs.json').write_text(json.dumps(report['scripted_input_schedule'], indent=2) + '\n')
    print('Prepared seven source-reviewed caption corrections; native and actual fit still required.')


if __name__ == '__main__':
    main()
