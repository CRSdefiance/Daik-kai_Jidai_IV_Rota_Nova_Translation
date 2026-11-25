"""Current full-fleet battle selection test with pinned bounded recovery/proximity."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_full_fleet_proximity_v652 import apply_fixture
from scripts.verify_village_wrap_v608 import read


def main():
    pre = read('work/analysis/full_fleet_battle_v652/preflight.json')
    saved = read('work/analysis/full_fleet_battle_v652/staffing_proof.json')['prepared_save']
    assert sha(Path(pre['candidate']).read_bytes()) == pre['candidate_sha256']
    assert sha(Path(saved['path']).read_bytes()) == saved['sha256']
    dispatch.apply_fixture = apply_fixture
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_battle_v652_near_target',
        '--frames', '120000', '--inputs-json', 'work/analysis/full_fleet_battle_v652/departure_prefix.json',
        '--capture-every', '999999', '--capture-at', '4800', '--touchscreen',
        '--battery-save', saved['path'], '--pause-at', '4800', '--dump-capture-ram',
        '--dump-pause-ram', '--dump-native-state', '--allow-battle-fixtures']
    harness.main()


if __name__ == '__main__':
    main()
