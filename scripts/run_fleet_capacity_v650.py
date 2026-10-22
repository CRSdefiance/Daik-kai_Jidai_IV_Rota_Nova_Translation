"""Ordinary fleet-capacity selection testing from an isolated donor copy."""
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_battle_fixture_v645 import apply_fixture
from scripts.verify_village_wrap_v608 import read


def main():
    root = Path('work/analysis/fleet_capacity_v650')
    pre = read(root / 'preflight.json')
    assert sha(Path(pre['candidate']).read_bytes()) == pre['candidate_sha256']
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    dispatch.apply_fixture = apply_fixture
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/fleet_capacity_v650_actual',
        '--frames', '120000', '--inputs-json', str(root / 'port_prefix.json'),
        '--capture-every', '999999', '--capture-at', '3200', '--touchscreen',
        '--battery-save', pre['donor'], '--pause-at', '3200', '--dump-capture-ram',
        '--dump-pause-ram', '--dump-native-state', '--allow-battle-fixtures']
    harness.main()


if __name__ == '__main__':
    main()
