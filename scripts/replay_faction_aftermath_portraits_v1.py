"""Exercise the original faction dissolution in an isolated sailing session."""

import argparse
from io import StringIO
import json
from pathlib import Path
import struct
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as conditions
from scripts import replay_shark_encounter_v1 as sailing
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_diplomatic_letter_portraits_v2 as predecessor
from scripts import stage_faction_aftermath_portraits_v2 as stage
from scripts.checkpoint_sailing_alert_review_v1 import branch_target
from scripts.review_faction_aftermath_portraits_v1 import SPANS


BASE, ARM, CLEAN = sailing.BASE, sailing.ARM, sailing.CLEAN
ENTRY, RETURN, RESUME, HANDLER = 0x30E54, 0x30E5C, 0x30F88, 0x3A3DC
STOP = ENTRY + 16
OUT, FINAL = stage.ROOT / 'dissolution', 11227
FACTION = 10


def fixture_controller(rom):
    arm, clean = (NdsImage.open(path).read_file(ARM) for path in (rom, CLEAN))
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in (*SPANS, (ENTRY, STOP), (0x30F88, 0x30F98)))
    assert branch_target(clean, 0x3A490) == BASE + 0x2C780
    assert branch_target(clean, 0x2B1D8) == BASE + HANDLER
    original = clean[ENTRY:STOP]
    patched = None

    def set_condition(current, raw, request):
        nonlocal patched
        assert current == arm and len(raw) == 0x400000
        cpu, get = sailing.get_machine(arm, raw)
        assert get(0x7F244) == 1
        companies = get(0xCB160)
        assert get(0x397D8, companies) == 2
        target = companies + 4 + FACTION * 76
        assert get(0x3D030, target) == FACTION and not get(0x3CFC8, target)
        mode = request['mode']
        assert request == {'mode': mode}
        if mode == 'request-dissolution':
            assert patched is None and raw[ENTRY:STOP] == original
            assert get(0x3CD78, target) == 34 and cpu.mem_read(target + 9, 1)[0] == 1
            fleets = get(0xCB1A8)
            for index, actor_id in ((10, 34), (27, 51)):
                fleet = fleets + 4 + 132 * index
                assert get(0x35320, fleet) == FACTION and not cpu.mem_read(fleet + 0x50, 1)[0] & 1
                actor = get(0x3697C, fleet)
                assert get(0x7EE08, actor) == actor_id
            # Literal load supplies the initialized faction object. After the native
            # handler returns, continue at the original random-event bypass.
            patched = (struct.pack('<I', 0xE59F0004) + sailing.branch(ENTRY + 4, HANDLER, True)
                       + sailing.branch(RETURN, RESUME, False) + struct.pack('<I', target))
            before, after = original, patched
        elif mode == 'restore-entry':
            assert patched is not None
            before, after = patched, original[:8] + patched[8:]
        else:
            assert mode == 'restore-return' and patched is not None
            before, after = original[:8] + patched[8:], original
            assert cpu.mem_read(target + 0x0B, 1)[0] == 0x73
        assert raw[ENTRY:STOP] == before
        assert bytes(cpu.mem_read(BASE, len(raw))) == raw
        changes = [dict(address=BASE + ENTRY + i, before=a, after=b)
                   for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
        return raw[:ENTRY] + after + raw[STOP:], dict(mode=mode, faction=FACTION,
            faction_object=target, only_temporary_sailing_instructions_changed=True,
            original_dissolution=BASE + HANDLER, original_sailing_resume=BASE + RESUME,
            clean_window_hex=original.hex(), changes=changes, natural_defeat=False)
    return set_condition


def commands():
    return [
        dict(until=8727, condition_fixture={'mode': 'request-dissolution'}, buttons=['UP'], duration=400),
        dict(until=8927, buttons=['UP', 'LEFT'], duration=200),
        dict(until=9627, buttons=['UP'], duration=700),
        dict(until=9827, condition_fixture={'mode': 'restore-entry'}, buttons=['A'], duration=8),
        *[dict(until=frame, buttons=['A'], duration=8) for frame in (10027, 10227, 10427, 10627)],
        dict(until=FINAL, condition_fixture={'mode': 'restore-return'}),
        dict(stop=True),
    ]


def replay():
    proof = sailing.load(stage.PROOF)
    assert sailing.digest(stage.ROM) == proof['research_ROM_sha256']
    terminal = sailing.load(sailing.MUTINY / 'terminal.json')
    assert sailing.digest(terminal['report']) == terminal['report_sha256']
    reference = sailing.load(terminal['report'])
    donor = reference['battery_save_preloaded']
    assert sailing.digest(donor['source']) == donor['source_sha256']
    OUT.mkdir()
    inputs = OUT / 'inputs.json'
    inputs.write_bytes((sailing.MUTINY / 'inputs.json').read_bytes())
    schedule = commands()
    plan = OUT / 'commands.json'
    sailing.save(plan, schedule)
    args = [sys.argv[0], '--rom', str(stage.ROM), '--out', str(OUT / 'capture'), '--frames', str(FINAL + 1),
            '--inputs-json', str(inputs), '--battery-save', donor['source'], '--touchscreen',
            '--capture-every', '999999', '--pause-at', str(sailing.PAUSE),
            '--allow-condition-fixtures', '--dump-pause-ram', '--dump-ram']
    original = conditions.set_condition, sys.stdin, sys.argv
    with StringIO(''.join(json.dumps(row) + '\n' for row in schedule)) as stream:
        try:
            conditions.set_condition, sys.stdin, sys.argv = fixture_controller(stage.ROM), stream, args
            harness.main()
        finally:
            conditions.set_condition, sys.stdin, sys.argv = original
    path = OUT / 'capture/capture_report.json'
    report = sailing.load(path)
    assert report['core_options'] == reference['core_options'] and report['ROM_sha256'] == proof['research_ROM_sha256']
    assert sailing.digest(donor['source']) == donor['source_sha256']
    assert [row['mode'] for row in report['synthetic_condition_fixtures']] == [
        'request-dissolution', 'restore-entry', 'restore-return']
    sailing.save(OUT / 'terminal.json', dict(report=str(path), report_sha256=sailing.digest(path),
        candidate_sha256=proof['research_ROM_sha256'], donor_sha256=donor['source_sha256'],
        commands_sha256=sailing.digest(plan), natural_defeat=False))


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=stage.ROOT / 'own_startup',
                               PRIOR=predecessor.ROOT / 'own_startup')
    FunctionType(startup.main.__code__, env)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('dissolution', 'startup'))
    (cold_boot if parser.parse_args().action == 'startup' else replay)()

