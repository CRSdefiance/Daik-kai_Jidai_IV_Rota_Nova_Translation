"""Prepare exact source/native/actual approval with no-effect scope and R64 wrap."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_seal_tools_v5393')
FLAGS=['all38_structural_commands_verified','all13_active_speech_targets_preserved',
    'all9_nonrelative_leaves_three_mixed_predicates_four_A000_C200_end_exact',
    'all16_relative_sites_and80_native_skip_cases_preserved','all125_mapped_structural_paths_preserve_all13_speeches_and_no_effect_paths',
    'progressive12_impersonal_FE1_and_FI0_FA0_FO0_preserved','single_end730_target676_preserved',
    'no_source2000_pause_2100_4100_resources_or_presentations','original_mixed_RNG_semantics_and_packed_effect_bytes_preserved',
    'source_and_target_prefix6_to128_byte_exact','exact_R64_source_prose_wrap_preserved',
    'representative_actual_display_controls_and_parent_return_approved']
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/seal_lil_B190_references_v5343.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index("\nif __name__",a)
    extra="""    wrap=Path(doc['source_bound_wrap_refinement_proof']);w=read(wrap)
    assert sha(wrap.read_bytes())==doc['source_bound_wrap_refinement_proof_sha256'] and w['only_changed_record_IDs']==['DK4_MES_B191_R0064']
    assert w['all13_words_controls_and_prose_unchanged'] and w['twelve_other_compiled_targets_exact'] and w['twelve_other_native_planes_exact']
    assert doc['exact_source_prose_R64_after_be_boundary_reviewed'] and not doc['no_record_specific_ordinary_boundary_exception_required']
    sourceblock=IlnkContainer.parse(NdsImage.open(PARENT).read_file('/data/SC2.DK4')).blocks[191]
    targetblock=IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks[191]
    assert sourceblock[6:128]==targetblock[6:128] and len(sourceblock)==736 and len(targetblock)==680
    assert plan['blocks'][0]['research_logical_end']==680 and plan['blocks'][0]['source_logical_end']==734
    assert visual['both_actual_rolls875_988_at8_76_return2_skip700_at28_and_apply_no_source_A000']
    assert visual['four_source_effect_alternatives_native_structural_only_not_actually_executed']
"""
    row=derive(source,'scripts/seal_lil_B191_references_v5393.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n','B190':'B191','prepare_lil_B190_research_v5331':'prepare_lil_B191_research_v5380','reference_approval_v5343':'reference_approval_v5393',
        'editorial_manuscript_v3':'editorial_manuscript_v4','editorial_manuscript_v4':'editorial_manuscript_v5',
        'reference_census_v5334/all29_commands_six_relative_sites':'reference_census_v5383/all38_commands_sixteen_relative_sites',
        'relocated_controls_v5336/all17_dispatches_one_RNG_predicate_three_effects_C200_and5_mapped_paths':'relocated_controls_v5385/all13_dispatches_three_RNG_predicates_four_effects_C200_and125_mapped_paths',
        'stored_v5329/all17_final_stored_targets68_macro':'stored_v5378b/all13_final_stored_targets52_macro',
        'ends_v5335/two_declared_tail_end_decodes_six_relative_sites':'ends_v5384/two_declared_tail_end_decodes_sixteen_relative_sites',
        'actual_v5340b/actual_all17_progressive_FE_RNG_effect':'actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect',
        'display_fixture_v5337':'display_fixture_v5386','actual_review_v5341b/all17_panels_16_fullscreens_conditional_return':'actual_review_v5390/all13_panels_20_fullscreens_no_effect_path_return',
        'all29_clean_current_target_commands_and_six_relative_sites':'all38_clean_current_target_commands_and_sixteen_relative_sites',
        "len(control['relocated_dispatch_cases'])==17 and len(control['all6_exact_nonrelative_leaves'])==6":"len(control['relocated_dispatch_cases'])==13 and len(control['all9_exact_nonrelative_leaves'])==9",
        "len(control['predicate_pairs'])==1":"len(control['predicate_pairs'])==3","len(control['A000_structural_pairs'])==3":"len(control['A000_structural_pairs'])==4",
        "len(control['all5_source_and_relocated_structural_paths_identical'])==5":"len(control['all125_source_and_relocated_structural_paths_identical'])==125",
        'predicate500_v5330/all12_aligned_original500_ownership_cases':'predicates_v5379/all36_original_mixed_predicate_ownership_cases',
        "len(scratch['cases'])==12 and scratch['unforced_cases']==3 and scratch['CPU_only_boundary_fixture_cases']==9":"len(scratch['cases'])==36 and scratch['unforced_cases']==9 and scratch['CPU_only_boundary_fixture_cases']==27",
        "len(stored['final_target_parity_cases'])==17 and stored['current_final_stored_macro_alignment_cases']==68":"len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52",
        '==(40,28)':'==(12,40)','all17_final_targets':'all13_final_targets',
        "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==17":"actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==13",
        '==[6934,6937]':'==[5977,5975]',"{'clean_Japanese':[52],'reviewed_English':[52]}":"{'clean_Japanese':[],'reviewed_English':[]}",
        'dict(total=9,speech=7,control_or_end=2)':'dict(total=12,speech=10,control_or_end=2)',
        "len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==2":"len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==4",
        '[(7690,[225,371,239,376]),(7870,[225,371,239,376])]':'[(6730,[225,371,239,376]),(6910,[225,371,239,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]',
        '[2467799992,2467799992]':'[759362961,1803218166]',"and visual['PRNG_equality']":"and not visual['PRNG_equality']", "len(visual['paired_full_screen_views'])==4":"len(visual['paired_full_screen_views'])==5",
        'source_all29_commands':'source_all38_commands','all38_stored_fixture_commands':'all47_stored_fixture_commands','==38 for f':'==47 for f','len(set(ids))==17':'len(set(ids))==13',
        'carried_result_v5340b':'carried_result_v5392','relocation_tools_v5328':'relocation_tools_v5377','all17_panels_on_three_native_sheets':'all13_panels_on_two_native_sheets',
        '    paths=[carry,layout,INPUT':extra+'    paths=[wrap,carry,layout,INPUT',
        'all17_panels_sixteen_progressive_one_FE_selected_effect':'all13_panels_twelve_progressive_one_FE_original_no_effect_path',
        'source_all29_commands_six_branches_one_predicate_three_alternative_effects':'source_all38_commands_16_branches_three_mixed_predicates_four_alternative_effects_and_no_effect_paths',
        'original_scene_result2_carried_through_UI_and_end_timing_shadow_differences_disclosed':'original_scene_two_unforced500_draws_skip700_and_no_A000_preserved',
        "block['block']==checked['block']==190 and len(block['command_map'])==29 and len(block['text_records'])==17":"block['block']==checked['block']==191 and len(block['command_map'])==38 and len(block['text_records'])==13",
        "len(block['relative_skip_fixups'])==6 and len(block['target_native_skip_cases'])==30":"len(block['relative_skip_fixups'])==16 and len(block['target_native_skip_cases'])==80",
        '==[(602,698)]':'==[(730,676)]','all17_source_native_reference':'all13_source_native_reference','references sealed:17 actual panels':'references sealed:13 actual panels',
    })
    before,after=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert before-after==Counter({2467799992:2}) and after-before==Counter({759362961:1,1803218166:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_mixed_predicate_no_effect_seal.json',dict(derivation=row,
        native_high_constants_preserved_except_measured_PRNG_data=True,no_effect_actual_scope_distinct_from_four_offline_alternatives=True,
        target680_logical680_no_tailzeros_and_source736_logical734_two_tailzeros_guarded=True,no_credit=True,full_goal_complete=False))
