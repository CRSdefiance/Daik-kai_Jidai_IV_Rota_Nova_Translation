"""Ordinary-input cold boot of the repaired ROM through Raphael's tutorial."""

import json
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands

ROM = Path('out/font_v2_square_scratch_fix_20261027_test.nds')
EXPECTED = '89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077'
ROOT = Path('work/raphael_tutorial_crowd_20261027')
CAP = Path('work/emulation_v193/raphael_tutorial_crowd_20261027')
PRIOR = Path('work/patch_interaction_audit_20261027/cases/rafael_guided/inputs.json')


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')


def main():
    assert sha(ROM.read_bytes()) == EXPECTED
    assert not ROOT.exists() and not CAP.exists()
    ROOT.mkdir(parents=True)
    inputs = ROOT/'opening_inputs.json'
    inputs.write_bytes(PRIOR.read_bytes())
    journal = ROOT/'navigation.jsonl'
    journal.write_text('', encoding='utf-8')
    save(ROOT/'plan.json',dict(ROM=str(ROM),ROM_sha256=EXPECTED,capture=str(CAP),
        opening_inputs=str(inputs),opening_inputs_sha256=sha(inputs.read_bytes()),
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        cold_boot=True,battery_preload=False,savestate_loaded=False,
        gameplay_or_event_or_rng_or_share_fixtures=False,
        harness_sha256=sha(Path(harness.__file__).read_bytes()),
        runner_sha256=sha(Path(__file__).read_bytes())))
    stream = GrowingCommands(journal)
    previous = sys.stdin
    sys.stdin = stream
    sys.argv = ['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),
        '--frames','240000','--inputs-json',str(inputs),'--pause-at','46020',
        '--capture-every','999999','--capture-at','44880','45240','45630','46020',
        '--touchscreen','--dump-pause-ram','--dump-capture-ram','--dump-ram','--dump-native-state']
    try:
        harness.main()
    finally:
        sys.stdin = previous
        stream.close()
    assert sha(ROM.read_bytes()) == EXPECTED
    save(ROOT/'terminal.json',dict(completed=True,ROM_sha256=EXPECTED,
        report=str(CAP/'capture_report.json'),no_gameplay_fixtures=True))


if __name__ == '__main__':
    main()
