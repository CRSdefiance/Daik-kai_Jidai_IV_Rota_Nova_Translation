"""Bind both source C200 sites and the tail end to all five prior-result values."""
from pathlib import Path
import struct
from scripts.prove_lil_B190_C200_v5318 import C200,adapter_source
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B194_carried_result_v5495c')
SOURCE=Path('work/analysis/lil_B194_source_v5489/all11_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    text=checked_text(adapter_source(),{
        'def current_C200(arm,common,raw,plan,block,command):':'def prior_C200(arm,common,raw,plan,block,command,prior):',
        'cpu.mem_write(result,bytes(24))':"cpu.mem_write(result,struct.pack('<6I',0,prior,0,0,0,0))",
        '(result,owner,length,0)':'(result,owner,length,prior)','values==(3,0,0,0,0,0)':'values==(3,prior,0,0,0,0)'})
    env=dict(C200.__globals__);exec(compile(text,__file__+'::two-source-C200-prior-result','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B194_voices_v5490/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    uis=[];ends=[]
    for label,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        image=NdsImage.open(path);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[194]
        for command in [c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0xC200]:
            for prior in [0,1,2,3,0xFFFFFFFF]:
                result=ctx.execute(env['prior_C200'],block,command,prior);ctx.machines.pop();assert result['native_result']==[3,prior,0,0,0,0]
                uis.append(dict(version=label,source_offset=command['offset'],prior_result=prior,case=result))
        for prior in [0,1,2,3,0xFFFFFFFF]:
            cpu=machine(image.read_file('/__arm9__.bin'));stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
            assert 8+struct.unpack_from('<H',block,4)[0]==len(block)==540 and block[536:]==bytes(4)
            cpu.mem_write(stream-16,b'\xa5'*(len(block)+48));cpu.mem_write(stream,block)
            cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+536,0,0));guard=bytes(cpu.mem_read(owner-16,64))
            cpu.mem_write(result-16,b'\xa5'*80);cpu.mem_write(result,struct.pack('<6I',0,prior,0,0,0,0))
            cpu.mem_write(length-16,b'\xa5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(0x02000000,0x400000))
            call(cpu,0x2A510,(result,owner,length,prior));values=list(struct.unpack('<6I',cpu.mem_read(result,24)))
            assert values==[0,prior,0,0,0,0] and struct.unpack('<I',cpu.mem_read(length,4))[0]==4
            assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,len(block)))==block
            for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
            ends.append(dict(version=label,end_offset=536,prior_result=prior,native_result=values,native_extent=4,all4MiB_owner_payload_and_ABI_guards_exact=True))
    assert len(uis)==20 and len(ends)==10 and not ctx.machines
    save(ROOT/'all20_C200_and10_end_prior_result_cases.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),C200_cases=uis,end_cases=ends,
        source_C200_offsets=[494,534],source_end_offset=536,source_owned_C200_adapter=text,all_five_prior_result_values_preserved_at_both_C200_and_end=True,
        CPU_only_input_fixtures_not_actual_branch_or_gameplay_result_forcing=True,actual_B194_gameplay_and_relocated_target_still_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('20 source/current C200 and10 end cases preserve all five prior values;owned writes and all unowned state/guards pass. No actual branch forced.')
