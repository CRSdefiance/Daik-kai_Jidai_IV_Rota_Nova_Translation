"""Credit nineteen newly integrated reviews once;preserve the complete ledger history."""
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

ROOT=Path('work/analysis/lil_B200_completion_v5877')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5878')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B200_editorial_manuscript_v5.json')
MENU=None
FINAL=Path('translations/lil_B200_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B200_release_v5873/registered_release_verification.json')
START=Path('work/analysis/lil_B200_startup_v5875/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=Path('work/analysis/lil_B200_registration_v5871/registration_receipt.json')
ACTUAL=Path('work/analysis/lil_B200_actual_v5861/nineteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
TRANSITIONS=Path('work/analysis/lil_B200_reference_approval_v5865/representative_display_control_and_transition_reconciliation.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5867/verified_handoff.json')
FAMILY='Lil-B200-collapse-inn-rescue-doctor-denial-thanks-and-Charm19'
KEY='Lil_B200_completion_v5877'
PARENT_KEY='previous_integrated_candidate_before_Lil_B200_completion_v5877'
PREVIOUS='previous_latest_checkpoint_before_Lil_B200_completion_v5877'
SCOPE='unfinished_editorial_scope_v5877'
WATCH='Lil_B200_v5877'
from scripts.lil_B200_completion_text_v5877 import NEXT,DETAILS

def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all586_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V5816']
    assert start['all_current_requested_and_final_framebuffers_equal_V5816'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed']
    assert view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==110 and reg['all_negatives_reject_before_mutation']
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19 and actual['complete_matching_holds']==73
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_source_indices']
    assert len(actual['actual_timing_differences'])==19 and len(actual['later_whole_RGB_differences'])==16
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[7676,7677]
    assert transitions['all19_actual_native_panels73_complete_holds_and_changed_scene_source_regions_match']
    assert transitions['original_inn_transition_picture47xx6003_two_A000_final4640_and_complete_end_results_preserved']
    assert transitions['no_open_translation_specific_display_or_control_finding'] and transitions['representative_shared_rules_approved']
    assert transitions['sampled_nontext_frames']==182 and transitions['nontext_equal_samples']==172
    assert transitions['following_sailing_cloud_difference_samples']==10 and transitions['command_start_or_return_difference_count']==19
    assert transitions['speech_duration_difference_count']==8 and transitions['all_nonspeech_control_durations_equal']
    assert transitions['source_and_English_return_frames']==[7676,7677] and transitions['later_sampled_whole_RGB_difference_count']==16
    assert transitions['six_prompt_blink_samples_and_ten_following_sailing_cloud_samples_visually_reviewed']
    assert transitions['PRNG_seeds_differ'] and transitions['complete_RNG_timing_cause_not_traced']
    assert len(set(transitions['final_13001_PRNG_seeds']))==2 and all(transitions['final_native_component_equality'].values())
    assert transitions['no_broad_world_effect_full_RAM_future_random_sequence_or_simulation_equivalence_claim']
    assert transitions['no_natural_event_activation_original_location_full_route_or_hardware_claim']
    assert transitions['Stranger_label_target_not_applied_and_name_review_still_open']
    assert transitions['total_successful_frames']==26002 and actual['actual_source_and_English_cold_boots']==2
    for evidence in [actual['evidence'],transitions['evidence']]:
        for path,digest in evidence.items():assert sha(Path(path).read_bytes())==digest
    tests=read('work/analysis/lil_B200_regressions_v5872/terminal.json')
    assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']==transitions['research_ROM_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==586 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B200_retention_v5876/pin_receipt.json')['all_prior_pins_preserved']
    return release

def restore(new):
    inverse=deepcopy(new);entry=inverse.pop(KEY);back=entry['inverse_preserved_values']
    inverse['current_integrated_candidate']=inverse.pop(PARENT_KEY);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(SCOPE)
    assert inverse['completed_editorial_families'].pop()['id']==FAMILY;inverse.update(back['root_values'])
    fresh=inverse['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert fresh[k][-19:]==entry['record_keys'];del fresh[k][-19:]
    assert fresh['record_IDs'][-19:]==entry['record_IDs'];del fresh['record_IDs'][-19:]
    assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values'])
    active=inverse['active_source_prose_drafts']
    for p in reversed([DOC]):
        assert active['manuscripts'].pop()==str(p) and active['route_record_subsets_pending'].pop(str(p))==[]
    active['note']=back['active_note']
    assert inverse['coverage_units'].pop()['id']==FAMILY;inverse['coverage_units'][back['route_unit_index']]=back['route_unit'];inverse['formatting_watchlist'].pop(WATCH)
    return inverse

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':13,'retain-wording':6} and doc['source_prose_or_completion_credit_added']==0
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[200]
        refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for command in mapping['blocks'][0]['choice_commands']:
            refs.update({r['id']:{**r,'target_hex':block[r['new_offset']:r['new_offset']+r['new_length']].hex(),'target_command_offset':command['new_offset']} for r in command['label_references']})
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);speech='source_selector' in row
            assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at
            if speech:assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['registered_runtime_catalog_entry','current_effective_macro_template_English','current_effective_paragraph','current_raw_storage_English','current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','source_prose_or_completion_credit_added','command_offset']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
            body=value[1:] if speech else value;template=body.decode('cp932');runtime=template.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')
            logical=' '.join(template.split())
            for macro in ['FI','FA','FO']:logical=logical.replace(macro,'{MACRO:'+macro+'}')
            newref=dict(block=200,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'))
            if speech:newref['header_offset']=at-5
            else:newref['command_offset']=ref['target_command_offset'];row['current_command_offset']=ref['target_command_offset']
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),
                record_index=newref['record_index'],current_record_index=newref['record_index'],current_English=template,current_stored_English=template,
                current_raw_storage_English=template,current_effective_runtime_English=runtime,current_effective_macro_template_hex=body.hex(),
                current_effective_macro_template_English=template,current_effective_paragraph=logical,registered_runtime_catalog_entry=None,
                completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,
                current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,
                decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release')
            assert row['current_effective_paragraph']==(row['english'].split('}',1)[1] if speech else row['english']) and all(row['review'].values())
        oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
        assert len(oldkeys)==6263 and len(keys)==19 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6263 and not fresh['pending_record_keys']
        summary=DETAILS+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS,PRIOR,Path(doc['reference_map']),Path(doc['native_font_proof']),
            Path('work/analysis/lil_B200_regressions_v5872/terminal.json'),Path('work/analysis/lil_B200_retention_v5876/pin_receipt.json'),Path(__file__)]}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
            revised=13,retained=6,source_prose_and_completion_credit_added_once=19,previous_B200_objects_uncredited=True,all19_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,
            actual_unique_speeches=19,offline_only_speeches=0,actual_menu_cases=0,actual_matching_holds=73,natural_event200_not_selected=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);rootnames=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated',
            'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']
        freshnames=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']
        routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
        back=dict(root_values={k:deepcopy(old[k]) for k in rootnames},fresh_values={k:deepcopy(fresh[k]) for k in freshnames},
            active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[200],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,
            revised_count=13,retained_count=6,fresh_revisions=13,fresh_retentions=6,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=6282,records_with_source_and_prose_pass=6285,records_with_source_prose_drafts=6285,records_revised_and_integrated=3941,retained_wordings_editorially_completed=2341)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC2.DK4']==4378;new[key]['/data/SC2.DK4']=4397
        keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871']
        note='6282 contextual rereads integrated;source/prose6285. B200 counted once;all wider families,retrospective names/role labels and earlier premature wrapping remain open.'
        for key in ['record_keys','integrated_record_keys']:f[key].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=6282,fresh_pass_records_integrated=6282,latest_contextual_manuscript=str(DOC),
            latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=19,final_review=str(FINAL),new_revisions=13,justified_retentions=6,new_completed_records=19,historical_reconciliation_only=False,
            actual_selected_source200_events=[],actual_B22_content_speeches=19,offline_only_speeches=0,actual_menu_cases=0,new_current_candidate_emulator_runs=2,explicit_content_fixture_runs=2,batch_new_frames=47404,goal_turn_new_frames=21402))
        active=new['active_source_prose_drafts']
        for p in [DOC]:
            assert str(p) not in active['manuscripts'] and str(p) not in active['route_record_subsets_pending']
            active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[]
        active['note']=note
        new['coverage_units'][routeindex].update(reviewed_route_records=4683,completed_route_records=4683,next=NEXT)
        new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[200],
            completion_credit_added=19,final_review=str(FINAL),actual_source_event200_selected=False,batch_new_emulator_runs=4,goal_turn_new_emulator_runs=2,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all19-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),
            zero_macros_two_FE_and_complete_reassurance_requests_and_take_care_phrases_preserved=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
            patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        new[PARENT_KEY]=old['current_integrated_candidate'];new['current_integrated_candidate']=current;new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=summary
        inventory=deepcopy(read(old['unfinished_editorial_scope_v5866']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B200_completed_v5877']=dict(final_review=str(FINAL),completed_objects=19,registered_candidate=release['candidate'],natural_event200_not_selected=True,
            actual_speeches=19,offline_only_speeches=0,actual_matching_holds=73,nontext_equal_samples=172,nontext_total_samples=182,
            speech_duration_changes=8,shifted_start_return_pairs=19,prompt_blink_sample_differences=6,following_sailing_cloud_sample_differences=10,
            final_PRNG_seeds_differ=True,complete_timing_cause_untraced=True,no_broad_postscene_simulation_equivalence_claim=True,
            Stranger_name_target_separate_unapplied=True)
        inventory['historical_Lil_B200_reference_approved_before_v5877']=inventory.pop('next_Lil_B200_reference_approved_uncredited_v5866')
        inventory['next_three_generic_speaker_labels_target_validation']=dict(actor_IDs=[164,165,172],drafts={'164':'Man','165':'Woman','172':'Stranger'},
            target_bytes_native_consumers_glyphs_bounds_substitutions_representative_and_registered_release_pending=True,
            all207_unaffected_name_fields_and_all_other_ROM_components_must_stay_exact=True,new_dialogue_credit=0,
            paired_label_proofs='work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json',
            anonymous_source_census='work/analysis/collapsed_speaker_lead_v5832/all_route_literal_uses_exact_name_fields_and_localization_finding.json')
        inventory['next_Lil_B201_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=201,clean_inventory_and_full_exchange_gloss_before_prior_English=True,
            reviewed_objects=0,new_completion_credit=0,no_B201_command_actor_or_control_assumptions_inherited=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4683,completed_route_records=4683,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B200_previously_uncredited_objects_completed=19,three_generic_label_targets_and_Lil_B201_clean_review_pending=True,untranslated_Alexandria_alias_caller_and_display_open=True,incomplete_COMMON=3,
            incomplete_credited_route_drafts=0,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,
            record_IDs=[r['id'] for r in rows],new_source_prose_reviews=19,new_completed_records=19,revised=13,retained=6,goal_turn_classification='progress',previous_goal_turn_classification='progress',batch_new_emulator_runs=4,goal_turn_new_emulator_runs=2,
            batch_new_frames=47404,goal_turn_new_frames=21402,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
        assert new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5877: Nineteen Lil B200 reviews integrated once in cumulative V5872\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5877\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=19,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six targets staged;nineteen reviews counted once in proposed ledger. Audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6282,6285,3941,2341)
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates();assert new['current_integrated_candidate']['sha256']==release['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists()
            save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,
                exactly19_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False))
            print('Six targets,all historical values and nineteen disjoint new keys audited.')
        elif mode=='apply':
            assert not (ROOT/'native_application_receipt.json').exists();assert read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False))
            print('Six audited completion files applied exactly.')
        else:
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();assert len(read(FINAL)['records'])==19
            oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};allkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(oldkeys)==6263 and len(allkeys)==6282
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly19_new_disjoint_source_prose_and_completed_records=True,
                completed=6282,source_prose=6285,revised=3941,retained=2341,SC2=4397,SC3=96,reviewed_routes=4683,completed_routes=4683,
                all586_manifest_batches114_accepted18_checks_verified=True,actual_unique_B200_speeches=19,offline_only_B200_speeches=0,actual_matching_holds=73,
                startup31_frames_and_five_actor_controls_match_V5816=True,source200_natural_eligibility_and_full_item_effect_semantics_not_claimed=True,
                speech_duration_changes=8,shifted_start_return_pairs=19,prompt_blink_differences=6,following_sailing_cloud_differences=10,final_PRNG_seeds_differ=True,
                complete_timing_cause_untraced=True,no_broad_postscene_equivalence_or_causal_claim=True,
                next_three_generic_labels_target_validation=True,next_Lil_B201_clean_review_pending=True,
                retrospective207_name_queue_and_paired164_165_role_labels_and172_Stranger_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5872 integration verified;6282 completed/6285 source-prose. Next three generic speaker labels and full broader editorial scope remain active.')
