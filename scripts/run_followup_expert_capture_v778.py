"""Single explicit fixture import adapter;the original emulator file is unchanged."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

HARNESS = Path('scripts/headless_desmume_v193.py')


def main():
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original = HARNESS.read_text(encoding='utf-8')
    old = 'from scripts.native_strategist_fixture_v624 import assign, assign_expert'
    new = 'from scripts.native_followup_expert_fixture_v778 import assign, assign_expert'
    assert original.count(old) == 1
    effective = original.replace(old, new)
    exec(compile(effective, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    path = Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_strategist_adapter'] = {
        'original_harness_unchanged': HARNESS.read_text(encoding='utf-8') == original,
        'original_harness_sha256': sha(HARNESS.read_bytes()), 'effective_program_sha256': sha(effective.encode()),
        'adapter_sha256': sha(Path(__file__).read_bytes()), 'single_import_replacement': True,
        'fixture_producer_sha256': sha(Path('scripts/native_followup_expert_fixture_v778.py').read_bytes()),
        'original_fixture_module_sha256': sha(Path('scripts/native_strategist_fixture_v624.py').read_bytes()),
        'original_experience_calendar_producer_sha256': sha(Path('scripts/native_scheme_expert_fixture_v776_v2.py').read_bytes())}
    save(path, report)


if __name__ == '__main__':
    main()
