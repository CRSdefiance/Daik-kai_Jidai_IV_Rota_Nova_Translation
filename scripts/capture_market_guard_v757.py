"""Replay frozen V756 display scenarios against the caller-scoped V757 build."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROOT = Path('work/analysis/market_stock_release_v757')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=('one', 'two', 'edge', 'seed3', 'newgame'))
    mode = p.parse_args().mode
    suffix = 'one_seed3_756' if mode == 'seed3' else 'newgame' if mode == 'newgame' else mode + '_756'
    source = CAP / ('market_v756_' + suffix) / 'capture_report.json'
    report = read(source)
    target = CAP / ('market_v757_' + mode + ('' if mode == 'newgame' else '_verified'))
    assert not target.exists()
    inputs = ROOT / ('inputs_' + mode + '.json')
    save(inputs, report['scripted_input_schedule'])
    adapter = ('scripts/headless_desmume_v193.py' if mode == 'newgame' else
               'scripts/run_market_stock_seed_capture_v757.py' if mode == 'seed3' else
               'scripts/run_market_stock_edge_capture_v757.py' if mode == 'edge' else
               'scripts/run_market_stock_capture_v757.py')
    cmd = [sys.executable, adapter, '--rom', 'out/all_routes_combined_v757_candidate.nds',
           '--out', str(target), '--frames', str(report['frames']), '--inputs-json', str(inputs),
           '--capture-every', '100000' if mode == 'newgame' else '200', '--capture-at',
           *map(str, report['exact_requested_capture_frames'])]
    commands = []
    if mode != 'newgame':
        cmd += ['--touchscreen', '--dump-capture-ram', '--battery-save',
                report['battery_save_preloaded']['source'], '--pause-at', '3200', '--allow-market-fixtures']
        commands = [{'market_fixture': {'mode': 'one' if mode == 'seed3' else mode},
                     'until': 7200 if mode == 'seed3' else report['frames']}]
        if mode == 'seed3':
            commands.append({'market_fixture': {'mode': 'rng', 'seed': 3}, 'until': report['frames']})
        commands.append({'stop': True})
    with (ROOT / ('capture_' + mode + '_verified.log')).open('w', encoding='utf-8') as log:
        result = subprocess.run(cmd, input=''.join(json.dumps(r) + '\n' for r in commands),
                                text=True, stdout=log, stderr=subprocess.STDOUT, check=False)
    assert result.returncode == 0, (mode, result.returncode)
    print(f'{mode}: V757 cold-boot replay complete', flush=True)


if __name__ == '__main__':
    main()
