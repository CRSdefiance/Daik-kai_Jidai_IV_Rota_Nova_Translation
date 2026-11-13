"""Unmodified current full opening, with planned read-only GPU checkpoints."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--detail', action='store_true')
    parser.add_argument('--committed', action='store_true')
    parser.add_argument('--full-committed', action='store_true')
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    assert sum((args.detail, args.committed, args.full_committed, args.baseline)) <= 1
    detail = args.detail
    name = 'full_config.json' if args.full_committed or args.baseline else 'committed_config.json' if args.committed else 'detail_config.json' if detail else 'run_config.json'
    config = read('work/analysis/opening_composition_v646/' + name)
    if args.committed or args.full_committed:
        from scripts import inspect_desmume_gpu_v630 as gpu
        from scripts.inspect_committed_gpu_v646 import export

        previous_export = gpu.export

        def combined(core, directory, expected_ram):
            result = previous_export(core, directory, expected_ram)
            extra = export(core, directory, expected_ram)
            data = {k: v for k, v in result.items() if k not in ('path', 'sha256')}
            data['read_only_committed_geometry'] = extra
            path = Path(result['path'])
            save(path, data)
            return {'path': str(path), 'sha256': sha(path.read_bytes()), **data}

        gpu.export = combined
    label = 'baseline' if args.baseline else 'committed_full' if args.full_committed else 'committed_v2' if args.committed else 'detail' if detail else 'actual'
    sys.argv = ['headless_desmume_v193.py', '--rom',
        'out/all_routes_combined_v640_candidate.nds', '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/opening_composition_v646_' + label,
        '--frames', str(config['frames']), '--capture-every', '999999',
        '--capture-at', *map(str, config['capture_frames'])]
    if not args.baseline:
        sys.argv += ['--capture-gpu-state-at', *map(str, config['gpu_export_frames'])]
    if detail:
        sys.argv += ['--capture-native-state-at', *map(str, config['native_export_frames'])]
    harness.main()


if __name__ == '__main__':
    main()
