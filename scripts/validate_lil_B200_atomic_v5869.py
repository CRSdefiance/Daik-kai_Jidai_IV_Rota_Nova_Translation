"""Reconstruct approved B200 and reject semantic errors before the sole ROM-image mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B200_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B200_references_v5865 import FLAGS,OUTPUT as DOC,MAP
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_atomic_v5869')
PARENT=Path('out/all_routes_combined_v5816_candidate.nds')
SEAL=Path('work/analysis/lil_B200_reference_approval_v5865/reference_approval.json')
NATIVE=Path('work/analysis/lil_B200_native_approval_v5849/all19_source_prose_current_native_approval.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    verified=read('work/analysis/editorial_handoff_verification_v5867/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(PARENT.read_bytes())==verified['candidate_sha256']
    doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    deps={str(DOC),str(MAP),str(SEAL),str(NATIVE),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B200_layout_v2.py','dk4tool/dialogue/lil_B200_profile.py','dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md'}
    deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file())
    deps.update(mapping[k] for k in ['source_plan','source_census']);deps.update(mapping['evidence'])
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py',
        'translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',
        *[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        value=read(p)
        if not isinstance(value,dict):continue
        for key in ['evidence','dependencies']:
            for item in value.get(key,{}) if isinstance(value.get(key),dict) else []:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    deps={p for p in deps if Path(p).resolve() not in excluded}
    conf=dict(format='dk4-lil-B200-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),reference_approval=str(SEAL),native_approval=str(NATIVE),
        required_map_flags=FLAGS,required_term_flags=owned.TERM_FLAGS,
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,config)
    assert test.read_file(owned.PATH)==Path(read(mapping['source_plan'])['target_SC2']).read_bytes() and len(proof['changed_records'])==19
    assert all(test.read_file(p)==v for _,p,v in parent.iter_files() if p!=owned.PATH) and all(test.read_file(p)==v for p,v in parent.iter_components())
    save(ROOT/'positive_reconstruction.json',proof)
    original_load=owned.load;negatives=[]
    def reject(label,path,edit):
        image=NdsImage.open(PARENT);value=deepcopy(read(path));before=deepcopy(value);edit(value);assert value!=before,label
        initial=[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']];calls=[];replace=image.replace_file
        image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
        owned.load=lambda p:deepcopy(value) if Path(p)==Path(path) else original_load(p)
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative accepted:'+label)
        finally:owned.load=original_load
        assert not calls and initial==[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']],label
        negatives.append(dict(label=label,rejected=True,reason=reason,sole_mutation_not_reached=True))
        if len(negatives)%10==0:print('Semantic negatives passed:'+str(len(negatives)),flush=True)
    mutations=[]
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
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,
        semantic_load_overrides_leave_real_hashes_intact_to_exercise_guards=True,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'atomic_validation_receipt.json',dict(positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        config=str(config),config_sha256=sha(config.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=19,
        dependencies=len(conf['dependencies']),new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(positive_records=19,semantic_negatives=len(negatives),dependencies=len(conf['dependencies']),all_before_mutation=True))
