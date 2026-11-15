"""Prove original C200/end preserve caller-owned result word for every result class."""
import struct
from pathlib import Path
from scripts.prove_lil_B191_C200_v5363 import C200,adapter_source
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B191_research_v5380 import PARENT,ROM,PLAN
ROOT=Path('work/analysis/lil_B191_carried_result_v5392')

if __name__=='__main__':
    assert not ROOT.exists()
    source=adapter_source()
    target=checked_text(source,{
        'def current_C200(arm,common,raw,plan,block,command):':'def prior_C200(arm,common,raw,plan,block,command,prior):',
        'cpu.mem_write(result,bytes(24))':"cpu.mem_write(result,struct.pack('<6I',0,prior,0,0,0,0))",
        '(result,owner,length,0)':'(result,owner,length,prior)',
        'values==(3,0,0,0,0,0)':'values==(3,prior,0,0,0,0)',
    })
    ns=dict(C200.__globals__);exec(compile(target,__file__+'::source-owned-prior-result','exec'),ns)
    doc=read('translations/lil_B191_editorial_manuscript_v4.json');packet=read(doc['source_context']);plan=read(PLAN)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B191_voices_v5357/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    mapping={c['old_offset']:c['new_offset'] for c in plan['blocks'][0]['command_map']}
    rows=[]
    for version,path in [('clean',Path('work/clean.nds')),('current',PARENT),('relocated',ROM)]:
        image=NdsImage.open(path);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[191]
        command=next(c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0xC200)
        command={**command,'offset':mapping[command['offset']] if version=='relocated' else command['offset']}
        for prior in [0,1,2,3,0xFFFFFFFF]:
            result=ctx.execute(ns['prior_C200'],block,command,prior);ctx.machines.pop()
            assert result['native_result']==[3,prior,0,0,0,0]
            cpu=machine(image.read_file('/__arm9__.bin'));stream,owner,out,length=0x02660000,0x02650000,0x02668000,0x02668100
            end=mapping[730] if version=='relocated' else 730
            logical=8+struct.unpack_from('<H',block,4)[0];assert end+4==logical
            cpu.mem_write(stream-16,b'\xa5'*(logical+48));cpu.mem_write(stream,block[:logical])
            cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+end,0,0));owned=bytes(cpu.mem_read(owner-16,64))
            cpu.mem_write(out-16,b'\xa5'*80);cpu.mem_write(out,struct.pack('<6I',0,prior,0,0,0,0))
            cpu.mem_write(length-16,b'\xa5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(0x02000000,0x400000))
            call(cpu,0x2A510,(out,owner,length,prior))
            values=list(struct.unpack('<6I',cpu.mem_read(out,24)))
            assert values==[0,prior,0,0,0,0] and struct.unpack('<I',cpu.mem_read(length,4))[0]==4
            assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owned
            assert bytes(cpu.mem_read(stream,logical))==block[:logical]
            for at in [stream-16,stream+logical,out-16,out+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
            rows.append(dict(version=version,prior_result=prior,C200=result,end_native_result=values,end_offset=end,end_extent=4,all4MiB_owner_payload_and_guards_exact=True))
    assert len(rows)==15 and not ctx.machines
    adapters=[]
    save(ROOT/'all15_C200_and15_end_prior_result_cases.json',dict(cases=rows,source_owned_adapter=target,
        adapters=adapters,prior_result_values=[0,1,2,3,0xFFFFFFFF],original_interpreter_preserves_caller_second_result_word=True,
        B190_initial_audit_diagnostic_preserved_as_history_only=True,emulator_runs_not_repeated=True,
        original_C200_and_end_preserve_all_five_prior_result_values=True,no_native_or_emulator_state_waiver=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,Path('scripts/audit_lil_B191_actual_v5389.py'),Path(__file__)]},
        no_credit=True,full_goal_complete=False))
    print('15 original C200 and15 end cases preserve prior result;all state/ABI guards pass. No emulator-state change or audit rewrite.')
