"""Replay the original promoter, specialty, and Market branches on the staged ROM."""

from argparse import ArgumentParser
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import native_market_fixture_v753 as market
from scripts import native_promoter_travel_fixture_v750 as promoter
from scripts import native_specialty_fixture_v752 as specialty
from scripts import replay_refit_help_startup_20261115 as startup
from scripts import run_market_capture_v753 as run_market
from scripts import run_promoter_travel_capture_v750 as run_promoter
from scripts import run_specialty_capture_v752 as run_specialty
from scripts import stage_town_market_wraps_20261115 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


base = stage.base
HISTORY = Path('work/emulation_v193')
CASES = {
    'promoter': (promoter, run_promoter, 'town_v750_accept_new', 'town_events_editorial_release_v1',
                 'promoter-travel', 'synthetic_promoter_travel_fixtures', (4600, 4800, 5000, 5400)),
    'specialty': (specialty, run_specialty, 'specialty_v752_accept_752_final', 'specialty_question_editorial_release_v1',
                  'specialty', 'synthetic_specialty_inventory_fixtures', (4200, 4600, 5000, 5200, 5800)),
    'market': (market, run_market, 'market_v753_low_funds_probe', 'market_replies_editorial_release_v1',
               'market', 'synthetic_market_display_fixtures', (5400, 5600, 6200, 6800)),
}


def history(case):
    _, _, old, _, _, _, frames = CASES[case]
    reference = HISTORY / old / 'capture_report.json'
    report = base.load(reference)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = Path(report['battery_save_preloaded']['source'])
    assert base.digest(donor) == report['battery_save_preloaded']['source_sha256']
    journal = base.load(reference.with_name('navigation_command_journal.json'))['commands_received']
    assert [row['frame'] for row in journal] == [3200, report['frames']]
    assert all(row['validation_passed'] for row in journal) and journal[-1]['command'] == {'stop': True}
    return reference, report, donor, [row['command'] for row in journal], frames


def fixture_for(case, arm_sha):
    module, _, _, config, _, _, _ = CASES[case]
    exact_config = Path(f'translations/{config}.json')

    def read(path):
        result = base.load(path)
        assert Path(path) == exact_config
        return result | {'target_arm9_sha256': arm_sha}

    # Retain all original fixtures' instruction, data-value and delta guards.
    return FunctionType(module.assign.__code__, vars(module) | dict(read=read))


def main(case):
    if case == 'startup':
        FunctionType(startup.main.__code__, vars(startup) | dict(stage=stage))()
        return
    module, runner, _, _, flag, fixture_key, _ = CASES[case]
    root = stage.ROOT / case
    assert not root.exists()
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    reference, old, source, commands, frames = history(case)
    end = old['frames']
    root.mkdir()
    donor = root / 'disposable_istanbul_input.dsv'
    donor.write_bytes(source.read_bytes())
    donor_sha = base.digest(donor)
    assert donor_sha == base.digest(source)
    inputs = root / 'inputs.json'
    base.save(inputs, old['scripted_input_schedule'])
    journal = root / 'commands.jsonl'
    journal.write_text(''.join(dumps(command) + '\n' for command in commands), encoding='utf-8')
    stdin, argv, fixture = sys.stdin, sys.argv, module.assign
    stream = GrowingCommands(journal)
    try:
        module.assign = fixture_for(case, staged['target_ARM9_sha256'])
        sys.stdin = stream
        sys.argv = [str(Path(runner.__file__)), '--rom', str(stage.ROM), '--out', str(root / 'capture'),
            '--frames', str(end + 1), '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
            '--press-start', '-1', '--capture-every', '999999', '--capture-at', *map(str, frames),
            '--pause-at', '3200', '--dump-pause-ram', '--dump-ram', f'--allow-{flag}-fixtures']
        runner.main()
    finally:
        sys.stdin, sys.argv, module.assign = stdin, argv, fixture
        stream.close()
    report_path = root / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == staged['candidate_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert base.digest(source) == base.digest(donor) == donor_sha
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert report['battery_save_preloaded']['source_sha256'] == donor_sha
    assert len(report[fixture_key]) == 1
    assert report[fixture_key][0]['changes'] == old[fixture_key][0]['changes']
    base.save(root / 'terminal.json', dict(case=case, report=str(report_path), report_sha256=base.digest(report_path),
        historical_capture=str(reference), historical_sha256=base.digest(reference), frames=end,
        donor_sha256=donor_sha, original_save_unchanged=True))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('startup', *CASES))
    main(parser.parse_args().case)
