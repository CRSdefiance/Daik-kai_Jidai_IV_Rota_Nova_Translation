"""Approve six viewed sheets with explicit timing/RNG/broader-state limits."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_actual_review_v6433');ACTUAL=Path('work/analysis/lil_B208_actual_v6431/all24_English_panels_complete_native_holds38_commands_and_source_comparison.json');LATER=Path('work/analysis/lil_B208_later_v6432/all44_later_RGB_differences_original_final_getters_and_honest_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();a,s=read(ACTUAL),read(LATER);assert a['actual_unique_speech_panels']==a['actual_English_speech_observations']==24 and a['complete_native_text_and_nameplate_holds']==95
    assert not any(a[k] for k in ['failures','offline_only_display_IDs','command_result_differences','command_UI_word_differences','paired_nontext_region_differences'])
    assert a['all_jobs_terminal_and_reaped'] and a['source_and_English_all38_commands29_source_plus9_initializers_observed'] and [v['exit_frame'] for v in a['versions']]==[8616,8616]
    assert [len(a[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[16,18,44]
    assert s['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and s['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False) and not s['whole_actor_and_captain_equal'] and not s['final_PRNG_equal'] and s['final_PRNG_seeds']==[4024327688,3039668243]
    assert len(s['broader_later_differences'])==44 and not s['prompt_bounded_later_differences'] and len(s['command_duration_changes'])==8 and all(r['word']==0x4000 for r in s['command_duration_changes'])
    assert [v['components']['calendar']['ticks'] for v in s['native_values']]==[1008,1005]
    sheets=[*a['review_sheets'],*a['transition_sheets'],s['review_sheet']];assert len(sheets)==6
    for r in sheets:assert sha(Path(r['path']).read_bytes())==r['sha256'];r.update(viewed=True,viewed_after_image_return=True)
    assert all(h['both_versions_in_same_semantic_speech_at_this_frame'] and h['paired_upper_portrait_name_region_equal'] and h['source_correct_nameplate_or_FE_absence_verified'] and h['all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane'] for r in a['actual_panels'] for h in r['holds'])
    fe=[r for r in a['actual_panels'] if r['prefix']==254];assert len(fe)==1 and fe[0]['source_record_index']==90 and len(fe[0]['holds'])==4 and fe[0]['name'] is None
    assert all(not h['nameplate_expected'] and h['FE_null_actor_absent_nameplate_region_matches_source'] for h in fe[0]['holds'])
    assert all(v['B208_exit']==8616 and len(v['B120_ends'])==1 and v['B120_ends'][0]['frame']==13414 for v in s['observed_scene_and_following_ends'])
    ROOT.mkdir(parents=True);save(ROOT/'viewed24_panels95_holds_thought_FE_and_honest_broader_later_scope.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),postscene_native_state_proof=str(LATER),postscene_native_state_proof_sha256=sha(LATER.read_bytes()),viewed_sheets=sheets,visual_review_pending=False,
        all24_complete_English23_progressive_one_FE_and_current_style11_names_visually_approved=True,all91_progressive_name_holds_and4_portraitless_named_FE_notice_holds_complete=True,private_thought_parentheses_and_separate_Cristina_Charm_plus1_FE_notice_preserved=True,no_open_translation_specific_display_control_or_return_finding=True,
        source_exit_frame=8616,English_exit_frame=8616,normal_port_return_frame=8710,following_B120_end_frame=13414,final16001_both_sailing_viewed=True,
        all16_timing18_RNG44_broader_RGB_eight_duration_and_different_final_state_witnesses_retained=True,
        state_and_tasks_equal_models_persistent_objects_calendar_actor_and_PRNG_differ=True,calendar_ticks=[1008,1005],final_PRNG_equal=False,final_PRNG_seeds=s['final_PRNG_seeds'],
        broader_first_middle_final_pairs_show_readable_departure_and_sailing_with_supply_cloud_lighting_and_weather_differences=True,
        broad_postscene_full_RAM_future_world_equivalence_unproven=True,no_complete_timing_RNG_or_world_difference_cause_claim=True,
        original6005_632E_two_A000_observed_not_full_stat_quest_inventory_or_eligibility_proof=True,natural_event208_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed=True,
        only_B22_complete_scene_fixture_with_nine_original_initializers_and_identical_ordinary_inputs=True,no_forced_conditions_roster_funds_RNG_results_RAM_battery_or_savestate=True,
        new_English_cold_boots=1,new_English_frames=16001,reused_source_frames=16001,total_paired_frames=32002,English_session80454_terminal_and_reaped=True,all_jobs_terminal_and_reaped=True,
        all_measured_later_differences_preserved_for_older_record_technical_reaudit=True,no_new_boot_pixel_mask_edit_retiming_or_duplicate_editorial_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,LATER,Path(__file__)]},new_review_credit=0,full_goal_complete=False));print('Viewed24 panels/95 complete holds/six sheets:thought,FE literal name/Charm+1,all38 results and town/sailing approved.16 timing/18 RNG/44 broader RGB and different final states explicitly retained.')
