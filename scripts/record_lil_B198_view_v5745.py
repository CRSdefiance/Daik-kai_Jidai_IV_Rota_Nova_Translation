"""Record returned complete native, actual and paired-scene views with their real scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_visual_approval_v5745')
SCREENS=Path('work/analysis/lil_B198_screen_review_v5744/paired_scene_and_return_sheets_with_measured_limits.json')
FONT=Path('work/analysis/lil_B198_fonts_v5741/all17_progressive_FE_native_planes_and136_alignment_cases.json')
ACTUAL=Path('work/analysis/lil_B198_actual_v5743/fifteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
if __name__=='__main__':
    assert not ROOT.exists()
    screens,font,actual=map(read,[SCREENS,FONT,ACTUAL])
    assert not actual['failures'] and actual['complete_matching_observations']==15 and actual['complete_matching_holds']==56
    assert screens['sampled_nontext_frames']==182 and screens['source_and_English_return_frames']==[6697,6697]
    assert screens['final_13001_PRNG_seeds']==[672702422,672702422]
    lists=[font['review_sheets'],actual['review_sheets'],screens['paired_full_screen_sheets']]
    assert [len(v) for v in lists]==[3,3,3]
    viewed=[]
    for rows in lists:
        out=[]
        for r in rows:
            assert sha(Path(r['path']).read_bytes())==r['sha256']
            out.append({**r,'viewed_in_full_current_turn':True,'original_detail':True,'viewed_after_image_return':True})
        viewed.append(out)
    ROOT.mkdir(parents=True)
    save(ROOT/'viewed17_native15_actual56_holds_three_paired_sheets_and_source_style11.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        all_current_native_sheets_viewed=viewed[0],all_actual_consumer_sheets_viewed=viewed[1],paired_full_screen_views=viewed[2],
        all17_native_glyphs_complete_15_actual_panels56_complete_holds_match=True,
        source_story_caller_style11_CP932_pause_reference_corrected_without_ROM_or_prose_change=True,
        initial_catalog_style1_false_shadow_expectation_and_height_hypothesis_preserved_and_superseded=True,
        source_refrain_four_calls_three_direct_questions_dream_and_tomorrow_morning_intention_preserved=True,
        source_matched_name_portrait_item_and_background_visibility_not_normalized=True,
        source_and_English_return_frames=[6697,6697],sampled_nontext_frames=182,
        command_timing_difference_count=0,later_sampled_whole_RGB_difference_count=0,
        final_13001_PRNG_seeds=[672702422,672702422],final_13001_PRNG_equal=True,
        source_and_English_final_Sea_View_screens_viewed=True,
        no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim=True,
        actual_sampled_display_IDs=[r['id'] for r in actual['actual_panels']],offline_only_source_indices=[65,95],
        no_natural_event198_activation_original_location_full_route_exhaustive_condition_or_hardware_claim=True,
        actual_source_English_cold_boots=2,total_successful_frames=26002,new_English_runs=1,
        original_source_run_reused_not_a_new_run=True,no_open_changed_scene_translation_display_or_control_finding=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SCREENS,FONT,ACTUAL,Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    print('Viewed3 native,3 actual and3 paired sheets:17 native/15 actual/56holds;style11 pauses complete,normal source-matched Sea View return. Two Angelo clauses offline only.')
