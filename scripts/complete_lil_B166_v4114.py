"""Complete previously credited B166 reviews only after registered release/startup gates."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B166_completion_text_v4114 import NEXT,ACTUAL_SCOPE,make_summary

ROOT = Path('work/analysis/lil_B166_completion_v4114')
FINAL = Path('translations/lil_B166_contextual_final_review_v1.json')
DOCS = [Path('translations/lil_B166_editorial_manuscript_v6.json'),Path('translations/lil_B166_choice_manuscript_v3.json')]
RELEASE = Path('work/analysis/lil_B166_release_v4111/registered_release_verification.json')
START = Path('work/analysis/lil_B166_startup_v4113/cold_boot_Lil_startup_town_verification.json')
VISUAL = START.parent/'current_six_frame_visual_review.json'
ACTUAL = Path('work/analysis/lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return.json')
TRANSITIONS = Path('work/analysis/lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review.json')
PRIOR = Path('work/analysis/lil_B166_checkpoint_v4090/checkpoint_receipt.json')
REG = Path('work/analysis/lil_B166_registration_v4109/registration_receipt.json')
FAMILY = 'Lil-B166-Manuel-ship-care-recruitment-optional-Workroom-advice44'
OFFLINE = {'DK4_MES_B166_R0087'}

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
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all541_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4046'] and start['paired_frame_count'] == 31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert not start['actual_selected_B166_IDs']
    assert view['viewed'] and view['sheet'] == start['review_sheet']
    assert view['sha256'] == start['review_sheet_sha256'] == sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels'] == 41 and actual['complete_matching_observations'] == 73
    assert actual['actual_new_cold_boot_runs'] == 4 and not actual['failures']
    assert reg['negative_count'] == 72 and reg['all_negatives_reject_before_mutation']
    docs = [read(path) for path in DOCS]
    doc = docs[0]
    mapping,sample = read(doc['reference_map']),read(doc['representative_proof'])
    rows = deepcopy([row for document in docs for row in document['records']])
    assert len(rows) == 44 and Counter(r['editorial_decision'] for r in rows) == {'revise':24,'retain-wording':20}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert set(sample['offline_only_display_IDs']) == OFFLINE and sample['Fernando_remark_not_actual_or_byte_identical_reuse']
    image = NdsImage.open(release['candidate'])
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256'] == start['candidate_sha256']
    refs = {r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    choices = {r['id']:r for b in mapping['blocks'] for c in b['choice_commands'] for r in c['label_references']}
    parity = {r['id']:r for r in read(doc['final_padding_proof'])['final_target_parity_cases']}
    stage = {r['id']:r for r in release['stage']['changed_records']}
    sampled = {r['id'] for r in actual['actual_panels']}
    assert len(sampled) == 41 and sampled|OFFLINE == set(refs) and not sampled&OFFLINE and len(choices) == 2
    for row in rows:
        ident = row['id']
        choice = row['kind'] == 'typed-choice-label'
        spec = (choices if choice else refs)[ident]
        at,block = spec['new_offset'],blocks[166]
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
        ref = dict(block=166,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'))
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
            actual_source_event166_selected=False,individual_actual_source_event_activation_not_claimed=True,
            current_complete_native_display_pending=False,registered_integration_pending=False,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        if choice:
            row.update(actual_advice_choice_result_observed=True,actual_choice_selection_still_pending=False,
                current_native_typed_choice_font_reference_and_outcome_binding_pending=False)
        if row['editorial_decision'] == 'retain-wording':
            assert paragraph == row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    oldkeys = {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    selected = {historical_key(r) for r in rows}
    assert len(oldkeys) == 5529 and len(selected) == 44 and not oldkeys&selected
    assert selected == {historical_key(r) for r in fresh['pending_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5573,5529,44)
    assert ledger['records_with_source_and_prose_pass'] == 5576 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3720
    assert docsfiles[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4090')
    ROOT.mkdir(parents=True)
    for path in [lp,*docsfiles]:
        copy2(path,ROOT/(path.name+'.before'))
    summary = make_summary(release)
    proofpaths = [*DOCS,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,Path(doc['reference_map']),
        Path(doc['representative_proof']),Path(doc['final_padding_proof']),Path(doc['source_nameplate_consumer_proof']),
        Path('scripts/lil_B166_completion_text_v4114.py'),Path(__file__)]
    evidence = {str(p):sha(p.read_bytes()) for p in proofpaths}
    final = dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(DOCS[0]),choices=str(DOCS[1]),manuscripts={str(p):sha(p.read_bytes()) for p in DOCS},
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
        revised=24,retained=20,source_prose_credit_already_recorded_in_V4090=True,
        all44_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,
        actual_sampled_B22_display_IDs=sorted(sampled),actual_sampled_choice_IDs=sorted(choices),offline_only_display_IDs=sorted(OFFLINE),
        actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=summary,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[166],
        record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=24,retained_count=20,
        fresh_revisions=24,fresh_retentions=20,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5573,records_revised_and_integrated=3551,retained_wordings_editorially_completed=2022)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] = 3720
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = []
    active = ledger['active_source_prose_drafts']
    for path,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][path] = [i for i in ids if ('/data/SC2.DK4',i) not in selected]
    for path in DOCS:
        if str(path) not in active['manuscripts']:
            active['manuscripts'].append(str(path))
        active['route_record_subsets_pending'][str(path)] = []
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='5573 fresh contextual rereads integrated;source/prose5576. Remaining348 physical B167-B180 speech leads,one choice-command lead and every wider editorial family remain open.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=5573,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],
        pending_contextual_families=[],latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOCS[0]),
        latest_contextual_choice_draft=str(DOCS[1]),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=44,final_review=str(FINAL),new_revisions=24,justified_retentions=20,
        new_completed_records=44,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=24,retained=20),
        actual_selected_B166_source_events=[],actual_sampled_B22_display_IDs=sorted(sampled),actual_sampled_choice_IDs=sorted(choices),
        offline_only_display_IDs=sorted(OFFLINE),new_current_candidate_emulator_runs=2,new_explicit_display_fixture_runs=4))
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=3974,completed_route_records=3974,next=NEXT)
        if unit['id'] == FAMILY:
            unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,
                completion_credit_added=44,final_review=str(FINAL),new_emulator_runs=6,new_current_candidate_emulator_runs=2,
                new_explicit_source_English_fixture_runs=4,actual_sampled_B22_display_IDs=sorted(sampled),
                actual_sampled_choice_IDs=sorted(choices),offline_only_display_IDs=sorted(OFFLINE),full_goal_complete=False)
    ledger['formatting_watchlist']['lil_B166_v4090'].update(status='complete-through-V4114',registered_release_pending=False,final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_B166_v4114'] = dict(status='all44-source-native-reference-representative-release-checks-pass',
        final_review=str(FINAL),evidence=evidence,no_glyph_bounds_pagination_or_control_waivers=True,
        actual_selected_B166_source_events=[],actual_sampled_B22_display_IDs=sorted(sampled),
        actual_sampled_choice_IDs=sorted(choices),offline_only_display_IDs=sorted(OFFLINE))
    candidate = dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],
        patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',
        details=summary,full_goal_complete=False)
    candidate.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    ledger['current_integrated_candidate'] = candidate
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v4090']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,next_focus=NEXT)
    inventory['lil_B166_completed_v4114'] = dict(completed_targets=44,final_review=str(FINAL),registered_candidate=release['candidate'],
        explicit_display_fixture_count=4,actual_unique_speeches=41,actual_English_observations=73,actual_typed_menu_choices=2,
        offline_only_display_IDs=sorted(OFFLINE),natural_source_event_not_selected=True,source_A000_effect_not_earned=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=3974,completed_route_records=3974,source_prose_pending_records=0,
                source_prose_pending_family=None,next=NEXT)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4114'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,
        incomplete_route_source_prose=0,remaining_B167_B180_physical_speeches=348,remaining_choice_command_leads=1,
        later_storylines_shared_town_shop_random_help_prose_open=True,Proof_terminology_consistency_open=True,
        canonical_Maria32_pending_uncredited=True,full_goal_complete=False)
    ledger['lil_B166_completion_v4114'] = dict(summary=summary,final_review=str(FINAL),evidence=evidence,
        goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint'] = summary
    keys = {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys == oldkeys|selected == {historical_key(r) for r in fresh['integrated_record_keys']} == {historical_key(r) for r in fresh['record_keys']}
    assert len(keys) == 5573 and ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 5576
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286',
                'lil_B157_provenance_amendment_v3784','promoted_main_build_v4083']:
        assert ledger[key] == before[key],key
    assert ledger['completed_editorial_families'][:-1] == before['completed_editorial_families']
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    save(lp,ledger)
    section = '## V4114: 44 Lil B166 reviews completed in V4110\n\n'+summary
    section += '\n\nFinal review: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,path in enumerate(docsfiles):
        first,rest = path.read_text(encoding='utf-8').split('\n',1)
        path.write_text(('# Current editorial handoff - V4114' if i == 0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V4114',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docsfiles]},prior_checkpoint=str(PRIOR),
        new_source_prose_reviews=0,new_completed_records=44,revised=24,retained=20,fresh_reread=5573,fresh_integrated=5573,
        fresh_pending=0,source_prose=5576,completed=5573,historical_revised=3551,historical_retained=2022,
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest_batches=541,accepted_layers=114,new_actual_emulator_runs=6,new_actual_fixture_runs=4,new_registered_startup_runs=2,
        actual_unique_speech_panels=41,actual_English_speech_observations=73,actual_choice_outcomes=2,
        offline_only_display_IDs=sorted(OFFLINE),remaining_B167_B180_physical_speeches=348,remaining_choice_command_leads=1,
        all_jobs_terminal=True,full_goal_complete=False))
    print('V4114:5573 reread/integrated,0pending;5576 source/prose,3551 revised/2022 retained.44 B166 reviews complete inV4110;full goal active.')
