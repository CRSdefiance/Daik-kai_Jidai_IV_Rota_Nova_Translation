"""Replay both original shark choices after scoped encounter initialization."""

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
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_shark_encounter_v1 as stage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_shark_encounter_v1 import ARM, BASE, CLEAN, START, STOP
from scripts.run_mutiny_replay_v1 import OUT as MUTINY, PAUSE
from scripts.stage_faction_and_epilogue_v2 import ROOT as PRIOR
from scripts.verify_personal_gameplay_v841 import get_machine


ENTRY, CONTINUE = 0x30F0C, 0x30F10
NEXT_TICK = 0x30F88
COMMON_HOLDS = tuple(range(9627, 12028, 200))
MENU, MENU_CONFIRM, FINAL = 12227, 12427, 13827


def branch(at, target, link):
    offset = (target - at - 8) // 4
    assert (target - at - 8) % 4 == 0 and -(1 << 23) <= offset < 1 << 23
    return struct.pack('<I', (0xEB000000 if link else 0xEA000000) | (offset & 0xFFFFFF))


def fixture_controller(rom):
    arm = NdsImage.open(rom).read_file(ARM)
    clean = NdsImage.open(CLEAN).read_file(ARM)
    assert clean[START:STOP] == arm[START:STOP]
    for lo, hi in ((0x30F04, 0x30F64), (0x7DB14, 0x7DBF4), (0x7E958, 0x7E960), (0x4A368, 0x4A394)):
        assert clean[lo:hi] == arm[lo:hi]
    entry, continuation = arm[ENTRY:ENTRY + 4], arm[CONTINUE:CONTINUE + 4]
    call, skip = branch(ENTRY, START, True), branch(CONTINUE, NEXT_TICK, False)
    saved_membership = {}

    def set_condition(current, raw, request):
        assert current == arm and len(raw) == 0x400000
        mode = request['mode']
        assert request == {'mode': mode}
        cpu, get = get_machine(arm, raw)
        assert get(0x7F244) == 1
        actor_root, company_root = get(0xCB184), get(0xCB160)
        faction = get(0x397D8, company_root)
        actors = {n: actor_root + 4 + n * 32 for n in (17, 22)}
        locations = {actor + 5 - BASE: n for n, actor in actors.items()}
        item = get(0xCB190) + 4 + 4 * 20
        after = bytearray(raw)
        if mode == 'initialize':
            assert not saved_membership and raw[ENTRY:CONTINUE + 4] == entry + continuation
            assert get(0x4A368, item) == 0
            saved_membership.update({address: raw[address] for address in locations})
            for at in saved_membership:
                after[at] = faction
            after[ENTRY:CONTINUE + 4] = call + skip
            staged_cpu, staged_get = get_machine(arm, bytes(after))
            assert all(staged_get(0x7DB14, actor) == 1 for actor in actors.values())
            assert staged_get(0x4A368, item) == 0
            assert bytes(staged_cpu.mem_read(BASE, len(raw))) == bytes(after)
            owned = {*range(ENTRY, CONTINUE + 4), *saved_membership}
        elif mode == 'restore-entry':
            assert raw[ENTRY:CONTINUE + 4] == call + skip
            after[ENTRY:ENTRY + 4] = entry
            owned = set(range(ENTRY, ENTRY + 4))
        else:
            assert mode == 'restore-return-and-roster' and raw[ENTRY:CONTINUE + 4] == entry + skip
            assert saved_membership.keys() == locations.keys()
            assert all(raw[address] == faction for address in saved_membership)
            for at, original in saved_membership.items():
                after[at] = original
            after[CONTINUE:CONTINUE + 4] = continuation
            owned = {*range(CONTINUE, CONTINUE + 4), *saved_membership}
        changes = [dict(address=BASE + offset, before=raw[offset], after=after[offset])
                   for offset in sorted(owned) if raw[offset] != after[offset]]
        assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(changes)
        assert bytes(cpu.mem_read(BASE, len(raw))) == raw
        return bytes(after), dict(mode=mode, original_captain=1, original_shark_entry=BASE + START,
            resume_target=BASE + NEXT_TICK, actor_membership_fields={n: BASE + at for at, n in locations.items()},
            state_isolated=True, changes=changes, natural_shark_battle=False)

    return set_condition


def commands(choice):
    result = [
        dict(until=8727, condition_fixture={'mode': 'initialize'}, buttons=['UP'], duration=400),
        dict(until=8927, buttons=['UP', 'LEFT'], duration=200),
        dict(until=9627, buttons=['UP'], duration=700),
    ]
    for frame in (*COMMON_HOLDS[1:], MENU):
        command = dict(until=frame, buttons=['A'], duration=8)
        if frame == COMMON_HOLDS[1]:
            command['condition_fixture'] = {'mode': 'restore-entry'}
        result.append(command)
    selection = dict(until=MENU_CONFIRM)
    if choice == 'raise':
        selection.update(buttons=['UP'], duration=8)
    result.append(selection)
    last = 13627 if choice == 'raise' else 13027
    result.extend(dict(until=frame, buttons=['A'], duration=8) for frame in range(12627, last + 1, 200))
    result.extend((dict(until=FINAL, condition_fixture={'mode': 'restore-return-and-roster'}), dict(stop=True)))
    return result


def replay(choice):
    proof = load(stage.PROOF)
    assert digest(stage.ROM) == proof['research_ROM_sha256']
    terminal = load(MUTINY / 'terminal.json')
    assert digest(terminal['report']) == terminal['report_sha256']
    reference = load(terminal['report'])
    donor = reference['battery_save_preloaded']
    assert digest(donor['source']) == donor['source_sha256']
    out = stage.ROOT / choice
    out.mkdir()
    inputs = out / 'inputs.json'
    inputs.write_bytes((MUTINY / 'inputs.json').read_bytes())
    schedule = commands(choice)
    command_path = out / 'commands.json'
    save(command_path, schedule)
    args = [sys.argv[0], '--rom', str(stage.ROM), '--out', str(out / 'capture'), '--frames', str(FINAL + 1),
            '--inputs-json', str(inputs), '--battery-save', donor['source'], '--touchscreen',
            '--capture-every', '999999', '--pause-at', str(PAUSE), '--allow-condition-fixtures',
            '--dump-pause-ram', '--dump-ram']
    old_fixture, old_stdin, old_args = conditions.set_condition, sys.stdin, sys.argv
    with StringIO(''.join(json.dumps(row) + '\n' for row in schedule)) as stream:
        try:
            conditions.set_condition, sys.stdin, sys.argv = fixture_controller(stage.ROM), stream, args
            harness.main()
        finally:
            conditions.set_condition, sys.stdin, sys.argv = old_fixture, old_stdin, old_args
    report = out / 'capture/capture_report.json'
    captured = load(report)
    assert captured['core_options'] == reference['core_options']
    assert digest(donor['source']) == donor['source_sha256']
    assert [row['mode'] for row in captured['synthetic_condition_fixtures']] == [
        'initialize', 'restore-entry', 'restore-return-and-roster']
    save(out / 'terminal.json', dict(report=str(report), report_sha256=digest(report), candidate_sha256=digest(stage.ROM),
        donor_unchanged=True, donor_sha256=donor['source_sha256'], commands_sha256=digest(command_path),
        input_prefix_sha256=digest(inputs), natural_shark_battle=False))


def replay_startup():
    env = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=stage.ROOT / 'own_startup',
                               PRIOR=PRIOR / 'own_startup')
    FunctionType(startup.main.__code__, env)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('raise', 'kill', 'startup'))
    phase = parser.parse_args().phase
    replay_startup() if phase == 'startup' else replay(phase)
