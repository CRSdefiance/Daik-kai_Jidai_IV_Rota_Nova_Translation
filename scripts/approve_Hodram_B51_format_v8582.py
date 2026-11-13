"""Approve five source-qualified formats with representative actual scope explicit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_format_v8582')
OLD = Path('translations/hodram_B51_editorial_manuscript_v3.json')
DOC = Path('translations/hodram_B51_editorial_manuscript_v4.json')
OLD_NAMES = Path('translations/hodram_B51_speaker_name_review_v1.json')
NAMES = Path('translations/hodram_B51_speaker_name_review_v2.json')
PROOFS = {
    'source_gloss': 'work/analysis/Hodram_B51_clean_gloss_v8549/five_first_clean_glosses_warning_andconditional_reactions.json',
    'source_controls': 'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json',
    'source_display': 'work/analysis/Hodram_B51_source_display_v8556/source_display.json',
    'source_view': 'work/analysis/Hodram_B51_source_view_v8557/source_view.json',
    'result_flow': 'work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    'current': 'work/analysis/Hodram_B51_current_v8559/current_effective.json',
    'logical': 'work/analysis/Hodram_B51_logical_v8561/logical_paragraphs.json',
    'pages': 'work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json',
    'native_view': 'work/analysis/Hodram_B51_native_review_v8564/native_body_review.json',
    'relocation': 'work/analysis/Hodram_B51_relocation_v8565/reconstruction.json',
    'stored': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
    'independent': 'work/analysis/Hodram_B51_independent_v8569/independent_reconstruction.json',
    'reference': 'work/analysis/Hodram_B51_reference_v8570b/research_image_receipt.json',
    'reference_qualification': 'work/analysis/Hodram_B51_reference_v8570b/qualification.json',
    'loaders': 'work/analysis/Hodram_B51_loaders_v8571/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
    'references': 'work/analysis/Hodram_B51_references_v8572/references.json',
    'fixtures': 'work/analysis/Hodram_B51_fixtures_v8573/two_whole_scripts.json',
    'models': 'work/analysis/Hodram_B51_models_v8575/native_models.json',
    'whole_actual': 'work/analysis/Hodram_B51_actual_v8576/B51/paired_actual_dialogue_headers_flow_returns.json',
    'whole_view': 'work/analysis/Hodram_B51_actual_review_v8579/whole_exchange_review.json',
    'comparison': 'work/analysis/Hodram_B51_comparison_v8577/paired_selected_path_comparison.json',
    'differences': 'work/analysis/Hodram_B51_difference_view_v8578/sheet.json',
}

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    old, names = map(read, [OLD, OLD_NAMES])
    data = {key: read(path) for key, path in PROOFS.items()}
    assert old['review_gates'] == ['source', 'context', 'localization', 'naturalness', 'formatting']
    assert old['translation_policy'] == 'natural-dialogue-v2' and old['target_locale'] == 'en-US' and old['encoder'] == 'dialogue-relocatable-v1'
    assert len(old['records']) == old['physical_speech_objects'] == 5 and old['typed_choice_objects'] == old['source_FE_panels'] == 0
    assert all(all(row['review'][key] for key in ['source', 'context', 'localization', 'naturalness']) and not row['review']['formatting'] for row in old['records'])
    assert data['native_view']['all_five_complete_bodies_visually_read'] and data['native_view']['no_qa_waivers']
    assert data['stored']['all5_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass']
    assert data['stored']['compiler_tail_creates_no_blank_oradditional_page'] and data['stored']['whole_current_inmemory_ROM_inverse_byte_exact']
    assert data['independent']['whole_target_block_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert data['reference']['only_changed_blocks'] == [51] and data['reference_qualification']['actual_changed_blocks'] == [51]
    assert len(data['stored']['stored_dispatches']) == 5 and len(data['stored']['stored_queries']) == 2 and len(data['stored']['normal_seeded_ends']) == 25
    assert len(data['result_flow']['caller_fragment_cases']) == 50 and len(data['result_flow']['source_structural_paths']) == 10
    assert not data['whole_actual']['unresolved'] and data['whole_actual']['all_observed_complete_body_name_holds_andnative_flow_pass']
    actual_review = data['whole_view']
    assert actual_review['all_three_sheets_directly_viewed'] and actual_review['actual_complete_source_andEnglish_body_name_holds'] == 56
    assert actual_review['actual_frames'] == 20002 and actual_review['unvisited_conditional_text_IDs'] == ['DK4_MES_B51_R0032']
    assert actual_review['Charles_actor18_complete_source_compiled_stored_macro_name_glyph_bounds_andrelocated_branches_bound_offline_not_actual']
    observed = set(actual_review['actual_source_speech_IDs'])
    assert len(observed) == 4 and observed | {'DK4_MES_B51_R0032'} == {r['id'] for r in old['records']}
    refs = {r['id']: r for r in data['stored']['records']}
    doc, ng = deepcopy(old), deepcopy(names)
    for row in doc['records']:
        ref = refs[row['id']]
        assert row['final_reference'] == ref['final_reference'] and row['final_stored_hex'] == ref['stored_hex'] and row['compiled_hex'] == ref['compiled_hex']
        actual = []
        for group in data['whole_actual']['groups']:
            speech = next((s for s in group['speeches'] if s['id'] == row['id']), None)
            if speech is not None:
                assert speech['complete_holds'] and speech['selected_capture']
                actual.append(dict(version=group['version'], source_selector=speech['source_selector'], name=speech['name'],
                    selected_capture=speech['selected_capture'], complete_holds=len(speech['complete_holds'])))
        assert len(actual) == (2 if row['id'] in observed else 0)
        reason = row['native_body_review_reason'] + ' Complete stored glyphs, compiler parity, original preambles/relative targets/queries/full end, exact references and independent inverses pass at the original216px width, without shortening, authored breaks, extra pages or QA waivers.'
        if actual:
            reason += ' Both complete initialized source/English runs show this single page, full name/portrait and normal transitions; the original unforced path is preserved.'
        else:
            reason += ' The original unforced raw predicate omits Charles in both actual runs. His exact actor18/voice0/name consumers, complete native source/English/stored page, twenty relevant guarded alignments across stages, bounds/pagination and all relocated branch extents are checked offline. Actor/header code and whole actual actors remain identical. Existing representative actual coverage plus these focused checks resolve the display/control risk without forcing a conditional visit; no actual Charles-header observation is claimed.'
        row.update(actual_display_evidence=actual, formatting_approval_reason=reason, formatting_registered_release_pending=True,
            current_review_status='all-five-individual-gates-reviewed-frozen-policy-atomic-registered-release-pending')
        row['review']['formatting'] = True
        row['final_hex'] = row['stored_hex'] = row['final_stored_hex']
    assert [r['actor_ID'] for r in ng['records']] == [1, 16, 18, 113] and all(all(r['review'].values()) for r in ng['records'])
    for name in ng['records']:
        name.update(actual_B51_header_observed=name['actor_ID'] in [1, 16, 113],
            actual_body_name_proof=PROOFS['whole_actual'], actual_body_name_proof_sha256=sha(Path(PROOFS['whole_actual']).read_bytes()),
            native_offline_only_B51_header=name['actor_ID'] == 18, registered_name_asset_change=False)
    ng.update(predecessor=str(OLD_NAMES), predecessor_sha256=sha(OLD_NAMES.read_bytes()),
        actual_observed_header_actor_IDs=[1, 16, 113], actor18_complete_native_header_only=True,
        all207_names_roles_aliases_customnames_andwider_Port_Worker_contexts_still_open=True, new_credit=0, full_goal_complete=False)
    ROOT.mkdir(parents=True)
    save(NAMES, ng)
    doc.update(predecessor_manuscript=str(OLD), predecessor_manuscript_sha256=sha(OLD.read_bytes()), names_packet=str(NAMES), names_packet_sha256=sha(NAMES.read_bytes()),
        all_five_four_prose_gates_true_formatting_false=False, all_five_formatting_gates_still_false=False, all_five_individual_five_gates_true=True,
        reference_ROM=data['reference']['research_ROM'], reference_ROM_sha256=data['reference']['research_ROM_sha256'],
        total_actual_frames=20002, actual_complete_body_name_holds=56, formatting_evidence={k: dict(path=p, sha256=sha(Path(p).read_bytes())) for k, p in PROOFS.items()},
        measured_limits=actual_review, status='all-five-individual-gates-reviewed-frozen-policy-atomic-registered-release-pending',
        remaining_required_work='Frozen source-qualified v2 policy, meaningful changed-input rejection tests, independent production evidence readers, one-complete-NDS atomic commit, registered cumulative release/exact clean-input patch/own startup, then once-only five-record credit.',
        no_new_ROM_orregistered_stage_orcompletion_credit=True, new_credit=0, full_goal_complete=False)
    for before, after in zip(old['records'], doc['records'], strict=True):
        for key in ['id', 'english', 'source_hex', 'source_reference', 'current_hex', 'current_reference', 'compiled_hex', 'final_reference', 'final_stored_hex', 'decision', 'finding', 'retention_reason']:
            assert before[key] == after[key]
    validate_natural_dialogue_batch(doc)
    save(DOC, doc)
    save(ROOT / 'formatting_approval.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), predecessor=str(OLD), predecessor_sha256=sha(OLD.read_bytes()),
        names=str(NAMES), names_sha256=sha(NAMES.read_bytes()), individual_speech_approvals=5, typed_choices=0, scoped_name_retentions=4,
        all5_five_gates_true=True, all_source_current_final_references_bound=True, all_approved_words_andcompiled_bytes_unchanged=True,
        actual_frames=20002, actual_emulator_runs=2, complete_holds=56, observed_speech_IDs=sorted(observed), unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
        no_FE_panel_oritem_geometry_claim=True, measured_limits=actual_review, standard_natural_dialogue_v2_validation_passes=True,
        registered_policy_atomic_build_patch_startup_andonceonly_credit_still_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [OLD, OLD_NAMES, *map(Path, PROOFS.values()), Path(__file__)]}))
    print('B51 five individual formatting gates approved; exact words/bytes/refs preserved. Four speeches actual, Charles focused native/offline; all limits retained. Standard v2 passes; policy/atomic/registered integration pending, zero credit.')
