"""Bind C200's original UI request with explicit unexecuted resource-body boundaries."""
import inspect,struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000
ROOT=Path('work/analysis/lil_B139_C200_v3461e')
SOURCE=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')

def C200(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan);stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    ui=struct.unpack_from('<I',arm,0x2975C)[0];ui2=struct.unpack_from('<I',arm,0x29760)[0];assert ui==0x02276F88 and ui2==ui+0x2000
    request,flag=ui2+0x438,ui2+0x470
    assert command['whole_command_hex']=='00c2' and command['native_extent']==2
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block)
    cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+command['offset'],0,0));owned=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4))
    before=bytes(cpu.mem_read(BASE,0x400000));calls=[];descriptors=[];writes=[];hs=[]
    def entry(u,pc,size,unused):
        obj,desc=u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1);assert obj==ui
        descriptors.append(dict(address=pc,UI_owner=obj,descriptor=desc,words=list(struct.unpack('<8I',u.mem_read(desc,32)))))
    def resource_boundary(u,pc,size,unused):
        calls.append(dict(address=pc,args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]],kind='explicit-unexecuted-native-presentation-resource-body'))
        u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    def write(u,access,address,size,value,unused):writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value))
    hs.append(cpu.hook_add(UC_HOOK_CODE,entry,begin=BASE+0x21B80,end=BASE+0x21B80))
    for pc in [0x28BAC,0x28A8C]:hs.append(cpu.hook_add(UC_HOOK_CODE,resource_boundary,begin=BASE+pc,end=BASE+pc))
    hs.append(cpu.hook_add(UC_HOOK_MEM_WRITE,write,begin=request,end=flag+3))
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=500000)
    finally:
        for h in hs:cpu.hook_del(h)
    assert len(descriptors)==1 and [c['address'] for c in calls]==[BASE+0x28BAC,BASE+0x28A8C]
    descriptor=descriptors[0]['words'];assert descriptor[1]==1 and descriptor[3]==13 and descriptor[7]==0
    assert calls[0]['args'][:3]==[ui,descriptor[2],13] and calls[1]['args'][0]==ui
    expected_words=[descriptor[1],descriptor[2],descriptor[3],descriptor[4],descriptor[5],descriptor[6],1]
    expected_writes=[dict(PC=BASE+pc,address=request+4*i,size=4,value=v) for i,(pc,v) in enumerate(zip([0x21BCC,0x21BD8,0x21BE0,0x21BE8,0x21BF0,0x21BF8,0x21C00],descriptor[1:8],strict=True))]
    expected_writes[-1]['PC']=BASE+0x21C00
    # The mode descriptor copies its zero final field,then marks the request pending.
    expected_writes.append(dict(PC=BASE+0x21C04,address=request+24,size=4,value=1))
    expected_writes.append(dict(PC=BASE+0x294C8,address=flag,size=4,value=1))
    assert writes==expected_writes,(writes,expected_writes)
    assert list(struct.unpack('<7I',cpu.mem_read(request,28)))==expected_words and struct.unpack('<I',cpu.mem_read(flag,4))[0]==1
    values=struct.unpack('<6I',cpu.mem_read(result,24));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];assert values==(3,0,0,0,0,0) and extent==2
    after=bytes(cpu.mem_read(BASE,0x400000));unowned=bytearray(after)
    for at,size in [(request,28),(flag,4)]:unowned[at-BASE:at-BASE+size]=before[at-BASE:at-BASE+size]
    assert unowned==before and bytes(cpu.mem_read(stream,len(block)))==block and bytes(cpu.mem_read(owner-16,64))==owned
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(offset=command['offset'],source_command_hex=command['whole_command_hex'],native_result=list(values),native_extent=extent,original_UI_descriptor=descriptors[0],resource_boundaries=calls,source_owned_UI_request_words=expected_words,source_owned_UI_writes=writes,source_owned_UI_spans=[dict(address=request,bytes=28),dict(address=flag,bytes=4)],all_other4MiB_actor_roster_event_RNG_and_models_exact=True,original_input_owner_guards_and_ABI_exact=True,resource_call_returns_are_unused_by_original_continuation=True,native_presentation_resource_bodies_not_executed=True,actual_scene_transition_not_observed=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');history=NdsImage.open(packet['historical_snapshot_ROM']).read_file('/__arm9__.bin')
    spans=[(0x29434,0x294D8),(0x21B80,0x21C14),(0x904BC,0x904F4)]
    assert all(arm[a:b]==clean[a:b]==history[a:b] for a,b in spans)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B139_B140_voices_v3460/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[139]
    command=next(c for b in packet['blocks'] if b['block']==139 for c in b['all_current_native_commands'] if c['word']==0xC200)
    result=ctx.execute(C200,block,command);ctx.machines.pop();assert not ctx.machines
    save(ROOT/'source_C200_UI_request_contract.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),block=139,cases=[result],source_code_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],source_owned_adapter=inspect.getsource(C200),previous_hardware_boundary_diagnostic='work/analysis/lil_B139_C200_diagnostic_v3461b/first_invalid_read.json',no_event_role_roster_or_gameplay_state_fixture=True,actual_selected_B139_IDs=[],new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_C200_result=result['native_result'],extent=2,UI_request_words=result['source_owned_UI_request_words'],owned_UI_writes=len(result['source_owned_UI_writes']),other4MiB_exact=True,resource_bodies_unexecuted=True,actual_scene_transition=False,new_credit=0))
