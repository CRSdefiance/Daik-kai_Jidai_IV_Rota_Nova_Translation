"""Native selector scope with current parent fields, codec and special routes."""
import inspect
from pathlib import Path
from types import SimpleNamespace
from scripts import verify_palace_runtime_v796 as old
from scripts.primary_town_runtime_v2077 import rows,SOURCE
from scripts.search_reports_runtime_v1659 import contract_rows
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_selector_v2082')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json');current=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');research=Path(plan['research_ARM9']).read_bytes()
 assert sha(current)==SOURCE and sha(research)==plan['target_ARM9_sha256']
 source=inspect.getsource(old.scope);a=source.index('        for parent in (0x02053D24');b=source.index('    finally:',a)
 source=source[:a]+'''        for parent,(offset,high,allowed) in records.items():
            def selected(value):
                check(parent,value if offset==0x274 else 0,queue=value if offset==0x27C else 0,gift=value if offset==0x270 else 0)
            if high:
                for low in (*range(0x6000,0x9000),0,65535):selected(high<<16|low)
                for wrong in (0,0x0111,0x0210,0x0212,0x1211,0xFFFF):
                    for low in sorted(allowed):selected(wrong<<16|low)
            else:
                for value in (*range(3668),65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF):selected(value)
        for parent in (0,0xFFFFFFFF,0x12053D24,0x02053EAC,0x02054048):
            for value in (0,63,64,842,905,3667,0x021189C0,0xFFFFFFFF):check(parent,value,value,value)
'''+source[b:]
 source=source[:source.index("    save(ROOT/'scope_proof.json'")]+'''    return count
'''
 receipts=[]
 for label,arm,members in [('current',current,contract_rows),('research2080',research,rows)]:
  bank=SimpleNamespace(COORD=0x02147A78,STATUS=0x021479D4,ENTRY=0x02132020)
  env={**old.__dict__,'new':SimpleNamespace(bank=bank,contract_rows=members)}
  exec(compile(source,__file__,'exec'),env);count=env['scope'](arm)
  receipts.append(dict(version=label,ARM9_sha256=sha(arm),cases=count,rows=members(),all_exact_routes_registers_SP_LR=True));print(label,count,'cases pass',flush=True)
 save(ROOT/'all_eight_parent_native_selector_and_ABI.json',dict(versions=receipts,total_cases=sum(r['cases']for r in receipts),effective_verifier_sha256=sha(source.encode()),historical_verifier_sha256=sha(Path(old.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_eight_parent_wrong_parent_numeric_pointer_alignment_highword_special_dispatch_checks=True,no_ROM_or_registry_mutation=True,full_goal_complete=False))
