"""Derive B178 atomic compilation with exact approved measurements, controls and names."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_compiler_tools_v4699');assert not ROOT.exists()
source=Path('dk4tool/patch/lil_B177_editorial_v1.py');text=source.read_text(encoding='utf-8')
doc=read('translations/lil_B178_editorial_manuscript_v4.json');visual=read(doc['postscene_native_state_proof'])
assert sha(Path(doc['postscene_native_state_proof']).read_bytes())==doc['postscene_native_state_proof_sha256']
timings=[(r['source']['original_source_offset'],r['source']['start'],r['source']['returned'],r['English']['start'],r['English']['returned'])
    for r in visual['actual_timing_differences']]
assert len(timings)==14 and visual['exact_timing_difference_counts']=={'total':14,'speech':12,'control_or_end':2}
a=text.index("    require(sample['all115_upper_");b=text.index('    actual_paths=',a)
actual="""    require(sample['all115_upper_portrait_name_samples_equal_and14_command_timing_differences_retained']
        and sample['five_native_state_components_whole1A04_actor_captain2_and_PRNG3306586022_equal']
        and sample['no_PRNG_causal_trace_future_world_full_RAM_or_hardware_equality_claim'],'measured representative limits required')
    require(observed['all13_complete_held_planes_and_source_paired_regions_match'] and observed['all13_speeches12_progressive1_impersonal_FE_actually_observed']
        and len(observed['all115_sampled_nontext_region_checks'])==observed['nontext_equal_samples']==115 and not observed['nontext_difference_samples']
        and observed['sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames'] and observed['whole_RGB_final9001_equal']
        and set(observed['postscene9001_native_component_equality'])=={'state','models','persistent_objects','tasks','calendar'}
        and all(observed['postscene9001_native_component_equality'].values()) and observed['postscene9001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[3306586022,3306586022]
        and observed['all_content_jobs_terminal'],'actual planes/regions/five components/actor and equal PRNG scope required')
    timings=observed['actual_timing_differences']
    expected_timings="""+repr(timings)+"""
    require([(r['source']['original_source_offset'],r['source']['start'],r['source']['returned'],r['English']['start'],r['English']['returned'])
        for r in timings]==expected_timings and all(r['source']['original_source_offset']==r['English']['original_source_offset']
        and r['source']['word']==r['English']['word']==(0xC200 if r['source']['original_source_offset']==488
            else 0 if r['source']['original_source_offset']==490 else 0x4000) for r in timings)
        and observed['exact_timing_difference_counts']=={'total':14,'speech':12,'control_or_end':2},
        'all fourteen exact command timings must remain disclosed')
    indicator=observed['sampled_postscene_whole_RGB_differences_unmasked']
    require([(r['frame'],r['whole_frame_difference_bbox']) for r in indicator]==[
        (6970,[224,360,240,371]),(7150,[224,360,240,371]),(7930,[224,360,240,376]),(8110,[224,360,240,376])]
        and all(r['upper_portrait_name_regions_equal'] and not r['whole_RGB_equal'] for r in indicator)
        and observed['all_four_following_indicator_differences_viewed_in_full_and_retained'] and observed['no_new_PRNG_causal_trace'],
        'all four unmasked indicator differences required')
    require(observed['source_A0008_C200488_single_end490_actually_executed'] and observed['future_world_equivalence_and_full_RAM_equality_not_claimed']
        and observed['following_scene_adds_no_editorial_credit'] and len(observed['paired_full_screen_views'])==4
        and all(s['viewed'] for s in observed['paired_full_screen_views']) and sum(len(s['frames'])*2 for s in observed['paired_full_screen_views'])==16,
        'actual source and following-scene/full-screen scope required')
"""
tool=derive(source,'dk4tool/patch/lil_B178_editorial_v1.py',{
    text[a:b]:actual,
    'lil_B177_layout_v3':'lil_B178_layout_v1','lil_B177':'lil_B178','B177':'B178',
    'SELECTORS={174,175,254}':'SELECTORS={166,167,168,254}',
    'all13_structural_commands':'all16_structural_commands','all10':'all13','progressive9_impersonal_FE1':'progressive12_impersonal_FE1',
    'single_end482_actual_target466_offline':'single_end490_actual_target452_offline',
    "len(native['cases'])==10 and native['current_original_macro_alignment_calls']==80":"len(native['cases'])==13 and native['current_original_macro_alignment_calls']==104",
    "(native['progressive_planes'],native['FE_planes'])==(9,1)":"(native['progressive_planes'],native['FE_planes'])==(12,1)",
    "('source_consumer_negative_controls',18)":"('source_consumer_negative_controls',20)",
    "len(stored['final_target_parity_cases'])==10 and stored['current_final_stored_macro_alignment_cases']==40":"len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52",
    "stored['new_parity_macro_alignment_cases']==24 and stored['exact_byte_identical_reused_macro_alignment_cases']==16":"stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==24",
    'all9_progressive_static_actors':'all12_progressive_static_actors',
    "ui['source_offset']==480 and ui['target_offset']==464":"ui['source_offset']==488 and ui['target_offset']==450",
    "[('current',482),('research',466)]":"[('current',490),('research',452)]",
    "expected_names={'174':'Owner','175':'Cook'}":"expected_names={'166':'Lady','167':'Lady','168':'Lady'}",
    'native_four_consumer_cases':'native_six_consumer_cases','len(namecases)==4':'len(namecases)==6',
    'four native name consumers':'six native name consumers','four read-only names':'six read-only names',
    'all10_panels9_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_town_return_pass':
        'all13_panels12_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_parent_return_pass',
    'original13_commands':'original16_commands','source_end482_actual_target466_offline_and_fixture_end_actual':'source_end490_actual_target452_offline_and_fixture_end_actual',
    "actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==10":"actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==13",
    '==[5255,5257]':'==[5977,5976]',"len(version['selected_B22_command_pairs'])==22 and len(version['selected_intervals'])==10":"len(version['selected_B22_command_pairs'])==25 and len(version['selected_intervals'])==13",
    'single_source_end482_actually_reached':'single_source_end490_actually_reached',
    "['original_source_offset']==482":"['original_source_offset']==490","['original_source_offset']==480":"['original_source_offset']==488",
    "len(sample['viewed_actual_sheets'])==2":"len(sample['viewed_actual_sheets'])==3",
    'len(rows)==len(set(ids))==10':'len(rows)==len(set(ids))==13',
    'ten exact records required':'thirteen exact records required',"=={'progressive':9,'system-FE':1}":"=={'progressive':12,'system-FE':1}",
    "=={'revise':5,'retain-wording':5}":"=={'revise':2,'retain-wording':11}",
    "mapping['blocks'][0]['block']==177":"mapping['blocks'][0]['block']==178",'[177]':'[178]',"row['block']==177":"row['block']==178",'block=177':'block=178',
    'end==486 and len(block)==488':'end==494 and len(block)==496','len(logical)==mapped(end)==470':'len(logical)==mapped(end)==456','len(target)==472':'len(target)==456',
    "len(commands)==13 and sum(c['word']==0x4000 for c in commands)==10":"len(commands)==16 and sum(c['word']==0x4000 for c in commands)==13",
    '==[(482,466)]':'==[(490,452)]',"exact=[(8,'00a0ffff01090fa1'),(480,'00c2'),(482,'00000000')]":"exact=[(8,'00a0ffff010002a1'),(488,'00c2'),(490,'00000000')]",
    'source_commands=13':'source_commands=16',
    'actual_two_retained_B22_fixtures_115_regions_equal_11_timings_14_indicator_differences_and_unequal_PRNG_disclosed_not_natural_source_activation':
        'actual_two_retained_B22_fixtures_115_regions_equal_14_timings_4_indicator_differences_and_equal_PRNG_disclosed_not_natural_source_activation',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,reviewed_actual_proof=doc['postscene_native_state_proof'],reviewed_actual_proof_sha256=doc['postscene_native_state_proof_sha256'],
    all_checks_readonly_until_single_replace_file=True,source496_logical494_target456_logical456=True,
    exact14_timings4_indicator_boxes_and_equal_PRNG_guarded=True,native104_stored52_fresh28_reused24_and51_negatives_bound=True,
    no_registry_builder_ROM_orledger_change=True,full_goal_complete=False))
print('Prepared B178 atomic compiler;source,three Lady names,six readonly paths and measured actual limits guarded.')
