"""Six-target zero-credit checkpoint with exact restoration of all prior history andcounts."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B225_pending_text_v7211 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_pending_checkpoint_v7211');VERIFY=Path('work/analysis/editorial_handoff_verification_v7212');LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7175/verified_handoff.json');DOC=Path('translations/lil_B225_editorial_manuscript_v2b.json')
KEY='lil_B225_review_pending_v7211';SCOPE='unfinished_editorial_scope_v7211';COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];VALUES=(6667,6670,6670,4172,2495)
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def gates():
    prior=read(PRIOR);ledger=read(LEDGER);current=ledger['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(current['manifest'])
    assert current['sha256']==prior['candidate_sha256']==sha(Path(current['path']).read_bytes())=='155e56c02d7b61deaee019785ef6e2c6926349652c8babc45fa12756df4229d5'
    assert current['profile']==manifest['profile']=='all-routes-unified-v7168' and len(manifest['batches'])==617 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    doc=read(DOC);font=read(doc['native_font_proof']);policy=read('work/analysis/lil_B225_policy_validation_v7210/thirteen_positives60_rejections_two_row_reasons_zero_waivers.json');oldactual=read(doc['historical_actual_English_proof']);later=read('work/analysis/lil_B225_later_v7206/following_final_components_and_measured_timing_RNG_RGB_limits.json')
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':8,'retain-wording':5} and len(doc['records'])==13 and all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert font['new_alignment_cases']==4 and font['exact_reused_alignment_cases']==100 and font['complete_native_pages']==14 and policy['positive_paragraph_count']==13 and policy['negative_count']==60 and all(r['rejected'] for r in policy['negative_cases'])
    assert oldactual['actual_native_pages']==14 and oldactual['actual_complete_body_holds']==oldactual['actual_complete_name_holds']==55 and oldactual['all_jobs_terminal_and_reaped'] and later['captain_IDs']==[2,2] and later['final_PRNG_seeds']==[4038666230,2006740429] and later['total_later_sampled_frames']==len(later['later_sampled_RGB_differences'])==163
    assert later['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False)
    return prior,doc
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,doc=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);rows=deepcopy(doc['records']);oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};assert len(oldkeys)==6667 and len({historical_key(r) for r in rows})==13 and not oldkeys&{historical_key(r) for r in rows};ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        summary=DETAILS+'\n\n'+NEXT
        scope=old['unfinished_editorial_scope_v7174'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT;inventory['Lil_B225_pending_v7211']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),pending_objects=13,source_initial_English14_pages55_holds_historical=True,revised_R16_native_opening35_cells_actual_pending=True,source_Sailor_label_not_invented_second_child=True,all_initial_timing_RNG_later_components_and163_RGB_differences_retained=True,new_credit=0,full_goal_complete=False)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,B22513_decisions_uncredited_until_final_registered_release=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
        put(['formatting_watchlist','lil_B225_v7211'],dict(status='pending-final-R16-stored-actual-reference-andregistered-release',manuscript=str(DOC),native_proof=doc['native_font_proof'],source_pages13_initial_English_pages14_source51_English55_complete_holds=True,only_R16_opening24_to35_cells_changed_all13_prose_unchanged=True,all13_formatting_gates_false=True,source_original_Sailor_cast_andcatalogue151_full207_scope_preserved=True,no_new_credit=True))
        put(['latest_checkpoint'],summary)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5067;put(['coverage_units',ri,'next'],NEXT)
        paths=[DOC,PRIOR,inv,Path(doc['native_font_proof']),Path(doc['native_review']),Path(doc['historical_actual_English_proof']),Path(doc['speaker_name_review']),Path(doc['source_context']),Path(doc['whole_exchange_clean_context']),Path('work/analysis/lil_B225_later_v7206/following_final_components_and_measured_timing_RNG_RGB_limits.json'),Path('work/analysis/lil_B225_later_pairs_v7206b/three_actual_later_pairs.json'),Path('work/analysis/lil_B225_policy_validation_v7210/thirteen_positives60_rejections_two_row_reasons_zero_waivers.json'),Path('translations/lil_B225_native_contract_v2.json'),Path('dk4tool/dialogue/lil_B225_profile_v2.py'),Path('dk4tool/dialogue/lil_B225_layout_v2.py'),Path('work/analysis/lil_B225_reference_v7199/research_image_receipt.json'),Path('work/analysis/lil_B225_loader_v7200/whole_SC2_and_B225_initial_entry_proof.json'),Path('work/analysis/lil_B225_reference_census_v7201/all16_commands_no_relative_or_typed_sites_and_shipped_census.json'),Path('scripts/lil_B225_pending_text_v7211.py'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,record_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows],source_reviewed_decisions=13,uncredited_revisions=8,uncredited_justified_retentions=5,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,all13_formatting_gates_false_pending_revised_capture_andrelease=True,initial_English_actual_proof=doc['historical_actual_English_proof'],initial_actual_English55_body55_headers_not_final_R16_proof=True,only_R16_native_wrap_changed_4_fresh100_exact_reused_cases=True,current_ROM_families_andall_five_credit_counters_unchanged=True,source_label_gloss_correction_andall_measured_later_differences_preserved=True,summary=summary,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_executed_capture_jobs_terminal_andreaped=True,full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and tuple(new[k] for k in COUNTERS)==VALUES
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7211: B225 contextual/native review pending final R16 capture andrelease; V7168 current\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7211; V7168 current, B225 pending\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            dest=ROOT/f'{i:02d}.after';dest.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(dest.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,zero_credit=True,full_goal_complete=False));print('B225 checkpoint staged:13 pending decisions,zero credits,V7168 unchanged. Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_all_prior_roots_nested_records_history_andcounters=True,all_six_before_andplanned_hashes_verified=True,zero_credit=True,full_goal_complete=False));print('B225 checkpoint deep inverse passes;every earlier record,family,counter andROM reference restores exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_before_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False));print('Six B225 pending targets applied exactly;V7168 andall completed counts unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],profile=prior['profile'],ARM9_sha256=prior['ARM9_sha256'],all_previous_roots_nested_history_families_ROM_refs_andcounters_restore_exactly=True,completed=6667,source_prose=6670,revised=4172,retained=2495,SC2=4781,SC3=96,reviewed_routes=5067,completed_routes=5067,all617_manifest_batches114_accepted18_checks_and110_verified_regressions_preserved=True,B225_pending_objects=13,B225_uncredited_revisions=8,B225_uncredited_retentions=5,new_credit=0,new_R16_opening35_native_not_final_actual_capture=True,initial_source13_pages51_holds_English14_pages55_holds_preserved=True,all_initial_later_differences_andsource_Sailor_cast_correction_preserved=True,current_native_input=prior['current_native_input'],current_native_input_sha256=prior['current_native_input_sha256'],main_V4701_preserved=True,all_capture_jobs_terminal_andreaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7211 verified:13 B225 decisions pending final R16 stored/actual/release;zero credit. V7168/6667 completed remain;full goal active.')
