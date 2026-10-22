"""Trace all Event Scenes plus ordinary raw-reader positive control, with baselines."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_file_requests_v681 import Observer
from scripts.prepare_file_requests_v681 import ROM, ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('gallery', 'ordinary'))
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    assert controls['observer_sha256'] == sha(Path('scripts/observe_file_requests_v681.py').read_bytes())
    config = read(ROOT / 'run_cases.json')[args.case]
    folder = CAP / f"file_requests_v681_{args.case}_{'baseline' if args.baseline else 'observed'}"
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': args.case, 'baseline': args.baseline, 'config': config,
        'inputs_sha256': sha(Path(config['inputs']).read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'observer_sha256': controls['observer_sha256'],
        'gallery_uses_byte_exact_authorized_system_unlock_save_not_earned_unlock': args.case == 'gallery'})
    loader, installed = ct.CDLL, []

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
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

    if not args.baseline:
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']), '--dump-ram']
    if args.case == 'gallery':
        sys.argv += ['--battery-save', config['save'], '--allow-gallery-fixtures',
                     '--gallery-save-fixture-manifest', config['fixture_manifest']]
        if not args.baseline:
            sys.argv += ['--dump-capture-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V681 terminal:', args.case, 'baseline:', args.baseline, flush=True)


if __name__ == '__main__':
    main()
