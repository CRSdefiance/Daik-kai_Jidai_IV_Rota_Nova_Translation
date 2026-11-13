"""Seal B174 references with explicit32-actual/one-offline representative scope."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B174_research_v4481 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_reference_approval_v4491')
INPUT=Path('translations/lil_B174_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B174_editorial_manuscript_v6.json')
MAP=Path('translations/lil_B174_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B174_reference_census_v4484/all45_commands_four_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B174_relocated_controls_v4486/all33_dispatches_predicate_pair_four_relative_sites_two_A000s_and8_leaves.json')
STORED=Path('work/analysis/lil_B174_stored_v4478/all33_final_stored_targets132_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B174_ends_v4485/two_declared_end_decodes_and_four_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B174_actual_v4489c/actual_all33_unforced_predicate_paths_effects_C200_and_end.json')
FIXTURE=Path('work/analysis/lil_B174_display_fixture_v4487/complete_effect_preserving_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B174_actual_review_v4490b/all6_actual_sheets_optional_scope_join_notice_paired_return_and_final_state.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT));plan,census,control,stored,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL])
    parent=NdsImage.open(PARENT)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert census['all45_clean_current_target_commands_and_four_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==33 and len(control['relocated_predicate_pairs'])==1
    assert len(control['all8_source_current_target_nonrelative_nonspeech_leaves'])==8 and len(control['relocated_C200_pairs'])==1
    assert control['original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor']
    assert len(control['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'])==2
    assert len(stored['final_target_parity_cases'])==33 and stored['current_final_stored_macro_alignment_cases']==132
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(48,84)
    assert stored['all33_final_targets_complete_native_planes_equal_reviewed_planes']
    assert len(ends['cases'])==2 and ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert ends['B174_single_end_finishes_declared_logical_end']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==32
    assert not actual['failures'] and not actual['paired_region_differences']
    offline=['DK4_MES_B174_R0069'];assert actual['offline_only_display_IDs']==offline
    assert actual['frames_per_boot']==16001 and actual['actual_new_cold_boot_runs']==2
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[10776,10774]
    assert all(v['unforced_predicate_result']==0 and len(v['selected_B22_command_pairs'])==51 for v in actual['versions'])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all6_actual_sheets_viewed'])==6 and len(visual['paired_full_screen_views'])==6
    assert len(visual['all232_sampled_nontext_region_checks'])==232 and visual['all232_sampled_nontext_regions_equal']
    assert visual['whole_RGB_town10810_and_final16001_equal'] and all(visual['postscene16001_native_component_equality'].values())
    assert visual['postscene16001_whole1A04_actor_models_and_captain2_equal']
    assert visual['both_source_A0002068_and2076_actually_executed'] and visual['source_C2002084_actually_executed']
    assert visual['original_VM_last_result0_preserved_through_type3_commands_C200_and_end']
    assert visual['source_relative_sites882890_actual_886894938_offline_native_only'] and visual['PRNG_equality_or_future_world_equivalence_not_claimed']
    assert visual['join_notice10570_complete_shared_text_plane_equal'] and visual['join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed']
    assert fixture['source_B174_two_presentations_one_resource_two_A000s_predicate_four_spans_C200_and_tail_end_retained']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all54_stored_fixture_commands'])==54 for f in fixture['fixtures'])
    ids=[r['id'] for r in actual['actual_panels']];all_ids=[r['id'] for r in doc['records']]
    assert set(ids)|set(offline)==set(all_ids) and not set(ids)&set(offline)
    native=read(doc['native_font_proof']);assert native['all33_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==264
    ROOT.mkdir(parents=True)
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence,viewed_actual_sheets=visual['all6_actual_sheets_viewed'],actual_two_disclosed_content_cold_boots_pass=True,
        content_frames_each=16001,new_emulator_runs=2,no_additional_focus_run_without_concrete_unresolved_risk=True,
        actual_selected_B174_source_events=[],actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,represented_reviewed_display_IDs=all_ids,
        all32_unconditional_panels_unforced_predicate_both_effects_C200_single_end_and_normal_town_return_pass=True,
        optional_Emilio69_offline_native_planes_names_dispatch_and_both_operand_paths_approved=True,
        original45_structural_commands_and_single_declared_endword_preserved=True,no_B174_source_command_omitted=True,
        original_B22_four_A000_initialization_commands_retained=True,source_predicate0_then6240_A0002068_A0002076_C2002084_and_end_executed=True,
        source_relative_sites882890_actual_886894938_offline_native_only=True,
        actual_source_0100_extent52_and_relocated_extent62_distinguished=True,
        actual_VM_descriptor_last_result0_preserved_through_type3_C200_and_end=True,
        single_end2086_actual=True,no_source_pause_invented_and_original_C200_retained=True,
        all232_sampled_nontext_regions_and_whole_RGB_town10810_and_final16001_equal=True,
        postscene16001_five_native_components_whole_actor_model_and_captain2_equal=True,
        complete_existing_join_notice_and_first_J_preserved=True,join_notice_A_indicator_blink_rectangle_only=[224,360,240,376],
        source_packed_predicate_and_A000_semantics_not_inferred=True,PRNG_and_future_world_equality_not_claimed=True,
        no_open_translation_specific_display_or_control_finding=True,no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=True,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==174
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,representative_scope_does_not_mean_every_branch_was_visited=True)
    assert len(block['command_map'])==45 and len(block['relative_skip_fixups'])==4 and len(block['target_native_skip_cases'])==20
    assert len(block['text_records'])==33 and not block['choice_commands'] and not block['actor_style_commands'] and not block['original2000_pause_and_resume_maps']
    assert block['original_declared_end_word_maps']==[dict(source_offset=2086,target_offset=2204,extent=4,source_four_zero_bytes_exact=True)]
    mapping=dict(format='dk4-lil-B174-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],
        all45_structural_commands_four_relative_sites_one_predicate_verified=True,all33_active_speech_targets_preserved=True,
        all8_leaves_two_presentations_one_resource_predicate_two_A000s_C200_and_single_end_exact=True,
        single_tail_endword_preserved=True,no_FE_consumers_and_FI0_FA0_FO0_preserved=True,
        no_source2100_4100_or_dynamic_objects=True,no_source2000_pause=True,
        all_four_relative_sites20_target_cases_and_both_optional_speech_paths_preserved=True,
        source_predicate874_optional_Emilio_then6240_two_A000s_C200_end_preserved=True,representative_shared_rules_approved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B174_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,path in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),
        ('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:
        doc[key],doc[key+'_sha256']=str(path),sha(path.read_bytes())
    for row in doc['records']:
        assert row['kind']=='progressive';observed=row['id'] in ids
        row['historical_pre_actual_display_scope']={k:row[k] for k in ['current_complete_native_display_pending','current_native_UI_body_explicit_unexecuted_boundary'] if k in row}
        row.update(status=doc['status'],current_text_hex=row['current_hex'],native_display_consumer='original_progressive_54020',
            actual_B22_display_fixture_observed=observed,offline_only_native_display_checked=not observed,
            current_complete_native_display_pending=False,current_native_UI_body_explicit_unexecuted_boundary=not observed,
            individual_actual_source_event_activation_not_claimed=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},
        all33_source_native_reference_and_representative_rules_approved=True,source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=offline,new_emulator_runs=2,
        registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All33 B174 reference approvals sealed:32 actual/one offline;45 commands,four relative sites,two effects,C200,single end and town return. Registered integration pending.')
