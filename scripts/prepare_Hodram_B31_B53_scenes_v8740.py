"""Prepare paired complete-block cold boots with identical ordinary controller inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_scene_tools_v8740');assert not root.exists()
    receipt=derive('scripts/run_Hodram_B52_v8649.py','scripts/run_Hodram_B31_B53_v8740.py',{
        'Hodram_B52_scene_runs_v8649':'Hodram_B31_B53_scene_runs_v8740','Hodram_B52_fixtures_v8648/two_whole_scripts.json':'Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json',
        'choices=[52]':'choices=[31,53]','frames={52:10001}':'frames={31:6001,53:6001}','_v8649':'_v8740',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        identical_ordinary_Hodram_NewGame_A_inputs_capture_schedule_and6001frames_perlanguage_andblock=True,
        all_observer_readonly_hostslot_restore_core_integrity_andcoldboot_guards_preserved=True,
        no_source_predicate_flags_roster_RNG_orresults_forced=True,observed_query_selected_branch_andunvisited_variant_to_be_measured=True,
        complete_body_name_glyphs_pagination_opaquecontrols_returns_andtransitions_not_yet_verified=True,
        no_natural_activation_original_location_earned_progress_fullroute_hardware_orcredit_claim=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
