"""Record three validated name revisions without duplicating any existing review credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.generic_speaker_labels_completion_text_v5897 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_completion_v5897')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5898')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5878/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/generic_speaker_labels_manuscript_v2.json')
RELEASE=Path('work/analysis/generic_speaker_labels_release_v5895/registered_release_verification.json')
START=Path('work/analysis/generic_speaker_labels_startup_v5894/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
KEY='generic_speaker_labels_completed_v5897'
SCOPE='unfinished_editorial_scope_v5897'
PARENT='previous_integrated_candidate_before_generic_speaker_labels_v5897'
PREVIOUS='previous_latest_checkpoint_before_generic_speaker_labels_v5897'
COUNTERS=dict(records_editorially_completed=6282,records_with_source_and_prose_pass=6285,records_revised_and_integrated=3941,retained_wordings_editorially_completed=2341)

def inverse(value):
    old=deepcopy(value);old['current_integrated_candidate']=old.pop(PARENT);old['latest_checkpoint']=old.pop(PREVIOUS);old.pop(KEY);old.pop(SCOPE);return old

def gates():
    r,s,v=map(read,[RELEASE,START,VIEW]);doc=read(DOC)
    assert r['all587_manifest_batches114_accepted_layers18_checks_present'] and r['whole_ROM_reconstruction_and_approved_reference_byte_exact']
    assert r['only_three_owned_primary_label_prefixes_changed_from_V5872'] and r['every_other_file_story_font_graphic_ARM7_overlay_entry_and_name_field_exact_to_V5872']
    assert s['all_current_requested_and_final_framebuffers_equal_V5872'] and s['paired_frame_count']==31 and s['all_five_postload_actor_model_and_captain_checks_equal']
    assert s['source_and_disposable_town_donor_unchanged'] and v['viewed'] and v['no_new_display_finding']
    assert v['sha256']==s['review_sheet_sha256']==sha(Path(s['review_sheet']).read_bytes())
    assert len(doc['records'])==3 and all(all(row['review'].values()) for row in doc['records'])
    atomic=read('work/analysis/generic_speaker_labels_atomic_v5889/atomic_validation_receipt.json')
    assert atomic['negative_count']==71 and atomic['dependency_count']==143 and atomic['all_negatives_reject_before_mutation']
    regression=read('work/analysis/generic_speaker_labels_regressions_v5891/terminal.json');assert regression['terminal'] and regression['returncode']==0
    assert '110 passed' in Path(regression['log']).read_text(encoding='utf-8')
    for case in ['newgame','town']:
        assert read(f'work/analysis/generic_speaker_labels_runs_v5893/{case}_terminal.json')['terminal']
    for case in ['tea','recovery']:
        assert read(f'work/analysis/generic_speaker_label_run_v5883_{case}/terminal.json')['terminal']
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==r[k+'_sha256']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return r,doc

def check(plan,applied=False):
    for row in plan['files']:
        assert sha(Path(row['target']).read_bytes())==row['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(row['planned']).read_bytes())==row['planned_sha256']
        assert sha(gzip.decompress(Path(row['before']).read_bytes()))==row['before_sha256']
        if row!=plan['files'][0]:assert Path(row['planned']).read_bytes().endswith(gzip.decompress(Path(row['before']).read_bytes()))
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()));new=read(plan['files'][0]['planned'])
    assert inverse(new)==old and sha(encode_ledger(old))==plan['files'][0]['before_sha256']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['completed_editorial_families']==old['completed_editorial_families']
    assert new['goal_status']=='active' and not new['full_goal_complete']
    assert read(PRIOR)['ledger_sha256']==plan['files'][0]['before_sha256']
    assert new['current_integrated_candidate']['sha256']==read(RELEASE)['candidate_sha256']
    gates();return new

def stage():
    assert not ROOT.exists() and not VERIFY.exists();r,doc=gates();before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==read(PRIOR)['ledger_sha256'] and not any(k in old for k in [KEY,SCOPE,PARENT,PREVIOUS])
    prior_scope=Path(old['unfinished_editorial_scope_v5877']['path']);assert sha(prior_scope.read_bytes())==old['unfinished_editorial_scope_v5877']['sha256']
    scope=deepcopy(read(prior_scope))
    scope['historical_three_generic_speaker_labels_pending_before_v5897']=scope.pop('next_three_generic_speaker_labels_target_validation')
    scope['retrospective_name_review_current_v5897']=dict(total_actor_catalog_entries=207,closed_source_context_label_leads=[164,165,172],
        current_labels={'164':'Man','165':'Woman','172':'Stranger'},remaining_actor_entries_not_newly_contextually_approved=204,
        all207_technical_getters_not_equivalent_to_all207_editorial_reviews=True,
        Samwell_middle_field_and_all_earlier_name_alias_leads_stay_open=True,
        final_manuscript=str(DOC),registered_release=str(RELEASE),duplicate_dialogue_and_previous_name_credit_added=0)
    scope['next_focus']=NEXT
    assert scope['next_Lil_B201_clean_review_pending']['reviewed_objects']==0
    ROOT.mkdir(parents=True);sp=ROOT/'unfinished_editorial_scope_inventory.json';save(sp,scope)
    paths=[PRIOR,DOC,RELEASE,START,VIEW,prior_scope,sp,Path(__file__),Path('scripts/generic_speaker_labels_completion_text_v5897.py'),
        Path('work/analysis/generic_speaker_labels_approval_v5887/three_label_source_native_display_approval.json'),
        Path('work/analysis/generic_speaker_labels_atomic_v5889/atomic_validation_receipt.json'),
        Path('work/analysis/generic_speaker_labels_registration_v5890/registration_receipt.json'),
        Path('work/analysis/generic_speaker_labels_regressions_v5891/terminal.json'),
        Path('work/analysis/generic_speaker_labels_retention_v5896/pin_receipt.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PARENT]=deepcopy(old['current_integrated_candidate']);new[PREVIOUS]=old['latest_checkpoint']
    new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new['current_integrated_candidate'].update(path=r['candidate'],sha256=r['candidate_sha256'],profile=r['profile'],
        ARM9_sha256=r['ARM9_sha256'],MESFILE_sha256=r['COMMON_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],manifest=r['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY)
    new[KEY]=dict(summary=SUMMARY,next=NEXT,records=doc['records'],evidence=evidence,new_integrated_label_revisions=3,
        duplicate_dialogue_or_prior_name_completion_credit=0,all_earlier_completed_families_and_counters_exact=True,
        all207_name_scope_open_other204_not_new_editorial_approvals=True,new_label_cold_boots=4,new_label_frames=37404,
        goal_turn_total_new_cold_boots=6,goal_turn_total_new_frames=58806,all_sessions_terminal_and_reaped=True,
        goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
    new[SCOPE]=dict(path=str(sp),sha256=sha(sp.read_bytes()),three_generic_label_leads_closed=True,
        all207_name_review_and_full_editorial_objective_active=True,full_goal_complete=False)
    assert inverse(new)==old;targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<104*1024*1024
    section='## V5897: Three contextual speaker labels integrated in V5891\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;prefix=('# Current editorial handoff - V5897\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[p]=prefix.replace('\n','\r\n').encode('utf-8')+p.read_bytes()
    for name in ['natural_dialogue_workflow.md','editorial_localization_and_layout_standard.md']:
        p=Path('docs')/name
        text='## Current initial speaker-label findings - V5897\n\nThe initial164/165 label lead below is now closed in experimental cumulative V5891 as Man/Woman;172 is Stranger. Exact whole-source contexts,five per-record gates,native names/macros/complete glyphs,bounds and representative scenes,registered release and startup checks are recorded in translations/generic_speaker_labels_manuscript_v2.json and work/analysis/editorial_handoff_verification_v5898/verified_handoff.json. Preserve the earlier pending wording below as historical context. The retrospective207-entry proper-name/role/alias review remains open,including earlier translations and Samwell middle-field consumers. Technical preservation of204 other actors does not supply new editorial approval. Full objective and all source-fidelity rules below remain active.\n\n'
        targets[p]=text.replace('\n','\r\n').encode('utf-8')+p.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz';planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True));print('Eight targets staged;three validated name revisions,no duplicate coverage. All original history preserved.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);phase=p.parse_args().phase
    if phase=='stage':stage()
    else:
        pp=ROOT/'staged_checkpoint.json';plan=read(pp)
        if phase=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();check(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(pp.read_bytes()),complete_inverse_all_old_bytes_and_evidence_exact=True));print('Eight-file deep-inverse preapplication audit passes.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_preapplication_audit.json')['plan_sha256']==sha(pp.read_bytes());check(plan)
            for row in plan['files']:assert Path(row['target']).is_relative_to(Path.cwd().resolve()) and Path(row['planned']).is_relative_to(ROOT.resolve())
            for row in plan['files']:
                with Path(row['target']).open('r+b') as f:f.write(Path(row['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(row['target']).read_bytes())==row['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_eight_targets_exact=True,all_original_history_preserved=True));print('Eight audited progress/ledger targets applied;all history retained.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_eight_targets_exact'];new=check(plan,True);r,doc=gates();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],
                patch=r['patch'],patch_sha256=r['patch_sha256'],profile=r['profile'],ARM9_sha256=r['ARM9_sha256'],
                all_original_root_nested_families_and_counters_preserved=True,**COUNTERS,completed=6282,source_prose=6285,revised=3941,retained=2341,
                SC2=4397,SC3=96,reviewed_routes=4683,completed_routes=4683,three_speaker_label_revisions_integrated=True,
                no_duplicate_dialogue_or_prior_name_credit=True,all587_batches114_accepted18_checks_pass=True,
                all207_name_review_scope_open_other204_not_contextually_approved_by_native_census=True,
                next_Lil_B201_clean_before_English=True,scope_inventory=new[SCOPE],four_label_boots37404_frames=True,
                goal_turn_new_cold_boots=6,goal_turn_new_frames=58806,all_sessions_terminal_and_reaped=True,
                main_V4701_preserved=True,no_promotion_commit_push_or_pruning=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5898 verified:three source-owned labels integrated,no duplicate credit;all6282 reviews/history intact. Full goal active;next freshB201.')
