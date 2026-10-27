"""Two-byte isolated town-condition display fixture; no earned event credit."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine

BASE=0x02000000
ARM_SHA='9e54d5456e1de352c2cdf574a8cca5bcb93fbbbd0414fdb38b627b1278617d92'


def set_condition(arm,raw,request):
    if sha(arm)!=ARM_SHA or len(raw)!=0x400000:raise ValueError('Exact V773 and4MiB RAM required')
    if request!={'town':2,'status':3,'days':30}:raise ValueError('Only the declared Amsterdam Boom30 display fixture is allowed')
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
    root=get(0xCB178);town=root+4+2*108;here=get(0xB6618)
    assert get(0xB2B48,(here,))==get(0xB2B48,(town,))==0
    assert struct.unpack('<H',u.mem_read(town+8,2))[0]&1
    assert get(0xB2E04,(town,))==12
    at=town+0x6A-BASE;assert 0<=at<at+2<=len(raw)
    after=bytearray(raw);after[at:at+2]=bytes((3,30));u.mem_write(BASE,bytes(after))
    assert get(0xB2E04,(town,))==3
    label=get(0xB2D58,(town,));assert bytes(u.mem_read(label,5))==b'Boom\0'
    changes=[{'address':BASE+i,'before':raw[i],'after':after[i]} for i in range(at,at+2) if raw[i]!=after[i]]
    assert len(changes)==2
    return bytes(after),{'synthetic_town_condition_display_fixture':True,'town_ID':2,'town_object':town,
        'status':3,'duration':30,'native_UI_label':'Boom','changes':changes,
        'only_status_and_duration_bytes_changed':True,'all_other4MiB_bytes_exact':True,
        'ROM_or_donor_save_changed':False,'natural_condition_event_verified':False,
        'original_native_getters_verified':True,'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after)}
