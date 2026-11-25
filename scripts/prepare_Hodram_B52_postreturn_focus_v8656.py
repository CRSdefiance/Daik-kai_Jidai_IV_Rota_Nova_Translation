"""Stop ordinary inputs after the measured B52 withdrawal exchange; preserve the longer runs as evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_postreturn_focus_tools_v8656');assert not root.exists()
    actual=Path('work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json');proof=read(actual)
    assert not proof['unresolved'] and [g['normal_return']['native_result'] for g in proof['groups']]==[[0,0],[0,0]]
    assert all(4485<g['normal_return']['frame']<4720 for g in proof['groups'])
    comparison=Path('work/analysis/Hodram_B52_comparison_v8655/paired_selected_path_comparison.json');long=read(comparison)['groups'][0]
    assert long['case']=='withdrawal' and not all(long['five_native_component_equality'].values())
    result=derive('scripts/run_Hodram_B52_v8649.py','scripts/run_Hodram_B52_postreturn_focus_v8656.py',{
        'Hodram_B52_scene_runs_v8649':'Hodram_B52_postreturn_focus_runs_v8656','_v8649':'_v8656','frames={52:10001}':'frames={52:5201}',
        'range(4000,frames-480,240)':'range(4000,4481,240)',
        'identical_ordinary_A_inputs.json':'identical_ordinary_A_stop_after4484_inputs.json',
        'no_controller_retiming_between_clean_Japanese_andrevised_English=True':'no_controller_retiming_between_clean_Japanese_andrevised_English=True,ordinary_input_case="same_default_inputs_through4484_then_no_further_buttons",focus_basis="work/analysis/Hodram_B52_postreturn_focus_tools_v8656/focus_basis.json",focus_basis_sha256=sha(Path("work/analysis/Hodram_B52_postreturn_focus_tools_v8656/focus_basis.json").read_bytes())',
    })
    root.mkdir(parents=True);save(root/'focus_basis.json',dict(derivation=result,original_default_actual=str(actual),original_default_actual_sha256=sha(actual.read_bytes()),original_long_comparison=str(comparison),original_long_comparison_sha256=sha(comparison.read_bytes()),observed_returns=[g['normal_return'] for g in proof['groups']],last_ordinary_A_start=4480,last_ordinary_A_duration=5,no_further_inputs_from_frame4485=True,all_NewGame_andA_inputs_before_stop_identical_to_original_default=True,both_languages_use_exact_same_unretimed_schedule=True,frames=5201,concrete_risk='Long withdrawal runs differ in final sampled world components after subsequent ordinary inputs; measure the immediate post-B52 state with no additional menu selections.',long_runs_differences_andall_earlier_evidence_preserved_not_replaced=True,no_ROM_RAM_seed_predicate_eventflag_orresult_change=True,no_claim_of_natural_activation_orfuture_world_equivalence=True,new_credit=0,full_goal_complete=False))
