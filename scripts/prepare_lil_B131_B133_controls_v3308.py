"""Bind61 complete speech preambles including real00 actor dispatch."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/prove_lil_B122_B127_controls_v3266.py');new=Path('scripts/prove_lil_B131_B133_controls_v3308b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B122_B127_controls_v3266':'lil_B131_B133_controls_v3308b',
      'work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json':'work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json',
      'work/analysis/lil_B122_B127_voices_v3264/current_native_input.json':'work/analysis/lil_B131_B133_voices_v3307b/current_native_input.json',
      'len(cases)==310':'len(cases)==122',"for c in cases)==20":"for c in cases)==2",'len(predicates)==14':'len(predicates)==5',
      "macros=={'FI':12,'FA':0,'FO':0}":"macros=={'FI':6,'FA':0,'FO':1}",
      'statics==[2,6,9,20,26,92,95,151]':'statics==[0,2,5,9,20]',
      'all155_source_current_dispatch_FE_null_actor_and14_predicates.json':'all61_source_current_dispatch_selector00_FE_and5_predicates.json',
      'all155_complete_preambles_have310_current_code_source_and_current_dispatch_cases':'all61_complete_preambles_have122_current_code_source_and_current_dispatch_cases',
      'all20_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback':'all2_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback',
      'all14_original_predicates_preserve_source_operands_results_and_unowned4MiB':'all5_original_predicates_preserve_source_operands_results_and_unowned4MiB',
      'source97_is_static_retainer151_without_dynamic_role_assignment=True':'source00_is_static_actor0_Rafael_Castor_without_role_assignment=True',
      "source2000_actual_rule_separately_bound='work/analysis/lil_B122_original2000_waits_v3265/original2000_actual_rule_and_current_source_binding.json',":'no_source2000_commands_in_next63_scope=True,',
      'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    anchor='    statics=sorted(';at=t.index(anchor)
    t=t[:at]+"    assert sum(c['source_selector']==0 for c in cases)==36\n"+t[at:]
    t=t[:t.rindex('    print(')]+"    print('122current-code source/current dispatches,including36real00Rafael andtwoFE null-actor cases,FI6/FO1/five native predicates pass. No rolefixtures ornewgameplay;complete context/prose/display/release pending.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_control_tools_v3308');root.mkdir(parents=True);save(root/'source00_dispatch_successor_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),source00_body_is_passed_after_complete_actor_selector=True,no_previous_producer_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
