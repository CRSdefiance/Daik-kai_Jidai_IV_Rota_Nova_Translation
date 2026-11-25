"""Replay Square distribution and the original epidemic business reply."""

from argparse import ArgumentParser
from hashlib import sha256
from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as condition
from scripts import native_missionary_fixture_v623 as missionary
from scripts import replay_refit_help_startup_20261115 as startup
from scripts import stage_square_samples_wraps_20261115 as stage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


base = stage.base
HISTORY = Path('work/emulation_v193')
CASES = {'samples': ('giveaway_v746_new', 'missionary_fixture', 'synthetic_missionary_Chapel_assignment_fixtures',
                    (4800, 5200, 6800, 7200, 8000)),
         'epidemic': ('shop_business_v745_new', 'condition_fixture', 'synthetic_condition_fixtures',
                      (5600, 5900, 6050, 6150, 6250, 6400))}


def history(case):
    old, _, _, frames = CASES[case]
    path = HISTORY / old / 'capture_report.json'
    report = base.load(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = Path(report['battery_save_preloaded']['source'])
    assert base.digest(donor) == report['battery_save_preloaded']['source_sha256']
    return path, report, donor, frames


def epidemic(arm, raw, request):
    assert sha256(arm).hexdigest() == base.load(stage.STORED)['target_ARM9_sha256']
    assert len(raw) == 0x400000 and request == {'town': 22, 'condition': 1, 'days': 30}
    clean = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert all(arm[a:b] == clean[a:b] for a, b in ((0xB2E04, 0xB2E30), (0x5FA98, 0x5FB54)))
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    assert get(0xB65E4) == 22
    town = get(0xB6618)
    assert town == get(0xCB178) + 4 + 22 * 108
    assert get(0xB2E04, (town,)) == 12
    at = town + 0x6A - BASE
    changed = raw[:at] + bytes((1, 30)) + raw[at + 2:]
    u.mem_write(BASE, changed)
    assert get(0xB2E04, (town,)) == 1
    assert get(0x5FA98, (0, town)) == 683
    changes = [dict(address=BASE + i, before=raw[i], after=changed[i]) for i in range(at, at + 2) if raw[i] != changed[i]]
    assert len(changes) == 2
    return changed, dict(town_ID=22, town_address=town, original_status=12, supplied_status=1, supplied_days=30,
        original_shop_selection=683, changes=changes, before_RAM_sha256=sha256(raw).hexdigest(),
        after_RAM_sha256=sha256(changed).hexdigest(), natural_condition_event_verified=False)


def sample_fixture():
    arm_sha = base.load(stage.STORED)['target_ARM9_sha256']
    return FunctionType(missionary.assign.__code__, vars(missionary) | {'ARMS': (arm_sha,)})


def main(case):
    if case == 'startup':
        FunctionType(startup.main.__code__, vars(startup) | dict(stage=stage))()
        return
    _, key, receipt_key, _ = CASES[case]
    reference, old, source, frames = history(case)
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    root = stage.ROOT / case
    root.mkdir()
    copy = root / 'disposable_istanbul_input.dsv'
    copy.write_bytes(source.read_bytes())
    donor_sha = base.digest(copy)
    assert donor_sha == base.digest(source)
    inputs = root / 'inputs.json'
    base.save(inputs, old['scripted_input_schedule'])
    end = old['frames']
    requests = [dict(until=end, **{key: True if case == 'samples' else {'town': 22, 'condition': 1, 'days': 30}}),
                {'stop': True}]
    journal = root / 'commands.jsonl'
    journal.write_text(''.join(dumps(row) + '\n' for row in requests), encoding='utf-8')
    stdin, argv, original_assign, original_condition = sys.stdin, sys.argv, missionary.assign, condition.set_condition
    stream = GrowingCommands(journal)
    try:
        missionary.assign = sample_fixture()
        condition.set_condition = epidemic
        sys.stdin = stream
        sys.argv = [harness.__file__, '--rom', str(stage.ROM), '--out', str(root / 'capture'),
            '--frames', str(end + 1), '--inputs-json', str(inputs), '--battery-save', str(copy),
            '--touchscreen', '--press-start', '-1', '--capture-every', '999999', '--capture-at', *map(str, frames),
            '--pause-at', '3200', '--dump-pause-ram', '--allow-missionary-fixtures' if case == 'samples' else '--allow-condition-fixtures']
        harness.main()
    finally:
        sys.stdin, sys.argv, missionary.assign, condition.set_condition = stdin, argv, original_assign, original_condition
        stream.close()
    path = root / 'capture/capture_report.json'
    report = base.load(path)
    assert report['ROM_sha256'] == staged['candidate_sha256'] and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert base.digest(source) == base.digest(copy) == donor_sha
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert report['battery_save_preloaded']['source_sha256'] == donor_sha
    assert len(report[receipt_key]) == 1
    base.save(root / 'terminal.json', dict(report=str(path), report_sha256=base.digest(path), source_save_sha256=donor_sha,
        historical_capture=str(reference), historical_sha256=base.digest(reference), original_save_unchanged=True))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('startup', *CASES))
    main(parser.parse_args().case)
