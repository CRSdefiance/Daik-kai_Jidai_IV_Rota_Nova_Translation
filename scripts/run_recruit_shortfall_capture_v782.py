"""One import adapter for the authorized isolated recruitment-state fixture."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')
FIXTURE = Path('scripts/native_recruit_shortfall_fixture_v782.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    fixture_sha = sha(FIXTURE.read_bytes())
    old = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert original.count(old) == 1
    effective = original.replace(old, 'from scripts.native_recruit_shortfall_fixture_v782 import set_condition')
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    assert sha(FIXTURE.read_bytes()) == fixture_sha
    assert HARNESS.read_text(encoding='utf-8') == original
    path = Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_recruitment_adapter'] = {
        'original_harness_unchanged': True, 'original_harness_sha256': sha(HARNESS.read_bytes()),
        'effective_program_sha256': sha(effective.encode()), 'adapter_sha256': sha(Path(__file__).read_bytes()),
        'single_import_replacement': True, 'fixture_producer_sha256': fixture_sha}
    save(path, report)


if __name__ == '__main__':
    main()
