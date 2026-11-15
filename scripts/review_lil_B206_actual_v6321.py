"""Record actually viewed B206 English panels, menus, returns and bounded later state."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_actual_review_v6321')
ACTUAL=Path('work/analysis/lil_B206_actual_v6319/all24_English_panels55_observations217_native_holds_five_menus_three_same_code_paths.json')
LATER=Path('work/analysis/lil_B206_later_v6320/unmasked_later_inventory_and_original_final_native_getters.json')
if __name__=='__main__':
    assert not ROOT.exists();d,later=map(read,[ACTUAL,LATER])
    assert not any(d[k] for k in ['failures','paired_nontext_region_differences','command_result_differences','command_UI_word_differences','offline_only_display_IDs'])
    assert (d['actual_unique_speech_panels'],d['actual_English_speech_observations'],d['complete_native_text_and_nameplate_holds'])==(24,55,217)
    assert len(d['actual_menu_cases'])==5 and sum(len(r['holds']) for r in d['actual_menu_cases'])==13
    assert all(r['actual_complete_dialogue_and_nameplate_observed'] and r['holds'] and all(h['all216x64_ink_gray_pixels_equal_complete_native_plane'] and h['complete_current_nameplate_glyphs_and_blank_guards_equal'] and h['both_versions_in_same_semantic_speech_at_this_frame'] and h['paired_upper_portrait_name_item_region_equal'] for h in r['holds']) for r in d['actual_panels'])
    assert all(r['actual_choice_label_order_selection_and_VM_return_bound'] and r['holds'] for r in d['actual_menu_cases'])
    assert [len(d[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[81,8,114]
    assert later['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and len(later['all_broad_later_samples'])==107 and len(later['prompt_bounded_samples'])==7
    assert len(later['command_duration_changes'])==6 and all(r['word']==0x4000 for r in later['command_duration_changes'])
    views=[]
    for s in d['review_sheets']+d['menu_sheets']+d['transition_sheets']+[later['representative_sheet']]:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];views.append({**s,'viewed':True,'viewed_after_image_return':True,'original_detail':True})
    assert len(views)==9
    evidence={**d['evidence'],**later['evidence'],str(ACTUAL):sha(ACTUAL.read_bytes()),str(LATER):sha(LATER.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    acquisition=[]
    for folder in ['shady_man_source_v6262_buy','lil_B206_English_v6313_buy']:
        p=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder/'frame_007860_cold_boot.png'
        acquisition.append(dict(path=str(p),sha256=sha(p.read_bytes()),frame=7860,viewed=True,viewed_after_image_return=True));evidence[str(p)]=sha(p.read_bytes())
    assert acquisition[0]['sha256']==acquisition[1]['sha256']
    measured=later['paired_final_state_measurements']
    assert [r['path'] for r in measured]==['buy','high_price','pitch_refusal']
    assert all(r['five_native_component_equality']['state'] and r['five_native_component_equality']['tasks'] for r in measured)
    assert all(not r['five_native_component_equality'][k] for r in measured[:2] for k in ['models','persistent_objects','calendar'])
    assert all(not r['whole_actor_and_captain_equal'] and not r['PRNG_equal'] for r in measured[:2])
    assert all(measured[2]['five_native_component_equality'].values()) and measured[2]['whole_actor_and_captain_equal'] and measured[2]['PRNG_equal']
    assert all(d[k] for k in ['all_command_paths_and_results_preserved','source_and_English_all51_commands42_source_plus9_initializers_observed','source_and_English_same_ARM9_COMMON_components_all_other_files_all335_other_blocks_and_input_schedules','all_jobs_terminal_and_reaped','no_capture_masking_pixel_edit_or_retiming'])
    for p,h in evidence.items():assert sha(Path(p).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'viewed24_panels_four_labels_three_paths_and_measured_later_scope.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),later_inventory=str(LATER),later_inventory_sha256=sha(LATER.read_bytes()),viewed_sheets=views,viewed_acquisition_frames=acquisition,
        visual_review='Viewed all24 English speech panels,all five menu visits on the full menu sheet,and all three source/English menu/port/final transition sheets. Qualified legend and charm claims remain the seller\'s pitch;Cristina\'s personal intent,friendship/gift/information reasoning,9000-gold asking price,acceptance and distinct price/pitch refusals remain coherent. All217 complete dialogue and current nameplate holds match native masks;Shady Man,Cristina Erneco and Lil Argot are complete and readable. All four labels and five visible chosen outcomes preserve original indices and branch associations,including the complete first T and final periods of That\'s expensive.... No clipping,lost glyph,unintended page,blank dialogue page or authored premature break found. Item138 Ceramic Earrings/Gift/dash is readable. Both acquisition frames7860 are byte-identical and show Ceramic Earrings acquired!. These unchanged generated/item consumers receive no duplicate source-object credit. All paths return through port/resupply/following B120 to ordinary sailing;pitch-refusal final shows the same readable Sailor warning Water has run out! in both versions.',
        later_review='Preserved all114 unmodified same-frame whole-RGB differences:seven advance-prompt-bounded samples and107 broader samples. Viewed representative earliest,middle and final broad pairs for both affected paths on an additional six-pair sheet. Buy first broad pair12720 preserves the readable departure log;high-price first broad pair8400 preserves port,with bird movement differing. Later both affected paths sail normally;clouds,lighting,wind and supply counts differ. Native exported final calendar ticks differ1316/1321 for buy and1105/1109 for high-price;their queried models,persistent objects,whole actor and PRNG also differ. Final state/tasks and queried cash34900 agree on all paths. Pitch-refusal has no later whole-RGB differences and all five queried components,whole actor,captain and PRNG agree at16001. These scoped measurements do not prove whole RAM or future simulation equality. Six scene-duration differences are all progressive speech intervals;the source opaque command bytes and command results are exact. No complete causal explanation of later timing/RNG/world differences is certified;all remain explicit for the later technical re-audit.',
        actual_unique_speech_panels=24,actual_speech_observations=55,complete_native_speech_and_nameplate_holds=217,actual_menu_visits=5,complete_menu_holds=13,offline_only_display_IDs=[],
        all51_commands42_original_plus9_initializers_observed=True,all_original_command_paths_words_and_results_equal=True,
        paired_command_timing_differences=d['command_timing_differences'],command_duration_changes=later['command_duration_changes'],within_scene_RNG_differences=d['command_RNG_differences'],postscene_RGB_differences=d['later_whole_RGB_differences'],postscene_difference_bounds=later['postscene_difference_bounds'],paired_final_state_measurements=measured,
        native_getters_applied_to_exported_copies_only=True,no_new_emulator_boot_or_forced_state=True,no_pixels_masked_retimed_or_edited=True,no_causal_explanation_of_timing_RNG_or_world_differences_certified=True,broad_postscene_full_RAM_future_world_equivalence_unproven=True,
        original_source_asking9000_not_completed_debit_affordability_or_outer_event_proof=True,natural_event206_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed=True,
        no_open_translation_specific_display_menu_control_or_return_finding=True,representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_further_focus_run_required_by_current_distinct_display_findings=True,
        new_successful_English_runs=3,new_successful_English_frames=48003,new_same_code_source_refusal_runs=2,new_same_code_source_refusal_frames=32002,reused_same_code_source_buy_runs=1,reused_same_code_source_buy_frames=16001,total_paired_frames=96006,new_frames_this_phase=80005,
        terminal_reaped_tool_sessions=[9109,69272,3917,28638,53081,14449],all_jobs_terminal_and_reaped=True,all_failed_producers_and_intermediate_outputs_preserved=True,
        all207_name_role_alias_and_individual_Cristina_consumers_remain_open=True,visual_review_pending=False,new_editorial_credit=0,evidence=evidence,full_goal_complete=False))
    print('Nine sheets and two whole acquisition frames viewed;24 panels/55 observations/217 holds,four labels/five menu outcomes approved within disclosed scope. All measured later differences retained;registered integration next.')
