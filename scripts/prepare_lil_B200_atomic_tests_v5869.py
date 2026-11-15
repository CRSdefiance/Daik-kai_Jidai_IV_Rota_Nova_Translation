"""Prepare exact positive reconstruction and meaningful pre-mutation semantic negatives."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_atomic_tools_v5869')
CASES='''    mutations=[]
    for key in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256']:
        mutations.append(('wrong-'+key,str(config),lambda v,k=key:v.update({k:'0'*64})))
    mutations += [
        ('lost-map-requirement',str(config),lambda v:v['required_map_flags'].pop()),
        ('lost-context-requirement',str(config),lambda v:v['required_term_flags'].pop()),
        ('missing-speech',str(DOC),lambda v:v['records'].pop()),
        ('wrong-policy',str(DOC),lambda v:v.update(translation_policy='natural-dialogue-v1')),
        ('wrong-locale',str(DOC),lambda v:v.update(target_locale='en-GB')),
        ('unchecked-format',str(DOC),lambda v:v.update(formatting_review_pending=True)),
        ('lost-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('invented-prose',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}An uncle rescued her.')),
        ('wrong-selector',str(DOC),lambda v:v['records'][0].update(source_selector=19)),
        ('wrong-preamble',str(DOC),lambda v:v['records'][0].update(source_complete_preamble_hex='0040ffff0013')),
        ('wrong-source-index',str(DOC),lambda v:v['records'][0].update(source_record_index=4)),
        ('wrong-current-index',str(DOC),lambda v:v['records'][0].update(current_record_index=4)),
        ('wrong-source-reference',str(DOC),lambda v:v['records'][0]['source_reference'].update(offset=14)),
        ('wrong-current-reference',str(DOC),lambda v:v['records'][0]['current_reference'].update(offset=14)),
        ('invented-FI',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}{MACRO:FI}')),
        ('invented-FA',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}{MACRO:FA}')),
        ('transferred-weak-waiver',str(DOC),lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy')),
        ('invented-authored-break',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}Thud!{LB}')),
        ('invented-private-thought',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}(Thud!)')),
        ('invented-old-runtime-override',str(DOC),lambda v:v['records'][0].update(registered_runtime_catalog_entry={'table_index':305})),
        ('actual-panel-claimed-offline',str(DOC),lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
        ('missing-command-map',str(MAP),lambda v:v['blocks'][0]['command_map'].pop()),
        ('missing-independent-map',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('invented-ancestor',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'][0]['target_0100_ancestors'].append(8)),
        ('wrong-source-extent',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=932)),
        ('wrong-target-extent',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=826)),
        ('invented-pause',str(MAP),lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({'old_offset':56,'new_offset':56})),
        ('wrong-target-record-index',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=6)),
        ('wrong-source-end',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(source_offset=928)),
        ('wrong-target-end',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=826)),
        ('missing-native-plane',doc['native_font_proof'],lambda v:v['cases'].pop()),
        ('clipped-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost-native-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-consumer-negative',doc['native_font_proof'],lambda v:v['negative_controls'].pop()),
        ('wrong-FE-count',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=1)),
        ('lost-stored-alignment',doc['final_padding_proof'],lambda v:v.update(current_final_stored_macro_alignment_cases=72)),
        ('lost-stored-plane',doc['final_padding_proof'],lambda v:v.update(all19_final_targets_complete_native_planes_equal_reviewed_planes=False)),
        ('lost-picture-or47xx',doc['relocated_control_proof'],lambda v:v['picture_and_short47xx_pairs'].pop()),
        ('wrong-actor-dispatch',doc['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][0].update(resolved_actor_ID=19)),
        ('missing-leaf',doc['relocated_control_proof'],lambda v:v['all12_source_current_target_control_leaves'].pop()),
        ('lost-end-probe',doc['termination_decode_proof'],lambda v:v['cases'].pop()),
        ('lost-native-negative',str(NATIVE),lambda v:v['formatter_negatives'].pop()),
        ('lost-viewed-native',str(NATIVE),lambda v:v['reviewed_sheets'][0].update(viewed_in_full_current_turn=False)),
        ('lost-courtesy-protection',doc['source_bound_wrap_retention_proof'],lambda v:v['protected_pairs'].pop()),
        ('fit-driven-shortening',doc['source_bound_wrap_retention_proof'],lambda v:v.update(all19_prose_wordings_controls_metrics_guards_phase_and_four_row_limits_unchanged=False)),
        ('wrong-prose-name',doc['actor_terminology_reconciliation'],lambda v:v['approved_prose_names'].update({'19':'Doctor Carlo'})),
        ('swapped-FE-roles',doc['actor_terminology_reconciliation'],lambda v:v.update(source_FE_impact_index=72)),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:v['fresh2_actor_names']['rows'][0].update(original_voice_class=0)),
        ('unapplied-Stranger-claimed-live',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'172':'Stranger'})),
        ('wrong-progressive-name',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'19':'Rafael'})),
        ('missing-name-consumer',doc['source_nameplate_consumer_proof'],lambda v:v['native_four_consumer_cases']['rows'].pop()),
        ('duplicate-name-consumer',doc['source_nameplate_consumer_proof'],lambda v:v['native_four_consumer_cases']['rows'].__setitem__(1,deepcopy(v['native_four_consumer_cases']['rows'][0]))),
        ('promoted-unused-occupation',doc['actor_terminology_reconciliation'],lambda v:v['actor172_label_localization_draft'].update(secondary_field_retained_as_evidence_not_silently_promoted_to_player_label=False)),
        ('draft-target-claimed-applied',doc['actor_terminology_reconciliation'],lambda v:v['actor172_label_localization_draft'].update(target_not_encoded_or_applied=False)),
        ('lost-reference-seal',str(SEAL),lambda v:v.update(all19_source_native_reference_and_representative_rules_approved=False))]
    actual_path=read(doc['representative_proof'])['actual_proof']
    mutations += [
        ('missing-actual-panel',actual_path,lambda v:v['actual_panels'].pop()),
        ('wrong-actual-holds',actual_path,lambda v:v.update(complete_matching_holds=72)),
        ('invented-offline-scope',actual_path,lambda v:v.update(offline_only_source_indices=[5])),
        ('wrong-command-result',actual_path,lambda v:v['versions'][1]['command_pairs'][-1].update(native_result=[3,0])),
        ('wrong-actual-inputs',actual_path,lambda v:v['versions'][1].update(input_schedule_sha256='0'*64)),
        ('wrong-actual-source-ID',actual_path,lambda v:v['versions'][1]['selected_intervals'][0].update(source_record_index=65)),
        ('wrong-actual-command-ID',actual_path,lambda v:v['versions'][0]['command_pairs'][-1].update(source_offset=924)),
        ('wrong-actual-native-plane',actual_path,lambda v:v['actual_panels'][0].update(native_plane_sha256='0'*64)),
        ('incomplete-actual-hold',actual_path,lambda v:v['actual_panels'][0]['holds'][0].update(complete_ink_gray_masks_equal_native_plane=False)),
        ('hiding-timing-differences',actual_path,lambda v:v['actual_timing_differences'].clear()),
        ('fabricated-timing-difference',actual_path,lambda v:v['actual_timing_differences'][0]['source'].update(start=0)),
        ('wrong-prompt-difference',actual_path,lambda v:v['later_whole_RGB_differences'][0].update(difference_bbox=[0,0,256,384])),
        ('wrong-sky-difference',actual_path,lambda v:v['later_whole_RGB_differences'][-1].update(difference_bbox=[0,192,256,294])),
        ('hiding-sky-nontext-difference',actual_path,lambda v:v['all_sampled_frame_comparisons'][-1].update(nontext_region_difference_bbox=None)),
        ('claiming-RNG-equality',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_seeds_equal=True)),
        ('claiming-RNG-causality',doc['postscene_native_state_proof'],lambda v:v.update(complete_RNG_timing_cause_not_traced=False)),
        ('claiming-world-equivalence',doc['postscene_native_state_proof'],lambda v:v.update(no_full_RAM_future_random_sequence_or_broad_world_equivalence_claim=False)),
        ('wrong-final-component',doc['postscene_native_state_proof'],lambda v:v['native_final_component_values'][1]['state'].update(cash=0)),
        ('lost-final-component-match',doc['postscene_native_state_proof'],lambda v:v['native_final_component_equality'].update(persistent_objects=False)),
        ('wrong-speech-duration-data',doc['postscene_native_state_proof'],lambda v:v['actual_command_duration_changes'][0].update(duration_delta=0)),
        ('pixel-masking',doc['postscene_native_state_proof'],lambda v:v.update(no_pixels_masked_retimed_or_edited=False)),
        ('unviewed-actual',doc['representative_proof'],lambda v:v['four_actual_and_six_paired_sheets_viewed'][0].update(viewed_after_image_return=False)),
        ('missing-viewed-scene',doc['representative_proof'],lambda v:v['four_actual_and_six_paired_sheets_viewed'].pop()),
        ('unconfirmed-later-differences',doc['representative_proof'],lambda v:v.update(six_prompt_blink_samples_and_ten_following_sailing_cloud_samples_visually_reviewed=False)),
        ('missing-source-command-claim',doc['representative_proof'],lambda v:v.update(all31_source_commands_plus9_initializers_stored_and40_observed_without_omission=False)),
        ('claiming-cloud-causality',doc['representative_proof'],lambda v:v.update(native_cloud_object_and_complete_RNG_timing_cause_not_traced=False)),
        ('incorrect-broad-goal-completion',str(DOC),lambda v:v.update(full_goal_complete=True))]
    for gate in ['source','context','localization','naturalness','formatting']:
        mutations.append(('missing-review-'+gate,str(DOC),lambda v,k=gate:v['records'][0]['review'].update({k:False})))
    for flag in FLAGS:mutations.append(('lost-map-'+flag,str(MAP),lambda v,k=flag:v.update({k:False})))
    for flag in owned.TERM_FLAGS:mutations.append(('lost-source-context-'+flag,doc['actor_terminology_reconciliation'],lambda v,k=flag:v.update({k:False})))
'''
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/validate_lil_B199_atomic_v5813c.py').read_text(encoding='utf-8')
    a=source.index('    mutations=[]');b=source.index('    for label,path,edit in mutations:',a)
    tool=derive('scripts/validate_lil_B199_atomic_v5813c.py','scripts/validate_lil_B200_atomic_v5869.py',{
        source[a:b]:CASES,'B199':'B200','lil_B199_editorial_v3':'lil_B200_editorial_v1',
        'seal_lil_B199_references_v5809':'seal_lil_B200_references_v5865','atomic_v5813c':'atomic_v5869',
        'v5756_candidate':'v5816_candidate','reference_approval_v5809':'reference_approval_v5865',
        'native_approval_v5793/all31_source_prose_current_native_approval':'native_approval_v5849/all19_source_prose_current_native_approval',
        'verification_v5811':'verification_v5867','lil_B199_layout_v3':'lil_B200_layout_v2',
        "len(proof['changed_records'])==31":"len(proof['changed_records'])==19",'positive_records=31':'positive_records=19'} )
    ROOT.mkdir(parents=True);save(ROOT/'prepared_positive_and_semantic_negative_tests.json',dict(tool=tool,
        source_current_native_reference_actual_timing_sky_name_and_goal_scope_negatives=True,
        semantic_load_overrides_do_not_weaken_real_file_hash_guards=True,sole_mutation_must_not_be_reached_by_any_negative=True,
        no_new_ROM_registry_or_review_credit=True,full_goal_complete=False))
