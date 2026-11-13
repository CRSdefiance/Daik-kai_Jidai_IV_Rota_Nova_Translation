"""One named ship's crew halfword, through its original setter, for a rare prompt."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine

BASE = 0x02000000
ARMS = {'d2d2670bfbbb8ce1c3433b0c1a6220f385ef8beba5678bea9e9d4bb612b57abb',
        'daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02'}


def set_condition(arm, raw, request):
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request != {'mode': 'required-crew-shortfall'}:
        raise ValueError('Exact V780/V782 and declared required-crew-shortfall fixture required')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x181B4, 0x181C4), (0x34FC0, 0x35094), (0x36C48, 0x36CB8), (0x57408, 0x576CC)):
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    index = get(0x2E58C)
    assert index == 1
    fleet = get(0xCB1A8)+4+index*132
    assert get(0x34674, (fleet,)) < 114
    ships = [get(0x36C94, (fleet+12+i*8,)) for i in range(5)]
    assert ships[0] and not any(ships[1:])
    model = ships[0]
    assert bytes(u.mem_read(model+8, 24)).split(b'\0')[0] == b'Vestaros'
    assert [get(fn, (fleet,)) for fn in (0x35048, 0x35004, 0x34FC0)] == [39, 39, 124]
    at = model+0x44
    assert struct.unpack('<H', u.mem_read(at, 2))[0] == get(0x181BC, (model,)) == 39
    get(0x181B4, (model, 0))
    assert get(0x181BC, (model,)) == 0 and get(0x35048, (fleet,)) == 0
    assert [get(fn, (fleet,)) for fn in (0x35004, 0x34FC0)] == [39, 124]
    result = bytearray(raw)
    result[at-BASE:at-BASE+2] = bytes(u.mem_read(at, 2))
    changed = [i for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert set(changed) <= {at-BASE, at-BASE+1} and changed
    return bytes(result), {
        'synthetic_recruitment_shortfall_fixture': True, 'mode': request['mode'], 'ARM9_sha256': sha(arm),
        'fleet_index': index, 'fleet': fleet, 'ship': model, 'ship_name': 'Vestaros',
        'native_setter': BASE+0x181B4, 'owned_crew_halfword': at, 'crew_before': 39, 'crew_after': 0,
        'required_crew_unchanged': 39, 'capacity_unchanged': 124,
        'changes': [{'address': BASE+i, 'before': raw[i], 'after': result[i]} for i in changed],
        'all_other4MiB_bytes_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(result),
        'no_earned_loss_recruitment_or_normal_crew_state_claim': True,
        'health_cash_inventory_location_calendar_code_and_original_saves_unchanged': True}
