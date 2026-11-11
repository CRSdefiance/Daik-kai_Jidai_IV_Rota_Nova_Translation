"""Replay original Search outcomes with the disclosed historical test fixtures."""

from inspect import getsource
from json import dumps, loads
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts import native_fatigue_region2_fixture_v1605 as location
from scripts import native_hot_spring_crew_v1650 as crew
from scripts import native_hot_spring_provisions_v1642 as supplies
from scripts import replay_battle_commands_and_outcomes_v1 as prior
from scripts import stage_crew_and_shore_reports_v2 as stage
from scripts.native_hot_spring_resilient_v1644 import preserve_natural_health
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


base = prior.base
STARTUP = stage.ROOT / 'own_startup'
SCENES = {
    'attack': (Path('work/analysis/search_reports_live_v1680'), 20792),
    'welcome': (Path('work/analysis/hot_spring_crew_v1651'), 46616),
}


def fixtures(expected_arm_sha):
    bound = {}
    for fixture, old_registry in (
        (location, 'work/analysis/fatigue_status_release_v1593/registered_release_verification.json'),
        (supplies, 'translations/hot_spring_notice_editorial_release_v1.json'),
        (crew, 'translations/hot_spring_notice_editorial_release_v1.json'),
    ):
        body = getsource(fixture.apply_fixture)
        if fixture is not crew:
            body = preserve_natural_health(body)

        def read(path, old=old_registry):
            if str(path) == old:
                return dict(ARM9_sha256=expected_arm_sha, target_arm9_sha256=expected_arm_sha)
            return base.load(path)

        env = vars(fixture) | {'read': read, '__file__': __file__}
        exec(compile(body, __file__ + '::historical-search-fixture', 'exec'), env)
        bound[tuple(fixture.REQUEST.items())] = env['apply_fixture']

    def apply(arm, raw, request):
        return bound[tuple(request.items())](arm, raw, request)

    return apply


def cold_boot():
    runner = prior.prior.prior.startup
    env = vars(runner) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(runner.main.__code__, env)()


def history(name):
    folder, end = SCENES[name]
    plan = base.load(folder / 'run_plan.json')
    report_path = Path(plan['capture_folder']) / 'capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == plan['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] >= end
    donor, inputs = Path(plan['source_donor']), Path(plan['original_load_inputs'])
    assert base.digest(donor) == plan['source_donor_sha256'] == report['battery_save_preloaded']['source_sha256']
    assert base.digest(inputs) == plan['original_load_inputs_sha256']
    journal = Path(plan['append_only_navigation'])
    assert base.digest(journal) == base.load(folder / 'terminal_preservation.json')['navigation_sha256']
    commands = [loads(line) for line in journal.read_text(encoding='utf-8').splitlines()]
    received = base.load(report_path.with_name('navigation_command_journal.json'))['commands_received']
    assert all(row['validation_passed'] for row in received)
    assert [row['command'] for row in received] == commands
    commands = [command for command in commands if command.get('until', end + 1) <= end]
    assert commands[-1]['until'] == end
    return plan, report_path, report, donor, inputs, commands + [dict(stop=True)], end


def gameplay(name):
    root = stage.ROOT / f'shore_{name}'
    assert not root.exists()
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    plan, old_report_path, _, donor, inputs, commands, end = history(name)
    root.mkdir()
    command_path = root / 'commands.jsonl'
    command_path.write_text(''.join(dumps(command) + '\n' for command in commands), encoding='utf-8')
    stream = GrowingCommands(command_path)
    old, old_fixture = (sys.stdin, sys.argv), dispatch.apply_fixture
    try:
        sys.stdin, dispatch.apply_fixture = stream, fixtures(proof['research_ARM9_sha256'])
        sys.argv = [str(Path(harness.__file__)), '--rom', str(stage.ROM), '--out', str(root / 'capture'),
            '--frames', str(end + 1), '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
            '--capture-every', '999999', '--pause-at', str(plan['initial_pause_frame']), '--dump-pause-ram',
            '--dump-ram', '--allow-battle-fixtures']
        harness.main()
    finally:
        sys.stdin, sys.argv = old
        dispatch.apply_fixture = old_fixture
        stream.close()
    report_path = root / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == proof['research_ROM_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert base.digest(donor) == plan['source_donor_sha256']
    base.save(root / 'terminal.json', dict(scenario=name, report=str(report_path), report_sha256=base.digest(report_path),
        commands=str(command_path), commands_sha256=base.digest(command_path), unchanged_original_save=True,
        historical_report=str(old_report_path), historical_report_sha256=base.digest(old_report_path)))


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['attack'], ['welcome'])
    if sys.argv[1] == 'startup':
        cold_boot()
    else:
        gameplay(sys.argv[1])
