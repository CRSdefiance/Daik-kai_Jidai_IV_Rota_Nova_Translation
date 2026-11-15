"""Exercise the original leak report and the supply depletion following mutiny."""

import argparse
import json
from pathlib import Path
import struct
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import branch_target, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.run_mutiny_replay_v1 import OUT as DONOR, set_condition as mutiny_selection
from scripts.run_sea_event_bubbles_focused_v2 import PAUSE
from scripts.seal_shared_text_source_v1 import CLEAN
from scripts.stage_ship_emergency_balanced_v2 import PROOF, ROM, ROOT
from scripts.stage_ship_emergency_review_v1 import ARM, BASE


FIELD = 0x02030F10
ORIGINAL, FOCUSED = (struct.pack('<I', value) for value in (0xE1A00004, 0xE3A00010))
HARNESS = Path('scripts/headless_desmume_v193.py')


def set_condition(arm, raw, request):
    mode = request['mode']
    if mode in ('select-mutiny', 'restore-mutiny-selection'):
        existing = FunctionType(mutiny_selection.__code__, {**mutiny_selection.__globals__, 'ROM': ROM})
        return existing(arm, raw, request)
    assert request == {'mode': mode} and mode in ('select-leak', 'restore-leak-selection')
    assert arm == NdsImage.open(ROM).read_file(ARM) and len(raw) == 0x400000
    clean = NdsImage.open(CLEAN).read_file(ARM)
    assert arm[0x30F04:0x30F64] == clean[0x30F04:0x30F64]
    assert arm[0x314B4:0x3160C] == clean[0x314B4:0x3160C]
    assert branch_target(clean, 0x30F14) == 0x02031EC0 and branch_target(clean, 0x30F60) == 0x020314B4
    assert word(clean, 0x31F68) == 0xEA000161 and word(clean, 0x324F4) == 0xE3A00016
    start = FIELD - BASE
    assert clean[start:start + 4] == ORIGINAL
    before, after = (ORIGINAL, FOCUSED) if mode == 'select-leak' else (FOCUSED, ORIGINAL)
    assert raw[start:start + 4] == before
    changes = [dict(address=FIELD + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:start] + after + raw[start + 4:], dict(mode=mode, instruction=FIELD, before=before.hex(),
        after=after.hex(), changes=changes, original_dispatcher=0x02031EC0,
        only_original_event_argument_forced=True, original_leak_selection_and_effects=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('leak', 'supplies'))
    mode = parser.parse_args().mode
    assert digest(ROM) == load(PROOF)['research_ROM_sha256']
    terminal = load(DONOR / 'terminal.json')
    report_path = Path(terminal['report'])
    assert digest(report_path) == terminal['report_sha256']
    prior = load(report_path)
    donor = Path(prior['battery_save_preloaded']['source'])
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    out = ROOT / mode
    out.mkdir()
    inputs, commands = out / 'inputs.json', out / 'commands.jsonl'
    inputs.write_bytes((DONOR / 'inputs.json').read_bytes())
    assert digest(inputs) == terminal['input_prefix_sha256']
    original_commands = Path(terminal['commands'])
    assert digest(original_commands) == terminal['commands_sha256']
    schedule = [json.loads(line) for line in original_commands.read_text(encoding='utf-8').splitlines()]
    if mode == 'leak':
        schedule = schedule[:4] + [{'stop': True}]
        schedule[0]['condition_fixture'] = {'mode': 'select-leak'}
        schedule[3]['condition_fixture'] = {'mode': 'restore-leak-selection'}
    commands.write_text(''.join(json.dumps(row) + '\n' for row in schedule), encoding='utf-8')
    source = HARNESS.read_text(encoding='utf-8')
    token = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(token) == 1
    source = source.replace(token, 'from scripts.run_ship_emergency_replays_v1 import set_condition')
    args = ['--rom', str(ROM), '--out', str(out / 'capture'), '--frames', '14000', '--inputs-json', str(inputs),
            '--battery-save', str(donor), '--touchscreen', '--capture-every', '999999',
            '--pause-at', str(PAUSE), '--allow-condition-fixtures', '--dump-pause-ram', '--dump-ram']
    old_input, old_args = sys.stdin, sys.argv
    stream = GrowingCommands(commands)
    try:
        sys.stdin, sys.argv = stream, [str(HARNESS), *args]
        exec(compile(source, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    finally:
        sys.stdin, sys.argv = old_input, old_args
        stream.close()
    report = out / 'capture/capture_report.json'
    assert load(report)['core_options'] == prior['core_options']
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    save(out / 'terminal.json', dict(mode=mode, report=str(report), report_sha256=digest(report),
        candidate_sha256=digest(ROM), commands=str(commands), commands_sha256=digest(commands),
        donor_unchanged=True, earlier_reference=str(report_path), earlier_reference_sha256=digest(report_path)))


if __name__ == '__main__':
    main()
