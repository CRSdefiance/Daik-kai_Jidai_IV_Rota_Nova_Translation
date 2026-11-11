"""Cold-boot the Golden Route candidate and replay the original sale and guild visit."""

import builtins
from inspect import getsource
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_golden_route_fixture_v613 as cost_fixture
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import run_golden_plaques_v613 as historical
from scripts import stage_golden_route_exchanges_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.review.parent.base
STARTUP = stage.ROOT / 'own_startup'
SALE = stage.ROOT / 'lisbon_sale_and_guild'
PREVIOUS = stage.review.parent.verified.replay.STARTUP
DONOR = historical.CAP / 'golden_route_plaques_v613_sale_current/capture_report.json'
SOURCE_ROM = Path('out/all_routes_combined_v613_candidate.nds')
PAUSE, END = 22000, 34300
CAPTURES = (22000, 22600, 23200, 23500, 23800, 24100, 24400, 24700, 25000, 30400,
            32800, 33100, 33400, 33700, 34000, END)


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=PREVIOUS)
    FunctionType(startup.main.__code__, env)()


def discount_salt_purchase(arm, raw, cost):
    assert arm == base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert base.digest(SOURCE_ROM) == base.load(DONOR)['ROM_sha256']
    reference = base.NdsImage.open(SOURCE_ROM).read_file(stage.ARM)
    bindings = ((0xBCCFC, 0xBCD7C), (0xDB148, 0xDB278), (0x2158694 - stage.BASE, 0x21586B0 - stage.BASE))
    for start, end in bindings:
        assert arm[start:end] == reference[start:end], (start, end)
    fixture = FunctionType(cost_fixture.discount_salt_purchase.__code__,
                           vars(cost_fixture) | {'ARMS': {cost_fixture.sha(arm)}})
    after, receipt = fixture(arm, raw, cost)
    return after, receipt | {'original_consumer_spans_match_observed_legacy_run': bindings}


def gameplay():
    staged = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == staged['research_ROM_sha256']
    donor = base.load(DONOR)
    assert donor['cold_boot'] and not donor['savestate_loaded'] and not donor['callback_errors']
    assert donor['frames'] == END and base.digest(SOURCE_ROM) == donor['ROM_sha256']
    assert donor['synthetic_golden_route_display_fixtures'][0]['frame'] == PAUSE
    assert not SALE.exists()
    SALE.mkdir()
    plan, commands = SALE / 'inputs.json', SALE / 'commands.jsonl'
    base.save(plan, donor['scripted_input_schedule'])
    schedule = [dict(golden_route_purchase_cost=1, until=END), dict(stop=True)]
    commands.write_text(''.join(dumps(row) + '\n' for row in schedule), encoding='utf-8')
    source = checked_text(getsource(harness.main), {
        'from scripts.native_golden_route_fixture_v613 import discount_salt_purchase':
            'from scripts.replay_golden_route_exchanges_v1 import discount_salt_purchase',
    })
    env = dict(vars(harness))
    exec(compile(source, __file__ + '::focused-sale', 'exec'), env)
    args = [str(Path(harness.__file__)), '--rom', str(stage.ROM), '--out', str(SALE / 'capture'),
            '--frames', str(END), '--inputs-json', str(plan), '--touchscreen',
            '--capture-every', '999999', '--capture-at', *map(str, CAPTURES),
            '--pause-at', str(PAUSE), '--dump-pause-ram', '--dump-capture-ram',
            '--allow-golden-route-fixtures']
    queue = iter(schedule)
    original_input, original_args = builtins.input, sys.argv
    try:
        builtins.input = lambda *unused: dumps(next(queue))
        sys.argv = args
        env['main']()
    finally:
        builtins.input, sys.argv = original_input, original_args
    report_path = SALE / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == staged['research_ROM_sha256'] and report['frames'] == END
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    base.save(SALE / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'],
        report=str(report_path), report_sha256=base.digest(report_path),
        source_capture=str(DONOR), source_capture_sha256=base.digest(DONOR),
        commands=str(commands), commands_sha256=base.digest(commands), inputs_sha256=base.digest(plan)))


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
