"""Identical ordinary input schedules;separate FE observer only for the distinct B56 panel."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_run_tools_v8816');assert not root.exists()
    ordinary=derive('scripts/run_Hodram_B31_B53_v8740.py','scripts/run_Hodram_B54_B60_v8816.py',{
        'Hodram_B31_B53_scene_runs_v8740':'Hodram_B54_B60_scene_runs_v8816',
        'Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json':'Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
        'choices=[31,53]':'choices=[54,57,58,59,60]',
        'frames={31:6001,53:6001}':'frames={54:6001,57:9001,58:16001,59:10001,60:10001}',
        '_v8740':'_v8816',
    })
    modal=derive('scripts/run_Hodram_B50_v8505.py','scripts/run_Hodram_B56_v8816.py',{
        'Hodram_B50_scene_runs_v8505':'Hodram_B54_B60_scene_runs_v8816',
        'Hodram_B50_fixtures_v8504/two_whole_scripts.json':'Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
        'choices=[50]':'choices=[56]',
        'frames={50:10001}':'frames={56:7001}',
        '_v8505\'':'_v8816\'',
        '    model=read("work/analysis/Hodram_B50_models_v8506/native_models.json")\n    FE_body=next(m for m in model["native_models"][version] if m["source_selector"]==254)["expanded_native_hex"]':
        '''    model=read('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json' if version=='clean_Japanese' else 'work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json')
    FE_body=next(m for m in model['records'] if m['source_selector']==254)['expanded_source_hex' if version=='clean_Japanese' else 'expanded_stored_hex']''',
    })
    root.mkdir(parents=True);save(root/'source_locked_run_derivations.json',dict(ordinary=ordinary,FE=modal,
        frames_by_block={54:6001,56:7001,57:9001,58:16001,59:10001,60:10001},
        identical_ordinary_Hodram_NewGame_andA_schedule_per_paired_language=True,no_language_specific_retiming=True,
        all_native_high_integer_constants_andoriginal_readonly_code_hostslot_restore_coldboot_guards_preserved=True,
        FE_held_state_schedule_unchanged_from_source_producer=True,source_FEnull_andEnglish_caption_bound_to_exact_current_models=True,
        no_savestate_RAM_roster_flags_funds_RNG_condition_orresults_forced=True,
        captured_events_andcompleteglyphs_headers_pagination_returns_andtransitions_still_require_actual_audit=True,
        no_natural_optional_activation_original_location_earned_progress_fullroute_orhardware_claim=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
