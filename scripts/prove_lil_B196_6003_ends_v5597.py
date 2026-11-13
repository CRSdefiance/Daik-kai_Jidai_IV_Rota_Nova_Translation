"""Bind the actual6003 boundary and every original end without an effect claim."""
import inspect,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_6003_ends_v5597')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
BASE=0x02000000

def command6003(arm,common,raw,plan,previous,boundary_return):
    cpu,get,provider=machine(arm,common,raw,plan)
    stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100;value=bytes.fromhex('0360')
    assert struct.unpack_from('<I',arm,0x29A9C)[0]==0x02386EFC
    cpu.mem_write(stream-16,b'\xA5'*34);cpu.mem_write(stream,value)
    cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));guard=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24))
    cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));calls=[]
    def boundary(u,pc,size,unused):
        assert [u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1)]==[0x02386EFC,3]
        assert u.reg_read(UC_ARM_REG_LR)==BASE+0x29A10
        calls.append(dict(address=pc,owned_first_two_arguments=[0x02386EFC,3],source_return_address=u.reg_read(UC_ARM_REG_LR),
            remaining_argument_registers_not_assigned_semantic_meaning=True,callee_body_unexecuted=True))
        u.reg_write(UC_ARM_REG_R0,boundary_return);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    h=cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+0x1097DC,end=BASE+0x1097DC)
    try:call(cpu,0x2A510,(result,owner,length,previous))
    finally:cpu.hook_del(h)
    decoded=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
    assert len(calls)==1 and decoded==[3,0,0,0,0,0] and extent==2
    assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,2))==value
    for at in [stream-16,stream+2,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(previous_result=previous,incidental_boundary_return=boundary_return,native_result=decoded,native_extent=extent,
        source_command_hex=value.hex(),original_boundary_calls=calls,all4MiB_owner_input_ABI_output_and_length_guards_exact=True,
        current_executed_instruction_addresses=len(provider.executed_current),not_audio_UI_item_money_effect_or_actual_gameplay_proof=True)

def end_case(arm,block,offset,previous):
    cpu=machine(arm);stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    value=block[offset:offset+4];assert value==bytes(4)
    cpu.mem_write(stream-16,b'\xA5'*36);cpu.mem_write(stream,value)
    cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));guard=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24))
    cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));reads=[]
    def source_read(u,access,address,size,value,unused):
        assert stream<=address and address+size<=stream+4
        reads.append(dict(relative_offset=address-stream,bytes=size))
    h=cpu.hook_add(UC_HOOK_MEM_READ,source_read,begin=stream-16,end=stream+19)
    try:call(cpu,0x2A510,(result,owner,length,previous))
    finally:cpu.hook_del(h)
    decoded=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
    assert decoded==[0,0,0,0,0,0] and extent==4 and reads
    assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,4))==value
    for at in [stream-16,stream+4,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(source_offset=offset,source_command_hex=value.hex(),previous_result=previous,native_result=decoded,native_extent=extent,
        source_operand_reads=reads,no_leading_or_post_four_byte_payload_read=True,all4MiB_owner_input_ABI_output_and_length_guards_exact=True,
        parser_end_contract_not_actual_branch_selection_or_full_VM_execution=True)

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[196] for im in images]
    commands=packet['blocks'][0]['all_current_native_commands'];ends=[c['offset'] for c in commands if c['word']==0]
    assert ends==[364,694,938,1266,1464,1708,1810]
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']==0x6003]==[(298,'0360')]
    arms=[im.read_file('/__arm9__.bin') for im in images];spans=[(0x299C8,0x29AA0),(0x1097DC,0x1097F0),(0x2A510,0x2A600)]
    assert all(arms[0][a:b]==arms[1][a:b] for a,b in spans)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B196_voices_v5591/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    cases=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for returned in [0,0xFFFFFFFF]:cases.append(ctx.execute(command6003,previous,returned));ctx.machines.pop()
    guarded=[]
    for version,arm,block in zip(['clean','current'],arms,blocks,strict=True):
        for offset in ends:
            for previous in [0,1,2,3,0xFFFFFFFF]:guarded.append(dict(version=version,**end_case(arm,block,offset,previous)))
    assert len(cases)==10 and len(guarded)==70 and not ctx.machines
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);disassembly=[]
    for a,b in spans:
        disassembly.extend(f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in decoder.disasm(arms[1][a:b],BASE+a))
    text=ROOT/'source_exact_6003_and_end_handler_spans.txt';text.write_text('\n'.join(disassembly)+'\n',encoding='utf-8')
    save(ROOT/'source6003_ten_boundary_cases_and_seventy_guarded_end_cases.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source6003_offset=298,source6003_command_hex='0360',source6003_cases=cases,source_declared_end_offsets=ends,source_end_cases=guarded,
        source6003_owned_two_arguments_and_original_callee_return_site_bound=True,source6003_callee_effect_semantics_and_body_unexecuted=True,
        all_seven_end_sites_both_images_five_prior_results_exact=True,all_end_payload_reads_within_four_bytes=True,
        source_bound_handler_spans=[dict(start=a,end=b,sha256=sha(arms[1][a:b])) for a,b in spans],
        source_owned_adapters=dict(command6003=inspect.getsource(command6003),end=inspect.getsource(end_case)),
        disassembly=str(text),disassembly_sha256=sha(text.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_choice_selection_branch_reachability_funds_item_and_stat_outcomes_not_proved=True,
        new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B1966003 original first-two-argument boundary:10 cases. All seven end sites:70 guarded source/current cases. Bodies/branch selection/funds/item/stat gameplay unexecuted.')
