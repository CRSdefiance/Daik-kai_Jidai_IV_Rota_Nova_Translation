"""Frozen emulator harness with one bounded calendar-fixture import adapter."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


if __name__=='__main__':
    path=Path('scripts/headless_desmume_v193.py');source=path.read_text(encoding='utf-8')
    assert sha(path.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    marker='from scripts.native_condition_fixture_v520 import set_condition';assert source.count(marker)==1
    effective=source.replace(marker,'from scripts.native_ceremony_fixture_v809 import set_condition')
    exec(compile(effective,str(path),'exec'),{'__name__':'__main__','__file__':str(path.resolve())})
    assert path.read_text(encoding='utf-8')==source
    p=Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json';report=read(p)
    report['ceremony_fixture_adapter_v809']=dict(one_fixture_import_replacement=True,
        no_dialogue_portrait_eligibility_outcome_or_original_time_handler_replacement=True,
        original_harness_sha256=sha(path.read_bytes()),effective_program_sha256=sha(effective.encode()),
        source_hashes={str(p):sha(p.read_bytes()) for p in (Path(__file__),Path('scripts/native_ceremony_fixture_v809.py'))})
    save(p,report)
