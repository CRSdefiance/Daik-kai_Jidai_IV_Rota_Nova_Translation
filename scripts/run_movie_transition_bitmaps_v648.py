"""Ordinary adjacent transition frames with read-only CPU/GPU source export."""
import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import inspect_desmume_gpu_v630 as gpu
from scripts.inspect_committed_gpu_v646 import export
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('route', choices=('rafael', 'lil', 'hodram'))
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--clean-control', action='store_true')
    args = parser.parse_args()
    root = Path('work/analysis/movie_transition_bitmaps_v648')
    pre, config = read(root / 'preflight.json'), read(root / 'run_configs.json')[args.route]
    assert sha(Path(pre['candidate']).read_bytes()) == pre['candidate_sha256']
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    selected_rom = pre['candidate']
    if args.clean_control:
        selected_rom = 'work/clean.nds'
        assert sha(Path(selected_rom).read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    original = gpu.export

    def combined(core, directory, expected_ram):
        result = original(core, directory, expected_ram)
        extra = export(core, directory, expected_ram)
        data = {k: v for k, v in result.items() if k not in ('path', 'sha256')}
        data['read_only_committed_geometry'] = extra
        path = Path(result['path'])
        save(path, data)
        return {'path': str(path), 'sha256': sha(path.read_bytes()), **data}

    if not (args.baseline or args.clean_control):
        gpu.export = combined
    suffix = args.route + ('_clean_control' if args.clean_control else '_baseline' if args.baseline else '')
    sys.argv = ['headless_desmume_v193.py', '--rom', selected_rom, '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/movie_transition_bitmaps_v648_' + suffix,
        '--frames', str(config['frames']), '--inputs-json', config['inputs'],
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames'])]
    if not (args.baseline or args.clean_control):
        sys.argv += ['--capture-gpu-state-at', *map(str, config['GPU_and_native_frames']),
                     '--capture-native-state-at', *map(str, config['GPU_and_native_frames'])]
    harness.main()


if __name__ == '__main__':
    main()
