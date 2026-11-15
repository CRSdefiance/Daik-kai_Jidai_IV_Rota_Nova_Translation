"""Record28 uncredited prose drafts and source-context name proposals without losing history."""
import argparse,gzip,json,os
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B206_source_checkpoint_text_v6255 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B206_source_prose_checkpoint_v6255');VERIFY=Path('work/analysis/editorial_handoff_verification_v6256')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v6226/verified_handoff.json')
DOC=Path('translations/lil_B206_editorial_manuscript_v1.json');APP=Path('work/analysis/lil_B206_prose_v6253/twenty_eight_uncredited_whole_exchange_prose_decisions.json');VIEW=Path('work/analysis/lil_B206_source_view_v6248/all24_source_speeches_four_labels_and_three_returns_viewed.json');NAMES=Path('translations/earring_speaker_names_editorial_proposal_v1.json');ACTUAL=Path('work/analysis/lil_B206_source_paths_v6247/three_actual_source_paths_all24_speeches_four_labels_all51_commands_and_returns.json')
KEY='Lil_B206_source_prose_review_v6255';SCOPE='unfinished_editorial_scope_v6255'
def inverse(d):
    d=deepcopy(d);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d
def gates():
    v,doc,a,view,names,actual=map(read,[PRIOR,DOC,APP,VIEW,NAMES,ACTUAL])
    for k in ['candidate','patch']:assert sha(Path(v[k]).read_bytes())==v[k+'_sha256']
    assert doc['current_ROM_sha256']==names['current_ROM_sha256']==v['candidate_sha256'] and a['manuscript_sha256']==sha(DOC.read_bytes()) and a['all28_have_four_prose_gates_true_formatting_false']
    assert len(doc['records'])==28 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':16,'retain-wording':12} and doc['formatting_review_pending']
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records'])==3 and names['proposed_name173_change']=='Suspicious Person -> Shady Man' and names['source_seller_direct_speeches_read']==112 and names['complete_seller_context_speeches_read']==195
    assert names['existing_Christina_references_pending_individual_reconciliation']==88 and names['current_Cristina_references_also_require_consistency_review']==23 and names['no_claim_of_completed_Cristina_consumer_reconciliation_or_all207_name_closure']
    assert view['all24_clean_source_speeches_and_four_typed_choice_labels_viewed'] and len(view['viewed_sheets'])==8 and actual['source_distinct_speech_observations']==24 and actual['actual_distinct_choice_labels']==4 and actual['total_frames']==48003
    for s in view['viewed_sheets']:assert s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256']
    notice=view['additional_whole_frame_acquisition_capture'];assert notice['viewed_after_image_return'] and sha(Path(notice['path']).read_bytes())==notice['PNG_sha256']
    for tag,version in [('buy',6243),('high_price',6245),('pitch_refusal',6246)]:
        run=Path(f'work/analysis/lil_B206_source_run_v{version}_{tag}');terminal=read(run/'terminal.json');assert terminal['terminal'] and terminal['observer_host_slots_restored']
    for source in [APP,VIEW,NAMES,ACTUAL]:
        for p,h in read(source).get('evidence',{}).items():assert sha(Path(p).read_bytes())==h
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return v,doc
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();v,doc=gates();before=LEDGER.read_bytes();assert sha(before)==v['ledger_sha256'];old=json.loads(before);new=deepcopy(old);assert KEY not in new and SCOPE not in new
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,compresslevel=9,mtime=0));scope=deepcopy(read(old['unfinished_editorial_scope_v6225']['path']));scope['next_focus']=NEXT
        scope['Lil_B206_source_prose_approved_uncredited_v6255']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),prose_receipt=str(APP),prose_receipt_sha256=sha(APP.read_bytes()),objects=28,speeches=24,typed_choice_labels=4,revised=16,retained=12,four_prose_gates_true_formatting_false=True,actual_source24_speeches4_labels51_commands_observed_over_three_paths=True,English_native_name_assets_relocation_actual_and_registered_release_pending=True,new_completion_credit=0)
        scope['speaker173_and_Cristina_contextual_name_decisions_v6249']=dict(proposal=str(NAMES),proposal_sha256=sha(NAMES.read_bytes()),proposed173='Shady Man',retained_working7='Cristina Erneco',seller_complete_exchanges_read=8,seller_context_speeches_read=195,old_Christina_spelling_speech_records_pending=88,current_Cristina_spelling_speech_records_for_consistency_review=23,other27_stored_name_exchanges_not_newly_claimed_fully_read=True,all207_and_other_consumers_remain_open=True,no_asset_or_name_completion_credit=True)
        scope['B206_initialized_source_cash_scope_v6248']=dict(source_view=str(VIEW),source_view_sha256=sha(VIEW.read_bytes()),source_asking_price=9000,observed_final_cash_each_path=34900,natural_outer_payment_semantics_unproved=True,no_free_item_or_original_bug_claim=True,retain_for_source_English_comparison_and_later_technical_reaudit=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
        sp=ROOT/'unfinished_editorial_scope_inventory.json';save(sp,scope);new[SCOPE]=dict(path=str(sp),sha256=sha(sp.read_bytes()),uncredited_B206_prose_approved_objects=28,incomplete_COMMON=3,retrospective207_names_all_four_storylines_and_wider_editorial_scope_preserved=True,full_goal_complete=False)
        paths=[DOC,APP,VIEW,NAMES,ACTUAL,PRIOR,Path('scripts/lil_B206_source_checkpoint_text_v6255.py'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths};new[KEY]=dict(previous_latest_checkpoint=old['latest_checkpoint'],summary=DETAILS,next_focus=NEXT,evidence=evidence,record_IDs=[r['id'] for r in doc['records']],objects=28,revised_drafts=16,retained_drafts=12,new_completion_credit=0,previous_goal_turn_classification='progress',goal_turn_classification='progress',new_source_runs=3,new_source_frames=48003,all_source_jobs_terminal_and_reaped=True,full_goal_complete=False);new['latest_checkpoint']=DETAILS+'\n\n'+NEXT
        targets={LEDGER:encode_ledger(new)};section='## V6255: B206 whole-exchange prose and name proposals;native assets/display/release pending\n\n'+DETAILS+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text('utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6255\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six checkpoint targets staged:28 uncredited prose drafts,exact names/alias queue and source scope;V6220 and all counters remain unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;v,doc=gates()
        assert all(new[k]==old[k] for k in ['current_integrated_candidate','records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_families','active_source_prose_drafts']) and tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6387,6390,3989,2398) and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(deep_inverse_preserves_every_prior_root_and_nested_value=True,staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),all_six_targets_and_source_prose_name_evidence_verified=True,no_duplicate_or_premature_review_credit=True,full_goal_complete=False));print('Six targets audited;deep inverse preserves all history and unchanged6387 completion count.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as f:f.write(Path(e['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all6_audited_targets_applied_exactly=True,all_before_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited checkpoint files applied;all previous values and NTFS compression preserved.')
        else:
            assert read(ROOT/'application_receipt.json')['all6_audited_targets_applied_exactly'] and not VERIFY.exists();VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=v['candidate'],candidate_sha256=v['candidate_sha256'],patch=v['patch'],patch_sha256=v['patch_sha256'],profile=v['profile'],all_prior_root_and_nested_history_preserved=True,B206_source_prose_approved_uncredited_objects=28,B206_revised_drafts=16,B206_retained_drafts=12,source_actual24_speeches4_labels51_commands_and_three_paths_verified=True,new_source_ROMs=1,new_source_cold_boot_runs=3,new_source_frames=48003,source_original_cash_scope_and_no_full_payment_claim_preserved=True,proposed173_Shady_Man_native_assets_and_release_pending=True,working_Cristina_Erneco_retention_and88_old_spelling_record_queue_preserved=True,completed=6387,source_prose=6390,revised=3989,retained=2398,SC2=4501,SC3=96,reviewed_routes=4787,completed_routes=4787,all_sessions_terminal_and_reaped=True,main_V4701_preserved=True,all207_names_all_storylines_shared_town_random_Help_prose_wraps_and_older_leads_preserved=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())));print('V6255 verified:28 uncredited B206 prose drafts and concrete name proposals. V6220,6387 completions,all history and full goal preserved.')
