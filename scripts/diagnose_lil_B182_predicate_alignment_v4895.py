"""Capture a strict CPU-only relocated-predicate alignment failure, if present."""
from pathlib import Path
from types import FunctionType
import inspect
from scripts.prove_lil_B182_predicate500_v4883 import probe500
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B182_predicate_alignment_v4895')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    p=Path('work/analysis/lil_B182_relocation_v4893/nested_source_relocation_research.json');plan=read(p)
    doc=read(plan['manuscript']);packet=read(doc['source_context']);spec=plan['blocks'][0]
    block=Path(spec['research_block']).read_bytes();assert sha(block)==spec['research_block_sha256']
    source=inspect.getsource(probe500)
    needle='    assert writes==expected_writes'
    assert source.count(needle)==1
    source=source.replace(needle,"    diagnostic(command,writes,expected_writes,before,bytes(cpu.mem_read(BASE,0x400000)))\n"+needle)
    def diagnostic(command,writes,expected,before,after):
        differences=[dict(offset=i,before=a,after=b) for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]
        save(ROOT/('offset'+str(command['offset'])+'_strict_write_diagnostic.json'),dict(
            command=command,writes=writes,expected_RNG_writes=expected,all4MiB_changed_bytes=differences,
            before_sha256=sha(before),after_sha256=sha(after),not_a_native_approval=True,
            CPU_only_no_actual_emulator_seed_write=True))
    env={**probe500.__globals__,'diagnostic':diagnostic};exec(compile(source,__file__+'::diagnostic','exec'),env)
    ctx=CurrentContext('work/analysis/lil_B182_voices_v4879/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    results=[]
    for mapped in [r for r in spec['command_map'] if r['word']==0x8000]:
        original=next(r for r in packet['blocks'][0]['all_current_native_commands'] if r['offset']==mapped['old_offset'])
        command={**original,'offset':mapped['new_offset']}
        try:
            result=ctx.execute(env['probe500'],block,command)
            results.append(dict(offset=command['offset'],strict_pass=True,result=result))
        except AssertionError as e:
            results.append(dict(offset=command['offset'],strict_pass=False,error=repr(e)))
        finally:ctx.machines.pop()
    save(ROOT/'diagnostic_receipt.json',dict(relocation_plan=str(p),relocation_plan_sha256=sha(p.read_bytes()),
        cases=results,source_owned_diagnostic_adapter=source,not_a_proof_or_waiver=True,new_emulator_runs=0,new_review_credit=0))
    print(results)
