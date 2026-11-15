"""Seal both companions with exact references and explicitly limited actual coverage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B197_research_v5676 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_reference_approval_v5687')
INPUT=Path('translations/lil_B197_editorial_manuscript_v3.json')
CHOICE_INPUT=Path('translations/lil_B197_choice_manuscript_v2.json')
OUTPUT=Path('translations/lil_B197_editorial_manuscript_v4.json')
CHOICE_OUTPUT=Path('translations/lil_B197_choice_manuscript_v3.json')
MAP=Path('translations/lil_B197_editorial_relocation_map_v1.json')
CENSUS=Path('work/analysis/lil_B197_reference_census_v5679/all39_commands6_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B197_relocated_controls_v5681e/all21_dispatches_three_picture_pairs_one_menu_and11_exact_leaves.json')
STORED=Path('work/analysis/lil_B197_stored_v5672/all21_final_stored_targets84_macro_cases_and_complete_planes.json')
STORED_MENUS=Path('work/analysis/lil_B197_stored_choices_v5673/one_final_typed_object_three_exact_references_and_both_even_alignments.json')
ENDS=Path('work/analysis/lil_B197_ends_v5680/two_declared_end_decodes_and_all6_in_block_relative_destinations.json')
ACTUAL=Path('work/analysis/lil_B197_actual_v5684b/three_paths_and_focused_refusal_highlight.json')
FIXTURE=Path('work/analysis/lil_B197_English_fixture_v5682/complete_B197_reviewed_English_B22_fixture.json')
VISUAL=Path('work/analysis/lil_B197_actual_review_v5686/viewed21_panels_three_options_returns_and_measured_scope.json')
CORRECTION=Path('work/analysis/lil_B197_control_correction_v5681c/source_trace_address_correction_and_stopped_receipt_preserved.json')
FLAGS=['all39_structural_commands_and6_relative_sites_verified','all21_speech_targets_and3_typed_labels_preserved',
       'all11_opaque_leaves_three_picture_boundaries_and_one_end_exact','progressive20_null_actor_FE1_no_macros_preserved',
       'one2200_count3_order_pointers_selection_and_cancel_preserved','all_original_stored_source_bytes_restored_by_inverse_with_two_tailzeros',
       'all21_actual_speech_panels35_observations128_native_holds_scope_explicit','all_three_choices_and_common_end_actual_verified',
       'representative_shared_rules_approved']
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUTPUT,CHOICE_OUTPUT,MAP])
    doc,choice=[deepcopy(read(p)) for p in [INPUT,CHOICE_INPUT]]
    plan,census,control,stored,menus,ends,actual,fixture,visual,correction=map(read,[PLAN,CENSUS,CONTROL,STORED,STORED_MENUS,ENDS,ACTUAL,FIXTURE,VISUAL,CORRECTION])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==choice['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==ends['research_ROM_sha256']
    assert sha(INPUT.read_bytes())==plan['manuscript_sha256']==stored['manuscript_sha256']==control['manuscript_sha256']
    assert sha(CHOICE_INPUT.read_bytes())==plan['choices_sha256']==menus['manuscript_sha256']
    assert census['all39_clean_current_target_commands_and6_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(control['relocated_dispatch_cases'])==21 and len(control['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==11
    assert len(control['picture_and47xx_current_relocated_pairs'])==3 and control['original47xx_R3_is_exact_mapped_stream_instruction_pointer']
    assert correction['correct_source_return_hex']=='0x02029FEC' and correction['source_return_decimal']==33726444
    assert stored['current_final_stored_macro_alignment_cases']==84 and stored['all21_final_targets_complete_native_planes_equal_reviewed_planes']
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(28,56)
    assert menus['source_count3_option_order_and_original_selection_cancel_results_preserved'] and menus['fresh_count_calls']==2 and menus['fresh_label_pointer_calls']==6
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
    assert not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences']
    assert len(actual['actual_panels'])==21 and len(actual['actual_menu_cases'])==3 and actual['offline_only_display_IDs']==[]
    assert actual['actual_English_speech_observations']==35 and actual['complete_native_holds']==128
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and visual['no_open_translation_specific_display_menu_control_or_return_finding'] and not visual['visual_review_pending']
    assert visual['new_successful_English_runs']==4 and visual['new_successful_English_frames']==43604 and visual['total_successful_frames']==82607
    assert len(visual['paired_command_timing_differences'])==59 and len(visual['postscene_whole_RGB_differences'])==82
    assert visual['broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks']
    assert fixture['all39_original_commands_with_reviewed_prose_and9_identical_original_init_commands_stored']
    assert len(fixture['fixtures'])==1 and not fixture['fixtures'][0]['explicitly_excluded_original_commands'] and len(fixture['fixtures'][0]['all48_stored_fixture_commands'])==48
    views=visual['all_actual_consumer_menu_sheets_viewed']+visual['paired_full_screen_views']
    assert len(views)==9 and all(s['viewed'] and s['viewed_after_image_return'] and s['original_detail'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views)
    for p,h in visual['evidence'].items():assert sha(Path(p).read_bytes())==h
    ids=[r['id'] for r in actual['actual_panels']];assert set(ids)=={r['id'] for r in doc['records']}
    assert sorted(r['native_result_words'][1] for r in actual['actual_menu_cases'])==[0,1,2]
    paths=[INPUT,CHOICE_INPUT,PLAN,CENSUS,CONTROL,STORED,STORED_MENUS,ENDS,ACTUAL,FIXTURE,VISUAL,CORRECTION,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    sample=ROOT/'representative_display_control_and_transition_reconciliation.json'
    save(sample,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],actual_original_menu_indices=[0,1,2],original_menu_offset=230,
        all_three_label_meanings_and_visible_selection_return_associations_verified=True,all_original_commands_stored_without_omission=True,
        common_original_end874_observed_after_all_three_choices=True,
        source_purchase_acceptance_then_romantic_rebuff_delegated_gift_and_common_Ian_Charm_notice_preserved=True,
        all21_speeches_actual_in_this_scene_without_imposing_global_exhaustive_gameplay=True,
        source_matched_blank_portrait_name_at64_and89_not_an_English_specific_defect=True,
        source_original47xx_return0x02029FEC_and_exact_mapped_R3_instruction_pointer_verified=True,
        actual_book_card_and_three_notices_not_full_item_or_Charm_semantics=True,
        viewed_actual_sheets=visual['all_actual_consumer_menu_sheets_viewed'],viewed_paired_full_screen_sheets=visual['paired_full_screen_views'],
        retained59_timing82_later_RGB_and_explicit_RNG_state_differences=True,no_complete_postscene_equivalence_or_causal_claim=True,
        no_open_translation_specific_display_or_control_finding=True,representative_shared_rules_approved=True,
        no_natural_eligibility_earned_affordability_full_route_hardware_or_full_state_claim=True,
        new_English_successful_runs=4,new_English_successful_frames=43604,reused_Japanese_runs=3,total_successful_frames=82607,
        two_failed_partial_runs_preserved_not_counted_as_passes=True,registered_release_and_current_startup_pending=True,evidence=evidence,full_goal_complete=False))
    block=deepcopy(plan['blocks'][0]);checked=census['blocks'][0]
    assert block['block']==checked['block']==197 and len(block['command_map'])==39 and len(block['text_records'])==21
    assert (block['source_bytes'],block['source_logical_end'],block['research_bytes'],block['research_logical_end'])==(880,878,1004,1002)
    assert len(block['relative_skip_fixups'])==6 and len(block['target_native_skip_cases'])==30 and len(block['choice_commands'])==1
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    block['target_block_sha256']=block.pop('research_block_sha256')
    block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,
        individual_naturally_selected_source_scene_unobserved=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[])
    mapping=dict(format='dk4-lil-B197-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(NdsImage.open(PARENT).read_file('/__arm9__.bin')),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=[block],**{f:True for f in FLAGS},
        actual_sampled_display_IDs=ids,offline_only_display_IDs=[],representative_proof=str(sample),source_plan=str(PLAN),source_census=str(CENSUS),
        final_padding_proof=str(STORED),final_choice_proof=str(STORED_MENUS),relocated_control_proof=str(CONTROL),termination_decode_proof=str(ENDS),postscene_native_state_proof=str(VISUAL),
        evidence={**evidence,str(sample):sha(sample.read_bytes())},actual_selected_B197_source_events=[],full_goal_complete=False)
    save(MAP,mapping)
    for batch,old,other,out in [(doc,INPUT,CHOICE_OUTPUT,OUTPUT),(choice,CHOICE_INPUT,OUTPUT,CHOICE_OUTPUT)]:
        batch.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),prose_companions=[str(other)],reference_map_pending=False,
            registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for key,p in [('reference_map',MAP),('representative_proof',sample),('final_padding_proof',STORED),('final_choice_proof',STORED_MENUS),('relocated_control_proof',CONTROL),('termination_decode_proof',ENDS),('postscene_native_state_proof',VISUAL)]:batch[key],batch[key+'_sha256']=str(p),sha(p.read_bytes())
        for r in batch['records']:
            r['historical_pre_actual_display_scope']={k:r[k] for k in ['current_complete_native_display_pending','current_native_UI_body_explicit_unexecuted_boundary','actual_choice_selection_still_pending'] if k in r}
            r.update(status=batch['status'],current_text_hex=r['current_hex'],actual_B22_display_fixture_observed=True,offline_only_native_display_checked=False,
                current_complete_native_display_pending=False,individual_actual_source_event_activation_not_claimed=True)
            if r['kind']!='typed-choice-label':
                r['native_display_consumer']='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020';r['current_native_UI_body_explicit_unexecuted_boundary']=False
            else:r.update(native_display_consumer='original2200_three_option_modal51FC0',actual_label_visible=True,actual_choice_all_outcomes_observed=True,
                actual_choice_selection_still_pending=False,choice_consumer_selection_geometry_native_display_pending=False)
        assert [r['english'] for r in batch['records']]==[r['english'] for r in read(old)['records']]
        validate_natural_dialogue_batch(batch);save(out,batch)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in [OUTPUT,CHOICE_OUTPUT]},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        evidence={**evidence,str(MAP):sha(MAP.read_bytes()),str(sample):sha(sample.read_bytes())},all24_source_native_reference_and_representative_rules_approved=True,
        source_prose_English_unchanged=True,actual_sampled_display_IDs=ids,offline_only_display_IDs=[],actual_original_menu_indices=[0,1,2],
        new_English_successful_runs=4,total_successful_frames=82607,new_editorial_credit=0,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B197 sealed24 objects:all21 speeches actual/35 observations/128 native holds/three visible options/common end.16 revisions/eight retentions unchanged. Differences retained;registered compiler/release/startup next.')
