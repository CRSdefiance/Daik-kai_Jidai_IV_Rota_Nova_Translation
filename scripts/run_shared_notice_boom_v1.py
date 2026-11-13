"""Exercise the original economic boom notice with one town accumulator fixture."""

import argparse
import json
import struct
import sys
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatcher
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_shared_notices_storage_v1 import ARM, ROOT
from scripts.verify_personal_gameplay_v841 import get_machine


RESEARCH = ROOT / 'stored_verification.json'
PREFIX = Path('out/shared_notice_departure_research_20261110_v1')
ACTION = 'copenhagen-investment-accumulator'
NOTICE = BASE + 0x546B8
TOWN_INDEX = 9
AMOUNT = 400000


def inspect_town(arm, raw):
    cpu, get = get_machine(arm, raw)
    town = get(0xCB178) + 4 + TOWN_INDEX * 108
    vtable = struct.unpack('<I', cpu.mem_read(town, 4))[0]
    getter, = struct.unpack('<I', cpu.mem_read(vtable + 8, 4))
    name = bytes(cpu.mem_read(get(getter - BASE, town), 64)).split(b'\0')[0]
    assert name == b'Copenhagen'
    return cpu, get, town


def check_native_update(arm, raw):
    cpu, _, town = inspect_town(arm, raw)
    selected = []

    def notice(u, _, size, data):
        pointer = u.reg_read(UC_ARM_REG_R1)
        selected.append(dict(number=u.reg_read(UC_ARM_REG_R0), return_PC=u.reg_read(UC_ARM_REG_LR),
            name=bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii')))
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, notice, begin=NOTICE, end=NOTICE)
    for register, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP), (UC_ARM_REG_R0, town)):
        cpu.reg_write(register, value)
    cpu.emu_start(BASE + 0xB3C08, STOP, count=200000)
    return cpu.reg_read(UC_ARM_REG_PC), selected


def fixture(arm, raw, action):
    assert action == ACTION and len(raw) == 0x400000
    registered = load(RESEARCH)
    assert arm == NdsImage.open(registered['target']).read_file(ARM)
    clean = NdsImage.open('work/clean.nds').read_file(ARM)
    for low, high in ((0xB23FC, 0xB2430), (0xB3C08, 0xB3F34), (0xB3FC8, 0xB3FE0)):
        assert arm[low:high] == clean[low:high] == raw[low:high]
    _, get, town = inspect_town(arm, raw)
    growth, status = get(0xB3FD4, town, 0), get(0xB2E04, town)
    assert (growth, status, get(0xB3FC8, town, 0)) == (3400, 12, 0)
    assert check_native_update(arm, raw) == (STOP, [])
    address = town + 0x1C
    at = address - BASE
    changed = raw[:at] + struct.pack('<I', AMOUNT) + raw[at + 4:]
    calls = [dict(number=126, return_PC=BASE + 0xB3E08, name='Copenhagen')]
    assert check_native_update(arm, changed) == (NOTICE, calls)
    changes = [dict(address=address + n, before=before, after=after)
        for n, (before, after) in enumerate(zip(raw[at:at + 4], changed[at:at + 4], strict=True)) if before != after]
    return changed, dict(action=ACTION, town_index=TOWN_INDEX, town_object=town, existing_growth=growth,
        existing_town_status=status, existing_accumulator=0, test_accumulator=AMOUNT, changes=changes,
        source_spans_equal_clean=True, exact_native_branch_before_emulator_test=calls,
        untouched_mode_company_time_location_and_code=True, earned_investment=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    out = args.output
    assert not out.exists() and out.resolve().drive.upper() == 'E:'
    research = load(RESEARCH)
    rom = Path(research['target'])
    assert digest(rom) == research['target_sha256']
    baseline = load(PREFIX / 'capture/capture_report.json')
    donor = Path(baseline['battery_save_preloaded']['source'])
    assert digest(donor) == baseline['battery_save_preloaded']['source_sha256']
    inputs = PREFIX / 'inputs.json'
    assert load(inputs) == baseline['scripted_input_schedule']
    out.mkdir()
    commands = out / 'navigation.jsonl'
    commands.write_text(json.dumps(dict(until=7500, duration=1, battle_fixture=ACTION)) + '\n', encoding='utf-8')
    cli = ['--rom', str(rom), '--out', str(out / 'capture'), '--frames', '9500',
        '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen', '--pause-at', '5300',
        '--capture-every', '250', '--dump-pause-ram', '--dump-ram', '--allow-battle-fixtures']
    save(out / 'run_plan.json', dict(candidate_sha256=digest(rom), donor_sha256=digest(donor),
        input_sha256=digest(inputs), baseline_report_sha256=digest(PREFIX / 'capture/capture_report.json'),
        argv=cli, runner_sha256=digest(__file__)))
    stream = GrowingCommands(commands)
    original = sys.stdin, sys.argv, dispatcher.apply_fixture
    try:
        sys.stdin, sys.argv, dispatcher.apply_fixture = stream, [sys.argv[0], *cli], fixture
        harness.main()
    finally:
        sys.stdin, sys.argv, dispatcher.apply_fixture = original
        stream.close()
    assert digest(donor) == baseline['battery_save_preloaded']['source_sha256']
    report = out / 'capture/capture_report.json'
    save(out / 'terminal.json', dict(exit_code=0, report=str(report), report_sha256=digest(report),
        navigation_sha256=digest(commands), donor_unchanged=True))


if __name__ == '__main__':
    main()
