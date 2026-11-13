"""Fresh actual ROM runs; battle replays the recorded navigation and fixtures."""

import argparse
import io
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_full_fleet_proximity_v653 import apply_fixture
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/queued_portrait_wrap_v653')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('staffing', 'battle', 'newgame'))
    parser.add_argument('--control', action='store_true')
    args = parser.parse_args()
    config = read(ROOT / 'run_configs.json')[args.case]
    if args.control:
        assert args.case == 'newgame'
        config = config['control']
    assert sha(Path(config['ROM']).read_bytes()) == config['ROM_sha256']
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    sys.argv = ['headless_desmume_v193.py', '--rom', config['ROM'], '--out', config['output'],
                '--frames', str(config.get('max_frames', config['frames'])), '--inputs-json', config['inputs'], '--touchscreen',
                '--capture-every', str(config['capture_every']), '--capture-at', *map(str, config['capture_frames'])]
    if config.get('donor'):
        assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
        sys.argv += ['--battery-save', config['donor'], '--dump-capture-ram']
    elif args.case == 'newgame':
        sys.argv += ['--dump-capture-ram', '--capture-native-state-at', '21000', '22500', '23100']
    if args.case == 'staffing':
        sys.argv += ['--capture-native-state-at', '5200', '12800']
    elif args.case == 'battle':
        assert sha(Path(config['commands']).read_bytes()) == config['commands_sha256']
        fixture = read(ROOT / 'fixture_preapply_proof.json')
        assert sha(Path(fixture['fixture_source']).read_bytes()) == fixture['fixture_source_sha256']
        dispatch.apply_fixture = apply_fixture
        sys.stdin = io.StringIO('\n'.join(json.dumps(c) for c in read(config['commands'])) + '\n')
        sys.argv += ['--pause-at', '4800', '--dump-pause-ram', '--dump-native-state', '--allow-battle-fixtures']
    harness.main()


if __name__ == '__main__':
    main()
