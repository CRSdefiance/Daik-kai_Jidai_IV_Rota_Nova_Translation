"""Use the complete Sea View heading instead of a blinking footer as an input cue."""

import argparse
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


class KaribibController(Controller):
    def navigate(self):
        yield from super().navigate()
        self.phases['encounter_first_dialogue'] = self.frame
        for _ in range(5):
            yield self.command(buttons=['A'], frames=400)
        self.phases['original_Attack_choice'] = self.frame
        yield self.command(buttons=['DOWN'], frames=100)
        self.phases['Not_our_authority_selection'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['noncombat_choice_committed'] = self.frame
        for _ in range(16):
            try:
                find_mask(self.font, 'Sea View', self.image(), (0, 0, 256, 16))
            except ValueError:
                yield self.command(buttons=['A'], frames=400)
            else:
                break
        else:
            raise AssertionError('Sea View heading absent after16 ordinary advances')
        self.phases['original_branch_return_to_Sea'] = self.frame
        yield {'until': self.frame + 400, 'location_town': 9}
        self.phases['post_encounter_docking_prompt'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        find_mask(self.font, 'Karibib', self.image(), (0, 10, 256, 40))
        self.phases['developed_town_return'] = self.frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strong-fleet', action='store_true')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    tag = 'five_ship_early_approach' if args.strong_fleet else 'early_approach'
    folder = CAP / ('Karibib_return_v667_' + tag)
    assert not folder.exists()
    donor = read('work/analysis/full_fleet_victory_v654/replay_preflight.json') if args.strong_fleet else pre
    assert sha(Path(donor['donor']).read_bytes()) == donor['donor_sha256']
    folder.mkdir()
    save(folder / 'run_contract.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'donor': donor['donor'], 'donor_sha256': donor['donor_sha256'],
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'prior_footer_equality_failure_retained': True, 'only_coordinate_approach_no_battle_or_outcome_flags': True})
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    controller = KaribibController(9, folder, arm, 'Kalahari')
    old_relocate, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, controller
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', '30000', '--inputs-json', str(PREVIOUS / 'inputs_chief_09.json'),
        '--battery-save', donor['donor'], '--pause-at', '5200', '--allow-location-fixtures',
        '--touchscreen', '--capture-every', '999999', '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old_relocate, stdin
    if controller.error:
        raise RuntimeError('Retained Karibib follow-up failure: ' + controller.error)
    print(f'V667 {tag}: actual Karibib return terminal at {controller.frame}.', flush=True)


if __name__ == '__main__':
    main()
