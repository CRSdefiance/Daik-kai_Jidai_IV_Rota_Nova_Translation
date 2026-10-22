"""Paired actual Market refusal/advice scenes and fixture-free New Game."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from scripts.review_market_contract_v758 import ROOT
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=('palace', 'governor', 'advice', 'newgame'))
    p.add_argument('--version', type=int, choices=(757, 758), required=True)
    args = p.parse_args()
    target = CAP / f'market_contract_v758_{args.mode}_{args.version}'
    assert not target.exists()
    original = read('work/analysis/market_stock_release_v756/inputs_trade_stock_final.json')
    events = [r for r in original if r['start'] <= 4401]
    frames = 6001 if args.mode == 'advice' else 5601
    events += [{'start': 4801, 'duration': 8, 'buttons': ['A']}, {'start': 5201, 'duration': 8, 'buttons': ['B']}]
    if args.mode == 'advice':
        events.append({'start': 5601, 'duration': 8, 'buttons': ['B']})
    if args.mode == 'newgame':
        events = read(CAP / 'market_v757_newgame/capture_report.json')['scripted_input_schedule']
        frames = 4000
    input_path = ROOT / f'inputs_{args.mode}_{args.version}.json'
    save(input_path, events)
    adapter = 'scripts/run_market_contract_capture_v758.py' if args.mode in ('governor', 'advice') else 'scripts/headless_desmume_v193.py'
    cmd = [sys.executable, adapter, '--rom', f'out/all_routes_combined_v{args.version}_candidate.nds',
           '--out', str(target), '--frames', str(frames), '--inputs-json', str(input_path),
           '--capture-every', '100000' if args.mode == 'newgame' else '200', '--capture-at']
    commands = []
    if args.mode == 'newgame':
        cmd += ['1600', '2000', '3200', '4000']
    else:
        captures = [3200, 4400, 4800, 5200, 5600] + ([6000] if args.mode == 'advice' else [])
        cmd += [*map(str, captures), '--touchscreen', '--dump-capture-ram', '--battery-save',
                'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv']
        if args.mode in ('governor', 'advice'):
            cmd += ['--pause-at', '3200', '--allow-market-fixtures']
            commands = [{'market_fixture': {'mode': args.mode}, 'until': frames}, {'stop': True}]
    with (ROOT / f'capture_{args.mode}_{args.version}.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(cmd, input=''.join(json.dumps(r) + '\n' for r in commands), text=True,
                                stdout=log, stderr=subprocess.STDOUT, check=False)
    assert result.returncode == 0, (args.mode, args.version, result.returncode)
    print(f'{args.mode} V{args.version} cold boot completed', flush=True)


if __name__ == '__main__':
    main()
