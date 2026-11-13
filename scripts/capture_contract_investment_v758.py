"""Unmodified investment amount dialog checks relocated caption bytes in use."""

import argparse
import subprocess
import sys
from pathlib import Path

from scripts.review_market_contract_v758 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--version', type=int, choices=(757, 758), required=True)
    version = p.parse_args().version
    target = Path('E:/Rota Nova translations/Generated/work/emulation_v193') / f'market_contract_v758_investment_{version}'
    assert not target.exists()
    events = [r for r in read('work/analysis/market_replies_v753/inputs_invest_probe.json') if r['start'] <= 5201]
    inputs = ROOT / f'inputs_investment_{version}.json'
    save(inputs, events)
    cmd = [sys.executable, 'scripts/headless_desmume_v193.py', '--rom', f'out/all_routes_combined_v{version}_candidate.nds',
           '--out', str(target), '--frames', '5600', '--inputs-json', str(inputs), '--touchscreen',
           '--capture-every', '200', '--capture-at', '3200', '4800', '5200', '5400', '5600', '--dump-capture-ram',
           '--battery-save', 'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv']
    with (ROOT / f'capture_investment_{version}.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)
    assert result.returncode == 0
    print(f'V{version} investment amount caption cold boot completed', flush=True)


if __name__ == '__main__':
    main()
