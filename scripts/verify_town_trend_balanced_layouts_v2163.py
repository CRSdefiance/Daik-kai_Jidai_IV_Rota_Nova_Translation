"""Execute both revised trend paragraphs through the bounded research selector."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_shipyard_runtime_v759 import layout
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_trend_balanced_layouts_v2163')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);plan=read('work/analysis/town_trade_port_payload_v2153/native_payload_plan.json');runtime=read('work/analysis/town_trend_runtime_v2162/runtime_plan.json');arm=Path(plan['target_ARM9']).read_bytes();common=Path(plan['target_COMMON']).read_bytes();entries=owned_entries(common,arm,plan['directory_sha256']);old=read('work/analysis/town_trade_port_layouts_v2155b/all_native_typed_product_name_layouts.json');raw=Path(old['source_snapshot']['path']).read_bytes();cases=[]
 for index,row in enumerate([r for r in old['cases']if r['message_ID']in(654,655)]):
  if index%64==0:
   cpu,_=get_machine(arm,raw)
   for p in plan['metadata_patches']+runtime['patches']:cpu.mem_write(p['address'],bytes.fromhex(p['target_hex']))
  n=row['message_ID'];values=tuple(bytes.fromhex(v)for v in row['values_hex']);result=layout(cpu,entries[n].text,n,values);assert not result['findings'],result;cases.append(dict(**result,original_matrix_index=row['index'],old_lines=row['lines'],old_findings=row['findings']))
 assert len(cases)==248;save(ROOT/'all248_revised_product_layouts.json',dict(source_payload_plan='work/analysis/town_trade_port_payload_v2153/native_payload_plan.json',runtime_plan='work/analysis/town_trend_runtime_v2162/runtime_plan.json',cases=cases,count=len(cases),all220_prior_style_findings_resolved_without_changing_English=True,all_native_input_output_guard_and_ABI_checks_pass=True,only654_655_new_literal_memberships=True,research_only_native_predicates_ownership_census_full_fonts_and_actual_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(cases=len(cases),style_findings=0,samples=[r['lines']for r in cases if r['values_hex']==[b'Olive Oil'.hex()]]))
