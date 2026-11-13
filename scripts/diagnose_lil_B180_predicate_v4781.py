"""Diagnose the source500 predicate's native writes; this grants no approval."""
from pathlib import Path
import inspect
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_predicate_diagnostic_v4781')
SOURCE=Path('work/analysis/lil_B180_source_v4773/all11_clean_current_complete_context.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    source=inspect.getsource(probe)
    source=source.replace('def probe(','def diagnostic(')
    needle="    before=bytes(cpu.mem_read(BASE,0x400000));calls=[];writes=[];scratch=0x02279600"
    assert source.count(needle)==1
    source=source.replace(needle,needle+"\n    all_writes=[]\n    whole_hook=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:all_writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=BASE,end=BASE+0x3FFFFF)")
    source=source.replace('finally:cpu.hook_del(h);cpu.hook_del(wh)','finally:cpu.hook_del(h);cpu.hook_del(wh);cpu.hook_del(whole_hook)')
    needle='unowned=bytearray(after);unowned[scratch-BASE:scratch-BASE+4]=before[scratch-BASE:scratch-BASE+4];assert unowned==before'
    assert source.count(needle)==1
    source=source.replace(needle,"delta=[i for i,(a,b)in enumerate(zip(before,after,strict=True)) if a!=b];changed=[]\n    for at in delta:\n        if changed and at==changed[-1][-1]+1:changed[-1].append(at)\n        else:changed.append([at])\n    changes=[dict(address=BASE+r[0],bytes=len(r),before_hex=before[r[0]:r[-1]+1].hex(),after_hex=after[r[0]:r[-1]+1].hex()) for r in changed]")
    source=source.replace("cpu.mem_write(scratch,before[scratch-BASE:scratch-BASE+4]);assert bytes(cpu.mem_read(BASE,0x400000))==before and", "cpu.mem_write(scratch,before[scratch-BASE:scratch-BASE+4]);assert")
    source=source.replace('sole_scratch_restore_recovers_all4MiB_exact=True,','diagnostic_only_no_preservation_approval=True,changed_main_RAM_spans=changes,all_native_main_RAM_writes=all_writes,executed_current_PCs=sorted(provider.executed_current),')
    source=source.replace('all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact=True,','input_owner_output_canaries_and_ABI_checked=True,unowned_state_contract_not_yet_proved=True,')
    namespace=dict(probe.__globals__);exec(compile(source,__file__+'::diagnostic-not-approval','exec'),namespace)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B180_voices_v4775/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    block=IlnkContainer.parse(NdsImage.open(packet['current_ROM']).read_file('/data/SC2.DK4')).blocks[180]
    cases=[]
    for c in packet['blocks'][0]['all_current_native_commands']:
        if c['word']==0x8000:
            cases.append(ctx.execute(namespace['diagnostic'],block,c));ctx.machines.pop()
    pcs=sorted({w['PC'] for c in cases for w in c['all_native_main_RAM_writes']})
    disassembly=[];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for pc in pcs:
        at=pc-0x02000000
        disassembly.append(dict(write_PC=pc,nearby=[dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in decoder.disasm(ctx.arm[max(0,at-28):at+32],max(0,at-28)+0x02000000)]))
    save(ROOT/'native500_write_diagnostic.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,write_PC_disassembly=disassembly,
        adapter=source,diagnostic_only_not_preservation_approval=True,no_gameplay_or_review_credit=True,
        next='Prove ownership and semantics of the original writes before approving predicates;do not globally waive the all4MiB gate.',full_goal_complete=False))
    print([dict(offset=c['offset'],native_result=c['native_result'],changes=c['changed_main_RAM_spans'],writes=c['all_native_main_RAM_writes']) for c in cases])
