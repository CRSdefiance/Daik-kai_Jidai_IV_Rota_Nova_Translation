"""Verify ordinary committed staffing/repair and retain both formatting findings."""

from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/full_fleet_battle_v652')
RUN = Path('E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_staffing_v652_actual')


def main():
    pre, report = read(ROOT / 'preflight.json'), read(RUN / 'capture_report.json')
    assert report['frames'] == 19600 and report['ROM_sha256'] == pre['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    snapshots = {r['frame']: r for r in report['read_only_pause_RAM_snapshots']}
    arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    rows = []
    for frame in (3200, 10200, 11200, 14000, 16800, 19600):
        s = snapshots[frame]
        raw = Path(s['path']).read_bytes()
        assert s['read_only_export'] and sha(raw) == s['sha256']
        u = machine(arm)
        u.mem_write(BASE, raw)

        def get(offset, args=(), cpu=u):
            call(cpu, offset, args)
            return cpu.reg_read(UC_ARM_REG_R0)

        assert get(0x2E58C) == 1
        fleet = get(0xCB1A8) + 4 + 0x84
        ships = []
        for slot in range(5):
            model = get(0x36C94, (fleet + 12 + slot * 8,))
            assert model
            ships.append({'slot': slot, 'model': model,
                          'name': bytes(u.mem_read(model + 8, 24)).split(b'\0')[0].decode('ascii'),
                          'Hull': get(0x183A0, (model,)), 'Crew': get(0x181BC, (model,))})
        expected = [(48, 19)] + [(25, 0)] * 4 if frame <= 11200 else [(48 if frame == 14000 else 60, 49)] + [(25, 19)] * 4
        assert [(s['Hull'], s['Crew']) for s in ships] == expected
        rows.append({'frame': frame, 'ships': ships, 'RAM_sha256': s['sha256']})
    saved = Path(report['battery_save_preloaded']['destination'])
    assert saved.read_bytes().endswith(b'|-DESMUME SAVE-|')
    assert sha(saved.read_bytes()) != pre['donor_sha256']
    save(ROOT / 'full_inputs.json', report['scripted_input_schedule'])
    save(ROOT / 'staffing_proof.json', {'candidate_sha256': pre['candidate_sha256'],
        'report': str(RUN / 'capture_report.json'), 'report_sha256': sha((RUN / 'capture_report.json').read_bytes()),
        'terminal_frames': 19600, 'no_savestate_or_gameplay_fixtures': True,
        'ordinary_committed_ship_states': rows, 'total_committed_crew': 125,
        'preview_does_not_change_persisted_models_until_original_confirmation': True,
        'source_donor_and_ROM_patch_registry_all_unchanged': True,
        'prepared_save': {'path': str(saved), 'sha256': sha(saved.read_bytes()),
                          'ordinary_slot6_Save_in_isolated_copy': True, 'cold_reload_pending': True},
        'new_visible_word_split_findings': [
            {'frame': 5200, 'native_ID': 890, 'source_table': 0x02118380, 'word': 'coins'},
            {'frame': 12800, 'native_ID': 71, 'source_table': 0x02117460, 'word': 'that'}],
        'original_recruitment_confirmation_call': 0x02057484,
        'original_queued_role_parent_return': 0x02053D24,
        'native_unassigned_table_actual_role_parent_still_to_bind': True,
        'miniature_Confirm_parents_and_actual_full_fleet_battle_rewards_still_open': True,
        'all18_plaques_incomplete_22_historical_scopes_retained': True, 'full_goal_complete': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V652:ordinary125 committed crew,full repair60/49,five valid saved models;two word-wrap findings retained.')


if __name__ == '__main__':
    main()
