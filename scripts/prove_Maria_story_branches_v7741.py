"""Source/current exact native relative spans, all five structural previous-result inputs."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_branches_v7741')
SOURCE=Path('work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json')
CURRENT=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
PRECEDENT=Path('scripts/prove_lil_B167_branches_v4122.py')
def native_skip(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan)
    owner,stream,result,length=0x02650000,0x02660000,0x02668000,0x02668100
    at,word=command['offset'],command['word'];span=struct.unpack_from('<H',block,at+2)[0]
    assert word in [0x100,0x200,0x300,0x400]
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block)
    before=bytes(cpu.mem_read(0x02000000,0x400000));cases=[]
    for last in [0,1,2,3,0xFFFFFFFF]:
        cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+at,0,0));owned=bytes(cpu.mem_read(owner-16,64))
        cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4))
        call(cpu,0x2A510,(result,owner,length,last))
        extent=struct.unpack('<I',cpu.mem_read(length,4))[0]
        taken=word==0x100 or word==0x200 and last==0 or word==0x300 and last==1 or word==0x400 and last==2
        assert extent==4+(span if taken else 0) and struct.unpack('<6I',cpu.mem_read(result,24))==(3,0,0,0,0,0)
        assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,len(block)))==block
        for address in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(address,16))==b'\xA5'*16
        cases.append(dict(previous_result_structural_argument=last,taken=taken,native_extent=extent,next_offset=at+extent,
            all4MiB_ABI_owner_input_output_andcanary_guards_exact=True))
    return dict(offset=at,word=word,span=span,cases=cases,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();source,current=map(read,[SOURCE,CURRENT]);image=NdsImage.open(current['current_ROM'])
    arm=image.read_file('/__arm9__.bin');clean=NdsImage.open(source['source_ROM']).read_file('/__arm9__.bin')
    spans=[(0x2A414,0x2A530),(0x24048,0x24118)];assert all(arm[a:b]==clean[a:b] for a,b in spans)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');groups=[];edges=[]
    for sg,cg in zip(source['groups'],current['groups'],strict=True):
        assert sg['block']==cg['block'];versions=[]
        for label,spec,blockhex,commands in [('clean-Japanese',sg,'clean_block_hex',sg['commands']),('current-English',cg,'current_block_hex',cg['all_current_commands'])]:
            block=bytes.fromhex(spec[blockhex]);logical=8+struct.unpack_from('<H',block,4)[0];boundaries={c['offset'] for c in commands}|{logical};results=[]
            for command in commands:
                if command['word'] not in [0x100,0x200,0x300,0x400]:continue
                at=command['offset'];span=struct.unpack_from('<H',block,at+2)[0]
                assert at+4 in boundaries and at+4+span in boundaries
                result=ctx.execute(native_skip,block,command);ctx.machines.pop()
                assert all(r['next_offset'] in boundaries for r in result['cases']);results.append(result)
                if label=='current-English':edges.append(dict(block=sg['block'],offset=at,word=command['word'],span_field_offset=at+2,
                    source_span=span,unmatched_next_offset=at+4,matched_skip_target=at+4+span,ancestor_0100_offsets=command['ancestor_0100_offsets']))
            versions.append(dict(version=label,block_sha256=sha(block),results=results))
        groups.append(dict(block=sg['block'],versions=versions))
    assert len(edges)==20 and not ctx.machines
    save(ROOT/'20_relative_sites200_guarded_original_source_current_cases.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],groups=groups,operands_requiring_adjustment_when_resizing=edges,
        native_cases=200,relative_span_base_is_command_plus4=True,source_owned_current_handler_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_owned_probe=inspect.getsource(native_skip),probe_precedent=str(PRECEDENT),probe_precedent_sha256=sha(PRECEDENT.read_bytes()),
        complete_nested0100_and0200_0300_branch_targets_are_mapped_native_boundaries=True,
        structural_previous_result_arguments_not_actual_condition_orstory_flag_forcing=True,no_natural_branch_reachability_orwhole_scene_claim=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,INPUT,PRECEDENT,Path(__file__)]},full_goal_complete=False))
    print('20exact relative sites/200 source-current native cases:all five structural result inputs preserve targets,ABI,all4MiB andcanaries.No natural branch claim.')
