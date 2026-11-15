"""Current/clean Rafael and Hodram transitions with optional isolated host scanline observation."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import inspect_desmume_gpu_v630 as gpu
from scripts.inspect_committed_gpu_v646 import export
from scripts.observe_transition_scanlines_v659 import Observer
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/transition_boundaries_v660')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('route', choices=('rafael','hodram'))
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    config = read(ROOT / 'run_configs.json')[args.route]
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    rom = 'work/clean.nds' if args.clean else pre['candidate']
    name = args.route + '_' + ('clean' if args.clean else 'current') + ('_baseline' if args.baseline else '_observed')
    folder = Path('E:/Rota Nova translations/Generated/work/emulation_v193/transition_boundaries_v660_' + name)
    loader, old_export, installed = ct.CDLL, gpu.export, []

    def combined(core, directory, expected_ram):
        value = old_export(core, directory, expected_ram)
        committed = export(core, directory, expected_ram)
        path = Path(value['path'])
        data = {k: v for k, v in value.items() if k not in ('path', 'sha256')}
        data['read_only_committed_geometry'] = committed
        save(path, data)
        return {'path': str(path), 'sha256': sha(path.read_bytes()), **data}

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'scanlines', config['scanline_frames'])
            original_run = core.retro_run
            original_run.restype = None

            def run():
                observer.frame += 1
                if observer.frame == min(observer.frames):
                    observer.install()
                original_run()
                if observer.frame == max(observer.frames):
                    observer.close()
            core.retro_run = run
            installed.append(observer)
        return core
    if not args.baseline:
        ct.CDLL, gpu.export = loaded, combined
    sys.argv = ['headless_desmume_v193.py', '--rom', rom, '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--capture-every', '999999',
        '--capture-at', *map(str, config['scanline_frames'])]
    if not args.baseline:
        sys.argv += ['--capture-gpu-state-at', *map(str, config['GPU_and_native_frames']),
                     '--capture-native-state-at', *map(str, config['GPU_and_native_frames'])]
    try:
        harness.main()
    finally:
        ct.CDLL, gpu.export = loader, old_export
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V660 terminal run:', name, 'observer frames:', len(installed[0].frames) if installed else 0, flush=True)


if __name__ == '__main__':
    main()
