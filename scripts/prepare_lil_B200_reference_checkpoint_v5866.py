"""Derive a deep-inverse checkpoint for sealed B200 references and measured gameplay limits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_reference_checkpoint_tools_v5866')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/checkpoint_lil_B200_and_names_v5841.py').read_text(encoding='utf-8')
    a=source.index('    assert doc[\'revised\']==13');b=source.index('    known=',a)
    checks='''    assert doc['revised']==13 and doc['retained']==6 and doc['source_prose_or_completion_credit_added']==0
    assert all(all(r['review'].values()) for r in rows)
    approval=read('work/analysis/lil_B200_reference_approval_v5865/reference_approval.json')
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['native_approved_revisions']==13 and approval['native_approved_retentions']==6
    assert approval['all19_source_native_reference_and_representative_rules_approved']
    assert approval['all_prior_evidence_and_measured_timing_prompt_cloud_PRNG_differences_preserved']
    sample=read(doc['representative_proof'])
    assert sample['all19_actual_native_panels73_complete_holds_and_changed_scene_source_regions_match']
    assert sample['sampled_nontext_frames']==182 and sample['nontext_equal_samples']==172
    assert sample['command_start_or_return_difference_count']==19 and sample['speech_duration_difference_count']==8
    assert sample['later_sampled_whole_RGB_difference_count']==16 and sample['PRNG_seeds_differ']
    assert all(sample['final_native_component_equality'].values()) and sample['Stranger_label_target_not_applied_and_name_review_still_open']
'''
    a2=source.index("    scope['next_Lil_B200_clean_review_pending'].update(");b2=source.index("    scope['B200_anonymous_role_label_v5841']",a2)
    scope='''    scope['historical_Lil_B200_clean_context_before_v5866']=scope.pop('next_Lil_B200_clean_review_pending')
    scope['next_Lil_B200_reference_approved_uncredited_v5866']=dict(file_path='/data/SC2.DK4',block=200,reviewed_objects=19,
        manuscript=str(DOC),reference_map=doc['reference_map'],representative_proof=doc['representative_proof'],
        native_revisions=13,native_retentions=6,new_completion_credit=0,actual_English_speeches=19,complete_matching_holds=73,
        source_commands=31,source_stored_bytes=932,target_stored_bytes=828,source_end=926,target_end=824,
        source_tailzeros=2,target_tailzeros=0,all19_native_glyph_planes_and152_alignments_pass=True,
        native_source_consumer_negatives=18,formatter_negatives=28,final_stored_macro_cases=76,
        source_cold_boot_reused=True,new_English_cold_boots=1,new_English_frames=13001,
        speech_duration_changes=8,shifted_pairs=19,later_prompt_differences=6,later_sailing_cloud_differences=10,
        final_PRNG_seeds_differ=True,complete_timing_and_cloud_native_object_untraced=True,
        atomic_compiler_registered_release_patch_and_current_startup_pending=True)
'''
    p=source.index("    paths=[PRIOR,");q=source.index("    evidence={",p)
    paths='''    paths=[PRIOR,PACKET,GLOSS,DOC,CONTEXT,ACTUAL,NAMES,old_scope,scopepath,Path(__file__),Path('scripts/lil_B200_reference_text_v5866.py'),
        Path('work/analysis/lil_B200_reference_approval_v5865/reference_approval.json'),Path(doc['reference_map']),Path(doc['representative_proof']),
        Path(doc['final_padding_proof']),Path(doc['relocated_control_proof']),Path(doc['termination_decode_proof']),Path(doc['postscene_native_state_proof']),
        Path(doc['native_font_proof']),Path('work/analysis/lil_B200_native_approval_v5849/all19_source_prose_current_native_approval.json'),
        Path('work/analysis/lil_B200_phrase_layout_v5846/complete_courtesy_requests_and_source_bound_formatter_successors.json'),
        Path('work/analysis/lil_B200_English_run_v5860_reviewed_English/terminal.json'),
        Path('work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json'),
        Path('work/analysis/lil_B200_research_v5853/research_image_receipt.json'),
        Path('work/analysis/lil_B200_English_fixture_v5859/pin_and_runner_receipt.json'),
        Path('work/analysis/lil_B200_screen_review_v5864/paired_scene_return_and_measured_sailing_difference_sheets.json'),
        Path('work/analysis/lil_B200_postscene_difference_v5863/unmodified_final_difference_pixel_inventory.json'),
        Path('releases/all_routes_unified_v5816/verification.json'),Path('translations/release_stack.json')]
    for terminal in ['work/analysis/lil_B200_English_run_v5860_reviewed_English/terminal.json','work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json']:
        assert read(terminal)['terminal'] and read(terminal)['observer_host_slots_restored']
'''
    k=source.index('    new[KEY]=dict(');l=source.index('    new[SCOPE]=dict(',k)
    entry='''    new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,all19_B200_objects_uncredited=True,revised=13,retained=6,
        all19_native_planes152_alignments18_consumer28_formatter_negatives_approved=True,
        actual19_English_panels73_complete_holds=True,speech_duration_changes=8,shifted_start_return_pairs=19,
        sampled_nontext_equal=172,sampled_nontext_total=182,later_prompt_differences=6,later_sailing_cloud_differences=10,
        final_PRNG_seeds_differ=True,no_broad_simulation_or_complete_causal_claim=True,
        new_label_Stranger_draft_not_applied=True,existing_164_165_Man_Woman_drafts_and207_queue_preserved=True,
        new_research_ROMs=2,new_English_cold_boots=1,new_English_frames=13001,reused_Japanese_cold_boots=1,
        all_sessions_terminal_and_reaped=True,goal_turn_classification='progress',previous_goal_turn_classification='progress',no_duplicate_credit=True,full_goal_complete=False)
'''
    v=source.index("            save(VERIFY/'verified_handoff.json'")
    tail='''            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
                patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,**COUNTERS,
                completed=6263,source_prose=6266,revised=3928,retained=2335,SC2=4378,SC3=96,reviewed_routes=4664,completed_routes=4664,
                B200_uncredited_objects=19,B200_approved_revisions=13,B200_approved_retentions=6,
                B200_native_planes=19,B200_native_alignments=152,B200_source_consumer_negatives=18,B200_formatter_negatives=28,
                B200_final_stored_macro_cases=76,B200_actual_English_panels=19,B200_complete_matching_holds=73,
                source_return=7676,English_return=7677,eight_speech_duration_changes=True,shifted_start_return_pairs=19,
                sampled_nontext_equal=172,sampled_nontext_total=182,later_prompt_differences=6,later_sailing_cloud_differences=10,
                final_PRNG_seeds_differ=True,no_broad_simulation_or_complete_causal_claim=True,
                new_research_ROMs=2,new_English_cold_boots=1,new_English_frames=13001,reused_Japanese_cold_boots=1,
                actor172_Stranger_target_pending=True,paired164_165_Man_Woman_drafts_preserved=True,catalog_queue=207,
                registered_release_compiler_and_current_startup_pending=True,no_promotion_commit_push_or_pruning=True,
                main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5867 verified:19 B200 reference/actual-approved objects remain uncredited;V5816/main/counters unchanged. Full goal active.')
'''
    changes={source[a:b]:checks,source[a2:b2]:scope,source[p:q]:paths,source[k:l]:entry,source[v:]:tail,
        'lil_B200_and_names_checkpoint_v5841':'lil_B200_reference_checkpoint_v5866',
        'verification_v5842':'verification_v5867','verification_v5822':'verification_v5842',
        'Lil_B200_clean_context_prose_and_anonymous_name_v5841':'Lil_B200_reference_approved_uncredited_v5866',
        "SCOPE='unfinished_editorial_scope_v5841'":"SCOPE='unfinished_editorial_scope_v5866'",
        'previous_latest_checkpoint_before_B200_and_names_v5841':'previous_latest_checkpoint_before_B200_references_v5866',
        "OLD_SCOPE='unfinished_editorial_scope_v5821'":"OLD_SCOPE='unfinished_editorial_scope_v5841'",
        'lil_B200_checkpoint_text_v5841':'lil_B200_reference_text_v5866','manuscript_v1.json':'manuscript_v5.json',
        '## V5841: B200 clean-source contextual draft and anonymous speaker-label review':'## V5866: B200 complete native/reference and19 English panels approved;registered release pending',
        '# Current editorial handoff - V5841':'# Current editorial handoff - V5866',
        'Six targets staged;B20019 prose objects and actor172 label remain uncredited and unintegrated.':'Six targets staged;B20019 approved reference objects remain uncredited pending registered release.'}
    tool=derive('scripts/checkpoint_lil_B200_and_names_v5841.py','scripts/checkpoint_lil_B200_references_v5866.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'prepared_lossless_reference_checkpoint.json',dict(tool=tool,all19_disjoint_objects_still_uncredited=True,
        complete_scope_history_names_and_measured_sailing_differences_preserved=True,new_review_credit=0,full_goal_complete=False))
    print('Lossless B200 reference checkpoint prepared;all counters and prior root/nested history must remain exact.')
