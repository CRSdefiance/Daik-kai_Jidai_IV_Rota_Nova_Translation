"""Read-only extra capture windows;original inputs and game logic unchanged."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


def main():
    path=Path('scripts/headless_desmume_v193.py')
    assert sha(path.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    windows_path=Path('work/analysis/letter_eligibility_v790/phase_windows.json')
    windows=read(windows_path)
    assert windows==[[11100,11200],[13900,14000],[17100,17200],[20700,20800]]
    source=path.read_text(encoding='utf-8')
    fixture='from scripts.native_condition_fixture_v520 import set_condition'
    capture='in_window = args.capture_window is not None and args.capture_window[0] <= frame <= args.capture_window[1]'
    assert source.count(fixture)==source.count(capture)==1
    effective=source.replace(fixture,'from scripts.native_letter_eligibility_v790 import set_condition')
    effective=effective.replace(capture,capture+' or any(first <= frame <= last for first,last in PHASE_WINDOWS)')
    exec(compile(effective,str(path),'exec'),{'__name__':'__main__','__file__':str(path.resolve()),'PHASE_WINDOWS':windows})
    assert source==path.read_text(encoding='utf-8')
    report_path=Path(sys.argv[sys.argv.index('--out')+1])/'capture_report.json'
    report=read(report_path)
    report['letter_phase_observer']={'original_harness_sha256':sha(path.read_bytes()),
        'adapter_sha256':sha(Path(__file__).read_bytes()),'effective_program_sha256':sha(effective.encode()),
        'fixture_sha256':sha(Path('scripts/native_letter_eligibility_v790.py').read_bytes()),
        'exact_read_only_capture_windows':windows,'windows_sha256':sha(windows_path.read_bytes()),
        'only_fixture_import_and_read_only_PNG_capture_predicate_replaced':True,
        'original_controller_schedule_and_game_logic_unchanged':True}
    save(report_path,report)


if __name__=='__main__':main()
