"""Freeze fresh cold-boot schedules and source-checked location fixtures."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_full_fleet_proximity_v653 import apply_fixture
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/queued_portrait_wrap_v653')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    rom = Path('out/all_routes_combined_v653_candidate.nds')
    arm = NdsImage.open(rom).read_file('/__arm9__.bin')
    configs = {}
    for case, old_run, frames, inputs, donor in (
        ('staffing', 'full_fleet_staffing_v652_actual', 19600,
         'work/analysis/full_fleet_battle_v652/full_inputs.json',
         read('work/analysis/full_fleet_battle_v652/preflight.json')['donor']),
        ('battle', 'full_fleet_battle_v652_near_target', 23600,
         'work/analysis/full_fleet_battle_v652/departure_prefix.json',
         read('work/analysis/full_fleet_battle_v652/staffing_proof.json')['prepared_save']['path']),
    ):
        report = read(CAP / old_run / 'capture_report.json')
        configs[case] = {'ROM': str(rom), 'ROM_sha256': sha(rom.read_bytes()),
            'output': str(CAP / ('queued_portrait_v653_' + case)),
            'baseline_report': str(CAP / old_run / 'capture_report.json'),
            'baseline_report_sha256': sha((CAP / old_run / 'capture_report.json').read_bytes()),
            'frames': frames, 'inputs': inputs, 'inputs_sha256': sha(Path(inputs).read_bytes()),
            'donor': donor, 'donor_sha256': sha(Path(donor).read_bytes()),
            'capture_frames': sorted({s['frame'] for s in report['frames_captured']}),
            'capture_every': 999999}
    original = read(CAP / 'full_fleet_battle_v652_near_target/navigation_command_journal.json')
    terminal = read(configs['battle']['baseline_report'])
    assert terminal['frames'] == 23600 and not terminal['callback_errors']
    assert original['commands_received'][-1]['command']['stop']
    commands = []
    for row in original['commands_received']:
        assert row['validation_passed']
        command = dict(row['command'])
        if row['frame'] == 15200:
            command['export_native_state'] = True
        commands.append(command)
    save(ROOT / 'battle_commands.json', commands)
    configs['battle']['commands'] = str(ROOT / 'battle_commands.json')
    configs['battle']['commands_sha256'] = sha((ROOT / 'battle_commands.json').read_bytes())
    configs['battle']['max_frames'] = 120000
    fixtures = []
    for frame in (4800, 5200):
        raw = (CAP / 'full_fleet_battle_v652_near_target' / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        after, proof = apply_fixture(arm, raw, 'approach')
        assert len(proof['owned_bytes']) == 8 and len(proof['changes']) == 4
        assert proof['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
        assert sha(after) == proof['after_RAM_sha256']
        fixtures.append({'frame': frame, 'offline_same_original_V652_RAM': True, 'proof': proof})
    try:
        apply_fixture(arm[:-1], raw, 'approach')
    except ValueError:
        pass
    else:
        raise AssertionError('Wrong ARM code accepted')
    cfg = dict(read('work/analysis/captain_prompt_wrap_v651/run_configs.json')['newgame_candidate'])
    cfg.update({'ROM': str(rom), 'ROM_sha256': sha(rom.read_bytes()),
                'output': str(CAP / 'queued_portrait_v653_newgame'),
                'baseline_report': str(Path(cfg['output']) / 'capture_report.json')})
    cfg['baseline_report_sha256'] = sha(Path(cfg['baseline_report']).read_bytes())
    configs['newgame'] = cfg
    save(ROOT / 'run_configs.json', configs)
    save(ROOT / 'fixture_preapply_proof.json', {
        'positive_offline_cases': fixtures, 'wrong_ARM_rejected': True,
        'fixture_source': 'scripts/native_full_fleet_proximity_v653.py',
        'fixture_source_sha256': sha(Path('scripts/native_full_fleet_proximity_v653.py').read_bytes()),
        'no_frontend_or_fixture_edits_after_live_start': True, 'full_goal_complete': False})
    print('V653 cold-boot schedules and exact coordinate-only fixture source frozen.')


if __name__ == '__main__':
    main()
