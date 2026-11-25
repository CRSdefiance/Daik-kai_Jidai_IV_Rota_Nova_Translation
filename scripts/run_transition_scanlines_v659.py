"""Current/clean Lil transitions with optional isolated host scanline observation."""

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

ROOT = Path('work/analysis/transition_scanlines_v659')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['inputs']).read_bytes()) == pre['inputs_sha256']
    rom = 'work/clean.nds' if args.clean else pre['candidate']
    name = ('clean' if args.clean else 'current') + ('_baseline' if args.baseline else '_observed')
    folder = Path('E:/Rota Nova translations/Generated/work/emulation_v193/transition_scanlines_v659_' + name)
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
            observer = Observer(core, folder / 'scanlines', pre['scanline_frames'])
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
        '--frames', str(pre['frames']), '--inputs-json', pre['inputs'], '--capture-every', '999999',
        '--capture-at', *map(str, pre['scanline_frames'])]
    if not args.baseline:
        sys.argv += ['--capture-gpu-state-at', '2858', '2860', '2863', '2865', '2868',
                     '--capture-native-state-at', '2858', '2860', '2863', '2865', '2868']
    try:
        harness.main()
    finally:
        ct.CDLL, gpu.export = loader, old_export
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V659 terminal run:', name, 'observer frames:', len(installed[0].frames) if installed else 0, flush=True)


if __name__ == '__main__':
    main()
