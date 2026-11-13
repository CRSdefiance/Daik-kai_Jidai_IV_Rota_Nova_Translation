"""Replay a terminal actual navigation schedule against the exact earlier ROM."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_transactions_v789')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--window',type=int,nargs=2)
    args = p.parse_args()
    source, destination = CAP/args.source, CAP/args.out
    assert not destination.exists()
    report = read(source/'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == '12a5d245dd0dee433f1c21bd97680805a54bfe4770df99d54380d39548283820'
    qualified = bool(report.get('synthetic_condition_fixtures'))
    snapshots = report.get('read_only_capture_RAM_snapshots', [])+report.get('read_only_pause_RAM_snapshots', [])
    frames = sorted({r['frame'] for r in snapshots} | {r['frame'] for r in report['frames_captured']})
    schedule = report['scripted_input_schedule']
    input_text = None
    script = 'scripts/headless_desmume_v193.py'
    extra = []
    if qualified:
        assert len(report['synthetic_condition_fixtures']) == 1
        at = report['synthetic_condition_fixtures'][0]['frame']
        journal = read(source/'navigation_command_journal.json')['commands_received']
        assert all(row['validation_passed'] for row in journal)
        assert journal[0]['frame'] == at and journal[-1]['command'].get('stop')
        schedule = [event for event in schedule if event['start'] <= at]
        input_text = '\n'.join(json.dumps(row['command']) for row in journal)+'\n'
        script = 'scripts/run_item_roles_v789.py'
        extra = ['--pause-at', str(at), '--allow-condition-fixtures', '--dump-pause-ram']
    inputs = ROOT/(args.out+'_inputs.json')
    save(inputs, schedule)
    cmd = [sys.executable, script, '--rom', 'out/all_routes_combined_v783_candidate.nds',
        '--out', str(destination), '--frames', str(report['frames']), '--inputs-json', str(inputs),
        '--battery-save', report['battery_save_preloaded']['source'], '--touchscreen', '--capture-every', '99999',
        '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram', *extra]
    if args.window: cmd += ['--capture-window',*map(str,args.window)]
    log = ROOT/(args.out+'.log')
    save(ROOT/(args.out+'_replay_plan.json'), {'source_report': str(source/'capture_report.json'),
        'source_report_sha256': sha((source/'capture_report.json').read_bytes()), 'command': cmd,
        'stdin_commands': input_text, 'log': str(log), 'qualified_three_byte_fixture': qualified,
        'plan_is_not_completion_evidence': True})
    with log.open('w', encoding='utf-8') as output:
        result = subprocess.run(cmd, input=input_text, text=True, encoding='utf-8', stdout=output, stderr=subprocess.STDOUT)
    assert result.returncode == 0, (result.returncode, str(log))
    final = read(destination/'capture_report.json')
    assert final['frames'] == report['frames'] and final['scripted_input_schedule'] == report['scripted_input_schedule']
    print(f'Exact earlier-ROM replay finished at{final["frames"]} frames:{destination}', flush=True)


if __name__ == '__main__':
    main()
