"""Run both town-confirmation transitions with the original Sao Tome setup."""

from inspect import getsource
from json import dumps, loads
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_aftermath_town_fixture_v1290 as original
from scripts import native_battle_fixture_v620 as dispatch
from scripts import replay_pirate_and_retreat_reports_v1 as prior
from scripts import stage_battle_commands_and_outcomes_v2 as stage
from scripts.replay_fleet_reports_v1 import DONOR, DONOR_SHA
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


base = prior.base
STARTUP = stage.ROOT / 'own_startup'
HISTORY = Path('work/analysis/aftermath_town_v1291')
HISTORICAL_CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_town_v1291_1266')


def cold_boot():
    runner = prior.prior.startup
    env = vars(runner) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(runner.main.__code__, env)()


def fixture_for_candidate():
    source = checked_text(getsource(original.apply_fixture), {
        "sha(arm) == read('translations/battle_aftermath_editorial_release_v1.json')['target_arm9_sha256']":
            "sha(arm) == read(stage.PROOF)['research_ARM9_sha256']",
        'actors+4+18*32': 'actors+4+16*32',
        '== 18 and get(0x7E100': '== 16 and get(0x7E100',
        'assignments[8] == 18 and assignments[15] == 208 and assignments.count(18)':
            'assignments[21] == 16 and assignments[15] == 208 and assignments.count(16)',
        'get(0x82BB8,duty,8,208)': 'get(0x82BB8,duty,21,208)',
        'get(0x82BB8,duty,15,18)': 'get(0x82BB8,duty,15,16)',
        'get(0x82478,duty,1) == 18': 'get(0x82478,duty,1) == 16',
        'duty+6+8,duty+6+15': 'duty+6+21,duty+6+15',
        "'First_Mate_existing_actor_ID':18": "'First_Mate_existing_actor_ID':16",
        "'prior_assignment_slot':8": "'prior_assignment_slot':21",
        'charles': 'gerhard',
    })
    water = FunctionType(original.water.__code__, original.water.__globals__ | {'ROM': stage.ROM})
    env = vars(original) | {'water': water, 'stage': stage, '__file__': __file__}
    exec(compile(source, __file__ + '::original-Sao-Tome-fixture', 'exec'), env)
    return env['apply_fixture']


def gameplay(action):
    assert action in ('accept', 'cancel')
    root = stage.ROOT / f'town_attack_{action}'
    assert not root.exists() and base.digest(DONOR) == DONOR_SHA
    evidence = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == evidence['research_ROM_sha256']
    historical = base.load(HISTORICAL_CAPTURE / 'capture_report.json')
    assert historical['cold_boot'] and not historical['savestate_loaded'] and not historical['callback_errors']
    assert historical['battery_save_preloaded']['source_sha256'] == DONOR_SHA
    journal = base.load(HISTORICAL_CAPTURE / 'navigation_command_journal.json')['commands_received']
    assert all(row['validation_passed'] for row in journal)
    previous = [loads(line) for line in (HISTORY / 'navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    assert [row['command'] for row in journal] == previous
    commands = [row for row in previous if row.get('until', 999999) <= 5810]
    assert commands[-1] == dict(until=5810, touch=[132, 123], duration=8)
    commands += [dict(until=5910, buttons=['A' if action == 'accept' else 'B'], duration=8),
                 dict(until=6010, duration=1), dict(stop=True)]
    root.mkdir()
    command_path = root / 'commands.jsonl'
    command_path.write_text(''.join(dumps(command) + '\n' for command in commands), encoding='utf-8')
    inputs = HISTORY / 'original_load_inputs.json'
    assert base.load(inputs) == [event for event in historical['scripted_input_schedule'] if event['start'] <= 3400]
    stream = GrowingCommands(command_path)
    old, old_fixture = (sys.stdin, sys.argv), dispatch.apply_fixture
    try:
        sys.stdin, dispatch.apply_fixture = stream, fixture_for_candidate()
        sys.argv = [str(Path(harness.__file__)), '--rom', str(stage.ROM), '--out', str(root / 'capture'),
            '--frames', '6011', '--inputs-json', str(inputs), '--battery-save', str(DONOR), '--touchscreen',
            '--capture-every', '999999', '--pause-at', '3400', '--dump-pause-ram', '--dump-ram', '--allow-battle-fixtures']
        harness.main()
    finally:
        sys.stdin, sys.argv = old
        dispatch.apply_fixture = old_fixture
        stream.close()
    report_path = root / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == evidence['research_ROM_sha256'] and report['frames'] == 6010
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert base.digest(DONOR) == DONOR_SHA
    base.save(root / 'terminal.json', dict(action=action, report=str(report_path), report_sha256=base.digest(report_path),
        commands=str(command_path), commands_sha256=base.digest(command_path), unchanged_original_save=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['accept'], ['cancel'])
    if sys.argv[1] == 'startup':
        cold_boot()
    else:
        gameplay(sys.argv[1])
