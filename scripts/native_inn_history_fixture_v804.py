"""Original Inn history-event inputs; no code, text, selectors or outcomes patched."""

import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import inn_editorial_runtime as month_literals
from dk4tool.rom.nds import NdsImage
from scripts.native_inn_fixture_v803 import set_condition as assign
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read


def set_condition(arm,raw,request):
    cfg=read('translations/inn_editorial_release_v1.json')
    assert sha(arm)==cfg['target_arm9_sha256'] and len(raw)==0x400000
    assert set(request)=={'mode','event','won','months_ago'} and request['mode']=='Inn-history'
    event=request['event'];won=request['won'];months=request['months_ago']
    assert event in ('fleet','raid','town-defense') and type(won) is bool and type(months) is int and 0<=months<=11
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x5C5B0,0x5CB2C),(0x5CB3C,0x5CE94),(0x3A074,0x3A0C8),(0x7DAF0,0x7DB14),(0x3CCD0,0x3CD2C))
    assert all(arm[lo:hi]==source[lo:hi] for lo,hi in spans)
    assert struct.unpack_from('<4I',arm,0x5CB2C)==(month_literals.LAST_MONTH,month_literals.THIS_MONTH,month_literals.MONTHS_AGO,month_literals.MONTHS_AGO)
    after,assignment=assign(arm,raw,{'mode':'Inn-strategist'})
    u=machine(arm);u.mem_write(BASE,after)
    def get(fn,args=()):call(u,fn,args,instruction_limit=300000);return u.reg_read(UC_ARM_REG_R0)
    def ptr(p):return struct.unpack('<I',u.mem_read(p,4))[0]
    def text(p):return bytes(u.mem_read(p,256)).split(b'\0')[0]
    company_root=get(0xCB160);town_id=get(0xB65E4);town=get(0xB6618);region=get(0xB2B48,(town,))
    assert town_id==22 and region==1
    output=bytearray(after);owned={r['address'] for r in assignment['changes']};known=[]
    # Match precisely the original information-report eligibility checks, then
    # use its original knowledge setter to make these companies already known.
    for i in range(20):
        company=company_root+4+i*76
        if not get(ptr(ptr(company)+16)-BASE,(company,)):continue
        if get(0x3CC74,(company,region))<=0:continue
        leader=get(0x3CD2C,(company,))
        if not leader or get(ptr(ptr(leader)+0x30)-BASE,(leader,)) or get(0x7DB0C,(leader,))!=1:continue
        before=get(0x7DB0C,(leader,));get(0x7DAF0,(leader,2,1))
        assert get(0x7DB0C,(leader,))==2
        p=leader+0x1A;output[p-BASE]=bytes(u.mem_read(p,1))[0];owned.add(p)
        known.append(dict(company_ID=i,leader=leader,address=p,before=before,after=2,original_setter=BASE+0x7DAF0))
    assert get(0x5CB3C,(0,region))==0
    market=company_root+struct.unpack_from('<I',arm,0x5CE90)[0]+region*8
    assert bytes(u.mem_read(market+4,1))==b'\x15'
    history=company_root+struct.unpack_from('<I',arm,0x5CA7C)[0]
    for i in range(5):
        record=history+12*i
        assert get(0x3A074,(record,))==4 and bytes(u.mem_read(record+4,1))==b'\x15'
    calendar=get(0xCB1B4);now=get(0xCCA44,(calendar,));then=(now-months)%12
    assert 0<=now<12
    before=bytes(u.mem_read(history,12));record=bytearray(before)
    record[4]=1 if event=='fleet' else 0
    record[5]=21 if event=='raid' else 0
    record[6]=115 if event=='fleet' else town_id
    record[7]=(record[7]&~1)|int(won);record[8]=then
    output[history-BASE+4:history-BASE+9]=record[4:9];owned.update(range(history+4,history+9))
    u.mem_write(history,bytes(record))
    original_type=get(0x3A074,(history,));assert original_type=={'fleet':0,'raid':1,'town-defense':2}[event]
    if event=='fleet':assert get(0x3CCD0,(company_root+4+record[5]*76,))==region
    else:assert get(0xB2B48,(get(0xCB178)+4+record[6]*108,))==region
    expected_id=(1197 if won else 1198) if event=='raid' else (1195 if won else 1196)
    result=bytes(output)
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(r['address'] in owned for r in changes)
    # Execute the unchanged real dispatcher on a separate native copy. Only
    # presentation is intercepted; fixture output remains pre-consumption input.
    v=machine(arm);v.mem_write(BASE,result);observed=[]
    def speech(c,pc,size,unused):
        sp=c.reg_read(UC_ARM_REG_SP)
        pointers=[c.reg_read(UC_ARM_REG_R2),c.reg_read(UC_ARM_REG_R3),struct.unpack('<I',c.mem_read(sp,4))[0]]
        observed.append(dict(message=c.reg_read(UC_ARM_REG_R1),speaker=c.reg_read(UC_ARM_REG_R0),
            values_hex=[bytes(c.mem_read(p,128)).split(b'\0')[0].hex() for p in pointers]))
        c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    hook=v.hook_add(UC_HOOK_CODE,speech,begin=BASE+0x53FE4,end=BASE+0x53FE4)
    try:call(v,0x5CD5C,(0,),instruction_limit=500000)
    finally:v.hook_del(hook)
    assert len(observed)==1 and observed[0]['message']==expected_id
    assert bytes(v.mem_read(history+4,1))==b'\x15'
    month_text=bytes.fromhex(observed[0]['values_hex'][0])
    number=str(months).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')
    assert month_text==(b'This month' if months==0 else b'Last month' if months==1 else number+b' months ago')
    return result,dict(synthetic_Inn_history_input_fixture=True,mode=request['mode'],request=request,
        ARM9_sha256=sha(arm),original_assignment=assignment,already_known_company_inputs=known,
        history_record=history,source_history_hex=before.hex(),fixture_history_hex=bytes(record).hex(),
        original_history_type=original_type,original_current_month=now,event_month=then,
        original_current_region=region,original_report_priority_exhausted_by_known_inputs=True,
        original_dispatcher_preflight=observed,source_dispatcher_consumes_event_in_separate_preflight=True,
        preflight_not_actual_emulator_or_earned_history=True,changes=changes,all_other4MiB_RAM_bytes_exact=True,
        no_code_text_dialogue_selection_menu_flags_or_result_replacement=True,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result))
