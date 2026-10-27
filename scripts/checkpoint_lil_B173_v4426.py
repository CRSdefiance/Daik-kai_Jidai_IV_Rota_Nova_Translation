"""Stage11 native-approved whole-exchange reviews once as pending integration."""
import json
from scripts.editorial_ledger_storage_v1 import encode_ledger
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B173_checkpoint_v4426')
PRIOR = Path('work/analysis/editorial_handoff_verification_v4409b/verified_handoff.json')
APPROVAL = Path('work/analysis/lil_B173_native_approval_v4425/approval_receipt.json')
DOC = Path('translations/lil_B173_editorial_manuscript_v3.json')
FAMILY = 'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11'
from scripts.lil_B173_checkpoint_text_v4426 import NEXT,SUMMARY

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    approval, doc = read(APPROVAL), read(DOC)
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    rows = doc['records']
    assert len(rows) == 11 and all(all(r['review'].values()) for r in rows)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5789,5789,0)
    selected = [dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert len({historical_key(r) for r in selected}) == 11
    assert not {historical_key(r) for r in selected} & {historical_key(r) for r in fresh['record_keys']}
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3936
    assert ledger['records_with_source_and_prose_pass'] == 5792
    docs = [Path('docs')/name for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-3').startswith('# Current editorial handoff - V4408')
    ROOT.mkdir(parents=True)
    for path in [lp,*docs]:
        copy2(path,ROOT/(path.name+'.before'))
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 5803
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] = 3947
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = [r['id'] for r in rows]
    active = ledger['active_source_prose_drafts']
    assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in rows]
    note = '5800 fresh rereads:5789 integrated/11 pending;source/prose5803. B173 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;11-Lil-B173-native-approved-pending-release',note=note)
    pending = dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[173],records=11,record_keys=selected,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],
        proposed_revisions=8,retentions=3,source_prose_reviews_added=11,completion_credit_added=0,
        pending=NEXT,new_emulator_runs=0,actual_selected_B173_IDs=[])
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5800,fresh_pass_records_integrated=5789,
        fresh_pass_records_pending_native_actual_release=11,pending_record_keys=selected,
        pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(DOC),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4201,completed_route_records=4190,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':doc['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B173_v4426'] = dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=5,
        all2_speech_sheets_viewed=True,actual_selected_B173_IDs=[],new_emulator_runs=0)
    previous = ledger['unfinished_editorial_scope_v4408']
    assert sha(Path(previous['path']).read_bytes()) == previous['sha256']
    inventory = deepcopy(read(previous['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[173],count=11,record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=11,next_focus=NEXT)
    inventory['B173_fresh_context_review_checkpoint_v4426'] = pending
    inventory['remaining_B174_B180_unreviewed_uncredited'] = dict(physical_speeches=123,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['earlier_B173_uncredited_leads_are_historical_after_V4426'] = True
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4201,completed_route_records=4190,source_prose_pending_records=11,source_prose_pending_family=FAMILY,next=NEXT)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4426'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,
        incomplete_route_source_prose=11,remaining_B174_B180_physical_speeches=123,remaining_choice_command_leads=0,
        canonical_Maria32_pending_uncredited=True,Proof_terminology_consistency_open=True,
        wider_story_shared_town_random_help_prose_open=True,full_goal_complete=False)
    paths = [PRIOR,APPROVAL,DOC,inv,Path(__file__),Path(approval['merged_native_proof'])]
    for key in ['source_context','control_contract','branch_proof','source_entry_proof','whole_exchange_context_notes',
                'effective_current_comparison','native_font_proof','actor_terminology_reconciliation',
                'source_effect_and_predicate_contract','source_nameplate_consumer_proof']:
        path = Path(doc[key])
        assert sha(path.read_bytes()) == doc[key+'_sha256']
        paths.append(path)
    evidence = {str(path):sha(path.read_bytes()) for path in paths}
    ledger['lil_B173_scope_reconciliation_v4426'] = dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=11,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    planned = {lp:encode_ledger(ledger)}
    section = '## V4426:11 B173 contextual/native reviews;integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for index,path in enumerate(docs):
        first,rest = path.read_text(encoding='utf-3').split('\n',1)
        planned[path] = (('# Current editorial handoff - V4426' if index==0 else first)+'\n\n'+section+rest).encode('utf-3')
    staged = ROOT/'staged'
    staged.mkdir()
    plan = []
    for index,(path,data) in enumerate(planned.items()):
        output = staged/(str(index)+'.planned')
        output.write_bytes(data)
        plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable = ['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4426',evidence=evidence,
        preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),
        new_source_prose_reviews=11,new_completed_records=0,proposed_revisions=8,justified_retentions=3,
        fresh_reread=5800,fresh_integrated=5789,fresh_pending=11,source_prose=5803,completed=5789,
        historical_revised=3678,historical_retained=2111,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4426 staged:5800 reread/5789 integrated/11 pending;5803 source/prose. Latest V4404 and promoted V4353 unchanged;full goal active.')
