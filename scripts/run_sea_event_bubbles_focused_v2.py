"""Test the original five-part bubbles sequence with one disclosed selector input."""

import json
from pathlib import Path
import struct
import sys

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_sea_event_balanced_wrap_v2 import ARM, EVIDENCE, ROM, ROOT


BASE, FIELD = 0x02000000, 0x02030F10
ORIGINAL = struct.pack('<I', 0xE1A00004)
FOCUSED = struct.pack('<I', 0xE3A0000B)
OUT = ROOT / 'focused_bubbles'
ORDINARY = Path('out/sea_events_20261110_v1/ordinary_bubbles')
PAUSE = 8327


def set_condition(arm, raw, request):
    assert arm == NdsImage.open(ROM).read_file(ARM) and len(raw) == 0x400000
    clean = NdsImage.open('work/clean.nds').read_file(ARM)
    lo, hi = 0x30F04, 0x30F20
    assert clean[lo:hi] == arm[lo:hi] and clean[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    assert arm[0x31EC0:0x325CC] == clean[0x31EC0:0x325CC]
    mode = request['mode']
    assert request == {'mode': mode} and mode in ('choose-bubbles', 'restore-selection')
    before, after = (ORIGINAL, FOCUSED) if mode == 'choose-bubbles' else (FOCUSED, ORIGINAL)
    start = FIELD - BASE
    assert raw[start:start + 4] == before
    changes = [dict(address=FIELD + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:start] + after + raw[start + 4:], dict(
        mode=mode, original_dispatcher=0x02031EC0, scoped_input=11, instruction=FIELD,
        before=before.hex(), after=after.hex(), changes=changes,
        only_original_event_argument_forced=True, natural_random_selection_verified=False)


def main():
    staged = load(EVIDENCE)
    assert digest(ROM) == staged['research_ROM_sha256']
    terminal = load(ORDINARY / 'terminal.json')
    prior = load(terminal['report'])
    assert digest(terminal['report']) == terminal['report_sha256']
    donor = Path(prior['battery_save_preloaded']['source'])
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    OUT.mkdir()
    inputs, navigation = OUT / 'original_input_prefix.json', OUT / 'commands.jsonl'
    save(inputs, [row for row in prior['scripted_input_schedule'] if row['start'] < PAUSE])
    first = dict(until=8727, condition_fixture={'mode': 'choose-bubbles'}, buttons=['UP'], duration=400)
    navigation.write_text(json.dumps(first) + '\n', encoding='utf-8')
    harness = Path('scripts/headless_desmume_v193.py')
    source = harness.read_text(encoding='utf-8')
    token = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(token) == 1
    effective = source.replace(token, 'from scripts.run_sea_event_bubbles_focused_v2 import set_condition')
    args = ['--rom', str(ROM), '--out', str(OUT / 'capture'), '--frames', '14000', '--inputs-json', str(inputs),
            '--battery-save', str(donor), '--touchscreen', '--capture-every', '999999',
            '--pause-at', str(PAUSE), '--allow-condition-fixtures', '--dump-pause-ram', '--dump-ram']
    previous = sys.stdin, sys.argv
    stream = GrowingCommands(navigation)
    try:
        sys.stdin, sys.argv = stream, [str(harness), *args]
        exec(compile(effective, str(harness), 'exec'),
             {'__name__': '__main__', '__file__': str(harness.resolve())})
    finally:
        sys.stdin, sys.argv = previous
        stream.close()
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    path = OUT / 'capture/capture_report.json'
    save(OUT / 'terminal.json', dict(report=str(path), report_sha256=digest(path),
        candidate_sha256=digest(ROM), commands=str(navigation), commands_sha256=digest(navigation),
        donor_unchanged=True, original_input_prefix_sha256=digest(inputs)))


if __name__ == '__main__':
    main()
