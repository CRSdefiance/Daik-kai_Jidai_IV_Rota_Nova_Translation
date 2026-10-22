"""Reach common developed Karibib with the previously authorized Maria save."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.run_Karibib_return_v667 import ROOT
from scripts.run_village_consistency_v666 import ROM, relocate
from scripts.run_village_development_v665 import PREVIOUS, Controller
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_village_wrap_v608 import read, save

FOLDER = CAP / 'Karibib_return_v667_Maria_Seoul'


class MariaController(Controller):
    def navigate(self):
        yield from super().navigate()
        find_mask(self.font, 'Karibib', self.image(), (0, 10, 256, 40))
        self.phases['actual_developed_Karibib'] = self.frame


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    saved = read('work/analysis/maria_asia_v516/saved_checkpoint.json')
    assert saved['production_cold_reload_verified'] and saved['selection_bypass_only_not_earned_unlock']
    assert sha(Path(saved['save']).read_bytes()) == saved['sha256']
    assert not FOLDER.exists()
    FOLDER.mkdir()
    save(FOLDER / 'run_contract.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'donor': saved['save'], 'donor_sha256': saved['sha256'],
        'Maria_selection_bypass_save_previously_authorized_not_earned_unlock': True,
        'source_save_checkpoint': 'work/analysis/maria_asia_v516/saved_checkpoint.json',
        'source_save_checkpoint_sha256': sha(Path('work/analysis/maria_asia_v516/saved_checkpoint.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'only_coordinate_approach_no_development_story_resource_or_outcome_flags': True})
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    controller = MariaController(9, FOLDER, arm, 'Kalahari')
    old_relocate, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, controller
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(FOLDER),
        '--frames', '30000', '--inputs-json', str(PREVIOUS / 'inputs_chief_09.json'),
        '--battery-save', saved['save'], '--pause-at', '5200', '--allow-location-fixtures',
        '--touchscreen', '--capture-every', '999999', '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old_relocate, stdin
    if controller.error:
        raise RuntimeError('Retained Maria Karibib failure: ' + controller.error)
    print(f'V667 Maria actual Karibib return terminal at {controller.frame}.', flush=True)


if __name__ == '__main__':
    main()
