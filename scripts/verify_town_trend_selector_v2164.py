"""All lowwords/eight parents plus fullword edges for compact selector andR2 ABI."""
from pathlib import Path
from types import SimpleNamespace
import inspect,hashlib
from scripts import verify_palace_runtime_v796 as prior
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_trend_selector_v2164')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);plan=read('work/analysis/town_trend_runtime_v2162/runtime_plan.json');current=NdsImage.open('out/all_routes_combined_v2143_candidate.nds').read_file('/__arm9__.bin');research=Path(plan['research_ARM9']).read_bytes();assert sha(current)==plan['source_ARM9_sha256']and sha(research)==plan['target_ARM9_sha256']
 source=inspect.getsource(prior.scope);a=source.index('        for parent in (0x02053D24');b=source.index('    finally:',a)
 source=source[:a]+'''        for parent,(offset,high,allowed) in records.items():
            def selected(value):
                check(parent,value if offset==0x274 else 0,queue=value if offset==0x27C else 0,gift=value if offset==0x270 else 0)
            for low in range(65536):selected(high<<16|low)
            for wrong in (0,1,0x0111,0x0210,0x0211,0x0212,0x1211,0xFFFF):
                if wrong==high:continue
                for low in sorted(allowed):selected(wrong<<16|low)
            for edge in(0x10000,0x10001,0x7FFFFFFF,0x80000000,0xFFFFFF00,0xFFFFFFFE,0xFFFFFFFF):selected(edge)
            for wrong_parent in(parent+0x10000,parent-0x10000,parent|0x10000000):
                for low in sorted(allowed):
                    value=high<<16|low;check(wrong_parent,value,value,value)
        for parent in(0,0xFFFFFFFF,0x12053D24,0x02053EAC,0x02054048):
            for value in(0,63,64,653,654,655,656,842,905,3667,0x021189C0,0xFFFFFFFF):check(parent,value,value,value)
'''+source[b:]
 source=source[:source.index("    save(ROOT/'scope_proof.json'")]+'''    return dict(cases=count,trace_sha256=trace.hexdigest())
'''
 source=source.replace('    count = 0','    count = 0\n    trace=hashlib.sha256()').replace('        nonlocal count','        nonlocal count,cpu,hooks\n        if count and count%2048==0:\n            for hook in hooks:cpu.hook_del(hook)\n            cpu=prepared(arm)\n            hooks=[cpu.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=t,end=t)for t in targets]')
 source=source.replace("        fields = {0x274:number,0x27C:queue,0x270:gift}","        cpu.mem_write(STACK-64,b'\\xA5'*64)\n        cpu.mem_write(STACK,b'\\xB3'*0x300)\n        fields = {0x274:number,0x27C:queue,0x270:gift}")
 source=source.replace('        cpu.emu_start(new.bank.ENTRY,STOP,count=10000)','        input_stack=bytes(cpu.mem_read(STACK,0x300))\n        cpu.emu_start(new.bank.ENTRY,STOP,count=10000)\n        assert bytes(cpu.mem_read(STACK-64,36))==b\'\\xA5\'*36 and bytes(cpu.mem_read(STACK,0x300))==input_stack')
 source=source.replace('        count += 1',"        trace.update(struct.pack('<5I',parent,number,queue,gift,route))\n        count += 1")
 receipts=[]
 for name,arm,members in[('current',current,plan['old_logical_rows']),('research2162',research,plan['logical_rows'])]:
  bank=SimpleNamespace(COORD=0x02147A78,STATUS=0x021479D4,ENTRY=0x02132020);env={**prior.__dict__,'hashlib':hashlib,'new':SimpleNamespace(bank=bank,contract_rows=lambda members=members:members)};exec(compile(source,__file__,'exec'),env);result=env['scope'](arm);receipts.append(dict(version=name,ARM9_sha256=sha(arm),**result));print(receipts[-1],flush=True)
 save(ROOT/'all_eight_parent_lowword_fullword_stack_and_R2_ABI.json',dict(versions=receipts,total_cases=sum(r['cases']for r in receipts),all65536lowwords_each_of8source_parents_each_current_and_research=True,all_wrong_highwords_alignment_parent_upper_words_fullword_edges_and_special_dispatch_pass=True,allR0_toR11_including_R2_and_SP_LR_preserved=True,all_input_stack_fields_unchanged=True,canaries_below_new28byte_entry_frame_preserved=True,native_machine_reinitialized_every2048_independent_cases=True,only_new_memberships=dict(parent=0x02054014,IDs=[654,655]),runtime_plan='work/analysis/town_trend_runtime_v2162/runtime_plan.json',runtime_plan_sha256=sha(Path('work/analysis/town_trend_runtime_v2162/runtime_plan.json').read_bytes()),effective_verifier_sha256=sha(source.encode()),historical_verifier_sha256=sha(Path(prior.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_or_registry_mutation=True,full_goal_complete=False))
