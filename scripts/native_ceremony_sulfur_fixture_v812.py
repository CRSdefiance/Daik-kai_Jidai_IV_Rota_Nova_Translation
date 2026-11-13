"""One existing cargo product byte for the original Cappadocia sulfur event."""

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
    assert request=={'mode':'ceremony-sulfur'}
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b]==clean[a:b] for a,b in ((0x36180,0x36230),(0x36C70,0x36CB0)))
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=300000)
        return u.reg_read(UC_ARM_REG_R0)
    def word(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    def text(at):return bytes(u.mem_read(at,128)).split(b'\0')[0]
    assert get(0xB65E4)==22
    root=get(0xCB124);goods=[]
    for n in range(124):
        ob=root+4+n*16;name=text(get(word(word(ob)+8)-BASE,(ob,)))
        if name==b'Sulfur':goods.append(n)
    assert len(goods)==1;product=goods[0]
    fleets=get(0xCB1A8);index=get(0x2E58C);fleet=fleets+4+index*0x84
    ship=get(0x36C94,(fleet+12,));name=text(ship+8)
    count=get(0x36180,(fleet,0x02440000));assert count==2
    before=bytes(u.mem_read(0x02440000,count*12));assert before[0]==raw[ship+0x50-BASE]
    assert before[0]!=product
    at=ship+0x50;result=bytearray(raw);result[at-BASE]=product
    u.mem_write(at,bytes([product]));assert get(0x36180,(fleet,0x02440000))==count
    after=bytes(u.mem_read(0x02440000,count*12))
    assert after==bytes([product])+before[1:]
    changes=[dict(address=at,before=raw[at-BASE],after=product)]
    assert sum(a!=b for a,b in zip(raw,result,strict=True))==1
    return bytes(result),dict(synthetic_one_existing_cargo_product_fixture=True,mode='ceremony-sulfur',
        fleet_index=index,fleet=fleet,ship=ship,ship_name=name.decode('ascii'),
        source_goods_ID=product,source_goods_name='Sulfur',original_cargo_getter=BASE+0x36180,
        original_cargo_count=count,fixture_cargo_count=count,before_cargo_hex=before.hex(),after_cargo_hex=after.hex(),
        one_byte_product_ID_changed_grade_prices_other_cargo_health_funds_code_location_and_quests_exact=True,
        original_quest_condition_consumption_and_outcome_handler_not_replaced=True,
        bought_or_earned_cargo_not_claimed=True,changes=changes,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result),ARM9_sha256=sha(arm))
