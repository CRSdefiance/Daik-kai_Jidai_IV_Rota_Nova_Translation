"""Mapped room assignment,one experience word and eleven calendar days only."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_strategist_fixture_v776 import assign
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call

BASE=0x02000000


def assign_expert(arm,raw,request):
    after,proof=assign(arm,raw,request)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a,b in ((0x7E668,0x7E678),(0x7E728,0x7E750),(0x7DCC8,0x7DE20),
                (0xCC9C8,0xCCA30),(0x567CC,0x56990),(0x571E0,0x572C8)):
        assert arm[a:b]==clean[a:b]
    u=machine(arm)
    u.mem_write(BASE,after)
    def get(fn,args=()):
        call(u,fn,args)
        return u.reg_read(UC_ARM_REG_R0)
    actor=proof['actor']
    calendar=get(0xCB1B4)
    xp=get(0x7E670,(actor,))
    secondary=get(0x7E668,(actor,))
    ticks=struct.unpack('<I',u.mem_read(calendar+8,4))[0]
    assert struct.unpack('<I',u.mem_read(actor+16,4))[0]==xp and ticks+528<2**32
    result=bytearray(after)
    owned=set(r['address'] for r in proof['changes'])
    for address,before,target in ((actor+16,xp,300000),(calendar+8,ticks,ticks+528)):
        old,new=struct.pack('<I',before),struct.pack('<I',target)
        assert result[address-BASE:address-BASE+4]==old
        for i in range(4):
            owned.add(address+i)
            if old[i]!=new[i]:proof['changes'].append({'address':address+i,'before':old[i],'after':new[i]})
        result[address-BASE:address-BASE+4]=new
    u.mem_write(BASE,bytes(result))
    assert get(0x7E670,(actor,))==300000 and get(0x7E668,(actor,))==secondary
    level=get(0x7E728,(actor,))
    skill=get(0x7DD38,(actor,7,6))
    speech=get(0x7DCC8,(actor,8))
    assert skill>=200 and speech>0
    changed={BASE+i for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b}
    assert changed=={r['address'] for r in proof['changes']} and changed<=owned
    assert len(changed)<=11
    proof.update({'synthetic_experience_and_calendar_fixture':True,
        'one_experience_counter_before':xp,'one_experience_counter_after':300000,
        'calendar_ticks_before':ticks,'calendar_ticks_after':ticks+528,'calendar_days_advanced':11,
        'original_level_after':level,'original_submenu_skill_after':skill,'original_Speech_after':speech,
        'only_three_declared_room_type_and_assignment_bytes_changed':False,
        'code_inventory_stats_money_location_other_bytes_unchanged':False,
        'all_other4MiB_bytes_exact':True,'stats_XP_money_location_calendar_unchanged':False,
        'only_three_assignment_bytes_one_XP_word_one_calendar_word_owned':True,
        'attributes_health_inventory_funds_location_code_menu_flags_unchanged':True,
        'earned_experience_time_refit_assignment_or_campaign_progress_not_claimed':True,
        'after_RAM_sha256':sha(result)})
    return bytes(result),proof
