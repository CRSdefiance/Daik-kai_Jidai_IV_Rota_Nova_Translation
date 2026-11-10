"""Replay the retained ordinary sailing input schedule; no injected gameplay state."""

import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness

ROOT = Path('work/font_offset_test_20261027')
ROM = Path('out/font_v2_draw_down_two_20261027_test.nds')


if __name__ == '__main__':
    prior = Path('work/emulation_v193/footer_measurement_v318/capture_report.json')
    old = json.loads(prior.read_text())
    assert old['cold_boot'] and not old['savestate_loaded'] and not old.get('battery_save_preloaded')
    inputs = ROOT / 'sailing_inputs.json'
    inputs.write_text(json.dumps(old['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    plan = dict(candidate=str(ROM), candidate_sha256=sha(ROM.read_bytes()), frames=32800,
        source_schedule_report=str(prior), source_schedule_report_sha256=sha(prior.read_bytes()),
        inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
        no_battery_savestate_RAM_or_gameplay_injection=True,
        old_input_schedule_may_reach_different_screens_after_editorial_timing_changes=True)
    (ROOT / 'sailing_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(ROOT / 'cold_boot_sailing'),
        '--frames', '32800', '--inputs-json', str(inputs), '--touchscreen', '--capture-every', '999999',
        '--capture-at', '1100', '4000', '11900', '24000', '28000', '30000', '30400', '30800', '31200', '32000', '32800']
    harness.main()
    path = ROOT / 'cold_boot_sailing/capture_report.json'
    report = json.loads(path.read_text())
    assert report['ROM_sha256'] == plan['candidate_sha256'] and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    (ROOT / 'sailing_terminal.json').write_text(json.dumps(dict(terminal=True,
        frames=report['frames'], report=str(path), report_sha256=sha(path.read_bytes()),
        candidate_sha256=plan['candidate_sha256']), indent=2) + '\n', encoding='utf-8')
    print('Ordinary sailing input replay complete; screen coverage awaits visual review.')
