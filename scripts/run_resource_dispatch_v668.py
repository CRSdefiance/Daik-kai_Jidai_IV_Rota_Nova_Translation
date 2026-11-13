"""Ordinary current New Game with optional read-only resource request tracing."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.inspect_resource_dispatch_v668 import ROM, ROOT
from scripts.observe_resource_dispatch_v668 import Observer
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--stack', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    inputs = Path('work/analysis/compact_origin_v621/ordinary_market_inputs.json')
    assert sha(inputs.read_bytes()) == '8cd108fed119546930dd783620ed3f0857497e15f6f16153584c32a68430248c'
    suffix = 'baseline' if args.baseline else 'observed_stack' if args.stack else 'observed'
    folder = CAP / ('resource_dispatch_v668_newgame_' + suffix)
    assert not folder.exists()
    loader, installed = ct.CDLL, []

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer')
            original_run = core.retro_run
            original_run.restype = None
            observer.install()

            def run():
                observer.next_frame()
                original_run()
            core.retro_run = run
            installed.append(observer)
        return core

    if not args.baseline:
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', '24100', '--inputs-json', str(inputs), '--capture-every', '300',
        '--capture-at', '1600', '2000', '2400', '2800', '3200', '4000', '6000', '24100']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V668 ordinary New Game terminal; observer:', not args.baseline, flush=True)


if __name__ == '__main__':
    main()
