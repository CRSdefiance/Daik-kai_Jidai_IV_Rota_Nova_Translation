"""Seal B175 references with32 actual panels and explicit second-end/visual-difference scope."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B175_research_v4525 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_reference_approval_v4536')
INPUT=Path('translations/lil_B175_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B175_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B175_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B175_reference_census_v4528/all39_commands_no_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B175_relocated_controls_v4530/all32_progressive_FE_dispatches_C200_pair_and7_leaves.json')
STORED=Path('work/analysis/lil_B175_stored_v4522/all32_final_stored_targets128_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B175_ends_v4529/four_declared_end_decodes_no_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B175_actual_v4534/actual_all32_progressive_FE_controls_C200_and_first_end.json')
FIXTURE=Path('work/analysis/lil_B175_display_fixture_v4531/complete_B175_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B175_actual_review_v4535/all6_actual_sheets_32_planes_scoped_transitions_return_and_final_state.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,MAP])
    doc=deepcopy(read(INPUT));plan,census,control,stored,ends,actual,fixture,visual=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL])
    parent=NdsImage.open(PARENT)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert census['all39_clean_current_target_commands_and_no_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==32 and sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==9
    assert len(control['all7_source_current_target_nonrelative_nonspeech_leaves'])==7 and len(control['relocated_C200_pairs'])==1
    assert control['all23_progressive_actors9_null_actor_FE_and_FI4_FA1_macro_expansions_exact']
    assert len(stored['final_target_parity_cases'])==32 and stored['current_final_stored_macro_alignment_cases']==128
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(68,60)
    assert stored['all32_final_targets_complete_native_planes_equal_reviewed_planes']
    assert len(ends['cases'])==4 and ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert ends['B175_second_end_finishes_declared_logical_end']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==32
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert actual['frames_per_boot']==16001 and actual['actual_new_cold_boot_runs']==2
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[10534,10535]
    assert all(len(v['selected_B22_command_pairs'])==47 and v['first_source_end1702_actually_reached'] and
               v['second_source_end1706_stored_but_unvisited_offline_decoder_only'] for v in actual['versions'])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all6_actual_sheets_viewed'])==6 and len(visual['paired_full_screen_views'])==8
    assert len(visual['all232_sampled_nontext_region_checks'])==232 and visual['nontext_equal_samples']==218
    assert len(visual['nontext_difference_samples'])==14 and visual['two_original_presentation_transition_differences_at_equal_duration_one_frame_offset']
    assert visual['twelve_following_sailing_foreground_cloud_differences_bounded_and_unmasked']
    assert visual['whole_RGB_town10570_through10870_equal'] and visual['final16001_whole_RGB_equality_not_claimed']
    assert all(visual['postscene16001_native_component_equality'].values()) and visual['postscene16001_whole1A04_actor_models_and_captain2_equal']
    assert visual['all_content_jobs_terminal'] and visual['PRNG_equality_causal_trace_and_future_world_equivalence_not_claimed']
    assert fixture['source_all39_commands_preserved_without_omission_or_flattening']
    assert all(not f['explicitly_excluded_original_commands'] and len(f['all48_stored_fixture_commands'])==48 for f in fixture['fixtures'])
    ids=[r['id'] for r in actual['actual_panels']];all_ids=[r['id'] for r in doc['records']]
    assert ids==all_ids and len(set(ids))==32
    native=read(doc['native_font_proof']);assert native['all32_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==256
    ROOT.mkdir(parents=True);paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence,viewed_actual_sheets=visual['all6_actual_sheets_viewed'],actual_two_disclosed_content_cold_boots_pass=True,
        content_frames_each=16001,new_emulator_runs=2,no_additional_focus_run_without_concrete_unresolved_risk=True,
        actual_selected_B175_source_events=[],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],represented_reviewed_display_IDs=all_ids,
        all32_panels23_progressive9_FE_three_presentations_resource_C200_first_end_and_normal_town_return_pass=True,
        original39_commands_and_both_declared_endwords_preserved=True,no_B175_source_command_omitted=True,
        original_B22_four_A000_initialization_commands_retained=True,first_end1702_actual_second_end1706_offline_native_only=True,
        two_transition_one_frame_differences_and_twelve_later_cloud_differences_retained=True,
        complete_native_text_planes_and_paired_held_nontext_regions_equal=True,
        whole_RGB_town_return_equal=True,final_whole_RGB_equality_not_claimed=True,
        five_native_state_components_and_whole1A04_actor_captain2_equal=True,
        no_PRNG_causal_trace_future_world_full_RAM_or_hardware_equality_claim=True,
        no_open_translation_specific_display_or_control_finding=True,no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=True,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0];assert block['block']==checked['block']==175
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_scope_does_not_mean_natural_event_eligibility=True)
    assert len(block['command_map'])==39 and len(block['text_records'])==32
    assert not block['relative_skip_fixups'] and not block['target_native_skip_cases'] and not block['choice_commands'] and not block['actor_style_commands']
    assert [(e['source_offset'],e['target_offset']) for e in block['original_declared_end_word_maps']]==[(1702,1690),(1706,1694)]
    flags=['all39_structural_commands_verified','all32_active_speech_targets_preserved',
        'all7_leaves_three_presentations_resource_C200_and_both_ends_exact','both_declared_endwords_preserved',
        'progressive23_FE9_and_FI4_FA1_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause',
        'no_source_relative_sites_predicates_or_A000','first_end1702_actual_second_end1706_offline','representative_shared_rules_approved']
    mapping=dict(format='dk4-lil-B175-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in flags},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B175_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,path in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('relocated_control_proof',CONTROL),
        ('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:doc[key],doc[key+'_sha256']=str(path),sha(path.read_bytes())
    for row in doc['records']:
        assert row['kind'] in ['progressive','system-FE']
        row['historical_pre_actual_display_scope']={k:row[k] for k in ['current_complete_native_display_pending','current_native_UI_body_explicit_unexecuted_boundary'] if k in row}
        row.update(status=doc['status'],current_text_hex=row['current_hex'],
            native_display_consumer='original_null_actor_FE_24310_then5473C' if row['kind']=='system-FE' else 'original_progressive_54020',
            actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,current_complete_native_display_pending=False,
            current_native_UI_body_explicit_unexecuted_boundary=False,individual_actual_source_event_activation_not_claimed=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},all32_source_native_reference_and_representative_rules_approved=True,
        source_prose_English_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],second_end1706_offline_only=True,
        scoped_visual_differences_retained=True,new_emulator_runs=2,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B175 references sealed:all32 actual panels,39 commands,C200,both ends with second offline;scoped transition/cloud differences retained. Registered integration pending.')
