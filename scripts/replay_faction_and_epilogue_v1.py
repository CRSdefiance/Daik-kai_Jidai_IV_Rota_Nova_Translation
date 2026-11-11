"""Replay the original four-panel epilogue with an isolated ending-state fixture."""

import argparse
from io import StringIO
import json
from pathlib import Path
import struct
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_ending_fixture_v537 as ending
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_faction_and_epilogue_v2 as stage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_discovery_rewards_v1 import RELEASE
from scripts.review_faction_and_epilogue_v1 import CLEAN, ARM
from scripts.stage_discovery_rewards_v1 import ROOT as PRIOR
from scripts.verify_personal_gameplay_v841 import get_machine


INPUT = PRIOR / 'auto/capture/capture_report.json'
BASELINE = Path('out/faction_and_epilogue_baseline_20261111_v1')
PAUSE, FINAL = 8000, 9600
HOLDS = (8200, 8440, 8680, 8920, 9160, 9360, FINAL)
PRESSES = (8321, 8561, 8801, 9041)
MANAGER = 0x02279668
STATE = MANAGER + 0x54 - ending.BASE
SUBSTATE = MANAGER + 0x5C - ending.BASE


def request_epilogue(arm, raw, captain):
    clean = NdsImage.open(CLEAN).read_file(ARM)
    for start, stop in ((0x3E140, 0x3E344), (0x7F244, 0x7F254), (0x5D44, 0x5D48)):
        assert arm[start:stop] == clean[start:stop]
    assert struct.unpack_from('<I', arm, 0x7F250) == (MANAGER,)
    assert struct.unpack_from('<I', arm, 0x5D44) == (MANAGER,)
    assert len(raw) == 0x400000
    assert struct.unpack_from('<I', raw, STATE) == (1,)
    assert struct.unpack_from('<I', raw, SUBSTATE) == (0,)
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == captain == 1
    assert bytes(cpu.mem_read(ending.BASE, len(raw))) == raw
    after = bytearray(raw)
    struct.pack_into('<I', after, STATE, 3)
    struct.pack_into('<I', after, SUBSTATE, 1)
    changes = [dict(address=ending.BASE + offset, before=raw[offset], after=after[offset])
               for offset in (STATE, SUBSTATE)]
    assert sum(old != new for old, new in zip(raw, after, strict=True)) == len(changes) == 2
    return bytes(after), dict(synthetic_ending_fixture=True, earned_completion_verified=False,
        actual_captain=captain, state_manager=MANAGER, requested_state=3, requested_substate=1,
        changes=changes, only_two_state_bytes_changed=True, original_epilogue_entry=0x0203E208)


def replay(staged):
    proof, parent, prior = map(load, (stage.PROOF, RELEASE, INPUT))
    rom, out, sha = ((stage.ROM, stage.ROOT / 'epilogue', proof['research_ROM_sha256']) if staged else
                     (Path(parent['candidate']), BASELINE / 'epilogue', parent['candidate_sha256']))
    assert digest(rom) == sha
    assert prior['ROM_sha256'] == parent['candidate_sha256'] and prior['cold_boot'] and not prior['savestate_loaded']
    assert not any(value for key, value in prior.items() if key.startswith('synthetic_'))
    donor = prior['battery_save_preloaded']
    assert digest(donor['source']) == donor['source_sha256']
    inputs = prior['scripted_input_schedule'] + [dict(start=frame, duration=8, buttons=['A']) for frame in PRESSES]
    out.mkdir(parents=True)
    save(out / 'inputs.json', inputs)
    commands = [dict(until=FINAL, ending_captain=1), dict(stop=True)]
    args = [sys.argv[0], '--rom', str(rom), '--out', str(out / 'capture'), '--frames', str(FINAL + 1),
            '--inputs-json', str(out / 'inputs.json'), '--battery-save', donor['source'], '--touchscreen',
            '--capture-every', '999999', '--capture-at', *map(str, HOLDS), '--dump-capture-ram',
            '--pause-at', str(PAUSE), '--dump-pause-ram', '--allow-ending-fixtures', '--dump-ram']
    saved_request, saved_stdin, saved_args = ending.request_ending, sys.stdin, sys.argv
    with StringIO(''.join(json.dumps(row) + '\n' for row in commands)) as stream:
        try:
            ending.request_ending, sys.stdin, sys.argv = request_epilogue, stream, args
            harness.main()
        finally:
            ending.request_ending, sys.stdin, sys.argv = saved_request, saved_stdin, saved_args
    report = out / 'capture/capture_report.json'
    result = load(report)
    assert result['ROM_sha256'] == sha and result['core_options'] == prior['core_options']
    assert digest(donor['source']) == donor['source_sha256']
    assert result['synthetic_ending_fixtures'][0]['only_two_state_bytes_changed']
    save(out / 'terminal.json', dict(report=str(report), report_sha256=digest(report), candidate_sha256=sha,
        prior_capture=str(INPUT), prior_capture_sha256=digest(INPUT), unchanged_donor_sha256=donor['source_sha256'],
        fixture_type='Original epilogue state and substate initialized after ordinary gameplay',
        earned_ending=False, commands=commands))


def replay_startup():
    env = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=stage.ROOT / 'own_startup',
                               PRIOR=PRIOR / 'own_startup')
    FunctionType(startup.main.__code__, env)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('baseline', 'staged', 'startup'))
    phase = parser.parse_args().phase
    if phase == 'startup':
        replay_startup()
    else:
        replay(phase == 'staged')
