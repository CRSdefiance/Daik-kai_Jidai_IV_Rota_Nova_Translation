"""One original room-occupant byte for an explicitly synthetic Emilio Cabin test."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000


def assign(arm,raw,request):
    if sha(arm)!=read('translations/personal_chatter_editorial_release_v1.json')['target_arm9_sha256'] or len(raw)!=0x400000 or request is not True:
        raise ValueError('Exact V838,4MiB RAM and explicit true required')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a,b in ((0x81F54,0x81FA0),(0x82BB8,0x82BD0),(0x132C0,0x132CC),(0x1278C,0x128B4)):
        assert arm[a:b]==clean[a:b]
    cpu=machine(arm)
    cpu.mem_write(BASE,raw)
    def get(at,*args):
        call(cpu,at,args)
        return cpu.reg_read(UC_ARM_REG_R0)
    controller=get(0xCB1A8)+0x2090
    model=get(0x82E04,controller)
    assert get(0x132C0,model,12)==12 and get(0x82BC4,controller,12)==208
    assert all(get(0x82BC4,controller,i)!=14 for i in range(31))
    actor=get(0xCB184)+4+14*32
    faction=get(0x7E958,actor)
    company=get(0x397D8,get(0xCB160))
    assert company==2 and faction==21 and get(0x7E100,actor)==0 and get(0x7E0B4,actor)==3
    # Execute the source setter only on the scoped controller allocation.
    old=bytes(cpu.mem_read(controller,0x40))
    get(0x82BB8,controller,12,14)
    new=bytes(cpu.mem_read(controller,0x40))
    assert [(i,a,b) for i,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]==[(18,208,14)]
    target=controller+18
    after=bytearray(raw)
    assert after[target-BASE]==208
    after[target-BASE]=14
    assert get(0x82BC4,controller,12)==14 and get(0x81F54,controller,14)==12
    return bytes(after),{'synthetic_Emilio_Cabin_occupant_fixture':True,'actor_ID':14,
        'original_actor_faction_preserved':faction,'player_company':company,
        'actor_not_claimed_as_normally_recruited_or_owned':True,'original_Cabin_room_type':12,
        'original_room_slot':12,'controller':controller,'original_setter':0x02082BB8,
        'one_owned_assignment_byte_only':True,'all_other_RAM_including_faction_calendar_stats_health_money_RNG_text_code_exact':True,
        'changes':[{'address':target,'before':208,'after':14}],
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(bytes(after)),
        'native_original_ordinary_selector_and_rendering_unmodified':True}
