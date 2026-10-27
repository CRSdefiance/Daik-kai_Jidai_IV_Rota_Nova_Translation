"""Stage37 native-approved whole-exchange reviews once as pending integration."""
import json
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_checkpoint_v4329')
PRIOR = Path('work/analysis/editorial_handoff_verification_v4308b/verified_handoff.json')
APPROVAL = Path('work/analysis/lil_B171_native_approval_v4328/approval_receipt.json')
DOC = Path('translations/lil_B171_editorial_manuscript_v4.json')
FAMILY = 'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37'
from scripts.lil_B171_checkpoint_text_v4329 import NEXT,SUMMARY

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    approval, doc = read(APPROVAL), read(DOC)
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    rows = doc['records']
    assert len(rows) == 37 and all(all(r['review'].values()) for r in rows)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5725,5725,0)
    selected = [dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert len({historical_key(r) for r in selected}) == 37
    assert not {historical_key(r) for r in selected} & {historical_key(r) for r in fresh['record_keys']}
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3872
    assert ledger['records_with_source_and_prose_pass'] == 5728
    docs = [Path('docs')/name for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4307')
    ROOT.mkdir(parents=True)
    for path in [lp,*docs]:
        copy2(path,ROOT/(path.name+'.before'))
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 5765
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] = 3909
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'] = [r['id'] for r in rows]
    active = ledger['active_source_prose_drafts']
    assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in rows]
    note = '5762 fresh rereads:5725 integrated/37 pending;source/prose5765. B171 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;37-Lil-B171-native-approved-pending-release',note=note)
    pending = dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[171],records=37,record_keys=selected,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],
        proposed_revisions=24,retentions=13,source_prose_reviews_added=37,completion_credit_added=0,
        pending=NEXT,new_emulator_runs=0,actual_selected_B171_IDs=[])
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5762,fresh_pass_records_integrated=5725,
        fresh_pass_records_pending_native_actual_release=37,pending_record_keys=selected,
        pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(DOC),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4163,completed_route_records=4126,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':doc['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B171_v4329'] = dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=16,
        all5_speech_sheets_viewed=True,actual_selected_B171_IDs=[],new_emulator_runs=0)
    previous = ledger['unfinished_editorial_scope_v4307']
    assert sha(Path(previous['path']).read_bytes()) == previous['sha256']
    inventory = deepcopy(read(previous['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[171],count=37,record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=37,next_focus=NEXT)
    inventory['B171_fresh_context_review_checkpoint_v4329'] = pending
    inventory['remaining_B172_B180_unreviewed_uncredited'] = dict(physical_speeches=161,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['earlier_B171_uncredited_leads_are_historical_after_V4329'] = True
    for unit in inventory['broader_coverage_units']:
        if unit['id'] == 'all-route-scenes':
            unit.update(reviewed_route_records=4163,completed_route_records=4126,source_prose_pending_records=37,source_prose_pending_family=FAMILY,next=NEXT)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4329'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,
        incomplete_route_source_prose=37,remaining_B172_B180_physical_speeches=161,remaining_choice_command_leads=0,
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
    ledger['lil_B171_scope_reconciliation_v4329'] = dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=37,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    planned = {lp:(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')}
    section = '## V4329:37 B171 contextual/native reviews;integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for index,path in enumerate(docs):
        first,rest = path.read_text(encoding='utf-8').split('\n',1)
        planned[path] = (('# Current editorial handoff - V4329' if index==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged = ROOT/'staged'
    staged.mkdir()
    plan = []
    for index,(path,data) in enumerate(planned.items()):
        output = staged/(str(index)+'.planned')
        output.write_bytes(data)
        plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable = ['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4329',evidence=evidence,
        preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),
        new_source_prose_reviews=37,new_completed_records=0,proposed_revisions=24,justified_retentions=13,
        fresh_reread=5762,fresh_integrated=5725,fresh_pending=37,source_prose=5765,completed=5725,
        historical_revised=3635,historical_retained=2090,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4329 staged:5762 reread/5725 integrated/37 pending;5765 source/prose. Latest V4303 and promoted V4251 unchanged;full goal active.')
