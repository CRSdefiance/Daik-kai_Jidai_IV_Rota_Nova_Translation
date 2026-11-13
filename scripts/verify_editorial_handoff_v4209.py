"""Independently audit all54 completions, exact integrated references and the full remaining scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4209')
CHECKPOINT = Path('work/analysis/lil_B168_completion_v4208')
OFFLINE = {'DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135'}

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt_path = CHECKPOINT / 'completion_receipt.json'
    receipt = read(receipt_path)
    lp = Path('translations/editorial_review_current_v1.json')
    ledger, before = read(lp), read(CHECKPOINT / (lp.name + '.before'))
    for path, digest in {**receipt['updated_files'], **receipt['evidence']}.items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    all_rows = [row for family in ledger['completed_editorial_families'] for row in family['records']]
    keys = {historical_key(row) for row in all_rows}
    assert len(all_rows) == len(keys) == len(fresh['record_keys']) == len(fresh['integrated_record_keys']) == 5656
    assert keys == {historical_key(row) for row in fresh['record_keys']} == {historical_key(row) for row in fresh['integrated_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5656, 5656, 0)
    assert fresh['pending_record_keys'] == fresh['pending_contextual_families'] == []
    assert (ledger['records_with_source_and_prose_pass'], ledger['records_with_source_prose_drafts'], ledger['records_editorially_completed'],
            ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5659, 5659, 5656, 3595, 2061)
    def decision(row):
        value = row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert isinstance(value, str) and value.startswith(('revis', 'retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(row) for row in all_rows) == {'revise': 3595, 'retain': 2061}
    assert dict(Counter(historical_key(row)[0] for row in all_rows)) == ledger['completed_editorial_record_counts_by_file']
    assert ledger['completed_editorial_families'][:-1] == before['completed_editorial_families']
    assert ledger['source_prose_reviewed_counts_by_file'] == before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 5659
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3803
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4'] == 64
    family = ledger['completed_editorial_families'][-1]
    final = read(family['final_review'])
    assert family['id'] == 'Lil-B168-Mikhail-recruitment-naturalist-item-information54'
    assert family['records'] == final['records'] and len(final['records']) == 54
    assert Counter(row['editorial_decision'] for row in final['records']) == {'revise': 28, 'retain-wording': 26}
    release = read('work/analysis/lil_B168_release_v4205/registered_release_verification.json')
    candidate = ledger['current_integrated_candidate']
    rom, old, clean = [NdsImage.open(path) for path in [candidate['path'], 'out/all_routes_combined_v4160_candidate.nds', 'work/clean.nds']]
    blocks, old_blocks, jp = [IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks for image in [rom, old, clean]]
    assert sha(Path(candidate['path']).read_bytes()) == candidate['sha256'] == release['candidate_sha256'] == final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes()) == candidate['patch_sha256'] == release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes() == Path(candidate['path']).read_bytes()
    assert sha(Path('work/clean.nds').read_bytes()) == release['clean_input_sha256']
    assert [index for index, (a, b) in enumerate(zip(old_blocks, blocks, strict=True)) if a != b] == [168]
    assert (len(old_blocks[168]), len(blocks[168])) == (2916, 2872)
    assert [path for _, path, value in old.iter_files() if rom.read_file(path) != value] == ['/data/SC2.DK4']
    assert all(rom.read_file(path) == value for path, value in old.iter_components())
    manifest, registry = read(candidate['manifest']), read('translations/release_stack.json')
    assert manifest['profile'] == candidate['profile'] == 'all-routes-unified-v4204'
    assert len(manifest['batches']) == 544 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers']) == 114 and registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4160'
    conf = read('translations/lil_B168_editorial_release_v1.json')
    for path, digest in conf['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    doc = read(final['manuscript'])
    mapping, stored = read(doc['reference_map']), read(doc['final_padding_proof'])
    expanded = {row['id']: row['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'] for row in stored['final_target_parity_cases']}
    refs = {row['id']: row for block in mapping['blocks'] for row in block['text_records']}
    macro_counts = Counter()
    for row in final['records']:
        assert row['block'] == 168 and all(row['review'].values())
        assert row['fresh_source_gloss'] == row['source_meaning'] and row['full_clean_context_precedes_comparison']
        source_at, raw = row['source_reference']['offset'], bytes.fromhex(row['source_hex'])
        assert jp[168][source_at:source_at + len(raw)] == raw and jp[168][source_at + len(raw)] == 0
        ref, value = row['integrated_reference'], bytes.fromhex(row['integrated_hex'])
        at = ref['offset']
        assert blocks[168][at:at + len(value)] == value and blocks[168][at + len(value)] == 0
        assert row['current_hex'] == row['integrated_hex'] and row['current_reference'] == ref
        assert row['record_index'] == blocks[168][:at].count(b'\0')
        predecessor = row['historical_source_prose_predecessor_fields']
        pa, pv = predecessor['current_reference']['offset'], bytes.fromhex(predecessor['current_hex'])
        assert old_blocks[168][pa:pa + len(pv)] == pv and old_blocks[168][pa + len(pv)] == 0
        assert jp[168][source_at - 5:source_at + 1].hex() == row['source_complete_preamble_hex'] == blocks[168][at - 5:at + 1].hex()
        assert refs[row['id']]['new_offset'] == at and value[0] == row['source_selector'] in [2, 6, 9, 20, 76, 87, 165, 166, 254]
        assert (row['source_selector'] == 254) == (row['kind'] == 'system-FE')
        assert bytes.fromhex(expanded[row['id']]).decode('ascii') == row['current_effective_runtime_English']
        for macro in ['FI', 'FA', 'FO']:
            assert raw.count(macro.encode()) == row['english'].count('{MACRO:' + macro + '}')
            macro_counts[macro] += raw.count(macro.encode())
        if row['editorial_decision'] == 'retain-wording':
            assert row['fresh_retained_wording_justification']
            assert row['english'].split('}', 1)[1] == row['effective_predecessor_macro_paragraph'] == row['effective_predecessor_paragraph']
        assert row['actual_B22_display_fixture_observed'] == (row['id'] not in OFFLINE)
        assert row['offline_only_complete_native_display_verified'] == (row['id'] in OFFLINE)
        assert not row['actual_source_event168_selected'] and row['individual_actual_source_event_activation_not_claimed']
    assert macro_counts == {'FI': 7, 'FA': 1, 'FO': 1}
    assert Counter(row['kind'] for row in final['records']) == {'progressive': 51, 'system-FE': 3}
    assert stored['current_final_stored_macro_alignment_cases'] == 216
    controls = read(doc['relocated_control_proof'])
    assert len(controls['relocated_dispatch_cases']) == 54 and len(controls['relocated_predicate_pairs']) == 3
    assert len(controls['all16_source_current_target_nonrelative_nonspeech_leaves']) == 16
    block = mapping['blocks'][0]
    assert len(block['command_map']) == 82 and len(block['relative_skip_fixups']) == 12 and len(block['target_native_skip_cases']) == 60
    assert [end['source_offset'] for end in block['original_declared_end_word_maps']] == [2906, 2910]
    actual = read('work/analysis/lil_B168_actual_v4200/actual_progressive_FE_three_predicates_full_effect_and_return.json')
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 51
    assert actual['actual_new_cold_boot_runs'] == 2 and set(actual['offline_only_display_IDs']) == OFFLINE
    assert all(version['actual_source_recruitment_effect']['result_words'] == [3, 0] for version in actual['versions'])
    transition = read('work/analysis/lil_B168_transition_review_v4201/all9_sheets_contact_FE_source_effect_and_paired_return_review.json')
    assert len(transition['all9_actual_sheets_viewed']) == 9 and len(transition['English_full_screen_views']) == 5
    assert len(transition['Japanese_full_screen_views']) == 3 and len(transition['paired_source_English_whole_RGB_returns']) == 1
    for view in transition['all9_actual_sheets_viewed'] + transition['English_full_screen_views'] + transition['Japanese_full_screen_views']:
        assert sha(Path(view['path']).read_bytes()) == view['sha256']
    startup = read('work/analysis/lil_B168_startup_v4207/cold_boot_Lil_startup_town_verification.json')
    view = read('work/analysis/lil_B168_startup_v4207/current_six_frame_visual_review.json')
    assert startup['candidate_sha256'] == candidate['sha256'] and startup['paired_frame_count'] == 31
    assert startup['all_current_requested_and_final_framebuffers_equal_V4160']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal'] and startup['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256'] == sha(Path(view['sheet']).read_bytes())
    reg = read('work/analysis/lil_B168_registration_v4203/registration_receipt.json')
    negatives = read(reg['negative_cases'])
    assert reg['negative_count'] == len(negatives['cases']) == 57 and all(row['rejected'] for row in negatives['cases'])
    units = {unit['id']: unit for unit in ledger['coverage_units']}
    assert units['all-route-scenes']['reviewed_route_records'] == units['all-route-scenes']['completed_route_records'] == 4057
    assert units[family['id']]['new_emulator_runs'] == 4
    assert all(not ids for ids in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] == []
    for key in ['reviewed_but_incomplete_COMMON_IDs', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c', 'Proof_terminology_consistency_lead_v3286',
                'lil_B157_provenance_amendment_v3784', 'promoted_main_build_v4186']:
        assert ledger[key] == before[key], key
    scope = ledger['unfinished_editorial_scope_v4208']
    assert sha(Path(scope['path']).read_bytes()) == scope['sha256'] and scope['incomplete_COMMON'] == 3 and scope['incomplete_route_source_prose'] == 0
    assert scope['remaining_B169_B180_physical_speeches'] == 267 and scope['remaining_choice_command_leads'] == 0
    assert scope['canonical_Maria32_pending_uncredited'] and scope['later_storylines_shared_town_shop_random_help_prose_open']
    next_lead = ledger['lil_B169_clean_context_only_uncredited_v4210']
    assert sha(Path(next_lead['path']).read_bytes()) == next_lead['sha256'] and next_lead['source_prose_or_completion_credit_added'] == 0
    assert next_lead['physical_speeches'] == 36 and next_lead['current_English_unexposed']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4208')
    ROOT.mkdir(parents=True)
    save(ROOT / 'verified_handoff.json', dict(checkpoint='V4208', ledger_sha256=sha(lp.read_bytes()), handoff_receipt=str(receipt_path),
        handoff_receipt_sha256=sha(receipt_path.read_bytes()), fresh_reread=5656, integrated=5656, pending=0, source_prose=5659,
        revised=3595, retained=2061, candidate=candidate['path'], candidate_sha256=candidate['sha256'], patch=candidate['patch'],
        patch_sha256=candidate['patch_sha256'], manifest_batches=544, accepted_layers=114,
        all54_clean_predecessor_integrated_references_and_retentions_verified=True,
        all82_commands12_spans60_skips216_stored_cases_three_predicates_FE_macros_and_names_bound=True,
        actual_two_B22_fixtures51_complete_planes_full_effect_and_normal_return_verified=True,
        three_conditional_remarks_explicitly_offline_only=True, actual_registered_startup31_whole_frames_and_five_models_verified=True,
        V4160_promoted_main_unchanged=True, all_prior_completions_and_wider_scope_preserved=True,
        remaining_B169_B180_physical_speeches=267, remaining_choice_command_leads=0, next_B169_36_clean_glosses_uncredited=True,
        full_goal_active=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('V4208 independently verified:5656/5656/0;5659 source/prose;544/114 stack;exact patch,scoped actual/native/startup pass. Full goal active.')
