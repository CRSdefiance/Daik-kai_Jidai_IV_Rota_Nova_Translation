"""Observe cached-direct/owner views during ordinary name editing; paired baseline."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_view_getters_v679 import Observer
from scripts.prepare_view_getters_v679 import ROM, ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--tag', default='')
    args = parser.parse_args()
    baseline = args.baseline
    assert not args.tag or args.tag.replace('_', '').isalnum()
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    controls = read(ROOT / 'native_filter_controls.json')
    assert len(controls['cases']) == 16
    assert controls['observer_sha256'] == sha(Path('scripts/observe_view_getters_v679.py').read_bytes())
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    folder = CAP / ('view_getters_v679_' + ('baseline' if baseline else 'observed') + ('_' + args.tag if args.tag else ''))
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'baseline': baseline, 'config': config,
        'runner_sha256': sha(Path(__file__).read_bytes()), 'observer_sha256': controls['observer_sha256'],
        'read_only_trace_no_battery_save_savestate_or_gameplay_fixture': True})
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer')
            observer.install()
            installed.append(observer)
            original = core.retro_run
            original.restype = None

            def run():
                observer.next_frame()
                original()
            core.retro_run = run
        return core

    if not baseline:
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']), '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V679 terminal:', 'baseline' if baseline else 'observed', flush=True)


if __name__ == '__main__':
    main()
