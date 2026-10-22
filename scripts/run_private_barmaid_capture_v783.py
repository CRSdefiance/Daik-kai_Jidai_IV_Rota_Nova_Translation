"""One inventory-import adapter; use the original Seoul donor and normal dialogue."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')
FIXTURE = Path('scripts/native_barmaid_gift_fixture_v783.py')
FROZEN = Path('scripts/native_barmaid_gift_fixture_v780_v3.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    marker = 'from scripts.native_inventory_fixture_v481 import transfer'
    assert original.count(marker) == 1
    effective = original.replace(marker, 'from scripts.native_barmaid_gift_fixture_v783 import transfer')
    before = {str(p): sha(p.read_bytes()) for p in (FIXTURE, FROZEN)}
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    assert HARNESS.read_text(encoding='utf-8') == original
    assert before == {p: sha(Path(p).read_bytes()) for p in before}
    path = Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_private_barmaid_adapter'] = {
        'original_harness_unchanged': True, 'original_harness_sha256': sha(HARNESS.read_bytes()),
        'effective_program_sha256': sha(effective.encode()), 'adapter_sha256': sha(Path(__file__).read_bytes()),
        'single_inventory_import_replacement': True, 'fixture_producer_sha256': before[str(FIXTURE)],
        'frozen_fixture_producer_sha256': before[str(FROZEN)],
        'no_location_relationship_rng_or_dialogue_injection': True}
    save(path, report)


if __name__ == '__main__':
    main()
