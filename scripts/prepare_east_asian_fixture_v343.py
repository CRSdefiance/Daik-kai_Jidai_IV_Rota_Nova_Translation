"""Current-ROM one-byte fourth-captain exposure; research only, not an unlock."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R10, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path('work/analysis/east_asian_town_v343')
PARENT = Path('out/all_routes_combined_v342_candidate.nds')
OPCODE, OBJECT = 0x9F068, 0x02460000


def main():
    rom = NdsImage.open(PARENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert struct.unpack_from('<I', arm, OPCODE)[0] == 0x03A00003
    assert arm[0x46DFC:0x46E30] == clean[0x46DFC:0x46E30]
    saved_object = struct.unpack_from('<I', arm, 0x9F0D0)[0]
    fixture = bytearray(arm)
    struct.pack_into('<I', fixture, OPCODE, 0x03A00004)
    fixture = bytes(fixture)
    assert [i for i, (a, b) in enumerate(zip(arm, fixture)) if a != b] == [OPCODE]
    cases = []
    for payload, variant in [(arm, 'original'), (fixture, 'research')]:
        u = machine(payload)
        for flags in range(16):
            for initial in (2, 3, 4, 0xA5A5A5A5):
                u.mem_write(saved_object + 0x38, struct.pack('<H', flags))
                u.mem_write(OBJECT - 16, b'\xA5' * (0x940 + 32))
                u.mem_write(OBJECT + 0x930, struct.pack('<I', initial))
                before = bytes(u.mem_read(OBJECT - 16, 0x940 + 32))
                u.reg_write(UC_ARM_REG_R10, OBJECT)
                u.reg_write(UC_ARM_REG_SP, STACK)
                u.emu_start(0x0209F05C, 0x0209F070, count=1000)
                expected = (3 if variant == 'original' else 4) if flags == 0 else initial
                assert struct.unpack('<I', u.mem_read(OBJECT + 0x930, 4))[0] == expected
                assert u.reg_read(UC_ARM_REG_PC) == 0x0209F070 and u.reg_read(UC_ARM_REG_SP) == STACK
                after = bytearray(u.mem_read(OBJECT - 16, 0x940 + 32))
                after[0x940:0x944] = before[0x940:0x944]
                assert bytes(after) == before
                assert bytes(u.mem_read(saved_object + 0x38, 2)) == struct.pack('<H', flags)
                cases.append({'variant': variant, 'flags': flags, 'initial_count': initial, 'result': expected})
    before = {path: raw for _, path, raw in rom.iter_files()} | dict(rom.iter_components())
    rom.replace_file('/__arm9__.bin', fixture)
    output = ROOT / 'research_only_Maria_selection_v343.nds'
    rom.save(output)
    checked = NdsImage.open(output)
    after = {path: raw for _, path, raw in checked.iter_files()} | dict(checked.iter_components())
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    assert checked.read_file('/__arm9__.bin') == fixture
    inputs = [{'start': 1000, 'duration': 12, 'buttons': ['START']},
              {'start': 1200, 'duration': 12, 'buttons': ['A']}]
    (ROOT / 'fixture_inputs.json').write_text(json.dumps(inputs, indent=2) + '\n')
    proof = {'parent': str(PARENT), 'parent_sha256': sha(PARENT.read_bytes()),
             'research_ROM': str(output), 'research_ROM_sha256': sha(output.read_bytes()),
             'only_changed_instruction_byte': OPCODE, 'native_selection_cases': cases,
             'save_flags_not_changed': True, 'all_other_code_files_components_exact_parent': True,
             'not_a_legitimate_unlock_or_registered_release': True, 'not_for_handoff': True}
    (ROOT / 'selection_fixture_manifest.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps({'native_cases': len(cases), 'one_research_byte': True, 'parent_unchanged': True}))


if __name__ == '__main__':
    main()
