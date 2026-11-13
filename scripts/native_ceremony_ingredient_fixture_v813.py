"""Five original cargo slots for isolated native Cappadocia ingredient tests."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.commodity_fidelity import TABLE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read

INGREDIENTS={'Sulfur':(94,'イオウ'),'Timber':(95,'木材'),'Saltpeter':(93,'ショウ石')}


def set_condition(arm,raw,request):
    cfg=read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) in (cfg['source_arm9_sha256'],cfg['target_arm9_sha256']) and len(raw)==0x400000
    assert set(request)=={'mode','ingredient'} and request['mode']=='ceremony-ingredient' and request['ingredient'] in INGREDIENTS
    product,japanese=INGREDIENTS[request['ingredient']]
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b]==clean[a:b] for a,b in ((0x36180,0x36230),(0x36C70,0x36CBC)))
    p=struct.unpack_from('<I',clean,TABLE+product*12)[0]
    assert clean[p-BASE:].split(b'\0')[0].decode('cp932')==japanese
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=300000)
        return u.reg_read(UC_ARM_REG_R0)
    def word(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    assert get(0xB65E4)==22
    ob=get(0xCB124)+4+product*16
    p=get(word(word(ob)+8)-BASE,(ob,))
    assert bytes(u.mem_read(p,96)).split(b'\0')[0].decode('ascii')==request['ingredient']
    index=get(0x2E58C);fleet=get(0xCB1A8)+4+index*0x84
    ship=get(0x36C94,(fleet+12,));assert ship
    assert all(get(0x36C94,(fleet+12+n*8,))==0 for n in range(1,5))
    before_count=get(0x36180,(fleet,0x02440000))
    before=bytes(u.mem_read(ship+0x50,60));assert all(before[n*12]<=125 and before[n*12+1]<=4 for n in range(5))
    result=bytearray(raw);changes=[]
    for n in range(5):
        at=ship+0x50+n*12
        if result[at-BASE]!=product:
            changes.append(dict(address=at,before=result[at-BASE],after=product))
            result[at-BASE]=product
    u.mem_write(BASE,bytes(result));assert get(0x36180,(fleet,0x02440000))==5
    cargo=bytes(u.mem_read(0x02440000,60));assert all(cargo[n*12]==product for n in range(5))
    for n in range(5):assert cargo[n*12+1:n*12+12]==before[n*12+1:n*12+12]
    assert sum(a!=b for a,b in zip(raw,result,strict=True))==len(changes)
    return bytes(result),dict(synthetic_ceremony_ingredient_cargo_fixture=True,mode=request['mode'],
        ingredient=request['ingredient'],commodity_ID=product,clean_Japanese=japanese,
        fleet_index=index,fleet=fleet,ship=ship,original_cargo_getter=BASE+0x36180,
        before_cargo_count=before_count,after_cargo_count=5,original_five_slot_span=[ship+0x50,ship+0x8C],
        source_native_five_slot_loop=BASE+0x361C8,before_ship_cargo_hex=before.hex(),after_native_cargo_hex=cargo.hex(),
        only_five_product_bytes_owned_grade_prices_other_cargo_health_funds_location_code_quests_and_calendar_exact=True,
        original_quest_quantity_test_consumption_accumulation_and_outcomes_not_replaced=True,
        earned_trade_purchase_or_normal_cargo_acquisition_not_claimed=True,
        changes=changes,before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result),ARM9_sha256=sha(arm))
