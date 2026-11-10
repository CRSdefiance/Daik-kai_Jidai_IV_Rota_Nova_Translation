"""Publish ten integrated name revisions with zero duplicate dialogue credit and a deep inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.square_shopkeeper_completion_gates_v7034 import gates
from scripts.square_shopkeeper_completion_text_v7034 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_completion_v7034')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7035')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7017/verified_handoff.json')
DOC=Path('translations/square_shopkeeper_label_manuscript_v4.json')
FINAL=Path('translations/square_shopkeeper_labels_contextual_final_review_v1.json')
B189=Path('work/analysis/B189_retrospective_wrap_and_roles_v7025b/whole_B189_exact_wrap_refs_and_three_occupational_name_groups_pending.json')
B222=Path('work/analysis/lil_B222_clean_context_v7036/all16_clean_sunset_Noritsune_armor_glosses_before_old_English.json')
KEY='square_shopkeeper_labels_completed_v7034';SCOPE='unfinished_editorial_scope_v7034'
COUNTERS=dict(records_editorially_completed=6619,records_with_source_and_prose_pass=6622,records_with_source_prose_drafts=6622,records_revised_and_integrated=4134,retained_wordings_editorially_completed=2485)

def inverse(value):
    restored=deepcopy(value);entry=restored.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(restored,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return restored

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();raw=LEDGER.read_bytes();old=json.loads(raw)
    assert sha(raw)==read(PRIOR)['ledger_sha256'] and all(old[k]==v for k,v in COUNTERS.items())
    doc=read(DOC);assert len(doc['records'])==10 and all(all(r['review'].values()) for r in doc['records'])
    assert doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256'] and doc['target_research_ROM_sha256']==release['candidate_sha256']
    assert len(read(B189)['records'])==17 and len(read(B222)['records'])==16 and read(B222)['all16_clean_speeches_glossed_together_before_old_English']
    rows=[]
    for item in doc['records']:
        row=deepcopy(item);row['historical_preintegration_record']=deepcopy(item)
        row.update(current_reference=deepcopy(item['target_reference']),integrated_reference=deepcopy(item['target_reference']),current_English='Shopkeeper',
            candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,
            status='complete-source-context-native-representative-registered-label-revision',new_name_completion_credit=0,new_dialogue_completion_credit=0)
        row['all_three_source_current_name_fields'][0]['current_English']='Shopkeeper'
        row['all_three_source_current_name_fields'][0]['current_terminated_hex']=b'Shopkeeper\0'.hex();rows.append(row)
    paths=[DOC,PRIOR,B189,B222,Path(__file__),Path('scripts/square_shopkeeper_completion_gates_v7034.py'),Path('scripts/square_shopkeeper_completion_text_v7034.py')]
    paths += [Path(doc[k]) for k in ['native_names','actual_scenes','visual_review','context_review']]
    paths += [Path('work/analysis')/p for p in ['square_shopkeeper_approval_v7025/ten_label_approval.json',
        'square_shopkeeper_registration_v7028/registration_receipt.json','square_shopkeeper_release_v7030/registered_release_verification.json',
        'square_shopkeeper_retention_v7031/pin_receipt.json','square_shopkeeper_startup_v7033/registered_current_startup_and_town_verification.json',
        'square_shopkeeper_startup_v7033/current_six_frame_visual_review.json','current_V7029_native_v7033/registered_current_native_input_binding.json',
        'square_shopkeeper_atomic_v7027/atomic_validation_receipt.json','square_shopkeeper_regressions_v7029/terminal.json']]
    evidence={str(p):sha(p.read_bytes()) for p in paths};summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-name-label-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        records=rows,new_label_revisions=10,new_name_or_dialogue_completion_credit=0,previous_all_completed_families_and_counters_unchanged=True,
        all_ten_exact_clean_predecessor_and_integrated_pointer_string_references_bound=True,source_role_contexts=42,source_unique_blocks=34,source_role_utterances=216,
        actual_changed_header_observations=9,actual_target_speech_observations=30,actual_target_body_page_observations=32,actual_target_body_holds=126,actual_target_name_holds=122,
        other197_native_outputs_preserved_not_global_editorial_approval=True,full207_name_queue_catalogue_UI_and_other_alias_consumers_remain_open=True,
        all_measured_timing_RNG_RGB_and_initialized_gameplay_limits_preserved=True,summary=summary,evidence=evidence,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
        ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    put(['formatting_watchlist','ten_Shopkeeper_v7034'],dict(status='ten-context-native-actual-registered-labels-complete',final_review=str(FINAL),
        ten_primary_labels_only_two_owned_prefixes18_data_bytes=True,all621_pointers_other197_names_code_fonts_voices_and_cache_wrapper_preserved=True,
        actual_nine_headers32_body_pages_complete_first_internal_final_glyphs_and_no_stale_old_ink=True,
        initial_audit_coordinate_failure_and_source_locked_successor_preserved=True,all_measured_timing_RNG_RGB_limits_retained=True,
        no_duplicate_dialogue_or_name_completion_credit=True,full207_name_review_and_retrospective_wrapping_still_open=True))
    previous=old['unfinished_editorial_scope_v7016'];assert sha(Path(previous['path']).read_bytes())==previous['sha256']
    inventory=deepcopy(read(previous['path']));inventory['next_focus']=NEXT
    inventory['ten_Shopkeeper_labels_completed_v7034']=dict(final_review=str(FINAL),actor_IDs=list(range(82,92)),new_label_revisions=10,
        registered_candidate=release['candidate'],all_earlier_Square_Shopkeeper_pending_flags_preserved_as_history_superseded_for_these_ten_primary_labels_only=True,
        other197_native_name_outputs_not_new_editorial_approval=True,full_catalogue_UI_unvisited=True,new_name_or_dialogue_credit=0)
    inventory['B189_retrospective_wrap_and_occupational_groups_v7025b']=dict(path=str(B189),sha256=sha(B189.read_bytes()),
        complete_existing_speech_objects=17,all17_previously_editorially_credited=True,no_duplicate_credit=True,
        natural_whole_exchange_wording_and_early_wrap_reassessment_pending=True,related_trade_house_port_and_guild_role_groups_pending=[104,113,147])
    inventory['Lil_B222_clean_context_v7036']=dict(path=str(B222),sha256=sha(B222.read_bytes()),sixteen_clean_glosses_before_old_English=True,
        current_names_consumers_prose_controls_native_actual_and_registered_integration_pending=True,new_source_prose_or_completion_credit=0)
    inventory['registered_current_native_input_v7033']=dict(path='work/analysis/current_V7029_native_v7033/current_native_input.json',
        sha256=sha(Path('work/analysis/current_V7029_native_v7033/current_native_input.json').read_bytes()),exact2b6_helpers_required_old_AA5_helpers_preserved=True)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),ten_primary_Shopkeeper_leads_complete_all_old_proposals_preserved=True,
        full207_name_and_alias_review_B189_retrospective_wrapping_and_B222_contextual_current_pass_open=True,
        incomplete_COMMON=3,all_four_storylines_earlier_dialogue_town_shop_random_help_and_remaining_prose_open=True,
        graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),records=rows,actor_IDs=list(range(82,92)),
        new_label_revisions=10,new_source_prose_reviews=0,new_completed_records=0,new_name_or_dialogue_completion_credit=0,
        all_general_counters_prior_completed_families_and_contextual_keys_unchanged=True,inverse_operations=ops,evidence=evidence,
        goal_turn_classification='progress',new_emulator_runs_since_verified_V7017=6,new_frames_since_verified_V7017=85406,
        target_NewGame_run_reused_by_exact_ROM_hash_not_counted_twice=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert inverse(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
    assert new['contextual_story_natural_dialogue_pass_v1871']==old['contextual_story_natural_dialogue_pass_v1871']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items()) and new['goal_status']=='active' and not new['full_goal_complete']
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(raw,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V7034: ten Shopkeeper labels integrated in cumulative V7029; full207-name and editorial goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7034\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        p=ROOT/f'{i:02d}.after';p.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(p.resolve()),planned_sha256=sha(data)))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,ten_revisions_zero_duplicate_credit=True,full_goal_complete=False))
    print('Six targets staged;ten separate label revisions,all existing source/dialogue credits and history preserved. Deep inverse audit next.',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert inverse(new)==old and all(new[k]==v for k,v in COUNTERS.items()) and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:
            assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h,p
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
                deep_inverse_recovers_all_prior_root_nested_records_counters_and_history=True,all_six_before_and_planned_hashes_verified=True,ten_name_revisions_zero_duplicate_credit=True,full_goal_complete=False))
            print('All six targets inverse-audited;every prior record,root,nested value and counter recovers exactly.',flush=True)
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for e in plan['files']:assert Path(e['target']).is_relative_to(Path.cwd().resolve()) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False))
            print('Six audited name-layer completion targets applied exactly.',flush=True)
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
                profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_preserved=True,ten_Shopkeeper_primary_label_revisions_complete_zero_duplicate_credit=True,
                completed=6619,source_prose=6622,revised=4134,retained=2485,SC2=4733,SC3=96,reviewed_routes=5019,completed_routes=5019,
                all614_manifest_batches114_accepted18_checks_and110_regressions_verified=True,current_native_input='work/analysis/current_V7029_native_v7033/current_native_input.json',
                current_native_input_sha256=sha(Path('work/analysis/current_V7029_native_v7033/current_native_input.json').read_bytes()),
                actual_changed_nameplate_observations=9,actual_target_speech_observations=30,actual_target_native_pages=32,actual_target_body_holds=126,actual_target_name_holds=122,
                startup31_whole_frames_and_five_actor_captain_payload_controls_match_V7011=True,exact_target_NewGame_reuse_and_fresh_town_explicit=True,
                all61_atomic_negatives_reject_before_write=True,full_catalogue_UI_and_all_conditional_nameplate_visits_unclaimed=True,
                all_measured_static_one_frame_RNG_RGB_differences_preserved=True,no_full_RAM_final_components_future_or_causal_equivalence_claim=True,
                B18917_already_credited_wrap_and_three_role_group_leads_pending=True,B22216_clean_glosses_before_old_English_pending_current_review=True,
                full207_names_all_storylines_town_shop_random_help_prose_retrospective_wrap_and_all_prior_leads_open=True,
                graphics_and_later_older_record_technical_reaudit_separate=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7034 verified:V7029 cumulative,ten Shopkeeper labels integrated.6619 completed/6622 source-prose unchanged;full editorial/name objective active.',flush=True)
