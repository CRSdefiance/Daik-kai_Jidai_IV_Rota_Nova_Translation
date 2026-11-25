"""Source-bound million-gold predicate and900000 payment on isolated copied contexts."""
import inspect,struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_funds_v3537')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
BASE=0x02000000
def finance(arm,common,raw,plan,target=None):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(BASE,0x400000));table=get(0xCB160);index=get(0x397D8,table);assert get(0x7F244)==2 and index==1;force=table+4+index*0x4C;funds=get(0x3CCC8,force)
    vt=struct.unpack('<I',cpu.mem_read(force,4))[0];ti=struct.unpack('<I',cpu.mem_read(vt-4,4))[0];name=struct.unpack('<I',cpu.mem_read(ti+4,4))[0];assert bytes(cpu.mem_read(name,32)).split(b'\0')[0]==b'6CForce'
    assert arm[0x3CCC8:0x3CCD0]==bytes.fromhex('0c0090e51eff2fe1') and struct.unpack_from('<I',before,force+12-BASE)[0]==funds
    if target is not None:get(0x3CC80,force,target-funds);assert get(0x3CCC8,force)==target
    after=bytes(cpu.mem_read(BASE,0x400000));changed=[BASE+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b];assert all(force+12<=i<force+16 for i in changed)
    return dict(raw_after=after,selected_company=index,source_CForce=force,funds_field=force+12,before_funds=funds,target_funds=target if target is not None else funds,source_RTTI='6CForce',only_source_owned_one_funds_word_changed=True,changed_byte_addresses=changed,before_RAM_sha256=sha(before),after_RAM_sha256=sha(after),fixture_is_offline_unit_input_not_earned_funds_or_event_progression=True)
def payment(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan);table=get(0xCB160);assert get(0x397D8,table)==1;force=table+4+76;old=get(0x3CCC8,force);scratch=0x02279600
    stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+command['offset'],0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));writes=[]
    h=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,at,size,val,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=at,size=size,value=val)),begin=BASE,end=BASE+0x3FFFFF)
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=500000)
    finally:cpu.hook_del(h)
    values=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];new=get(0x3CCC8,force);assert command['whole_command_hex']=='00a0ffffbdff0191' and extent==8 and values==[3,0,0,0,0,0] and new==max(0,old-900000)
    after=bytes(cpu.mem_read(BASE,0x400000));allowed={*range(force+12,force+16),*range(scratch,scratch+4)};changed=[BASE+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b];assert all(at in allowed for at in changed) and all(set(range(w['address'],w['address']+w['size']))<=allowed for w in writes)
    fixed=bytearray(after);fixed[force+12-BASE:force+16-BASE]=before[force+12-BASE:force+16-BASE];fixed[scratch-BASE:scratch-BASE+4]=before[scratch-BASE:scratch-BASE+4];assert fixed==before
    cpu.mem_write(scratch,before[scratch-BASE:scratch-BASE+4]);assert bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,len(block)))==block
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(source_command_hex=command['whole_command_hex'],source_offset=command['offset'],native_result=values,native_extent=extent,before_funds=old,after_funds=new,payment_delta=new-old,source_CForce=force,source_funds_address=force+12,original_main_RAM_writes=writes,only_source_owned_money_and_decoder_unaligned_scratch_changed=True,all_other4MiB_actor_roster_event_RNG_models_ABI_input_owner_and_output_guards_exact=True,decoder_scratch_restored=True,current_executed_instruction_addresses=len(provider.executed_current),not_a_live_event_or_earned_payment=True)
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[141];commands=packet['blocks'][0]['all_current_native_commands'];condition=next(c for c in commands if c['whole_command_hex']=='0080ffff0e0001a1');pay=next(c for c in commands if c['whole_command_hex']=='00a0ffffbdff0191')
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B141_voices_v3533/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');identity=ctx.execute(finance);ctx.machines.pop();assert identity.pop('raw_after')==ctx.raw;cases=[]
    for funds in [0,899999,900000,999999,1000000,1000001,2000000]:
        fixture=ctx.execute(finance,funds);ctx.machines.pop();raw=fixture.pop('raw_after');pred=ctx.execute(probe,block,condition,raw=raw);ctx.machines.pop();expected=0 if funds<1000000 else 1 if funds==1000000 else 2;assert pred['native_result']==[2,expected,0,0,0,0]
        effect=ctx.execute(payment,block,pay,raw=raw);ctx.machines.pop();cases.append(dict(input_funds=funds,offline_fixture=fixture,source_predicate=pred,source_payment=effect,low_funds_payment_is_isolated_decoder_case_not_claimed_reachable_path=funds<1000000))
    assert not ctx.machines
    save(ROOT/'source_million_threshold_and900000_payment_seven_boundary_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),original_selected_Lil_company_money_identity=identity,cases=cases,source_predicate_word='0080ffff0e0001a1',source_payment_word='00a0ffffbdff0191',source_threshold_gold=1000000,source_payment_gold=900000,all_tests_are_copied_offline_native_contexts_not_gameplay_or_earned_progression=True,all_code_executed_current_ROM_exact=True,no_shared_helper_or_production_RAM_ROM_registry_ledger_change=True,portable_source_owned_adapters=dict(finance=inspect.getsource(finance),payment=inspect.getsource(payment)),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_threshold=1000000,source_payment=900000,boundary_cases=7,actual_historical_funds=identity['before_funds'],gameplay=False,credit=0))
