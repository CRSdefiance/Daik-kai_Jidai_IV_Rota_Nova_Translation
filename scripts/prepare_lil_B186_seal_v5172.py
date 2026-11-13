"""Prepare the source/native/reference/actual seal with measured B186 facts."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_seal_preparation_v5172')
if __name__=='__main__':
    assert not ROOT.exists()
    a=Path('scripts/seal_lil_B182_references_v4909b.py');b=Path('scripts/seal_lil_B186_references_v5172.py')
    row=derive(a,b,{
        'B182':'B186','prepare_lil_B182_research_v4897':'prepare_lil_B186_research_v5160',
        'reference_approval_v4909':'reference_approval_v5172','editorial_manuscript_v3':'editorial_manuscript_v5','editorial_manuscript_v4':'editorial_manuscript_v6',
        'reference_census_v4900/all25_commands_ten_relative_sites':'reference_census_v5163/all24_commands_six_relative_sites',
        'relocated_controls_v4902/all8_dispatches_two_RNG_predicates_three_effects_C200_and25_mapped_paths':
        'relocated_controls_v5165/all12_dispatches_one_RNG_predicate_three_effects_C200_and5_mapped_paths',
        'stored_v4894/all8_final_stored_targets32_macro_cases':'stored_v5158/all12_final_stored_targets48_macro_cases',
        'ends_v4901/two_declared_tail_end_decodes_ten_relative_sites':'ends_v5164/two_declared_tail_end_decodes_six_relative_sites',
        'actual_v4906/actual_all8':'actual_v5169/actual_all12','display_fixture_v4903':'display_fixture_v5166',
        'actual_review_v4907/all8_panels_48_fullscreens_conditional_return_and_measured_differences_v2':'actual_review_v5170/all12_panels_20_fullscreens_conditional_return_and_measured_differences',
        'all25_structural_commands_verified':'all24_structural_commands_verified','all8_active_speech_targets':'all12_active_speech_targets',
        'all7_nonrelative_leaves_two500_predicates':'all6_nonrelative_leaves_one700_predicate',
        'all10_relative_sites_and50_native_skip_cases':'all6_relative_sites_and30_native_skip_cases',
        'all25_mapped_structural_paths_preserve_all8_speeches':'all5_mapped_structural_paths_preserve_all12_speeches',
        'progressive7_impersonal_FE1':'progressive11_impersonal_FE1','single_end632_target648':'single_end646_target578',
        'all25_clean_current_target_commands_and_ten_relative_sites':'all24_clean_current_target_commands_and_six_relative_sites',
        "len(control['relocated_dispatch_cases'])==8 and len(control['all7_exact_nonrelative_leaves'])==7":
        "len(control['relocated_dispatch_cases'])==12 and len(control['all6_exact_nonrelative_leaves'])==6",
        "len(control['predicate_pairs'])==2":"len(control['predicate_pairs'])==1",
        "len(control['all25_source_and_relocated_structural_paths_identical'])==25":"len(control['all5_source_and_relocated_structural_paths_identical'])==5",
        'predicate500_v4896/all24_aligned_and_unaligned_original500':'predicate700_v5159/all12_aligned_and_unaligned_original700',
        "len(scratch['cases'])==24 and scratch['unforced_cases']==6 and scratch['CPU_only_boundary_fixture_cases']==18":
        "len(scratch['cases'])==12 and scratch['unforced_cases']==3 and scratch['CPU_only_boundary_fixture_cases']==9",
        "for r in scratch['cases'])==8":"for r in scratch['cases'])==4",
        "len(stored['final_target_parity_cases'])==8 and stored['current_final_stored_macro_alignment_cases']==32":
        "len(stored['final_target_parity_cases'])==12 and stored['current_final_stored_macro_alignment_cases']==48",
        '==(16,16)':'==(36,12)','all8_final_targets':'all12_final_targets',
        "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==8":
        "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==12",
        '==[4776,4775]':'==[5735,5737]',"{'clean_Japanese':[532],'reviewed_English':[532]}":"{'clean_Japanese':[560],'reviewed_English':[560]}",
        'dict(total=13,speech=7,control_or_end=6)':'dict(total=10,speech=4,control_or_end=6)',
        "len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==18":"len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==4",
        "assert all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in visual['sampled_postscene_whole_RGB_differences_unmasked'])":
        "assert [(r['frame'],r['whole_frame_difference_bbox']) for r in visual['sampled_postscene_whole_RGB_differences_unmasked']]==[(6490,[225,371,239,376]),(6670,[225,371,239,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]",
        '[3723009301,403514907]':'[1803218166,2467799992]',
        "len(visual['paired_full_screen_views'])==12":"len(visual['paired_full_screen_views'])==5",
        "s['viewed']":"s['viewed_after_image_return']",
        'source_all25_commands_preserved':'source_all24_commands_preserved','all34_stored_fixture_commands':'all33_stored_fixture_commands','==34 for f':'==33 for f',
        'len(set(ids))==8':'len(set(ids))==12',
        'all8_panels_seven_progressive_one_FE':'all12_panels_eleven_progressive_one_FE',
        'source_all25_commands_ten_branches_two_predicates':'source_all24_commands_six_branches_one_predicate',
        'original_scene_RNG_outcome_equal_final_RNG_and_timing_indicator_differences_disclosed':
        'original_scene_predicate_results_equal_draws_seeds_timing_and_indicator_differences_disclosed',
        "block['block']==checked['block']==182 and len(block['command_map'])==25 and len(block['text_records'])==8":
        "block['block']==checked['block']==186 and len(block['command_map'])==24 and len(block['text_records'])==12",
        "len(block['relative_skip_fixups'])==10 and len(block['target_native_skip_cases'])==50":
        "len(block['relative_skip_fixups'])==6 and len(block['target_native_skip_cases'])==30",
        '==[(632,648)]':'==[(646,578)]','all8_source_native_reference':'all12_source_native_reference',
        'B182 references sealed:8 actual panels':'B186 references sealed:12 actual panels',
    })
    before,after=native_numbers(a.read_text(encoding='utf-8')),native_numbers(b.read_text(encoding='utf-8'))
    assert before-after==Counter({3723009301:1,403514907:1})
    assert after-before==Counter({1803218166:1,2467799992:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_source_native_actual_seal.json',dict(derivation=row,
        only_high_integer_literal_changes_are_two_measured_final_PRNG_values=True,
        source_and_target_native_command_addresses_unchanged=True,no_future_world_or_full_RAM_equivalence_claim=True,
        new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared exact B186 seal;only two measured PRNG data values change among high integer literals.')
