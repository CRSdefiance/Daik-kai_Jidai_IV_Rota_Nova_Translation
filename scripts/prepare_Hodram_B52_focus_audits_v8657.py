"""Audit the focused no-further-input withdrawal pair and retain all observed state differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_focus_audit_tools_v8657');assert not root.exists();tools=[]
    tools.append(derive('scripts/audit_Hodram_B52_actual_v8651.py','scripts/audit_Hodram_B52_focus_v8657.py',{
        'Hodram_B52_actual_v8651':'Hodram_B52_focus_actual_v8657','Hodram_B52_scene_runs_v8649':'Hodram_B52_postreturn_focus_runs_v8656','{52:10001}':'{52:5201}','no_B51_FE_panel':'no_B52_FE_panel',
    }))
    source=Path('scripts/compare_Hodram_B52_actual_v8655.py').read_text(encoding='utf-8')
    a=source.index('    for case,proofpath,return_key,selected in [');b=source.index('        number=52;',a)
    tools.append(derive('scripts/compare_Hodram_B52_actual_v8655.py','scripts/compare_Hodram_B52_focus_v8658.py',{
        source[a:b]:"    for case,proofpath,return_key,selected in [('withdrawal-postreturn-focus','work/analysis/Hodram_B52_focus_actual_v8657/B52/paired_actual_dialogue_headers_flow_returns.json','normal_return',0)]:\n",
        'Hodram_B52_comparison_v8655':'Hodram_B52_focus_comparison_v8658','total_actual_frames=40004':'total_actual_frames=10402',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_native_high_integer_constants_andmultiplicity_preserved=True,complete_native_body_name_sourceflow_return_andall_original_component_actor_RNG_calendar_RGB_guards_preserved=True,focus_inputs_end_after4484_identically_forboth_languages_not_retimed=True,all_original_long_run_differences_remain_separate=True,no_assertion_of_future_simulation_equivalence=True,new_credit=0,full_goal_complete=False))
