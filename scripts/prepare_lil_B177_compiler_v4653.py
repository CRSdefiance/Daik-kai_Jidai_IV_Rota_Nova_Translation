"""Derive B177 atomic compilation with measured timing/RGB/PRNG limits enforced."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_compiler_tools_v4653')
assert not ROOT.exists()
source=Path('dk4tool/patch/lil_B176_editorial_v2.py')
text=source.read_text(encoding='utf-8')
start=text.index("    require(observed['all10_complete_held_planes")
end=text.index("    actual_paths=",start)
actual="""    require(sample['all115_upper_portrait_name_samples_equal_and11_command_timing_differences_retained']
        and sample['five_native_state_components_whole1A04_actor_captain2_equal_PRNG_difference_retained']
        and sample['no_PRNG_causal_trace_future_world_full_RAM_or_hardware_equality_claim'],'measured representative limits required')
    require(observed['all10_complete_held_planes_and_source_paired_regions_match'] and observed['all10_speeches9_progressive1_impersonal_FE_actually_observed']
        and len(observed['all115_sampled_nontext_region_checks'])==observed['nontext_equal_samples']==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_town5290_through5950_and_final9001_equal']
        and observed['whole_RGB_final9001_equal'] and all(observed['postscene9001_native_component_equality'].values())
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'] and not observed['PRNG_equality']
        and observed['postscene9001_PRNG_seeds']==[463267532,403514907] and observed['all_content_jobs_terminal'],
        'actual planes/regions/state and unequal PRNG scope required')
    timings=observed['actual_timing_differences']
    expected_timings=[(68,3095,3336,3095,3335),(118,3336,3573,3335,3576),
        (212,3573,3813,3576,3816),(248,3813,4053,3816,4056),(296,4053,4293,4056,4296),
        (316,4293,4534,4296,4536),(376,4534,4774,4536,4776),(392,4774,5014,4776,5016),
        (438,5014,5254,5016,5256),(480,5254,5255,5256,5257),(482,5255,5255,5257,5257)]
    require([(r['source']['original_source_offset'],r['source']['start'],r['source']['returned'],
        r['English']['start'],r['English']['returned']) for r in timings]==expected_timings
        and all(r['source']['original_source_offset']==r['English']['original_source_offset']
            and r['source']['word']==r['English']['word']==(0xC200 if r['source']['original_source_offset']==480
                else 0 if r['source']['original_source_offset']==482 else 0x4000) for r in timings)
        and observed['exact_timing_difference_counts']=={'total':11,'speech':9,'control_or_end':2},
        'all eleven exact command timings must remain disclosed')
    indicator=observed['fourteen_following_A_button_indicator_animation_differences_retained_unmasked']
    require([r['frame'] for r in indicator]==[6010,6190,7210,7390,7450,7630,7690,7870,8170,8350,8410,8590,8770,8950]
        and all(r['whole_frame_difference_bbox']==([224,370,240,376] if r['frame']==6010
            else [225,371,239,376] if r['frame']==6190 else [224,360,240,376])
            and r['upper_portrait_name_regions_equal'] and not r['whole_RGB_equal'] for r in indicator)
        and observed['fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained']
        and observed['no_new_PRNG_causal_trace'],'all fourteen unmasked indicator differences required')
    require(observed['source_A0008_C200480_single_end482_actually_executed'] and observed['future_world_equivalence_and_full_RAM_equality_not_claimed']
        and observed['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
        and len(observed['paired_full_screen_views'])==3 and all(s['viewed'] for s in observed['paired_full_screen_views'])
        and sum(len(s['frames'])*2 for s in observed['paired_full_screen_views'])==12,
        'actual source and following-scene/full-screen scope required')
"""
tool=derive(source,'dk4tool/patch/lil_B177_editorial_v1.py',{
    text[start:end]:actual,
    'lil_B176_layout_v4':'lil_B177_layout_v3','lil_B176':'lil_B177','B176':'B177',
    'single_end386_actual_target400_offline':'single_end482_actual_target466_offline',
    'source_end386_actual_target400_offline_and_fixture_end_actual':'source_end482_actual_target466_offline_and_fixture_end_actual',
    "stored['new_parity_macro_alignment_cases']==16 and stored['exact_byte_identical_reused_macro_alignment_cases']==24":
        "stored['new_parity_macro_alignment_cases']==24 and stored['exact_byte_identical_reused_macro_alignment_cases']==16",
    "ui['source_offset']==384 and ui['target_offset']==398":"ui['source_offset']==480 and ui['target_offset']==464",
    "[('current',386),('research',400)]":"[('current',482),('research',466)]",
    '==[5256,5256]':'==[5255,5257]',
    'single_source_end386_actually_reached':'single_source_end482_actually_reached',
    "['original_source_offset']==386":"['original_source_offset']==482",
    "['original_source_offset']==384":"['original_source_offset']==480",
    "mapping['blocks'][0]['block']==176":"mapping['blocks'][0]['block']==177",
    '[176]':'[177]',"row['block']==176":"row['block']==177",'block=176':'block=177',
    'end==390 and len(block)==392':'end==486 and len(block)==488',
    'len(logical)==mapped(end)==404':'len(logical)==mapped(end)==470',
    'len(target)==404':'len(target)==472',
    '==[(386,400)]':'==[(482,466)]',
    "exact=[(8,'00a0ffff010a0da1'),(384,'00c2'),(386,'00000000')]":
        "exact=[(8,'00a0ffff01090fa1'),(480,'00c2'),(482,'00000000')]",
    'actual_two_retained_B22_fixtures_all_nontext_timings_equal_not_natural_source_activation=True':
        'actual_two_retained_B22_fixtures_115_regions_equal_11_timings_14_indicator_differences_and_unequal_PRNG_disclosed_not_natural_source_activation=True',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,source488_logical486_target472_logical470=True,
    all_checks_readonly_until_single_replace_file=True,source_end482_target466=True,
    exact11_timing_pairs14_indicator_boxes_and_unequal_PRNG_seeds_guarded=True,
    native80_stored40_fresh24_reused16_and49_negatives_bound=True,
    no_registry_builder_ROM_orledger_change=True,full_goal_complete=False))
print('Prepared B177 atomic compiler with exact source and measured actual-difference guards.')
