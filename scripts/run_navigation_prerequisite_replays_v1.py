"""Replay the natural Ceuta warning and the focused Captain's Cabin warning."""

import argparse
from io import StringIO
import json
from pathlib import Path
import struct
import sys

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_navigation_prerequisite_review_v1 import ARM, BASE, CLEAN, branch_target
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.stage_navigation_prerequisite_balanced_v2 import PROOF, ROM, ROOT


HARNESS = Path('scripts/headless_desmume_v193.py')
FIELD = 0x020996BC
ORIGINAL, FOCUSED = (struct.pack('<I', value) for value in (0xE3500000, 0xE1500000))


def set_condition(arm, raw, request):
    mode = request['mode']
    assert request == {'mode': mode} and mode in ('require-cabin', 'restore-cabin')
    assert arm == NdsImage.open(ROM).read_file(ARM) and len(raw) == 0x400000
    clean = NdsImage.open(CLEAN).read_file(ARM)
    start = FIELD - BASE
    assert arm[0x9963C:0x99740] == clean[0x9963C:0x99740]
    assert arm[start:start + 4] == ORIGINAL and branch_target(arm, 0x996B8) == 0x020829C8
    before, after = (ORIGINAL, FOCUSED) if mode == 'require-cabin' else (FOCUSED, ORIGINAL)
    assert raw[start:start + 4] == before
    changes = [dict(address=FIELD + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:start] + after + raw[start + 4:], dict(mode=mode, instruction=FIELD,
        before=before.hex(), after=after.hex(), changes=changes,
        purpose_5_test_only=True, original_warning_selection_and_return=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('ceuta', 'cabin'))
    mode = parser.parse_args().mode
    assert digest(ROM) == load(PROOF)['research_ROM_sha256']
    donor_run = 'ordinary_voyage_v315' if mode == 'ceuta' else 'auto_move_riga_v399'
    earlier = Path('work/emulation_v193') / donor_run / 'capture_report.json'
    prior = load(earlier)
    donor = Path(prior['battery_save_preloaded']['source'])
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    assert prior['cold_boot'] and not prior['savestate_loaded']
    frames = 7200 if mode == 'ceuta' else 7800
    at = (5600, 6000, 6400, 6800, 7200) if mode == 'ceuta' else (6800, 7200, 7500, 7800)
    initial_end = frames if mode == 'ceuta' else 7200
    out = ROOT / mode
    out.mkdir()
    inputs = out / 'inputs.json'
    save(inputs, [row for row in prior['scripted_input_schedule'] if row['start'] <= initial_end])
    args = ['--rom', str(ROM), '--out', str(out / 'capture'), '--frames', str(frames),
            '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
            '--capture-every', '999999', '--dump-capture-ram', '--dump-ram',
            '--capture-at', *map(str, at)]
    source = HARNESS.read_text(encoding='utf-8')
    commands = []
    if mode == 'cabin':
        args += ['--pause-at', '7200', '--allow-condition-fixtures', '--dump-pause-ram']
        commands = [
            {'until': 7500, 'buttons': ['A'], 'duration': 8, 'condition_fixture': {'mode': 'require-cabin'}},
            {'until': 7800, 'buttons': ['A'], 'duration': 8, 'condition_fixture': {'mode': 'restore-cabin'}},
            {'stop': True},
        ]
        token = 'from scripts.native_condition_fixture_v520 import set_condition'
        assert source.count(token) == 1
        source = source.replace(token, 'from scripts.run_navigation_prerequisite_replays_v1 import set_condition')
    old_input, old_args = sys.stdin, sys.argv
    with StringIO(''.join(json.dumps(row) + '\n' for row in commands)) as stream:
        try:
            sys.stdin, sys.argv = stream, [str(HARNESS), *args]
            exec(compile(source, str(HARNESS), 'exec'), {'__name__': '__main__', '__file__': str(HARNESS.resolve())})
        finally:
            sys.stdin, sys.argv = old_input, old_args
    report = out / 'capture/capture_report.json'
    assert load(report)['core_options'] == prior['core_options']
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    save(out / 'terminal.json', dict(mode=mode, report=str(report), report_sha256=digest(report),
        candidate_sha256=digest(ROM), earlier_reference=str(earlier), earlier_reference_sha256=digest(earlier),
        donor_sha256=digest(donor), initial_inputs_sha256=digest(inputs), source_sha256=digest(__file__),
        focused_commands=commands))


if __name__ == '__main__':
    main()
