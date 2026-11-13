"""Derive B176's atomic compiler from the offset/index-guarded predecessor."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_compiler_tools_v4593')
assert not ROOT.exists()
source=Path('dk4tool/patch/lil_B175_editorial_v2.py')
text=source.read_text(encoding='utf-8')
def section(start,end):
    a=text.index(start);return text[a:text.index(end,a)]
old_flags=section('FLAGS=','\n\ndef load')
old_controls=section("    require(len(controls['relocated_dispatch_cases'])", "    ui=controls[")
old_names=section("    require(names['approved_prose_names']", "    require(sample[")
old_actual=section("    require(sample[", "    require(len(native['review_sheets'])")
flags="""FLAGS=['all13_structural_commands_verified','all10_active_speech_targets_preserved',
    'all3_leaves_one_A000_C200_and_single_end_exact','single_declared_tail_endword_preserved',
    'progressive9_impersonal_FE1_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects',
    'no_source2000_pause','no_source_relative_sites_predicates_resources_or_presentations',
    'source_A000_raw_operand_bytes_preserved_without_inferred_semantics',
    'single_end386_actual_target400_offline','representative_shared_rules_approved']"""
controls="""    require(len(controls['relocated_dispatch_cases'])==10 and len(controls['all3_source_current_target_nonrelative_nonspeech_leaves'])==3
        and len(controls['relocated_C200_pairs'])==len(controls['relocated_A000_structural_pairs'])==1
        and controls['all9_progressive_static_actors1_impersonal_null_actor_FE_and_no_FI_FA_FO_exact']
        and controls['original_no_relative_predicate_pause_resources_presentations_or_typed_objects_preserved']
        and controls['single_end_preserved_actual_reachability_pending'] and controls['source_A000_packed_operand_semantics_not_inferred'],
        'relocated consumer/control scope required')
    effect=controls['relocated_A000_structural_pairs'][0]
    require(effect['source_offset']==effect['target_offset']==8 and len(effect['cases'])==2
        and effect['nondecode_effect_callee_bridged_zero_return_not_body_or_game_state_execution']
        and all(c['error'] is None and len(c['rows'])==1 and c['rows'][0]['word']==0xA000 and c['rows'][0]['native_extent']==8 for c in effect['cases']),
        'source A000 structural scope differs')
"""
names="""    expected_names={'174':'Owner','175':'Cook'}
    require(names['approved_prose_names']==names['progressive_nameplate_values']==names['full_catalogue_values']==expected_names,'source-bound role labels differ')
    namecases=names['native_four_consumer_cases']['rows']
    require(len(namecases)==4 and {r['actor_ID'] for r in namecases}==SELECTORS-{254}
        and all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in namecases),
        'four native name consumers required')
    require(all(r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring'
        and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in namecases),'four read-only names required')
"""
actual="""    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['content_frames_each']==9001 and sample['new_emulator_runs']==2
        and sample['all10_panels9_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_town_return_pass']
        and sample['original13_commands_and_single_declared_tail_endword_preserved'] and sample['no_B176_source_command_omitted']
        and sample['source_end386_actual_target400_offline_and_fixture_end_actual']
        and sample['original_B22_four_A000_initialization_commands_and_one_source_A000_retained']
        and sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_B176_source_events']==[]
        and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all10_complete_held_planes_and_source_paired_regions_match'] and observed['all10_speeches9_progressive1_impersonal_FE_actually_observed']
        and len(observed['all115_sampled_nontext_region_checks'])==observed['nontext_equal_samples']==115
        and not observed['nontext_difference_samples'] and not observed['actual_timing_differences']
        and observed['all_sampled_whole_RGB_from5290_through9001_equal'] and observed['whole_RGB_final9001_equal']
        and all(observed['postscene9001_native_component_equality'].values()) and observed['postscene9001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[403514907,403514907]
        and observed['all_content_jobs_terminal'],'actual planes/timing/state required')
    require(observed['source_A0008_C200384_single_end386_actually_executed'] and observed['future_world_equivalence_and_full_RAM_equality_not_claimed']
        and observed['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit'],'actual source and following-scene scope required')
    actual_paths=[p for p in sample['evidence'] if p.endswith('actual_all10_progressive_FE_A000_C200_and_single_end.json')]
    require(len(actual_paths)==1,'one exact actual proof required');actual=load(actual_paths[0])
    require(sha(Path(actual_paths[0]).read_bytes())==sample['evidence'][actual_paths[0]] and not actual['failures'] and not actual['paired_region_differences']
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==10 and actual['offline_only_display_IDs']==[]
        and len(actual['versions'])==2 and actual['frames_per_boot']==9001 and actual['actual_new_cold_boot_runs']==2,'two complete actual paths required')
    require([v['fixture_exit_frame'] for v in actual['versions']]==[5256,5256],'observed exits differ')
    for version in actual['versions']:
        require(len(version['selected_B22_command_pairs'])==22 and len(version['selected_intervals'])==10
            and sum(r['prefix']==254 for r in version['selected_intervals'])==1 and version['single_source_end386_actually_reached']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and version['selected_B22_command_pairs'][-1]['original_source_offset']==386
            and version['source_C200']['original_source_offset']==384 and version['source_C200']['result_words']==[3,0]
            and len(version['source_A000'])==1 and version['source_A000'][0]['original_source_offset']==8
            and version['source_A000'][0]['result_words']==[3,0],'actual source command scope differs')
"""
tool=derive(source,'dk4tool/patch/lil_B176_editorial_v1.py',{
    old_flags:flags,old_controls:controls,old_names:names,old_actual:actual,
    'lil_B175_layout_v1':'lil_B176_layout_v4','lil_B175':'lil_B176','B175':'B176',
    'SELECTORS={2,9,183,184,185,254}':'SELECTORS={174,175,254}',
    'all32_five_review_gates_true':'all10_five_review_gates_true',
    "len(native['cases'])==32 and native['current_original_macro_alignment_calls']==256":"len(native['cases'])==10 and native['current_original_macro_alignment_calls']==80",
    'all32_current_native_speech_planes_pass':'all10_current_native_speech_planes_pass',
    "(native['progressive_planes'],native['FE_planes'])==(23,9)":"(native['progressive_planes'],native['FE_planes'])==(9,1)",
    "('source_consumer_negative_controls',24),('source_macro_preservation_negatives',9)":"('source_consumer_negative_controls',18),('source_macro_preservation_negatives',3)",
    "len(stored['final_target_parity_cases'])==32 and stored['current_final_stored_macro_alignment_cases']==128":"len(stored['final_target_parity_cases'])==10 and stored['current_final_stored_macro_alignment_cases']==40",
    "stored['new_parity_macro_alignment_cases']==68 and stored['exact_byte_identical_reused_macro_alignment_cases']==60":"stored['new_parity_macro_alignment_cases']==16 and stored['exact_byte_identical_reused_macro_alignment_cases']==24",
    'all32_final_targets_complete_native_planes_equal_reviewed_planes':'all10_final_targets_complete_native_planes_equal_reviewed_planes',
    "ui['source_offset']==1700 and ui['target_offset']==1688":"ui['source_offset']==384 and ui['target_offset']==398",
    "ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==4":"ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2",
    'B175_second_end_finishes_declared_logical_end':'B176_single_end_finishes_declared_logical_end',
    'four guarded endword decodes required':'two guarded tail endword decodes required',
    "[('current',1702),('current',1706),('research',1690),('research',1694)]":"[('current',386),('research',400)]",
    "len(native['review_sheets'])==4 and len(sample['viewed_actual_sheets'])==6":"len(native['review_sheets'])==2 and len(sample['viewed_actual_sheets'])==2",
    'len(rows)==len(set(ids))==32':'len(rows)==len(set(ids))==10','32 exact records required':'ten exact records required',
    "=={'progressive':23,'system-FE':9}":"=={'progressive':9,'system-FE':1}",
    "=={'revise':19,'retain-wording':13}":"=={'revise':5,'retain-wording':5}",
    "mapping['blocks'][0]['block']==175":"mapping['blocks'][0]['block']==176",'[175]':'[176]',
    "row['block']==175":"row['block']==176",'block=175':'block=176',
    "require(macros=={b'FI':4,b'FA':1},'complete macro scope differs')":"require(not macros,'source has no FI/FA/FO substitutions')",
    'end==1710 and len(block)==1712':'end==390 and len(block)==392',
    'len(logical)==mapped(end)==1698':'len(logical)==mapped(end)==404','len(target)==1700':'len(target)==404',
    "len(commands)==39 and sum(c['word']==0x4000 for c in commands)==32":"len(commands)==13 and sum(c['word']==0x4000 for c in commands)==10",
    '==[(1702,1690),(1706,1694)]':'==[(386,400)]','both source endwords required':'single source tail endword required',
    "exact=[(8,'0060'),(10,'4463'),(72,'9646ca80'),(1264,'35467d80'),(1700,'00c2'),(1702,'00000000'),(1706,'00000000')]":
        "exact=[(8,'00a0ffff010a0da1'),(384,'00c2'),(386,'00000000')]",
    'seven exact leaves required':'three exact leaves required',
    '==[0x6000,0x6344,0x4696,0x4635,0xC200,0,0]':'==[0xA000,0xC200,0]',
    'source_commands=39':'source_commands=13',
    'all32_progressive_FE_speeches_FI4_FA1_three_presentations_resource_C200_and_both_ends_preserved':
        'all10_progressive_impersonal_FE_speeches_no_macros_A000_C200_and_single_end_preserved',
    'actual_two_retained_B22_fixtures_and_scoped_visual_differences_not_natural_source_activation':
        'actual_two_retained_B22_fixtures_all_nontext_timings_equal_not_natural_source_activation',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,source_commands=13,source_speeches=10,progressive=9,FE=1,
    leading_A000=1,C200=1,end=1,offset_and_NUL_index_reconstruction_guard_retained=True,
    only_after_all_checks_image_mutation=True,no_registry_builder_ROM_ledger_change=True,full_goal_complete=False))
