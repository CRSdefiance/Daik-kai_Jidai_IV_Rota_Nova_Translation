"""Use the original mutiny encounter and choices with one temporary branch selection."""

import json
from pathlib import Path
import struct
import sys

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import branch_target
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.run_sea_event_bubbles_focused_v2 import OUT as DONOR, PAUSE
from scripts.seal_shared_text_source_v1 import CLEAN
from scripts.stage_mutiny_review_v1 import ARM, BASE, PROOF, ROM, ROOT


OUT = ROOT / 'focused_mutiny'
FIELD = 0x02030F0C
ORIGINAL, FOCUSED = (struct.pack('<I', word) for word in (0xE28D1030, 0xEA00000F))
HARNESS = Path('scripts/headless_desmume_v193.py')


def set_condition(arm, raw, request):
    assert arm == NdsImage.open(ROM).read_file(ARM) and len(raw) == 0x400000
    clean = NdsImage.open(CLEAN).read_file(ARM)
    assert arm[0x30F04:0x30F64] == clean[0x30F04:0x30F64]
    assert arm[0x3160C:0x31B50] == clean[0x3160C:0x31B50]
    assert branch_target(clean, 0x30F58) == 0x0203160C
    assert clean[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    assert FIELD + 8 + ((struct.unpack('<I', FOCUSED)[0] & 0xFFFFFF) << 2) == 0x02030F50
    mode = request['mode']
    assert request == {'mode': mode} and mode in ('select-mutiny', 'restore-mutiny-selection')
    before, after = (ORIGINAL, FOCUSED) if mode == 'select-mutiny' else (FOCUSED, ORIGINAL)
    start = FIELD - BASE
    assert raw[start:start + 4] == before
    changes = [dict(address=FIELD + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:start] + after + raw[start + 4:], dict(mode=mode, instruction=FIELD,
        before=before.hex(), after=after.hex(), changes=changes, original_mutiny_caller=0x02030F50,
        only_native_encounter_selection_forced=True, natural_mutiny_prerequisite_not_exercised=True)


def main():
    assert digest(ROM) == load(PROOF)['research_ROM_sha256']
    terminal = load(DONOR / 'terminal.json')
    report_path = Path(terminal['report'])
    assert digest(report_path) == terminal['report_sha256']
    reference = load(report_path)
    donor = Path(reference['battery_save_preloaded']['source'])
    assert digest(donor) == reference['battery_save_preloaded']['source_sha256']
    OUT.mkdir()
    inputs, commands = OUT / 'inputs.json', OUT / 'commands.jsonl'
    inputs.write_bytes((DONOR / 'original_input_prefix.json').read_bytes())
    schedule = [
        dict(until=8727, condition_fixture={'mode': 'select-mutiny'}, buttons=['UP'], duration=400),
        dict(until=8927, buttons=['UP', 'LEFT'], duration=200),
        dict(until=9627, buttons=['UP'], duration=700),
        dict(until=9827, condition_fixture={'mode': 'restore-mutiny-selection'}, buttons=['A'], duration=8),
        dict(until=10027, buttons=['A'], duration=8),
        dict(until=10127, buttons=['DOWN'], duration=8),
        *[dict(until=frame, buttons=['A'], duration=8) for frame in range(10327, 11728, 200)],
        dict(stop=True),
    ]
    commands.write_text(''.join(json.dumps(row) + '\n' for row in schedule), encoding='utf-8')
    source = HARNESS.read_text(encoding='utf-8')
    token = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(token) == 1
    effective = source.replace(token, 'from scripts.run_mutiny_replay_v1 import set_condition')
    args = ['--rom', str(ROM), '--out', str(OUT / 'capture'), '--frames', '14000', '--inputs-json', str(inputs),
            '--battery-save', str(donor), '--touchscreen', '--capture-every', '999999',
            '--pause-at', str(PAUSE), '--allow-condition-fixtures', '--dump-pause-ram', '--dump-ram']
    old_input, old_args = sys.stdin, sys.argv
    stream = GrowingCommands(commands)
    try:
        sys.stdin, sys.argv = stream, [str(HARNESS), *args]
        exec(compile(effective, str(HARNESS), 'exec'),
             {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
    finally:
        sys.stdin, sys.argv = old_input, old_args
        stream.close()
    path = OUT / 'capture/capture_report.json'
    report = load(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['core_options'] == reference['core_options']
    assert digest(donor) == reference['battery_save_preloaded']['source_sha256']
    save(OUT / 'terminal.json', dict(report=str(path), report_sha256=digest(path),
        candidate_sha256=digest(ROM), commands=str(commands), commands_sha256=digest(commands),
        donor_unchanged=True, input_prefix_sha256=digest(inputs)))


if __name__ == '__main__':
    main()
