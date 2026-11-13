"""Current ordinary UI sequences with optional primitive-entry observation."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.inspect_graphic_paints_v669 import ROM, ROOT
from scripts.observe_graphic_paints_v669 import Observer
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('newgame', 'equipment'), default='newgame')
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--tag', default='')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert not args.tag or args.tag.replace('_', '').isalnum()
    suffix = ('_' + args.tag) if args.tag else ''
    folder = CAP / f"graphic_paints_v669_{args.case}_{'baseline' if args.baseline else 'observed'}{suffix}"
    assert not folder.exists()
    if args.case == 'newgame':
        inputs = Path('work/analysis/compact_origin_v621/ordinary_market_inputs.json')
        frames, every, selected, donor = 24100, 300, [1600, 2000, 2400, 2800, 3200, 4000, 6000, 24100], None
        assert sha(inputs.read_bytes()) == '8cd108fed119546930dd783620ed3f0857497e15f6f16153584c32a68430248c'
    else:
        old = read('work/analysis/equipment_cursor_v663/preflight.json')
        inputs, frames, every = Path('work/analysis/equipment_cursor_v663/inputs.json'), 8063, 999999
        selected = [4300, 6300] + [f for s in (6400, 6800, 7200, 7600, 8000) for f in range(s, s + 64)]
        donor = old['donor']
        assert sha(Path(donor).read_bytes()) == old['donor_sha256']
    folder.mkdir()
    save(folder / 'run_contract.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'case': args.case, 'baseline': args.baseline, 'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()),
        'frames': frames, 'donor': donor, 'donor_sha256': sha(Path(donor).read_bytes()) if donor else None,
        'runner_sha256': sha(Path(__file__).read_bytes()), 'no_savestate_or_gameplay_fixtures': True})
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
        '--frames', str(frames), '--inputs-json', str(inputs), '--touchscreen',
        '--capture-every', str(every), '--capture-at', *map(str, selected)]
    if donor:
        sys.argv += ['--battery-save', donor]
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V669 terminal:', args.case, 'observed:', not args.baseline, flush=True)


if __name__ == '__main__':
    main()
