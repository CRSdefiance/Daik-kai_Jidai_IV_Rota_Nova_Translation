"""Execute original parent/VM tails with poisoned unowned cache bytes."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R8,UC_ARM_REG_R10,UC_ARM_REG_R11
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_lil_B141_research_v3554 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_termination_v3557b')
ACTIVE=0x02279668+0x54
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);spec=plan['blocks'][0];old_end,new_end=spec['source_logical_end'],spec['research_logical_end'];edge=next(e for e in spec['relative_skip_fixups'] if e['offset']==508)
    assert (old_end,new_end,edge['matched_skip_target'],edge['new_matched_skip_target'])==(974,898,970,894)
    cases=[]
    for label,path in [('clean',Path('work/clean.nds')),('current',PARENT),('research',ROM)]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[141];u=machine(arm);cache=STACK+0x10;begin=cache+8;logical_end=8+struct.unpack_from('<I',block,4)[0];physical_end=begin+len(block);reads=[];executed=set();phase=['setup']
        assert arm[0x23F4C:0x24134]==NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0x23F4C:0x24134]
        def code(cpu,pc,size,d):
            if 0x02000000<=pc and pc+size<=0x02000000+len(arm):assert bytes(cpu.mem_read(pc,size))==arm[pc-0x02000000:pc-0x02000000+size];executed.add(pc)
        def observe(cpu,a,at,size,value,d):
            if phase[0]=='tail' and begin<=at<begin+0x2400:reads.append(dict(PC=cpu.reg_read(UC_ARM_REG_PC),offset=at-begin,bytes=size,hex=bytes(cpu.mem_read(at,size)).hex()))
        hs=[u.hook_add(UC_HOOK_CODE,code),u.hook_add(UC_HOOK_MEM_READ,observe)]
        try:
            tails=[('insufficient_after_C200',edge['new_offset'] if label=='research' else 508),('funded_after_effects',next(c['new_offset'] for c in spec['command_map'] if c['old_offset']==966) if label=='research' else 966)]
            for name,offset in tails:
                for mode in [0,1]:
                    for previous in [0,1,2]:
                        phase[0]='setup';u.mem_write(STACK-0x100,b'\xA5'*0x2700);u.mem_write(cache,struct.pack('<2I',0x02134578,141));u.mem_write(begin,block);u.mem_write(ACTIVE,struct.pack('<I',1))
                        for r,v in [(UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP),(UC_ARM_REG_R0,cache),(UC_ARM_REG_R1,141),(UC_ARM_REG_R4,cache),(UC_ARM_REG_R5,0x021343E4),(UC_ARM_REG_R11,0x021345B0),(UC_ARM_REG_R10,0x02410010),(UC_ARM_REG_R8,mode)]:u.reg_write(r,v)
                        u.emu_start(0x02023F4C,0x0202405C,count=2000);assert u.reg_read(UC_ARM_REG_PC)==0x0202405C
                        sp=u.reg_read(UC_ARM_REG_SP);assert struct.unpack('<I',u.mem_read(sp+4,4))[0]==begin+8
                        # Declared private VM-tail input,not an event flag or gameplay fixture.
                        u.mem_write(sp+4,struct.pack('<I',begin+offset));u.reg_write(UC_ARM_REG_R8,previous);reads.clear();phase[0]='tail';u.emu_start(0x0202405C,0x02023F50,count=2000)
                        assert u.reg_read(UC_ARM_REG_PC)==0x02023F50 and u.reg_read(UC_ARM_REG_SP)==STACK
                        assert reads and all(r['offset']+r['bytes']<=logical_end for r in reads) and max(r['offset']+r['bytes'] for r in reads)==logical_end
                        assert bytes(u.mem_read(begin,len(block)))==block and bytes(u.mem_read(physical_end,32))==b'\xA5'*32
                        cases.append(dict(version=label,path=name,mode=mode,private_previous_result=previous,source_tail_offset=offset,logical_end=logical_end,in_block_terminator_offset=logical_end-4,payload_reads=reads.copy(),original_VM_returned_without_reading_alignment_or_unowned_cache_tail=True,whole_block_and_nonzero_tail_canaries_exact=True))
        finally:
            for h in hs:u.hook_del(h)
    assert len(cases)==36;ROOT.mkdir(parents=True)
    save(ROOT/'both_funding_paths_stop_at_in_block_terminator_nonzero_tail.json',dict(plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),cases=cases,source_insufficient_jump_target=970,target_insufficient_jump_target=894,source_logical_end=974,target_logical_end=898,prior_planning_zero_cache_tail_assumption_disproved_and_unnecessary=True,whole_loader_preserves_post_payload_canaries_instead_of_zeroing_them=True,all36_original_parent_VM_tail_cases_return_before_unowned_cache_bytes=True,private_cache_parent_and_tail_inputs_explicit_not_gameplay=True,original_VM_return_address=0x02023F50,outer_event_parent_continuation_not_executed=True,prior_harness_overran_VM_return_into_unsupplied_outer_event_context=True,no_UI_resource_or_scene_outcome_execution_claim=True,no_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('36 clean/current/relocated original VM tails terminate inside the block with poisoned cache tail intact;zero-tail assumption rejected.')
