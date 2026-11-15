"""Add an explicitly named country-briefing fixture to the unchanged historical harness."""

import hashlib
import sys
from pathlib import Path

from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')


def main():
    assert hashlib.sha256(HARNESS.read_bytes()).hexdigest() == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    replacements = {
        'from scripts.native_missionary_fixture_v623 import assign as assign_missionary':
            'from scripts.native_country_briefing_fixture_v748 import assign as assign_missionary',
        "'missionary_fixture'": "'country_fixture'",
        'args.allow_missionary_fixtures': 'args.allow_country_fixtures',
        '--allow-missionary-fixtures': '--allow-country-fixtures',
        "'synthetic_missionary_Chapel_assignment_fixtures'": "'synthetic_country_briefing_fixtures'",
        'Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.':
            'Isolated country share/region/RNG fixture applied; ordinary event acquisition is not claimed.',
        'Allow the bounded three-byte Chapel/Manuel role fixture for Square display testing.':
            'Allow the bounded country share/region/RNG fixture for Square display testing.',
        'Missionary display fixture requires': 'Country fixture requires',
    }
    effective, counts = original, {}
    for old, new in replacements.items():
        count = effective.count(old)
        assert count in (1, 2), (old, count)
        counts[old] = count
        effective = effective.replace(old, new)
    # Trusted local program; exact substitutions and both program hashes are recorded.
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})  # noqa: S102
    report = Path(sys.argv[sys.argv.index('--out') + 1]) / 'capture_report.json'
    data = read(report)
    data['controlled_country_harness_adapter'] = {
        'unchanged_original_harness_sha256': hashlib.sha256(HARNESS.read_bytes()).hexdigest(),
        'effective_in_memory_program_sha256': hashlib.sha256(effective.encode('utf-8')).hexdigest(),
        'adapter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exact_token_replacement_counts': counts,
        'original_harness_file_unchanged': HARNESS.read_text(encoding='utf-8') == original}
    assert data['controlled_country_harness_adapter']['original_harness_file_unchanged']
    save(report, data)


if __name__ == '__main__':
    main()
