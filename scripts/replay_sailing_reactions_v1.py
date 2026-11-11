"""Replay the original returning-wind and white-whale portrait sequences."""

import json
from pathlib import Path
from struct import unpack
import sys
from types import FunctionType, SimpleNamespace

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import replay_item_production_advice_v1 as precedent
from scripts import stage_sailing_reactions_v2 as candidate
from scripts.native_call_abi_v764 import call
from scripts.native_inventory_fixture_v481 import machine
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.run_sea_event_bubbles_focused_v2 import OUT as DONOR_REPLAY


stage = SimpleNamespace(**candidate.stage_environment())
ROOT = stage.ROOT / 'focused_reactions'
STARTUP = stage.ROOT / 'own_startup'
PRIOR = stage.parent.TEST.parent / 'trade_good_descriptions_staged_20261111_v4' / 'own_startup'
PAUSE, END = 8327, 12000
COMMANDS = (
    dict(until=9700, condition_fixture={'event': 'wind'}, buttons=['UP'], duration=400),
    dict(until=9900, buttons=['A'], duration=8),
    dict(until=11400, condition_fixture={'event': 'whale'}, buttons=[], duration=8),
    dict(until=11600, buttons=['A'], duration=8),
    dict(until=11800, buttons=['A'], duration=8),
    dict(until=END, buttons=['A'], duration=8),
    dict(stop=True),
)


def set_condition(arm, raw, request):
    event = request['event']
    assert request == {'event': event} and event in ('wind', 'whale')
    assert arm == stage.NdsImage.open(stage.ROM).read_file(stage.ARM) and len(raw) == 0x400000
    source = stage.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    for start, end in ((0x82B0C, 0x82B38), (0x7A570, 0x7AE54)):
        assert source[start:end] == arm[start:end]
    cpu = machine(arm)
    cpu.mem_write(stage.BASE, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    assert get(0x7F244) == 1
    fleet = get(0xCB1A8) + 0x2090
    clock = get(0xCB1B4)
    tick = unpack('<I', cpu.mem_read(clock + 8, 4))[0]
    before = get(0x82B30, fleet)
    kind = {'wind': 24, 'whale': 11}[event]
    assert before == 27, (event, before)
    get(0x82B0C, fleet, kind)
    assert get(0x82B30, fleet) == kind and get(0x82B28, fleet) == tick
    after = bytes(cpu.mem_read(stage.BASE, len(raw)))
    allowed = {fleet + 0x2C, *range(fleet + 0x30, fleet + 0x34)}
    changes = [dict(address=stage.BASE + i, before=x, after=y) for i, (x, y) in enumerate(zip(raw, after)) if x != y]
    assert changes and all(row['address'] in allowed for row in changes)
    return after, dict(event=event, original_fleet_condition_setter=0x02082B0C,
        fleet=fleet, previous_condition=before, supplied_condition=kind, original_timestamp=tick,
        changes=changes, timer_and_original_dialogue_dispatch_run_in_emulator=True,
        natural_event_selection_verified=False)


def gameplay():
    base = stage.base
    assert not ROOT.exists()
    evidence = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == evidence['research_ROM_sha256']
    terminal = base.load(DONOR_REPLAY / 'terminal.json')
    assert base.digest(terminal['report']) == terminal['report_sha256']
    donor = base.load(terminal['report'])['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    source_inputs = DONOR_REPLAY / 'original_input_prefix.json'
    assert base.digest(source_inputs) == terminal['original_input_prefix_sha256']
    ROOT.mkdir()
    commands = ROOT / 'commands.jsonl'
    commands.write_text(''.join(json.dumps(command) + '\n' for command in COMMANDS), encoding='utf-8')
    harness = Path('scripts/headless_desmume_v193.py')
    source = harness.read_text(encoding='utf-8')
    token = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(token) == 1
    source = source.replace(token, 'from scripts.replay_sailing_reactions_v1 import set_condition')
    args = ['--rom', str(stage.ROM), '--out', str(ROOT / 'capture'), '--frames', str(END + 1),
        '--inputs-json', str(source_inputs), '--battery-save', donor['source'], '--touchscreen',
        '--capture-every', '999999', '--pause-at', str(PAUSE), '--allow-condition-fixtures',
        '--dump-pause-ram', '--dump-ram']
    old_in, old_args = sys.stdin, sys.argv
    stream = GrowingCommands(commands)
    try:
        sys.stdin, sys.argv = stream, [str(harness), *args]
        exec(compile(source, str(harness), 'exec'), {'__name__': '__main__', '__file__': str(harness.resolve())})
    finally:
        sys.stdin, sys.argv = old_in, old_args
        stream.close()
    report_path = ROOT / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == evidence['research_ROM_sha256'] and report['frames'] == END
    assert base.digest(donor['source']) == donor['source_sha256']
    base.save(ROOT / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'], report=str(report_path),
        report_sha256=base.digest(report_path), commands=str(commands), commands_sha256=base.digest(commands),
        unchanged_original_save=True))


def cold_boot():
    env = vars(precedent.startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=PRIOR)
    FunctionType(precedent.startup.main.__code__, env)()


if __name__ == '__main__':
    assert sys.argv[1:] in (['gameplay'], ['startup'])
    (gameplay if sys.argv[1] == 'gameplay' else cold_boot)()
