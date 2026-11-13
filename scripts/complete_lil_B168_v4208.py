"""Stage B168 completion only after the registered release and fresh startup gates."""
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save
from scripts.lil_B168_completion_text_v4208 import NEXT, ACTUAL_SCOPE, make_summary

ROOT = Path('work/analysis/lil_B168_completion_v4208')
FINAL = Path('translations/lil_B168_contextual_final_review_v1.json')
DOC = Path('translations/lil_B168_editorial_manuscript_v8.json')
RELEASE = Path('work/analysis/lil_B168_release_v4205/registered_release_verification.json')
START = Path('work/analysis/lil_B168_startup_v4207/cold_boot_Lil_startup_town_verification.json')
VISUAL = START.parent / 'current_six_frame_visual_review.json'
ACTUAL = Path('work/analysis/lil_B168_actual_v4200/actual_progressive_FE_three_predicates_full_effect_and_return.json')
TRANSITIONS = Path('work/analysis/lil_B168_transition_review_v4201/all9_sheets_contact_FE_source_effect_and_paired_return_review.json')
PRIOR = Path('work/analysis/lil_B168_checkpoint_v4188/checkpoint_receipt.json')
REG = Path('work/analysis/lil_B168_registration_v4203/registration_receipt.json')
FAMILY = 'Lil-B168-Mikhail-recruitment-naturalist-item-information54'
OFFLINE = {'DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135'}

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    before = deepcopy(ledger)
    docs = [Path('docs') / name for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']]
    prior = read(PRIOR)
    for path in [lp, *docs]:
        assert sha(path.read_bytes()) == prior['updated_files'][str(path.resolve())], str(path)
    release, start, view, actual, reg = map(read, [RELEASE, START, VISUAL, ACTUAL, REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all544_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4160'] and start['paired_frame_count'] == 31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert not start['actual_selected_B168_IDs']
    assert view['viewed'] and view['sheet'] == start['review_sheet']
    assert view['sha256'] == start['review_sheet_sha256'] == sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 51
    assert actual['actual_new_cold_boot_runs'] == 2 and not actual['failures'] and not actual['paired_region_differences']
    assert reg['negative_count'] == 57 and reg['all_negatives_reject_before_mutation']
    doc = read(DOC)
    mapping, sample = read(doc['reference_map']), read(doc['representative_proof'])
    rows = deepcopy(doc['records'])
    assert len(rows) == 54 and Counter(row['editorial_decision'] for row in rows) == {'revise': 28, 'retain-wording': 26}
    assert all(all(row['review'].values()) and row['source_meaning'] and row['localization_note'] for row in rows)
    assert set(sample['offline_only_display_IDs']) == OFFLINE and sample['three_conditional_remarks_not_actual_or_byte_identical_reuse']
    image = NdsImage.open(release['candidate'])
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256'] == start['candidate_sha256']
    refs = {row['id']: row for block in mapping['blocks'] for row in block['text_records']}
    parity = {row['id']: row for row in read(doc['final_padding_proof'])['final_target_parity_cases']}
    stage = {row['id']: row for row in release['stage']['changed_records']}
    sampled = {row['id'] for row in actual['actual_panels']}
    assert len(sampled) == 51 and sampled | OFFLINE == set(refs) and not sampled & OFFLINE
    for row in rows:
        ident, spec = row['id'], refs[row['id']]
        at, block = spec['new_offset'], blocks[168]
        value = bytes.fromhex(spec['target_hex'])
        body = value[1:]
        cases = parity[ident]['current_final_target_macro_alignment_cases']['cases']
        effective = bytes.fromhex(cases[0]['output_hex'])
        assert stage[ident]['new_offset'] == at and block[at:at + len(value)] == value and block[at + len(value)] == 0
        assert effective == body.replace(b'FI', b'Lil').replace(b'FA', b'Argot').replace(b'FO', b'Argot Co.')
        assert len(cases) == 4 and all(bytes.fromhex(case['output_hex']) == effective for case in cases)
        assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex'] and value[0] == row['source_selector']
        fields = ['current_reference', 'current_hex', 'current_English', 'current_record_index', 'record_index',
            'current_raw_storage_English', 'current_effective_runtime_English', 'current_effective_macro_template_hex',
            'current_effective_macro_template_English', 'current_effective_paragraph', 'registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields'] = {key: deepcopy(row[key]) for key in fields if key in row}
        ref = dict(block=168, offset=at, bytes=len(value), record_index=block[:at].count(b'\0'), header_offset=at - 5)
        paragraph = row['english'].split('}', 1)[1]
        row.update(current_reference=ref, current_hex=value.hex(), current_text_hex=value.hex(), integrated_reference=ref,
            integrated_hex=value.hex(), current_record_index=ref['record_index'], record_index=ref['record_index'],
            completed_candidate_reference=release['candidate'], completed_candidate_sha256=release['candidate_sha256'],
            current_English=body.decode('ascii'), current_raw_storage_English=body.decode('ascii'),
            current_effective_runtime_English=effective.decode('ascii'), current_effective_macro_template_hex=body.hex(),
            current_effective_macro_template_English=body.decode('ascii'), current_effective_paragraph=paragraph,
            registered_runtime_catalog_entry=None, effective_predecessor_macro_paragraph=row['effective_predecessor_paragraph'],
            historical_editorial_decision=row['editorial_decision'], actual_B22_display_fixture_observed=ident in sampled,
            offline_only_complete_native_display_verified=ident in OFFLINE, actual_display_or_byte_identical_reuse_claim=ident in sampled,
            actual_source_event168_selected=False, individual_actual_source_event_activation_not_claimed=True,
            current_complete_native_display_pending=False, registered_integration_pending=False,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        if row['editorial_decision'] == 'retain-wording':
            assert paragraph == row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    old_keys = {historical_key(row) for family in ledger['completed_editorial_families'] for row in family['records']}
    selected = {historical_key(row) for row in rows}
    assert len(old_keys) == 5602 and len(selected) == 54 and not old_keys & selected
    assert selected == {historical_key(row) for row in fresh['pending_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5656, 5602, 54)
    assert ledger['records_with_source_and_prose_pass'] == 5659 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3803
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4188')
    ROOT.mkdir(parents=True)
    for path in [lp, *docs]:
        copy2(path, ROOT / (path.name + '.before'))
    summary = make_summary(release)
    proof_paths = [DOC, RELEASE, START, VISUAL, ACTUAL, TRANSITIONS, PRIOR, REG, Path(doc['reference_map']),
        Path(doc['representative_proof']), Path(doc['final_padding_proof']), Path(doc['source_nameplate_consumer_proof']),
        Path('scripts/lil_B168_completion_text_v4208.py'), Path(__file__)]
    next_clean = Path('work/analysis/lil_B169_clean_context_v4210/all36_complete_B169_exchange_and_fresh_glosses.json')
    next_source = read(next_clean)
    assert next_source['total_editorial_objects'] == 36 and next_source['no_predecessor_English_exposed']
    assert next_source['source_prose_or_completion_credit_added'] == 0
    proof_paths.append(next_clean)
    evidence = {str(path): sha(path.read_bytes()) for path in proof_paths}
    final = dict(format='dk4-contextual-final-review-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        manuscript=str(DOC), manuscripts={str(DOC): sha(DOC.read_bytes())}, candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        profile=release['profile'], records=rows, revised=28, retained=26, source_prose_credit_already_recorded_in_V4188=True,
        all54_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True, actual_sampled_B22_display_IDs=sorted(sampled),
        offline_only_display_IDs=sorted(OFFLINE), actual_verification_scope=ACTUAL_SCOPE, evidence=evidence, summary=summary, full_goal_complete=False)
    save(FINAL, final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY, file_path='/data/SC2.DK4', blocks=[168], record_IDs=[row['id'] for row in rows],
        final_review=str(FINAL), records=rows, revised_count=28, retained_count=26, fresh_revisions=28, fresh_retentions=26, actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5656, records_revised_and_integrated=3595, retained_wordings_editorially_completed=2061)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] = 3803
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = []
    active = ledger['active_source_prose_drafts']
    for path, ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][path] = [ident for ident in ids if ('/data/SC2.DK4', ident) not in selected]
    if str(DOC) not in active['manuscripts']:
        active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)] = []
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='5656 fresh contextual rereads integrated;source/prose5659. Remaining267 physical B169-B180 speech leads,zero choice-command leads and every wider editorial family remain open.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=5656, fresh_pass_records_pending_native_actual_release=0, pending_record_keys=[],
        pending_contextual_families=[], latest_pending_contextual_family=None, latest_contextual_manuscript=str(DOC), latest_completed_family=FAMILY,
        latest_final_review=str(FINAL), coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY, records=54, final_review=str(FINAL), new_revisions=28, justified_retentions=26,
        new_completed_records=54, historical_reconciliation_only=False, historical_decisions_newly_completed=dict(revised=28, retained=26),
        actual_selected_B168_source_events=[], actual_sampled_B22_display_IDs=sorted(sampled), offline_only_display_IDs=sorted(OFFLINE),
        new_current_candidate_emulator_runs=2, new_explicit_display_fixture_runs=2))
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4057, completed_route_records=4057, next=NEXT)
        if unit['id'] == FAMILY:
            unit.update(status='complete-contextual-current-native-references-representative-and-registered-release', pending=None,
                completion_credit_added=54, final_review=str(FINAL), new_emulator_runs=4, new_current_candidate_emulator_runs=2,
                new_explicit_source_English_fixture_runs=2, actual_sampled_B22_display_IDs=sorted(sampled), offline_only_display_IDs=sorted(OFFLINE), full_goal_complete=False)
    ledger['formatting_watchlist']['lil_B168_v4188'].update(status='complete-through-V4208', registered_release_pending=False, final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_B168_v4208'] = dict(status='all54-source-native-reference-representative-release-checks-pass', final_review=str(FINAL),
        evidence=evidence, no_glyph_bounds_pagination_or_control_waivers=True, actual_selected_B168_source_events=[],
        actual_sampled_B22_display_IDs=sorted(sampled), offline_only_display_IDs=sorted(OFFLINE))
    candidate = dict(path=release['candidate'], sha256=release['candidate_sha256'], profile=release['profile'], MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'], patch=release['patch'], patch_sha256=release['patch_sha256'], manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted', details=summary, full_goal_complete=False)
    candidate.update({f'SC{index}_sha256': release['story_hashes'][f'SC{index}'] for index in range(4)})
    ledger['current_integrated_candidate'] = candidate
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v4188']['path']))
    inventory.update(incomplete_route_source_prose_groups=[], incomplete_route_source_prose_count=0, next_focus=NEXT)
    inventory['lil_B168_completed_v4208'] = dict(completed_targets=54, final_review=str(FINAL), registered_candidate=release['candidate'],
        explicit_display_fixture_count=2, actual_unique_speeches=51, actual_FE_panels=3, offline_only_display_IDs=sorted(OFFLINE),
        natural_source_event_not_selected=True, no_B168_command_omitted_in_content_fixtures=True)
    next_lead = dict(path=str(next_clean), sha256=sha(next_clean.read_bytes()), physical_speeches=36,
        source_glosses_before_predecessor_English=True, current_English_unexposed=True,
        current_names_controls_terms_native_and_release_pending=True, source_prose_or_completion_credit_added=0)
    inventory['next_B169_clean_context_only_uncredited_v4210'] = next_lead
    ledger['lil_B169_clean_context_only_uncredited_v4210'] = next_lead
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4057, completed_route_records=4057, source_prose_pending_records=0, source_prose_pending_family=None, next=NEXT)
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v4208'] = dict(path=str(inv), sha256=sha(inv.read_bytes()), incomplete_COMMON=3, incomplete_route_source_prose=0,
        remaining_B169_B180_physical_speeches=267, remaining_choice_command_leads=0, later_storylines_shared_town_shop_random_help_prose_open=True,
        Proof_terminology_consistency_open=True, canonical_Maria32_pending_uncredited=True, full_goal_complete=False)
    ledger['lil_B168_completion_v4208'] = dict(summary=summary, final_review=str(FINAL), evidence=evidence, goal_turn_classification='progress', full_goal_complete=False)
    ledger['latest_checkpoint'] = summary
    keys = {historical_key(row) for family in ledger['completed_editorial_families'] for row in family['records']}
    assert keys == old_keys | selected == {historical_key(row) for row in fresh['integrated_record_keys']} == {historical_key(row) for row in fresh['record_keys']}
    assert len(keys) == 5656 and ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 5659
    preserved = ['reviewed_but_incomplete_COMMON_IDs', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal',
        'native_source_universe_inventory_v2701c', 'Proof_terminology_consistency_lead_v3286', 'lil_B157_provenance_amendment_v3784', 'promoted_main_build_v4186']
    for key in preserved:
        assert ledger[key] == before[key], key
    assert ledger['completed_editorial_families'][:-1] == before['completed_editorial_families']
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    planned = ROOT / (lp.name + '.planned')
    planned.write_bytes((json.dumps(ledger, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    staged = [dict(target=str(lp.resolve()), before_sha256=sha(lp.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(planned.read_bytes()))]
    section = '## V4208: 54 Lil B168 reviews completed in V4204\n\n' + summary
    section += '\n\nFinal review: ' + FINAL.as_posix() + '. Release: ' + RELEASE.as_posix() + '. Startup: ' + START.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '.\n\nNext: ' + NEXT + '\n\n'
    for index, path in enumerate(docs):
        first, rest = path.read_text(encoding='utf-8').split('\n', 1)
        data = (('# Current editorial handoff - V4208' if index == 0 else first) + '\n\n' + section + rest).encode('utf-8')
        planned = ROOT / (path.name + '.planned')
        planned.write_bytes(data)
        staged.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(data)))
    receipt = dict(checkpoint='V4208', final_review=str(FINAL), final_review_sha256=sha(FINAL.read_bytes()), evidence=evidence,
        updated_files={entry['target']: entry['planned_sha256'] for entry in staged}, prior_checkpoint=str(PRIOR),
        new_source_prose_reviews=0, new_completed_records=54, revised=28, retained=26, fresh_reread=5656, fresh_integrated=5656,
        fresh_pending=0, source_prose=5659, completed=5656, historical_revised=3595, historical_retained=2061,
        candidate=release['candidate'], candidate_sha256=release['candidate_sha256'], patch=release['patch'], patch_sha256=release['patch_sha256'],
        manifest_batches=544, accepted_layers=114, new_actual_emulator_runs=4, new_actual_fixture_runs=2, new_registered_startup_runs=2,
        actual_unique_speech_panels=51, actual_FE_panels=3, offline_only_display_IDs=sorted(OFFLINE),
        remaining_B169_B180_physical_speeches=267, remaining_choice_command_leads=0, all_jobs_terminal=True, full_goal_complete=False)
    receipt_path = ROOT / 'staged_completion_receipt.json'
    save(receipt_path, receipt)
    save(ROOT / 'staged_completion.json', dict(files=staged, staged_receipt=str(receipt_path), staged_receipt_sha256=sha(receipt_path.read_bytes()),
        no_current_ledger_or_document_mutation_yet=True))
    print('V4208 completion staged after registered gates; native application and final audit pending. Full goal active.')
