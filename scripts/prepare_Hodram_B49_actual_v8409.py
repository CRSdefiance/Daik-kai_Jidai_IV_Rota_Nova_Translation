"""Rebind the branch-aware actual audit to the observed complete B49 entry fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_audit_tools_v8409');assert not root.exists()
    result=derive('scripts/audit_Hodram_actual_v8282.py','scripts/audit_Hodram_B49_actual_v8409.py',{
        'Hodram_actual_v8282':'Hodram_B49_actual_v8409',
        'work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json':'work/analysis/Hodram_B49_fixtures_v8406/two_whole_scripts.json',
        'work/analysis/Hodram_actual_models_v8281b/28_clean_native_bodies28_exact_revised_reuses_six_current_headers.json':'work/analysis/Hodram_B49_models_v8408/native_models.json',
        'Hodram_scene_runs_v8280':'Hodram_B49_scene_runs_v8407',
        'choices=[137,45,46]':'choices=[49]',
        '{137:24001,45:10001,46:16001}[number]':'{49:10001}[number]',
        'full_resource_4800_layout0_hide4700_andlater_state_comparison_separate_pending=number==46':'full_resource_4820_layout2_hide4700_andlater_state_comparison_separate_pending=True',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_original_branch_flow_complete_body_multi_actor_nameplate_masks_andcallback_guards_preserved=True,whole_script_containsFE_butonly_observed_progressive_path_is_claimed=True,unvisited_conditional_speeches_remain_listed=True,new_credit=0,full_goal_complete=False))
