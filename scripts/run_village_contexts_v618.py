"""Run authorized village-proximity tests on the unchanged combined V617 ROM."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_contexts_v618 import relocate


def main():
    donor = Path('work/analysis/weapon_voyage_v476/syracuse_test_copy.dsv')
    assert sha(donor.read_bytes()) == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
    if '--battery-save' not in sys.argv:
        sys.argv += ['--battery-save', str(donor)]
    else:
        assert sha(Path(sys.argv[sys.argv.index('--battery-save') + 1]).read_bytes()) == sha(donor.read_bytes())
    original = location.relocate
    location.relocate = relocate
    try:
        harness.main()
    finally:
        location.relocate = original


if __name__ == '__main__':
    main()
