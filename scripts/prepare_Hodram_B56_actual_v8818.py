"""Source-lock complete actual FE/progressive audit to the B56 paired capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B56_actual_tools_v8818');assert not root.exists()
    result=derive('scripts/audit_Hodram_B50_actual_v8507.py','scripts/audit_Hodram_B56_actual_v8818.py',{
        'Hodram_B50_actual_v8507':'Hodram_B56_actual_v8818',
        'Hodram_B50_fixtures_v8504/two_whole_scripts.json':'Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
        'Hodram_B50_models_v8506/native_models.json':'Hodram_B54_B60_models_v8817/native_models.json',
        'Hodram_B50_scene_runs_v8505':'Hodram_B54_B60_scene_runs_v8816',
        'choices=[50]':'choices=[56]',
        '{50:10001}':'{56:7001}',
        'full_resource_4800_layout0_hide4700_andlater_state_comparison_separate_pending':'full_FE_live_context_andlater_state_comparison_separate_pending',
    })
    root.mkdir(parents=True);save(root/'source_locked_actual_audit.json',dict(derivation=result,
        all_original_native_flow_fullglyph_name_FE_null_residentpayload_readonly_coldboot_andinput_guards_unchanged=True,
        B56_three_speeches_one_FE_panel_singlepage_native_models_andcomplete_return_scope=True,
        no_new_frames_natural_event_activation_fullroute_orhardware_claim=True,new_credit=0,full_goal_complete=False))
