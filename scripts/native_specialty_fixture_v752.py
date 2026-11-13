"""One inventory availability bit; run original eligibility to its question call."""

from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import read


def eligibility(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    result = []
    executed = set()

    def observe(u, address, size, unused):
        executed.add(address)
        if address == BASE + 0x53F9C:
            names = [bytes(u.mem_read(u.reg_read(r), 80)).split(b'\0')[0].decode('ascii') for r in (UC_ARM_REG_R2, UC_ARM_REG_R3)]
            result.append({'message': u.reg_read(UC_ARM_REG_R1), 'names': names})
            u.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, observe)
    try:
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, 0x027E0000)
        cpu.emu_start(BASE + 0xBAB64, 0x027E0000, count=100000)
    finally:
        cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_PC) in (0x027E0000, BASE + 0x53F9C)
    return result, sorted(executed)


def assign(arm, raw, request):
    config = read('translations/specialty_question_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])
    assert request == {'item': 4} and len(raw) == 4194304
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xBAB64:0xBADC8] == clean[0xBAB64:0xBADC8]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    call(cpu, 0xB65E4, ())
    assert cpu.reg_read(UC_ARM_REG_R0) == 22
    call(cpu, 0xCB190, ())
    address = cpu.reg_read(UC_ARM_REG_R0) + 4 + 4 * 20 + 17
    at = address - BASE
    assert raw[at] == 8
    after = bytearray(raw)
    after[at] |= 4
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == 1
    before_question, _ = eligibility(arm, raw)
    questions, executed = eligibility(arm, bytes(after))
    assert before_question == [] and questions == [{'message': 742, 'names': ['Baby Shark', 'Caviar']}]
    assert {BASE + a for a in (0xBAB64,0x4A224,0x4A448,0xBAC1C,0xB3B58,0xB5154,0xB3FD4,0xBAD0C)} <= set(executed)
    return bytes(after), {'synthetic_specialty_inventory_fixture': True,
        'changes': [{'address': address, 'before': 8, 'after': 12, 'field': 'Baby Shark original inventory availability bit'}],
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'original_full_eligibility_reaches_question_with_only_availability_bit': questions,
        'before_fixture_original_eligibility_returns_without_question': True,
        'executed_original_eligibility_instruction_addresses': executed,
        'all_other_RAM_stock_town_technology_money_location_flags_and_items_unchanged': True,
        'ordinary_item_acquisition_and_UI_or_transfer_not_claimed_by_this_probe': True,
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
