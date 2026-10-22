"""Disclosed original eligibility inputs for isolated Palace playback.

No text, code, menu flags, dialogue selection or transaction result is patched.
"""

import struct

from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_SP,UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK

ARMS={'efde1eeffac95af843f489c6ff388a950cc1faabccce9f0962ce54ca32de8bc5',
      'e3074ecfb6196ddea857f92850720625d4c16da05d046a3899166d2bfa00a323'}
MODES=('Market-introduction','Market-recommendation','contract-insufficient-funds','Istanbul-treasure-headquarters')


def set_condition(arm,raw,request):
    if sha(arm) not in ARMS or len(raw)!=0x400000 or set(request)!={'mode'} or request['mode'] not in MODES:
        raise ValueError('Exact V792/V797 and one declared Palace qualification mode required')
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x5D4EC,0x5E1FC),(0x82F18,0x82F84),(0x3CC80,0x3CD2C),(0x4A1F8,0x4A230))
    assert all(arm[lo:hi]==source[lo:hi] for lo,hi in spans)
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):
        call(cpu,fn,args,instruction_limit=300000);return cpu.reg_read(UC_ARM_REG_R0)
    company_root=get(0xCB160);company_id=get(0x397D8,(company_root,));company=company_root+4+company_id*76
    actors=get(0xCB184);admiral=actors+0x19E4;town=get(0xB65E4)
    assert company_id==2 and town==22
    output=bytearray(raw);fields=[];owned=set()
    def field(at,value,meaning):
        old=bytes(output[at-BASE:at-BASE+len(value)])
        output[at-BASE:at-BASE+len(value)]=value
        fields.append({'address':at,'source_hex':old.hex(),'target_hex':value.hex(),'meaning':meaning})
        owned.update(range(at-BASE,at-BASE+len(value)))
    mode=request['mode']
    if mode.startswith('Market-'):
        code=0 if mode=='Market-introduction' else 1
        before=bytes(cpu.mem_read(admiral+0x68,4));get(0x82F18,(admiral,code))
        assert get(0x82F60,(admiral,))==code
        after=bytes(cpu.mem_read(admiral+0x68,4))
        assert (int.from_bytes(before,'little')^int.from_bytes(after,'little'))&~3==0
        field(admiral+0x68,after,f'Original Market letter setter82F18:mode{code}')
    elif mode=='contract-insufficient-funds':
        before=get(0x3CCC8,(company,));get(0x3CC80,(company,(1-before)&0xffffffff))
        assert get(0x3CCC8,(company,))==1
        field(company+12,bytes(cpu.mem_read(company+12,4)),'Original money method3CC80 adjusts isolated company funds to1')
        get(0x82F18,(admiral,2));field(admiral+0x68,bytes(cpu.mem_read(admiral+0x68,4)),'Clear any test Market letter through original setter')
    else:
        assert get(0x3CD24,(company,)) in (7,22)
        field(company+11,bytes([22]),'Temporary headquarters eligibility input;original3CD24 reads this one-byte field')
        item=get(0xCB190)+4+13*20
        assert get(0x4A448,(item,))==0 and get(0x4A410,(item,))==12500 and not get(0x4A1F8,(item,))
        get(0x4A204,(item,1));assert get(0x4A224,(item,))==4
        field(item+17,bytes(cpu.mem_read(item+17,1)),'Original acquired-flag setter grants Alchemy Book13;no loan/return flag is forced')
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,output,strict=True)) if a!=b]
    assert all(c['address']-BASE in owned for c in changes)
    cpu.mem_write(BASE,bytes(output))
    # Execute the original eligibility loop before the UI call. The six
    # enabled fields are observations, never patched fixture outputs.
    template=struct.unpack_from('<I',arm,0x5D63C)[0]
    cpu.mem_write(STACK+12,bytes(cpu.mem_read(template,96)))
    cpu.reg_write(UC_ARM_REG_SP,STACK)
    cpu.emu_start(BASE+0x5D518,BASE+0x5D60C,count=1000000)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x5D60C
    flags=[struct.unpack('<I',cpu.mem_read(STACK+0x10+i*16,4))[0] for i in range(6)]
    if mode=='Market-introduction':assert flags[3]==1
    elif mode=='Market-recommendation':assert flags[2]==1
    elif mode=='Istanbul-treasure-headquarters':assert flags[4]==1
    return bytes(output),{'synthetic_Palace_qualification_fixture':True,'mode':mode,'ARM9_sha256':sha(arm),
        'company':company,'player_company_id':company_id,'town_id':town,'admiral':admiral,
        'original_menu_eligibility_flags_after':flags,'source_defined_fields':fields,'changes':changes,
        'all_other4MiB_RAM_bytes_exact':True,'original_menu_filters_dialogue_and_outcome_methods_unmodified':True,
        'earned_letter_treasure_funds_headquarters_or_normal_travel_not_claimed':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(output),
        'original_source_spans':[{'offsets':[lo,hi],'sha256':sha(source[lo:hi])} for lo,hi in spans]}
