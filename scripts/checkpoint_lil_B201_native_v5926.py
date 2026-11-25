"""Preserve26 uncredited native-approved B201 reviews with complete old-ledger inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.lil_B201_checkpoint_text_v5926 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_native_checkpoint_v5926')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5927')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5898/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Lil_B201_native_approved_v5926'
SCOPE='unfinished_editorial_scope_v5926'
PREVIOUS='previous_latest_checkpoint_before_Lil_B201_native_v5926'
DOC=Path('translations/lil_B201_editorial_manuscript_v5.json')
MENU=Path('translations/lil_B201_choice_manuscript_v2.json')
APPROVAL=Path('work/analysis/lil_B201_native_approval_v5925/all26_source_prose_current_native_approval.json')
ACTUAL=Path('work/analysis/lil_B201_source_paths_v5914/two_actual_source_choice_paths_all24_speeches_all53_commands_and_returns.json')
COUNTERS=dict(records_editorially_completed=6282,records_with_source_and_prose_pass=6285,records_revised_and_integrated=3941,retained_wordings_editorially_completed=2341)

def inverse(value):
    old=deepcopy(value);old['latest_checkpoint']=old.pop(PREVIOUS);old.pop(KEY);old.pop(SCOPE);return old

def gates():
    doc,menu,approval,actual=map(read,[DOC,MENU,APPROVAL,ACTUAL])
    assert approval['all26_five_gates_approved'] and approval['all26_objects_uncredited']
    assert len(doc['records'])==24 and len(menu['records'])==2 and all(all(r['review'].values()) for r in doc['records']+menu['records'])
    assert len(approval['thirteen_individual_rowcount_reasons'])==13 and len(approval['formatter_negatives'])==28
    assert approval['covered_native_alignment_cases']==approval['exact_byte_identical_reused_native_alignment_cases']==192
    assert approval['source_consumer_negatives']==24 and approval['changed_phrase_layout_indices']==[21,24,34,86,97]
    assert actual['source_distinct_speech_observations']==24 and actual['total_speech_observations']==37 and not actual['unvisited_source_indices']
    assert actual['all44_source_commands_and9_original_initializers_observed_over_two_paths'] and actual['total_frames']==26002
    assert [(r['actual_choice_result'],r['exit_frame']) for r in actual['versions']]==[([2,0],7895),([2,1],7416)]
    for sheet in approval['viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    for case,version in [('buy',5911),('decline',5913)]:assert read(f'work/analysis/lil_B201_source_run_v{version}_{case}/terminal.json')['terminal']
    prior=read(PRIOR)
    for key in ['candidate','patch']:assert sha(Path(prior[key]).read_bytes())==prior[key+'_sha256']
    registry=read('translations/release_stack.json');assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(registry['accepted_layers'])==114
    return doc,menu,approval,actual

def check(plan,applied=False):
    for row in plan['files']:
        assert sha(Path(row['target']).read_bytes())==row['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(row['planned']).read_bytes())==row['planned_sha256']
        before=gzip.decompress(Path(row['before']).read_bytes());assert sha(before)==row['before_sha256']
        if row!=plan['files'][0]:assert Path(row['planned']).read_bytes().endswith(before)
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()));new=read(plan['files'][0]['planned'])
    assert inverse(new)==old and sha(encode_ledger(old))==plan['files'][0]['before_sha256']
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    assert new['completed_editorial_families']==old['completed_editorial_families']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete'] and read(PRIOR)['ledger_sha256']==plan['files'][0]['before_sha256']
    gates();return new

def stage():
    assert not ROOT.exists() and not VERIFY.exists();doc,menu,approval,actual=gates()
    before=LEDGER.read_bytes();old=json.loads(before);prior=read(PRIOR)
    assert sha(before)==prior['ledger_sha256'] and not any(k in old for k in [KEY,SCOPE,PREVIOUS])
    oldscope=Path(old['unfinished_editorial_scope_v5897']['path']);assert sha(oldscope.read_bytes())==old['unfinished_editorial_scope_v5897']['sha256']
    scope=deepcopy(read(oldscope));scope['historical_Lil_B201_clean_inventory_pending_before_v5926']=scope.pop('next_Lil_B201_clean_review_pending')
    scope['Lil_B201_native_review_v5926']=dict(speech_manuscript=str(DOC),choice_manuscript=str(MENU),native_approval=str(APPROVAL),
        reviewed_uncredited_objects=26,speeches=24,choice_labels=2,revisions=12,individually_justified_retentions=14,
        native_covered_alignments=192,native_source_negatives=24,native_formatter_negatives=28,
        actual_source_paths=str(ACTUAL),actual_source_distinct_speeches=24,actual_source_total_speech_observations=37,
        source_boots=2,source_frames=26002,both_Buy_Pass_original_results_observed=True,
        relocation_stored_targets_references_English_actual_compiler_registered_release_and_startup_pending=True,
        source_item_card_does_not_certify_title_or_effects=True,new_global_name_or_dialogue_credit=0)
    scope['source_Trader105_label_retention_v5926']=dict(current_label='Trader',source_primary='交易所の親父',unused_secondary='イスラム',
        B201_full_context_native_two_getters_and_actual_nameplate_bound=True,
        no_father_age_religion_nationality_or_biography_inferred=True,no_name_asset_changed=True,
        not_global_closure_of_actor105_or207_name_queue=True)
    scope['next_focus']=NEXT;ROOT.mkdir(parents=True);sp=ROOT/'unfinished_editorial_scope_inventory.json';save(sp,scope)
    paths=[PRIOR,DOC,MENU,APPROVAL,ACTUAL,oldscope,sp,Path(__file__),Path('scripts/lil_B201_checkpoint_text_v5926.py'),
        Path('work/analysis/lil_B201_clean_inventory_v5900/all_clean_B201_speeches_before_predecessor_comparison.json'),
        Path('work/analysis/lil_B201_clean_context_v5901/all24_clean_rigging_price_negotiation_purchase_refusal_and_three_stat_glosses.json'),
        Path('work/analysis/lil_B201_source_v5902/all26_clean_current_complete_context_with_two_choice_labels.json'),
        Path('work/analysis/lil_B201_comparison_v5915/complete_clean_context_source_paths_three_names_prices_stat_terms_and_item_scope.json'),
        Path('work/analysis/lil_B201_author_v5917/all26_clean_first_contextual_decisions.json'),
        Path('work/analysis/lil_B201_fonts_v5923c/all24_progressive_FE_native_planes_and192_alignment_cases.json'),
        Path('work/analysis/lil_B201_choices_v5924/all1_typed_menu_native_proof.json'),
        Path('work/analysis/lil_B201_phrase_layout_v5921/complete_phrase_preserving_successors.json'),
        Path('work/analysis/lil_B201_phrase_layout_v5921/corrected_unvalidated_comma_tag_proposal.json'),
        Path('work/analysis/lil_B201_phrase_layout_v5921/final_readability_successors.json'),
        Path('work/analysis/lil_B201_source_fixture_v5910/pin_receipt.json'),Path('releases/all_routes_unified_v5891/verification.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,records=doc['records'],typed_choice_records=menu['records'],
        all26_reviewed_objects_uncredited_and_absent_from_current_ROM=True,revisions=12,retentions=14,new_editorial_credit=0,new_name_credit=0,
        new_source_ROMs=1,new_Japanese_source_cold_boots=2,new_source_frames=26002,new_English_cold_boots=0,
        all_sessions_terminal_and_reaped=True,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
    new[SCOPE]=dict(path=str(sp),sha256=sha(sp.read_bytes()),B201_uncredited_objects=26,
        names207_queue_three_completed_label_leads_and_all_other_editorial_scope_preserved=True,full_goal_complete=False)
    assert inverse(new)==old;targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<106*1024*1024
    section='## V5926: B201 complete clean/source/native review;26 objects await integration\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;prefix=('# Current editorial handoff - V5926\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[p]=prefix.replace('\n','\r\n').encode('utf-8')+p.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        after=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz';after.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),planned=str(after.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True));print('Six progress targets staged;26 B201 native reviews remain uncredited;full scope/history retained.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);phase=p.parse_args().phase
    if phase=='stage':stage()
    else:
        pp=ROOT/'staged_checkpoint.json';plan=read(pp)
        if phase=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();check(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(pp.read_bytes()),complete_inverse_all_old_bytes_and_evidence_exact=True));print('Six-file complete inverse/preapplication audit passes.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_preapplication_audit.json')['plan_sha256']==sha(pp.read_bytes());check(plan)
            for row in plan['files']:assert Path(row['target']).is_relative_to(Path.cwd().resolve()) and Path(row['planned']).is_relative_to(ROOT.resolve())
            for row in plan['files']:
                with Path(row['target']).open('r+b') as f:f.write(Path(row['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_exact=True,all_original_history_preserved=True));print('Six audited progress targets applied with full history and counters intact.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_exact'];new=check(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
                patch=prior['patch'],patch_sha256=prior['patch_sha256'],profile=prior['profile'],ARM9_sha256=prior['ARM9_sha256'],
                all_original_root_nested_families_counters_and_integrated_candidate_preserved=True,**COUNTERS,
                completed=6282,source_prose=6285,revised=3941,retained=2341,SC2=4397,SC3=96,reviewed_routes=4683,completed_routes=4683,
                B201_uncredited_objects=26,B201_speech_objects=24,B201_choice_labels=2,B201_revisions=12,B201_retentions=14,
                B201_source_native_five_gates_approved=True,B201_covered_native_alignments=192,B201_consumer_negatives=24,B201_formatter_negatives=28,
                B201_complete_source_paths=2,B201_actual_distinct_speeches=24,B201_total_source_speech_observations=37,
                goal_turn_new_Japanese_cold_boots=2,goal_turn_new_Japanese_frames=26002,goal_turn_new_English_cold_boots=0,
                B201_relocation_English_actual_atomic_compiler_and_registered_release_pending=True,
                scope_inventory=new[SCOPE],all207_name_review_scope_and_every_earlier_pending_lead_preserved=True,
                main_V4701_preserved=True,no_promotion_commit_push_or_pruning=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5927 verified:26 B201 source/native approvals saved uncredited;V5891/main/6282 completed reviews unchanged. Full goal active.')
