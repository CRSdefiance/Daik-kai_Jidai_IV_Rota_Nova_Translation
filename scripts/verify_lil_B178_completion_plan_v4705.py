"""Validate every staged completion change and all historical values before application."""
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_lil_B178_v4705 import ROOT,DOC,FINAL,FAMILY,RELEASE,REG
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save


def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}


if __name__=='__main__':
    output=ROOT/'independent_preapplication_audit.json'
    assert not output.exists()
    workspace=Path.cwd().resolve()
    plan=read(ROOT/'staged_completion.json')
    assert len(plan['files'])==6
    lp=Path('translations/editorial_review_current_v1.json')
    for entry in plan['files']:
        target,planned=Path(entry['target']),Path(entry['planned'])
        assert target.is_relative_to(workspace) and planned.is_relative_to(ROOT.resolve())
        assert sha(target.read_bytes())==entry['before_sha256']
        assert sha(planned.read_bytes())==entry['planned_sha256']
    entry=next(r for r in plan['files'] if Path(r['target'])==lp.resolve())
    before=read(lp);ledger=read(entry['planned'])
    assert Path(entry['planned']).read_bytes()==encode_ledger(ledger) and Path(entry['planned']).stat().st_size<100*1024*1024
    assert lp.read_bytes()==(ROOT/(lp.name+'.before')).read_bytes()
    allowed={'completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','reviewed_but_incomplete_route_record_IDs',
        'active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units','formatting_watchlist',
        'current_integrated_candidate','unfinished_editorial_scope_v4705','lil_B178_completion_v4705','latest_checkpoint'}
    same_except(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    family=ledger['completed_editorial_families'][-1];final=read(FINAL);doc=read(DOC)
    assert family['id']==FAMILY and family['records']==final['records']
    assert len(family['records'])==13 and Counter(r['editorial_decision'] for r in family['records'])=={'revise':2,'retain-wording':11}
    assert [r['english'] for r in family['records']]==[r['english'] for r in doc['records']]
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5898,5901,3740,2158)
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    same_except(old,fresh,{'integrated_record_keys','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release',
        'pending_record_keys','pending_contextual_families','latest_pending_contextual_family','latest_contextual_manuscript',
        'latest_completed_family','latest_final_review','coverage_note','reconciled_families'})
    assert fresh['integrated_record_keys']==old['integrated_record_keys']+old['pending_record_keys']
    assert not fresh['pending_record_keys'] and not fresh['pending_contextual_families'] and fresh['latest_pending_contextual_family'] is None
    assert fresh['reconciled_families'][:-1]==old['reconciled_families']
    assert fresh['reconciled_families'][-1]['historical_decisions_newly_completed']=={'revised':2,'retained':11}
    keys=[historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']]
    assert len(keys)==len(set(keys))==5898
    assert set(keys)=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    active,prior=ledger['active_source_prose_drafts'],before['active_source_prose_drafts']
    same_except(prior,active,{'manuscripts','route_record_subsets_pending','status','note'})
    assert active['manuscripts']==prior['manuscripts']
    assert active['route_record_subsets_pending']=={**prior['route_record_subsets_pending'],str(DOC):[]}
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':
            same_except(a,b,{'reviewed_route_records','completed_route_records','next'})
            assert b['reviewed_route_records']==b['completed_route_records']==4299
        elif a['id']==FAMILY:
            same_except(a,b,{'status','pending','completion_credit_added','final_review','new_emulator_runs','new_current_candidate_emulator_runs',
                'new_explicit_source_English_fixture_runs','actual_sampled_B22_display_IDs','offline_only_display_IDs','full_goal_complete'})
            assert b['completion_credit_added']==13 and b['pending'] is None
        else:assert a==b
    same_except(before['formatting_watchlist'],ledger['formatting_watchlist'],{'lil_B178_v4679','lil_B178_v4705'})
    same_except(before['formatting_watchlist']['lil_B178_v4679'],ledger['formatting_watchlist']['lil_B178_v4679'],{'status','registered_release_pending','final_review'})
    scope=ledger['unfinished_editorial_scope_v4705']
    assert scope['canonical_Maria32_pending_uncredited'] and scope['remaining_B179_B180_physical_speeches']==25
    inventory,oldinventory=read(scope['path']),read(before['unfinished_editorial_scope_v4697']['path'])
    same_except(oldinventory,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units','lil_B178_completed_v4705'})
    for a,b in zip(oldinventory['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']=='all-route-scenes':same_except(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
        else:assert a==b
    receipt=read(plan['staged_receipt'])
    assert sha(Path(plan['staged_receipt']).read_bytes())==plan['staged_receipt_sha256']
    for path,digest in receipt['evidence'].items():
        assert sha(Path(path).read_bytes())==digest,path
    assert read(REG)['negative_count']==98
    tests=read('work/analysis/lil_B178_release_tools_v4701/regression_test_results.json')
    assert tests['returncode']==0 and '78 passed' in tests['output']
    assert ledger['current_integrated_candidate']['sha256']==read(RELEASE)['candidate_sha256']==final['candidate_sha256']
    assert read('translations/promoted_build.json')['profile']=='all-routes-unified-v4595'
    for row in plan['files']:
        if Path(row['target']).suffix=='.md':
            oldtext=Path(row['target']).read_text(encoding='utf-8')
            assert Path(row['planned']).read_text(encoding='utf-8').endswith(oldtext.split('\n',1)[1])
    save(output,dict(all_six_before_and_planned_hashes_verified=True,all_prior_root_and_nested_history_preserved=True,
        source_prose_credit_unchanged_completion_adds_ten_once=True,all5898_completed_record_keys_unique=True,
        historical_count_delta=dict(revised=2,retained=11),full_goal_active=True,promoted_main_V4595_unchanged=True,
        current_metadata_not_mutated=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All staged B178 completion values independently validated before writes;ten completions only,full history/objective/main preserved.')
