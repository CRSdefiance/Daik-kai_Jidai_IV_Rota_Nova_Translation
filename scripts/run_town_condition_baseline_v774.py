"""Named two-byte town display fixture through the unchanged emulator harness."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

HARNESS=Path('scripts/headless_desmume_v193.py')


def main():
    assert sha(HARNESS.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    original=HARNESS.read_text(encoding='utf-8');effective=original;counts={}
    replacements={
        'from scripts.native_condition_fixture_v520 import set_condition':'from scripts.native_town_condition_baseline_v774 import set_condition',
        "'condition_fixture'":"'town_condition_fixture'",'args.allow_condition_fixtures':'args.allow_town_condition_fixtures',
        '--allow-condition-fixtures':'--allow-town-condition-fixtures',
        "'synthetic_condition_fixtures'":"'synthetic_town_condition_fixtures'",
        'Synthetic condition applied; natural condition event is not verified.':'Two-byte synthetic Amsterdam Boom display fixture applied;natural condition event not verified.',
        'Allow labeled isolated crew condition tests; never verifies natural condition events.':'Allow the declared two-byte Amsterdam Boom display fixture;never verifies a natural condition event.'}
    for old,new in replacements.items():
        count=effective.count(old);assert count in(1,2),(old,count);counts[old]=count;effective=effective.replace(old,new)
    legacy='''                    from scripts.native_condition_fixture_v637 import (
                        ARM_SHA as current_condition_sha,
                    )

                    if sha(arm) == current_condition_sha:
                        from scripts.native_condition_fixture_v637 import set_condition
'''
    assert effective.count(legacy)==1;effective=effective.replace(legacy,'')
    exec(compile(effective,str(HARNESS),'exec'),{'__name__':'__main__','__file__':str(HARNESS.resolve())})
    path=Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json';report=read(path)
    report['controlled_town_condition_adapter']={'original_harness_file_unchanged':HARNESS.read_text(encoding='utf-8')==original,
        'original_harness_sha256':sha(HARNESS.read_bytes()),'effective_program_sha256':sha(effective.encode()),
        'adapter_sha256':sha(Path(__file__).read_bytes()),'exact_token_replacement_counts':counts,
        'fixture_producer_sha256':sha(Path('scripts/native_town_condition_baseline_v774.py').read_bytes())}
    assert report['controlled_town_condition_adapter']['original_harness_file_unchanged'];save(path,report)


if __name__=='__main__':main()
