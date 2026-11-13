"""Cold-boot the exact staged ROM and isolate one original empty-crew condition."""

import json
import struct
import sys
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, machine
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_ship_command_release_v1 import CANDIDATE, STAGED


OUT = Path('out/ship_command_empty_crew_20261110_v1')
PRIOR = Path('out/ship_command_menu_capture_20261110_v4')
ACTION = 'empty-secondary-crew'
ARM_SHA = 'f9afa693ba4f7abd8ebf59c46585a7522aed52a9cfd07534965bb867b72fdfb0'


def fixture(arm, raw, action):
    from hashlib import sha256

    assert action == ACTION and len(raw) == 0x400000
    assert sha256(arm).hexdigest() == ARM_SHA
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x2C1E0,0x2C620), (0x35048,0x350FC), (0x36C48,0x36C94), (0x55444,0x5544C)]
    assert all(arm[a:b] == clean[a:b] for a,b in spans)
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    assert get(0x2E58C) == 1
    fleet = get(0xCB1A8)+4+0x84
    assert get(0x36914, fleet) == 1
    assert get(0x35094, fleet) == 6
    ships = [get(0x36C70, fleet+12+slot*8) for slot in (0,1)]
    assert all(BASE <= p <= BASE+len(raw)-0x1C for p in ships) and len(set(ships)) == 2
    assert all(bytes(cpu.mem_read(p, 4)) == struct.pack('<I', 0x02143A80) for p in ships)
    crew = [get(0x55444, p) for p in ships]
    assert all(0 < n < 255 for n in crew)
    model = get(0xAB158, ships[1])
    assert BASE <= model <= BASE+len(raw)-140
    name = bytes(cpu.mem_read(model+8, 24)).split(b'\0', 1)[0].decode('cp932')
    assert name == 'Latina'
    address = ships[1]+0x1A
    assert raw[address-BASE:address-BASE+2] == struct.pack('<H', crew[1])
    changed = bytearray(raw)
    changed[address-BASE:address-BASE+2] = b'\0\0'
    cpu.mem_write(address, b'\0\0')
    assert get(0x35094, fleet) == 1
    assert get(0x35048, fleet) > 0 and get(0x55444, ships[0]) == crew[0]
    return bytes(changed), dict(action=ACTION, fleet=fleet, ship_slot=1, ship_name=name,
        original_crew=crew[1], flagship_crew_preserved=crew[0], original_empty_slot_search_returns=1,
        changes=[dict(address=address, before=crew[1], after=0)], verified_only_original_mobile_crew_field_changed=True,
        earned_crew_loss_or_battle_outcome=False, original_mode_position_and_inventory_unchanged=True,
        before_sha256=sha256(raw).hexdigest(), after_sha256=sha256(changed).hexdigest())


def main():
    assert not OUT.exists() and OUT.resolve().drive.upper() == 'E:'
    staged = load(STAGED)
    prior = load(PRIOR/'run_plan.json')
    terminal = load(PRIOR/'terminal.json')
    donor, inputs = Path(prior['donor']), Path(prior['initial_input_schedule'])
    assert digest(CANDIDATE) == staged['candidate_sha256'] == prior['ROM_sha256']
    assert digest(donor) == prior['donor_sha256'] and digest(inputs) == prior['initial_input_schedule_sha256']
    journal_source = PRIOR/'navigation_inputs.jsonl'
    assert digest(journal_source) == terminal['final_journal_sha256']
    commands = [json.loads(s) for s in journal_source.read_text(encoding='utf-8').splitlines()][:3]
    assert commands[-1]['until'] == 7600
    commands.append(dict(until=7800, duration=1, battle_fixture=ACTION))
    OUT.mkdir()
    journal = OUT/'navigation_inputs.jsonl'
    journal.write_text(''.join(json.dumps(row)+'\n' for row in commands), encoding='utf-8')
    args = ['headless_desmume_v193.py','--rom',str(CANDIDATE),'--out',str(OUT/'capture'),
        '--frames','11000','--inputs-json',str(inputs),'--battery-save',str(donor),'--touchscreen',
        '--capture-every','999999','--pause-at','4800','--allow-battle-fixtures','--dump-ram']
    plan = OUT/'run_plan.json'
    save(plan, dict(candidate_sha256=digest(CANDIDATE), donor_sha256=digest(donor), initial_commands=commands,
        run_arguments=args, research_fixture_only=True, stage_rom_bytes_unmodified=True, tool_source_sha256=digest(__file__)))
    stream = GrowingCommands(journal)
    originals = sys.stdin, sys.argv, dispatch.apply_fixture
    try:
        sys.stdin, sys.argv, dispatch.apply_fixture = stream, args, fixture
        harness.main()
    finally:
        sys.stdin, sys.argv, dispatch.apply_fixture = originals
        stream.close()
    assert digest(donor) == prior['donor_sha256']
    report = OUT/'capture/capture_report.json'
    result = load(report)
    assert result['cold_boot'] and not result['savestate_loaded'] and result['ROM_sha256'] == staged['candidate_sha256']
    assert len(result['synthetic_battle_recovery_proximity_fixtures']) == 1
    save(OUT/'terminal.json', dict(exit_code=0, report=str(report), report_sha256=digest(report),
        plan_sha256=digest(plan), journal_sha256=digest(journal), original_donor_unchanged=True))


if __name__ == '__main__':
    main()
