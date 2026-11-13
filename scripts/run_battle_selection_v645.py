"""Cold-boot current ROM to the original encounter; isolated test copy only."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_battle_fixture_v645 import apply_fixture


def main():
    rom = Path('out/all_routes_combined_v640_candidate.nds')
    donor = Path('work/analysis/lubeck_voyage_v421/donor_test_copy.dsv')
    assert sha(rom.read_bytes()) == '93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e'
    assert sha(donor.read_bytes()) == '97997ce6fbeda9ff0272c08d7420e96676240b017e0037b721ed7c5eb52770d5'
    dispatch.apply_fixture = apply_fixture
    sys.argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out',
        'E:/Rota Nova translations/Generated/work/emulation_v193/battle_selection_v645_actual',
        '--frames', '60000', '--inputs-json',
        'work/analysis/battle_contexts_v620/sea_encounter_prefix.json',
        '--capture-every', '999999', '--capture-at', '20000', '20400',
        '--touchscreen', '--battery-save', str(donor), '--pause-at', '20400',
        '--dump-capture-ram', '--dump-pause-ram', '--dump-native-state',
        '--allow-battle-fixtures']
    harness.main()


if __name__ == '__main__':
    main()
