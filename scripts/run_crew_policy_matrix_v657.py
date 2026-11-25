"""Ordinary current five-ship Assign Sailors policy testing on an isolated save."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/crew_policy_matrix_v657')


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', pre['output'],
                '--frames', '60000', '--inputs-json', pre['inputs'], '--touchscreen',
                '--capture-every', '999999', '--capture-at', '3200',
                '--battery-save', pre['donor'], '--pause-at', '3200',
                '--dump-capture-ram', '--dump-pause-ram', '--dump-native-state']
    harness.main()


if __name__ == '__main__':
    main()
