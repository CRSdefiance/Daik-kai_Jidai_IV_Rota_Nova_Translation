"""Explicit Survey3/Lookout1 adapter;original harness and completed adapters stay unchanged."""

import hashlib
import sys
from pathlib import Path

from scripts.verify_village_wrap_v608 import read,save

HARNESS=Path('scripts/headless_desmume_v193.py')


def main():
    original=HARNESS.read_text(encoding='utf-8')
    assert hashlib.sha256(HARNESS.read_bytes()).hexdigest()=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    replacements={
        'from scripts.native_missionary_fixture_v623 import assign as assign_missionary':'from scripts.native_survey_lookout_fixture_v877 import assign as assign_missionary',
        "'missionary_fixture'":"'survey_lookout_fixture'",'args.allow_missionary_fixtures':'args.allow_survey_lookout_fixtures',
        '--allow-missionary-fixtures':'--allow-survey-lookout-fixtures',
        "'synthetic_missionary_Chapel_assignment_fixtures'":"'synthetic_survey_lookout_assignment_fixtures'",
        'Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.':'Isolated Survey3/Lookout1 room assignment applied;no earned refit,qualification or recruitment credit.',
        'Allow the bounded three-byte Chapel/Manuel role fixture for Square display testing.':'Allow only declared2/3 Survey3/Lookout1 room and assignment bytes in the disposable test.',
        'Missionary display fixture requires':'Survey3/Lookout1 fixture requires'}
    effective,counts=original,{}
    for old,new in replacements.items():
        counts[old]=effective.count(old);assert counts[old] in (1,2),(old,counts[old])
        effective=effective.replace(old,new)
    exec(compile(effective,str(HARNESS),'exec'),{'__name__':'__main__','__file__':str(HARNESS.resolve())})
    folder=Path(sys.argv[sys.argv.index('--out')+1]);path=folder/'capture_report.json';report=read(path)
    report['controlled_survey_lookout_adapter']={'original_harness_file_unchanged':HARNESS.read_text(encoding='utf-8')==original,
        'unchanged_harness_sha256':hashlib.sha256(HARNESS.read_bytes()).hexdigest(),
        'effective_program_sha256':hashlib.sha256(effective.encode('utf-8')).hexdigest(),
        'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_replacement_counts':counts}
    assert report['controlled_survey_lookout_adapter']['original_harness_file_unchanged'];save(path,report)


if __name__=='__main__':main()
