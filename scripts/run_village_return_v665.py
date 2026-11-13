"""Repeat an original missed return with a disclosed extra coordinate-only approach."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_village_development_v665 as original
from scripts.verify_village_wrap_v608 import save


class ReturnController(original.Controller):
    def navigate(self):
        repeated = False
        for command in super().navigate():
            if not repeated and self.phases.get('return_docking_prompt') == self.frame:
                repeated = True
                self.phases['missed_return_before_reapproach'] = self.frame
                yield {'until': self.frame + 400, 'location_town': self.village}
                self.phases['reapproach_docking_prompt'] = self.frame
                command['until'] = self.frame + 400
                save(self.folder / 'return_fixture_provenance.json', {
                    'original_runner': str(Path(original.__file__)),
                    'original_runner_sha256': sha(Path(original.__file__).read_bytes()),
                    'extension_runner': str(Path(__file__)),
                    'extension_runner_sha256': sha(Path(__file__).read_bytes()),
                    'extra_approach_frame': self.phases['missed_return_before_reapproach'],
                    'only_extra_command_is_coordinate_approach_no_password_development_or_scene_flags': True})
            yield command


if __name__ == '__main__':
    original.Controller = ReturnController
    original.main()
