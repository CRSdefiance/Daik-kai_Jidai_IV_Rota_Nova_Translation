"""Bound original low trend pair and SDK seed; no inventory/location changes."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm,raw,request):
    config=read('translations/category_dialogue_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'],config['target_arm9_sha256'])
    assert set(request)=={'product'} and type(request['product']) is int and 0<=request['product']<124 and len(raw)==4194304
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x5F904,0x5FCA0),(0xB30EC,0xB3134),(0xB31E0,0xB320C),(0x519D4,0x51A28),(0xD9824,0xD9868),(0xC5B7C,0xC5BA0)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);assert get(0xB65E4)==22
    slots=[get(0xB30EC,(town,n)) for n in (0,1)]
    assert [bytes(cpu.mem_read(p,2)) for p in slots]==[bytes((125,0)),bytes((125,0))]
    product=request['product'];object_pointer=get(0xCB124)+4+product*16
    assert get(0xC5B7C,(object_pointer,))==product
    category=cpu.mem_read(object_pointer+12,1)[0]
    # Use the actual initialized object's category, exactly as5FC40 does.
    # Static resource byte6 is not identical for every runtime product.
    assert 0<=category<18
    seed_pointer=struct.unpack_from('<I',arm,0xD9830)[0]
    values=[(slots[1],bytes((product,10)),'original second town trend pair'),(seed_pointer,struct.pack('<I',3),'original SDK RNG seed')]
    after=bytearray(raw);changes=[]
    for address,data,field in values:
        for n,value in enumerate(data):
            at=address+n-BASE
            if after[at]!=value:changes.append({'address':BASE+at,'before':after[at],'after':value,'field':field});after[at]=value
    assert 2<=len(changes)<=6 and sum(a!=b for a,b in zip(raw,after,strict=True))==len(changes)
    cpu.mem_write(BASE,bytes(after));assert get(0xB31E0,(town,product))==10
    return bytes(after),{'synthetic_category_trend_fixture':True,'changes':changes,'product':product,'category':category,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'ARM9_sha256':sha(arm),
        'source_trend_value':10,'source_RNG_seed':3,'all_other_RAM_inventory_money_location_quests_and_flags_unchanged':True,
        'original_UI_topic_selection_requires_actual_pixel_verification':True,'earned_trend_or_exact_UI_RNG_draw_count_not_claimed':True,
        'fixture_source_sha256':sha(Path(__file__).read_bytes())}
