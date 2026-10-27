"""One explicit condition-import adapter; original emulator harness is preserved."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')
FIXTURE = Path('scripts/native_unidentified_fleet_fixture_v783.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    marker = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert original.count(marker) == 1
    effective = original.replace(marker, 'from scripts.native_unidentified_fleet_fixture_v783 import set_condition')
    digest = sha(FIXTURE.read_bytes())
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    assert HARNESS.read_text(encoding='utf-8') == original and sha(FIXTURE.read_bytes()) == digest
    path = Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_unidentified_fleet_adapter'] = {
        'original_harness_unchanged': True, 'original_harness_sha256': sha(HARNESS.read_bytes()),
        'effective_program_sha256': sha(effective.encode()), 'adapter_sha256': sha(Path(__file__).read_bytes()),
        'single_import_replacement': True, 'fixture_producer_sha256': digest}
    save(path, report)


if __name__ == '__main__':
    main()
