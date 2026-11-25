"""Replay a recorded New Game path through Deck View and both Filter options."""

from argparse import ArgumentParser
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import check_rafael_voyage_ceuta_20261119 as precedent
from scripts import headless_desmume_v193 as harness
from scripts import stage_deck_view_guidance_20261119 as stage
from scripts.run_activity_special_live_v988 import GrowingCommands

base = stage.base
ROOT = stage.ROOT / 'ordinary_deck'
HISTORY = Path('work/emulation_v193/deck_filter_v263/capture_report.json')
LISBON = Path('work/rafael_deck_after_trade_20261119/corrected/capture/capture_report.json')
LISBON_ROOT = stage.ROOT / 'ordinary_lisbon_deck'
JOURNAL = LISBON_ROOT / 'navigation.jsonl'
LISBON_START = 16800
STARTUP_DIR = stage.ROOT / 'own_startup'
STARTUP = stage.ROOT / 'own_startup_verification.json'
FRAMES = (18800, 19200, 19600, 20000, 20400, 20800, 21200, 21600, 22000)
END = FRAMES[-1] + 1


def schedule():
    recorded = base.load(HISTORY)
    assert recorded['cold_boot'] and not recorded['savestate_loaded'] and not recorded['callback_errors']
    assert not recorded.get('battery_save_preloaded') and recorded['frames'] == 20800
    assert not any(v for k, v in recorded.items() if k.startswith('synthetic_'))
    events = recorded['scripted_input_schedule']
    assert events[-1] == dict(start=20401, duration=12, buttons=['A'])
    return [*events, *(dict(start=frame, duration=12, buttons=[button]) for frame, button in (
        (20901, 'DOWN'), (21301, 'A'), (21701, 'B')))]


def capture(case):
    root = ROOT / case
    assert not root.exists()
    previous, proof = map(base.load, (stage.parent.RELEASE, stage.PROOF))
    assert previous['candidate_sha256'] == proof['predecessor_sha256'] == base.digest(stage.parent.ROM)
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    target = stage.parent.ROM if case == 'parent' else stage.ROM
    root.mkdir(parents=True)
    inputs = root / 'inputs.json'
    base.save(inputs, schedule())
    original = sys.argv
    sys.argv = [harness.__file__, '--rom', str(target), '--out', str(root / 'capture'), '--frames', str(END),
        '--inputs-json', str(inputs), '--press-start', '-1', '--capture-every', '999999',
        '--capture-at', *map(str, FRAMES), '--dump-capture-ram']
    try:
        harness.main()
    finally:
        sys.argv = original


def lisbon_capture(case):
    root = LISBON_ROOT / case
    assert not root.exists() and JOURNAL.is_file()
    prev, proof, recorded = map(base.load, (stage.parent.RELEASE, stage.PROOF, LISBON))
    assert base.digest(stage.parent.ROM) == prev['candidate_sha256'] == proof['predecessor_sha256']
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    assert recorded['cold_boot'] and not recorded['savestate_loaded'] and not recorded['callback_errors']
    assert not any(v for k, v in recorded.items() if k.startswith('synthetic_'))
    donor = recorded['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    root.mkdir(parents=True)
    inputs = root / 'inputs.json'
    base.save(inputs, recorded['scripted_input_schedule'])
    target = stage.parent.ROM if case == 'parent' else stage.ROM
    argv, original = sys.argv, sys.stdin
    stream = GrowingCommands(JOURNAL)
    try:
        sys.stdin = stream
        sys.argv = [harness.__file__, '--rom', str(target), '--out', str(root/'capture'), '--frames', '30000',
            '--inputs-json', str(inputs), '--press-start', '-1', '--touchscreen', '--battery-save', donor['source'],
            '--capture-every', '999999', '--pause-at', str(LISBON_START), '--dump-pause-ram']
        harness.main()
    finally:
        sys.argv, sys.stdin = argv, original
        stream.close()
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('parent', 'revised', 'capture-startup', 'startup', 'patch'))
    parser.add_argument('--lisbon', action='store_true')
    args = parser.parse_args()
    action = args.action
    adapted = SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, STAGED=stage.ROOT, parent=stage.parent)
    scope = vars(precedent) | dict(stage=adapted, STARTUP=STARTUP, STARTUP_DIR=STARTUP_DIR)
    if action in ('parent', 'revised'):
        (lisbon_capture if args.lisbon else capture)(action)
    elif action == 'patch':
        FunctionType(precedent.patch.__code__, scope)()
    else:
        FunctionType(precedent.startup.__code__, scope)(action == 'capture-startup')
