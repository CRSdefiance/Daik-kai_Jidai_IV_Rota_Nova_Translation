"""Prepare the exact conditional source/native/actual seal with measured B190 facts."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_seal_preparation_v5343')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/seal_lil_B186_references_v5172.py');target=Path('scripts/seal_lil_B190_references_v5343.py');text=source.read_text(encoding='utf-8')
    row=derive(source,target,{
        'B186':'B190','prepare_lil_B186_research_v5160':'prepare_lil_B190_research_v5331','reference_approval_v5172':'reference_approval_v5343',
        'editorial_manuscript_v5':'editorial_manuscript_v3','editorial_manuscript_v6':'editorial_manuscript_v4',
        'reference_census_v5163/all24_commands':'reference_census_v5334/all29_commands',
        'relocated_controls_v5165/all12_dispatches':'relocated_controls_v5336/all17_dispatches',
        'stored_v5158/all12_final_stored_targets48_macro':'stored_v5329/all17_final_stored_targets68_macro',
        'ends_v5164':'ends_v5335','actual_v5169/actual_all12':'actual_v5340b/actual_all17','display_fixture_v5166':'display_fixture_v5337',
        'actual_review_v5170/all12_panels_20_fullscreens':'actual_review_v5341b/all17_panels_16_fullscreens',
        'all24_structural_commands':'all29_structural_commands','all12_active_speech':'all17_active_speech',
        'one700_predicate':'one500_predicate','all5_mapped_structural_paths_preserve_all12_speeches':'all5_mapped_structural_paths_preserve_all17_speeches',
        'progressive11_impersonal':'progressive16_impersonal','single_end646_target578':'single_end602_target698',
        'all24_clean_current_target':'all29_clean_current_target',"len(control['relocated_dispatch_cases'])==12":"len(control['relocated_dispatch_cases'])==17",
        'predicate700_v5159/all12_aligned_and_unaligned_original700':'predicate500_v5330/all12_aligned_original500',
        "sum(r['operand_pointer_unaligned'] for r in scratch['cases'])==4":"sum(r['operand_pointer_unaligned'] for r in scratch['cases'])==0",
        "len(stored['final_target_parity_cases'])==12 and stored['current_final_stored_macro_alignment_cases']==48":"len(stored['final_target_parity_cases'])==17 and stored['current_final_stored_macro_alignment_cases']==68",
        '==(36,12)':'==(40,28)','all12_final_targets':'all17_final_targets',
        "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==12":"actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==17",
        '==[5735,5737]':'==[6934,6937]',"{'clean_Japanese':[560],'reviewed_English':[560]}":"{'clean_Japanese':[52],'reviewed_English':[52]}",
        'dict(total=10,speech=4,control_or_end=6)':'dict(total=9,speech=7,control_or_end=2)',
        "len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==4":"len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==2",
        '[(6490,[225,371,239,376]),(6670,[225,371,239,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]':'[(7690,[225,371,239,376]),(7870,[225,371,239,376])]',
        '[1803218166,2467799992]':'[2467799992,2467799992]',"and not visual['PRNG_equality']":"and visual['PRNG_equality']",
        "len(visual['all_actual_consumer_sheets_viewed'])==2 and len(visual['paired_full_screen_views'])==5":"len(visual['all_actual_consumer_sheets_viewed'])==3 and len(visual['paired_full_screen_views'])==4",
        'source_all24_commands':'source_all29_commands','all33_stored_fixture_commands':'all38_stored_fixture_commands','==33 for f':'==38 for f',
        'len(set(ids))==12':'len(set(ids))==17','all12_panels_eleven_progressive':'all17_panels_sixteen_progressive',
        'source_all24_commands_six_branches':'source_all29_commands_six_branches',
        'original_scene_predicate_results_equal_draws_seeds_timing_and_indicator_differences_disclosed':'original_scene_result2_carried_through_UI_and_end_timing_shadow_differences_disclosed',
        "block['block']==checked['block']==186 and len(block['command_map'])==24 and len(block['text_records'])==12":"block['block']==checked['block']==190 and len(block['command_map'])==29 and len(block['text_records'])==17",
        '==[(646,578)]':'==[(602,698)]','all12_source_native_reference':'all17_source_native_reference','references sealed:12 actual panels':'references sealed:17 actual panels',
        "    paths=[INPUT,PLAN,CENSUS":"    carry=Path('work/analysis/lil_B190_carried_result_v5340b/all15_C200_and15_end_prior_result_cases.json');carried=read(carry)\n    assert len(carried['cases'])==15 and visual['original_carried_result2_C200_3_2_and_end_0_2_preserved']\n    layout=Path('work/analysis/lil_B190_relocation_tools_v5328/viewed_layout_retention_reasons.json')\n    assert read(layout)['all17_panels_on_three_native_sheets_viewed_after_image_return']\n    paths=[carry,layout,INPUT,PLAN,CENSUS",
        "    for key,path in [('reference_map',MAP)":"    for key,path in [('layout_retention_review_proof',layout),('carried_result_proof',carry),('reference_map',MAP)",
    })
    before,after=native_numbers(text),native_numbers(target.read_text(encoding='utf-8'))
    assert before-after==Counter({1803218166:1}) and after-before==Counter({2467799992:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_native_actual_seal.json',dict(derivation=row,
        only_high_integer_change_is_measured_final_PRNG_data=True,carried_result_and_individual_layout_proofs_bound=True,
        no_native_address_or_constant_changed=True,no_review_credit=True,full_goal_complete=False))
