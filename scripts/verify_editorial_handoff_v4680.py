"""Deep-audit all pending-review metadata/history before applying B178 credit."""
import argparse
from collections import Counter
import os
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B178_v4679 import ROOT as CHECKPOINT,DOC,APPROVAL,FAMILY,PRIOR
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4680')


def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    assert not ROOT.exists()
    plan=read(CHECKPOINT/'mutation_plan.json');receipt=read(CHECKPOINT/'staged_receipt.json')
    assert len(plan)==6 and len({r['target'] for r in plan})==6
    lp=Path('translations/editorial_review_current_v1.json')
    for r in plan:
        target,planned=Path(r['target']),Path(r['planned'])
        assert target.is_relative_to(Path.cwd()) and planned.is_relative_to(CHECKPOINT.resolve())
        assert sha(target.read_bytes())==r['before_sha256'] and sha(planned.read_bytes())==r['planned_sha256']
        assert (CHECKPOINT/(target.name+'.before')).read_bytes()==target.read_bytes()
    entry=next(r for r in plan if Path(r['target'])==lp.resolve());before=read(lp);ledger=read(entry['planned'])
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    assert Path(entry['planned']).read_bytes()==encode_ledger(ledger) and Path(entry['planned']).stat().st_size<100*1024*1024
    same_except(before,ledger,{'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4679','lil_B178_scope_reconciliation_v4679','latest_checkpoint'})
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated',
        'retained_wordings_editorially_completed'])==(5885,5901,3738,2147)
    assert ledger['records_with_source_prose_drafts']==5901 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert ledger['source_prose_reviewed_counts_by_file']=={**before['source_prose_reviewed_counts_by_file'],'/data/SC2.DK4':4045}
    doc,approval=read(DOC),read(APPROVAL);rows=doc['records'];validate_natural_dialogue_batch(doc)
    assert len(rows)==13 and Counter(r['editorial_decision'] for r in rows)=={'revise':2,'retain-wording':11}
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())} and not doc['formatting_review_pending']
    selected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];ids=[r['id'] for r in rows]
    old,fresh=before['contextual_story_natural_dialogue_pass_v1871'],ledger['contextual_story_natural_dialogue_pass_v1871']
    same_except(old,fresh,{'record_keys','record_IDs','fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release','pending_record_keys','pending_contextual_families','latest_pending_contextual_family',
        'latest_contextual_manuscript','coverage_note'})
    assert fresh['record_keys']==old['record_keys']+selected and fresh['record_IDs']==old['record_IDs']+ids
    assert len({historical_key(r) for r in fresh['record_keys']})==5898 and fresh['pending_record_keys']==selected
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release'])==(5898,5885,13)
    assert fresh['integrated_record_keys']==old['integrated_record_keys'] and fresh['latest_pending_contextual_family']==FAMILY
    pending=fresh['pending_contextual_families'];assert len(pending)==1 and pending[0]['records']==13 and pending[0]['proposed_revisions']==2 and pending[0]['retentions']==11
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={**before['reviewed_but_incomplete_route_record_IDs'],'/data/SC2.DK4':ids}
    a,b=before['active_source_prose_drafts'],ledger['active_source_prose_drafts']
    same_except(a,b,{'manuscripts','route_record_subsets_pending','status','note'})
    assert b['manuscripts']==a['manuscripts']+[str(DOC)] and b['route_record_subsets_pending']=={**a['route_record_subsets_pending'],str(DOC):ids}
    assert len(ledger['coverage_units'])==len(before['coverage_units'])+1
    for a,b in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if a['id']=='all-route-scenes':
            same_except(a,b,{'reviewed_route_records','completed_route_records','next'})
            assert (b['reviewed_route_records'],b['completed_route_records'])==(4299,4286)
        else:assert a==b
    assert ledger['coverage_units'][-1]=={**pending[0],'status':doc['status'],'full_goal_complete':False}
    same_except(before['formatting_watchlist'],ledger['formatting_watchlist'],{'lil_B178_v4679'})
    scope=ledger['unfinished_editorial_scope_v4679'];inventory=read(scope['path']);oldinventory=read(before['unfinished_editorial_scope_v4659']['path'])
    assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['incomplete_route_source_prose']==13 and scope['remaining_B179_B180_physical_speeches']==25
    same_except(oldinventory,inventory,{'incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units',
        'B178_fresh_context_review_checkpoint_v4679','remaining_B179_B180_unreviewed_uncredited','earlier_B178_uncredited_leads_are_historical_after_V4679'})
    for a,b in zip(oldinventory['broader_coverage_units'],inventory['broader_coverage_units'],strict=True):
        if a['id']=='all-route-scenes':same_except(a,b,{'reviewed_route_records','completed_route_records','source_prose_pending_records','source_prose_pending_family','next'})
        else:assert a==b
    assert inventory['incomplete_route_source_prose_count']==13 and inventory['B178_fresh_context_review_checkpoint_v4679']==pending[0]
    for p,h in {**receipt['evidence'],**receipt['preserved_release_files']}.items():assert sha(Path(p).read_bytes())==h,p
    native=read(doc['native_font_proof'])
    assert len(native['cases'])==13 and native['current_original_macro_alignment_calls']==104
    assert (native['progressive_planes'],native['FE_planes'])==(12,1)
    assert len(native['review_sheets'])==2 and all(s['viewed_in_full_current_turn'] for s in native['review_sheets'])
    for key,count in [('source_bound_formatter_negatives',28),('source_consumer_negative_controls',20),('source_macro_preservation_negatives',3)]:
        assert len(native[key])==count and all(r['rejected'] for r in native[key])
    blocks=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[178] for p in ['work/clean.nds',doc['current_ROM']]]
    for row in rows:
        for block,ref,value in zip(blocks,[row['source_reference'],row['current_reference']],[row['source_hex'],row['current_hex']],strict=True):
            at=ref['offset'];raw=bytes.fromhex(value)
            assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0 and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert all(row['review'].values()) and row['source_meaning']==row['fresh_source_gloss']
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    for r in plan:
        if Path(r['target']).suffix=='.md':assert Path(r['planned']).read_text(encoding='utf-8').endswith(Path(r['target']).read_text(encoding='utf-8').split('\n',1)[1])
    ROOT.mkdir(parents=True)
    save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,all_prior_root_nested_history_and_objective_preserved=True,
        all13_source_current_native_and11_retention_references_bound=True,new_source_prose_reviews=13,new_completed_records=0,
        current_metadata_not_mutated=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if args.apply:
        for r in plan:
            assert sha(Path(r['target']).read_bytes())==r['before_sha256'] and sha(Path(r['planned']).read_bytes())==r['planned_sha256']
        for r in plan:
            data=Path(r['planned']).read_bytes()
            with Path(r['target']).open('r+b') as stream:
                stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['planned_sha256']
        assert all(sha(Path(p).read_bytes())==h for p,h in receipt['preserved_release_files'].items())
        receipt.update(ledger_sha256=sha(lp.read_bytes()),updated_files={str(Path(r['target']).relative_to(Path.cwd())):r['planned_sha256'] for r in plan})
        save(CHECKPOINT/'checkpoint_receipt.json',receipt)
        save(ROOT/'verified_handoff.json',dict(checkpoint='V4679',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5898,integrated=5885,pending=13,
            source_prose=5901,revised=3738,retained=2147,all_prior_root_nested_history_and_full_objective_preserved=True,
            all13_source_current_native_and11_retention_references_verified=True,native_alignment_cases=104,native_negatives=51,
            main_V4595_and_latest_experimental_V4655_preserved=True,all_jobs_terminal=True,full_goal_active=True,full_goal_complete=False,
            producer_sha256=sha(Path(__file__).read_bytes())))
        print('V4679 applied after independent deep audit:5898 reread/5885 completed/13 pending;5901 source/prose. No completion credit;full goal active.')
    else:print('Deep pending-review audit passed;no metadata written. Reuse audit evidence before a separate apply successor.')
