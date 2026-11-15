"""Seal all37 B171 reviews with exact relocation and scoped four-boot evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B171_research_v4334 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B171_reference_approval_v4346')
INPUT=Path('translations/lil_B171_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B171_editorial_manuscript_v5.json')
MAP=Path('translations/lil_B171_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B171_reference_census_v4337/all45_commands_zero_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B171_relocated_controls_v4339/all37_progressive_dispatches_C200_and8_leaves.json')
STORED=Path('work/analysis/lil_B171_stored_v4333/all37_final_stored_targets148_macro_cases_and_complete_planes.json')
ENDS=Path('work/analysis/lil_B171_ends_v4338/four_declared_end_decodes_and_zero_relative_sites.json')
ACTUAL=Path('work/analysis/lil_B171_actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end.json')
FIXTURE=Path('work/analysis/lil_B171_display_fixture_v4340/complete_effect_preserving_B22_fixtures.json')
VISUAL=Path('work/analysis/lil_B171_transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review.json')
REPEAT=Path('work/analysis/lil_B171_repeat_verification_v4344/post_B171_actor_captain_and_same_ROM_repeat_comparison.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,OUTPUT])
    doc=deepcopy(read(INPUT))
    plan,census,control,stored,ends,actual,fixture,visual,repeat=map(read,[PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,REPEAT])
    parent,image=NdsImage.open(PARENT),NdsImage.open(ROM)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert census['all45_clean_current_target_commands_and_zero_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==37 and not control['relocated_predicate_pairs']
    assert len(control['all8_source_current_target_nonrelative_nonspeech_leaves'])==8
    assert len(control['relocated_C200_pairs'])==1 and control['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
    assert control['both_consecutive_endwords_and_no_source_pause_or_A000_preserved']
    assert stored['current_final_stored_macro_alignment_cases']==148 and len(stored['final_target_parity_cases'])==37
    assert stored['all37_final_targets_complete_native_planes_equal_reviewed_planes']
    assert ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==4
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==37
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_or_control_finding']
    assert len(visual['all7_actual_sheets_viewed'])==7 and len(visual['English_full_screen_views'])==6
    assert len(visual['Japanese_full_screen_views'])==4 and len(visual['paired_source_English_whole_RGB_town_returns'])==1
    assert visual['first_end2112_actual_second_end2116_stored_and_native_decoder_only']
    assert fixture['source_B171_4500_4621_61FF_6325_C200_and_both_ends_retained_without_invented_A000_or_pause']
    assert all(not row['explicitly_excluded_original_commands'] for row in fixture['fixtures'])
    assert repeat['paired_town11770_whole1A04_actor_models_and_captain2_equal']
    assert repeat['cross_language_command_order_results_and_first_end_word_equal']
    assert repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
    assert repeat['cross_language_exit_frames']==[11737,11735]
    assert len(repeat['cross_language_command_timing_differences'])==22
    assert all(all(row['component_equality'].values()) for row in repeat['paired_native_persistent_state_and_PRNG_samples'] if row['frame']<=16450)
    native=read(doc['native_font_proof'])
    assert native['all37_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==296
    ids=[row['id'] for row in actual['actual_panels']]
    assert set(ids)=={row['id'] for row in doc['records']}
    ROOT.mkdir(parents=True)
    paths=[INPUT,PLAN,CENSUS,CONTROL,STORED,ENDS,ACTUAL,FIXTURE,VISUAL,REPEAT,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        evidence=evidence,viewed_actual_sheets=visual['all7_actual_sheets_viewed'],actual_two_disclosed_content_cold_boots_pass=True,
        two_additional_focused_repeats_postscene_state_and_PRNG_checked=True,
        actual_selected_B171_source_events=[],actual_sampled_display_IDs=ids,offline_only_display_IDs=[],represented_reviewed_display_IDs=ids,
        actual37_progressive_panels_dream_morning_resource_C200_first_end_and_normal_town_return_pass=True,
        original45_commands_and_both_declared_endwords_preserved=True,no_B171_source_command_omitted=True,
        first_end2112_actual_second2116_native_decoder_only=True,
        original_B22_four_A000_initialization_commands_retained=True,no_source_A000_or_pause_invented=True,
        no_open_translation_specific_display_or_control_finding=True,later59_sailing_differences_preserved_with_explicit_inference_and_state_scope=True,
        no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=True,new_emulator_runs=4,
        registered_release_and_current_startup_pending=True,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==171
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],
        external_entry_and_actual_revised_paths_approval_pending=False,individual_naturally_selected_source_scene_unobserved=True)
    assert len(block['command_map'])==45 and not block['relative_skip_fixups'] and not block['target_native_skip_cases']
    assert len(block['text_records'])==37 and not block['choice_commands'] and not block['actor_style_commands']
    assert not block['original2000_pause_and_resume_maps']
    assert [e['source_offset'] for e in block['original_declared_end_word_maps']]==[2112,2116]
    assert [e['target_offset'] for e in block['original_declared_end_word_maps']]==[2302,2306]
    mapping=dict(format='dk4-lil-B171-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],
        all45_commands_zero_relative_sites_zero_predicates_verified=True,all37_active_speech_targets_preserved=True,
        all8_leaves_four_presentations_one_resource_C200_and_both_ends_exact=True,
        both_consecutive_declared_endwords_preserved=True,no_FE_consumers_and_FI1_FO0_preserved=True,
        no_source2100_4100_or_dynamic_objects=True,no_source_A000_or2000_pause=True,representative_shared_rules_approved=True,
        representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(STORED),
        relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),focused_repeat_proof=str(REPEAT),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B171_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),reference_map_pending=False,
        registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for key,path in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),
                     ('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('focused_repeat_proof',REPEAT)]:
        doc[key],doc[key+'_sha256']=str(path),sha(path.read_bytes())
    for row in doc['records']:
        assert row['kind']=='progressive'
        row.update(status=doc['status'],current_text_hex=row['current_hex'],native_display_consumer='original_progressive_54020',
            actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,individual_actual_source_event_activation_not_claimed=True)
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(INPUT)['records']]
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},reference_map=str(MAP),
        reference_map_sha256=sha(MAP.read_bytes()),evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},
        all37_source_native_reference_and_representative_rules_approved=True,source_prose_English_unchanged=True,
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],new_emulator_runs=4,
        registered_release_and_current_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All37 B171 approvals sealed:45 commands,8 leaves,148 stored cases,dream/morning/C200/first-end/town return. Four boots;later sailing differences scoped. Registered integration pending.')
