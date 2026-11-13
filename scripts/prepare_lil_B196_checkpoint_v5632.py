"""Prepare a six-target lossless reference/gameplay progress checkpoint;zero credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_checkpoint_tools_v5632')
GATES='''def gates():
    packet,evidence=original_native_gates()
    from scripts.seal_lil_B196_references_v5631 import OUTPUT,CHOICE_OUTPUT,MAP,VISUAL,ACTUAL,STORED,STORED_MENUS,CENSUS,CONTROL,ENDS,PLAN,ROM
    receipt_path=Path('work/analysis/lil_B196_reference_approval_v5631/approval_receipt.json')
    receipt=read(receipt_path);doc,choice=map(read,[OUTPUT,CHOICE_OUTPUT])
    assert receipt['manuscripts']=={str(p):sha(p.read_bytes()) for p in [OUTPUT,CHOICE_OUTPUT]}
    assert receipt['all36_source_native_reference_and_representative_rules_approved'] and receipt['source_prose_English_unchanged']
    assert receipt['reference_map_sha256']==sha(MAP.read_bytes()) and receipt['new_editorial_credit']==0
    assert len(doc['records'])==24 and len(choice['records'])==12
    rows=doc['records']+choice['records']
    assert sum(r['editorial_decision']=='revise' for r in rows)==15 and sum(r['editorial_decision']=='retain-wording' for r in rows)==21
    assert all(all(r['review'].values()) for r in rows)
    assert all(r['fresh_retained_wording_justification'] for r in rows if r['editorial_decision']=='retain-wording')
    visual,actual,mapping=map(read,[VISUAL,ACTUAL,MAP])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not visual['visual_review_pending']
    assert visual['no_open_translation_specific_display_menu_control_or_return_finding'] and not actual['failures']
    assert len(actual['actual_panels'])==13 and len(actual['all_actual_speech_observations'])==24 and len(actual['actual_menu_cases'])==13
    assert len(actual['offline_only_display_IDs'])==11 and receipt['actual_buy_menu_offsets']==[218,1588]
    assert receipt['actual_pass_menu_offsets']==[218,582,832,1156,1370,1588]
    assert visual['actual_new_cold_boot_runs']==6 and visual['total_frames']==78006
    assert not actual['command_timing_differences'] and not actual['later_whole_RGB_differences']
    assert len(visual['reaped_tool_sessions'])==6
    assert len(mapping['blocks'][0]['mapped_native_commands'])==119 and len(mapping['blocks'][0]['relative_skip_fixups'])==52
    assert mapping['blocks'][0]['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    for data in [receipt,visual,mapping,read(STORED),read(STORED_MENUS),read(CENSUS),read(CONTROL),read(ENDS)]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
    for s in visual['all_actual_consumer_menu_sheets_viewed']+visual['paired_full_screen_views']+[visual['first_buy_postscene_view']]:
        assert s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'];evidence[s['path']]=s['sha256']
    extra=[OUTPUT,CHOICE_OUTPUT,MAP,VISUAL,ACTUAL,STORED,STORED_MENUS,CENSUS,CONTROL,ENDS,PLAN,receipt_path,PRIOR,Path(__file__),Path('scripts/lil_B196_checkpoint_text_v5632.py')]
    evidence.update({str(p):sha(p.read_bytes()) for p in extra})
    assert sha(ROM.read_bytes())==mapping['blocks'][0].get('unowned_appended_copy',{}).get('ROM_sha256',sha(ROM.read_bytes()))
    prior=read(PRIOR);assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    packet['records']=doc['records'];packet['typed_choice_records']=choice['records']
    return packet,evidence

'''
SCOPE_BLOCK='''        scope['historical_Lil_B196_native_approved_before_v5632']=scope.pop('next_Lil_B196_native_approved_uncredited_v5613')
        scope['next_Lil_B196_reference_approved_uncredited_v5632']=dict(
            speech_manuscript='translations/lil_B196_editorial_manuscript_v4.json',
            speech_manuscript_sha256=sha(Path('translations/lil_B196_editorial_manuscript_v4.json').read_bytes()),
            choice_manuscript='translations/lil_B196_choice_manuscript_v3.json',
            choice_manuscript_sha256=sha(Path('translations/lil_B196_choice_manuscript_v3.json').read_bytes()),
            reference_map='translations/lil_B196_editorial_relocation_map_v1.json',
            reference_map_sha256=sha(Path('translations/lil_B196_editorial_relocation_map_v1.json').read_bytes()),
            objects=36,speeches=24,choice_labels=12,typed_choice_objects=6,revisions=15,retentions=21,
            uncredited=True,source_prose_native_relocation_stored_reference_representative_approved=True,
            actual_speech_panels=13,offline_only_speeches=11,actual_menu_cases=13,actual_cold_boots=6,actual_frames=78006,
            actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
            atomic_compiler_registered_cumulative_clean_patch_and_startup_pending=True,
            exact_R74_three_ordinary_wraps_with_all_words_native_guards_retained=True)
'''
ENTRY='''        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
            reference_approved_uncredited_objects=36,speech_objects=24,typed_choice_labels=12,typed_choice_objects=6,
            proposed_revisions=15,individually_justified_retentions=21,source_prose_or_completion_credit_added=0,
            all36_source_context_localization_naturalness_native_reference_and_representative_approved=True,
            source_stored_logical=[1816,1814],target_stored_logical=[1668,1668],source_tailzeros=2,target_tailzeros=0,
            commands=119,relative_sites=52,target_skip_cases=260,exact_opaque_leaves=37,ends=7,
            final_stored_speech_alignments=96,fresh_stored_alignments=40,exact_reused_alignments=56,
            final_stored_menu_count_calls=12,final_stored_menu_pointer_calls=24,
            actual_speech_panels=13,actual_speech_observations=24,offline_only_speeches=11,actual_menu_cases=13,
            actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
            actual_end_offsets=[364,1708,1810],actual_exit_frames=[4299,5258,5255],
            new_ROMs=3,new_emulator_runs=6,total_frames=78006,all_six_sessions_terminal_and_reaped=True,
            zero_measured_command_timing_or_sampled_postscene_RGB_differences=True,
            paired_five_native_groups_actor_captain_and_PRNG_equal_within_scope=True,
            earlier_failed_audit_and_state_serialization_producers_preserved=True,
            remaining_gates=['atomic-speech-and-six-menu-compiler-and-meaningful-negatives',
                'registered-cumulative-build-with-both-companions','clean-input-patch-release-checks-and-current-startup','credit36-once-after-integration'],
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B196_reference_approved_uncredited_objects=36,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
'''
VERIFY_BLOCK='''        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6155,source_prose=6158,revised=3874,retained=2281,SC2=4270,SC3=96,reviewed_routes=4556,completed_routes=4556,
            reference_approved_uncredited_Lil_B196_objects=36,B196_speeches=24,B196_choice_labels=12,B196_menus=6,
            proposed_revisions=15,individually_justified_retentions=21,all36_source_native_reference_representative_gates_true=True,
            actual_unique_speech_panels=13,offline_only_speeches=11,actual_speech_observations=24,actual_menu_cases=13,
            actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
            atomic_compiler_registered_release_clean_patch_and_current_startup_pending=True,
            new_editorial_credit=0,new_ROMs=3,new_emulator_runs=6,actual_frames=78006,main_V4701_preserved=True,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5632 verified;V5580 remains current.36 B196 reference/representative approvals uncredited;atomic integration next.Full editorial objective active.')
'''

if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/checkpoint_lil_B196_v5613.py');text=source.read_text(encoding='utf-8')
    g=text.index('def gates():');a=text.index('def audit(',g)
    s=text.index("        scope['historical_Lil_B196_source_only_before_v5613']");se=text.index("        inventory=ROOT/",s)
    k=text.index('        new[KEY]=');ke=text.index('        new[PREVIOUS]=',k)
    v=text.index("        save(VERIFY/'verified_handoff.json'")
    row=derive(source,'scripts/checkpoint_lil_B196_v5632.py',{
        text[g:a]:GATES,text[s:se]:SCOPE_BLOCK,text[k:ke]:ENTRY,text[v:]:VERIFY_BLOCK,
        'from scripts.checkpoint_lil_B196_v5599 import gates as original_source_gates':'from scripts.checkpoint_lil_B196_v5613 import gates as original_native_gates',
        'Lil_B196_native_review_v5613':'Lil_B196_reference_review_v5632',
        'v5613':'v5632','verification_v5614':'verification_v5633','verification_v5600':'verification_v5614',
        'unfinished_editorial_scope_v5599':'unfinished_editorial_scope_v5613',
        "'native_layout_retention_reason']":"'native_layout_retention_reason','actual_B22_display_fixture_observed','offline_only_native_display_checked','actual_label_visible','actual_choice_all_outcomes_observed']",
        'B196 contextual native reviews approved;36 uncredited objects':'B196 relocation and representative gameplay approved;36 uncredited objects',
        'native-review checkpoint':'reference/gameplay checkpoint','native-review checkpoint files':'reference/gameplay checkpoint files'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_checkpoint.json',dict(tool=row,source_prose_credit=0,completed_credit=0,
        previous_native_checkpoint_and_all_nested_history_preserved_by_full_inverse=True,
        six_targets=True,new_ROMs=3,new_emulator_runs=6,frames=78006,full_goal_complete=False))
