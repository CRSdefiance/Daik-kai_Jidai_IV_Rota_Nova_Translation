"""Single fixture import adapter; preserve the original emulator harness."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')
FIXTURE = Path('scripts/native_item_roles_v789.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    old = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert original.count(old) == 1
    effective = original.replace(old, 'from scripts.native_item_roles_v789 import set_condition')
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    assert HARNESS.read_text(encoding='utf-8') == original
    path = Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['item_role_adapter'] = {'original_harness_sha256': sha(HARNESS.read_bytes()),
        'single_import_replacement': True, 'effective_program_sha256': sha(effective.encode()),
        'fixture_producer_sha256': sha(FIXTURE.read_bytes()), 'adapter_sha256': sha(Path(__file__).read_bytes()),
        'no_dialogue_or_menu_logic_replacement': True}
    save(path, report)


if __name__ == '__main__':
    main()
