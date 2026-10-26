"""Bind eight original/relocated in-block end commands with poisoned unread post-payload guards."""
import struct,inspect
from pathlib import Path
from unicorn import UC_HOOK_MEM_READ
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.prepare_lil_B142_B145_research_v3597 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_ends_v3604')
BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);cases=[];bounds=[]
    for label,path in [('current',PARENT),('research',ROM)]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;cpu=machine(arm)
        for b in plan['blocks']:
            n=b['block'];block=blocks[n];logical_end=8+struct.unpack_from('<H',block,4)[0];end=next(c for c in b['command_map'] if c['word']==0);at=end['old_offset'] if label=='current' else end['new_offset'];assert at+4==logical_end and block[at:at+4]==bytes(4);stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100;cpu.mem_write(stream-16,b'\xA5'*(len(block)+64));cpu.mem_write(stream,block[:logical_end]);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+at,0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));reads=[];h=cpu.hook_add(UC_HOOK_MEM_READ,lambda u,a,p,s,v,d:reads.append(dict(address=p,size=s)),begin=stream+logical_end,end=stream+logical_end+31)
            try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=100000)
            finally:cpu.hook_del(h)
            values=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];assert values==[0,0,0,0,0,0] and extent==4 and not reads and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,logical_end))==block[:logical_end] and bytes(cpu.mem_read(stream+logical_end,32))==b'\xA5'*32
            for p in [stream-16,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
            cases.append(dict(version=label,block=n,end_offset=at,logical_end=logical_end,end_hex='00000000',native_result=values,native_extent=extent,post_logical_payload_guard_byte=0xA5,post_logical_payload_reads=reads,all4MiB_owner_input_ABI_result_and_length_guards_exact=True))
    for b in plan['blocks']:
        native_boundaries={c['new_offset'] for c in b['command_map']};assert all(e['new_matched_skip_target'] in native_boundaries and e['new_unmatched_next'] in native_boundaries for e in b['relative_skip_fixups']);bounds.append(dict(block=b['block'],all_relative_destinations_are_in_block_commands_not_logical_end=True,source_end=next(c['old_offset'] for c in b['command_map'] if c['word']==0),target_end=next(c['new_offset'] for c in b['command_map'] if c['word']==0)))
    assert len(cases)==8;ROOT.mkdir(parents=True);save(ROOT/'eight_end_decodes_and_all25_in_block_relative_destinations.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_plan=str(PLAN),source_plan_sha256=sha(PLAN.read_bytes()),cases=cases,branch_destination_bounds=bounds,all8_original_end_decodes_return_type0_extent4_without_post_payload_read=True,no_end_decode_zero_tail_dependency=True,no_relative_destination_at_or_beyond_logical_end=True,full_VM_or_outer_event_parent_tail_not_executed_by_this_probe=True,actual_B22_fixture_end_class_normal_exit_bound_separately=True,no_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Eight source/target end commands return0/extent4 with nonzero unread post-payload canaries;all25branch sites stay at in-block commands. Decoder scope,not full VM claim.')
