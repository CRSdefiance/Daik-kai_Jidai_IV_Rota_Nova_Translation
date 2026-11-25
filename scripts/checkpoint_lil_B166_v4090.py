"""Credit B166's 44 contextual/native reviews as pending, preserving completion."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B166_checkpoint_v4090')
PRIOR = Path('releases/all_routes_unified_v4046/verification/promotion_final_audit.json')
APPROVAL = Path('work/analysis/lil_B166_native_approval_v4082/approval_receipt.json')
DOCS = [Path('translations/lil_B166_editorial_manuscript_v5.json'),
        Path('translations/lil_B166_choice_manuscript_v2.json')]
FAMILY = 'Lil-B166-Manuel-ship-care-recruitment-optional-Workroom-advice44'
NEXT = ('Complete B166 relocation and final stored/native references, representative source/English '
        'speech, actual advice-choice returns and transitions; then register and build the complete '
        'cumulative canonical stack, reconstruct the clean-input patch and check startup. Continue '
        'B167-B180 and every wider editorial family. V4046 remains the promoted main build.')
SUMMARY = '''V4090 reconciles 44 fresh contextual/native reviews for the complete Lil SC2 B166 Manuel exchange: 24 proposed revisions and 20 individually justified retentions. All 42 clean Japanese speeches and both advice labels were read as a complete conversation and individually glossed before predecessor English comparison. Preserve Manuel's absorbed ship improvements and apologies, Lil's mounting impatience and frank technical ignorance, the crying-ship personification, Camille's enthusiastic persuasion, optional Fernando's dry complaint, reluctant consent, Manuel's long absence and hesitation, grateful acceptance and full introduction, and the optional flagship Workroom advice. Original names are Manuel Almeida, Fernando Dias and Camille. No kinship, rank, numeric duration, formal retirement, named source port or earned recruitment is invented.

Keep sail placement/type, additional sails, gun batteries and cannon type; bind all nine room names and Speech, Shipwright and Surgeon to reviewed Help. Preserve affected officers and sailors, the grouped food/water benefit, treatment and faster recovery, repairs while sailing and assistance with shipyard refits/repairs. Do not add stat thresholds, instant/full cures or individual room-resource mappings. Original source bindings preserve 62 commands, 42 complete progressive preambles, actors 2/9/20/23, FI3, eight relative sites/80 clean-current cases, one unforced Fernando predicate, 11 opaque leaves, two resources/20 boundary cases, six presentation sites, one typed menu, one late A000 and one end. Both advice paths rejoin before A000; declining advice does not reject employment. Spoken consent and the introduction do not move the original runtime effect. Six original name consumers retain scratch ownership. The later older-record technical re-audit remains open.

Native approval V4082b covers 42 complete 216x64 speech planes, 336 logical/compiled alignment cases, 17 source-consumer negatives, 14 formatter negatives, six choice selection/cancel cases and eight style-label planes. Six final speech sheets, the native menu sheet and four actual menu screens were viewed or exactly match viewed predecessors. Fifteen narrow row-count notes exempt no other issue. Final phrase flow and the synthetic menu finding are resolved without changing reviewed meanings, controls, labels, guards or adding authored padding. Read-only observations identify logical 54x12 caption views within the actual 256x36 backing. Three focused menu-only cold boots show complete captions and highlight movement; no B166 speech, actual accepted choice/return, source event eligibility or recruitment is claimed.

Coverage becomes 5573 fresh contextual rereads: 5529 integrated/completed and 44 pending integration. Source/prose becomes 5576, including 3720 SC2 and unchanged 64 SC3; route reviewed/completed is 3974/3930. Completed historical decisions remain 3527 revised/2002 retained. This reconciles the previously separate uncredited B166 objects exactly once; it adds no completion credit, ROM change, registration or new gameplay. Promoted main V4046 remains 539 manuscript batches/114 accepted layers with the verified exact clean-input patch and immutable construction baseline.

Remaining B167-B180 contains 348 physical speeches and one choice-command lead; this is not the full Lil/project denominator. Every wider storyline, shared shop/town dialogue, random scene, help and remaining player-facing prose stays in scope. Preserve COMMON 750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency and Samwell's uncredited full-catalogue middle-field lead. Graphics and all 18 plaques remain separate; retain the later older-record technical re-audit/queued 0D gap. Preserve every ROM, translation, draft, producer, proof, failure and clean/canonical input. The full goal remains active.'''

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    before = deepcopy(ledger)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    approval = read(APPROVAL)
    manuscripts = [read(p) for p in DOCS]
    assert approval['manuscripts'] == {str(p): sha(p.read_bytes()) for p in DOCS}
    rows = [r for d in manuscripts for r in d['records']]
    assert len(rows) == len({r['id'] for r in rows}) == 44
    assert Counter(r['editorial_decision'] for r in rows) == {'revise': 24, 'retain-wording': 20}
    assert all(all(r['review'].values()) for r in rows)
    assert approval['new_completed_records'] == approval['new_source_prose_reviews'] == 0
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'],
            fresh['fresh_pass_records_pending_native_actual_release']) == (5529, 5529, 0)
    selected = [dict(file_path='/data/SC2.DK4', id=r['id']) for r in rows]
    assert not {historical_key(r) for r in selected} & {historical_key(r) for r in fresh['record_keys']}
    assert ledger['records_with_source_and_prose_pass'] == 5532
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3676
    docs = [Path('docs') / n for n in ['editorial_handoff_current.md', 'translation_progress.md',
            'editorial_review_goal.md', 'todo.md', 'known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4083')
    ROOT.mkdir(parents=True)
    for path in [lp, *docs]:
        copy2(path, ROOT / (path.name + '.before'))
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 5576
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] = 3720
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = [r['id'] for r in rows]
    active = ledger['active_source_prose_drafts']
    for path, doc in zip(DOCS, manuscripts, strict=True):
        assert str(path) not in active['manuscripts']
        active['manuscripts'].append(str(path))
        active['route_record_subsets_pending'][str(path)] = [r['id'] for r in doc['records']]
    note = '5573 fresh rereads:5529 integrated/44 pending; source/prose5576. B166 is credited once as pending; no completion or actual story/choice-return credit.'
    active.update(status='3-reviewed-COMMON-incomplete;44-Lil-B166-native-approved-pending-release', note=note)
    pending = dict(id=FAMILY, file_path='/data/SC2.DK4', blocks=[166], records=44, record_keys=selected,
                   manuscript=str(DOCS[0]), manuscript_sha256=sha(DOCS[0].read_bytes()),
                   manuscripts=approval['manuscripts'], proposed_revisions=24, retentions=20,
                   source_prose_reviews_added=44, completion_credit_added=0, pending=NEXT,
                   new_emulator_runs=0, prior_menu_only_cold_boots=3, actual_selected_B166_IDs=[])
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5573, fresh_pass_records_integrated=5529,
                 fresh_pass_records_pending_native_actual_release=44, pending_record_keys=selected,
                 pending_contextual_families=[pending], latest_pending_contextual_family=FAMILY,
                 latest_contextual_manuscript=str(DOCS[0]), coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=3974, completed_route_records=3930, next=NEXT)
    ledger['coverage_units'].append({**pending, 'status': manuscripts[0]['status'], 'full_goal_complete': False})
    ledger['formatting_watchlist']['lil_B166_v4090'] = dict(status='native-approved;credited-pending-relocation-story-choices-release',
        approval=str(APPROVAL), approval_sha256=sha(APPROVAL.read_bytes()), row_count_notes=15,
        all6_speech_and_menu_sheets_viewed=True, actual_selected_B166_IDs=[], new_emulator_runs=0,
        supersedes_uncredited_status_at_V4072_and_V4083_without_deleting_history=True)
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v4072']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY, file_path='/data/SC2.DK4',
        blocks=[166], count=44, record_IDs=[r['id'] for r in rows])], incomplete_route_source_prose_count=44, next_focus=NEXT)
    inventory['B166_credited_native_approved_pending_v4090'] = pending
    inventory['earlier_B166_uncredited_inventory_entries_are_historical'] = True
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=3974, completed_route_records=3930,
                source_prose_pending_records=44, source_prose_pending_family=FAMILY, next=NEXT)
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v4090'] = dict(path=str(inv), sha256=sha(inv.read_bytes()),
        incomplete_COMMON=3, incomplete_route_source_prose=44, remaining_B167_B180_physical_speeches=348,
        remaining_B167_B180_choice_command_leads=1, canonical_Maria32_pending_uncredited=True,
        Proof_terminology_consistency_open=True, wider_story_shared_town_random_help_prose_open=True, full_goal_complete=False)
    paths = [PRIOR, APPROVAL, *DOCS, inv, Path(__file__), Path(approval['merged_native_proof'])]
    for key in ['source_context', 'control_contract', 'branch_proof', 'source_entry_proof',
                'whole_exchange_context_notes', 'effective_current_comparison', 'native_font_proof',
                'actor_terminology_reconciliation', 'source_effect_and_predicate_contract', 'source_nameplate_consumer_proof']:
        path = Path(manuscripts[0][key])
        assert sha(path.read_bytes()) == manuscripts[0][key + '_sha256']
        paths.append(path)
    evidence = {str(p): sha(p.read_bytes()) for p in paths}
    ledger['lil_B166_scope_reconciliation_v4090'] = dict(summary=SUMMARY, evidence=evidence,
        pending_family=pending, source_prose_reviews_added=44, completion_credit_added=0, full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    for key in ['completed_editorial_families', 'records_editorially_completed', 'records_revised_and_integrated',
                'retained_wordings_editorially_completed', 'completed_editorial_record_counts_by_file',
                'current_integrated_candidate', 'reviewed_but_incomplete_COMMON_IDs', 'unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal', 'native_source_universe_inventory_v2701c',
                'Proof_terminology_consistency_lead_v3286', 'lil_B157_provenance_amendment_v3784', 'promoted_main_build_v4083']:
        assert ledger[key] == before[key], key
    save(lp, ledger)
    section = '## V4090: 44 B166 contextual/native reviews; integration pending\n\n' + SUMMARY
    section += '\n\nApproval: ' + APPROVAL.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '.\n\n'
    for i, path in enumerate(docs):
        first, rest = path.read_text(encoding='utf-8').split('\n', 1)
        path.write_text(('# Current editorial handoff - V4090' if i == 0 else first) + '\n\n' + section + rest,
                        encoding='utf-8', newline='\n')
    save(ROOT / 'checkpoint_receipt.json', dict(checkpoint='V4090', evidence=evidence,
        updated_files={str(p): sha(p.read_bytes()) for p in [lp, *docs]}, prior_verified_handoff=str(PRIOR),
        new_source_prose_reviews=44, new_completed_records=0, proposed_revisions=24, justified_retentions=20,
        fresh_reread=5573, fresh_integrated=5529, fresh_pending=44, source_prose=5576, completed=5529,
        historical_revised=3527, historical_retained=2002, new_emulator_runs=0, all_jobs_terminal=True, full_goal_complete=False))
    print('V4090:5573 reread/5529 integrated/44 pending;5576 source/prose. V4046 main unchanged;full goal active.')
