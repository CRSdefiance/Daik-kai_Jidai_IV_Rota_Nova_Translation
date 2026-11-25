"""Independent original/repaired cold boots for captain prompts and New Game."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/captain_prompt_wrap_v651')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('fleet_control', 'fleet_candidate', 'newgame_control', 'newgame_candidate'))
    args = parser.parse_args()
    config = read(ROOT / 'run_configs.json')[args.case]
    assert sha(Path(config['ROM']).read_bytes()) == config['ROM_sha256']
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    sys.argv = ['headless_desmume_v193.py', '--rom', config['ROM'], '--out', config['output'],
                '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
                '--capture-every', str(config['capture_every']), '--capture-at', *map(str, config['capture_frames'])]
    if config.get('donor'):
        assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
        sys.argv += ['--battery-save', config['donor'], '--dump-capture-ram',
                     '--capture-native-state-at', '32600', '35800']
    harness.main()


if __name__ == '__main__':
    main()
