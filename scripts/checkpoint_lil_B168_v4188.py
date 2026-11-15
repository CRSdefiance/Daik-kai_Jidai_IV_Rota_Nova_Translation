"""Stage 54 contextual/native reviews once as pending; leave every completion intact."""
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B168_checkpoint_v4188')
PRIOR = Path('work/analysis/promotion_v4186/promotion_receipt.json')
APPROVAL = Path('work/analysis/lil_B168_native_approval_v4187/approval_receipt.json')
DOC = Path('translations/lil_B168_editorial_manuscript_v7.json')
FAMILY = 'Lil-B168-Mikhail-recruitment-naturalist-item-information54'
NEXT = 'Complete B168 relocation and stored/native references, representative Japanese/English story, distinct presentation/contact and FE panels, original effect and normal return; then registered cumulative release, exact clean-input patch and startup. Continue B169-B180 and every wider editorial family. V4160 remains the promoted main build; preserve all ROMs and earlier translations.'
SUMMARY = '''V4188 records 54 fresh contextual/native reviews for the complete Lil SC2 B168 Mikhail recruitment exchange and item-information notices: 28 proposed revisions and 26 individually justified retentions. All 54 clean Japanese speeches were read as one exchange and individually glossed before predecessor English comparison. Preserve optional Julio warnings, the shopkeeper's local reputation, two women's admiration, Mikhail's confident peppercorn/Brunei explanation and rabbit-droppings reversal, his bust-size boast, Lil's objections, Camille's ambiguous reassurance and self-deprecating group remark, optional Fernando's wounded aside, Mikhail's refusal of a man's invitation and sudden decision after meeting Lil. Keep the intrusive calls, withdrawal of invitation, reluctant consent, unfinished condition, source touching cue, protest, comic yelp and sigh. Familiar addresses create no kinship; add no degree, rank, age, body-part detail, romance, particular blow, source port, item award or botanical correction.

Source-owned bindings preserve 51 progressive speeches, three distinct null-actor FE panels, FI7/FA1/FO1, eight static actors 2/6/9/20/76/87/165/166, 82 commands, twelve relative sites/120 clean-current structural cases, three membership predicates, four resources/40 boundary cases, six presentation commands, sixteen opaque leaves, one later A000 and both consecutive end words at clean offsets2906/2910. Original getters bind sixteen name consumers: ten owned scratch paths and six read-only generic-role paths. Printable57/4C/A5/A6 remain actor selectors. Mikhail is a naturalist, cannot serve as a ship's officer on the Deck, enables detailed item information, and X is pressed while that information is displayed. Current reviewed Help/Deck, Items and Brunei terms are bound. Offline getter/resource/structural probes establish neither natural eligibility nor full effects; the original runtime effect stays after the contact/protest sequence. The later older-record technical re-audit stays open.

Native approval V4187 covers all 54 complete planes: 51 progressive216x64 and three FE logical228x48/physical228x64 with native12/16 row spacing and a single complete page. All432 logical/compiled alignment cases, complete leading/internal/final glyphs, unique cells and zero row origins pass. All seven final sheets were viewed. Twenty narrow row-count notes exempt no glyph, bounds, pagination, macro, control, weak-ending, orphan or blank-page issue. Twenty-six source-consumer, three missing-macro and fourteen formatter rejection controls pass. Phrase-flow refinements preserve complete meaning and every runtime substitution. No manual break, padding, metric/guard change or wording waiver. No B168 gameplay or actual transition coverage is claimed yet.

Coverage becomes5656 fresh contextual rereads:5602 integrated/completed and54 pending. Source/prose becomes5659, including3803 SC2 and unchanged64 SC3; reviewed/completed route objects4057/4003. Historical completed decisions remain3567 revised/2035 retained. B168 is credited once as pending, with no completion credit. Main promoted V4160 remains543 manuscript batches/114 accepted layers and its exact clean-input patch. Immutable canonical input, registry, builder, promoted pointer, all prior completions and all earlier ROMs/translations/drafts/executed producers/proofs/failures remain unchanged.

Remaining B169-B180 contains267 physical speeches and zero typed choice-command leads; this is not a full Lil/project denominator. Every wider storyline, shared shop/town dialogue, random scene, Help and remaining prose stays open. Preserve COMMON750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency, Samwell's full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate; retain the later older-record technical re-audit/queued0D gap. Full goal active.'''
UNCHANGED = ['completed_editorial_families', 'records_editorially_completed', 'records_revised_and_integrated',
 'retained_wordings_editorially_completed', 'completed_editorial_record_counts_by_file', 'current_integrated_candidate',
 'reviewed_but_incomplete_COMMON_IDs', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal',
 'native_source_universe_inventory_v2701c', 'Proof_terminology_consistency_lead_v3286',
 'lil_B157_provenance_amendment_v3784', 'promoted_main_build_v4186']

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    before = deepcopy(ledger)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    approval, doc = read(APPROVAL), read(DOC)
    assert approval['manuscripts'] == {str(DOC): sha(DOC.read_bytes())}
    rows = doc['records']
    assert len(rows) == len({r['id'] for r in rows}) == 54
    assert Counter(r['editorial_decision'] for r in rows) == {'revise': 28, 'retain-wording': 26}
    assert all(all(r['review'].values()) for r in rows)
    assert approval['new_completed_records'] == approval['new_source_prose_reviews'] == 0
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5602, 5602, 0)
    selected = [dict(file_path='/data/SC2.DK4', id=r['id']) for r in rows]
    assert not {historical_key(r) for r in selected} & {historical_key(r) for r in fresh['record_keys']}
    assert ledger['records_with_source_and_prose_pass'] == 5605
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3749
    docs = [Path('docs') / n for n in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4186')
    ROOT.mkdir(parents=True)
    for path in [lp, *docs]:
        copy2(path, ROOT / (path.name + '.before'))
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 5659
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] = 3803
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = [r['id'] for r in rows]
    active = ledger['active_source_prose_drafts']
    assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in rows]
    note = '5656 fresh rereads:5602 integrated/54 pending;source/prose5659. B168 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;54-Lil-B168-native-approved-pending-release', note=note)
    pending = dict(id=FAMILY, file_path='/data/SC2.DK4', blocks=[168], records=54, record_keys=selected,
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), manuscripts=approval['manuscripts'],
        proposed_revisions=28, retentions=26, source_prose_reviews_added=54, completion_credit_added=0,
        pending=NEXT, new_emulator_runs=0, actual_selected_B168_IDs=[])
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5656, fresh_pass_records_integrated=5602,
        fresh_pass_records_pending_native_actual_release=54, pending_record_keys=selected,
        pending_contextual_families=[pending], latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(DOC), coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4057, completed_route_records=4003, next=NEXT)
    ledger['coverage_units'].append({**pending, 'status': doc['status'], 'full_goal_complete': False})
    ledger['formatting_watchlist']['lil_B168_v4188'] = dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL), approval_sha256=sha(APPROVAL.read_bytes()), row_count_notes=20,
        all7_speech_and_FE_sheets_viewed=True, actual_selected_B168_IDs=[], new_emulator_runs=0)
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v4164']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY, file_path='/data/SC2.DK4', blocks=[168], count=54, record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=54, next_focus=NEXT)
    inventory['B168_fresh_context_review_checkpoint_v4188'] = pending
    inventory['remaining_B169_B180_unreviewed_uncredited'] = dict(physical_speeches=267, typed_choice_command_leads=0, not_full_Lil_or_project_denominator=True)
    inventory['remaining_B168_B180_inventory_is_historical_at_V4164'] = True
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4057, completed_route_records=4003, source_prose_pending_records=54, source_prose_pending_family=FAMILY, next=NEXT)
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v4188'] = dict(path=str(inv), sha256=sha(inv.read_bytes()),
        incomplete_COMMON=3, incomplete_route_source_prose=54, remaining_B169_B180_physical_speeches=267,
        remaining_choice_command_leads=0, canonical_Maria32_pending_uncredited=True, Proof_terminology_consistency_open=True,
        wider_story_shared_town_random_help_prose_open=True, full_goal_complete=False)
    paths = [PRIOR, APPROVAL, DOC, inv, Path(__file__), Path(approval['merged_native_proof'])]
    for key in ['source_context', 'control_contract', 'branch_proof', 'source_entry_proof', 'whole_exchange_context_notes',
                'effective_current_comparison', 'native_font_proof', 'actor_terminology_reconciliation',
                'source_effect_and_predicate_contract', 'source_nameplate_consumer_proof']:
        path = Path(doc[key])
        assert sha(path.read_bytes()) == doc[key + '_sha256']
        paths.append(path)
    stable = [Path('translations/release_stack.json'), Path('translations/promoted_build.json'), Path('scripts/build_integrated_release.py')]
    evidence = {str(path): sha(path.read_bytes()) for path in paths}
    ledger['lil_B168_scope_reconciliation_v4188'] = dict(summary=SUMMARY, evidence=evidence, pending_family=pending,
        source_prose_reviews_added=54, completion_credit_added=0, full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    for key in UNCHANGED:
        assert ledger[key] == before[key], key
    staged = ROOT / 'staged'
    staged.mkdir()
    planned = {lp: (json.dumps(ledger, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8')}
    section = '## V4188: 54 B168 contextual/native reviews; integration pending\n\n' + SUMMARY + '\n\nApproval: ' + APPROVAL.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '.\n\nNext: ' + NEXT + '\n\n'
    for index, path in enumerate(docs):
        first, rest = path.read_text(encoding='utf-8').split('\n', 1)
        planned[path] = (('# Current editorial handoff - V4188' if index == 0 else first) + '\n\n' + section + rest).encode('utf-8')
    plan = []
    for index, (path, data) in enumerate(planned.items()):
        output = staged / (str(index) + '.planned')
        output.write_bytes(data)
        plan.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()),
                         planned=str(output.resolve()), planned_sha256=sha(data)))
    save(ROOT / 'mutation_plan.json', plan)
    save(ROOT / 'staged_receipt.json', dict(checkpoint='V4188', evidence=evidence,
        preserved_release_files={str(path): sha(path.read_bytes()) for path in stable},
        prior_verified_handoff=str(PRIOR), new_source_prose_reviews=54, new_completed_records=0,
        proposed_revisions=28, justified_retentions=26, fresh_reread=5656, fresh_integrated=5602,
        fresh_pending=54, source_prose=5659, completed=5602, historical_revised=3567, historical_retained=2035,
        new_emulator_runs=0, all_jobs_terminal=True, full_goal_complete=False))
    print('V4188 staged:5656 reread/5602 integrated/54 pending;5659 source/prose. Promoted V4160 unchanged;full goal active.')
