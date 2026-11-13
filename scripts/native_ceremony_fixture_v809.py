"""One source-mapped calendar word for isolated original ceremony testing."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read


def set_condition(arm,raw,request):
    cfg=read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) in (cfg['source_arm9_sha256'],cfg['target_arm9_sha256']) and len(raw)==0x400000
    assert set(request)=={'mode','day'} and request['mode']=='ceremony-day'
    target_day=request['day'];assert type(target_day) is int and 14<=target_day<=28
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xCC9C8:0xCCA30]==clean[0xCC9C8:0xCCA30]
    assert arm[0x61B44:0x61C18]==clean[0x61B44:0x61C18]
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=300000)
        return u.reg_read(UC_ARM_REG_R0)
    calendar=get(0xCB1B4);town=get(0xB65E4)
    assert town==22 and BASE<=calendar<BASE+len(raw)-12
    dest=0x02451000
    def date():
        get(0xCC9C8,(calendar,dest,dest+4,dest+8))
        return list(struct.unpack('<3I',u.mem_read(dest,12)))
    before_date=date();delta=target_day-(before_date[1]+1)
    assert 0<=delta<=14
    at=calendar+8;ticks=struct.unpack_from('<I',raw,at-BASE)[0]
    value=ticks+delta*48;assert value<2**32
    result=bytearray(raw);struct.pack_into('<I',result,at-BASE,value)
    u.mem_write(at,struct.pack('<I',value));after_date=date()
    assert after_date[0]==before_date[0] and after_date[1]+1==target_day and after_date[2]==before_date[2]
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(at<=r['address']<at+4 for r in changes) and len(changes)<=4
    return bytes(result),dict(synthetic_ceremony_calendar_fixture=True,mode=request['mode'],day=target_day,
        town_ID=town,original_calendar_object=calendar,only_owned_calendar_word=at,
        original_date_provider=BASE+0xCC9C8,before_native_date=before_date,after_native_date=after_date,
        before_ticks=ticks,after_ticks=value,synthetic_days_forward=delta,changes=changes,
        all_other4MiB_bytes_including_code_speaker_dialogue_selection_menu_outcome_and_inventory_exact=True,
        original_ceremony_eligibility_dialogue_effects_and_time_handler_not_replaced=True,
        elapsed_daily_updates_food_costs_or_earned_campaign_progress_not_claimed=True,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result),ARM9_sha256=sha(arm))
