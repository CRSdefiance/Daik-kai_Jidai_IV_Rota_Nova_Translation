"""Athens date/facility/discovery inputs, including before ordinary docking."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def set_condition(arm, raw, request):
    cfg = read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) in (cfg['source_arm9_sha256'], cfg['target_arm9_sha256']) and len(raw) == 0x400000
    assert set(request) == {'mode', 'facility', 'day'} and request['mode'] == 'ceremony-Athens'
    role, day = request['facility'], request['day']
    assert type(role) is int and role in (9, 11) and type(day) is int and 20 <= day <= 24
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xB5050, 0xB508C), (0xCC9C8, 0xCCA30), (0x610FC, 0x61C18), (0x87318, 0x873F4))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    assert all(raw[a:b] == arm[a:b] for a, b in spans)
    u = machine(arm); u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args, instruction_limit=500000)
        return u.reg_read(UC_ARM_REG_R0)

    fleet = get(0xCB1A8)+4+get(0x2E58C)*0x84
    current = get(0xB65E4); fleet_town = get(0x34674, (fleet,))
    assert current == 19 or fleet_town == 0x73
    town = get(0xCB178)+4+19*108
    assert get(0xB5170, (town,)) == 7
    site = get(0xCB16C)+4+7*8
    mask_at, tick_at, flag_at = town+12, get(0xCB1B4)+8, site+4
    mask = struct.unpack_from('<I', raw, mask_at-BASE)[0]
    old_ticks = struct.unpack_from('<I', raw, tick_at-BASE)[0]
    old_flag = raw[flag_at-BASE]; dest = 0x02451000

    def date():
        get(0xCC9C8, (tick_at-8, dest, dest+4, dest+8))
        return list(struct.unpack('<3I', u.mem_read(dest, 12)))

    before_date = date()
    for days in range(61):
        ticks = old_ticks+48*days
        assert ticks < 2**32
        u.mem_write(tick_at, struct.pack('<I', ticks)); after_date = date()
        if after_date[1]+1 == day:
            break
    else:
        raise AssertionError('No target within 60 forward days')
    assert before_date[2] == after_date[2]
    for n in (9, 10, 11):
        get(0xB5050, (town, n, int(n == role)))
        assert bool(get(0xB507C, (town, n))) == (n == role)
    new_mask = struct.unpack('<I', u.mem_read(mask_at, 4))[0]
    assert new_mask == (mask & ~0xE00) | (1 << role)
    # Prove the flag with the original discovery method. Discard its fame/reward.
    reward = get(0x87318, (site, 19, role))
    flag = bytes(u.mem_read(flag_at, 1))[0]; assert flag == old_flag | 1
    after = bytearray(raw)
    struct.pack_into('<I', after, tick_at-BASE, ticks)
    struct.pack_into('<I', after, mask_at-BASE, new_mask)
    after[flag_at-BASE] = flag
    allowed = set(range(tick_at, tick_at+4)) | set(range(mask_at, mask_at+4)) | {flag_at}
    changes = [dict(address=BASE+i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert all(r['address'] in allowed for r in changes)
    return bytes(after), dict(synthetic_ceremony_Athens_fixture=True, town_ID=19, site_ID=7,
        current_town_at_application=current, fleet_port_at_application=fleet_town, facility_role=role, target_day=day,
        before_native_date=before_date, after_native_date=after_date, before_ticks=old_ticks, after_ticks=ticks,
        synthetic_forward_days=days, before_facility_mask=mask, after_facility_mask=new_mask,
        before_discovery_flags=old_flag, after_discovery_flags=flag, native_discovery_reward_not_applied=reward,
        only_calendar_word_Athens_facility_mask_and_site7_flag_owned=True,
        original_eligibility_speakers_dialogue_effects_time_and_docking_not_replaced=True,
        earned_access_discovery_or_elapsed_daily_updates_not_claimed=True, changes=changes,
        before_RAM_sha256=sha(raw), after_RAM_sha256=sha(after), ARM9_sha256=sha(arm))
