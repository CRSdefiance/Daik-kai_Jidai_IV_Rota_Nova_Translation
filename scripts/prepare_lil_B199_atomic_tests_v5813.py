"""Prepare semantic pre-mutation negatives for the exact B199 source and measured scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_atomic_test_tools_v5813')
MUTATIONS='''    mutations=[]
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
        ('invented-prose',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:16}Hello, sister.')),
        ('wrong-selector',str(DOC),lambda v:v['records'][0].update(source_selector=2)),
        ('wrong-preamble',str(DOC),lambda v:v['records'][0].update(source_complete_preamble_hex='0040ffff0002')),
        ('wrong-source-index',str(DOC),lambda v:v['records'][0].update(source_record_index=4)),
        ('wrong-current-index',str(DOC),lambda v:v['records'][0].update(current_record_index=4)),
        ('wrong-source-reference',str(DOC),lambda v:v['records'][0]['source_reference'].update(offset=14)),
        ('wrong-current-reference',str(DOC),lambda v:v['records'][0]['current_reference'].update(offset=14)),
        ('missing-FI',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==37).update(english='{SPEAKER:09}Lil! Stop throwing things! Ow!')),
        ('duplicated-FI',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==37).update(english='{SPEAKER:09}{MACRO:FI}! {MACRO:FI}! Stop throwing things! Ow!')),
        ('transferred-weak-waiver',str(DOC),lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy')),
        ('invented-authored-break',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:16}By the way,{LB}who is that man?')),
        ('private-thought-made-audible',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==70).update(english="{SPEAKER:09}Got away again. Samwell's quick on his feet.")),
        ('live-Camille-misreported-Kamil',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==58).update(effective_predecessor_paragraph='Kamil! Come on!')),
        ('lost-existing-Camille-catalog-entry',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==58).update(registered_runtime_catalog_entry=None)),
        ('actual-panel-claimed-offline',str(DOC),lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
        ('missing-command-map',str(MAP),lambda v:v['blocks'][0]['command_map'].pop()),
        ('missing-independent-map',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('invented-ancestor',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'][0]['target_0100_ancestors'].append(8)),
        ('wrong-source-extent',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=1168)),
        ('wrong-target-extent',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=1116)),
        ('lost-pause',str(MAP),lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].pop()),
        ('wrong-pause-resume',str(MAP),lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'][0].update(target_resume=70)),
        ('wrong-target-record-index',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=6)),
        ('wrong-source-end',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(source_offset=1164)),
        ('wrong-target-end',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=1112)),
        ('missing-native-plane',doc['native_font_proof'],lambda v:v['cases'].pop()),
        ('clipped-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost-native-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-consumer-negative',doc['native_font_proof'],lambda v:v['negative_controls'].pop()),
        ('lost-stored-alignment',doc['final_padding_proof'],lambda v:v.update(current_final_stored_macro_alignment_cases=120)),
        ('lost-stored-plane',doc['final_padding_proof'],lambda v:v.update(all31_final_targets_complete_native_planes_equal_reviewed_planes=False)),
        ('lost-picture-or47xx',doc['relocated_control_proof'],lambda v:v['picture_and_short47xx_pairs'].pop()),
        ('lost-relocated-pause',doc['relocated_control_proof'],lambda v:v['one_source_pause_and_resume_map'].update(target_resume=70)),
        ('wrong-actor-dispatch',doc['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][0].update(resolved_actor_ID=2)),
        ('missing-leaf',doc['relocated_control_proof'],lambda v:v['all16_source_current_target_control_leaves'].pop()),
        ('lost-end-probe',doc['termination_decode_proof'],lambda v:v['cases'].pop()),
        ('lost-native-negative',str(NATIVE),lambda v:v['formatter_negatives'].pop()),
        ('lost-viewed-native',str(NATIVE),lambda v:v['reviewed_sheets'][0].update(viewed_in_full_current_turn=False)),
        ('lost-idiom-protection',doc['source_bound_wrap_retention_proof'],lambda v:v.update(source70_full_idiom_protected_without_new_word_or_manual_break=False)),
        ('fit-driven-shortening',doc['source_bound_wrap_retention_proof'],lambda v:v.update(R95_no_word_shortened_and_no_width_guard_phase_or_four_row_limit_changed=False)),
        ('wrong-prose-name',doc['actor_terminology_reconciliation'],lambda v:v['approved_prose_names'].update({'9':'Kamil'})),
        ('private-indices-lost',doc['actor_terminology_reconciliation'],lambda v:v.update(private_parentheses_source_indices=[])),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:v['fresh3_actor_names']['rows'][0].update(original_voice_class=0)),
        ('silently-repaired-Samwell-field',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'22':'Samwell da Khan'})),
        ('wrong-progressive-name',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'9':'Rafael'})),
        ('lost-reference-seal',str(SEAL),lambda v:v.update(all31_source_native_reference_and_representative_rules_approved=False))]
    actual_path=read(doc['representative_proof'])['actual_proof']
    mutations += [
        ('missing-actual-panel',actual_path,lambda v:v['actual_panels'].pop()),
        ('wrong-actual-holds',actual_path,lambda v:v.update(complete_matching_holds=119)),
        ('invented-offline-scope',actual_path,lambda v:v.update(offline_only_source_indices=[5])),
        ('wrong-command-result',actual_path,lambda v:v['versions'][1]['command_pairs'][-1].update(native_result=[3,0])),
        ('wrong-actual-inputs',actual_path,lambda v:v['versions'][1].update(input_schedule_sha256='0'*64)),
        ('wrong-actual-ID',actual_path,lambda v:v['versions'][1]['selected_intervals'][0].update(source_record_index=65)),
        ('hiding-timing-differences',actual_path,lambda v:v['actual_timing_differences'].clear()),
        ('wrong-prompt-difference',actual_path,lambda v:v['later_whole_RGB_differences'][0].update(difference_bbox=[0,0,256,384])),
        ('claiming-RNG-equality',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_seeds_equal=True)),
        ('hiding-RNG-difference',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_difference_preserved_not_removed_or_reseeded=False)),
        ('claiming-RNG-causality',doc['postscene_native_state_proof'],lambda v:v.update(complete_RNG_timing_cause_not_traced=False)),
        ('claiming-world-equivalence',doc['postscene_native_state_proof'],lambda v:v.update(no_full_RAM_future_random_sequence_or_broad_world_equivalence_claim=False)),
        ('wrong-final-component',doc['postscene_native_state_proof'],lambda v:v['native_final_component_values'][1]['state'].update(cash=0)),
        ('lost-final-component-match',doc['postscene_native_state_proof'],lambda v:v['native_final_component_equality'].update(persistent_objects=False)),
        ('wrong-speech-duration-data',doc['postscene_native_state_proof'],lambda v:v['six_actual_speech_duration_changes'][0].update(duration_delta=0)),
        ('pixel-masking',doc['postscene_native_state_proof'],lambda v:v.update(no_pixels_masked_retimed_or_edited=False)),
        ('unviewed-actual',doc['representative_proof'],lambda v:v['six_actual_and_six_paired_sheets_viewed'][0].update(viewed_after_image_return=False)),
        ('missing-viewed-scene',doc['representative_proof'],lambda v:v['six_actual_and_six_paired_sheets_viewed'].pop()),
        ('unconfirmed-prompt-identity',doc['representative_proof'],lambda v:v.update(six_later_differences_visually_confirmed_advance_prompt_blink=False)),
        ('missing-source-command-claim',doc['representative_proof'],lambda v:v.update(all47_source_commands_plus9_initializers_stored_and56_observed_without_omission=False))]
    for gate in ['source','context','localization','naturalness','formatting']:
        mutations.append(('missing-review-'+gate,str(DOC),lambda v,k=gate:v['records'][0]['review'].update({k:False})))
'''
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/validate_lil_B198_atomic_v5754.py').read_text(encoding='utf-8')
    prefix=source[:source.index('    mutations=[]')]
    suffix=source[source.index('    for flag in FLAGS:'):]
    planned=checked_text(prefix+MUTATIONS+suffix,{
        'B198':'B199','lil_B198_editorial_v2':'lil_B199_editorial_v1','atomic_v5754':'atomic_v5813',
        'combined_v5692':'combined_v5756','seal_lil_B198_references_v5746':'seal_lil_B199_references_v5809',
        'reference_approval_v5746':'reference_approval_v5809','native_approval_v5724/all17':'native_approval_v5793/all31',
        'verification_v5751':'verification_v5811','lil_B198_layout_v2':'lil_B199_layout_v3',
        "len(proof['changed_records'])==17":"len(proof['changed_records'])==31",'positive_records=17':'positive_records=31'})
    out=Path('scripts/validate_lil_B199_atomic_v5813.py');assert not out.exists();out.write_text(planned,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'prepared_semantic_negatives.json',dict(script=str(out),all_tests_target_B199_actual_scope=True,
        no_new_ROM_registry_or_review_credit=True,full_goal_complete=False))
