"""Choose the original noncombat slaver branch, then approach developed Karibib."""

import sys
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.run_village_consistency_v666 import ROM, relocate
from scripts.run_village_development_v665 import PREVIOUS, Controller
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Karibib_return_v667')
FOLDER = CAP / 'Karibib_return_v667_noncombat'


class KaribibController(Controller):
    def navigate(self):
        yield from super().navigate()
        self.phases['encounter_first_dialogue'] = self.frame
        for _ in range(5):
            yield self.command(buttons=['A'], frames=400)
        assert self.frame == 14580
        self.phases['original_Attack_choice'] = self.frame
        reference = CAP / 'village_development_v665_09_story/frame_014580_navigation.png'
        assert self.image().tobytes() == Image.open(reference).convert('RGB').tobytes()
        yield self.command(buttons=['DOWN'], frames=100)
        self.phases['Not_our_authority_selection'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['noncombat_choice_committed'] = self.frame
        reference = Image.open(CAP / 'village_development_v665_09_story/frame_016580_navigation.png').convert('RGB')
        footer = reference.crop((0, 366, 256, 384)).tobytes()
        for _ in range(16):
            if self.image().crop((0, 366, 256, 384)).tobytes() == footer:
                break
            yield self.command(buttons=['A'], frames=400)
        else:
            raise AssertionError('Original noncombat branch did not return to Sea within16 advances')
        self.phases['original_noncombat_return_to_Sea'] = self.frame
        yield {'until': self.frame + 400, 'location_town': 9}
        self.phases['post_encounter_docking_prompt'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        find_mask(self.font, 'Karibib', self.image(), (0, 10, 256, 40))
        self.phases['developed_town_return'] = self.frame


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists() and not FOLDER.exists()
    previous = read('work/analysis/village_consistency_v666/release_proof.json')
    assert sha(ROM.read_bytes()) == previous['candidate_sha256']
    old = read('work/analysis/village_development_v665/preflight.json')
    assert sha(Path(old['donor']).read_bytes()) == old['donor_sha256']
    release = {str(p): sha(p.read_bytes()) for p in
        [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
         Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': previous['candidate_sha256'],
        'donor': old['donor'], 'donor_sha256': old['donor_sha256'], 'release_hashes': release,
        'previous_goal_turn_classification': 'progress: V666 seven integrated repairs, eight terminal runs and archive verified',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'output': str(FOLDER), 'fixture_source': 'scripts/run_village_consistency_v666.py',
        'fixture_source_sha256': sha(Path('scripts/run_village_consistency_v666.py').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    FOLDER.mkdir()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    controller = KaribibController(9, FOLDER, arm, 'Kalahari')
    old_relocate, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, controller
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(FOLDER),
        '--frames', '30000', '--inputs-json', str(PREVIOUS / 'inputs_chief_09.json'),
        '--battery-save', old['donor'], '--pause-at', '5200', '--allow-location-fixtures',
        '--touchscreen', '--capture-every', '999999', '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old_relocate, stdin
    if controller.error:
        raise RuntimeError('Retained Karibib controller failure: ' + controller.error)
    print(f'V667 original Karibib return terminal at {controller.frame}.', flush=True)


if __name__ == '__main__':
    main()
