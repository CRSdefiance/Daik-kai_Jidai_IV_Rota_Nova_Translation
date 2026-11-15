"""Record seven source/native approvals; registered gameplay gates remain open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.retreat_transfer_native_plan_v1514 import compiled, IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/retreat_transfer_native_review_v1518')
OLD = Path('translations/retreat_transfer_editorial_manuscript_v2.json')
NEW = Path('translations/retreat_transfer_editorial_manuscript_v3.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc = read(OLD)
    paths = {
        'native_font_proof': 'work/analysis/retreat_transfer_fonts_v1515/native_font_research.json',
        'native_copy_proof': 'work/analysis/retreat_transfer_copies_v1516/all_native_copies_and_prefix_cache_sequence.json',
        'escape_regression_proof': 'work/analysis/retreat_transfer_escape_v1517/original_direct_escape_regression.json',
        'native_runtime_proof': 'work/analysis/retreat_transfer_runtime_v1510/native_runtime_verification.json',
    }
    fonts, copies, escape, runtime = [read(paths[k]) for k in paths]
    plan = read('work/analysis/retreat_transfer_payload_v1514/native_payload_plan.json')
    assert fonts['manuscript_sha256'] == sha(OLD.read_bytes())
    assert len(fonts['cases']) == 208 and not fonts['findings']
    assert len(fonts['invalid_compiler_inputs_rejected']) == 15
    assert len(fonts['all206_source_existing_actor_choices']) == 206
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_original_direct_pipeline_cases']) == 13
    assert all(p['ARM9_sha256'] == plan['target_ARM9_sha256'] and p['COMMON_sha256'] == plan['target_COMMON_sha256'] for p in [fonts, copies, escape])
    assert runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert read('work/analysis/retreat_transfer_runtime_v1510/scope_proof.json')['total_cases'] == 529429
    assert read('work/analysis/retreat_transfer_runtime_v1510/runtime_plan.json')['patches'] == plan['runtime_plan']['patches']
    for case in fonts['cases']:
        assert not case['findings'] and case['full228x64_native_and_independent_font_exact']
        assert case['all_literal_name_bytes_complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass']
        if case['preview']:
            assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    assert len(fonts['sheets_for_visual_review']) == 8
    for sheet in fonts['sheets_for_visual_review']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT / 'all64_native_panels_visual_review.json'
    save(visual, {'sheets': fonts['sheets_for_visual_review'],
        'all8_sheets_and64_native_panels_actually_visually_reviewed': True,
        'all208_full_glyph_planes_uniform6px_margins_complete_names_bounds_and_blank_paper_pass': True,
        'default_Latina_and_FALCON_ICARUS_FIFOFOFU_commands_start_complete_on_second_row': True,
        'maximal18byte_names_use_complete_three_row_balanced_wraps_without_missing_name_bytes': True,
        'source_CJK_font_shadows_and_fullwidth_spacing_preserved': True,
        'remaining_layout_findings': 0, 'registered_build_and_original_transfer_replay_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    approved = deepcopy(doc)
    approved.update(formatting_review_pending=False, status='seven-source-native-approved;registered-release-original-transfer-pending',
        reviewed_research_manuscript=str(OLD), reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        visual_review=str(visual), visual_review_sha256=sha(visual.read_bytes()))
    for key, path in paths.items():
        approved[key], approved[key + '_sha256'] = path, sha(Path(path).read_bytes())
    for row in approved['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-approved;registered-release-original-transfer-pending'
    validate_natural_dialogue_batch(approved)
    save(NEW, approved)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1323, 1467, 144)
    save(ROOT / 'coverage_before_native_approval.json', before)
    assert not set(IDS) & set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['records_with_source_and_prose_pass'] += 7
    ledger['records_with_source_prose_drafts'] += 7
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 7
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'], *IDS])
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(set(drafts['native_message_IDs']) | set(IDS))
    drafts['manuscripts'].append(str(NEW))
    drafts['manuscript_record_subsets_pending'][str(NEW)] = list(IDS)
    drafts['note'] = 'Retreat7 source/native approved, not yet integrated or replayed. Earlier144 reviewed COMMON entries and broader shared/routes/raw prose remain pending.'
    ledger['coverage_units'].append({'id': 'Shared-retreat-transfer7-source-prose', 'status': approved['status'],
        'native_message_IDs': list(IDS), 'manuscript': str(NEW), 'source_context': doc['source_context'],
        'native_visual_review': str(visual), 'completed_entries_added': 0, 'full_goal_complete': False})
    ledger['formatting_watchlist']['retreat_transfer7'] = {
        'native_message_IDs': list(IDS), 'native_approved_manuscript': str(NEW),
        'native_font_evidence': paths['native_font_proof'], 'native_visual_review': str(visual),
        'original_defect': 'V1492 role53DB8/27C/table02117080 treats some custom ship names as speech commands.',
        'native_literal_names_208_cases_pass': True, 'all64_review_panels_visually_reviewed': True,
        'registered_release_pending': True, 'original_transfer_replay_pending': True,
        'full_goal_complete': False}
    summary = ('V1518 source/native-approves seven retreat notices2683-2689, all revised: faithful flagship incapacitation and transfer to another ship. '
        '208 complete original role/printf/macro/wrap/font planes across8 voices26 names,206 existing actor choices,15 compiler negatives, '
        '529429 native selector/ABI cases,7336 copies180 cache sequences13 earlier escapes pass. All8 sheets64 panels actually viewed; '
        'literal names, edge letters, uniform margins and bounds pass. Existing186/188 selector bytes,172-byte gate,3661 other texts/copies, '
        '40 blocks and123040 staged bytes preserved. Registered build/exact patch/startup/original transfer replay remain pending. '
        'Counts1323 complete(985 revised338 retained),1474 source/prose,151 reviewed-incomplete COMMON. V1492 remains promoted; '
        'canonical,V997,V1430 completed-native reference,graphics/all18 plaques and later older-record re-audit remain unchanged/open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id': 'V1518-retreat7-source-native-approved', 'manuscript': str(NEW),
        'proof': str(ROOT / 'native_approval_receipt.json'), 'source_prose_reviews_added': 7, 'completed_entries_added': 0, 'full_goal_complete': False})
    for key in ['records_editorially_completed', 'records_revised_and_integrated', 'retained_wordings_editorially_completed',
                'completed_editorial_record_counts_by_file', 'current_integrated_candidate', 'current_native_relocation_reference',
                'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit']:
        assert ledger[key] == before[key], key
    save(ledger_path, ledger)
    text = '# V1518 retreat transfer native approval\n\n' + summary + '\n\nOriginal V1492 transfer evidence: `work/analysis/stronger_fleet_return_verified_v1505/actual_declaration_defeat_and_transfer_return.json`. '
    text += 'The normal original actor/table choice is2684; these native probes and role counterfactuals do not establish revised gameplay. No new completion credit.\n'
    Path('docs/retreat_transfer_v1518_native_checkpoint.md').write_text(text, encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs') / name).open('a', encoding='utf-8', newline='\n') as f:
            f.write('\n\n## V1518 retreat transfer native approval\n\n' + summary + '\n\nSee [checkpoint](retreat_transfer_v1518_native_checkpoint.md).\n')
    save(ROOT / 'native_approval_receipt.json', {'manuscript': str(NEW), 'manuscript_sha256': sha(NEW.read_bytes()),
        'proofs': {p: sha(Path(p).read_bytes()) for p in [*paths.values(), str(visual)]},
        'completed': 1323, 'source_prose': 1474, 'reviewed_incomplete_COMMON': 151,
        'source_prose_reviews_added': 7, 'completed_entries_added': 0,
        'registered_release_and_original_transfer_pending': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Retreat7 source/native approved;1474 source/prose,1323 complete,151 COMMON pending. Registered build/original transfer remain open.')
