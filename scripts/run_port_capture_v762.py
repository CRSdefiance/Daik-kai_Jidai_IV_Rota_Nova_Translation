"""Named temporary Port-service prerequisites; historical emulator unchanged."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    source = HARNESS.read_text(encoding='utf-8'); effective = source
    replacements = {
        'from scripts.native_missionary_fixture_v623 import assign as assign_missionary': 'from scripts.native_port_fixture_v762 import assign as assign_missionary',
        "'missionary_fixture'": "'port_service_fixture'", 'args.allow_missionary_fixtures': 'args.allow_port_service_fixtures',
        '--allow-missionary-fixtures': '--allow-port-service-fixtures',
        "'synthetic_missionary_Chapel_assignment_fixtures'": "'synthetic_port_service_fixtures'",
        'Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.': 'Isolated native service prerequisite applied; no earned supplies or financial state claim.',
        'Allow the bounded three-byte Chapel/Manuel role fixture for Square display testing.': 'Allow isolated native money or water/food prerequisites through original methods.',
        'Missionary display fixture requires': 'Port-service fixture requires'}
    counts = {}
    for old, new in replacements.items():
        count = effective.count(old); assert count in (1, 2), (old, count)
        counts[old] = count; effective = effective.replace(old, new)
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    path = Path(sys.argv[sys.argv.index('--out') + 1]) / 'capture_report.json'; report = read(path)
    assert HARNESS.read_text(encoding='utf-8') == source
    report['controlled_port_service_harness_adapter'] = {'unchanged_original_harness_sha256': sha(HARNESS.read_bytes()),
        'original_harness_file_unchanged': True, 'effective_program_sha256': sha(effective.encode('utf-8')),
        'adapter_sha256': sha(Path(__file__).read_bytes()), 'exact_token_replacement_counts': counts}
    save(path, report)


if __name__ == '__main__': main()
