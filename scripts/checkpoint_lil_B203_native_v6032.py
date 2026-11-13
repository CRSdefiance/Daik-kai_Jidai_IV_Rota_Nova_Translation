"""Preserve all history while registering twenty-two uncredited native-reviewed drafts."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B203_native_checkpoint_text_v6032 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B203_native_checkpoint_v6032')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6033')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6009/verified_handoff.json')
DOC=Path('translations/lil_B203_editorial_manuscript_v4.json')
APPROVAL=Path('work/analysis/lil_B203_native_approval_v6031/all22_source_prose_current_native_approval.json')
KEY='Lil_B203_native_approved_v6032'
SCOPE='unfinished_editorial_scope_v6032'
def inverse(new):
    d=deepcopy(new);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d
def gates():
    prior=read(PRIOR);doc,approval=read(DOC),read(APPROVAL)
    assert approval['all22_five_gates_approved'] and approval['manuscript_sha256']==sha(DOC.read_bytes()) and len(doc['records'])==22 and all(all(r['review'].values()) for r in doc['records'])
    assert len(approval['formatter_negatives'])==28 and approval['source_consumer_negatives']==22 and approval['covered_native_alignment_cases']==176 and approval['all22_objects_uncredited']
    assert doc['source_prose_or_completion_credit_added']==0 and doc['all22_objects_still_uncredited']
    for k in ['candidate','patch']:assert sha(Path(prior[k]).read_bytes())==prior[k+'_sha256']
    for p,h in read('releases/all_routes_unified_v5998/immutable_input_audit.json')['inputs'].items():assert sha(Path(p).read_bytes())==h
    registry=read('translations/release_stack.json');manifest=read(Path(prior['candidate']).with_suffix('.manifest.json'));assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(manifest['batches'])==590 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    move=read('work/analysis/storage_recovery_v5974/verified_dependency_move.json');assert move['Files']==1964 and move['Bytes']==211810825 and move['EveryFileHashPreserved'] and move['OriginalPathIsJunction'] and move['ROMsOrTranslationsDeleted']==0
    return prior,doc,approval
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();prior,doc,approval=gates();before=LEDGER.read_bytes();assert sha(before)==prior['ledger_sha256'];old=json.loads(before);new=deepcopy(old);assert KEY not in new and SCOPE not in new
        summary=DETAILS+'\n\n'+NEXT;inventory=deepcopy(read(old['unfinished_editorial_scope_v6008']['path']));inventory['next_focus']=NEXT;inventory['historical_B203_clean_only_before_v6032']=inventory.pop('Lil_B203_clean_only_uncredited_v6008')
        inventory['Lil_B203_native_review_v6032']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_approval=str(APPROVAL),native_approval_sha256=sha(APPROVAL.read_bytes()),reviewed_uncredited_objects=22,revisions=9,individually_justified_retentions=13,native_covered_alignments=176,source_consumer_negatives=22,formatter_negatives=28,actual_source_speeches=22,source_boots=1,source_frames=13001,actual_English_scene_relocation_references_and_registered_release_pending=True)
        inventory['B203_names_and_unspoken_item_title_context_v6032']=dict(proof=doc['contextual_reconciliation'],source_defined_Mysterious_Old_Man_retained_no_doctor_or_nationality_invented=True,Mikhail_full_middle_name_and_progressive_omission_preserved=True,item18_card_bound_without_inserting_an_unspoken_title=True,no_global_name_or_item_widget_completion_credit=True)
        inventory['following_B43_source_item_term_observed_v6032']=dict(file_path='/data/SC2.DK4',block=43,command_offset=12,frame=8410,proof=doc['contextual_reconciliation'],existing_source_item_Local_Product_terminology_lead_still_open=True,new_editorial_credit=0)

        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
        paths=[DOC,APPROVAL,PRIOR,Path('scripts/lil_B203_native_checkpoint_text_v6032.py'),Path(__file__),*[Path(doc[k]) for k in ['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','source_nameplate_consumer_proof','actor_terminology_reconciliation','contextual_reconciliation','actual_original_response_paths','effective_current_comparison','native_font_proof','native_formatter_module','scoped_profile_module']]];evidence={str(p):sha(p.read_bytes()) for p in paths}
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory);new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),B203_uncredited_objects=22,names207_queue_and_all_wider_editorial_scope_preserved=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,previous_latest_checkpoint=old['latest_checkpoint'],evidence=evidence,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),reviewed_uncredited_objects=22,revised=9,retained=13,new_source_prose_reviews=0,new_completed_records=0,new_research_ROMs=1,new_emulator_runs=1,new_frames=13001,all_jobs_terminal_and_reaped=True,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False);new['latest_checkpoint']=summary;assert inverse(new)==old
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V6032: B203 native-reviewed22 objects await integration;V5998 preserved\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            target=Path('docs')/name;text=target.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6032\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[target]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;22 native-reviewed B203 drafts remain uncredited,V5998 unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;prior,doc,approval=gates()
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['records_editorially_completed']==6327 and new['records_with_source_and_prose_pass']==6330 and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_audit.json').exists();save(ROOT/'independent_audit.json',dict(deep_inverse_preserves_all_history=True,all_six_targets_and_immutable_inputs_verified=True,staged_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False));print('Deep inverse,six targets,22 five-gate drafts and immutable inputs audited.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_audit.json')['staged_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,full_goal_complete=False));print('Six audited native checkpoint files applied.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True);result={**prior,'previous_verified_handoff':str(PRIOR),'previous_verified_handoff_sha256':sha(PRIOR.read_bytes()),'ledger_sha256':sha(LEDGER.read_bytes()),'all_prior_history_and_current_candidate_exactly_preserved':True,'latest_checkpoint_key':KEY,'B203_clean_source_glosses':22,'B203_native_approved_uncredited_objects':22,'B203_target_reviews_uncredited':True,'B203_native_approval':str(APPROVAL),'prior_English_B203_speech_unread':False,'B203_contextual_predecessor_comparison_complete':True,'B203_actual_source_speeches':22,'B203_actual_English_speeches':0,'B203_registered_integration_pending':True,'new_source_prose_or_completion_credit':0,'goal_turn_classification':'progress','all_jobs_terminal_and_reaped':True,'evidence':plan['evidence'],'producer_sha256':sha(Path(__file__).read_bytes())};save(VERIFY/'verified_handoff.json',result);print('Verified V6032:B20322 native-approved uncredited drafts,V5998/6327 completed unchanged;full editorial/name goal active.')
