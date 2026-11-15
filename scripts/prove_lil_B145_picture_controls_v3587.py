"""Bind three original picture descriptors and original hide boundary without executing resources."""
import struct,inspect
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B145_picture_controls_v3587')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
BASE=0x02000000
def picture(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan);word=command['word'];assert word in [0x4821,0x4822,0x4823,0x4700];stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+command['offset'],0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));calls=[]
    def boundary(u,pc,size,unused):
        args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];assert args[0]==0x02276F88
        if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None
        else:
            assert pc==BASE+0x28A64 and u.reg_read(UC_ARM_REG_LR)==BASE+0x2A0A0;operand=struct.unpack_from('<H',block,command['offset']+2)[0];desc=list(struct.unpack('<4I',u.mem_read(args[1],16)));layout=list(struct.unpack('<3I',u.mem_read(args[2],12)));assert desc==[(operand>>8)&3,operand&255,1,(operand>>11)&15] and layout==[(word>>4)&15,(word>>2)&3,word&3]
        calls.append(dict(address=pc,args=args,descriptor=desc,layout=layout,original_return_address=u.reg_read(UC_ARM_REG_LR),resource_body_unexecuted=True));u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hs=[cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+p,end=BASE+p) for p in [0x28A64,0x28A8C]]
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=500000)
    finally:
        for h in hs:cpu.hook_del(h)
    values=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];assert len(calls)==1 and values==[3,0,0,0,0,0] and extent==command['native_extent']==(2 if word==0x4700 else 4);assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,len(block)))==block
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(source_offset=command['offset'],source_command_hex=command['whole_command_hex'],native_result=values,native_extent=extent,original_picture_boundary_calls=calls,all4MiB_owner_input_ABI_output_and_length_guards_exact=True,resource_body_and_selected_scene_unexecuted=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);g=next(g for g in packet['blocks'] if g['block']==145);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for version,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        block=IlnkContainer.parse(NdsImage.open(path).read_file('/data/SC2.DK4')).blocks[145]
        for c in g['all_current_native_commands']:
            if c['word'] in [0x4821,0x4822,0x4823,0x4700]:cases.append(dict(version=version,**ctx.execute(picture,block,c)));ctx.machines.pop()
    assert len(cases)==8 and not ctx.machines
    for a,b in zip(cases[:4],cases[4:],strict=True):assert a['original_picture_boundary_calls']==b['original_picture_boundary_calls'] and a['source_command_hex']==b['source_command_hex']
    save(ROOT/'three_original_item_picture_descriptors_and_hide_eight_cases.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,item_descriptors=[175,182,156],source_control_operand_layout_bits_preserved=True,source_owned_adapter=inspect.getsource(picture),all_resource_bodies_explicit_unexecuted=True,not_actual_picture_gameplay_or_earned_inventory_or_graphics_repair=True,other_A000_effects_require_exact_source_byte_preservation_not_invented_semantics=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Eight source/current482x/4700 cases pass;item descriptors175/182/156 and hide boundary exact. Resource bodies unexecuted.')
