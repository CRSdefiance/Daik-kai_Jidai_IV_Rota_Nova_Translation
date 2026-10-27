"""Source-derived town assignments; isolated native queries, not live visits."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v414_candidate.nds')
OUT = Path('work/analysis/environment_assignments_v425')


def main():
    current = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds')
    arm = current.read_file('/__arm9__.bin')
    original = clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c'
    ranges = [(0xB6674, 0xB6690), (0xB6CA0, 0xB6CCC),
              (0xB7294, 0xB7630), (0xB7C30, 0xB7C54),
              (0xB7F5C, 0xB8014), (0xB8014, 0xB80DC)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    u, old = machine(arm), machine(original)
    rows, cases = [], []
    owner = 0x02460000
    for index in range(114):
        call(u, 0xCD6B8, (index,))
        metadata = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 116))
        name_pointer = struct.unpack_from('<I', metadata)[0]
        name = bytes(u.mem_read(name_pointer, 96)).split(b'\0')[0].decode('cp932')
        style = []
        for native in (old, u):
            native.mem_write(owner, b'\xA5' * 4096)
            native.reg_write(UC_ARM_REG_R4, owner)
            native.reg_write(UC_ARM_REG_R5, index)
            native.emu_start(0x020B6674, 0x020B6690, count=12)
            assert native.reg_read(UC_ARM_REG_PC) == 0x020B6690
            expected = 1 if 58 <= index <= 60 else 0
            assert struct.unpack('<I', native.mem_read(owner + 0xFF0, 4))[0] == expected
            after = bytearray(native.mem_read(owner, 4096))
            after[0xFF0:0xFF4] = b'\xA5' * 4
            assert after == b'\xA5' * 4096
            style.append(expected)
        # Towns >=86 have development-dependent background branches. Do not
        # supply invented development fields or claim their assignments here.
        backgrounds = []
        if index < 86:
            for facility in range(12):
                outputs = []
                for native in (old, u):
                    call(native, 0xB7294, (index, facility))
                    outputs.append(native.reg_read(UC_ARM_REG_R0))
                assert outputs[0] == outputs[1]
                backgrounds.append(outputs[1])
                cases.append({'town': index, 'facility': facility, 'background': outputs[1]})
        rows.append({'town_index': index, 'name': name,
                     'metadata_sha256': sha(metadata), 'metadata_street_flag': metadata[20],
                     'alternate_facility_style': bool(style[1]),
                     'backgrounds_by_facility_0_to_11': backgrounds})
    alternate = [row for row in rows if row['alternate_facility_style']]
    assert [row['name'] for row in alternate] == ['Nagasaki', 'Osaka', 'Naha']
    retained = {}
    for resource in (32, 33, 35, 37):
        assignments = [{'town_index': row['town_index'], 'name': row['name'],
                        'facilities': [i for i, bg in enumerate(row['backgrounds_by_facility_0_to_11']) if bg == resource]}
                       for row in rows if resource in row['backgrounds_by_facility_0_to_11']]
        path = f'/towngrp/towngrp{resource:02d}.pxl'
        assert current.read_file(path) == clean.read_file(path)
        retained[str(resource)] = {'path': path, 'source_sha256': sha(current.read_file(path)),
                                   'native_assignments': assignments}
    for path in ('/_pxl/kbj04.pxl', '/_pxl/kbj08.pxl'):
        assert current.read_file(path) == clean.read_file(path)
    proof = {'format': 'dk4-environment-assignments-v425', 'candidate': str(ROM),
             'candidate_sha256': sha(ROM.read_bytes()),
             'source_exact_code_ranges': ranges,
             'style_fragment_cases_clean_and_current': 228,
             'complete_background_getter_cases_clean_and_current': len(cases) * 2,
             'alternate_facility_towns': alternate, 'retained_backgrounds': retained,
             'towns': rows, 'background_cases': cases,
             'scope': 'Original static town metadata and full native background getters for towns0-85; original style initializer fragment with supplied town index/owner. No live visits, unlocks, GPU composition or development-dependent towns86-113 are credited.',
             'ROM_or_save_modified': False, 'all18_plaques_fully_completed': False,
             'full_goal_complete': False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'assignment_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'alternate_facility_towns': [r['name'] for r in alternate],
                      'background_assignments': retained, 'native_cases': 228 + len(cases) * 2}))


if __name__ == '__main__':
    main()
