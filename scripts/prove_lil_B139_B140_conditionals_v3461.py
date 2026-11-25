"""Bind twelve raw predicates,query129 and the sourceC200 parser contract."""
import inspect,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_B140_conditionals_v3461')
SOURCE=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
INPUT=Path('work/analysis/lil_B139_B140_voices_v3460/current_native_input.json')
BASE=0x02000000

def probe(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan)
    stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block)
    cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+command['offset'],0,0));guard=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4))
    before=bytes(cpu.mem_read(BASE,0x400000));calls=[];writes=[];scratch=0x02279600
    def trace(u,pc,size,unused):calls.append(dict(address=pc,args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]))
    h=cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x23840,end=BASE+0x23840)
    wh=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,access,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=scratch,end=scratch+3)
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=500000)
    finally:cpu.hook_del(h);cpu.hook_del(wh)
    values=struct.unpack('<6I',cpu.mem_read(result,24));extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
    assert extent==command['native_extent'] and command['word'] in [0x8000,0x8100,0xC200]
    if command['word'] in [0x8000,0x8100]:assert values[0]==2
    if command['word']==0x8100:assert values[1] in [0,1]
    if command['word']==0xC200:assert values== (3,0,0,0,0,0) and extent==2 and command['whole_command_hex']=='00c2'
    after=bytes(cpu.mem_read(BASE,0x400000));operand=stream+command['offset']+4;expected_write=command['word']==0x8000 and operand%4!=0
    assert struct.unpack_from('<I',arm,0x2A5E8)[0]==scratch and arm[0x2A5D8:0x2A5DC]==bytes.fromhex('000081e5')
    expected=[dict(PC=BASE+0x2A5D8,address=scratch,size=4,value=int.from_bytes(block[command['offset']+4:command['offset']+8],'little'))] if expected_write else []
    assert writes==expected
    unowned=bytearray(after);unowned[scratch-BASE:scratch-BASE+4]=before[scratch-BASE:scratch-BASE+4];assert unowned==before
    cpu.mem_write(scratch,before[scratch-BASE:scratch-BASE+4]);assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(stream,len(block)))==block and bytes(cpu.mem_read(owner-16,64))==guard
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(offset=command['offset'],word=command['word'],source_command_hex=command['whole_command_hex'],native_result=list(values),native_extent=extent,original_event_completion_calls=calls,original_unaligned_operand_read_scratch_writes=writes,source_owned_scratch_address=scratch,sole_scratch_restore_recovers_all4MiB_exact=True,current_executed_instruction_addresses=len(provider.executed_current),all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact=True,no_predicate_or_event_flag_forced=True)

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');history=NdsImage.open(packet['historical_snapshot_ROM']).read_file('/__arm9__.bin')
    spans=[(0x29874,0x299C8),(0x293B8,0x2976C),(0x2A510,0x2A600),(0x23840,0x23A28)]
    assert all(arm[a:b]==clean[a:b]==history[a:b] for a,b in spans)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;cases=[];queries=[];controls=[]
    for b in packet['blocks']:
        for c in b['all_current_native_commands']:
            if c['word'] not in [0x8000,0x8100,0xC200]:continue
            source=next(p for p in b['all_clean_native_commands'] if p['offset']==c['offset']);assert source['whole_command_hex']==c['whole_command_hex']
            result=ctx.execute(probe,blocks[b['block']],c);ctx.machines.pop();row=dict(block=b['block'],**result)
            if c['word']==0x8100:
                expected=int.from_bytes(bytes.fromhex(c['whole_command_hex'])[2:4],'little');assert expected==129 and len(result['original_event_completion_calls'])==1 and result['original_event_completion_calls'][0]['args'][1]==129;queries.append(row)
            else:assert result['original_event_completion_calls']==[]
            (controls if c['word']==0xC200 else cases).append(row)
    assert len(cases)==13 and sum(c['word']==0x8000 for c in cases)==12 and len(queries)==len(controls)==1 and not ctx.machines
    constants={}
    for c in cases:
        if c['source_command_hex'] in constants:assert constants[c['source_command_hex']]==c['native_result'][1]
        constants[c['source_command_hex']]=c['native_result'][1]
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);out=[]
    for a,b in spans:out.extend(f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in decoder.disasm(arm[a:b],BASE+a))
    p=ROOT/'source_exact_native_handlers.txt';p.write_text('\n'.join(out)+'\n',encoding='utf-8')
    save(ROOT/'source13_conditionals_and_C200_contract.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),conditional_cases=cases,original_event_queries=queries,source_C200_cases=controls,scoped_expected_unforced_results=constants,source_8000_raw_evaluator_result_not_assumed_boolean=True,source_8100_normalizes_event129_query_to_boolean=True,C200_original_two_byte_parser_result3_and_no_unowned_RAM_change_verified=True,C200_semantic_plot_effect_not_invented_and_no_actual_scene_transition_claim=True,source_handler_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],disassembly=str(p),disassembly_sha256=sha(p.read_bytes()),source_owned_probe=inspect.getsource(probe),native_input=str(INPUT),native_input_sha256=sha(INPUT.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_gameplay_state_fixtures_or_source_changes=True,actual_selected_B139_B140_IDs=[],new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(conditional_cases=len(cases),predicates=12,event_query=129,C200_cases=1,C200_result=controls[0]['native_result'],source_results=constants,no_unowned_RAM_change=True,new_credit=0))
