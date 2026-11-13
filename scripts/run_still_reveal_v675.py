"""Unchanged Maria New Game with read-only snapshots before original upper painting."""

import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_scene_entry_v675 import FRAMES, Observer
from scripts.research_still_reveal_v675 import ROOT
from scripts.run_maria_dispatch_v674 import CAPTURE_FRAMES
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    prior = read('work/analysis/maria_opening_v674/preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    folder = CAP / 'still_reveal_v675_before_iterator_v3'
    assert not folder.exists()
    folder.mkdir(parents=True)
    save(folder / 'run_contract.json', {'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_scene_entry_v675.py').read_bytes()),
        'inputs_sha256': sha(Path('work/analysis/maria_opening_v674/dispatch_inputs.json').read_bytes()),
        'read_only_before_iterator_snapshots_not_savestate_loading_or_gameplay_write': True})
    loader, installed = ct.CDLL, []

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'before_paint')
            original_run = core.retro_run
            original_run.restype = None
            observer.install()

            def run():
                observer.next_frame()
                original_run()
            core.retro_run = run
            installed.append(observer)
        return core

    ct.CDLL = loaded
    selected = sorted(set(FRAMES) | set(CAPTURE_FRAMES))
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', '4000', '--inputs-json', 'work/analysis/maria_opening_v674/dispatch_inputs.json',
        '--battery-save', prior['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', prior['manifest'], '--capture-every', '999999',
        '--capture-at', *map(str, selected), '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V675 before-paint source capture terminal.', flush=True)


if __name__ == '__main__':
    main()
