"""Derive both complete saved-run comparisons, retaining all native/RGB guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_comparison_tools_v8765');assert not root.exists()
    receipt=derive('dk4tool/patch/hodram_B51_comparison_v1.py','dk4tool/patch/hodram_B31_B53_comparison_v1.py',{
        "len(comparison['groups'])==1,'one complete B51 exchange comparison'":"len(comparison['groups'])==2,'two complete block exchange comparisons'",
        "for choice,declared in zip(['whole'],comparison['groups'],strict=True):\n        number=51":"for number,declared in zip([31,53],comparison['groups'],strict=True):\n        choice='whole'",
        "require(declared['block']==number and (choice=='whole' or declared['choice']==choice),'exact paired B51 comparison membership');groups=data['actual']['groups'] if choice=='whole' else [g for g in data['tail_actual']['groups'] if g['choice']==choice];old,new=groups":"require(declared['block']==number and declared['ordinary_default_input_case'] is True,'exact paired block/default-input membership');groups=data['B31_actual' if number==31 else 'B53_actual']['groups'];old,new=groups",
        "declared['normal_returns']":"declared['script_returns']",
        "require(declared['source_has_no_picture_orhide_sites'] and declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032'],'exact unforced four-speech path andoffline-only Charles scope')":"require(declared['opaque_effect_semantics_not_inferred_from_structural_preservation'] is True and declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']==(['DK4_MES_B31_R0013'] if number==31 else []),'exact unforced selected paths/short variant offline-only/opaque semantics uninferred')",
        "total_rgb==89 and [s['later_RGB_samples'] for s in summaries]==[89]":"total_rgb==68 and [s['later_RGB_samples'] for s in summaries]==[34,34]",
        "'89laterRGBpairs andboth initialized Hodram captain1 tails'":"'68laterRGBpairs andfour initialized Hodram captain1 snapshots'",
        "proof['total_actual_frames']==20002":"proof['total_actual_frames']==24004",
        "[g['later_RGB_differences'] for g in result['groups']]==[3] and [g['duration_differences'] for g in result['groups']]==[2],'all three laterRGB differences andtwo command-duration differences retained'":"[g['later_RGB_differences'] for g in result['groups']]==[0,0] and [g['duration_differences'] for g in result['groups']]==[0,0],'all measured laterRGB andcommand-duration comparisons retained'",
        "[list(map(int,['2294662370','3116913577']))],'unequal final PRNG retained despiteequal source-script boundary values without future-outcome inference'":"[list(map(int,['3325064553','3325064553']))]*2,'equal measured final PRNG values retained without future-outcome inference'",
        'all_source_qualified_query_branch_path_andunvisited_Charles_scope_checked':'all_source_qualified_unforced_paths_andunvisited_short_B31_scope_checked',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        all_original_native_state_models_persistentobjects_tasks_calendar_wholeactors_captain_RNG_RGB_andreadonly_guards_preserved=True,
        both_complete_wholeblock_pairs_all_three_decodedlength_differences_andzero_measured_duration_UI_RNG_followingdifferences_bound=True,
        all68_later_full_RGBpairs_andfour_complete_final_snapshots_recomputed=True,
        no_capture_orproducer_replay_no_ROMcommit_orcredit=True,new_credit=0,full_goal_complete=False))
