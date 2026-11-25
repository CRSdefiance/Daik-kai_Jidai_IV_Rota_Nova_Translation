"""Ordinary Lil New Game positive control; no wedding trigger or gameplay fixture."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_graphic_paints_v669 as paints
from scripts.observe_wedding_runtime_v676 import Observer
from scripts.research_wedding_command_v676 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'runtime_contract.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert config['inputs_sha256'] == sha((ROOT / 'ordinary_inputs.json').read_bytes())
    folder = CAP / ('wedding_source_v676_' + ('baseline' if args.baseline else 'observed'))
    assert not folder.exists()
    folder.mkdir(parents=True)
    save(folder / 'run_contract.json', {'baseline': args.baseline,
        'runtime_contract_sha256': sha((ROOT / 'runtime_contract.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'no_gameplay_or_script_or_movie_substitution': True})
    loader, old_root, installed = ct.CDLL, paints.ROOT, []
    paints.ROOT = ROOT

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer', capacity=500000)
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
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', str(ROOT / 'ordinary_inputs.json'),
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']),
        '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    paints.ROOT = old_root
    print('V676 ordinary Lil runtime control terminal; baseline:', args.baseline, flush=True)


if __name__ == '__main__':
    main()
