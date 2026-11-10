"""Preserve B200 draft/name progress with a deep inverse and unchanged coverage counters."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B200_checkpoint_text_v5841 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_and_names_checkpoint_v5841')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5842')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5822/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Lil_B200_clean_context_prose_and_anonymous_name_v5841'
SCOPE='unfinished_editorial_scope_v5841'
PREVIOUS='previous_latest_checkpoint_before_B200_and_names_v5841'
OLD_SCOPE='unfinished_editorial_scope_v5821'
COUNTERS=dict(records_editorially_completed=6263,records_with_source_and_prose_pass=6266,records_revised_and_integrated=3928,retained_wordings_editorially_completed=2335)
PACKET=Path('work/analysis/lil_B200_source_v5826/all19_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B200_clean_context_v5825/all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json')
DOC=Path('translations/lil_B200_editorial_manuscript_v1.json')
CONTEXT=Path('work/analysis/lil_B200_comparison_v5838/complete_clean_context_source_scene_names_role_label_and_terms.json')
ACTUAL=Path('work/analysis/lil_B200_source_paths_v5837/one_actual_source_path_and_complete_command_intervals.json')
NAMES=Path('work/analysis/collapsed_speaker_lead_v5832/all_route_literal_uses_exact_name_fields_and_localization_finding.json')

def inverse(value):
    old=deepcopy(value);old['latest_checkpoint']=old.pop(PREVIOUS);old.pop(KEY);old.pop(SCOPE);return old

def check(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
        assert sha(gzip.decompress(Path(item['before']).read_bytes()))==item['before_sha256']
    for p,digest in plan['evidence'].items():assert sha(Path(p).read_bytes())==digest
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()));new=read(plan['files'][0]['planned'])
    assert inverse(new)==old and sha(encode_ledger(old))==plan['files'][0]['before_sha256']
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete'];prior=read(PRIOR)
    assert prior['ledger_sha256']==plan['files'][0]['before_sha256']
    for key in ['candidate','patch']:assert sha(Path(prior[key]).read_bytes())==prior[key+'_sha256']
    assert read('translations/release_stack.json')['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return new

def stage():
    assert not ROOT.exists() and not VERIFY.exists();before=LEDGER.read_bytes();old=json.loads(before);prior=read(PRIOR)
    assert sha(before)==prior['ledger_sha256'] and not any(k in old for k in [KEY,SCOPE,PREVIOUS])
    packet,gloss,doc,context,actual,names=map(read,[PACKET,GLOSS,DOC,CONTEXT,ACTUAL,NAMES]);rows=doc['records']
    assert len(rows)==len(gloss['records'])==19 and gloss['prior_English_speech_unread']
    assert doc['revised']==13 and doc['retained']==6 and doc['source_prose_or_completion_credit_added']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in rows)
    known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    assert len(known)==6263 and not known&{historical_key(r) for r in rows}
    assert packet['current_ROM_sha256']==prior['candidate_sha256']
    assert context['source_actual_speeches']==19 and not context['offline_only_speeches'] and len(context['viewed_source_sheets'])==8
    assert actual['source_end926_return_frame']==7676 and len(actual['command_pairs'])==40
    assert names['source_blocks_scanned']==1307 and len(names['selected_native_blocks'])==4
    assert sum(len(b['direct_role_speeches']) for b in names['selected_native_blocks'])==32
    assert context['actor172_label_localization_draft']['proposed']=='Stranger' and context['actor172_label_localization_draft']['target_not_encoded_or_applied']
    old_scope=Path(old[OLD_SCOPE]['path']);assert sha(old_scope.read_bytes())==old[OLD_SCOPE]['sha256']
    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT
    scope['next_Lil_B200_clean_review_pending'].update(clean19_source_gloss_path=str(GLOSS),source_current_packet=str(PACKET),
        manuscript=str(DOC),revisions=13,retentions=6,clean_first_glosses=19,new_completion_credit=0,
        source_controls_and_all19_Japanese_scene_speeches_observed=True,native_English_layout_reference_actual_compiler_and_release_pending=True)
    scope['B200_anonymous_role_label_v5841']=dict(actor_ID=172,current='Collapsed Person',draft='Stranger',source='行き倒れ',
        source_secondary='アフリカ水夫',current_native_consumers=2,direct_literal_source_speeches=32,complete_identical_speech_exchanges=4,
        source_header_only_difference_in_SC3_byte2=True,whole_context=str(CONTEXT),exact_source_current_fields_and_owners=str(NAMES),
        proposed_target_not_applied=True,target_native_display_substitution_and_registered_release_pending=True,new_name_review_credit=0)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    ROOT.mkdir(parents=True);scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
    paths=[PRIOR,PACKET,GLOSS,DOC,CONTEXT,ACTUAL,NAMES,old_scope,scopepath,Path(__file__),Path('scripts/lil_B200_checkpoint_text_v5841.py'),
        Path('scripts/lil_B200_prose_v5839.py'),Path('scripts/author_lil_B200_v5840.py'),
        Path('work/analysis/lil_B200_author_v5840/all19_clean_first_contextual_decisions.json'),
        Path('work/analysis/lil_B200_voices_v5827/current207_catalog_eight_voices_and_two_source_selectors.json'),
        Path('work/analysis/lil_B200_dispatches_v5828/all19_source_current_dispatches_no_macros_and12_control_leaves.json'),
        Path('work/analysis/lil_B200_entry_v5829/source_EV2_B200_action_dependency_and_native_getter_binding.json'),
        Path('work/analysis/lil_B200_branches_v5830/original_relative_skip_operand_proof.json'),
        Path('work/analysis/lil_B200_names_v5831/four_original_progressive_and_catalogue_name_consumers.json'),
        Path('work/analysis/lil_B200_controls_v5833/twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end.json'),
        Path('work/analysis/lil_B200_source_fixture_v5835/complete_B200_source_B22_fixture.json'),
        Path('work/analysis/lil_B200_source_fixture_v5835/pin_receipt.json'),
        Path('work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json'),
        Path('work/analysis/lil_B199_runs_v5818/newgame_terminal.json'),Path('work/analysis/lil_B199_runs_v5818/town_terminal.json'),
        Path('releases/all_routes_unified_v5816/verification.json'),Path('releases/all_routes_unified_v5816/README.md'),Path('translations/release_stack.json')]
    assert read('work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json')['observer_host_slots_restored']
    for terminal in ['work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json',
        'work/analysis/lil_B199_runs_v5818/newgame_terminal.json','work/analysis/lil_B199_runs_v5818/town_terminal.json']:
        assert read(terminal)['terminal']
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,all19_B200_objects_uncredited=True,
        revised=13,retained=6,actor172_Strander_metadata_typo_in_v1_flag_not_player_prose=True,
        new_label_Stranger_draft_not_applied=True,existing_164_165_Man_Woman_drafts_and207_queue_preserved=True,
        new_research_ROMs=1,new_source_Japanese_cold_boots=1,new_source_Japanese_frames=13001,
        total_goal_turn_new_cold_boots=3,total_goal_turn_new_frames=34403,all_sessions_terminal_and_reaped=True,
        goal_turn_classification='progress',previous_goal_turn_classification='progress',no_duplicate_credit=True,full_goal_complete=False)
    new[SCOPE]=dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),Lil_B200_uncredited_objects=19,
        retrospective207_name_queue_and_paired_role_labels_preserved=True,actor172_Stranger_target_pending=True,full_goal_complete=False)
    assert inverse(new)==old;targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
    section='## V5841: B200 clean-source contextual draft and anonymous speaker-label review\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V5841\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz';planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True))
    print('Six targets staged;B20019 prose objects and actor172 label remain uncredited and unintegrated.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);phase=p.parse_args().phase
    if phase=='stage':stage()
    else:
        pp=ROOT/'staged_checkpoint.json';plan=read(pp)
        if phase=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();check(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(pp.read_bytes()),all_before_planned_evidence_hashes_exact=True,deep_nested_inverse_and_exact_old_ledger_bytes_verified=True))
            print('Six-file preapplication and complete inverse audit pass.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_preapplication_audit.json')['plan_sha256']==sha(pp.read_bytes());check(plan)
            for item in plan['files']:
                assert Path(item['target']).is_relative_to(Path.cwd().resolve()) and Path(item['planned']).is_relative_to(ROOT.resolve())
            for item in plan['files']:
                with Path(item['target']).open('r+b') as f:f.write(Path(item['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_exact=True,all_original_history_preserved=True));print('Six audited checkpoint targets applied with original history intact.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_exact'];new=check(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
                patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,**COUNTERS,
                completed=6263,source_prose=6266,revised=3928,retained=2335,SC2=4378,SC3=96,reviewed_routes=4664,completed_routes=4664,
                B200_uncredited_clean_glosses=19,B200_draft_revisions=13,B200_draft_retentions=6,B200_source_current_dispatches=38,B200_native_name_consumers=4,
                B200_actual_Japanese_speech_panels=19,B200_Japanese_cold_boots=1,B200_Japanese_frames=13001,B200_end_frame=7676,
                actor172_source_literal_uses=32,actor172_identical_complete_speech_exchanges=4,actor172_Stranger_target_pending=True,
                actor172_unused_secondary_field_not_silently_promoted=True,paired164_165_Man_Woman_drafts_preserved=True,catalog_queue=207,
                goal_turn_new_cold_boots=3,goal_turn_new_frames=34403,earlier_B199_source_English_content_runs_reused=True,
                no_promotion_commit_push_or_pruning=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5842 verified:19 B200 drafts and speaker-name progress saved;V5816/main/counters unchanged. Full goal active.')
