"""Stage,audit,apply and verify one contextual name revision while preserving every prior value."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.shady_man_completion_text_v6275 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_label_completion_v6275');VERIFY=Path('work/analysis/editorial_handoff_verification_v6276');PRIOR=Path('work/analysis/editorial_handoff_verification_v6256/verified_handoff.json');LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/shady_man_label_manuscript_v2.json');RELEASE=Path('work/analysis/shady_man_label_release_v6271/registered_release_verification.json');START=Path('work/analysis/shady_man_startup_v6273/cold_boot_Lil_startup_town_verification.json');VIEW=START.parent/'current_six_frame_visual_review.json'
KEY='shady_man_label_completed_v6275';SCOPE='unfinished_editorial_scope_v6275';PARENT='previous_integrated_candidate_before_shady_man_v6275';PREVIOUS='previous_latest_checkpoint_before_shady_man_v6275'
COUNTERS=dict(records_editorially_completed=6387,records_with_source_and_prose_pass=6390,records_revised_and_integrated=3989,retained_wordings_editorially_completed=2398)
def inverse(d):
    d=deepcopy(d);d['current_integrated_candidate']=d.pop(PARENT);d['latest_checkpoint']=d.pop(PREVIOUS);d.pop(KEY);d.pop(SCOPE);return d
def gates():
    r,s,v,doc=map(read,[RELEASE,START,VIEW,DOC])
    assert r['all595_manifest_batches114_accepted_layers18_checks_present'] and r['whole_ROM_reconstruction_and_approved_reference_byte_exact'] and r['only_one_owned_primary_label_prefix_changed_from_V6220'] and r['every_other_file_story_font_graphic_ARM7_overlay_entry_and_name_field_exact_to_V6220']
    assert s['all_current_requested_and_final_framebuffers_equal_V6220'] and s['paired_frame_count']==31 and s['all_five_postload_actor_model_and_captain_checks_equal'] and s['source_and_disposable_town_donor_unchanged']
    assert v['viewed'] and v['no_new_display_finding'] and v['sha256']==s['review_sheet_sha256']==sha(Path(s['review_sheet']).read_bytes())
    assert len(doc['records'])==1 and all(doc['records'][0]['review'].values())
    atomic=read('work/analysis/shady_man_label_atomic_v6267/atomic_validation_receipt.json');assert atomic['negative_count']==57 and atomic['dependency_count']==138 and atomic['all_negatives_reject_before_mutation']
    regression=read('work/analysis/shady_man_regressions_v6270/terminal.json');assert regression['terminal'] and regression['returncode']==0 and '110 passed' in Path(regression['log']).read_text('utf-8')
    for case in ['newgame','town']:assert read(f'work/analysis/shady_man_runs_v6272/{case}_terminal.json')['terminal']
    run=read('work/analysis/shady_man_source_run_v6262_buy/terminal.json');assert run['terminal'] and run['observer_host_slots_restored']
    assert read('work/analysis/shady_man_label_retention_v6274/pin_receipt.json')['all_prior_pins_preserved']
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==r[k+'_sha256']
    binding=read('work/analysis/current_V6270_native_v6279/verified_current_context_binding.json');assert binding['candidate_sha256']==r['candidate_sha256'] and binding['current_actual_opening4000_and_all123264_staged_bytes_bound']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return r,doc
def check(plan,applied=False):
    for row in plan['files']:
        assert sha(Path(row['target']).read_bytes())==row['planned_sha256' if applied else 'before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256'] and sha(gzip.decompress(Path(row['before']).read_bytes()))==row['before_sha256']
        if row!=plan['files'][0]:assert Path(row['planned']).read_bytes().endswith(gzip.decompress(Path(row['before']).read_bytes()))
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items()) and new['completed_editorial_families']==old['completed_editorial_families'] and new['active_source_prose_drafts']==old['active_source_prose_drafts']
    assert new['goal_status']=='active' and not new['full_goal_complete'] and read(PRIOR)['ledger_sha256']==plan['files'][0]['before_sha256']
    assert new['current_integrated_candidate']['sha256']==read(RELEASE)['candidate_sha256'];gates();return new
def stage():
    assert not ROOT.exists() and not VERIFY.exists();r,doc=gates();raw=LEDGER.read_bytes();old=json.loads(raw);assert sha(raw)==read(PRIOR)['ledger_sha256'] and not any(k in old for k in [KEY,SCOPE,PARENT,PREVIOUS])
    prior_scope=Path(old['unfinished_editorial_scope_v6255']['path']);assert sha(prior_scope.read_bytes())==old['unfinished_editorial_scope_v6255']['sha256'];scope=deepcopy(read(prior_scope));scope['next_focus']=NEXT
    scope['actor173_name_review_current_v6275']=dict(closed_source_context_label_lead=173,current_primary='Shady Man',manuscript=str(DOC),registered_release=str(RELEASE),all8_direct_seller_exchanges195_speeches_read=True,only173_primary_changed_206_other_actors_not_new_editorial_approvals=True,all207_proper_names_roles_aliases_and_older_consumers_stay_open=True,retained_Cristina_Erneco_working_name_and88_Christina23_Cristina_record_queue_preserved=True,historical_v6249_proposal_and_v6255_pending_findings_preserved_and_superseded_for173_only=True,new_duplicate_dialogue_or_name_credit=0)
    scope['B206_next_native_relocation_actual_release_v6275']=dict(manuscript='translations/lil_B206_editorial_manuscript_v1.json',prose_objects=28,revised_drafts=16,retained_drafts=12,actor173_asset_dependency_validated_in_V6270=True,English_native_menu_relocation_actual_and_registered_release_still_pending=True,current_parent=r['candidate'],new_completion_credit=0)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    ROOT.mkdir(parents=True);sp=ROOT/'unfinished_editorial_scope_inventory.json';save(sp,scope)
    paths=[PRIOR,DOC,RELEASE,START,VIEW,prior_scope,sp,Path(__file__),Path('scripts/shady_man_completion_text_v6275.py'),Path('work/analysis/shady_man_label_approval_v6266/one_label_source_native_display_approval.json'),Path('work/analysis/shady_man_label_atomic_v6267/atomic_validation_receipt.json'),Path('work/analysis/shady_man_label_registration_v6269/registration_receipt.json'),Path('work/analysis/shady_man_regressions_v6270/terminal.json'),Path('work/analysis/shady_man_label_retention_v6274/pin_receipt.json'),Path('work/analysis/current_V6270_native_v6279/verified_current_context_binding.json')];evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PARENT]=deepcopy(old['current_integrated_candidate']);new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new['current_integrated_candidate'].update(path=r['candidate'],sha256=r['candidate_sha256'],profile=r['profile'],ARM9_sha256=r['ARM9_sha256'],MESFILE_sha256=r['COMMON_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],manifest=r['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY)
    new[KEY]=dict(summary=SUMMARY,next=NEXT,records=doc['records'],evidence=evidence,new_integrated_label_revisions=1,duplicate_dialogue_or_prior_name_completion_credit=0,all_earlier_completed_families_counters_and_uncredited_B206_draft_exact=True,all207_name_scope_open_other206_not_new_editorial_approvals=True,new_label_and_startup_cold_boots=3,new_label_and_startup_frames=37403,all_sessions_terminal_and_reaped=True,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
    new[SCOPE]=dict(path=str(sp),sha256=sha(sp.read_bytes()),actor173_label_lead_closed_B206_prose_still_uncredited=True,all207_name_review_and_full_editorial_objective_active=True,full_goal_complete=False)
    assert inverse(new)==old;targets={LEDGER:encode_ledger(new)};section='## V6275: Shady Man contextual name revision integrated in cumulative V6270\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;prefix=('# Current editorial handoff - V6275\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode('utf-8')+p.read_bytes()
    for name in ['natural_dialogue_workflow.md','editorial_localization_and_layout_standard.md']:
        p=Path('docs')/name;prefix='## Current speaker-name finding - V6275\n\nActor173 is now Shady Man in experimental cumulative V6270,following eight complete clean seller exchanges,all native name/field/macro/font checks,ten actual headers,registered exact clean-input patch and startup tests. Earlier Man/Woman/Stranger remain. Exact references and rationale:translations/shady_man_label_manuscript_v2.json. Keep every historical pending proposal below as evidence,superseded for173 only. The full207 proper-name/role/alias review,individual Cristina/Christina consumers and wider editorial goal remain open. Preserve approved names and all source-fidelity rules.\n\n';targets[p]=prefix.replace('\n','\r\n').encode('utf-8')+p.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz';planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0));files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True));print('Eight targets staged:one integrated label,zero duplicate credit,unchanged6387 completions and all28 B206 drafts/history preserved.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);phase=p.parse_args().phase
    if phase=='stage':stage()
    else:
        pp=ROOT/'staged_checkpoint.json';plan=read(pp)
        if phase=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();check(plan);save(ROOT/'preapplication_audit.json',dict(plan_sha256=sha(pp.read_bytes()),deep_inverse_all_prior_root_and_nested_values_and_evidence_exact=True));print('Eight-file inverse/history and evidence audit passed.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['plan_sha256']==sha(pp.read_bytes());check(plan)
            for row in plan['files']:assert Path(row['target']).is_relative_to(Path.cwd().resolve()) and Path(row['planned']).is_relative_to(ROOT.resolve())
            for row in plan['files']:
                with Path(row['target']).open('r+b') as f:f.write(Path(row['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_eight_targets_exact=True,all_original_history_preserved=True));print('Eight audited checkpoint files applied;all history/compression preserved.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_eight_targets_exact'];new=check(plan,True);r,doc=gates();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],profile=r['profile'],ARM9_sha256=r['ARM9_sha256'],all_prior_root_nested_families_counters_and_B206_draft_history_preserved=True,**COUNTERS,completed=6387,source_prose=6390,revised=3989,retained=2398,SC2=4501,SC3=96,reviewed_routes=4787,completed_routes=4787,actor173_Shady_Man_integrated=True,no_duplicate_dialogue_or_prior_name_credit=True,all595_batches114_accepted18_checks57_negatives110_regressions_pass=True,all207_name_and_Cristina_alias_scope_open=True,B206_uncredited_prose_objects=28,B206_native_menus_relocation_actual_and_release_pending=True,scope_inventory=new[SCOPE],three_label_and_startup_boots37403_frames=True,all_sessions_terminal_and_reaped=True,main_V4701_preserved=True,no_promotion_commit_push_or_pruning=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())));print('V6275 verified:Shady Man integrated inV6270;all6387 reviews/28uncredited B206 prose drafts/history intact. Fullgoal active.')
