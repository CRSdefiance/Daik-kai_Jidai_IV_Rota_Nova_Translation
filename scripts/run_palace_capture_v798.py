"""Frozen original capture harness with one explicitly declared fixture adapter."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


def main():
    path=Path('scripts/headless_desmume_v193.py');source=path.read_text(encoding='utf-8')
    assert sha(path.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    marker='from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(marker)==1
    effective=source.replace(marker,'from scripts.native_palace_fixture_v798 import set_condition')
    exec(compile(effective,str(path),'exec'),{'__name__':'__main__','__file__':str(path.resolve())})
    assert path.read_text(encoding='utf-8')==source
    report_path=Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json';report=read(report_path)
    report['Palace_fixture_adapter']={'one_fixture_import_replacement':True,
        'no_dialogue_menu_transaction_outcome_or_game_logic_replacement':True,
        'original_harness_sha256':sha(path.read_bytes()),'effective_program_sha256':sha(effective.encode()),
        'source_hashes':{str(p):sha(p.read_bytes()) for p in (Path('scripts/run_palace_capture_v798.py'),Path('scripts/native_palace_fixture_v798.py'))}}
    save(report_path,report)


if __name__=='__main__':main()
