"""Replay forced crew assignment with a valid-length literal ship name."""

import json
import sys
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatcher
from scripts import run_ship_command_empty_crew_v1 as prior
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import ARM, OUT, SHIP_CAP
from scripts.probe_button_prompt_native import BASE
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.verify_personal_gameplay_v841 import get_machine


LIVE = Path('out/shared_crew_notices_live_20261110_v2')
PREFLIGHT = OUT / 'native_preflight.json'
NAME = b'FIFOFOFUABCDEFGHIJ'


def fixture(arm, raw, action):
    staged = load(PREFLIGHT)
    assert arm == NdsImage.open(staged['research_ROM']).read_file(ARM)
    target_sha = sha256(arm).hexdigest()
    inherited = FunctionType(prior.fixture.__code__, {**prior.fixture.__globals__, 'ARM_SHA': target_sha})
    crew_only, proof = inherited(arm, raw, action)
    assert len(NAME) == load(SHIP_CAP)['max_name_bytes_excluding_NUL'] == 18
    cpu, get = get_machine(arm, crew_only)
    ship = get(0x36C70, proof['fleet'] + 12 + 8 * proof['ship_slot'])
    model, model_root = get(0xAB158, ship), get(0xCB148)
    index, remainder = divmod(model - model_root - 4, 0x8C)
    assert 0 <= index < 50 and remainder == 0
    vtable = int.from_bytes(cpu.mem_read(ship, 4), 'little')
    getter = int.from_bytes(cpu.mem_read(vtable + 4, 4), 'little')
    field = get(getter - BASE, ship)
    assert field == model + 8 and bytes(cpu.mem_read(field, 19)).split(b'\0')[0] == b'Latina'
    assert bytes(cpu.mem_read(field + 19, 4)) == crew_only[field - BASE + 19:field - BASE + 23]
    before = crew_only[field - BASE:field - BASE + 19]
    result = crew_only[:field - BASE] + NAME + b'\0' + crew_only[field - BASE + 19:]
    cpu.mem_write(field, NAME + b'\0')
    assert get(getter - BASE, ship) == field and bytes(cpu.mem_read(field, 19)) == NAME + b'\0'
    changes = [dict(address=field + i, before=a, after=b)
        for i, (a, b) in enumerate(zip(before, NAME + b'\0', strict=True)) if a != b]
    return result, {**proof, 'changes': proof['changes'] + changes,
        'ship_name': NAME.decode('ascii'), 'ship_name_before': 'Latina', 'ship_name_field': field,
        'ship_model_index': index, 'native_name_getter': getter, 'declared_name_field_bytes': 19,
        'after_sha256': sha256(result).hexdigest(), 'both_fixture_fields_only': True,
        'verified_only_original_mobile_crew_field_changed': False}


def main():
    assert not LIVE.exists() and LIVE.resolve().drive.upper() == 'E:'
    staged = load(PREFLIGHT)
    rom = Path(staged['research_ROM'])
    assert digest(rom) == staged['research_ROM_sha256']
    earlier = load(prior.OUT / 'terminal.json')
    schedule = prior.OUT / 'navigation_inputs.jsonl'
    assert digest(schedule) == earlier['journal_sha256']
    commands = [json.loads(row) for row in schedule.read_text(encoding='utf-8').splitlines()]
    assert commands[-1] == {'stop': True}
    for row in commands:
        if row.get('export_native_state'):
            del row['export_native_state']
    commands[-2]['export_native_state'] = True
    source = load(prior.PRIOR / 'run_plan.json')
    donor, inputs = Path(source['donor']), Path(source['initial_input_schedule'])
    assert digest(donor) == source['donor_sha256'] and digest(inputs) == source['initial_input_schedule_sha256']
    LIVE.mkdir()
    journal = LIVE / 'navigation.jsonl'
    journal.write_text(''.join(json.dumps(row) + '\n' for row in commands), encoding='utf-8')
    args = ['--rom', str(rom), '--out', str(LIVE / 'capture'), '--frames', '9000',
        '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
        '--capture-every', '999999', '--pause-at', '4800', '--allow-battle-fixtures',
        '--dump-pause-ram', '--dump-ram']
    save(LIVE / 'run_plan.json', dict(candidate_sha256=digest(rom), donor_sha256=digest(donor),
        original_input_sha256=digest(inputs), commands=commands, args=args, runner_sha256=digest(__file__)))
    stream = GrowingCommands(journal)
    original = sys.stdin, sys.argv, dispatcher.apply_fixture
    try:
        sys.stdin, sys.argv, dispatcher.apply_fixture = stream, [sys.argv[0], *args], fixture
        harness.main()
    finally:
        sys.stdin, sys.argv, dispatcher.apply_fixture = original
        stream.close()
    assert digest(donor) == source['donor_sha256']
    report = LIVE / 'capture/capture_report.json'
    save(LIVE / 'terminal.json', dict(exit_code=0, report=str(report), report_sha256=digest(report),
        journal_sha256=digest(journal), donor_unchanged=True))


if __name__ == '__main__':
    main()
