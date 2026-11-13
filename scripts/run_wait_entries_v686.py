"""Repeat source/current openings with read-only actual modal entry/return tracing."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_wait_entries_v686 import Observer
from scripts.run_opening_holds_v686 import CAP, CLEAN, CURRENT, FRAMES, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version', choices=('source', 'current'))
    version = parser.parse_args().version
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    controls = read(ROOT / 'wait_native_prefix_controls.json')
    assert controls['current_observer_sha256'] == sha(Path('scripts/observe_wait_entries_v686.py').read_bytes())
    folder = CAP / ('opening_wait_entries_v686_' + version)
    assert not folder.exists()
    folder.mkdir()
    manifest = pre['source_unlock_manifest'] if version == 'source' else str(ROOT / 'current_unlock_manifest.json')
    save(folder / 'run_contract.json', {'version': version,
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': controls['current_observer_sha256'],
        'inputs_sha256': pre['inputs_sha256'], 'unlock_manifest': manifest,
        'unlock_manifest_sha256': sha(Path(manifest).read_bytes())})
    loader, installed = ct.CDLL, []

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer', version)
            observer.install()
            installed.append(observer)
            original = core.retro_run
            original.restype = None

            def advance():
                observer.next_frame()
                original()
            core.retro_run = advance
        return core

    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(CLEAN if version == 'source' else CURRENT),
        '--out', str(folder), '--frames', '31000', '--inputs-json', pre['inputs'], '--touchscreen',
        '--battery-save', pre['donor'], '--allow-gallery-fixtures', '--gallery-save-fixture-manifest', manifest,
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V686 actual modal interval trace terminal:', version, flush=True)


if __name__ == '__main__':
    main()
