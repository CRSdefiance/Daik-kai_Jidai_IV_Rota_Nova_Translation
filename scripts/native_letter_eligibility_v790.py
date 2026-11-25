"""Source-defined qualification inputs for isolated Istanbul diplomacy tests."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_item_roles_v789 import ARMS
from scripts.native_machine_scoped_v764 import machine

BASE=0x02000000


def set_condition(arm,raw,request):
    if sha(arm) not in ARMS or len(raw)!=0x400000 or request!={'mode':'Istanbul-letter-eligibility'}:
        raise ValueError('Exact V783/V788 and declared Istanbul qualification inputs required')
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x5B26C,0x5BC8C),(0x825E4,0x8261C),(0x829C8,0x82A44),
        (0x82EB0,0x82ED4),(0x3CB30,0x3CB90),(0x4A204,0x4A230),
        (0x7DCC8,0x7DE20),(0x7E668,0x7E750))
    for lo,hi in spans:assert arm[lo:hi]==source[lo:hi]
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):
        call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
    def name(obj,slot=8):
        vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
        fn=struct.unpack('<I',cpu.mem_read(vt+slot,4))[0]
        at=get(fn-BASE,(obj,))
        return bytes(cpu.mem_read(at,128)).split(b'\0')[0].decode('cp932')
    assert get(0xB65E4)==22 and get(0x7F244)==1
    controller=get(0xCB1A8)+0x2090
    model=get(0x82E04,(controller,))
    assert get(0x825E4,(controller,1))==208
    assert get(0x132C0,(model,15))==6 and get(0x82BC4,(controller,15))==208
    old_room=[i for i in range(31) if get(0x82BC4,(controller,i))==16]
    assert old_room==[21]
    actor=get(0xCB184)+4+16*32
    assert name(actor,0x20)=='Gerhard' and get(0x7E958,(actor,))==2
    company_root=get(0xCB160)
    own=get(0x397D8,(company_root,))
    assert own==2 and get(0x3CCC8,(company_root+4+own*76,))>=1000
    town=get(0xB6618);region=get(0xB2B48,(town,))
    assert region==1
    item=get(0xCB190)+4+(148+region)*20
    assert name(item)=="Cambyses' Crown" and get(0x82EB0,(region,))==0
    result=bytearray(raw);fields=[];owned=set()
    def write(at,payload,label):
        before=bytes(result[at-BASE:at-BASE+len(payload)])
        result[at-BASE:at-BASE+len(payload)]=payload
        fields.append({'address':at,'source_hex':before.hex(),'target_hex':payload.hex(),'meaning':label})
        owned.update(range(at-BASE,at-BASE+len(payload)))
    write(controller+6+21,bytes([208]),'Remove Gerhard from his original room21')
    write(controller+6+15,bytes([16]),'Assign Gerhard to existing First Mate room15')
    write(actor+16,struct.pack('<I',300000),'Disclosed XP qualification input')
    # Execute the original one-byte acquired-flag setter; copy only its proven
    # destination word back into the live fixture,not native CPU call scratch.
    before_native=bytes(cpu.mem_read(BASE,0x800000))
    get(0x4A204,(item,1))
    after_native=bytes(cpu.mem_read(BASE,0x800000))
    changed_native={i for i,(a,b) in enumerate(zip(before_native,after_native,strict=True)) if a!=b}
    assert changed_native=={item+17-BASE}
    write(item+17,bytes(cpu.mem_read(item+17,1)),'Original acquired bit for the regional proof item')
    targets=[]
    for target,value in ((0,1),(6,2)):
        other=company_root+4+target*76
        own_obj=company_root+4+own*76
        assert get(0x3CB30,(other,own))==0
        lower,upper=sorted((own,target))
        at=company_root+4+lower*76+0x1F+upper
        write(at,bytes([value]),f'Original symmetric relation field for factions{own}/{target}:state{value}')
        targets.append({'faction_ID':target,'name':name(other),'relation_state':value})
    cpu.mem_write(BASE,bytes(result))
    assert get(0x825E4,(controller,1))==16
    assert get(0x7E670,(actor,))==300000 and get(0x7DCC8,(actor,7))==215
    assert get(0x82EB0,(region,))==4
    for target,value in ((0,1),(6,2)):
        assert get(0x3CB30,(company_root+4+target*76,own))==value
        assert get(0x3CB30,(company_root+4+own*76,target))==value
    eligible=[]
    for mode,expected in enumerate((5,4,1,1,4,5)):
        count=get(0x5BB4C,(0,mode,0x02470000))
        ids=list(struct.unpack('<'+'I'*count,cpu.mem_read(0x02470000,count*4))) if count else []
        assert count==expected,(mode,count,ids)
        eligible.append({'type':mode,'count':count,'faction_IDs':ids})
    changed={i for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b}
    assert changed<=owned and len(changed)<=9
    return bytes(result),{'synthetic_diplomatic_qualification_fixture':True,'mode':request['mode'],
        'ARM9_sha256':sha(arm),'controller':controller,'actor':actor,'First_Mate':'Gerhard',
        'original_Speech_after':215,'regional_proof_item_ID':149,'regional_proof_item':"Cambyses' Crown",
        'relation_targets':targets,'all_six_original_target_filters':eligible,'source_defined_fields':fields,
        'changes':[{'address':BASE+i,'before':raw[i],'after':result[i]} for i in sorted(changed)],
        'all_other4MiB_bytes_exact':True,'money_location_calendar_ship_layout_code_and_menu_flags_unchanged':True,
        'earned_XP_assignment_proof_item_relations_or_outcomes_not_claimed':True,
        'original_source_spans':[{'offsets':[lo,hi],'sha256':sha(source[lo:hi])} for lo,hi in spans],
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result)}
