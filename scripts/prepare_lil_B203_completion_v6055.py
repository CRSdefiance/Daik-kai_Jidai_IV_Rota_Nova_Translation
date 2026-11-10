"""Derive an exact-inverse once-only B203 completion producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
GATES='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all591_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V5998']
    assert start['all_current_requested_and_final_framebuffers_equal_V5998'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==76 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['complete_matching_observations'],actual['complete_matching_holds'])==(22,22,86) and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_source_indices']
    assert actual['all31_source_commands_and9_initializers_stored'] and actual['same_observed_source_path_original_results_no_predicates_and_end810']
    assert transitions['no_open_translation_specific_display_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==6 and transitions['generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350']
    assert transitions['source_English_exit_frames']==[8374,8373] and transitions['command_timing_differences']==23 and transitions['later_prompt_differences']==18 and transitions['all_later_differences_bounded_to_advance_prompt']
    state=read(transitions['measured_state_proof']);assert sha(Path(transitions['measured_state_proof']).read_bytes())==transitions['measured_state_proof_sha256']
    assert state['actual_command_duration_changes']==[dict(source_offset=208,word=0x4000,source_duration=241,English_duration=240,delta=-1)] and not state['within_scene_RNG_differences'] and all(state['native_final_component_equality'].values()) and state['whole_actor_and_captain_equal'] and state['final_PRNG_equal']
    tests=read('work/analysis/lil_B203_regressions_v6050/terminal.json');assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B203_reference_v6037_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==591 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release
'''
if __name__=='__main__':
    p=Path('scripts/complete_lil_B202_v6003b.py');source=p.read_text(encoding='utf-8');oldgate=source[source.index('def gates():'):source.index('\ndef restore(')]
    changes={
        oldgate:GATES.rstrip(),'B202':'B203','lil_B202_completion_text_v6003':'lil_B203_completion_text_v6055',
        'lil_B202_completion_v6003':'lil_B203_completion_v6055','verification_v6004':'verification_v6056',
        'translations/lil_B202_editorial_manuscript_v6.json':'translations/lil_B203_editorial_manuscript_v5.json',
        'lil_B202_contextual_final_review_v1':'lil_B203_contextual_final_review_v1',
        'lil_B202_release_v5999':'lil_B203_release_v6051','lil_B202_startup_v6001':'lil_B203_startup_v6053',
        'lil_B202_actual_v5992/nineteen_actual_panels_source_matched_controls_and_complete_native_holds.json':'lil_B203_actual_v6044/twenty_two_actual_panels_source_matched_controls_and_complete_native_holds.json',
        'lil_B202_actual_review_v5993/viewed19_panels_complete_return_and_honest_measured_scope.json':'lil_B203_actual_review_v6045/viewed22_panels_complete_return_and_honest_measured_scope.json',
        'verification_v5981':'verification_v6033','lil_B202_registration_v5997':'lil_B203_registration_v6049','lil_B202_retention_v6002':'lil_B203_retention_v6054',
        'Lil-B202-unsolicited-book-handoff-pursuit-glassmaking-and-self-interest19':'Lil-B203-cordyceps-medicinal-book-offer-companion-interest-and1000-to100-negotiation22',
        'Lil_B202_completion_v6003':'Lil_B203_completion_v6055','unfinished_editorial_scope_v6003':'unfinished_editorial_scope_v6055','Lil_B202_v6003':'Lil_B203_v6055',
        '[-19:]':'[-22:]',"{'revise':6,'retain-wording':13}":"{'revise':9,'retain-wording':13}",
        '.blocks[202]':'.blocks[203]','dict(block=202,':'dict(block=203,',
        "'native_plane_verified_not_actual_English_gameplay']":"'native_plane_verified_not_actual_English_gameplay','current_native_extent']",
        "if speech:newref['header_offset']=at-5":"if speech:\n                newref['header_offset']=at-5\n                command=next(c for c in mapping['blocks'][0]['mapped_native_commands'] if c['new_offset']==at-5);assert command['word']==0x4000 and command['new_native_extent']>=len(value)+6\n                row['integrated_native_extent']=row['current_native_extent']=command['new_native_extent']",
        'len(oldkeys)==6308 and len(keys)==19':'len(oldkeys)==6327 and len(keys)==22',
        "fresh['fresh_pass_records_integrated']==6308":"fresh['fresh_pass_records_integrated']==6327",
        'scripts/lil_B202_completion_text_v6003.py':'scripts/lil_B203_completion_text_v6055.py','lil_B202_regressions_v5998':'lil_B203_regressions_v6050',
        'revised=6,retained=13':'revised=9,retained=13',
        'source_prose_and_completion_credit_added_once=19':'source_prose_and_completion_credit_added_once=22','all19_exact':'all22_exact',
        'actual_unique_speeches=19,actual_speech_observations=19':'actual_unique_speeches=22,actual_speech_observations=22',
        'actual_matching_holds=74':'actual_matching_holds=86','natural_event202_not_selected':'natural_event203_not_selected',
        'blocks=[202]':'blocks=[203]','revised_count=6,retained_count=13,fresh_revisions=6':'revised_count=9,retained_count=13,fresh_revisions=9',
        'records_editorially_completed=6327,records_with_source_and_prose_pass=6330,records_with_source_prose_drafts=6330,records_revised_and_integrated=3959,retained_wordings_editorially_completed=2368':'records_editorially_completed=6349,records_with_source_and_prose_pass=6352,records_with_source_prose_drafts=6352,records_revised_and_integrated=3968,retained_wordings_editorially_completed=2381',
        "==4423;new[key]['/data/SC2.DK4']=4442":"==4442;new[key]['/data/SC2.DK4']=4464",
        '6327 contextual rereads integrated;source/prose6330. B202 counted once.':'6349 contextual rereads integrated;source/prose6352. B203 counted once.',
        'fresh_pass_records_explicitly_reread=6327,fresh_pass_records_integrated=6327':'fresh_pass_records_explicitly_reread=6349,fresh_pass_records_integrated=6349',
        'records=19,final_review=str(FINAL),new_revisions=6,justified_retentions=13,new_completed_records=19':'records=22,final_review=str(FINAL),new_revisions=9,justified_retentions=13,new_completed_records=22',
        'actual_selected_source202_events=[],actual_B22_content_speeches=19,actual_speech_observations=19':'actual_selected_source203_events=[],actual_B22_content_speeches=22,actual_speech_observations=22',
        'reviewed_route_records=4728,completed_route_records=4728':'reviewed_route_records=4750,completed_route_records=4750',
        'completion_credit_added=19':'completion_credit_added=22','actual_source_event202_selected':'actual_source_event203_selected',
        'all19-source-native':'all22-source-native','all26_commands19_preambles7_leaves':'all31_commands22_preambles9_leaves',
        "old['unfinished_editorial_scope_v5980']":"old['unfinished_editorial_scope_v6032']",
        'historical_Lil_B202_native_review_before_v6003':'historical_Lil_B203_native_review_before_v6055','Lil_B202_native_review_v5980':'Lil_B203_native_review_v6032','Lil_B202_completed_v6003':'Lil_B203_completed_v6055',
        'completed_objects=19':'completed_objects=22','actual_speeches=19,actual_speech_observations=19':'actual_speeches=22,actual_speech_observations=22','complete_native_holds=74':'complete_native_holds=86',
        "inventory['next_Lil_B203_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=203,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B202_actor_voice_menu_macro_effect_or_end_assumptions_inherited=True)":"inventory['next_Lil_B204_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=204,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B203_actor_voice_menu_macro_effect_or_end_assumptions_inherited=True)",
        'Lil_B202_previously_uncredited_objects_completed=19,next_Lil_B203_clean_review_pending=True':'Lil_B203_previously_uncredited_objects_completed=22,next_Lil_B204_clean_review_pending=True',
        'new_source_prose_reviews=19,new_completed_records=19':'new_source_prose_reviews=22,new_completed_records=22',
        '## V6003: B202 complete exchange integrated once in cumulative V5998':'## V6055: B203 complete exchange integrated once in cumulative V6050',
        '# Current editorial handoff - V6003':'# Current editorial handoff - V6055',
        'new_completed_records=19,evidence=evidence':'new_completed_records=22,evidence=evidence','Six targets staged;19 reviews':'Six targets staged;22 reviews',
        '(6327,6330,3959,2368)':'(6349,6352,3968,2381)','exactly19_new_disjoint':'exactly22_new_disjoint','values and19 disjoint':'values and22 disjoint',
        "len(read(FINAL)['records'])==19":"len(read(FINAL)['records'])==22",'len(allkeys)==6327':'len(allkeys)==6349',
        'completed=6327,source_prose=6330,revised=3959,retained=2368,SC2=4442,SC3=96,reviewed_routes=4728,completed_routes=4728':'completed=6349,source_prose=6352,revised=3968,retained=2381,SC2=4464,SC3=96,reviewed_routes=4750,completed_routes=4750',
        'all590_manifest_batches114_accepted18_checks_verified':'all591_manifest_batches114_accepted18_checks_verified',
        'actual_unique_B202_speeches=19,actual_speech_observations=19':'actual_unique_B203_speeches=22,actual_speech_observations=22',
        'startup31_frames_and_five_actor_controls_match_V5947':'startup31_frames_and_five_actor_controls_match_V5998',
        'source202_natural_activation':'source203_natural_activation',
        'next_Lil_B203_clean_review_pending=True,retrospective207_name_queue':'next_Lil_B204_clean_review_pending=True,retrospective207_name_queue',
        'V5998 verified:6327 completed/6330 source-prose. B203':'V6050 verified:6349 completed/6352 source-prose. B204',
    }
    proof=derive(str(p),'scripts/complete_lil_B203_v6055.py',changes)
    root=Path('work/analysis/lil_B203_completion_preparation_v6055');root.mkdir(parents=True);save(root/'derivation.json',proof)
    print('B203 completion producer prepared;shared coverage unchanged.')
