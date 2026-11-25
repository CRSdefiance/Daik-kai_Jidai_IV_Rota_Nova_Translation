"""Ordinary recruitment/assignment for the saved five-ship graphics test."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read


def main():
    pre = read('work/analysis/full_fleet_battle_v652/preflight.json')
    assert sha(Path(pre['candidate']).read_bytes()) == pre['candidate_sha256']
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_staffing_v652_actual',
        '--frames', '80000', '--inputs-json', 'work/analysis/fleet_capacity_v650/port_prefix.json',
        '--capture-every', '999999', '--capture-at', '3200', '--touchscreen',
        '--battery-save', pre['donor'], '--pause-at', '3200', '--dump-capture-ram',
        '--dump-pause-ram', '--dump-native-state']
    harness.main()


if __name__ == '__main__':
    main()
