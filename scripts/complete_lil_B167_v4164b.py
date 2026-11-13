"""Complete previously credited B167 reviews only after registered release/startup gates."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B167_completion_text_v4164 import NEXT,ACTUAL_SCOPE,make_summary

ROOT = Path('work/analysis/lil_B167_completion_v4164')
FINAL = Path('translations/lil_B167_contextual_final_review_v1.json')
DOCS = [Path('translations/lil_B167_editorial_manuscript_v13.json'),Path('translations/lil_B167_choice_manuscript_v3.json')]
RELEASE = Path('work/analysis/lil_B167_release_v4161/registered_release_verification.json')
START = Path('work/analysis/lil_B167_startup_v4163/cold_boot_Lil_startup_town_verification.json')
VISUAL = START.parent/'current_six_frame_visual_review.json'
ACTUAL = Path('work/analysis/lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns.json')
TRANSITIONS = Path('work/analysis/lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review.json')
PRIOR = Path('work/analysis/lil_B167_checkpoint_v4155/checkpoint_receipt.json')
REG = Path('work/analysis/lil_B167_registration_v4159b/registration_receipt.json')
FAMILY = 'Lil-B167-Shipwright-complete-sail-lesson-accept-refuse29'
OFFLINE = {'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    before = deepcopy(ledger)
    docsfiles = [Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md',
        'editorial_review_goal.md','todo.md','known_issues.md']]
    prior = read(PRIOR)
    for path in [lp,*docsfiles]:
        assert sha(path.read_bytes()) == prior['updated_files'][str(path)]
    release,start,view,actual,reg = map(read,[RELEASE,START,VISUAL,ACTUAL,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all543_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4110'] and start['paired_frame_count'] == 31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert not start['actual_selected_B167_IDs']
    assert view['viewed'] and view['sheet'] == start['review_sheet']
    assert view['sha256'] == start['review_sheet_sha256'] == sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels'] == 25 and actual['complete_matching_observations'] == 28
    assert actual['actual_new_cold_boot_runs'] == 4 and not actual['failures']
    assert reg['negative_count'] == 78 and reg['all_negatives_reject_before_mutation']
    docs = [read(path) for path in DOCS]
    doc = docs[0]
    mapping,sample = read(doc['reference_map']),read(doc['representative_proof'])
    rows = deepcopy([row for document in docs for row in document['records']])
    assert len(rows) == 29 and Counter(r['editorial_decision'] for r in rows) == {'revise':16,'retain-wording':13}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert set(sample['offline_only_display_IDs']) == OFFLINE and sample['both_Cesare_remarks_not_actual_or_byte_identical_reuse']
    image = NdsImage.open(release['candidate'])
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256'] == start['candidate_sha256']
    refs = {r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    choices = {r['id']:r for b in mapping['blocks'] for c in b['choice_commands'] for r in c['label_references']}
    parity = {r['id']:r for r in read(doc['final_padding_proof'])['final_target_parity_cases']}
    stage = {r['id']:r for r in release['stage']['changed_records']}
    sampled = {r['id'] for r in actual['actual_panels']}
    assert len(sampled) == 25 and sampled|OFFLINE == set(refs) and not sampled&OFFLINE and len(choices) == 2
    for row in rows:
        ident = row['id']
        choice = row['kind'] == 'typed-choice-label'
        spec = (choices if choice else refs)[ident]
        at,block = spec['new_offset'],blocks[167]
        value = row['english'].encode('ascii') if choice else bytes.fromhex(spec['target_hex'])
        body = value if choice else value[1:]
        effective = body if choice else bytes.fromhex(parity[ident]['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'])
        assert stage[ident]['new_offset'] == at and block[at:at+len(value)] == value and block[at+len(value)] == 0
        assert effective == body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if not choice:
            cases = parity[ident]['current_final_target_macro_alignment_cases']['cases']
            assert len(cases) == 4 and all(bytes.fromhex(c['output_hex']) == effective for c in cases)
            assert block[at-5:at+1].hex() == row['source_complete_preamble_hex'] and value[0] == row['source_selector']
        fields = ['current_reference','current_hex','current_English','current_record_index','record_index',
            'current_raw_storage_English','current_effective_runtime_English','current_effective_macro_template_hex',
            'current_effective_macro_template_English','current_effective_paragraph','registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields'] = {k:deepcopy(row[k]) for k in fields if k in row}
        ref = dict(block=167,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'))
        if choice:
            ref.update(command_offset=mapping['blocks'][0]['choice_commands'][0]['new_offset'],option_index=row['option_index'])
        else:
            ref['header_offset'] = at-5
        paragraph = row['english'] if choice else row['english'].split('}',1)[1]
        row.update(current_reference=ref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=ref,
            integrated_hex=value.hex(),current_record_index=ref['record_index'],record_index=ref['record_index'],
            completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],
            current_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),
            current_effective_runtime_English=effective.decode('ascii'),current_effective_macro_template_hex=body.hex(),
            current_effective_macro_template_English=body.decode('ascii'),current_effective_paragraph=paragraph,
            registered_runtime_catalog_entry=None,effective_predecessor_macro_paragraph=row['effective_predecessor_paragraph'],
            historical_editorial_decision=row['editorial_decision'],actual_B22_display_fixture_observed=ident in sampled or choice,
            offline_only_complete_native_display_verified=ident in OFFLINE,actual_display_or_byte_identical_reuse_claim=ident in sampled or choice,
            actual_source_event167_selected=False,individual_actual_source_event_activation_not_claimed=True,
            current_complete_native_display_pending=False,registered_integration_pending=False,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        if choice:
            row.update(actual_menu_choice_result_observed=True,actual_choice_selection_still_pending=False,
                current_native_typed_choice_font_reference_and_outcome_binding_pending=False)
        if row['editorial_decision'] == 'retain-wording':
            assert paragraph == row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    oldkeys = {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    selected = {historical_key(r) for r in rows}
    assert len(oldkeys) == 5573 and len(selected) == 29 and not oldkeys&selected
    assert selected == {historical_key(r) for r in fresh['pending_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5602,5573,29)
    assert ledger['records_with_source_and_prose_pass'] == 5605 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3749
    assert docsfiles[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4155')
    ROOT.mkdir(parents=True)
    for path in [lp,*docsfiles]:
        copy2(path,ROOT/(path.name+'.before'))
    summary = make_summary(release)
    proofpaths = [*DOCS,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,Path(doc['reference_map']),
        Path(doc['representative_proof']),Path(doc['final_padding_proof']),Path(doc['source_nameplate_consumer_proof']),
        Path('scripts/lil_B167_completion_text_v4164.py'),Path(__file__)]
    evidence = {str(p):sha(p.read_bytes()) for p in proofpaths}
    final = dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(DOCS[0]),choices=str(DOCS[1]),manuscripts={str(p):sha(p.read_bytes()) for p in DOCS},
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
        revised=16,retained=13,source_prose_credit_already_recorded_in_V4136=True,
        all29_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,
        actual_sampled_B22_display_IDs=sorted(sampled),actual_sampled_choice_IDs=sorted(choices),offline_only_display_IDs=sorted(OFFLINE),
        actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=summary,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[167],
        record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=16,retained_count=13,
        fresh_revisions=16,fresh_retentions=13,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5602,records_revised_and_integrated=3567,retained_wordings_editorially_completed=2035)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] = 3749
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = []
    active = ledger['active_source_prose_drafts']
    for path,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][path] = [i for i in ids if ('/data/SC2.DK4',i) not in selected]
    for path in DOCS:
        if str(path) not in active['manuscripts']:
            active['manuscripts'].append(str(path))
        active['route_record_subsets_pending'][str(path)] = []
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='5602 fresh contextual rereads integrated;source/prose5605. Remaining321 physical B168-B180 speech leads,zero choice-command leads and every wider editorial family remain open.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=5602,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],
        pending_contextual_families=[],latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOCS[0]),
        latest_contextual_choice_draft=str(DOCS[1]),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=29,final_review=str(FINAL),new_revisions=16,justified_retentions=13,
        new_completed_records=29,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=16,retained=13),
        actual_selected_B167_source_events=[],actual_sampled_B22_display_IDs=sorted(sampled),actual_sampled_choice_IDs=sorted(choices),
        offline_only_display_IDs=sorted(OFFLINE),new_current_candidate_emulator_runs=2,new_explicit_display_fixture_runs=4))
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4003,completed_route_records=4003,next=NEXT)
        if unit['id'] == FAMILY:
            unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,
                completion_credit_added=29,final_review=str(FINAL),new_emulator_runs=6,new_current_candidate_emulator_runs=2,
                new_explicit_source_English_fixture_runs=4,actual_sampled_B22_display_IDs=sorted(sampled),
                actual_sampled_choice_IDs=sorted(choices),offline_only_display_IDs=sorted(OFFLINE),full_goal_complete=False)
    ledger['formatting_watchlist']['lil_B167_v4136'].update(status='complete-through-V4164',registered_release_pending=False,final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_B167_v4164'] = dict(status='all29-source-native-reference-representative-release-checks-pass',
        final_review=str(FINAL),evidence=evidence,no_glyph_bounds_pagination_or_control_waivers=True,
        actual_selected_B167_source_events=[],actual_sampled_B22_display_IDs=sorted(sampled),
        actual_sampled_choice_IDs=sorted(choices),offline_only_display_IDs=sorted(OFFLINE))
    candidate = dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],
        patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',
        details=summary,full_goal_complete=False)
    candidate.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    ledger['current_integrated_candidate'] = candidate
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v4136']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,next_focus=NEXT)
    inventory['lil_B167_completed_v4164'] = dict(completed_targets=29,final_review=str(FINAL),registered_candidate=release['candidate'],
        explicit_display_fixture_count=4,actual_unique_speeches=25,actual_English_observations=28,actual_typed_menu_choices=2,
        offline_only_display_IDs=sorted(OFFLINE),natural_source_event_not_selected=True,no_B167_command_omitted_in_content_fixtures=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4003,completed_route_records=4003,source_prose_pending_records=0,
                source_prose_pending_family=None,next=NEXT)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4164'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,
        incomplete_route_source_prose=0,remaining_B168_B180_physical_speeches=321,remaining_choice_command_leads=0,
        later_storylines_shared_town_shop_random_help_prose_open=True,Proof_terminology_consistency_open=True,
        canonical_Maria32_pending_uncredited=True,full_goal_complete=False)
    ledger['lil_B167_completion_v4164'] = dict(summary=summary,final_review=str(FINAL),evidence=evidence,
        goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint'] = summary
    keys = {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys == oldkeys|selected == {historical_key(r) for r in fresh['integrated_record_keys']} == {historical_key(r) for r in fresh['record_keys']}
    assert len(keys) == 5602 and ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 5605
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286',
                'lil_B157_provenance_amendment_v3784','promoted_main_build_v4083']:
        assert ledger[key] == before[key],key
    assert ledger['completed_editorial_families'][:-1] == before['completed_editorial_families']
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    planned=ROOT/(lp.name+'.planned');save(planned,ledger)
    staged=[dict(target=str(lp),before_sha256=sha(lp.read_bytes()),planned=str(planned),planned_sha256=sha(planned.read_bytes()))]
    section='## V4164: 29 Lil B167 reviews completed in V4160\n\n'+summary
    section+='\n\nFinal review: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,path in enumerate(docsfiles):
        first,rest=path.read_text(encoding='utf-8').split('\n',1)
        data=(('# Current editorial handoff - V4164' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
        planned=ROOT/(path.name+'.planned');planned.write_bytes(data)
        staged.append(dict(target=str(path),before_sha256=sha(path.read_bytes()),planned=str(planned),planned_sha256=sha(data)))
    receipt=dict(checkpoint='V4164',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        evidence=evidence,updated_files={r['target']:r['planned_sha256'] for r in staged},prior_checkpoint=str(PRIOR),
        new_source_prose_reviews=0,new_completed_records=29,revised=16,retained=13,fresh_reread=5602,fresh_integrated=5602,
        fresh_pending=0,source_prose=5605,completed=5602,historical_revised=3567,historical_retained=2035,
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest_batches=543,accepted_layers=114,new_actual_emulator_runs=6,new_actual_fixture_runs=4,new_registered_startup_runs=2,
        actual_unique_speech_panels=25,actual_English_speech_observations=28,actual_choice_outcomes=2,
        offline_only_display_IDs=sorted(OFFLINE),remaining_B168_B180_physical_speeches=321,remaining_choice_command_leads=0,
        all_jobs_terminal=True,full_goal_complete=False)
    save(ROOT/'staged_completion_receipt.json',receipt)
    save(ROOT/'staged_completion.json',dict(files=staged,staged_receipt=str(ROOT/'staged_completion_receipt.json'),
        staged_receipt_sha256=sha((ROOT/'staged_completion_receipt.json').read_bytes()),no_current_ledger_or_document_mutation_yet=True))
    print('V4164 completion staged after registered gates; native application and final seal pending. Full goal remains active.')
