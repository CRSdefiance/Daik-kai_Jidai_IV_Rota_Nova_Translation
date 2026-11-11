"""Replay Lisbon trade and Guild reporting from a verified ordinary battery save."""

import builtins
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_golden_route_exchanges_v1 as prior
from scripts import replay_trade_good_descriptions_v1 as trade
from scripts import stage_golden_route_exchanges_v2 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


base = prior.base
STARTUP = stage.ROOT / 'own_startup'
SALE = stage.ROOT / 'lisbon_sale_and_guild'
PAUSE, END = 10400, 26000
discount_salt_purchase = FunctionType(prior.discount_salt_purchase.__code__, vars(prior) | {'stage': stage})
cold_boot = FunctionType(prior.cold_boot.__code__, vars(prior) | dict(stage=stage, STARTUP=STARTUP))


def gameplay():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    plan = base.load(trade.SOURCE / 'run_plan.json')
    donor = plan['source_save']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    original_inputs = trade.SOURCE / 'unchanged_ordinary_inputs.json'
    assert base.digest(original_inputs) == plan['unchanged_inputs_sha256']
    inputs = [row for row in base.load(original_inputs) if row['start'] <= PAUSE]
    assert inputs[-1] == dict(start=10001, duration=8, buttons=['DOWN'])
    SALE.mkdir()
    schedule, commands = SALE / 'inputs.json', SALE / 'commands.jsonl'
    base.save(schedule, inputs)
    with commands.open('x', encoding='utf-8'):
        pass
    harness = prior.harness
    source = checked_text(getsource(harness.main), {
        'from scripts.native_golden_route_fixture_v613 import discount_salt_purchase':
            'from scripts.replay_golden_route_exchanges_v2 import discount_salt_purchase',
    })
    env = dict(vars(harness))
    exec(compile(source, __file__ + '::lisbon-trade-and-guild', 'exec'), env)
    args = [str(Path(harness.__file__)), '--rom', str(stage.ROM), '--out', str(SALE / 'capture'),
            '--frames', str(END), '--inputs-json', str(schedule), '--touchscreen', '--press-start', '-1',
            '--capture-every', '999999', '--pause-at', str(PAUSE),
            '--dump-pause-ram', '--allow-golden-route-fixtures', '--battery-save', donor['source']]
    original_input, original_args = builtins.input, sys.argv
    reader = GrowingCommands(commands)
    try:
        builtins.input = lambda *unused: reader.readline().rstrip('\n')
        sys.argv = args
        env['main']()
    finally:
        builtins.input, sys.argv = original_input, original_args
        reader.close()
    report_path = SALE / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == proof['research_ROM_sha256'] and report['frames'] <= END
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['source_sha256'] == base.digest(donor['source']) == donor['source_sha256']
    base.save(SALE / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'],
        report=str(report_path), report_sha256=base.digest(report_path),
        source_capture=str(trade.SOURCE / 'run_plan.json'), source_capture_sha256=base.digest(trade.SOURCE / 'run_plan.json'),
        commands=str(commands), commands_sha256=base.digest(commands), inputs_sha256=base.digest(schedule),
        original_save_unchanged=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
