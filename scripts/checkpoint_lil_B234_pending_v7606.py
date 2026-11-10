"""Stage, audit, apply and independently verify a zero-credit pending-review checkpoint."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B234_final_paths_v7602 import *
from scripts.lil_B234_pending_text_v7606 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B234_pending_checkpoint_v7606');VERIFY=Path('work/analysis/editorial_handoff_verification_v7607');LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7570/verified_handoff.json')
KEY='lil_B234_review_pending_v7606';SCOPE='unfinished_editorial_scope_v7606'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];VALUES=(6783,6786,6786,4237,2546)
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def gates():
    prior,ledger=map(read,[PRIOR,LEDGER]);current=ledger['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(current['manifest'])
    assert current['sha256']==prior['candidate_sha256']==sha(Path(current['path']).read_bytes()) and current['profile']==manifest['profile']=='all-routes-unified-v7563'
    assert len(manifest['batches'])==625 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    doc,seal,mapping,font,policy,stored,a,l=map(read,[SEALED,SEAL,MAP,FONT,POLICY,STORED,ACTUAL,LATER])
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes()) and seal['all18_five_gates_andexact_references_approved'] and seal['research_ROM_sha256']==sha(ROM.read_bytes()) and doc['current_ROM_sha256']==current['sha256']
    assert len(doc['records'])==18 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':14,'retain-wording':4} and all(all(r['review'].values()) for r in doc['records']) and doc['registered_integration_pending']
    assert (font['complete_native_pages'],font['logical_compiled_input_alignment_cases'],stored['stored_alignment_cases'],stored['fresh_alignment_cases'],stored['exact_reused_alignment_cases'],stored['zero_ink_parity_tail_count'])==(18,144,72,28,44,7)
    assert policy['positive_paragraph_count']==18 and policy['negative_count']==len(policy['negative_cases'])==83 and all(r['rejected'] for r in policy['negative_cases']) and len(policy['row_count_reasons'])==8 and policy['all_base_QA_diagnostics_preserved_one_exact_R33_line1_article_classification']
    warned=[r for r in doc['records'] if r['exact_reviewed_base_warnings']]
    assert len(warned)==1 and warned[0]['source_record_index']==33 and warned[0]['exact_reviewed_base_warnings']==[dict(severity='warning',code='weak-line-ending',message="line 1 ends with weak wrap word 'the'")] and sum(bool(r['row_count_reason']) for r in doc['records'])==8
    assert a['actual_unique_speeches']==a['actual_native_pages']==18 and a['actual_complete_body_holds']==a['actual_complete_name_holds']==71 and not a['incomplete_sampled_body_holds'] and a['all29_commands_observed'] and a['all_jobs_terminal_and_reaped'] and not read(VIEW)['visual_review_pending']
    assert (len(a['command_comparison_differences']),len(a['command_duration_changes']),len(l['later_sampled_RGB_differences']),l['total_later_sampled_frames'])==(18,8,0,147)
    assert mapping['observed_comparison_contract']==seal['observed_comparison_contract'] and read(CONTROL)['original_normal_end1528_four_bytes_andtarget_zero_storage_tail_preserved']
    assert [(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in read(ENTRY)['selected_B234_source_events']]==[(234,234,235,[],[])]
    n=read(NAMES);assert n['both_null_middle_fields_andsame_text_full_getters_preserved'] and n['both_actual_final_English_personal_androle_headers_complete'] and n['full_catalogue_UI_unvisited'] and n['spoken_alias']['English']=='Filippo'
    assert {(r['actor_ID'],r['english'],r['catalogue_current']) for r in n['records']}=={(19,'Carlo Sinat','Carlo Sinat'),(104,'Trader','Trader')}
    item=read(ITEM);r=item['source_named_item'];assert (r['record_ID'],r['Japanese'],r['English'],r['current_storage_kind'])==('DK4_ITEM_POINTER_106','グレゴリウスの冠',"Gregory's Crown",'static-current-ARM9')
    region=item['actor104_regional_secondary_storage_contract'];assert (region['current_pointer'],region['current_deployed_payload_offset'],region['current_physical_ARM9_storage_offset'])==(37256672,960,1518924)
    np=read(NAMEPROOF);assert (np['name_literal_alignment_count'],np['fresh_native_name_font_alignment_cases'],np['exact_reused_native_name_font_alignment_cases'],np['complete_name_component_plane_count'])==(20,8,12,5)
    for p,h in read('translations/lil_B234_native_contract_v1.json')['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    return prior,doc
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,doc=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);rows=deepcopy(doc['records']);oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows};assert len(oldkeys)==6783 and len(keys)==18 and not oldkeys&keys;ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        summary=DETAILS+'\n\n'+NEXT;scope=old['unfinished_editorial_scope_v7569'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory['Lil_B234_pending_v7606']=dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),pending_objects=18,uncredited_revisions=14,uncredited_retentions=4,all18_five_individual_source_native_stored_actual_reference_gates_complete=True,registered_atomic_build_patch_startup_pending=True,source1468_logical1468_tail0_target1532_logical1532_tail0_full_inverse=True,eight_row_reasons_one_exact_R33_line1_article_warning=True,new_credit=0,full_goal_complete=False)
        inventory['B234_item106_role_alias_regional_offset_scope_v7578']=dict(proof=str(ITEM),sha256=sha(ITEM.read_bytes()),names=str(NAMES),source_named_item=deepcopy(read(ITEM)['source_named_item']),regional_storage_contract=deepcopy(read(ITEM)['actor104_regional_secondary_storage_contract']),no_new_asset_getter_card_mechanic_orother_consumer_approval=True)
        inventory['B234_clean_other_route_counterpart_leads_v7578b']=dict(proof='work/analysis/lil_B234_clean_counterparts_v7578b/byte_identical_clean_papal_trade_exchange_counterpart_leads.json',SC0B246_andSC1B237_current_context_native_entry_andrelease_unreviewed=True,new_credit=0)
        inventory['later_B234_technical_reaudit_v7606']=dict(actual=str(ACTUAL),later=str(LATER),eighteen_command_eight_duration_timing_RNG_differences_preserved=True,all147_later_RGB_andfive_queried_components_actors_captains_andseeds_equal_only_within_measured_scope=True,three_source_andEnglish_R5_CP932_light_gray_holds_andgeneric_offline_preview_shade_distinction_preserved=True,failed_7586b_key_andmissing_module_andearly_English_fixture_before_census_failure_preserved=True,all_initial_andrefined_layouts_andone_exact_R33_warning_preserved=True,incidental_B120_Camille_Lil_sailing_no_new_credit=True,no_full_RAM_future_orbroad_causal_equivalence_claim=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,B23418_sealed_decisions_uncredited_until_final_registered_release=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist','lil_B234_v7606'],dict(status='sealed-native-stored-actual-reference-pending-atomic-registered-release',manuscript=str(SEALED),native_proof=str(FONT),all18_original_single_four_row_pages144logical72stored=True,actual18pages71body71headers=True,eight_row_reasons_one_exact_R33_warning_R5_CP932_palette_preserved=True,no_new_credit=True));put(['latest_checkpoint'],summary)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5183;put(['coverage_units',ri,'next'],NEXT)
        paths=[SEALED,MAP,SEAL,APPROVED,APPROVAL,PRIOR,inv,ROM,PARENT,ENTRY,LOADER,CENSUS,*map(Path,proof_paths().values()),Path(doc['source_context']),Path(doc['whole_exchange_clean_context']),Path(doc['source_visual_review']),Path('scripts/lil_B234_final_paths_v7602.py'),Path('scripts/lil_B234_pending_text_v7606.py'),Path('work/analysis/lil_B234_seal_tools_v7604/source_locked_reference_seal.json'),Path('work/analysis/lil_B234_atomic_tools_v7605/source_locked_atomic_compiler.json'),Path('dk4tool/patch/lil_B234_editorial_v1.py'),Path('translations/release_stack.json'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),records=rows,record_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows],source_reviewed_decisions=18,uncredited_revisions=14,uncredited_justified_retentions=4,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,all18_five_gates_true_atomic_registered_release_patch_startup_pending=True,current_ROM_families_andall_five_credit_counters_unchanged=True,summary=summary,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_executed_capture_jobs_terminal_andreaped=True,full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and tuple(new[k] for k in COUNTERS)==VALUES
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7606: B234 sealed pending registered integration; V7563 current\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7606; V7563 current, B234 sealed pending\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            dest=ROOT/f'{i:02d}.after';dest.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(dest.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,zero_credit=True,full_goal_complete=False));print('B234 checkpoint staged:18 sealed pending decisions,zero credits,V7563 unchanged;deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_all_prior_roots_nested_records_history_andcounters=True,all_six_before_andplanned_hashes_verified=True,zero_credit=True,full_goal_complete=False));print('B234 checkpoint deep inverse passes;all prior roots,records,families,counters andROM references restore exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_before_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False));print('Six B234 pending targets applied exactly;V7563 andall completed counts unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True);verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),all_previous_roots_nested_history_families_ROM_refs_andcounters_restore_exactly=True,B234_pending_objects=18,B234_uncredited_revisions=14,B234_uncredited_retentions=4,new_credit=0,all18_B234_sealed_native_stored_actual_reference_gates_pass=True,B234_actual_source18pages71body71headers_English18pages71body71headers=True,B234_source1468_logical1468_tail0_target1532_logical1532_tail0_bound=True,B234_eight_row_reasons_one_exact_R33_warning_andR5_CP932_palette=True,B234_all_timing_differences_scoped_later_equalities_failures_andfull_prior_scope_preserved=True,full_goal_active=True,full_goal_complete=False,pending_checkpoint=str(ROOT/'application_receipt.json'),producer_sha256=sha(Path(__file__).read_bytes()));save(VERIFY/'verified_handoff.json',verified);print('V7606 verified:18 sealed B234 decisions pending registered integration;zero credits,V7563/6783 completed unchanged.Full goal active.')
