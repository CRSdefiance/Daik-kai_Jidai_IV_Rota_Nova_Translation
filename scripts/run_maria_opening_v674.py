"""Original Maria New Game playback; source system unlock, no movie substitution."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import inspect_desmume_gpu_v630 as gpu
from scripts.inspect_committed_gpu_v646 import export
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('pilot', 'observed', 'baseline'), default='pilot')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['manifest']).read_bytes()) == pre['manifest_sha256']
    folder = CAP / ('maria_opening_v674_' + args.case)
    assert not folder.exists()
    folder.mkdir(parents=True)
    save(folder / 'run_contract.json', {'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'case': args.case,
        'no_ROM_RAM_or_movie_replacement_no_earned_unlock': True})
    original = gpu.export

    def combined(core, directory, expected_ram):
        result = original(core, directory, expected_ram)
        extra = export(core, directory, expected_ram)
        data = {k: v for k, v in result.items() if k not in ('path', 'sha256')}
        data['read_only_committed_geometry'] = extra
        path = Path(result['path'])
        save(path, data)
        return {'path': str(path), 'sha256': sha(path.read_bytes()), **data}

    if args.case == 'pilot':
        tail = ['--frames', '12000', '--inputs-json', str(ROOT / 'pilot_inputs.json'),
            '--capture-every', '999999', '--pause-at', '2000', '--dump-pause-ram', '--dump-ram']
    else:
        config = read(ROOT / 'run_config.json')
        assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
        tail = ['--frames', str(config['frames']), '--inputs-json', config['inputs'],
            '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames'])]
        if args.case == 'observed':
            gpu.export = combined
            tail += ['--capture-gpu-state-at', *map(str, config['gpu_export_frames'])]
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--battery-save', pre['donor'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', pre['manifest'], *tail]
    try:
        harness.main()
    finally:
        gpu.export = original
    print('V674 Maria opening terminal:', args.case, flush=True)


if __name__ == '__main__':
    main()
