"""Ordinary captain-specific opening playback, with read-only source export."""

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
    args = parser.parse_args()
    label = args.route
    root = Path('work/analysis/route_opening_movies_v647')
    config, pre = read(root / 'run_configs.json')[label], read(root / 'preflight.json')
    assert sha(Path(pre['candidate']).read_bytes()) == pre['candidate_sha256']
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    original = gpu.export

    def combined(core, directory, expected_ram):
        result = original(core, directory, expected_ram)
        extra = export(core, directory, expected_ram)
        data = {k: v for k, v in result.items() if k not in ('path', 'sha256')}
        data['read_only_committed_geometry'] = extra
        path = Path(result['path'])
        save(path, data)
        return {'path': str(path), 'sha256': sha(path.read_bytes()), **data}

    if not args.baseline:
        gpu.export = combined
    suffix = label + ('_baseline' if args.baseline else '')
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/route_opening_movies_v647_' + suffix,
        '--frames', str(config['frames']), '--inputs-json', config['inputs'],
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames'])]
    if not args.baseline:
        sys.argv += ['--capture-gpu-state-at', *map(str, config['gpu_export_frames'])]
    harness.main()


if __name__ == '__main__':
    main()
