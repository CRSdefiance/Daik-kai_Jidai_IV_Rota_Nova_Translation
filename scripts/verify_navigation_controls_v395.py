"""Matched actual D-pad heading tests and the original eight-way selector fragment."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R10, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine
from scripts.read_navigation_snapshot_v391 import inspect

ROOT = Path('work/analysis/navigation_controls_v395')
ROM = Path('out/all_routes_combined_v388_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x76A4C:0x76B34] == clean[0x76A4C:0x76B34]
    digest = sha(ROM.read_bytes())
    u = machine(arm)
    owner = 0x02460000
    source_cases = []
    for held, angle in [(0x1000, 0), (0x3000, 32), (0x2000, 64), (0x6000, 96),
                        (0x4000, 128), (0xC000, 160), (0x8000, 192), (0x9000, 224)]:
        u.mem_write(owner + 0x50B4, struct.pack('<I', held))
        u.mem_write(STACK, b'\xA5' * 32)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R10, owner)
        u.emu_start(0x02076A4C, 0x02076B28, count=100)
        assert u.reg_read(UC_ARM_REG_PC) == 0x02076B28
        expected = bytearray(b'\xA5' * 32)
        expected[8] = angle
        assert bytes(u.mem_read(STACK, 32)) == expected
        assert bytes(u.mem_read(owner + 0x50B4, 4)) == struct.pack('<I', held)
        source_cases.append({'held_bits': held, 'target_angle': angle})

    cases = []
    baseline = None
    loading = read(Path('work/analysis/navigation_touch_v386/loading_only_inputs_v391.json'))
    for key, angle in [('up', 0), ('right', 64), ('down', 128), ('left', 192)]:
        folder = Path('work/emulation_v193') / f'navigation_controls_v395_{key}'
        report_path = folder / 'capture_report.json'
        r = read(report_path)
        assert r['ROM_sha256'] == digest and r['frames'] == 6128
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        assert r['scripted_input_schedule'] == loading + [{'start': 6001, 'duration': 128, 'buttons': [key.upper()]}]
        captures = {}
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            if row['frame'] <= 6000:
                captures[row['frame']] = row['PNG_sha256']
        if baseline is None:
            baseline = captures
        assert captures == baseline
        snapshot = r['read_only_RAM_snapshot']
        assert snapshot['read_only_export']
        sample = inspect(Path(snapshot['path']), ROM)
        assert sample['snapshot_sha256'] == snapshot['sha256']
        assert sample['direction_byte'] == angle
        cases.append({'button': key.upper(), 'actual_direction_byte': angle,
                      'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
                      'same_genuine_donor_sha256': r['battery_save_preloaded']['source_sha256'],
                      'whole_pre_input_frames': sorted(captures), 'ship_sample': sample})
    assert len({r['same_genuine_donor_sha256'] for r in cases}) == 1
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'original_eight_way_selector_fragment_cases': source_cases,
             'fragment_start': 0x02076A4C, 'fragment_stop_before_rudder_call': 0x02076B28,
             'held_word_and_owner_and_fragment_entry_are_explicit_native_contracts': True,
             'full_controller_touch_gate_turn_rate_not_claimed': True,
             'actual_matched_cold_boot_direction_cases': cases,
             'all18_whole_pre_input_frames_equal_across_four_runs': len(baseline) == 18,
             'cardinal_buttons_reach_original_selected_angles': True,
             'not_a_free_rotation_command': True,
             'land_collision_and_ongoing_sailing_can_change_later_heading': True,
             'no_port_or_equipment_acquisition_proved_here': True,
             'ROM_changed': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    assert len(baseline) == 18
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Eight original selection fragments and four actual cardinal controls pass; all18 earlier frames match.')


if __name__ == '__main__':
    main()
