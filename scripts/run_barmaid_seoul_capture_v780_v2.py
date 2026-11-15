"""Single named location import adapter;historical emulator harness stays exact."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    old = 'from scripts.native_location_fixture_v519 import relocate'
    new = 'from scripts.native_barmaid_location_fixture_v780_v2 import relocate'
    assert original.count(old) == 1
    effective = original.replace(old, new)
    inventory_import = 'from scripts.native_inventory_fixture_v481 import transfer'
    assert effective.count(inventory_import) == 1
    effective = effective.replace(inventory_import, 'from scripts.native_barmaid_gift_fixture_v780_v3 import transfer')
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    path = Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_location_adapter'] = {
        'original_harness_file_unchanged': HARNESS.read_text(encoding='utf-8') == original,
        'original_harness_sha256': sha(HARNESS.read_bytes()), 'effective_program_sha256': sha(effective.encode()),
        'adapter_sha256': sha(Path(__file__).read_bytes()), 'single_import_replacement': False, 'exact_location_and_gift_imports_only': True,
        'gift_fixture_producer_sha256': sha(Path('scripts/native_barmaid_gift_fixture_v780_v3.py').read_bytes()),
        'fixture_producer_sha256': sha(Path('scripts/native_barmaid_location_fixture_v780_v2.py').read_bytes())}
    save(path, report)


if __name__ == '__main__':
    main()
