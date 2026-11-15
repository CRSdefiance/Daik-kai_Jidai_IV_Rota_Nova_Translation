"""Replay the original Square rumor selections with disclosed region and RNG fixtures."""

from argparse import ArgumentParser
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_missionary_fixture_v623 as dispatcher
from scripts import native_regional_rumor_fixture_v749 as fixture
from scripts import replay_refit_help_startup_20261115 as startup
from scripts import stage_square_rumors_20261115 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


base = stage.base
FRAMES = (5600, 5900, 6050, 6150, 6250, 6400)
FIXTURE_RECEIPT = 'synthetic_missionary_Chapel_assignment_fixtures'


def history(region):
    path = Path(f'work/emulation_v193/rumors_v749_region{region}_final_new/capture_report.json')
    report = base.load(path)
    assert report['frames'] == 6500 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = Path(report['battery_save_preloaded']['source'])
    assert base.digest(donor) == report['battery_save_preloaded']['source_sha256']
    return path, report, donor


def region_fixture(region):
    stage_receipt, release = map(base.load, (stage.STORED, stage.parent.RELEASE))
    arm_sha = stage_receipt['target_ARM9_sha256']
    assert arm_sha == release['target_ARM9_sha256']
    config = dict(source_arm9_sha256=arm_sha, target_arm9_sha256=arm_sha)
    direct = FunctionType(fixture.assign.__code__, vars(fixture) | dict(read=lambda _: config))

    def apply(arm, raw, enabled):
        assert enabled is True
        return direct(arm, raw, {'region': region})

    return apply


def main(case):
    if case == 'startup':
        FunctionType(startup.main.__code__, vars(startup) | dict(stage=stage))()
        return
    region = int(case)
    old_path, old, donor = history(region)
    root = stage.ROOT / f'region{region}'
    root.mkdir()
    donor_copy = root / 'disposable_hodram_istanbul.dsv'
    donor_copy.write_bytes(donor.read_bytes())
    donor_sha = base.digest(donor_copy)
    inputs = root / 'inputs.json'
    base.save(inputs, old['scripted_input_schedule'])
    end = old['frames']
    journal = root / 'commands.jsonl'
    commands = [dict(until=end, missionary_fixture=True), {'stop': True}]
    journal.write_text(''.join(dumps(command) + '\n' for command in commands), encoding='utf-8')
    original = sys.stdin, sys.argv, dispatcher.assign
    stream = GrowingCommands(journal)
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    try:
        sys.stdin = stream
        dispatcher.assign = region_fixture(region)
        sys.argv = [harness.__file__, '--rom', str(stage.ROM), '--out', str(root / 'capture'),
            '--frames', str(end + 1), '--inputs-json', str(inputs), '--battery-save', str(donor_copy),
            '--touchscreen', '--press-start', '-1', '--capture-every', '999999', '--capture-at', *map(str, FRAMES),
            '--pause-at', '5800', '--dump-pause-ram', '--dump-capture-ram', '--allow-missionary-fixtures']
        harness.main()
    finally:
        sys.stdin, sys.argv, dispatcher.assign = original
        stream.close()
    path = root / 'capture/capture_report.json'
    report = base.load(path)
    assert report['ROM_sha256'] == staged['candidate_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert base.digest(donor) == base.digest(donor_copy) == donor_sha
    assert report['battery_save_preloaded']['source_sha256'] == donor_sha
    used, = report[FIXTURE_RECEIPT]
    assert used['synthetic_regional_rumor_fixture'] and used['expected_native_rumor_message'] == 709 + region
    base.save(root / 'terminal.json', dict(report=str(path), report_sha256=base.digest(path), donor_sha256=donor_sha,
        original_save_unchanged=True, history=str(old_path), history_sha256=base.digest(old_path),
        harness_fixture_slot='Reused original generic RAM fixture slot. The installed callback supplies only the regional rumor setup.'))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('startup', '0', '20'))
    main(parser.parse_args().case)
