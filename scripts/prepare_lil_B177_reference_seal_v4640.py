"""Prepare B177 reference approval with measured indicator/timing/PRNG scope."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_reference_seal_tools_v4640')
assert not ROOT.exists()
source=Path('scripts/seal_lil_B176_references_v4590.py')
text=source.read_text(encoding='utf-8')
start=text.index("    assert visual['representative_actual_coverage")
end=text.index("    assert fixture[",start)
old_visual=text[start:end]
new_visual="""    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all2_actual_sheets_viewed'])==2 and all(s['viewed'] for s in visual['all2_actual_sheets_viewed'])
    assert len(visual['paired_full_screen_views'])==3 and sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==12
    assert all(s['viewed'] for s in visual['paired_full_screen_views'])
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115
    assert not visual['nontext_difference_samples'] and visual['exact_timing_difference_counts']=={'total':11,'speech':9,'control_or_end':2}
    assert len(visual['actual_timing_differences'])==11
    differences=visual['fourteen_following_A_button_indicator_animation_differences_retained_unmasked']
    assert len(differences)==14 and visual['fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained']
    for row in differences:
        a,b,c,d=row['whole_frame_difference_bbox']
        assert 224<=a<c<=240 and 360<=b<d<=376 and row['frame']>=6010
    assert visual['whole_RGB_town5290_through5950_and_final9001_equal'] and visual['whole_RGB_final9001_equal']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['all_content_jobs_terminal'] and not visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[463267532,403514907]
    assert visual['future_world_equivalence_and_full_RAM_equality_not_claimed'] and visual['no_new_PRNG_causal_trace']
"""
tool=derive(source,'scripts/seal_lil_B177_references_v4640.py',{
    old_visual:new_visual,'B176':'B177','lil_B176':'lil_B177',
    'prepare_lil_B176_research_v4579':'prepare_lil_B177_research_v4629',
    'reference_approval_v4590':'reference_approval_v4640',
    "INPUT=Path('translations/lil_B176_editorial_manuscript_v3.json')":"INPUT=Path('translations/lil_B177_editorial_manuscript_v5.json')",
    "OUTPUT=Path('translations/lil_B176_editorial_manuscript_v4.json')":"OUTPUT=Path('translations/lil_B177_editorial_manuscript_v6.json')",
    'reference_census_v4582':'reference_census_v4632','relocated_controls_v4584':'relocated_controls_v4634',
    'stored_v4576':'stored_v4626','ends_v4583':'ends_v4633','actual_v4588':'actual_v4638',
    'display_fixture_v4585':'display_fixture_v4635','actual_review_v4589':'actual_review_v4639',
    '==(16,24)':'==(24,16)',
    "v['single_source_end386_actually_reached']":"v['single_source_end482_actually_reached']",
    "and v['fixture_exit_frame']==5256 for v in actual['versions']":"for v in actual['versions'])\n    assert [v['fixture_exit_frame'] for v in actual['versions']]==[5255,5257] # retained original timing" ,
    "    assert all(len(v['selected_B22_command_pairs'])==22 and v['single_source_end386_actually_reached']\n               and v['fixture_exit_frame']==5256 for v in actual['versions'])":
        "    assert all(len(v['selected_B22_command_pairs'])==22 and v['single_source_end482_actually_reached'] for v in actual['versions'])\n    assert [v['fixture_exit_frame'] for v in actual['versions']]==[5255,5257]",
    'source_end386_actual_target400_offline_and_fixture_end_actual':'source_end482_actual_target466_offline_and_fixture_end_actual',
    'all115_nontext_samples_and_all22_command_timings_equal':
        'all115_upper_portrait_name_samples_equal_and11_command_timing_differences_retained',
    'five_native_state_components_whole1A04_actor_captain2_and_PRNG_equal':
        'five_native_state_components_whole1A04_actor_captain2_equal_PRNG_difference_retained',
    'no_future_world_full_RAM_or_hardware_equality_claim':'no_PRNG_causal_trace_future_world_full_RAM_or_hardware_equality_claim',
    "block['block']==checked['block']==176":"block['block']==checked['block']==177",
    '==[(386,400)]':'==[(482,466)]','single_end386_actual_target400_offline':'single_end482_actual_target466_offline',
    'single_end386_actually_reached':'single_end482_actually_reached',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,native_planes=10,actual_sheets=2,paired_full_screens=12,
    upper_portrait_name_samples_equal=115,following_indicator_RGB_differences=14,exact_command_timing_differences=11,
    unequal_PRNG_and_full_RAM_future_world_limits_retained=True,no_editorial_credit_added=True,full_goal_complete=False))
