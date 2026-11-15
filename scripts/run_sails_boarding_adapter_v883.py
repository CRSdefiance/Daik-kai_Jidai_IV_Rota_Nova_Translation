"""Explicit SailHandling0/Boarding7 adapter;original harness and completed adapters stay unchanged."""

import hashlib
import sys
from pathlib import Path

from scripts.verify_village_wrap_v608 import read,save

HARNESS=Path('scripts/headless_desmume_v193.py')


def main():
    original=HARNESS.read_text(encoding='utf-8')
    assert hashlib.sha256(HARNESS.read_bytes()).hexdigest()=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    replacements={
        'from scripts.native_missionary_fixture_v623 import assign as assign_missionary':'from scripts.native_sails_boarding_fixture_v883 import assign as assign_missionary',
        "'missionary_fixture'":"'sails_boarding_fixture'",'args.allow_missionary_fixtures':'args.allow_sails_boarding_fixtures',
        '--allow-missionary-fixtures':'--allow-sails-boarding-fixtures',
        "'synthetic_missionary_Chapel_assignment_fixtures'":"'synthetic_sails_boarding_assignment_fixtures'",
        'Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.':'Isolated SailHandling0/Boarding7 room assignment applied;no earned refit,qualification or recruitment credit.',
        'Allow the bounded three-byte Chapel/Manuel role fixture for Square display testing.':'Allow only declared2/3 SailHandling0/Boarding7 room and assignment bytes in the disposable test.',
        'Missionary display fixture requires':'SailHandling0/Boarding7 fixture requires'}
    effective,counts=original,{}
    for old,new in replacements.items():
        counts[old]=effective.count(old);assert counts[old] in (1,2),(old,counts[old])
        effective=effective.replace(old,new)
    exec(compile(effective,str(HARNESS),'exec'),{'__name__':'__main__','__file__':str(HARNESS.resolve())})
    folder=Path(sys.argv[sys.argv.index('--out')+1]);path=folder/'capture_report.json';report=read(path)
    report['controlled_sails_boarding_adapter']={'original_harness_file_unchanged':HARNESS.read_text(encoding='utf-8')==original,
        'unchanged_harness_sha256':hashlib.sha256(HARNESS.read_bytes()).hexdigest(),
        'effective_program_sha256':hashlib.sha256(effective.encode('utf-8')).hexdigest(),
        'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_replacement_counts':counts}
    assert report['controlled_sails_boarding_adapter']['original_harness_file_unchanged'];save(path,report)


if __name__=='__main__':main()
