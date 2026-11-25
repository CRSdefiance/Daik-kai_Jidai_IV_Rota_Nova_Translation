"""Repeat only the focused intro's concrete later-state difference with eight read-only RAM samples."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_intro_risk_tools_v8231')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/run_Gerhard_intro_v8228.py','scripts/run_Gerhard_intro_risk_v8231.py',{
        'Gerhard_intro_display_runs_v8228':'Gerhard_intro_risk_runs_v8231',
        'Gerhard_intro_B{block}_route{route}_{version}_v8228':'Gerhard_intro_risk_B{block}_route{route}_{version}_v8231',
        'captures=sorted(set(range(2350,12001,60))|{12000})':'captures=[3970,4330,4810,5770,6310,9730,10510,12000]',
        "*map(str,captures),'--dump-ram']":"*map(str,captures),'--dump-capture-ram','--dump-ram']",
        'complete_body_header_palette_transition_return_andlate_state_analysis_pending=True':'eight_readonly_RAM_samples_exact_replay_andlater_state_analysis_pending=True',
        '12001-frame focused introduction display capture terminal;body/header/return/transition analysis pending':'12001-frame focused introduction repeat terminal;exact replay/RAM phase analysis pending',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        same_ROM_same_inputs_same_horizon_only8_selective_readonly_RAM_exports_added=True,
        concrete_risk_intro_later_models_persistent_objects_actors_RNG_and29of106_RGB_differences=True,
        initial_all5_actual_body_masks_and262nameholds_not_repeated_asnewcoverage=True,
        no_seed_orcontroller_retiming_no_story_flag_role_roster_funds_result_forcing=True,
        all_original_runtime_observer_andhost_restoration_guards_preserved=True,new_credit=0,full_goal_complete=False))
    print('Prepared focused intro repeat with8 read-only RAM phases;identicalROM/input/horizon,allguards preserved.')
