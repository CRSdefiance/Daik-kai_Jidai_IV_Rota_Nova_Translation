"""Record the viewed paired title/notice sheet and retain all measured differences."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_actual_review_v6087')
ACTUAL=Path('work/analysis/shachihoko_B204_card_actual_v6084c/complete_source_path_and_unmasked_title_acquisition_prompt_frame_differences.json')
GLYPHS=Path('work/analysis/shachihoko_actual_name_glyphs_v6086/four_native_planes_and_all_actual_title_notice_holds_match.json')
if __name__=='__main__':
    assert not ROOT.exists();a,g=map(read,[ACTUAL,GLYPHS]);picture=Path(a['selected_sheet']);assert sha(picture.read_bytes())==a['selected_sheet_sha256'] and len(g['cases'])==4
    counts={k:sum(bool(r['measured_difference_pixel_counts'][k]) for r in a['whole_frames_with_measured_differences']) for k in ['item_title','acquisition_notice_text','advance_prompt']}
    ROOT.mkdir(parents=True);save(ROOT/'viewed_actual_title_acquisition_notice_and_measured_scope.json',dict(viewed=True,sheet=str(picture),sheet_sha256=sha(picture.read_bytes()),selected_six_actual_full_screen_panels_viewed=True,
        all_native_complete_title_and_notice_masks_pass=True,actual_nameplate_Lil_and_Jam_item_image_category_and_other_UI_preserved=True,
        actual_four_plane_hold_counts=[dict(case=r['case'],kind=r['kind'],holds=len(r['all_actual_holds'])) for r in g['cases']],
        whole_frames_compared=a['whole_frames_compared'],whole_frames_equal=a['whole_frames_equal'],measured_difference_frame_classes=counts,
        parent_target_scene_ends=[a['source_parent_end_return_frame'],a['target_end_return_frame']],timing_or_RNG_differing_completed_pairs=len(a['command_timing_and_interval_RNG_differences']),
        command_duration_changes=a['command_duration_changes'],all_measured_completed_paths_results_and_lengths_equal=True,
        no_mask_retiming_full_RAM_future_RNG_or_complete_causal_equivalence_claim=True,
        generated_acquisition_notice_is_not_a21st_stored_B204_speech_or_new_generic_notice_approval=True,
        initialized_Amsterdam_B22_fixture_not_natural_event_activation_original_location_or_earned_item=True,
        item_description_COMMON2931_active_staged_copy_and_item_list_consumer_review_still_pending=True,
        current_registered_candidate_and_main_unchanged=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,GLYPHS,Path(__file__)]}))
    print(dict(viewed=True,difference_classes=counts,scene_ends=[a['source_parent_end_return_frame'],a['target_end_return_frame']],no_release_or_credit=True))
