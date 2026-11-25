"""Original ordinary Save/Load workflow with a read-only RAM-stream observer."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_memory_streams_v682 import Observer
from scripts.prepare_memory_streams_v682 import ROM, ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    baseline = parser.parse_args().baseline
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 20
    assert controls['current_observer_sha256'] == sha(Path('scripts/observe_memory_streams_v682.py').read_bytes())
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
    folder = CAP / ('memory_streams_v682_' + ('baseline' if baseline else 'observed'))
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'baseline': baseline, 'config': config,
        'runner_sha256': sha(Path(__file__).read_bytes()), 'observer_sha256': controls['current_observer_sha256'],
        'ordinary_save_load_with_isolated_byte_exact_cartridge_save_no_live_gameplay_fixture': True})
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

    if not baseline:
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--battery-save', config['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, config['capture_frames']), '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V682 terminal; baseline:', baseline, flush=True)


if __name__ == '__main__':
    main()
