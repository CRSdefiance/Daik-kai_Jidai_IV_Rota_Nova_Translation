"""Independently audit B166 completion, exact integrated references and remaining full scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/editorial_handoff_verification_v4115')
CHECKPOINT = Path('work/analysis/lil_B166_completion_v4114')

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt_path = CHECKPOINT/'completion_receipt.json'
    receipt = read(receipt_path)
    lp = Path('translations/editorial_review_current_v1.json')
    ledger,before = read(lp),read(CHECKPOINT/(lp.name+'.before'))
    for path,digest in {**receipt['updated_files'],**receipt['evidence']}.items():
        assert sha(Path(path).read_bytes()) == digest,path
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    allrows = [r for g in ledger['completed_editorial_families'] for r in g['records']]
    keys = {historical_key(r) for r in allrows}
    assert len(allrows) == len(keys) == len(fresh['record_keys']) == len(fresh['integrated_record_keys']) == 5573
    assert keys == {historical_key(r) for r in fresh['record_keys']} == {historical_key(r) for r in fresh['integrated_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5573,5573,0)
    assert fresh['pending_record_keys'] == fresh['pending_contextual_families'] == []
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],
            ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
            ledger['retained_wordings_editorially_completed']) == (5576,5576,5573,3551,2022)
    def decision(row):
        value = row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert isinstance(value,str) and value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in allrows) == {'revise':3551,'retain':2022}
    assert dict(Counter(historical_key(r)[0] for r in allrows)) == ledger['completed_editorial_record_counts_by_file']
    assert ledger['completed_editorial_families'][:-1] == before['completed_editorial_families']
    assert ledger['source_prose_reviewed_counts_by_file'] == before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 5576
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3720
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4'] == 64
    family = ledger['completed_editorial_families'][-1]
    final = read(family['final_review'])
    assert family['id'] == 'Lil-B166-Manuel-ship-care-recruitment-optional-Workroom-advice44'
    assert family['records'] == final['records'] and len(final['records']) == 44
    assert Counter(r['editorial_decision'] for r in final['records']) == {'revise':24,'retain-wording':20}
    release = read('work/analysis/lil_B166_release_v4111/registered_release_verification.json')
    candidate = ledger['current_integrated_candidate']
    rom,old,clean = [NdsImage.open(p) for p in [candidate['path'],'out/all_routes_combined_v4046_candidate.nds','work/clean.nds']]
    blocks,oldblocks,jp = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [rom,old,clean]]
    assert sha(Path(candidate['path']).read_bytes()) == candidate['sha256'] == release['candidate_sha256'] == final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes()) == candidate['patch_sha256'] == release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes() == Path(candidate['path']).read_bytes()
    assert sha(Path('work/clean.nds').read_bytes()) == release['clean_input_sha256']
    assert [n for n,(a,b) in enumerate(zip(oldblocks,blocks,strict=True)) if a!=b] == [166]
    assert (len(oldblocks[166]),len(blocks[166])) == (2952,2972)
    assert [p for _,p,value in old.iter_files() if rom.read_file(p)!=value] == ['/data/SC2.DK4']
    assert all(rom.read_file(p)==value for p,value in old.iter_components())
    manifest,registry = read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile'] == candidate['profile'] == 'all-routes-unified-v4110'
    assert len(manifest['batches']) == 541 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers']) == 114 and registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4046'
    conf = read('translations/lil_B166_editorial_release_v1.json')
    for path,digest in conf['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest,path
    doc = read(final['manuscript'])
    mapping,stored = read(doc['reference_map']),read(doc['final_padding_proof'])
    expanded = {r['id']:r['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'] for r in stored['final_target_parity_cases']}
    refs = {r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    choices = {r['id']:r for b in mapping['blocks'] for c in b['choice_commands'] for r in c['label_references']}
    for row in final['records']:
        choice = row['kind']=='typed-choice-label'
        assert row['block'] == 166 and all(row['review'].values())
        assert row['fresh_source_gloss'] == row['source_meaning'] and row['full_clean_context_precedes_comparison']
        at,raw = row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert jp[166][at:at+len(raw)] == raw and jp[166][at+len(raw)] == 0
        ref,value = row['integrated_reference'],bytes.fromhex(row['integrated_hex'])
        at = ref['offset']
        assert blocks[166][at:at+len(value)] == value and blocks[166][at+len(value)] == 0
        assert row['current_hex'] == row['integrated_hex'] and row['current_reference'] == ref
        assert row['record_index'] == blocks[166][:at].count(b'\0')
        predecessor = row['historical_source_prose_predecessor_fields']
        pa,pv = predecessor['current_reference']['offset'],bytes.fromhex(predecessor['current_hex'])
        assert oldblocks[166][pa:pa+len(pv)] == pv and oldblocks[166][pa+len(pv)] == 0
        paragraph = row['english'] if choice else row['english'].split('}',1)[1]
        if choice:
            assert row['option_index'] in [0,1] and paragraph == ['Please do','Decline'][row['option_index']]
            assert value.decode('ascii') == paragraph and choices[row['id']]['new_offset'] == at
            assert row['actual_advice_choice_result_observed'] and not row['actual_choice_selection_still_pending']
            assert not row['current_native_typed_choice_font_reference_and_outcome_binding_pending']
        else:
            sa = row['source_reference']['offset']
            assert jp[166][sa-5:sa+1].hex() == row['source_complete_preamble_hex'] == blocks[166][at-5:at+1].hex()
            assert refs[row['id']]['new_offset'] == at and value[0] == row['source_selector'] in [2,9,20,23]
            assert bytes.fromhex(expanded[row['id']]).decode('ascii') == row['current_effective_runtime_English']
            for macro in ['FI','FA','FO']:
                assert raw.count(macro.encode()) == row['english'].count('{MACRO:'+macro+'}')
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification']
            assert paragraph == row['effective_predecessor_macro_paragraph'] == row['effective_predecessor_paragraph']
        assert row['actual_B22_display_fixture_observed'] == (row['id']!='DK4_MES_B166_R0087')
        assert row['offline_only_complete_native_display_verified'] == (row['id']=='DK4_MES_B166_R0087')
        assert not row['actual_source_event166_selected'] and row['individual_actual_source_event_activation_not_claimed']
    assert Counter(r['kind'] for r in final['records']) == {'progressive':42,'typed-choice-label':2}
    assert stored['current_final_stored_macro_alignment_cases'] == 168
    controls = read(doc['relocated_control_proof'])
    assert len(controls['relocated_dispatch_cases']) == 42 and len(controls['relocated_predicate_pairs']) == 1
    assert len(controls['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 11
    assert len(controls['relocated_choice_getter_phases']) == 2
    block = mapping['blocks'][0]
    assert len(block['command_map']) == 62 and len(block['relative_skip_fixups']) == 8 and len(block['target_native_skip_cases']) == 40
    assert [e['source_offset'] for e in block['original_declared_end_word_maps']] == [2948]
    actual = read('work/analysis/lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return.json')
    assert not actual['failures'] and actual['fresh_actual_unique_speech_panels'] == 41 and actual['complete_matching_observations'] == 73
    assert [r['native_result_words'] for r in actual['actual_menu_cases']] == [[2,0],[2,1]] and actual['actual_new_cold_boot_runs'] == 4
    assert actual['offline_only_display_IDs'] == ['DK4_MES_B166_R0087']
    transition = read('work/analysis/lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review.json')
    assert len(transition['all7_actual_sheets_viewed']) == 7 and len(transition['English_full_screen_views']) == 11
    assert len(transition['Japanese_full_screen_views']) == 3 and len(transition['paired_source_English_whole_RGB_returns']) == 2
    for sheet in transition['all7_actual_sheets_viewed']+transition['English_full_screen_views']+transition['Japanese_full_screen_views']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    startup = read('work/analysis/lil_B166_startup_v4113/cold_boot_Lil_startup_town_verification.json')
    view = read('work/analysis/lil_B166_startup_v4113/current_six_frame_visual_review.json')
    assert startup['candidate_sha256'] == candidate['sha256'] and startup['paired_frame_count'] == 31
    assert startup['all_current_requested_and_final_framebuffers_equal_V4046']
    assert startup['all_five_postload_actor_model_and_captain_checks_equal'] and startup['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256'] == sha(Path(view['sheet']).read_bytes())
    reg = read('work/analysis/lil_B166_registration_v4109/registration_receipt.json')
    negatives = read(reg['negative_cases'])
    assert reg['negative_count'] == len(negatives['cases']) == 72 and all(r['rejected'] for r in negatives['cases'])
    units = {u['id']:u for u in ledger['coverage_units']}
    assert units['all-route-scenes']['reviewed_route_records'] == units['all-route-scenes']['completed_route_records'] == 3974
    assert units[family['id']]['new_emulator_runs'] == 6
    assert all(not ids for ids in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] == []
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286',
                'lil_B157_provenance_amendment_v3784','promoted_main_build_v4083']:
        assert ledger[key] == before[key],key
    scope = ledger['unfinished_editorial_scope_v4114']
    assert sha(Path(scope['path']).read_bytes()) == scope['sha256'] and scope['incomplete_COMMON'] == 3 and scope['incomplete_route_source_prose'] == 0
    assert scope['remaining_B167_B180_physical_speeches'] == 348 and scope['remaining_choice_command_leads'] == 1
    assert scope['canonical_Maria32_pending_uncredited'] and scope['later_storylines_shared_town_shop_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4114')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4114',ledger_sha256=sha(lp.read_bytes()),
        handoff_receipt=str(receipt_path),handoff_receipt_sha256=sha(receipt_path.read_bytes()),fresh_reread=5573,integrated=5573,pending=0,
        source_prose=5576,revised=3551,retained=2022,candidate=candidate['path'],candidate_sha256=candidate['sha256'],
        patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=541,accepted_layers=114,
        all44_clean_predecessor_integrated_references_and_retentions_verified=True,
        all62_commands8_spans40_skips168_stored_cases_predicate_resources_single_end_and_names_bound=True,
        actual_four_B22_fixtures41_unique73_observations_both_choices_and_returns_verified=True,
        conditional_Fernando_remark_explicitly_offline_only=True,actual_registered_startup31_whole_frames_and_five_models_verified=True,
        V4046_promoted_main_unchanged=True,all_prior_completions_and_wider_scope_preserved=True,
        remaining_B167_B180_physical_speeches=348,remaining_choice_command_leads=1,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4114 independently verified:5573/5573/0;5576 source/prose;541/114 stack;exact patch,scoped actual/native/startup pass. Full goal active.')
