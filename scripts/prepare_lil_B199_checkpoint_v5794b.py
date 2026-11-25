"""Prepare a lossless six-file native-approved progress checkpoint, without credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_checkpoint_tools_v5794b')
SCOPE_TEXT='''    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT
    scope['historical_Lil_B199_clean_source_before_v5794']=scope.pop('next_Lil_B199_clean_review_pending')
    scope['next_Lil_B199_native_approved_uncredited_v5794']=dict(
        manuscript='translations/lil_B199_editorial_manuscript_v5.json',
        native_approval='work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json',
        source_actual='work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json',
        reviewed_objects=31,revisions=11,justified_retentions=20,new_completion_credit=0,
        source_actual_speeches=31,source_actual_frames=13001,source_end_return_frame=10776,
        native_alignment_cases=248,source_consumer_negatives=22,formatter_negatives=28,
        effective_R58_registered_catalog_Camille_and_question_already_integrated=True,
        preserved_one_FI_two_private_thoughts_and_two_attempted_gift_corrections=True,
        English_reference_relocation_actual_atomic_compiler_and_registered_release_pending=True)
    scope['C_drive_space_recovery_v5790']=dict(
        cache_manifest='work/analysis/storage_recovery_v5790/before_manifest.json',
        relocation_receipt='work/analysis/storage_recovery_v5790/relocation_receipt.json',
        compressed_logical_bytes_verification='work/analysis/storage_recovery_v5790/unchanged_document_hashes_and_preserved_failed_layout.json',
        preserved_cache_files=102,preserved_cache_byte_count_bound_in_receipt=True,
        no_ROM_translation_or_proof_deleted=True,resolved_not_blocking=True,
        failed_formatter_v2_zero_byte_preserved=True,approved_formatter='dk4tool/dialogue/lil_B199_layout_v3.py')
'''
EXTRA='''        Path('translations/lil_B199_editorial_manuscript_v5.json'),
        Path('work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json'),
        Path('work/analysis/lil_B199_fonts_v5792/all31_progressive_FE_native_planes_and248_alignment_cases.json'),
        Path('work/analysis/lil_B199_controls_v5778/sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json'),
        Path('work/analysis/lil_B199_source_fixture_v5780/complete_B199_source_B22_fixture.json'),
        Path('work/analysis/lil_B199_source_fixture_v5780/pin_receipt.json'),
        Path('work/analysis/lil_B199_source_run_v5781_clean_Japanese/terminal.json'),
        Path('work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json'),
        Path('work/analysis/lil_B199_comparison_v5783b/all31_complete_clean_and_predecessor_exchange.json'),
        Path('work/analysis/lil_B199_comparison_v5783b/complete_clean_context_actual_source_and_project_name_reconciliation.json'),
        Path('work/analysis/lil_B199_comparison_correction_v5783c/correction_receipt.json'),
        Path('work/analysis/lil_B199_macro_markup_v5786/one_exact_runtime_macro_markup_no_prose_change.json'),
        Path('work/analysis/lil_B199_idiom_layout_v5790b/one_complete_idiom_protection_and_justified_three_row_gift_response.json'),
        Path('work/analysis/storage_recovery_v5790/before_manifest.json'),
        Path('work/analysis/storage_recovery_v5790/relocation_receipt.json'),
        Path('work/analysis/storage_recovery_v5790/unchanged_document_hashes_and_preserved_failed_layout.json'),
        Path('dk4tool/dialogue/lil_B199_layout_v2.py'),Path('dk4tool/dialogue/lil_B199_layout_v3.py'),
        Path('dk4tool/dialogue/lil_B199_profile.py'),Path('scripts/lil_B199_checkpoint_text_v5794.py'),
'''
GATES='''    manuscript=read('translations/lil_B199_editorial_manuscript_v5.json')
    approval=read('work/analysis/lil_B199_native_approval_v5793/all31_source_prose_current_native_approval.json')
    actual=read('work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json')
    terminal=read('work/analysis/lil_B199_source_run_v5781_clean_Japanese/terminal.json')
    assert len(manuscript['records'])==31 and manuscript['revised']==11 and manuscript['retained']==20
    assert all(all(r['review'].values()) for r in manuscript['records'])
    assert manuscript['source_prose_or_completion_credit_added']==0 and not manuscript['formatting_review_pending']
    assert approval['manuscript_sha256']==sha(Path(approval['manuscript']).read_bytes())
    assert approval['all248_current_native_alignment_cases_and_complete_planes_pass']
    assert approval['source_consumer_negatives']==22 and len(approval['formatter_negatives'])==28
    assert actual['selected_source_speech_indices']==[r['source_record_index'] for r in manuscript['records']]
    assert not actual['unvisited_source_indices'] and actual['source_end1162_return_frame']==10776 and actual['total_frames']==13001
    assert len(actual['command_pairs'])==56 and terminal['terminal'] and terminal['observer_host_slots_restored']
    fixture=read('work/analysis/lil_B199_source_fixture_v5780/complete_B199_source_B22_fixture.json')['fixtures'][0]
    assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==terminal['research_ROM_sha256']
    assert len(fixture['all56_stored_fixture_commands'])==56 and len(fixture['original_text_records'])==31
    assert any(Path(p['path']).resolve()==Path(fixture['research_ROM']).resolve() for p in read('translations/rom_retention_pins.json'))
'''
if __name__=='__main__':
    assert not ROOT.exists()
    text=Path('scripts/checkpoint_lil_B199_and_names_v5776.py').read_text(encoding='utf-8')
    a=text.index('SUMMARY=(');b=text.index('\ndef inverse(',a)
    x=text.index("    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT")
    y=text.index("    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope",x)
    changes={text[a:b]:'from scripts.lil_B199_checkpoint_text_v5794 import SUMMARY,NEXT\n',text[x:y]:SCOPE_TEXT,
        'lil_B199_and_names_checkpoint_v5776':'lil_B199_native_checkpoint_v5794',
        'verification_v5777':'verification_v5795','verification_v5762':'verification_v5777',
        "KEY='Lil_B199_clean_source_and_couple_names_context_v5776'":"KEY='Lil_B199_source_prose_native_approved_uncredited_v5794'",
        "SCOPE='unfinished_editorial_scope_v5776'":"SCOPE='unfinished_editorial_scope_v5794'",
        'previous_latest_checkpoint_before_B199_and_names_v5776':'previous_latest_checkpoint_before_B199_native_v5794',
        "OLD_SCOPE='unfinished_editorial_scope_v5761'":"OLD_SCOPE='unfinished_editorial_scope_v5776'",
        '    ROOT.mkdir(parents=True);scopepath=ROOT/':GATES+'    ROOT.mkdir(parents=True);scopepath=ROOT/',
        "        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/release_stack.json')]":
        EXTRA+"        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/release_stack.json')]",
        'no_new_ROM_emulator_or_duplicate_credit=True':'one_new_source_research_ROM_one13001_frame_boot_no_completion_credit=True',
        'Lil_B199_uncredited_objects=31,':'Lil_B199_uncredited_objects=31,native_approved_objects=31,',
        '## V5776: B199 clean-first context and paired speaker-label localization draft':
        '## V5794: B199 complete source scene and31 native-approved contextual reviews',
        '# Current editorial handoff - V5776':'# Current editorial handoff - V5794',
        'Six targets staged;31 clean B199 objects and two proposed role-label changes remain uncredited.':
        'Six targets staged;31 native-approved B199 objects remain uncredited pending English reference/actual/release.',
        'catalog_queue=207,no_new_ROM_or_emulator_run=True,no_promotion_commit_push_or_pruning=True,':
        'catalog_queue=207,new_source_research_ROMs=1,new_source_cold_boots=1,new_source_frames=13001,native_approved_B199_objects=31,native_alignment_cases=248,source_consumer_negatives=22,formatter_negatives=28,no_English_scene_or_registered_release_claim=True,no_promotion_commit_push_or_pruning=True,',
        'V5777 verified: source progress saved;V5756/main/counters unchanged. Full goal active.':
        'V5795 verified:31 native-approved uncredited reviews and one complete Japanese source boot saved;V5756/main/counters unchanged. Full goal active.'}
    result=derive('scripts/checkpoint_lil_B199_and_names_v5776.py','scripts/checkpoint_lil_B199_native_v5794.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_checkpoint_derivation.json',dict(derivation=result,
        six_file_hash_gzip_fsync_and_full_inverse_protocol_preserved=True,no_coverage_or_ROM_mutation_yet=True))
    print('Lossless31-object native-approved checkpoint tool prepared;no shared mutations yet.')
