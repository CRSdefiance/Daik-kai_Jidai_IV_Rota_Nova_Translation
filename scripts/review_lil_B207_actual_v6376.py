"""Record the five viewed English/paired sheets without claiming simulation equality."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_actual_review_v6376')
ACTUAL=Path('work/analysis/lil_B207_actual_v6374/all13_English_panels_complete_native_holds24_commands_and_source_comparison.json')
LATER=Path('work/analysis/lil_B207_later_v6375/original_final_native_getters_and_all_six_prompt_differences.json')
if __name__=='__main__':
    assert not ROOT.exists();a,s=read(ACTUAL),read(LATER)
    assert a['actual_unique_speech_panels']==a['actual_English_speech_observations']==13 and a['complete_native_text_and_nameplate_holds']==51
    assert not any(a[k] for k in ['failures','offline_only_display_IDs','command_result_differences','command_UI_word_differences','paired_nontext_region_differences'])
    assert a['all_jobs_terminal_and_reaped'] and a['source_and_English_all24_commands15_source_plus9_initializers_observed']
    assert len(a['command_timing_differences'])==13 and len(a['command_RNG_differences'])==3 and len(a['later_whole_RGB_differences'])==6
    assert s['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and all(s['five_native_component_equality'].values()) and s['whole_actor_and_captain_equal']
    assert not s['final_PRNG_equal'] and s['final_PRNG_seeds']==[940971730,2496127907]
    assert s['all_postscene_differences_inside_advance_prompt_rectangle'] and not s['broad_later_RGB_differences']
    sheets=[*a['review_sheets'],*a['transition_sheets'],s['review_sheet']];assert len(sheets)==5
    for r in sheets:
        assert sha(Path(r['path']).read_bytes())==r['sha256'];r.update(viewed=True,viewed_after_image_return=True)
    assert [v['exit_frame'] for v in a['versions']]==[5976,5974]
    assert all(h['both_versions_in_same_semantic_speech_at_this_frame'] and h['paired_upper_portrait_name_region_equal'] for r in a['actual_panels'] for h in r['holds'])
    ROOT.mkdir(parents=True)
    save(ROOT/'viewed13_panels51_native_holds_and_honest_timing_RNG_prompt_scope.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),postscene_native_state_proof=str(LATER),postscene_native_state_proof_sha256=sha(LATER.read_bytes()),viewed_sheets=sheets,visual_review_pending=False,
        all13_complete_English_and_current_style11_nameplates_visually_approved=True,no_open_translation_specific_display_control_or_return_finding=True,
        source_exit_frame=5976,English_exit_frame=5974,normal_port_return_frame=6070,final11001_both_following_B120_still_active_black_upper=True,
        all13_timing_three_interval_RNG_six_prompt_RGB_and_final_PRNG_differences_retained=True,
        five_measured_native_groups_whole_actor_and_captain_equal_not_whole_state=True,final_PRNG_equal=False,final_PRNG_seeds=s['final_PRNG_seeds'],
        broad_postscene_full_RAM_future_world_equivalence_unproven=True,no_complete_timing_or_RNG_cause_claim=True,
        original_A000_observed_not_full_quest_inventory_or_eligibility_proof=True,natural_event207_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed=True,
        only_B22_complete_scene_fixture_with_nine_original_initializers_and_identical_ordinary_inputs=True,no_forced_conditions_roster_funds_RNG_results_RAM_battery_or_savestate=True,
        new_English_cold_boots=1,new_English_frames=11001,reused_source_frames=11001,total_paired_frames=22002,all_jobs_terminal_and_reaped=True,
        no_new_boot_pixel_mask_edit_retiming_or_duplicate_editorial_credit=True,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,LATER,Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    print('Viewed13 panels/51 native holds;all24 commands and return approved. Timing/RNG/prompt and final-seed differences retained;no full-world equality claim.')
