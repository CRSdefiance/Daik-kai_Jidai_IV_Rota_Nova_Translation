"""Bounded market share and original regional standing for village-rumor tests."""

import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.native_recruit_shortfall_fixture_v782 import ARMS, BASE
from scripts.probe_button_prompt_native import STACK, STOP


def set_condition(arm, raw, request):
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request not in ({'mode': 'village-casual'}, {'mode': 'village-formal'}):
        raise ValueError('Exact V780/V782 and a declared village-dialogue mode required')
    formal = request['mode'] == 'village-formal'
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0x56650, 0x56704), (0x576CC, 0x578E0), (0x3CC38, 0x3CC80), (0xB4A88, 0xB4AD4)):
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    town = get(0xB6618)
    assert get(0xB65E4) == 22
    region = get(0xB2B48, (town,))
    own = get(0x397D8)
    assert own == 2 and region == 1
    company = get(0xCB160)+4+own*76
    assert bytes(u.mem_read(town+0x10, 6)) == bytes((9, 99, 21, 0, 21, 0))
    assert get(0xB4A88, (town,)) == 0 and get(0x3CC74, (company, region)) == 0
    assert get(0xB3FD4, (town, 0)) >= 3000
    # Source market slots are (company byte, share byte), as in the prior
    # authorized Market fixtures. Preserve their total99 and both unused bytes.
    result = bytearray(raw)
    result[town+0x10-BASE:town+0x16-BASE] = bytes((9, 68, 2, 31, 21, 0))
    owned = set(range(town+0x10-BASE, town+0x16-BASE))
    standing_at = company+0x10+region*2
    if formal:
        get(0x3CC38, (company, region, 3000))
        assert get(0x3CC74, (company, region)) == 3000
        result[standing_at-BASE:standing_at-BASE+2] = bytes(u.mem_read(standing_at, 2))
        owned.update((standing_at-BASE, standing_at-BASE+1))
    u.mem_write(BASE, bytes(result))
    assert get(0xB4A88, (town,)) == 31 and get(0xB4AA8, (town, 9)) == 68
    assert get(0x3CC74, (company, region)) == (3000 if formal else 0)
    seen = []

    def stop(c, pc, size, unused):
        seen.append(pc)
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE, stop, begin=BASE+a, end=BASE+a) for a in (0x566D8, 0x566F0)]
    try:
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.emu_start(BASE+0x56688, STOP, count=100000)
        assert seen == [BASE+(0x566D8 if formal else 0x566F0)]
    finally:
        for h in hooks:
            u.hook_del(h)
    # Check the complete original village selector with a declared temporary
    # information record. This is a CPU preflight, not an actual dialogue claim.
    scratch = 0x02479000
    u.mem_write(scratch, struct.pack('<5I', 0, 0, int(formal), 0, 0))
    speeches = []

    def speech(c, pc, size, unused):
        at = c.reg_read(UC_ARM_REG_R2)
        speeches.append({'speaker': c.reg_read(UC_ARM_REG_R0), 'ID': c.reg_read(UC_ARM_REG_R1),
                         'argument_hex': bytes(c.mem_read(at, 256)).split(b'\0')[0].hex()})
        c.emu_stop()

    hook = u.hook_add(UC_HOOK_CODE, speech, begin=BASE+0x53FE4, end=BASE+0x53FE4)
    try:
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R0, scratch)
        u.reg_write(UC_ARM_REG_R1, 22)
        u.emu_start(BASE+0x576CC, STOP, count=100000)
        assert len(speeches) == 1 and speeches[0]['ID'] == (1028 if formal else 1029)
    finally:
        u.hook_del(hook)
    changed = [i for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert set(changed) <= owned and len(changed) == (5 if formal else 3)
    return bytes(result), {
        'synthetic_village_rumor_prerequisite_fixture': True, 'mode': request['mode'], 'ARM9_sha256': sha(arm),
        'town_ID': 22, 'native_town': town, 'current_company': own,
        'original_market_slots': [9, 99, 21, 0, 21, 0], 'fixture_market_slots': [9, 68, 2, 31, 21, 0],
        'total_share99_preserved': True, 'native_own_share_after': 31,
        'regional_standing_halfword': standing_at, 'standing_after': 3000 if formal else 0,
        'original_standing_method': BASE+0x3CC38 if formal else None,
        'original_Tavern_style_branch': seen[0], 'CPU_only_full_village_selector_preflight': speeches[0],
        'changes': [{'address': BASE+i, 'before': raw[i], 'after': result[i]} for i in changed],
        'all_other4MiB_bytes_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(result),
        'cash_health_cargo_location_village_discovery_code_menu_flags_and_original_saves_unchanged': True,
        'no_earned_market_share_reputation_or_village_discovery_claim': True}
