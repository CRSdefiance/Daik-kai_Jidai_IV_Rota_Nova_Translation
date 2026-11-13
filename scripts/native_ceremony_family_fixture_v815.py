"""Isolated religious-facility and forward calendar inputs; original scenes run."""

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
    assert set(request) == {'mode', 'facility', 'day'} and request['mode'] == 'ceremony-family'
    role, day = request['facility'], request['day']
    assert type(role) is int and role in (9, 10, 11)
    assert type(day) is int and 23 <= day <= 27
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xB5050, 0xB508C), (0xB811C, 0xB8174), (0xCC9C8, 0xCCA30), (0x610FC, 0x61C18))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    u = machine(arm); u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args, instruction_limit=500000)
        return u.reg_read(UC_ARM_REG_R0)

    assert get(0xB65E4) == 22
    town = get(0xB6618); calendar = get(0xCB1B4)
    mask_at = town+12; tick_at = calendar+8
    mask = struct.unpack_from('<I', raw, mask_at-BASE)[0]
    old_ticks = struct.unpack_from('<I', raw, tick_at-BASE)[0]
    dest = 0x02451000

    def date():
        get(0xCC9C8, (calendar, dest, dest+4, dest+8))
        return list(struct.unpack('<3I', u.mem_read(dest, 12)))

    before_date = date()
    for days in range(0, 61):
        ticks = old_ticks+48*days
        assert ticks < 2**32
        u.mem_write(tick_at, struct.pack('<I', ticks))
        after_date = date()
        if after_date[1]+1 == day:
            break
    else:
        raise AssertionError('No target date within 60 forward days')
    assert after_date[2] == before_date[2]
    for n in (9, 10, 11):
        get(0xB5050, (town, n, int(n == role)))
        assert bool(get(0xB507C, (town, n))) == (n == role)
    new_mask = struct.unpack('<I', u.mem_read(mask_at, 4))[0]
    assert new_mask == (mask & ~0xE00) | (1 << role)
    assert get(0xB811C) == 9
    after = bytes(u.mem_read(BASE, len(raw)))
    allowed = set(range(tick_at, tick_at+4)) | set(range(mask_at, mask_at+4))
    changes = [dict(address=BASE+i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert all(r['address'] in allowed for r in changes)
    return after, dict(synthetic_ceremony_family_fixture=True, mode=request['mode'], facility_role=role,
        target_day=day, town_ID=22, original_calendar_getter=BASE+0xCC9C8,
        before_native_date=before_date, after_native_date=after_date,
        before_ticks=old_ticks, after_ticks=ticks, synthetic_forward_days=days,
        before_facility_mask=mask, after_facility_mask=new_mask,
        original_facility_setter=BASE+0xB5050, native_icon_count=9,
        only_calendar_word_and_facility_mask_owned=True, changes=changes,
        original_day_and_choice_eligibility_dialogue_speakers_effects_and_returns_not_replaced=True,
        natural_campaign_facility_availability_and_elapsed_daily_updates_not_claimed=True,
        before_RAM_sha256=sha(raw), after_RAM_sha256=sha(after), ARM9_sha256=sha(arm))
