"""Prepare paired default-input B52 captures; selected controller paths must be measured."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_default_scene_tools_v8649');assert not root.exists()
    result=derive('scripts/run_Hodram_B51_v8574.py','scripts/run_Hodram_B52_v8649.py',{
        'Hodram_B51_scene_runs_v8574':'Hodram_B52_scene_runs_v8649','Hodram_B51_fixtures_v8573':'Hodram_B52_fixtures_v8648','choices=[51]':'choices=[52]','frames={51:10001}':'frames={52:10001}','_v8574':'_v8649',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,identical_ordinary_NewGame_andA_input_schedules_forboth_languages=True,all_observer_readonly_host_slot_restore_core_integrity_andcoldboot_guards_preserved=True,actual_menu_choice_path_complete_glyphs_headers_backing_returns_andtransitions_must_be_measured=True,alternate_choice_geometry_end_behavior_tests_remain_pending=True,no_predicate_eventflag_RNG_roster_orresult_forcing=True,no_natural_activation_location_earned_progress_fullroute_hardware_orcredit_claim=True,new_credit=0,full_goal_complete=False))
