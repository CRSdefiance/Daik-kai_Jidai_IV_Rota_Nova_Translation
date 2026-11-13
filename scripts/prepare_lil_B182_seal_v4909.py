"""Prepare B182 reference sealing with measured differences and operand scratch bound."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    print(derive('scripts/seal_lil_B180_references_v4816.py','scripts/seal_lil_B182_references_v4909.py',{
        'B180':'B182','reference_approval_v4816':'reference_approval_v4909',
        'prepare_lil_B180_research_v4800':'prepare_lil_B182_research_v4897',
        'reference_census_v4803/all28':'reference_census_v4900/all25',
        'relocated_controls_v4805/all11':'relocated_controls_v4902/all8',
        'stored_v4799/all11_final_stored_targets44':'stored_v4894/all8_final_stored_targets32',
        'ends_v4804':'ends_v4901','actual_v4811c/actual_all11':'actual_v4906/actual_all8',
        'display_fixture_v4808':'display_fixture_v4903',
        'actual_review_v4812/all2_actual_sheets11_planes_fullscreens_and_resolved_effect_state':
        'actual_review_v4907/all8_panels_48_fullscreens_conditional_return_and_measured_differences_v2',
        'all28':'all25','all11':'all8','progressive10':'progressive7',
        'single_end572_target542':'single_end632_target648',
        "len(control['relocated_dispatch_cases'])==11":"len(control['relocated_dispatch_cases'])==8",
        "len(stored['final_target_parity_cases'])==11 and stored['current_final_stored_macro_alignment_cases']==44":
        "len(stored['final_target_parity_cases'])==8 and stored['current_final_stored_macro_alignment_cases']==32",
        '==(20,24)':'==(16,16)',"actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==11":
        "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==8",
        '==[5495,5496]':'==[4776,4775]',
        "visual['no_open_translation_specific_display_or_control_finding']":"visual['no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding']",
        "    assert visual['measured_persistent_town_difference_resolved_to_original_effect']":
        "    assert visual['observed_random_path_difference']['same_control_path']\n    assert visual['observed_random_path_difference']['original_effects_by_case']=={'clean_Japanese':[532],'reviewed_English':[532]}\n    assert visual['exact_timing_difference_counts']==dict(total=13,speech=7,control_or_end=6)\n    assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==18\n    assert all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in visual['sampled_postscene_whole_RGB_differences_unmasked'])\n    assert visual['postscene9001_PRNG_seeds']==[3723009301,403514907] and not visual['PRNG_equality']\n    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']\n    assert visual['whole_RGB_final9001_equal']",
        'all2_actual_sheets_viewed':'all_actual_consumer_sheets_viewed',
        "len(visual['paired_full_screen_views'])==9":"len(visual['paired_full_screen_views'])==12",
        "visual['total_frames']==30004 and visual['actual_new_cold_boot_runs']==4":"visual['total_frames']==18002 and visual['actual_new_cold_boot_runs']==2",
        'all37_stored_fixture_commands':'all34_stored_fixture_commands','==37 for f':'==34 for f',
        'len(set(ids))==11':'len(set(ids))==8',
        "Path(visual['effect_boundary_proof'])":"Path('work/analysis/lil_B182_predicate500_v4896/all24_aligned_and_unaligned_original500_ownership_cases.json')",
        'all11_panels_ten_progressive':'all8_panels_seven_progressive',
        'new_emulator_runs=4,total_frames=30004':'new_emulator_runs=2,total_frames=18002',
        "block['block']==checked['block']==180 and len(block['command_map'])==28 and len(block['text_records'])==11":
        "block['block']==checked['block']==182 and len(block['command_map'])==25 and len(block['text_records'])==8",
        '==[(572,542)]':'==[(632,648)]',
        'original_RNG_and_effect_state_difference_fully_disclosed_within_checked_scope=True':
        'original_scene_RNG_outcome_equal_final_RNG_and_timing_indicator_differences_disclosed=True',
        "source_FE_notice_remains_impersonal_and_alternative_A000_packed_operand_semantics_not_inferred":
        "source_FE_notice_remains_impersonal_and_alternative_A000_packed_operand_semantics_not_inferred",
        'references sealed:11 actual panels':'references sealed:8 actual panels'
    }))
