"""Decode both declared endwords per image,including both B156 words."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_READ
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.prepare_lil_B156_research_v3724 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B156_ends_v3729')
BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);cases=[];bounds=[]
    for label,path in [('current',PARENT),('research',ROM)]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;cpu=machine(arm)
        for b in plan['blocks']:
            n=b['block'];block=blocks[n];logical_end=8+struct.unpack_from('<H',block,4)[0];ends=[c for c in b['command_map'] if c['word']==0];assert len(ends)==(2 if n==156 else 1)
            for index,end in enumerate(ends):
                at=end['old_offset'] if label=='current' else end['new_offset'];assert block[at:at+4]==bytes(4) and at+4<=logical_end
                if index==len(ends)-1:assert at+4==logical_end
                stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100;cpu.mem_write(stream-16,b'\xA5'*(len(block)+64));cpu.mem_write(stream,block[:logical_end]);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+at,0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));reads=[];h=cpu.hook_add(UC_HOOK_MEM_READ,lambda u,a,p,s,v,d:reads.append(dict(address=p,size=s)),begin=stream+logical_end,end=stream+logical_end+31)
                try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=100000)
                finally:cpu.hook_del(h)
                values=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];assert values==[0,0,0,0,0,0] and extent==4 and not reads and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,logical_end))==block[:logical_end] and bytes(cpu.mem_read(stream+logical_end,32))==b'\xA5'*32
                for p in [stream-16,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
                cases.append(dict(version=label,block=n,declared_end_index=index,end_offset=at,logical_end=logical_end,at_logical_tail=at+4==logical_end,end_hex='00000000',native_result=values,native_extent=extent,post_logical_payload_guard_byte=165,post_logical_payload_reads=reads,all4MiB_owner_input_ABI_result_and_length_guards_exact=True))
    for b in plan['blocks']:
        boundary={c['new_offset'] for c in b['command_map']};assert all(e['new_matched_skip_target'] in boundary and e['new_unmatched_next'] in boundary for e in b['relative_skip_fixups']);bounds.append(dict(block=b['block'],all_relative_destinations_are_in_block_commands_not_logical_end=True,declared_end_word_maps=b['original_declared_end_word_maps']))
    assert len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2;ROOT.mkdir(parents=True);save(ROOT/'four_declared_end_decodes_and_all12_in_block_relative_destinations.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_plan=str(PLAN),source_plan_sha256=sha(PLAN.read_bytes()),cases=cases,branch_destination_bounds=bounds,all4_declared_end_decodes_return_type0_extent4_without_post_payload_read=True,B156_first_end_precedes_second_end_and_declared_logical_end=True,no_end_decode_zero_tail_dependency=True,no_relative_destination_at_or_beyond_logical_end=True,second_B156_declared_word_decoder_probe_not_actual_reachability_claim=True,full_VM_or_outer_event_parent_tail_not_executed_by_this_probe=True,no_ROM_registry_ledger_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Four declared current/target endwords pass with poisoned unread post-payload guards;B156 bothwords preserved. Decoder scope,not reachability/fullVM.')
