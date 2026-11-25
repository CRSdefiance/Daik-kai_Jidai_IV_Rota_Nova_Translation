"""Replay validated journal inputs after a terminated test; no savestate loading."""

import argparse
import builtins
import json
import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_fleet_v615')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--follow-navigation', action='store_true')
    args = parser.parse_args()
    journal = read(CAP / 'regional_fleet_v615_manuel/navigation_command_journal.json')
    plan = read(ROOT / 'manuel_replay_inputs.json')
    valid, rejected = [], []
    for row in journal['commands_received']:
        frame, command = row['frame'], row['command']
        if 'touch' in command and not all(0 <= v < bound for v, bound in zip(command['touch'], (256, 192), strict=True)):
            rejected.append(row)
            continue
        valid.append(row)
        if frame >= 17400 and (command.get('buttons') or command.get('touch')):
            plan.append({'start': frame + 1, 'duration': command.get('duration', 12),
                         'buttons': command.get('buttons', []),
                         **({'touch': command['touch']} if command.get('touch') is not None else {})})
    assert rejected == [journal['commands_received'][-1]] and rejected[0]['frame'] == 24600
    pause = 24600
    folder = 'regional_fleet_v615_navigation'
    if args.follow_navigation:
        navigation = read(CAP / folder / 'navigation_command_journal.json')
        for row in navigation['commands_received']:
            command, frame = row['command'], row['frame']
            if not row.get('validation_passed') or frame < 24600:
                continue
            if command.get('buttons') or command.get('touch'):
                plan.append({'start': frame + 1, 'duration': command.get('duration', 12),
                             'buttons': command.get('buttons', []),
                             **({'touch': command['touch']} if command.get('touch') is not None else {})})
            pause = command['until']
        assert pause == 26600
        folder = 'regional_fleet_v615_stockholm'
    plan_path = ROOT / ('stockholm_resume_inputs.json' if args.follow_navigation else 'validated_resume_inputs.json')
    save(plan_path, plan)
    save(ROOT / 'rejected_navigation_and_recovery.json', {'terminal_test': 'regional_fleet_v615_manuel',
         'terminal_exit': 1, 'invalid_touch': [105, 260], 'actual_native_touch_bounds': [256, 192],
         'rejected_command_not_replayed': rejected, 'last_captured_frame': 24600,
         'new_run_is_cold_boot_replay_no_savestate': True, 'source_fixture_commands': valid[:3],
         'harness_now_validates_navigation_before_any_fixture_and_keeps_the_same_pause_on_rejection': True,
         'old_partial_run_has_no_terminal_report_and_no_completion_credit': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', 'out/all_routes_combined_v613_candidate.nds',
                '--out', str(CAP / folder), '--frames', '60000',
                '--inputs-json', str(plan_path), '--battery-save',
                'work/analysis/weapon_voyage_v476/syracuse_test_copy.dsv', '--touchscreen',
                '--pause-at', '3400', '--dump-pause-ram', '--capture-every', '999999',
                '--capture-at', '17400', '24600', '--dump-capture-ram',
                '--allow-finance-fixtures', '--allow-crew-ability-fixtures']
    commands = iter(({'company_funds': 1000000, 'until': 11400},
                     {'regional_admiral_command': 150, 'until': 17400},
                     {'regional_manuel_command': 150, 'until': pause}))
    original = builtins.input

    def next_command(*args):
        command = next(commands, None)
        return json.dumps(command) if command is not None else original(*args)

    builtins.input = next_command
    try:
        harness.main()
    finally:
        builtins.input = original


if __name__ == '__main__':
    main()
