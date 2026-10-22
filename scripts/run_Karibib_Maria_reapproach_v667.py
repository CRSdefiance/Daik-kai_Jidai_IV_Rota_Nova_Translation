"""Repeat Maria's missed return with one additional coordinate-only approach."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_Karibib_Maria_v667 as original
from scripts.run_village_return_v665 import ReturnController
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_village_wrap_v608 import save


class MariaReturnController(ReturnController):
    def navigate(self):
        yield from super().navigate()
        find_mask(self.font, 'Karibib', self.image(), (0, 10, 256, 40))
        self.phases['actual_developed_Karibib'] = self.frame


def main():
    original.FOLDER = CAP / 'Karibib_return_v667_Maria_Seoul_reapproach'
    original.MariaController = MariaReturnController
    try:
        original.main()
    finally:
        if original.FOLDER.exists():
            save(original.FOLDER / 'Maria_reapproach_extension.json', {
                'source': str(Path(__file__)), 'source_sha256': sha(Path(__file__).read_bytes()),
                'base_runner': str(Path(original.__file__)), 'base_runner_sha256': sha(Path(original.__file__).read_bytes()),
                'extra_fixture': 'one coordinate-only reapproach at original missed-return pause',
                'no_password_development_story_resource_or_outcome_flags': True})


if __name__ == '__main__':
    main()
