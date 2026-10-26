"""Scope final dispatch/predicate proof to61 speeches including18actor00."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/prove_lil_B122_B127_relocated_controls_v3292.py');new=Path('scripts/prove_lil_B131_B133_relocated_controls_v3333b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'prepare_lil_B122_B127_research_v3289b':'prepare_lil_B131_B133_research_v3330b',
      'lil_B122_B127_relocated_controls_v3292':'lil_B131_B133_relocated_controls_v3333b',
      'lil_B122_B127_editorial_manuscript_v5.json':'lil_B131_B133_editorial_manuscript_v4.json',
      'lil_B122_B127_reference_census_v3291/all312_commands64_relative_sites_and_shipped_entry_census.json':'lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census.json',
      'lil_B122_B127_fonts_v3283':'lil_B131_B133_fonts_v3324b',
      'len(dispatches)==155':'len(dispatches)==61',"for r in dispatches)==10":"for r in dispatches)==1",'len(predicates)==14':'len(predicates)==5',
      'all155_relocated_dispatches_and14_predicate_pairs.json':'all61_relocated_dispatches_source00_and5_predicate_pairs.json',
      'all155_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all61_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text',
      'all10_FE_preserve_original_null_actor_before_dynamic_fallback':'all1_FE_preserves_original_null_actor_before_dynamic_fallback',
      'all14_predicate_current_relocated_results_and_source_operands_equal':'all5_predicate_current_relocated_results_and_source_operands_equal',
      'static97_is_retainer151_without_fallback_assignment=True':'all18_final_source00_speeches_are_static_Rafael0_without_role_assignment=True',
      'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    a='    evidence={str(p):';at=t.index(a);t=t[:at]+"    assert sum(r['source_selector']==0 and r['resolved_actor_ID']==0 for r in dispatches)==18\n"+t[at:]
    t=t[:t.rindex('    print(')]+"    print('61 relocated dispatches,including18source00Rafael,oneFE null actor andfive predicate pairs pass. Original source operands/results andunowned RAM preserved;no selected gameplay orrelease claim.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B131_B133_control_tools_v3333');root.mkdir(parents=True);save(root/'relocated_source00_control_successor.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),all_source00_body_bytes_and_Lil_macros_must_reach_original_consumer=True,no_previous_producer_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
