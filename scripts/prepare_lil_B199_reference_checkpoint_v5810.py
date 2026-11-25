"""Prepare a history-preserving reference-approved checkpoint with measured actual scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_reference_checkpoint_tools_v5810')
SCOPE_TEXT='''    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT
    scope['historical_Lil_B199_native_approved_before_v5810']=scope.pop('next_Lil_B199_native_approved_uncredited_v5794')
    scope['next_Lil_B199_reference_approved_uncredited_v5810']=dict(
        manuscript='translations/lil_B199_editorial_manuscript_v6.json',
        reference_map='translations/lil_B199_editorial_relocation_map_v1.json',
        reference_approval='work/analysis/lil_B199_reference_approval_v5809/reference_approval.json',
        reviewed_objects=31,revisions=11,justified_retentions=20,new_completion_credit=0,
        actual_English_panels=31,complete_native_holds=120,sampled_nontext_frames=182,
        source_return10776_English10778=True,speech_duration_changes=6,shifted_command_pairs=34,
        later_prompt_RGB_differences=6,final_PRNG_seeds_differ=True,all_queried_native_final_components_equal=True,
        no_broad_future_world_or_RNG_equivalence_claim=True,atomic_compiler_semantic_negatives_registered_release_and_startup_pending=True)
    scope['C_drive_space_recovery_v5810']=dict(
        manifest='work/analysis/storage_recovery_v5810/before_manifest.json',
        receipt='work/analysis/storage_recovery_v5810/relocation_receipt.json',
        preserved_runtime_files=29402,all_bytes_bound_in_receipt_original_path_retained=True,
        no_ROM_translation_or_proof_deleted=True,resolved_not_blocking=True,
        failed_text_helper_zero_byte_preserved=True,text_helper='scripts/lil_B199_reference_text_v5810b.py')
'''
GATES='''    reference=read('work/analysis/lil_B199_reference_approval_v5809/reference_approval.json')
    assert reference['all31_source_native_reference_and_representative_rules_approved'] and reference['source_prose_English_and_compiled_targets_unchanged']
    assert sha(Path(reference['manuscript']).read_bytes())==reference['manuscript_sha256']
    assert sha(Path(reference['reference_map']).read_bytes())==reference['reference_map_sha256']
    en_actual=read('work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json')
    state=read('work/analysis/lil_B199_timing_state_v5808b/six_speech_duration_changes_34_shifted_pairs_prompt_bounds_and_native_state.json')
    assert en_actual['actual_unique_speech_panels']==en_actual['complete_matching_observations']==31 and en_actual['complete_matching_holds']==120
    assert not en_actual['failures'] and not en_actual['paired_region_differences'] and en_actual['offline_only_source_indices']==[]
    assert len(en_actual['all_sampled_frame_comparisons'])==182 and all(r['nontext_region_difference_bbox'] is None for r in en_actual['all_sampled_frame_comparisons'])
    assert len(en_actual['actual_timing_differences'])==34 and len(en_actual['later_whole_RGB_differences'])==6
    assert state['actual_proof_sha256']==sha(Path('work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json').read_bytes())
    assert all(state['native_final_component_equality'].values()) and not state['final_PRNG_seeds_equal']
    en_terminal=read('work/analysis/lil_B199_English_run_v5806_reviewed_English/terminal.json')
    assert en_terminal['terminal'] and en_terminal['observer_host_slots_restored']
    recovery=read('work/analysis/storage_recovery_v5810/relocation_receipt.json')
    assert recovery['Files']==29402 and recovery['AllOriginalPathsByteExact'] and recovery['NoContentModified']
    assert recovery['GeneratedROMsTranslationsAndProofsDeleted']==0 and Path(recovery['OriginalPath']).is_dir()
'''
EXTRA='''        Path('translations/lil_B199_editorial_manuscript_v6.json'),Path('translations/lil_B199_editorial_relocation_map_v1.json'),
        Path('work/analysis/lil_B199_reference_approval_v5809/reference_approval.json'),
        Path('work/analysis/lil_B199_reference_approval_v5809/representative_display_control_and_transition_reconciliation.json'),
        Path('work/analysis/lil_B199_stored_v5798/all31_final_stored_targets124_macro_cases_and_complete_planes.json'),
        Path('work/analysis/lil_B199_research_v5800/research_image_receipt.json'),
        Path('work/analysis/lil_B199_loader_v5801/whole_SC2_and_B199_initial_entry_proof.json'),
        Path('work/analysis/lil_B199_reference_census_v5802/all47_commands_no_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_B199_ends_v5803/two_declared_tail_end_decodes_no_relative_sites.json'),
        Path('work/analysis/lil_B199_relocated_controls_v5804/all31_dispatches_two_picture_two47xx_pairs_one_pause_and16_exact_leaves.json'),
        Path('work/analysis/lil_B199_English_fixture_v5805/complete_B199_English_B22_fixture.json'),
        Path('work/analysis/lil_B199_English_fixture_v5805/pin_and_runner_receipt.json'),
        Path('work/analysis/lil_B199_English_run_v5806_reviewed_English/terminal.json'),
        Path('work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json'),
        Path('work/analysis/lil_B199_screen_review_v5808/paired_scene_and_return_sheets_with_measured_limits.json'),
        Path('work/analysis/lil_B199_timing_state_v5808b/six_speech_duration_changes_34_shifted_pairs_prompt_bounds_and_native_state.json'),
        Path('work/analysis/storage_recovery_v5810/before_manifest.json'),Path('work/analysis/storage_recovery_v5810/relocation_receipt.json'),
        Path('scripts/lil_B199_reference_text_v5810.py'),Path('scripts/lil_B199_reference_text_v5810b.py'),
'''
if __name__=='__main__':
    assert not ROOT.exists()
    text=Path('scripts/checkpoint_lil_B199_native_v5794.py').read_text(encoding='utf-8')
    a=text.index("    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT")
    b=text.index("    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope",a)
    result=derive('scripts/checkpoint_lil_B199_native_v5794.py','scripts/checkpoint_lil_B199_references_v5810.py',{
        text[a:b]:SCOPE_TEXT,'lil_B199_native_checkpoint_v5794':'lil_B199_reference_checkpoint_v5810',
        'verification_v5795':'verification_v5811','verification_v5777':'verification_v5795',
        'Lil_B199_source_prose_native_approved_uncredited_v5794':'Lil_B199_reference_approved_uncredited_v5810',
        "SCOPE='unfinished_editorial_scope_v5794'":"SCOPE='unfinished_editorial_scope_v5810'",
        "OLD_SCOPE='unfinished_editorial_scope_v5776'":"OLD_SCOPE='unfinished_editorial_scope_v5794'",
        'previous_latest_checkpoint_before_B199_native_v5794':'previous_latest_checkpoint_before_B199_references_v5810',
        'from scripts.lil_B199_checkpoint_text_v5794 import':'from scripts.lil_B199_reference_text_v5810b import',
        '    ROOT.mkdir(parents=True);scopepath=ROOT/':GATES+'    ROOT.mkdir(parents=True);scopepath=ROOT/',
        "        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/release_stack.json')]":
        EXTRA+"        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/release_stack.json')]",
        'one_new_source_research_ROM_one13001_frame_boot_no_completion_credit=True':'two_new_research_ROMs_one_new_English13001_frame_boot_no_completion_credit=True',
        'native_approved_objects=31,':'native_approved_objects=31,reference_and_English_content_approved_objects=31,',
        '## V5794: B199 complete source scene and31 native-approved contextual reviews':
        '## V5810: B199 references and31 English scene panels approved;registered release pending',
        '# Current editorial handoff - V5794':'# Current editorial handoff - V5810',
        'Six targets staged;31 native-approved B199 objects remain uncredited pending English reference/actual/release.':
        'Six targets staged;31 B199 reference/English-scene approved objects remain uncredited pending atomic compiler/release.',
        'new_source_research_ROMs=1,new_source_cold_boots=1,new_source_frames=13001,':
        'new_research_ROMs=2,new_English_content_cold_boots=1,new_English_frames=13001,reused_Japanese_cold_boots=1,',
        'no_English_scene_or_registered_release_claim=True':'all31_English_panels120_holds182_nontext_samples_approved=True,measured_timing_prompt_and_PRNG_differences_preserved=True,no_registered_release_claim=True',
        'V5795 verified:31 native-approved uncredited reviews and one complete Japanese source boot saved;V5756/main/counters unchanged. Full goal active.':
        'V5811 verified:31 reference/English-scene approved objects saved without credit. V5756/main/counters exact;atomic compiler/release next. Full goal active.'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_checkpoint_tool.json',dict(derivation=result,
        all_original_root_and_nested_history_recoverable=True,no_shared_mutation_yet=True))
    print('Reference-approved six-file checkpoint prepared;all historical inverse/hash/fsync guards retained.')
