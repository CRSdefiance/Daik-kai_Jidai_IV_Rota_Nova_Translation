"""Current captured captain data selects native M29..M32 caller arguments."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.research_graphics_file_open_v301 import DIGEST, MOVIE, ROM, ROOT
from scripts.verify_ordinary_name_fidelity_research import initialized


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x40C08:0x40C20] == clean[0x40C08:0x40C20]
    assert arm[0x7F244:0x7F270] == clean[0x7F244:0x7F270]
    cases = []
    for route, name in enumerate(('rafael', 'hodram', 'lil', 'maria')):
        path = Path(f'work/emulation_v193/reviewed_names_v299_{name}/capture_report.json')
        capture = read(path)
        expected_rom = (Path('work/analysis/reviewed_name_release_v299/maria_selection_research_only.nds')
                        if name == 'maria' else ROM)
        assert capture['ROM_sha256'] == sha(expected_rom.read_bytes())
        assert capture['cold_boot'] and not capture['savestate_loaded'] and not capture['callback_errors']
        snapshot = capture['read_only_RAM_snapshot']
        raw = Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(raw) == 0x400000 and sha(raw) == snapshot['sha256']
        cpu = initialized(arm)
        cpu.mem_write(BASE, raw)
        # This original getter/argument block does not touch a patched instruction
        # or altered static field. Captured player data remains read-only.
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        before = bytes(cpu.mem_read(BASE, 0x400000))
        cpu.emu_start(BASE + 0x40C08, MOVIE, count=10000)
        assert cpu.reg_read(UC_ARM_REG_PC) == MOVIE
        assert cpu.reg_read(UC_ARM_REG_R0) == 29 + route
        assert all(cpu.reg_read(r) == 0 for r in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3))
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK
        after = bytes(cpu.mem_read(BASE, 0x400000))
        changes = [BASE + i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
        assert all(STACK - 64 <= at < STACK for at in changes)
        cases.append({'player': name, 'captured_RAM': snapshot, 'native_FLS_index': cpu.reg_read(UC_ARM_REG_R0),
                      'native_getter_and_original_caller_argument_setup_executed': True,
                      'captured_player_data_and_all_nonstack_RAM_unchanged': True,
                      'movie_trigger_playback_or_legitimate_unlock_not_claimed': True,
                      'Maria_source_is_declared_selection_test_not_legitimate_unlock': name == 'maria'})
    formats = []
    for offset, expected in ((0x28B84, '/evstill/evstill%03u.pxl'), (0xB7270, '/towngrp/towngrp%02u.pxl')):
        instruction = struct.unpack_from('<I', arm, offset)[0]
        position = offset + 8 + (instruction & 4095) * (1 if instruction & 0x800000 else -1)
        pointer = struct.unpack_from('<I', arm, position)[0]
        raw = arm[pointer - BASE:].split(b'\0', 1)[0].decode('ascii')
        assert raw == expected
        formats.append({'caller_literal': BASE + offset, 'format_pointer': pointer, 'actual_format': raw})
    proof = {'format': 'dk4-native-graphics-caller-arguments-v301', 'candidate_sha256': DIGEST,
             'captain_dependent_movie_argument_cases': cases, 'whole_file_generated_formats': formats,
             'source_getter_and_caller_bytes_exact_clean': True,
             'scope': 'Original caller argument preparation with current captured player data; decoder, trigger, GPU and unlock behavior unproved.',
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'caller_argument_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Four actual captured captain contexts select M29..M32; whole-file formats are evstill and towngrp.')


if __name__ == '__main__':
    main()
