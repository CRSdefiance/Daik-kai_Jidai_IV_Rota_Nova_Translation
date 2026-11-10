"""Preserve B200 draft/name progress with a deep inverse and unchanged coverage counters."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B200_reference_text_v5866 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_reference_checkpoint_v5866')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5867')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5842/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Lil_B200_reference_approved_uncredited_v5866'
SCOPE='unfinished_editorial_scope_v5866'
PREVIOUS='previous_latest_checkpoint_before_B200_references_v5866'
OLD_SCOPE='unfinished_editorial_scope_v5841'
COUNTERS=dict(records_editorially_completed=6263,records_with_source_and_prose_pass=6266,records_revised_and_integrated=3928,retained_wordings_editorially_completed=2335)
PACKET=Path('work/analysis/lil_B200_source_v5826/all19_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B200_clean_context_v5825/all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json')
DOC=Path('translations/lil_B200_editorial_manuscript_v5.json')
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
    assert all(all(r['review'].values()) for r in rows)
    approval=read('work/analysis/lil_B200_reference_approval_v5865/reference_approval.json')
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['native_approved_revisions']==13 and approval['native_approved_retentions']==6
    assert approval['all19_source_native_reference_and_representative_rules_approved']
    assert approval['all_prior_evidence_and_measured_timing_prompt_cloud_PRNG_differences_preserved']
    sample=read(doc['representative_proof'])
    assert sample['all19_actual_native_panels73_complete_holds_and_changed_scene_source_regions_match']
    assert sample['sampled_nontext_frames']==182 and sample['nontext_equal_samples']==172
    assert sample['command_start_or_return_difference_count']==19 and sample['speech_duration_difference_count']==8
    assert sample['later_sampled_whole_RGB_difference_count']==16 and sample['PRNG_seeds_differ']
    assert all(sample['final_native_component_equality'].values()) and sample['Stranger_label_target_not_applied_and_name_review_still_open']
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
    scope['historical_Lil_B200_clean_context_before_v5866']=scope.pop('next_Lil_B200_clean_review_pending')
    scope['next_Lil_B200_reference_approved_uncredited_v5866']=dict(file_path='/data/SC2.DK4',block=200,reviewed_objects=19,
        manuscript=str(DOC),reference_map=doc['reference_map'],representative_proof=doc['representative_proof'],
        native_revisions=13,native_retentions=6,new_completion_credit=0,actual_English_speeches=19,complete_matching_holds=73,
        source_commands=31,source_stored_bytes=932,target_stored_bytes=828,source_end=926,target_end=824,
        source_tailzeros=2,target_tailzeros=0,all19_native_glyph_planes_and152_alignments_pass=True,
        native_source_consumer_negatives=18,formatter_negatives=28,final_stored_macro_cases=76,
        source_cold_boot_reused=True,new_English_cold_boots=1,new_English_frames=13001,
        speech_duration_changes=8,shifted_pairs=19,later_prompt_differences=6,later_sailing_cloud_differences=10,
        final_PRNG_seeds_differ=True,complete_timing_and_cloud_native_object_untraced=True,
        atomic_compiler_registered_release_patch_and_current_startup_pending=True)
    scope['B200_anonymous_role_label_v5841']=dict(actor_ID=172,current='Collapsed Person',draft='Stranger',source='行き倒れ',
        source_secondary='アフリカ水夫',current_native_consumers=2,direct_literal_source_speeches=32,complete_identical_speech_exchanges=4,
        source_header_only_difference_in_SC3_byte2=True,whole_context=str(CONTEXT),exact_source_current_fields_and_owners=str(NAMES),
        proposed_target_not_applied=True,target_native_display_substitution_and_registered_release_pending=True,new_name_review_credit=0)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    ROOT.mkdir(parents=True);scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
    paths=[PRIOR,PACKET,GLOSS,DOC,CONTEXT,ACTUAL,NAMES,old_scope,scopepath,Path(__file__),Path('scripts/lil_B200_reference_text_v5866.py'),
        Path('work/analysis/lil_B200_reference_approval_v5865/reference_approval.json'),Path(doc['reference_map']),Path(doc['representative_proof']),
        Path(doc['final_padding_proof']),Path(doc['relocated_control_proof']),Path(doc['termination_decode_proof']),Path(doc['postscene_native_state_proof']),
        Path(doc['native_font_proof']),Path('work/analysis/lil_B200_native_approval_v5849/all19_source_prose_current_native_approval.json'),
        Path('work/analysis/lil_B200_phrase_layout_v5846/complete_courtesy_requests_and_source_bound_formatter_successors.json'),
        Path('work/analysis/lil_B200_English_run_v5860_reviewed_English/terminal.json'),
        Path('work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json'),
        Path('work/analysis/lil_B200_research_v5853/research_image_receipt.json'),
        Path('work/analysis/lil_B200_English_fixture_v5859/pin_and_runner_receipt.json'),
        Path('work/analysis/lil_B200_screen_review_v5864/paired_scene_return_and_measured_sailing_difference_sheets.json'),
        Path('work/analysis/lil_B200_postscene_difference_v5863/unmodified_final_difference_pixel_inventory.json'),
        Path('releases/all_routes_unified_v5816/verification.json'),Path('translations/release_stack.json')]
    for terminal in ['work/analysis/lil_B200_English_run_v5860_reviewed_English/terminal.json','work/analysis/lil_B200_source_run_v5836_clean_Japanese/terminal.json']:
        assert read(terminal)['terminal'] and read(terminal)['observer_host_slots_restored']
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,all19_B200_objects_uncredited=True,revised=13,retained=6,
        all19_native_planes152_alignments18_consumer28_formatter_negatives_approved=True,
        actual19_English_panels73_complete_holds=True,speech_duration_changes=8,shifted_start_return_pairs=19,
        sampled_nontext_equal=172,sampled_nontext_total=182,later_prompt_differences=6,later_sailing_cloud_differences=10,
        final_PRNG_seeds_differ=True,no_broad_simulation_or_complete_causal_claim=True,
        new_label_Stranger_draft_not_applied=True,existing_164_165_Man_Woman_drafts_and207_queue_preserved=True,
        new_research_ROMs=2,new_English_cold_boots=1,new_English_frames=13001,reused_Japanese_cold_boots=1,
        all_sessions_terminal_and_reaped=True,goal_turn_classification='progress',previous_goal_turn_classification='progress',no_duplicate_credit=True,full_goal_complete=False)
    new[SCOPE]=dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),Lil_B200_uncredited_objects=19,
        retrospective207_name_queue_and_paired_role_labels_preserved=True,actor172_Stranger_target_pending=True,full_goal_complete=False)
    assert inverse(new)==old;targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
    section='## V5866: B200 complete native/reference and19 English panels approved;registered release pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V5866\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz';planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True))
    print('Six targets staged;B20019 approved reference objects remain uncredited pending registered release.')

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
                B200_uncredited_objects=19,B200_approved_revisions=13,B200_approved_retentions=6,
                B200_native_planes=19,B200_native_alignments=152,B200_source_consumer_negatives=18,B200_formatter_negatives=28,
                B200_final_stored_macro_cases=76,B200_actual_English_panels=19,B200_complete_matching_holds=73,
                source_return=7676,English_return=7677,eight_speech_duration_changes=True,shifted_start_return_pairs=19,
                sampled_nontext_equal=172,sampled_nontext_total=182,later_prompt_differences=6,later_sailing_cloud_differences=10,
                final_PRNG_seeds_differ=True,no_broad_simulation_or_complete_causal_claim=True,
                new_research_ROMs=2,new_English_cold_boots=1,new_English_frames=13001,reused_Japanese_cold_boots=1,
                actor172_Stranger_target_pending=True,paired164_165_Man_Woman_drafts_preserved=True,catalog_queue=207,
                registered_release_compiler_and_current_startup_pending=True,no_promotion_commit_push_or_pruning=True,
                main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5867 verified:19 B200 reference/actual-approved objects remain uncredited;V5816/main/counters unchanged. Full goal active.')
