"""Approve source/native presentation only; actual special-target inspection remains open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sea_responses_native_plan_v1556 import compiled, IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sea_responses_native_review_v1561')
OLD = Path('translations/sea_responses_editorial_manuscript_v1.json')
NEW = Path('translations/sea_responses_editorial_manuscript_v2.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc = read(OLD)
    paths = {'native_font_proof': 'work/analysis/sea_responses_fonts_v1558/native_font_research.json',
        'native_copy_proof': 'work/analysis/sea_responses_copies_v1559/all_native_copies_and_prefix_cache_sequence.json',
        'escape_regression_proof': 'work/analysis/sea_responses_escape_v1560/original_direct_escape_regression.json',
        'native_runtime_proof': 'work/analysis/sea_responses_runtime_v1557/native_runtime_verification.json'}
    fonts, copies, escape, runtime = [read(p) for p in paths.values()]
    plan = read('work/analysis/sea_responses_payload_v1556/native_payload_plan.json')
    assert fonts['manuscript_sha256'] == sha(OLD.read_bytes()) and len(fonts['cases']) == 8 and not fonts['findings']
    assert len(fonts['all207_existing_actor_choices']) == 207 and len(fonts['seven_CPU_only_role_counterfactuals']) == 7
    assert len(fonts['invalid_compiler_inputs_rejected']) == 14
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_original_direct_pipeline_cases']) == 13
    assert all(p['ARM9_sha256'] == plan['target_ARM9_sha256'] and p['COMMON_sha256'] == plan['target_COMMON_sha256'] for p in [fonts, copies, escape])
    assert runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert read('work/analysis/sea_responses_runtime_v1557/scope_proof.json')['total_cases'] == 529455
    assert read('work/analysis/sea_responses_runtime_v1557/runtime_plan.json')['patches'] == plan['runtime_plan']['patches']
    for case in fonts['cases']:
        assert not case['findings'] and case['full228x64_native_and_independent_font_exact']
        assert case['complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    assert len(fonts['sheets_for_visual_review']) == 1
    for sheet in fonts['sheets_for_visual_review']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT / 'all8_native_panels_visual_review.json'
    save(visual, {'sheets': fonts['sheets_for_visual_review'], 'all1_sheet_and8_native_panels_actually_visually_reviewed': True,
        'all8_full_glyph_planes_ordered_complete_letters_uniform6px_margins_bounds_and_blank_paper_pass': True,
        'five_revised_and_three_retained_exclamations_source_faithful_no_war_or_species_added': True,
        'all7_CPU_role_counterfactuals_change_only_one_original_roster_byte_each': True,
        'remaining_layout_findings': 0, 'registered_build_and_original_special_target_inspection_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    approved = deepcopy(doc)
    approved.update(formatting_review_pending=False, status='eight-source-native-approved;registered-release-original-inspection-pending',
        reviewed_research_manuscript=str(OLD), reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        visual_review=str(visual), visual_review_sha256=sha(visual.read_bytes()))
    for key, path in paths.items():
        approved[key], approved[key + '_sha256'] = path, sha(Path(path).read_bytes())
    for row in approved['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-approved;registered-release-original-inspection-pending'
    validate_natural_dialogue_batch(approved)
    save(NEW, approved)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1338, 1490, 152)
    save(ROOT / 'coverage_before_native_approval.json', before)
    drafts = ledger['active_source_prose_drafts']
    drafts['manuscripts'].append(str(NEW))
    drafts['manuscript_record_subsets_pending'][str(OLD)] = []
    drafts['manuscript_record_subsets_pending'][str(NEW)] = list(IDS)
    unit = next(u for u in ledger['coverage_units'] if u['id'] == 'Shared-sea-inspection-fear-awe8-source-prose')
    unit.update(status=approved['status'], native_approved_manuscript=str(NEW), native_visual_review=str(visual))
    ledger['formatting_watchlist']['sea_inspection_fear_awe8'].update(native_approved_manuscript=str(NEW),
        native_font_proof=paths['native_font_proof'], native_visual_review=str(visual), all8_panels_actually_viewed=True,
        native_font_visual_registered_release_and_original_inspection_pending=False,
        registered_release_and_original_inspection_pending=True)
    summary = ('V1561 native-approves8 creature/ghost inspection reactions2209-2216:5 revised3 retained. False war removed;source voice/intent and no-argument/no-macro contract preserved. '
        'All8 original logical-role7/printf/macro/post-expansion-wrap/full native and independent font planes,ordered complete letters,uniform6px margins,bounds,blank paper, '
        '207 original actor choices,7 one-byte CPU-only role counterfactuals and14 compiler negatives pass. Complete8-panel sheet is actually viewed;no layout findings. '
        '529455 native selector/ABI cases,7336 complete copies180 cache sequences13 earlier escapes pass. One exact role-table membership encodes186/188 bytes, '
        '172-byte gate and123040 staged bytes unchanged;3663 other/retained copies,40 blocks,all earlier helpers/routes/graphics/fonts preserved. '
        'Registered ROM/exact patch/startup/original special-target inspection remain pending. Activation pilots are disclosed research,not earned/natural spawns or event completion. '
        'Counts1338 complete(1000 revised338 retained),1490 source/prose,152 reviewed-incomplete COMMON. V1542 experimental,V1492 promoted;full goal and separate graphics/all18 plaques remain open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id': 'V1561-sea-inspection8-native-approved', 'manuscript': str(NEW),
        'proof': str(ROOT / 'native_approval_receipt.json'), 'source_prose_reviews_added': 0, 'completed_entries_added': 0, 'full_goal_complete': False})
    for k in ['records_editorially_completed', 'records_revised_and_integrated', 'records_with_source_and_prose_pass',
        'reviewed_but_incomplete_COMMON_IDs', 'current_native_relocation_reference', 'current_integrated_candidate',
        'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal']:
        assert ledger[k] == before[k], k
    save(ledger_path, ledger)
    Path('docs/sea_responses_v1561_native_checkpoint.md').write_text('# V1561 eight sea inspection reactions native-approved\n\n' + summary +
        '\n\nNo revised special-target dialogue has been seen in-game yet. The role-counterfactual probes are CPU-only and do not prove recruitment,encounter eligibility or original event activation.\n', encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs') / name).open('a', encoding='utf-8', newline='\n') as f:
            f.write('\n\n## V1561 sea inspection8 native approval\n\n' + summary + '\n\nSee [checkpoint](sea_responses_v1561_native_checkpoint.md).\n')
    save(ROOT / 'native_approval_receipt.json', {'manuscript': str(NEW), 'manuscript_sha256': sha(NEW.read_bytes()),
        'proofs': {p: sha(Path(p).read_bytes()) for p in [*paths.values(), str(visual)]},
        'completed': 1338, 'source_prose': 1490, 'reviewed_incomplete_COMMON': 152, 'completed_entries_added': 0,
        'registered_release_and_original_inspection_pending': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Sea inspection8 source/native approved;1338 complete/1490 reviewed;registered build and original special-target event pending.')
