"""Credit thirteen disjoint B207 records only after release/startup; conserve all history."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B207_completion_text_v6385 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B207_completion_v6385');VERIFY=Path('work/analysis/editorial_handoff_verification_v6386')
LEDGER=Path('translations/editorial_review_current_v1.json');DOC=Path('translations/lil_B207_editorial_manuscript_v6.json');FINAL=Path('translations/lil_B207_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B207_release_v6381/registered_release_verification.json');START=Path('work/analysis/lil_B207_startup_v6384/cold_boot_Lil_startup_town_verification.json');VIEW=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B207_actual_v6374/all13_English_panels_complete_native_holds24_commands_and_source_comparison.json');TRANSITIONS=Path('work/analysis/lil_B207_actual_review_v6376/viewed13_panels51_native_holds_and_honest_timing_RNG_prompt_scope.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6364/verified_handoff.json');REG=Path('work/analysis/lil_B207_registration_v6379/registration_receipt.json');PIN=Path('work/analysis/lil_B207_retention_v6382/pin_receipt.json')
FAMILY='Lil-B207-Minotaur-Axe-uncertain-island-clue-conditional-search-and-undecided-gift13';KEY='Lil_B207_completion_v6385';SCOPE='unfinished_editorial_scope_v6385';WATCH='Lil_B207_v6385'
ROOTVALUES=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','current_integrated_candidate','latest_checkpoint']
FRESHVALUES=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']

def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all598_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6327']
    assert start['all_current_requested_and_final_framebuffers_equal_V6327'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==71 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_native_text_and_nameplate_holds'])==(13,13,51)
    assert not any(actual[k] for k in ['failures','paired_nontext_region_differences','command_result_differences','command_UI_word_differences','offline_only_display_IDs'])
    assert actual['source_and_English_all24_commands15_source_plus9_initializers_observed'] and actual['all_command_paths_and_results_preserved'] and actual['all_jobs_terminal_and_reaped']
    assert transitions['no_open_translation_specific_display_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==5
    assert [len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[13,3,6]
    state=read(transitions['postscene_native_state_proof']);assert sha(Path(transitions['postscene_native_state_proof']).read_bytes())==transitions['postscene_native_state_proof_sha256']
    assert all(state['five_native_component_equality'].values()) and state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['final_PRNG_seeds']==[940971730,2496127907]
    assert transitions['all13_timing_three_interval_RNG_six_prompt_RGB_and_final_PRNG_differences_retained'] and transitions['broad_postscene_full_RAM_future_world_equivalence_unproven'] and transitions['natural_event207_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed'] and transitions['final11001_both_following_B120_still_active_black_upper']
    tests=read('work/analysis/lil_B207_regressions_v6380/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B207_reference_v6367_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==598 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release

def restore(value):
    d=deepcopy(value);entry=d.pop(KEY);back=entry['inverse_preserved_values'];d.pop(SCOPE);d.update(back['root_values']);assert d['completed_editorial_families'].pop()['id']==FAMILY
    fresh=d['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert fresh[k][-13:]==entry['record_keys'];del fresh[k][-13:]
    assert fresh['record_IDs'][-13:]==entry['record_IDs'];del fresh['record_IDs'][-13:]
    assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values']);active=d['active_source_prose_drafts']
    assert active['manuscripts'].pop()==str(DOC) and active['route_record_subsets_pending'].pop(str(DOC))==[];active['note']=back['active_note']
    assert d['coverage_units'].pop()['id']==FAMILY;d['coverage_units'][back['route_unit_index']]=back['route_unit'];d['formatting_watchlist'].pop(WATCH)
    return d

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':7}
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[207];refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','current_native_extent','source_prose_or_completion_credit_added','formatting_reason','current_native_UI_body_explicit_unexecuted_boundary']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row};body=value[1:];template=body.decode('cp932');logical=' '.join(template.split());newref=dict(block=207,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
            command=next(c for c in mapping['blocks'][0]['mapped_native_commands'] if c['new_offset']==at-5);assert command['word']==0x4000 and command['new_native_extent']>=len(value)+6
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),record_index=newref['record_index'],current_record_index=newref['record_index'],integrated_native_extent=command['new_native_extent'],current_native_extent=command['new_native_extent'],current_English=template,current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=template,current_effective_paragraph=logical,registered_runtime_catalog_entry=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,current_native_voice_macro_entry_and_context_pending=False,native_plane_verified_not_actual_English_gameplay=False,actual_English_complete_panel_and_native_holds_verified=True,current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release',current_native_UI_body_explicit_unexecuted_boundary=False,
                formatting_reason='Historical native-only proof/UI limits preserved. Separate actual evidence verifies all13 complete English/current-style11-name panels,51 holds,all24 fixture command paths/results and town return. One exact it/if ordinary boundary and three rowcount reasons remain;no glyph,bounds,pagination or control waiver.',actual_complete_display_proof=str(ACTUAL),actual_complete_display_proof_sha256=sha(ACTUAL.read_bytes()))
            assert logical==row['english'].split('}',1)[1] and all(row['review'].values())
        oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows};assert len(oldkeys)==6415 and len(keys)==13 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6415 and not fresh['pending_record_keys']
        summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        paths=[DOC,RELEASE,START,VIEW,REG,PIN,ACTUAL,TRANSITIONS,PRIOR,Path(doc['reference_map']),Path(__file__),Path('scripts/lil_B207_completion_text_v6385.py'),Path('work/analysis/lil_B207_regressions_v6380/terminal.json')];evidence={str(p):sha(p.read_bytes()) for p in paths}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=6,retained=7,source_prose_and_completion_credit_added_once=13,previous_B207_objects_uncredited=True,all13_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_unique_speeches=13,actual_speech_observations=13,offline_only_speeches=0,actual_matching_holds=51,natural_event207_not_selected=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');back=dict(root_values={k:deepcopy(old[k]) for k in ROOTVALUES},fresh_values={k:deepcopy(fresh[k]) for k in FRESHVALUES},active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[207],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=6,retained_count=7,fresh_revisions=6,fresh_retentions=7,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=6428,records_with_source_and_prose_pass=6431,records_with_source_prose_drafts=6431,records_revised_and_integrated=4011,retained_wordings_editorially_completed=2417)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC2.DK4']==4529;new[key]['/data/SC2.DK4']=4542
        keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871'];note='6428 contextual rereads integrated;source/prose6431. All13 B207 records counted once. Full four-storyline,earlier dialogue,shared town/shop/random/Help/prose,207-name/role/alias and premature-wrap review remains active.'
        for key in ['record_keys','integrated_record_keys']:f[key].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=6428,fresh_pass_records_integrated=6428,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=13,final_review=str(FINAL),new_revisions=6,justified_retentions=7,new_completed_records=13,historical_reconciliation_only=False,actual_selected_source207_events=[],actual_B22_content_speeches=13,actual_speech_observations=13,offline_only_speeches=0,complete_text_nameplate_holds=51,current_candidate_emulator_runs=2,current_candidate_frames=21402,source_English_content_runs=2,source_English_content_frames=22002,new_English_content_runs=1,new_English_content_frames=11001,reused_source_frames=11001))
        active=new['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'] and str(DOC) not in active['route_record_subsets_pending'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
        new['coverage_units'][routeindex].update(reviewed_route_records=4828,completed_route_records=4828,next=NEXT);new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[207],completion_credit_added=13,final_review=str(FINAL),actual_source_event207_selected=False,current_candidate_emulator_runs=2,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all13-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),all15_commands13_preambles_one_A000_complete_end_and_original_results_preserved=True,one_exact_source_ordinary_boundary_three_rowcount_reasons=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False);current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});new['current_integrated_candidate']=current;new['latest_checkpoint']=summary
        prior_scope=old['unfinished_editorial_scope_v6363'];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256'];inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
        inventory['Lil_B207_completed_v6385']=dict(final_review=str(FINAL),completed_objects=13,registered_candidate=release['candidate'],actual_speeches=13,complete_native_text_nameplate_holds=51,all15_source_commands_and9_initializers_observed=True,natural_event207_not_selected=True,old_pending_native_reference_actual_flags_preserved_as_history_and_superseded_here=True,all13timing3RNG6promptRGB_and_different_final_PRNG_limits_preserved=True)
        inventory['next_Lil_B208_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=208,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B207_actor_macro_item_conditional_search_effect_or_end_assumptions_inherited=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4828,completed_route_records=4828,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B207_previously_uncredited_objects_completed=13,next_Lil_B208_clean_review_pending=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_and_role_labels_open=True,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=13,new_completed_records=13,revised=6,retained=7,goal_turn_classification='progress',previous_goal_turn_classification='progress',goal_turn_new_emulator_runs=3,goal_turn_new_frames=32403,reused_verified_source_frames=11001,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V6385: B207 complete exchange integrated once in cumulative V6380\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V6385\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(target.read_bytes(),mtime=0))
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=13,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;13 disjoint reviews proposed once. Deep-inverse audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6428,6431,4011,2417)
        for entry in plan['files']:assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256'] and sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates()
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,exactly13_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False));print('Six targets,all historical values and13 disjoint new keys audited.')
        elif mode=='apply':
            assert not (ROOT/'native_application_receipt.json').exists() and read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False));print('Six audited files applied exactly.')
        else:
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists() and len(read(FINAL)['records'])==13
            allkeys={historical_key(r) for family in new['completed_editorial_families'] for r in family['records']};assert len(allkeys)==6428
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_preserved=True,exactly13_new_disjoint_source_prose_and_completed_records=True,completed=6428,source_prose=6431,revised=4011,retained=2417,SC2=4542,SC3=96,reviewed_routes=4828,completed_routes=4828,all598_manifest_batches114_accepted18_checks_verified=True,actual_unique_B207_speeches=13,actual_speech_observations=13,offline_only_B207_speeches=0,actual_matching_holds=51,startup31_frames_and_five_actor_controls_match_V6327=True,source207_natural_activation_original_location_earned_progress_full_quest_inventory_and_effect_semantics_not_claimed=True,measured13timing3RNG6promptRGB_and_different_final_PRNG_limits_preserved=True,no_broad_postscene_equivalence_or_causal_claim=True,next_Lil_B208_clean_review_pending=True,retrospective207_name_queue_and_all_prior_leads_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V6380 verified:6428 completed/6431 source-prose. B208 and the full broader editorial/name-review objective remain active.')
