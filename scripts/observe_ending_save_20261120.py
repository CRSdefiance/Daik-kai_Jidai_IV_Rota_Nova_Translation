"""Trace the DS ending save prompt from a disposable Rafael cartridge save."""

import io
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_ending_fixture_v537 as fixture
from scripts import observe_setup_save_common_v1 as observe
from scripts import register_tavern_round_digits_20261120 as current
from scripts.seal_shared_text_source_v1 import ARM, CLEAN


base = current.base
ROOT = Path('work/ending_save_scope_20261120')
HISTORY = Path('work/analysis/ending_transitions_v642')
EARLIER = Path('work/emulation_v193/ending_transitions_v642_rafael/capture_report.json')
PROMPT, SAVE = 0x0205466C, 0x0203EC84
# The generic observer labels both wrapper register snapshots as message_ID.
# At these two entries its index 6 captures r2. Only the COMMON calls below
# establish the loaded message ID. The wrapper traces establish the call sites.
TRACE_ARGUMENTS = observe.REQUESTS | {PROMPT: 6, SAVE: 6}


def replay(choice):
    previous, release, preflight = map(base.load, (EARLIER, current.RELEASE, HISTORY / 'preflight.json'))
    rom = current.stage.ROOT / 'clean_rebuilt.nds'
    assert base.digest(rom) == release['candidate_sha256']
    assert previous['ROM_sha256'] == preflight['candidate_sha256']
    before, after = map(base.NdsImage.open, (CLEAN, rom))
    clean_arm, arm = before.read_file(ARM), after.read_file(ARM)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    assert fixture.sha(arm) == release['target_ARM9_sha256']
    for row in preflight['original_code_ranges'][:5]:
        lo, hi = row['offset']
        assert row['exact_clean'] and fixture.sha(arm[lo:hi]) == row['sha256'] and arm[lo:hi] == clean_arm[lo:hi]
    assert after.read_file('/FLS/M29.fls') == before.read_file('/FLS/M29.fls')
    donor = previous['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    assert previous['scripted_input_schedule'] == base.load(HISTORY / 'rafael_inputs.json')
    earlier_fixture, = previous['synthetic_ending_fixtures']
    assert earlier_fixture['frame'] == 3000 and earlier_fixture['active_captain_id'] == 0

    folder = ROOT / choice
    assert not folder.exists()
    construct = FunctionType(observe.scoped_observer.__code__, vars(observe) | {'REQUESTS': TRACE_ARGUMENTS})
    trace_class = construct(rom, folder)
    inputs = folder / 'inputs.json'
    base.save(inputs, previous['scripted_input_schedule'])
    commands = [dict(ending_captain=0, until=12400),
                dict(buttons=['B' if choice == 'no' else 'A'], duration=8, until=13100)]
    if choice in ('save', 'confirm'):
        commands.extend([dict(buttons=['DOWN'], duration=8, until=13500),
                         dict(buttons=['A'], duration=8, until=14100)])
    if choice == 'confirm':
        commands.append(dict(buttons=['A'], duration=8, until=15200))
    end = commands[-1]['until']
    commands.append(dict(stop=True))
    command_file = folder / 'commands.json'
    base.save(command_file, commands)
    stream = io.StringIO(''.join(json.dumps(row) + '\n' for row in commands))
    original_ct, original_argv, original_stdin = harness.ct, sys.argv, sys.stdin
    original_shas = fixture.VERIFIED_ARM_SHAS
    attached = []

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(original_ct, name)

        def CDLL(self, path, *args, **kwargs):
            core = original_ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                recorder = trace_class(core, folder)
                recorder.install()
                attached.append(recorder)
                advance = core.retro_run
                advance.restype = None

                def tick():
                    recorder.header[0] += 1
                    advance()

                core.retro_run = tick
            return core

    try:
        fixture.VERIFIED_ARM_SHAS = original_shas | {fixture.sha(arm)}
        harness.ct, sys.stdin = CoreLoader(), stream
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'),
                    '--frames', str(end + 300), '--capture-every', '999999', '--pause-at', '3000',
                    '--inputs-json', str(inputs), '--press-start', '-1', '--touchscreen',
                    '--battery-save', donor['source'], '--allow-ending-fixtures']
        if choice == 'confirm':
            sys.argv += ['--capture-at', '14280', '14600']
        harness.main()
    finally:
        fixture.VERIFIED_ARM_SHAS = original_shas
        harness.ct, sys.argv, sys.stdin = original_ct, original_argv, original_stdin
        stream.close()
        for recorder in attached:
            recorder.close()
    recorder, = attached
    recorder.save()
    report = base.load(folder / 'capture/capture_report.json')
    assert report['frames'] == end and report['ROM_sha256'] == release['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['earned_completion_verified'] and not report['hardware_device_verification']
    applied, = report['synthetic_ending_fixtures']
    assert applied['frame'] == 3000 and applied['changes'] == earlier_fixture['changes']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('choice', choices=['yes', 'no', 'save', 'confirm'])
    replay(parser.parse_args().choice)
