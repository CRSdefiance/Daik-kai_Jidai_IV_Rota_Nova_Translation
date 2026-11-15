"""Cold boot ordinary Hodram inputs to actual comma/question-mark dialogue."""

import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.prepare_ascii_punctuation_all_20261027 import ROOT, ROM, save


if __name__ == '__main__':
    inputs = Path('work/font_offset_one_20261027/hodram_inputs.json')
    prior_report_path = Path('work/font_offset_one_20261027/cold_boot_hodram/capture_report.json')
    prior = json.loads(prior_report_path.read_text())
    captures = [1, 60, 180, 1100, 1600, 2000, 3000, 4000, 5000, 6000, 7000]
    output = ROOT / 'cold_boot_hodram'
    assert not output.exists()
    digest = sha(ROM.read_bytes())
    assert digest == json.loads(ROM.with_suffix('.manifest.json').read_text())['candidate_sha256']
    save(ROOT / 'hodram_plan.json', dict(candidate=str(ROM), candidate_sha256=digest,
        frames=7001, captures=captures, inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
        predecessor_report=str(prior_report_path), predecessor_report_sha256=sha(prior_report_path.read_bytes()),
        ordinary_input_only=True, no_savestate_battery_or_new_RAM_fixture=True))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(output),
        '--frames', '7001', '--inputs-json', str(inputs), '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, captures)]
    harness.main()
    report = json.loads((output / 'capture_report.json').read_text())
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] == 7001
    for key in ['scripted_input_schedule', 'core_DLL_sha256', 'core_options']:
        assert report[key] == prior[key]
    save(ROOT / 'hodram_terminal.json', dict(terminal=True, frames=report['frames'],
        candidate_sha256=digest, report=str(output / 'capture_report.json'),
        report_sha256=sha((output / 'capture_report.json').read_bytes()),
        ordinary_inputs_match_retained_predecessor=True, hardware_or_full_route_verification=False))
    print('Hodram ordinary-input cold boot complete')
