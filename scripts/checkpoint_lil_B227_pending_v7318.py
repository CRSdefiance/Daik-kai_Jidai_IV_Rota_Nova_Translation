"""Six-target sealed-decision checkpoint; preserve every prior record andcounter exactly."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B227_final_paths_v7315 import *
from scripts.lil_B227_pending_text_v7318 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B227_pending_checkpoint_v7318');VERIFY=Path('work/analysis/editorial_handoff_verification_v7319');LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7284/verified_handoff.json')
KEY='lil_B227_review_pending_v7318';SCOPE='unfinished_editorial_scope_v7318';COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];VALUES=(6700,6703,6703,4192,2508)
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def gates():
    prior=read(PRIOR);ledger=read(LEDGER);current=ledger['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(current['manifest'])
    assert current['sha256']==prior['candidate_sha256']==sha(Path(current['path']).read_bytes())=='6297529d4e1a4b51be95f2f8a9634cba0142f8a5682b5d8d1416905e42521259'
    assert current['profile']==manifest['profile']=='all-routes-unified-v7277' and len(manifest['batches'])==619 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    doc,seal,mapping,font,policy,stored,actual,later=map(read,[SEALED,SEAL,MAP,FONT,POLICY,STORED,ACTUAL,LATER])
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes()) and seal['all9_five_gates_andexact_references_approved'] and seal['research_ROM_sha256']==sha(ROM.read_bytes()) and doc['current_ROM_sha256']==current['sha256']
    assert len(doc['records'])==9 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':7,'retain-wording':2} and all(all(r['review'].values()) for r in doc['records']) and doc['registered_integration_pending']
    assert font['complete_native_pages']==9 and font['logical_compiled_input_alignment_cases']==72 and stored['stored_alignment_cases']==36 and stored['fresh_alignment_cases']==20 and stored['exact_reused_alignment_cases']==16 and stored['zero_ink_parity_tail_count']==5
    assert policy['positive_paragraph_count']==9 and policy['negative_count']==len(policy['negative_cases'])==50 and all(r['rejected'] for r in policy['negative_cases']) and len(policy['row_count_reasons'])==2
    assert actual['actual_unique_speeches']==actual['actual_native_pages']==9 and actual['actual_complete_body_holds']==actual['actual_complete_name_holds']==35 and not actual['incomplete_sampled_body_holds'] and actual['all22_commands_observed'] and actual['all_jobs_terminal_and_reaped'] and not read(VIEW)['visual_review_pending']
    assert (len(actual['command_comparison_differences']),len(actual['command_duration_changes']),len(later['later_sampled_RGB_differences']),later['total_later_sampled_frames'])==(11,4,120,183) and later['captain_IDs']==[2,2] and later['final_PRNG_seeds']==[2971698614,2367937388]
    assert mapping['observed_comparison_contract']==seal['observed_comparison_contract'] and read(CONTROL)['original_normal_end702_four_bytes_andtarget_tail2_preserved']
    for p,h in read('translations/lil_B227_native_contract_v1.json')['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    return prior,doc
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,doc=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);rows=deepcopy(doc['records']);oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows};assert len(oldkeys)==6700 and len(keys)==9 and not oldkeys&keys;ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        summary=DETAILS+'\n\n'+NEXT;scope=old['unfinished_editorial_scope_v7283'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory['Lil_B227_pending_v7318']=dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),pending_objects=9,uncredited_revisions=7,uncredited_retentions=2,all9_five_individual_gates_source_native_stored_actual_reference_complete=True,registered_atomic_build_patch_startup_pending=True,source668_target708_logical706_targettail2_fullinverse=True,three_A000_controls_preserved=True,one_exact_R15_phrasal_verb_warning_andtwo_row_reasons_preserved=True,all_measured_late_differences_preserved=True,new_credit=0,full_goal_complete=False)
        inventory['next_Lil_B227_source_only_gloss_complete']['superseded_by_sealed_pending_review']=dict(manuscript=str(SEALED),all_historical_pending_flags_preserved=True,new_credit=0)
        inventory['later_B227_technical_reaudit_v7318']=dict(actual=str(ACTUAL),later=str(LATER),all11_command4_duration120of183_RGB_andcalendar_PRNG_differences_preserved=True,seal_preflight_only_two_independently_measured_seed_replacements_all_other_high_native_integers_exact=True,incidental_B120_Sailor_hunger_no_new_review_credit=True,no_full_RAM_future_orbroad_causal_equivalence_claim=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,B2279_sealed_decisions_uncredited_until_final_registered_release=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
        put(['formatting_watchlist','lil_B227_v7318'],dict(status='sealed-native-stored-actual-reference-pending-atomic-registered-release',manuscript=str(SEALED),native_proof=str(FONT),all9_original_single_four_row_pages72logical36stored=True,actual9pages35body35headers=True,one_exact_R15_step_in_comma_warning_preserved=True,two_row_reasons_all_base_QA_preserved=True,source_names_full207_andall_earlier_wrapping_scope_preserved=True,no_new_credit=True));put(['latest_checkpoint'],summary)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5100;put(['coverage_units',ri,'next'],NEXT)
        paths=[SEALED,MAP,SEAL,APPROVED,APPROVAL,PRIOR,inv,ROM,*map(Path,proof_paths().values()),Path(doc['source_context']),Path(doc['whole_exchange_clean_context']),Path(doc['source_visual_review']),Path('scripts/lil_B227_final_paths_v7315.py'),Path('scripts/lil_B227_pending_text_v7318.py'),Path('work/analysis/lil_B227_seal_tools_v7317b/source_locked_reference_seal.json'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),records=rows,record_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows],source_reviewed_decisions=9,uncredited_revisions=7,uncredited_justified_retentions=2,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,all9_five_gates_true_atomic_registered_release_patch_startup_pending=True,current_ROM_families_andall_five_credit_counters_unchanged=True,source_names_andall_late_measurements_andfull_prior_objective_preserved=True,summary=summary,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_executed_capture_jobs_terminal_andreaped=True,full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and tuple(new[k] for k in COUNTERS)==VALUES
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7318: B227 sealed pending registered integration; V7277 current\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7318; V7277 current, B227 sealed pending\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            dest=ROOT/f'{i:02d}.after';dest.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(dest.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,zero_credit=True,full_goal_complete=False));print('B227 sealed checkpoint staged:nine pending decisions,zero credits,V7277 unchanged;deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_all_prior_roots_nested_records_history_andcounters=True,all_six_before_andplanned_hashes_verified=True,zero_credit=True,full_goal_complete=False));print('B227 checkpoint deep inverse passes;every prior root,record,family,counter andROM reference restores exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_before_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False));print('Six B227 pending targets applied exactly;V7277 andall completed counts unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],profile=prior['profile'],ARM9_sha256=prior['ARM9_sha256'],all_previous_roots_nested_history_families_ROM_refs_andcounters_restore_exactly=True,completed=6700,source_prose=6703,revised=4192,retained=2508,SC2=4814,SC3=96,reviewed_routes=5100,completed_routes=5100,all619_manifest_batches114_accepted18_checks_and110_verified_regressions_preserved=True,B227_pending_objects=9,B227_uncredited_revisions=7,B227_uncredited_retentions=2,new_credit=0,all9_sealed_native_stored_actual_reference_gates_pass=True,actual_source9pages35body35headers_English9pages35body35headers=True,all_three_A000_normal_end_andtarget_tail2_preserved=True,one_exact_R15_phrasal_verb_warning_two_row_reasons_andall_base_QA_preserved=True,all_late_differences_full_name_andretrospective_wrap_scope_preserved=True,current_native_input=prior['current_native_input'],current_native_input_sha256=prior['current_native_input_sha256'],main_V4701_preserved=True,all_capture_jobs_terminal_andreaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7318 verified:nine sealed B227 decisions pending registered integration;zero credit.V7277/6700 completed remain;full goal active.')
