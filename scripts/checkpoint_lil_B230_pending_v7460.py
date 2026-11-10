"""Six-target zero-credit checkpoint with a complete prior-ledger inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B230_final_paths_v7457 import *
from scripts.lil_B230_pending_text_v7460 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B230_pending_checkpoint_v7460');VERIFY=Path('work/analysis/editorial_handoff_verification_v7461');LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7425/verified_handoff.json')
KEY='lil_B230_review_pending_v7460';SCOPE='unfinished_editorial_scope_v7460';COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];VALUES=(6739,6742,6742,4211,2528)
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def gates():
    prior=read(PRIOR);ledger=read(LEDGER);current=ledger['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(current['manifest'])
    assert current['sha256']==prior['candidate_sha256']==sha(Path(current['path']).read_bytes()) and current['profile']==manifest['profile']=='all-routes-unified-v7418'
    assert len(manifest['batches'])==622 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    doc,seal,mapping,font,policy,stored,actual,later=map(read,[SEALED,SEAL,MAP,FONT,POLICY,STORED,ACTUAL,LATER])
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes()) and seal['all17_five_gates_andexact_references_approved'] and seal['research_ROM_sha256']==sha(ROM.read_bytes()) and doc['current_ROM_sha256']==current['sha256']
    assert len(doc['records'])==17 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':9,'retain-wording':8} and all(all(r['review'].values()) for r in doc['records']) and doc['registered_integration_pending']
    assert (font['complete_native_pages'],font['logical_compiled_input_alignment_cases'],stored['stored_alignment_cases'],stored['fresh_alignment_cases'],stored['exact_reused_alignment_cases'],stored['zero_ink_parity_tail_count'])==(17,136,68,24,44,6)
    assert policy['positive_paragraph_count']==17 and policy['negative_count']==len(policy['negative_cases'])==76 and all(r['rejected'] for r in policy['negative_cases']) and len(policy['row_count_reasons'])==7 and policy['all_base_QA_diagnostics_preserved_zero_warning_waivers']
    assert actual['actual_unique_speeches']==actual['actual_native_pages']==17 and actual['actual_complete_body_holds']==actual['actual_complete_name_holds']==67 and not actual['incomplete_sampled_body_holds'] and actual['all28_commands_observed'] and actual['all_jobs_terminal_and_reaped'] and not read(VIEW)['visual_review_pending']
    assert (len(actual['command_comparison_differences']),len(actual['command_duration_changes']),len(later['later_sampled_RGB_differences']),later['total_later_sampled_frames'])==(17,6,88,151)
    assert mapping['observed_comparison_contract']==seal['observed_comparison_contract'] and read(CONTROL)['original_normal_end974_four_bytes_andtarget_two_byte_tail_preserved']
    assert [(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in read(ENTRY)['selected_B230_source_events']]==[(230,230,231,[229],[])]
    sam=next(r for r in read(NAMES)['records'] if r['actor_ID']==22);assert sam['catalogue_current']=='Samwell ダ Khan' and not sam['catalogue_wording_editorially_approved'] and sam['actual_final_English_header_observed']
    item=read(ITEM)['source_named_item'];assert (item['record_ID'],item['Japanese'],item['English'],item['current_storage_kind'])==('DK4_ITEM_POINTER_052','不死鳥のバシネット','Phoenix Bascinet','static-current-ARM9')
    assert read(NAMEPROOF)['fresh_native_name_font_alignment_cases']==0 and read(NAMEPROOF)['exact_reused_native_name_font_alignment_cases']==32 and read(PLACE)['no_name_item_country_asset_orcredit_change']
    for p,h in read('translations/lil_B230_native_contract_v1.json')['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    return prior,doc
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,doc=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);rows=deepcopy(doc['records']);oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows};assert len(oldkeys)==6739 and len(keys)==17 and not oldkeys&keys;ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        summary=DETAILS+'\n\n'+NEXT;scope=old['unfinished_editorial_scope_v7424'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory['Lil_B230_pending_v7460']=dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),pending_objects=17,uncredited_revisions=9,uncredited_retentions=8,all17_five_individual_source_native_stored_actual_reference_gates_complete=True,registered_atomic_build_patch_startup_pending=True,source988_logical988_tail0_target980_logical978_tail2_full_inverse=True,seven_row_reasons_zero_warnings_waivers=True,new_credit=0,full_goal_complete=False)
        inventory['next_Lil_B230_source_only_gloss_complete']['superseded_by_sealed_pending_review']=dict(manuscript=str(SEALED),all_historical_pending_flags_preserved=True,new_credit=0)
        inventory['Britain_untranslated_country_label_consumer_lead_v7434']=dict(proof=str(PLACE),sha256=sha(PLACE.read_bytes()),untranslated_literal=deepcopy(read(PLACE)['untranslated_country_literal']),no_asset_UI_orcredit_approval=True)
        inventory['later_B230_technical_reaudit_v7460']=dict(actual=str(ACTUAL),later=str(LATER),seventeen_command_six_duration_88of151_RGB_andcalendar_PRNG_actor_differences_preserved=True,source_Sailor_water_vsEnglish_Sea_View_final_contrast=True,country_reader_guard_failure_andexact_owned_reader_successor_preserved=True,earlier_layout_weak_in_warning_andtwo_refinements_preserved=True,final_view_duplicate_console_word_metadata_only=True,incidental_B120_Camille_Sailor_and_sailing_no_new_credit=True,no_full_RAM_future_orbroad_causal_equivalence_claim=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,B23017_sealed_decisions_uncredited_until_final_registered_release=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist','lil_B230_v7460'],dict(status='sealed-native-stored-actual-reference-pending-atomic-registered-release',manuscript=str(SEALED),native_proof=str(FONT),all17_original_single_four_row_pages136logical68stored=True,actual17pages67body67headers=True,seven_row_reasons_zero_warnings_waivers=True,no_new_credit=True));put(['latest_checkpoint'],summary)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5139;put(['coverage_units',ri,'next'],NEXT)
        paths=[SEALED,MAP,SEAL,APPROVED,APPROVAL,PRIOR,inv,ROM,PARENT,ENTRY,LOADER,CENSUS,*map(Path,proof_paths().values()),Path(doc['source_context']),Path(doc['whole_exchange_clean_context']),Path(doc['source_visual_review']),Path('scripts/lil_B230_final_paths_v7457.py'),Path('scripts/lil_B230_pending_text_v7460.py'),Path('work/analysis/lil_B230_seal_tools_v7459/source_locked_reference_seal.json'),Path('translations/release_stack.json'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),records=rows,record_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows],source_reviewed_decisions=17,uncredited_revisions=9,uncredited_justified_retentions=8,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,all17_five_gates_true_atomic_registered_release_patch_startup_pending=True,current_ROM_families_andall_five_credit_counters_unchanged=True,summary=summary,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_executed_capture_jobs_terminal_andreaped=True,full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and tuple(new[k] for k in COUNTERS)==VALUES
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7460: B230 sealed pending registered integration; V7418 current\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7460; V7418 current, B230 sealed pending\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            dest=ROOT/f'{i:02d}.after';dest.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(dest.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,zero_credit=True,full_goal_complete=False));print('B230 checkpoint staged:17 sealed pending decisions,zero credits,V7418 unchanged;deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_all_prior_roots_nested_records_history_andcounters=True,all_six_before_andplanned_hashes_verified=True,zero_credit=True,full_goal_complete=False));print('B230 checkpoint deep inverse passes;all prior roots,records,families,counters andROM references restore exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_before_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False));print('Six B230 pending targets applied exactly;V7418 andall completed counts unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True);verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),all_previous_roots_nested_history_families_ROM_refs_andcounters_restore_exactly=True,B230_pending_objects=17,B230_uncredited_revisions=9,B230_uncredited_retentions=8,new_credit=0,all17_B230_sealed_native_stored_actual_reference_gates_pass=True,B230_actual_source17pages67body67headers_English17pages67body67headers=True,B230_source988_tail0_target980_logical978_tail2_bound=True,B230_seven_row_reasons_zero_warnings_orwaivers=True,B230_all_late_differences_andfull_prior_scope_preserved=True,full_goal_active=True,full_goal_complete=False,pending_checkpoint=str(ROOT/'application_receipt.json'),producer_sha256=sha(Path(__file__).read_bytes()));save(VERIFY/'verified_handoff.json',verified);print('V7460 verified:17 sealed B230 decisions pending registered integration;zero credits,V7418/6739 completed unchanged.Full goal active.')
