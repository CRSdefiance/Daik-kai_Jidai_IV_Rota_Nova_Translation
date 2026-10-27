"""Cold-boot recovery of the observed ship purchase, then interactive formation."""

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
    parser.add_argument('--admiral', action='store_true')
    parser.add_argument('--manuel', action='store_true')
    args = parser.parse_args()
    inputs = read(ROOT / 'start_inputs.json')
    # Reconstructed from the actual previous command/capture sequence; the
    # interrupted process has no terminal report and is not a completed run.
    events = [(3400, {'touch': [229, 98]}), (3800, {'buttons': ['A']}),
              (4200, {'buttons': ['A']}), (4600, {'buttons': ['B']}),
              (5000, {'touch': [128, 138]}), (5400, {'buttons': ['A']}),
              (5800, {'buttons': ['B']}), (6200, {'touch': [128, 56]}),
              (6600, {'buttons': ['A']}), (7000, {'buttons': ['A']}),
              (7400, {'buttons': ['A']}), (7800, {'buttons': ['A']}),
              (8200, {'buttons': ['A']}), (8600, {'buttons': ['Y']}),
              (9000, {'buttons': ['B']}), (9400, {'buttons': ['X']}),
              (9800, {'buttons': ['A']})]
    for frame, values in events:
        inputs.append({'start': frame + 1, 'duration': 8, 'buttons': values.get('buttons', []),
                       **({'touch': values['touch']} if 'touch' in values else {})})
    plan = ROOT / 'purchase_recovery_inputs.json'
    save(plan, inputs)
    save(ROOT / 'interrupted_purchase_run.json', {
        'interrupted_output': str(CAP / 'regional_fleet_v615_funded'),
        'last_observed_frame': 10200, 'terminal_report_missing': True,
        'process_handle_missing_and_no_Python_process_observed_before_recovery': True,
        'recovery_is_fresh_cold_boot_not_savestate': True,
        'source_fixture_funds': 1000000, 'fixture_frame': 3400,
        'captured_original_ship_purchase_sequence_retained': True, 'completion_credit': False})
    pause = 10200
    if args.admiral:
        baseline = read(CAP / 'regional_fleet_v615_formation/capture_report.json')
        assert baseline['frames'] == 11400 and not baseline['callback_errors']
        inputs = baseline['scripted_input_schedule']
        plan = ROOT / 'ability_replay_inputs.json'
        save(plan, inputs)
        pause = 11400
    if args.manuel:
        baseline = read(CAP / 'regional_fleet_v615_admiral/capture_report.json')
        assert baseline['frames'] == 17400 and not baseline['callback_errors']
        plan = ROOT / 'manuel_replay_inputs.json'
        save(plan, baseline['scripted_input_schedule'])
        pause = 11400
    folder = 'regional_fleet_v615_manuel' if args.manuel else 'regional_fleet_v615_admiral' if args.admiral else 'regional_fleet_v615_formation'
    sys.argv = ['headless_desmume_v193.py', '--rom', 'out/all_routes_combined_v613_candidate.nds',
                '--out', str(CAP / folder), '--frames', '60000',
                '--inputs-json', str(plan), '--battery-save', 'work/analysis/weapon_voyage_v476/syracuse_test_copy.dsv',
                '--touchscreen', '--pause-at', '3400', '--dump-pause-ram', '--capture-every', '999999',
                '--capture-at', '10200', '--dump-capture-ram', '--allow-finance-fixtures', '--allow-crew-ability-fixtures']
    original_input = builtins.input
    first = True
    second = args.manuel

    def next_command(*args):
        nonlocal first, second
        if first:
            first = False
            return json.dumps({'company_funds': 1000000, 'until': pause})
        if second:
            second = False
            return json.dumps({'regional_admiral_command': 150, 'until': 17400})
        return original_input(*args)

    builtins.input = next_command
    try:
        harness.main()
    finally:
        builtins.input = original_input


if __name__ == '__main__':
    main()
