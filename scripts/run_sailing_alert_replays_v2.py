"""Replay ordinary sailing and focused level-up and becalmed displays."""

import argparse
import json
from pathlib import Path
import struct
import sys
from types import FunctionType

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.run_sea_event_bubbles_focused_v2 import OUT as FOCUSED, PAUSE, set_condition as bubbles_selector
from scripts.stage_sailing_alert_balanced_v2 import PROOF, ROM, ROOT


HISTORIC_REEFS = Path('work/emulation_v193/sailing_conditions_v309/capture_report.json')
HARNESS = Path('scripts/headless_desmume_v193.py')


def set_condition(arm, raw, request):
    env = {**bubbles_selector.__globals__, 'ROM': ROM}
    mode = request['mode']
    if mode in ('choose-becalmed', 'restore-becalmed'):
        # Dispatcher index 18 reaches the original Calm branch at 02032508.
        assert request == {'mode': mode}
        assert struct.unpack_from('<I', arm, 0x31F70)[0] == 0xEA000164
        env['FOCUSED'] = struct.pack('<I', 0xE3A00012)
        selector = FunctionType(bubbles_selector.__code__, env)
        delegate_mode = 'choose-bubbles' if mode == 'choose-becalmed' else 'restore-selection'
        result, receipt = selector(arm, raw, {'mode': delegate_mode})
        return result, receipt | {'mode': mode, 'scoped_input': 18}
    return FunctionType(bubbles_selector.__code__, env)(arm, raw, request)


def inputs_for(mode, output):
    reference = HISTORIC_REEFS if mode == 'reefs' else FOCUSED / 'capture/capture_report.json'
    report = load(reference)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    inputs = output / 'inputs.json'
    if mode == 'reefs':
        schedule = report['scripted_input_schedule']
        save(inputs, schedule)
        args = ['--frames', '30000', '--capture-at', '4000', '16000', '28000', '28400',
                '28800', '29200', '30000', '--dump-capture-ram']
        return reference, report, inputs, args, None, None
    inputs.write_bytes((FOCUSED / 'original_input_prefix.json').read_bytes())
    terminal = load(FOCUSED / 'terminal.json')
    assert digest(reference) == terminal['report_sha256']
    commands = output / 'commands.jsonl'
    previous_commands = Path(terminal['commands'])
    assert digest(previous_commands) == terminal['commands_sha256']
    if mode == 'levelup':
        commands.write_bytes(previous_commands.read_bytes())
    else:
        schedule = [json.loads(line) for line in previous_commands.read_text(encoding='utf-8').splitlines()]
        schedule = schedule[:4] + [{'stop': True}]
        schedule[0]['condition_fixture'] = {'mode': 'choose-becalmed'}
        schedule[3]['condition_fixture'] = {'mode': 'restore-becalmed'}
        commands.write_text(''.join(json.dumps(step) + '\n' for step in schedule), encoding='utf-8')
    donor = Path(report['battery_save_preloaded']['source'])
    assert digest(donor) == report['battery_save_preloaded']['source_sha256']
    args = ['--frames', '14000', '--battery-save', str(donor), '--pause-at', str(PAUSE),
            '--allow-condition-fixtures', '--dump-pause-ram']
    return reference, report, inputs, args, commands, donor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('reefs', 'levelup', 'becalmed'))
    mode = parser.parse_args().mode
    proof = load(PROOF)
    assert digest(ROM) == proof['research_ROM_sha256']
    output = ROOT / mode
    output.mkdir()
    reference, prior, inputs, args, commands, donor = inputs_for(mode, output)
    source = HARNESS.read_text(encoding='utf-8')
    if commands:
        token = 'from scripts.native_condition_fixture_v520 import set_condition'
        assert source.count(token) == 1
        source = source.replace(token, 'from scripts.run_sailing_alert_replays_v2 import set_condition')
    args += ['--rom', str(ROM), '--out', str(output / 'capture'), '--inputs-json', str(inputs),
             '--touchscreen', '--capture-every', '999999', '--dump-ram']
    old_input, old_args = sys.stdin, sys.argv
    stream = GrowingCommands(commands) if commands else None
    try:
        if stream:
            sys.stdin = stream
        sys.argv = [str(HARNESS), *args]
        exec(compile(source, str(HARNESS), 'exec'),
             {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    finally:
        sys.stdin, sys.argv = old_input, old_args
        if stream:
            stream.close()
    actual = output / 'capture/capture_report.json'
    report = load(actual)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['core_options'] == prior['core_options']
    if donor:
        assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
        if mode == 'levelup':
            assert digest(commands) == digest(FOCUSED / 'commands.jsonl')
    else:
        assert report['scripted_input_schedule'] == prior['scripted_input_schedule']
        assert not report.get('battery_save_preloaded')
    save(output / 'terminal.json', dict(mode=mode, candidate_sha256=digest(ROM),
        report=str(actual), report_sha256=digest(actual),
        earlier_reference=str(reference), earlier_reference_sha256=digest(reference),
        focused_bubbles_selector=mode == 'levelup', focused_becalmed_selector=mode == 'becalmed',
        original_fixture_donor_unchanged=bool(donor)))


if __name__ == '__main__':
    main()
