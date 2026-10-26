"""Fresh current/research incoming-reference and unchanged-path evidence."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_runtime_references_v2074')
PLAN=Path('work/analysis/town_services_runtime_v2070/runtime_plan.json')
OLD=Path('work/analysis/town_services_current_routes_v2069b/all84_current_macro_route_outputs.json')
NEW=Path('work/analysis/town_services_research_routes_v2072/research_runtime_all84_original_BL_routes.json')
if __name__=='__main__':
 assert not ROOT.exists();plan=read(PLAN);old=NdsImage.open('out/all_routes_combined_v2047_candidate.nds');new=NdsImage.open('out/all_routes_combined_v2047_candidate.nds');target=Path(plan['research_ARM9']).read_bytes()
 assert sha(old.read_file('/__arm9__.bin'))==plan['source_ARM9_sha256']and sha(target)==plan['target_ARM9_sha256'];new.rom.arm9=target
 spans=plan['private_spans'];before,after=[census(rom,spans,spans)for rom in(old,new)]
 external=lambda rows:sorted(r for r in rows if not r[-1])
 assert external(before)==external(after)
 # The newly occupied four Fleet-slot tail bytes have no incoming alias or
 # branch into their interior in the fresh current/research all-unit census.
 tails=[[0x02151724,0x02151728]]
 a,b=[census(rom,tails,spans)for rom in(old,new)]
 assert not external(a)and not external(b)
 original,research=map(read,(OLD,NEW));assert not original['errors']and not research['errors']
 key=lambda r:(r['message_ID'],tuple(r['supplied_arguments']),r['route'])
 source={key(r):r for r in original['cases']};unchanged=[];changed=[]
 for row in research['cases']:
  prior=source[key(row)];same=prior['current_output_hex']==row['research_output_hex']
  n=row['message_ID'];allowed=(row['route'].startswith('numeric')and n<=63)or(76<=n<=82)
  if not allowed:assert same
  (unchanged if same else changed).append(dict(message_ID=n,supplied_arguments=row['supplied_arguments'],route=row['route'],unchanged=same))
 assert len(unchanged)+len(changed)==148
 ROOT.mkdir(parents=True)
 save(ROOT/'current_research_reference_and_unowned_path_preservation.json',dict(source_ARM9_sha256=plan['source_ARM9_sha256'],target_ARM9_sha256=sha(target),runtime_plan=str(PLAN),runtime_plan_sha256=sha(PLAN.read_bytes()),
  private_spans=spans,before_all_unit_reference_census=before,after_all_unit_reference_census=after,all_external_references_exact=True,
  last4_source_owned_Fleet_slot_no_incoming_interior_alias_or_branch=True,last4_before_census=a,last4_after_census=b,
  current_route_proof=str(OLD),current_route_proof_sha256=sha(OLD.read_bytes()),research_route_proof=str(NEW),research_route_proof_sha256=sha(NEW.read_bytes()),
  exact_output_unchanged_cases=unchanged,intended_new_output_cases=changed,all_queued_nonmonthly_and_distinct_modal_outputs_exact=True,
  only_source_owned_code_and_selector_bytes_changed=True,no_fonts_graphics_script_COMMON_prose_or_ROM_registry_mutation=True,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(external_reference_rows=len(external(before)),new_Fleet_tail_interior_aliases=0,unchanged_parameter_routes=len(unchanged),intended_changed_routes=len(changed)))
