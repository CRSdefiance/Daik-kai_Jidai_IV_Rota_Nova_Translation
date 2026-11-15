"""Record13 uncredited whole-exchange decisions and exact name/item leads;preserve all history."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B207_source_checkpoint_text_v6352 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B207_source_prose_checkpoint_v6352')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6353')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6334/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B207_editorial_manuscript_v1.json')
APP=Path('work/analysis/lil_B207_prose_v6350/all13_exact_source_current_findings_six_revisions_seven_retentions.json')
VIEW=Path('work/analysis/lil_B207_source_view_v6348/all13_source_speeches_nameplates_and_town_return_viewed.json')
ACTUAL=Path('work/analysis/lil_B207_source_actual_v6347/all13_source_speeches_all24_commands_and_complete_return.json')
CURRENT=Path('work/analysis/lil_B207_effective_v6349b/all13_effective_current_paragraphs_and_source_item_name.json')
KEY='Lil_B207_source_prose_review_v6352'
SCOPE='unfinished_editorial_scope_v6352'
def inverse(value):
    result=deepcopy(value);entry=result.pop(KEY);result.pop(SCOPE);result['latest_checkpoint']=entry['previous_latest_checkpoint'];return result
def gates():
    prior,doc,app,view,actual,current=map(read,[PRIOR,DOC,APP,VIEW,ACTUAL,CURRENT])
    for k in ['candidate','patch']:assert sha(Path(prior[k]).read_bytes())==prior[k+'_sha256']
    assert doc['current_ROM_sha256']==prior['candidate_sha256'] and app['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(doc['records'])==13 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':6,'retain-wording':7} and doc['formatting_review_pending'] and app['all13_first_four_gates_approved'] and app['all13_formatting_gates_false']
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert all('{LB}' not in r['english'] and '{LB@' not in r['english'] and '{ALIGN@' not in r['english'] for r in doc['records'])
    assert not view['visual_review_pending'] and len(view['viewed_sheets'])==4 and view['actual_source_speeches']==13 and view['source_exit_frame']==5976 and view['actual_town_return_frame']==6070 and view['following_B120_complete_end_not_observed']
    for row in view['viewed_sheets']:assert row['viewed_after_image_return'] and sha(Path(row['path']).read_bytes())==row['sha256']
    assert actual['source_distinct_speech_observations']==13 and len(actual['command_pairs'])==24 and actual['all15_source_commands_and9_original_initializers_observed'] and actual['total_frames']==11001 and actual['all_jobs_terminal_and_reaped'] and not actual['unvisited_source_indices']
    terminal=read('work/analysis/lil_B207_source_run_v6346/terminal.json');assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
    assert current['all13_current_dispatch_bodies_equal_raw_storage_no_catalogue_override'] and current['item_name_binding']['item_ID']==41 and current['item_name_binding']['source_Japanese']=='ミノタウロスの斧' and current['item_name_binding']['current_English']=='Minotaur Axe'
    assert len(current['existing_source_current_Minotaur_descriptions'])==1 and current['existing_source_current_Minotaur_descriptions'][0]['message_ID']==2856 and current['existing_mixed_width_F_is_a_separate_native_encoding_metrics_lead']
    binding=read('work/analysis/current_V6327_native_v6337/verified_current_context_binding.json');assert binding['candidate_sha256']==prior['candidate_sha256'] and binding['current_ARM9_COMMON_directory_and_executed_instruction_guards_preserved'] and binding['current_actual_opening4000_and_all123264_staged_bytes_bound']
    names=read(doc['actor_terminology_reconciliation']);assert [r['actor_ID'] for r in names['source_name_fields']]==[2,14] and names['source_name_fields'][1]['progressive']==names['source_name_fields'][1]['catalogue']=='Emilio Ｆerog'
    for proof in [app,view,actual,current]:
        for p,h in proof.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h
    for key in ['source_context','actual_source_visual_review','actor_terminology_reconciliation','source_prose_module','effective_current_comparison','control_contract','source_control_leaves','source_entry_proof']:assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    registry=read('translations/release_stack.json');manifest=read(Path(prior['candidate']).with_suffix('.manifest.json'));assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(manifest['batches'])==597 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    return prior,doc
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not VERIFY.exists();prior,doc=gates();raw=LEDGER.read_bytes();assert sha(raw)==prior['ledger_sha256'];old=json.loads(raw);new=deepcopy(old);assert KEY not in old and SCOPE not in old
        previous=old['unfinished_editorial_scope_v6333'];assert sha(Path(previous['path']).read_bytes())==previous['sha256'];scope=deepcopy(read(previous['path']));scope['next_focus']=NEXT
        scope['Lil_B207_source_prose_approved_uncredited_v6352']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),prose_receipt=str(APP),prose_receipt_sha256=sha(APP.read_bytes()),objects=13,speeches=13,revised=6,retained=7,four_prose_gates_true_formatting_false=True,actual_source13speeches15commands9initializers11001frames_town_return_observed=True,English_native_name_metrics_relocation_actual_and_registered_release_pending=True,new_completion_credit=0)
        scope['Emilio_Ferog_current_encoding_metrics_lead_v6352']=dict(source_names=doc['actor_terminology_reconciliation'],source_names_sha256=doc['actor_terminology_reconciliation_sha256'],actor_ID=14,source_primary='エミリオ',source_surname='フェローグ',current_serialized_full_name='Emilio Ｆerog',actual_visible_name_complete_and_readable=True,fullwidth_F_not_automatic_ASCII_conversion_or_renaming=True,proper_name_context_and_all_relevant_native_consumer_metrics_review_pending=True,no_name_asset_or_global207_name_credit=True)
        scope['B207_item41_title_and_COMMON2856_description_distinct_v6352']=dict(proof=str(CURRENT),proof_sha256=sha(CURRENT.read_bytes()),item_ID=41,current_title='Minotaur Axe',description_COMMON_ID=2856,spoken_title_consistency_revision_without_item_asset_change=True,failed_exact_title_in_COMMON_assumption_preserved=True,new_item_credit=0)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
        ROOT.mkdir(parents=True);sp=ROOT/'unfinished_editorial_scope_inventory.json';save(sp,scope);new[SCOPE]=dict(path=str(sp),sha256=sha(sp.read_bytes()),uncredited_B207_prose_approved_objects=13,incomplete_COMMON=3,retrospective207_names_all_four_storylines_and_wider_editorial_scope_preserved=True,full_goal_complete=False)
        paths=[PRIOR,DOC,APP,VIEW,ACTUAL,CURRENT,sp,Path(__file__),Path('scripts/lil_B207_source_checkpoint_text_v6352.py'),Path('work/analysis/current_V6327_native_v6337/verified_current_context_binding.json'),Path('work/analysis/lil_B207_source_fixture_v6345/pin_receipt.json'),Path('work/analysis/lil_B207_source_run_v6346/terminal.json')]
        paths.extend(Path(doc[k]) for k in ['source_context','actor_terminology_reconciliation','control_contract','source_control_leaves','source_entry_proof']);evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(previous_latest_checkpoint=old['latest_checkpoint'],summary=DETAILS,next_focus=NEXT,evidence=evidence,record_IDs=[r['id'] for r in doc['records']],objects=13,revised_drafts=6,retained_drafts=7,new_completion_credit=0,new_research_ROMs=1,new_source_runs=1,new_source_frames=11001,all_source_jobs_terminal_and_reaped=True,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
        new['latest_checkpoint']=DETAILS+'\n\n'+NEXT;assert inverse(new)==old;targets={LEDGER:encode_ledger(new)};section='## V6352: B207 whole-exchange source/prose review;name metrics and native/release pending\n\n'+DETAILS+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            target=Path('docs')/name;prefix=('# Current editorial handoff - V6352\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[target]=prefix.replace('\n','\r\n').encode('utf-8')+target.read_bytes()
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz';planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0));files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),backup=str(backup.resolve()),before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence));print('Six targets staged:13 uncredited B207 decisions,exact name/item/source leads;all V6327 history/counters retained.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress(Path(plan['files'][0]['backup']).read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;prior,doc=gates()
        assert all(new[k]==old[k] for k in ['current_integrated_candidate','records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_families','active_source_prose_drafts']) and tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6415,6418,4005,2410) and new['goal_status']=='active' and not new['full_goal_complete']
        for row in plan['files']:assert sha(Path(row['target']).read_bytes())==row['planned_sha256' if mode=='verify' else 'before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256'] and sha(gzip.decompress(Path(row['backup']).read_bytes()))==row['before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_every_prior_root_nested_value_and_counters_exact=True,no_duplicate_or_premature_review_credit=True));print('Six-target deep-inverse/history and source/prose/name/item evidence audit passed.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for row in plan['files']:assert Path(row['target']).is_relative_to(Path.cwd().resolve()) and Path(row['planned']).is_relative_to(ROOT.resolve())
            for row in plan['files']:
                with Path(row['target']).open('r+b') as stream:stream.write(Path(row['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all6_targets_applied_exactly=True,all_original_history_and_compression_preserved=True));print('Six audited ledger/progress targets applied;all old history/counters preserved.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_applied_exactly'];VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],profile=prior['profile'],ARM9_sha256=prior['ARM9_sha256'],completed=6415,source_prose=6418,revised=4005,retained=2410,SC2=4529,SC3=96,reviewed_routes=4815,completed_routes=4815,all_prior_root_nested_history_and_counters_exact=True,B207_all13_source_context_prose_approved_formatting_false=True,B207_six_revisions_seven_retentions_still_uncredited=True,Emilio_Ferog_mixedwidth_F_native_metrics_review_lead_open=True,item41_Minotaur_Axe_and_COMMON2856_description_bound=True,actual_B207_source_speeches=13,actual_source_commands_with_initializers=24,source_exit_frame=5976,town_return_frame=6070,final11001_B120_still_active_complete_end_unobserved=True,new_research_ROMs=1,new_source_runs=1,new_source_frames=11001,all_source_jobs_terminal_and_reaped=True,current_own_native_input='work/analysis/current_V6327_native_v6337/current_native_input.json',scope_inventory=new[SCOPE],main_V4701_preserved=True,all207_names_all_storylines_and_full_editorial_objective_preserved=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V6352 verified:13 B207 whole-exchange decisions remain uncredited;name/native/release review next. Current cumulative V6327/6415 completions and full goal preserved.')
