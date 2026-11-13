"""Independently validate exact source/current/integrated references and ledger delta."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_lil_B180_v4826 import ROOT,DOC,FINAL,FAMILY,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG,PRIOR,B181
from scripts.verify_village_wrap_v608 import read,save

def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}

def audit(before,ledger):
    allowed={'completed_editorial_families','records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts',
        'records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file',
        'source_prose_reviewed_counts_by_file','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units',
        'formatting_watchlist','current_integrated_candidate','unfinished_editorial_scope_v4826','lil_B180_completion_v4826','latest_checkpoint'}
    same_except(before,ledger,allowed)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    family=ledger['completed_editorial_families'][-1];final,doc=read(FINAL),read(DOC);rows=family['records']
    assert family['id']==FAMILY and rows==final['records'] and len(rows)==11
    assert (family['revised_count'],family['retained_count'],final['revised'],final['retained'])==(5,6,5,6)
    assert final['source_prose_and_completion_credit_added_once']==11 and final['previous_B180_objects_uncredited']
    assert [r['english'] for r in rows]==[r['english'] for r in doc['records']]
    all_rows=[r for f in ledger['completed_editorial_families'] for r in f['records']];keys=[historical_key(r) for r in all_rows]
    assert len(keys)==len(set(keys))==5923
    def decision(r):
        v=r.get('historical_editorial_decision') or r.get('decision') or r.get('editorial_decision')
        assert isinstance(v,str) and v.startswith(('revis','retain'));return 'revise' if v.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in all_rows)=={'revise':3753,'retain':2170}
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5923,5926,5926,3753,2170)
    for field in ['source_prose_reviewed_counts_by_file','completed_editorial_record_counts_by_file']:
        assert ledger[field]=={**before[field],'/data/SC2.DK4':4070}
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==5923
    fresh,old=[d['contextual_story_natural_dialogue_pass_v1871'] for d in [ledger,before]]
    fresh_allowed={'record_keys','integrated_record_keys','record_IDs','fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note','reconciled_families'}
    same_except(old,fresh,fresh_allowed)
    selected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    for field in ['record_keys','integrated_record_keys']:assert fresh[field]==old[field]+selected
    assert fresh['record_IDs']==old['record_IDs']+[r['id'] for r in rows]
    assert fresh['reconciled_families'][:-1]==old['reconciled_families']
    assert fresh['reconciled_families'][-1]['new_completed_records']==11
    assert fresh['reconciled_families'][-1]['historical_decisions_newly_completed']==dict(revised=5,retained=6)
    assert not fresh['pending_record_keys'] and not fresh['pending_contextual_families']
    assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==5923
    assert set(keys)=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    active,prior=[d['active_source_prose_drafts'] for d in [ledger,before]]
    same_except(prior,active,{'manuscripts','route_record_subsets_pending','note'})
    assert active['manuscripts']==prior['manuscripts']+[str(DOC)]
    assert active['route_record_subsets_pending']=={**prior['route_record_subsets_pending'],str(DOC):[]}
    assert sum(map(len,active['route_record_subsets_pending'].values()))==0 and active['native_message_IDs']==[750,751,752]
    assert len(ledger['coverage_units'])==len(before['coverage_units'])+1
    for a,b in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if a['id']=='all-route-scenes':
            same_except(a,b,{'reviewed_route_records','completed_route_records','next'})
            assert b['reviewed_route_records']==b['completed_route_records']==4324
        else:assert a==b
    assert ledger['coverage_units'][-1]['id']==FAMILY and ledger['coverage_units'][-1]['completion_credit_added']==11
    same_except(before['formatting_watchlist'],ledger['formatting_watchlist'],{'lil_B180_v4826'})
    scope=ledger['unfinished_editorial_scope_v4826'];assert scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0
    assert scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open'] and scope['next_B181_physical_speeches_uncredited']==10
    inventory,oldinv=read(scope['path']),read(before['unfinished_editorial_scope_v4753']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    same_except(oldinv,inventory,{'next_focus','broader_coverage_units','historical_B180_remaining_scope_before_v4826',
        'remaining_B180_unreviewed_uncredited','lil_B180_completed_v4826','next_B181_clean_context_v4831'})
    assert inventory['historical_B180_remaining_scope_before_v4826']==oldinv['remaining_B180_unreviewed_uncredited']
    assert inventory['remaining_B180_unreviewed_uncredited']['physical_speeches']==0
    for a,b in zip(oldinv['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']=='all-route-scenes':same_except(a,b,{'reviewed_route_records','completed_route_records','next'})
        else:assert a==b
    lead=read(B181);assert len(lead['records'])==10 and lead['new_review_credit']==0 and lead['read_no_predecessor_English']
    assert not {('/data/SC2.DK4','DK4_MES_B181_R'+str(r['source_record_index']).zfill(4)) for r in lead['records']}&set(keys)
    release,start,view,actual,transitions,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all562_manifest_batches_and114_accepted_layers_present']
    assert start['paired_frame_count']==31 and start['all_current_requested_and_final_framebuffers_equal_V4766']
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and view['viewed']
    assert sha(Path(view['sheet']).read_bytes())==view['sha256']==start['review_sheet_sha256']
    assert reg['negative_count']==52 and reg['all_negatives_reject_before_mutation']
    tests=read('work/analysis/lil_B180_release_tools_v4822/regression_test_results.json');assert tests['returncode']==0 and '78 passed' in tests['output']
    rom=Path(release['candidate']);assert sha(rom.read_bytes())==release['candidate_sha256']==start['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert rom.read_bytes()==Path('out/lil_B180_reference_v4801_RESEARCH_ONLY.nds').read_bytes()==Path(release['exact_patch_reconstruction']).read_bytes()
    manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==562 and len(registry['accepted_layers'])==114 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('translations/promoted_build.json')['profile']=='all-routes-unified-v4701'
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    target=IlnkContainer.parse(NdsImage.open(rom).read_file('/data/SC2.DK4')).blocks[180]
    japanese=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[180]
    predecessor=IlnkContainer.parse(NdsImage.open(doc['current_ROM']).read_file('/data/SC2.DK4')).blocks[180]
    original={r['id']:r for r in doc['records']};mapping=read(doc['reference_map']);refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    for r in rows:
        old=original[r['id']];ref=refs[r['id']]
        assert r['english']==old['english'] and all(r['review'].values()) and r['source_meaning']==r['fresh_source_gloss']
        h=r['historical_source_prose_predecessor_fields']
        for data,loc,value in [(japanese,r['source_reference'],r['source_hex']),(predecessor,h['current_reference'],h['current_hex']),(target,r['integrated_reference'],r['integrated_hex'])]:
            at=loc['offset'];raw=bytes.fromhex(value);assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert r['integrated_reference']['offset']==ref['new_offset'] and r['integrated_reference']['record_index']==target[:ref['new_offset']].count(b'\0')
        assert r['actual_B22_display_fixture_observed'] and not r['offline_only_complete_native_display_verified'] and not r['actual_source_event180_selected']
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    assert Counter(r['kind'] for r in rows)=={'progressive':10,'system-FE':1}
    assert actual['complete_matching_observations']==11 and not actual['failures'] and not actual['paired_region_differences']
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[31,26]
    assert transitions['nontext_equal_samples']==115 and transitions['measured_persistent_town_difference_resolved_to_original_effect']
    assert transitions['PRNG_equality'] is False and transitions['postscene9001_PRNG_seeds']==[2467799992,790984746]
    assert transitions['postscene9001_native_component_equality']['persistent_objects'] is False
    effect=read(transitions['effect_boundary_proof']);assert effect['final9001_four_array_differences']['all90_towns']==[dict(offset=1294,before=59,after=61)]
    assert effect['no_unresolved_translation_specific_state_difference_within_checked_arrays']
    assert before['lil_B180_contextual_references_v4817']['source_prose_or_completion_credit_added']==0

if __name__=='__main__':
    output=ROOT/'independent_preapplication_audit.json';assert not output.exists()
    plan=read(ROOT/'staged_completion.json');assert len(plan['files'])==6;workspace=Path.cwd().resolve()
    lp=Path('translations/editorial_review_current_v1.json')
    for r in plan['files']:
        p,s=Path(r['target']),Path(r['planned']);assert p.is_relative_to(workspace) and s.is_relative_to(ROOT.resolve())
        assert sha(p.read_bytes())==r['before_sha256'] and sha(s.read_bytes())==r['planned_sha256']
    row=next(r for r in plan['files'] if Path(r['target'])==lp.resolve());before=read(lp);ledger=read(row['planned'])
    assert lp.read_bytes()==(ROOT/(lp.name+'.before')).read_bytes()
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    assert Path(row['planned']).read_bytes()==encode_ledger(ledger) and Path(row['planned']).stat().st_size<100*1024*1024
    audit(before,ledger)
    receipt=read(plan['staged_receipt']);assert sha(Path(plan['staged_receipt']).read_bytes())==plan['staged_receipt_sha256']
    for p,h in receipt['evidence'].items():assert sha(Path(p).read_bytes())==h
    for r in plan['files']:
        if Path(r['target']).suffix=='.md':assert Path(r['planned']).read_text(encoding='utf-8').endswith(Path(r['target']).read_text(encoding='utf-8').split('\n',1)[1])
    save(output,dict(all_six_before_and_planned_hashes_verified=True,all_prior_root_and_nested_history_preserved=True,
        source_prose_and_completion_adds11_once=True,all5923_completed_keys_unique=True,full_goal_active=True,
        staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All staged B180 completion changes audited:11 source/prose+11 completions once;5923 unique completed keys,full history and scope preserved.')
