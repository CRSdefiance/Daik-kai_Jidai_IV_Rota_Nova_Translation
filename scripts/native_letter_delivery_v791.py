"""Explicit qualification,random-input and registered-letter deadline controls."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_item_roles_v789 import ARMS
from scripts.native_letter_eligibility_v790 import set_condition as qualify
from scripts.native_machine_scoped_v764 import machine

BASE=0x02000000


def set_condition(arm,raw,request):
    if request=={'mode':'Istanbul-letter-eligibility'}:return qualify(arm,raw,request)
    allowed=({'mode':'controlled-letter-random-input'},{'mode':'two-registered-letter-deadlines'})
    if sha(arm) not in ARMS or len(raw)!=0x400000 or request not in allowed:
        raise ValueError('Exact source ROM and declared delivery-control request required')
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0xD9824,0xD9868),(0x519D4,0x51A28),(0x91598,0x91658),(0x93BAC,0x93C04)):
        assert arm[lo:hi]==source[lo:hi]
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):
        call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    result=bytearray(raw);fields=[];owned=set()
    def write(at,value,label):
        before=struct.unpack_from('<I',result,at-BASE)[0]
        struct.pack_into('<I',result,at-BASE,value)
        fields.append({'address':at,'before':before,'after':value,'meaning':label})
        owned.update(range(at-BASE,at-BASE+4))
    if request['mode']=='controlled-letter-random-input':
        state=struct.unpack_from('<I',source,0xD9830)[0]
        seed=struct.unpack_from('<I',source,0x51A24)[0]
        assert state==0x02168EB8 and seed==1234
        before=bytes(cpu.mem_read(BASE,0x800000))
        get(0xD9824,(seed,))
        after=bytes(cpu.mem_read(BASE,0x800000))
        assert {i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b}<=set(range(state-BASE,state-BASE+4))
        write(state,seed,'Original initial seed supplied as a disclosed paired-test input')
    else:
        controller=get(0xCB1A8)+0x2090
        assert get(0xB65E4)==22 and get(0x825E4,(controller,1))==16
        pool,clock=get(0xCB130),get(0xCB1B4)
        now=struct.unpack('<I',cpu.mem_read(clock+8,4))[0]
        context=get(0xCB19C)
        assert struct.unpack('<I',cpu.mem_read(context+0x135C,4))[0]==64
        records=[]
        for index,kind in ((4,2),(5,0)):
            obj=pool+4+index*16
            body=bytes(cpu.mem_read(obj,16))
            assert struct.unpack_from('<I',body)[0]==0x0214C618
            assert list(body[4:8])==[kind,2,16,0]
            assert struct.unpack_from('<I',body,12)[0]>now
            records.append({'index':index,'object':obj,'source_record_hex':body.hex()})
            write(obj+12,now+48,'Accelerate an already normally registered letter to next day')
        fields.append({'current_tick':now,'deadline_tick':now+48,'original_records':records,
            'source_dispatcher':0x02091598,'source_due_comparison':0x02091604})
    changed={i for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b}
    assert changed<=owned and len(changed)<=(4 if request['mode']=='controlled-letter-random-input' else 8)
    return bytes(result),{'synthetic_letter_delivery_control':True,'mode':request['mode'],'ARM9_sha256':sha(arm),
        'declared_fields':fields,'changes':[{'address':BASE+i,'before':raw[i],'after':result[i]} for i in sorted(changed)],
        'all_other4MiB_bytes_exact':True,'text_dialogue_menu_outcome_logic_money_and_calendar_unchanged':True,
        'earned_delivery_timing_or_uncontrolled_random_outcomes_not_claimed':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result)}
