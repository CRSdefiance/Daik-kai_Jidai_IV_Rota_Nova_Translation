"""Exercise the original Galley and language-refusal assignment paths."""

import argparse
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import struct
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_sea_approach_village_replay_v1 import STARTUP as PARENT
from scripts.stage_sera_assignment_review_v1 import ACTOR, ARM, BASE, FLAGS, PROOF, ROM, ROOT
from scripts.verify_personal_gameplay_v841 import get_machine, rtti


HARNESS = Path('scripts/headless_desmume_v193.py')
REFERENCE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_cabin_v840_838_Charles_after/capture_report.json')
STARTUP = ROOT / 'own_startup'
SLOT = 12
CASES = {'galley': (15, 1, 1357), 'cabin': (12, 1, 1358), 'refusal': (2, 1, 1359), 'language': (15, 0, 1360)}


def set_condition(arm, raw, request):
    mode = request['mode']
    assert request == {'mode': mode} and mode in CASES
    assert arm == NdsImage.open(ROM).read_file(ARM) and len(raw) == 0x400000
    room, language, number = CASES[mode]
    cpu, get = get_machine(arm, raw)
    matches, at = [], raw.find(struct.pack('<I', 0x021314E8))
    while at >= 0:
        parent = at - 0x2194
        if parent >= 0 and struct.unpack_from('<I', raw, parent)[0] == 0x02130EF0:
            matches.append(BASE + parent)
        at = raw.find(struct.pack('<I', 0x021314E8), at + 4)
    owner, = matches
    assert rtti(raw, 0x02130EF0) == '18CDeckPersonnelView'
    actor, previous_room = struct.unpack('<2I', cpu.mem_read(owner + 0x40, 8))
    assert (actor, previous_room) == (18, 9)
    controller = get(0xCB1A8) + 0x2090
    model = get(0x82E04, controller)
    assert get(0x132C0, model, SLOT) == 12
    assert get(0x82BC4, controller, SLOT) == 208
    assert ACTOR not in [get(0x82BC4, controller, n) for n in range(31)]
    obj = get(0xCB184) + 4 + ACTOR * 32
    assert get(0x7EE08, obj) == ACTOR
    assert get(0x7E100, obj) == 0
    get(0x23C8C, FLAGS, 2, language)
    assert get(0x23C60, FLAGS, 2) == language * 4
    eligible = int(language and room in (12, 15))
    assert get(0x15DE4, ACTOR, room) == eligible
    if eligible:
        assert get(0x81FA4, controller, room, ACTOR) == 1
    flags = struct.unpack('<I', cpu.mem_read(FLAGS + 4, 4))[0]
    initial = struct.unpack_from('<I', raw, FLAGS + 4 - BASE)[0]
    assert flags == ((initial & ~4) | (4 if language else 0))
    fields = {model + 0x1E + SLOT: bytes([room]), owner + 0x40: struct.pack('<2I', ACTOR, 32),
        FLAGS + 4: struct.pack('<I', flags)}
    after, changes = bytearray(raw), []
    for address, values in fields.items():
        offset = address - BASE
        changes.extend(dict(address=address + i, before=raw[offset + i], after=value)
            for i, value in enumerate(values) if raw[offset + i] != value)
        after[offset:offset + len(values)] = values
    return bytes(after), dict(mode=mode, selection_owner=owner, controller=controller, actor_object=obj,
        actor_ID=ACTOR, slot=SLOT, room_type=room, language_bit=language, original_eligibility=eligible,
        expected_message_ID=number, changes=changes, selected_actor_room_type_and_language_bit_only=True,
        fixture_earned_recruitment_or_language_learning=False, before_RAM_sha256=sha256(raw).hexdigest(),
        after_RAM_sha256=sha256(after).hexdigest())


def replay(mode):
    assert digest(ROM) == load(PROOF)['research_ROM_sha256']
    prior = load(REFERENCE)
    donor = Path(prior['battery_save_preloaded']['source'])
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    out = ROOT / mode
    out.mkdir()
    inputs = out / 'inputs.json'
    save(inputs, [row for row in prior['scripted_input_schedule'] if row['start'] <= 4400])
    commands = [
        {'until': 4600, 'buttons': ['A'], 'duration': 8, 'condition_fixture': {'mode': mode}},
        {'until': 4800, 'buttons': ['A'], 'duration': 8}, {'stop': True},
    ]
    args = ['--rom', str(ROM), '--out', str(out / 'capture'), '--frames', '4801',
            '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
            '--capture-every', '999999', '--pause-at', '4400', '--allow-condition-fixtures',
            '--dump-pause-ram', '--dump-ram']
    source = HARNESS.read_text(encoding='utf-8')
    token = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(token) == 1
    source = source.replace(token, 'from scripts.run_sera_assignment_replay_v1 import set_condition')
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
        candidate_sha256=digest(ROM), earlier_reference=str(REFERENCE), earlier_reference_sha256=digest(REFERENCE),
        unchanged_donor_sha256=digest(donor), commands=commands))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('galley', 'language', 'startup'))
    mode = parser.parse_args().mode
    if mode == 'startup':
        run = FunctionType(startup.main.__code__, {**startup.main.__globals__, 'EVIDENCE': PROOF,
            'ROM': ROM, 'STARTUP': STARTUP, 'PRIOR': PARENT})
        run()
    else:
        replay(mode)


if __name__ == '__main__':
    main()
