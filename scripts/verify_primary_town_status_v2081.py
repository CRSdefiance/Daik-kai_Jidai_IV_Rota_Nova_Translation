"""Native status regression for the relocated-table successor."""
import inspect
from pathlib import Path
from types import SimpleNamespace
from scripts import verify_recruitment_runtime_v771 as old
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_status_v2081')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/town_services_runtime_v2080/runtime_plan.json')
 source=inspect.getsource(old.field_contracts)
 assert source.count('runtime.STATUS,STOP')==1 and source.count('STACK-BASE-32:STACK-BASE')==2
 source=source.replace('runtime.STATUS,STOP','runtime.STATUS|1,STOP').replace('STACK-BASE-32:STACK-BASE','STACK-BASE-36:STACK-BASE')
 env={**old.__dict__,'runtime':SimpleNamespace(**{**old.runtime.__dict__,'STATUS':0x021479D4}),'make':lambda a,changed=False:prepared(a)}
 exec(compile(source,__file__,'exec'),env)
 current=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');target=Path(plan['research_ARM9']).read_bytes()
 receipts=[]
 for label,arm in [('current',current),('research2080',target)]:
  cases=env['field_contracts'](arm);assert len(cases)==140
  receipts.append(dict(version=label,ARM9_sha256=sha(arm),cases=cases,count=len(cases),all_native_whole8MiB_and_ABI_guards_pass=True))
  print(label,len(cases),'status cases pass',flush=True)
 assert receipts[0]['cases']==receipts[1]['cases']
 rejected=Path(read('work/analysis/town_services_runtime_v2077/runtime_plan.json')['research_ARM9']).read_bytes()
 try:env['field_contracts'](rejected)
 except AssertionError:reproduced=True
 else:raise AssertionError('V2077 failed-output regression was not reproduced')
 save(ROOT/'current_and_corrected_relocated_status_native_equivalence.json',dict(versions=receipts,total_cases=280,earlier2077_output_assertion_reproduced=True,current_and2080_typed_outputs_exact=True,effective_verifier_sha256=sha(source.encode()),historical_verifier_sha256=sha(Path(old.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_or_registry_mutation=True,full_goal_complete=False))
