"""Credit seventeen newly integrated reviews once;preserve the complete ledger history."""
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

ROOT=Path('work/analysis/lil_B190_completion_v5351')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5352')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B190_editorial_manuscript_v4.json')
FINAL=Path('translations/lil_B190_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B190_release_v5347/registered_release_verification.json')
START=Path('work/analysis/lil_B190_startup_v5349/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=Path('work/analysis/lil_B190_registration_v5345/registration_receipt.json')
ACTUAL=Path('work/analysis/lil_B190_actual_v5340b/actual_all17_progressive_FE_RNG_effect_C200_and_single_end.json')
TRANSITIONS=Path('work/analysis/lil_B190_actual_review_v5341b/all17_panels_16_fullscreens_conditional_return_and_measured_differences.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5310/verified_handoff.json')
NEXT_SOURCE=Path('work/analysis/lil_B191_clean_context_v5355/all13_clean_exchange_and_fresh_glosses.json')
FAMILY='Lil-B190-reported-retail-cure-doubt-shopping-and-prospective-Havana17'
KEY='Lil_B190_completion_v5351'
PARENT_KEY='previous_integrated_candidate_before_Lil_B190_completion_v5351'
PREVIOUS='previous_latest_checkpoint_before_Lil_B190_completion_v5351'
SCOPE='unfinished_editorial_scope_v5351'
WATCH='Lil_B190_v5351'
from scripts.lil_B190_completion_text_v5351 import NEXT,DETAILS

def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all574_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert start['all_current_requested_and_final_framebuffers_equal_V5304'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==88 and reg['all_negatives_reject_before_mutation']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==17 and not actual['failures']
    assert sum(len(r['holds']) for r in actual['actual_panels'])==67
    assert transitions['fixture_return_frames']==[6934,6937] and transitions['exact_timing_difference_counts']==dict(total=9,speech=7,control_or_end=2)
    assert len(transitions['sampled_postscene_whole_RGB_differences_unmasked'])==2 and not transitions['all_sampled_postscene_whole_RGB_equal'] and transitions['nine_timing_and_two_original_indicator_shadow_differences_retained_without_masking_or_retiming'] and transitions['original_carried_result2_C200_3_2_and_end_0_2_preserved']
    assert transitions['whole_RGB_final9001_equal'] and transitions['postscene9001_PRNG_seeds']==[2467799992,2467799992] and transitions['PRNG_equality']
    assert transitions['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and transitions['no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding']
    tests=read('work/analysis/lil_B190_regressions_v5346/terminal.json');assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==574 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B190_retention_v5350/pin_receipt.json')['all_prior_pins_preserved']
    source=read(NEXT_SOURCE);assert len(source['records'])==17 and source['read_no_predecessor_English'] and source['new_review_credit']==0
    return release

def restore(new):
    inverse=deepcopy(new);entry=inverse.pop(KEY);back=entry['inverse_preserved_values']
    inverse['current_integrated_candidate']=inverse.pop(PARENT_KEY);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(SCOPE)
    assert inverse['completed_editorial_families'].pop()['id']==FAMILY;inverse.update(back['root_values'])
    fresh=inverse['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert fresh[k][-17:]==entry['record_keys'];del fresh[k][-17:]
    assert fresh['record_IDs'][-17:]==entry['record_IDs'];del fresh['record_IDs'][-17:]
    assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values'])
    active=inverse['active_source_prose_drafts'];assert active['manuscripts'].pop()==str(DOC)
    assert active['route_record_subsets_pending'].pop(str(DOC))==[];active['note']=back['active_note']
    assert inverse['coverage_units'].pop()['id']==FAMILY;inverse['coverage_units'][back['route_unit_index']]=back['route_unit'];inverse['formatting_watchlist'].pop(WATCH)
    return inverse

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':10,'retain-wording':7} and doc['source_prose_or_completion_credit_added']==0
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[190]
        refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex'])
            assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','source_prose_or_completion_credit_added']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
            body=value[1:];assert not any(m in body for m in [b'FI',b'FA',b'FO'])
            newref=dict(block=190,offset=at,header_offset=at-5,bytes=len(value),record_index=block[:at].count(b'\0'))
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),
                record_index=newref['record_index'],current_record_index=newref['record_index'],current_English=body.decode('ascii'),current_stored_English=body.decode('ascii'),
                current_raw_storage_English=body.decode('ascii'),current_effective_runtime_English=body.decode('ascii'),current_effective_macro_template_hex=body.hex(),
                current_effective_macro_template_English=body.decode('ascii'),current_effective_paragraph=' '.join(body.decode('ascii').split()),registered_runtime_catalog_entry=None,
                completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,
                current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,
                decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release')
            assert row['current_effective_paragraph']==row['english'].split('}',1)[1] and all(row['review'].values())
        oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
        assert len(oldkeys)==6071 and len(keys)==17 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6071 and not fresh['pending_record_keys']
        summary=DETAILS+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS,PRIOR,NEXT_SOURCE,Path(doc['reference_map']),Path(doc['native_font_proof']),
            Path('work/analysis/lil_B190_regressions_v5346/terminal.json'),Path('work/analysis/lil_B190_retention_v5350/pin_receipt.json'),Path(__file__)]}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
            revised=10,retained=7,source_prose_and_completion_credit_added_once=17,previous_B190_objects_uncredited=True,all17_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,
            actual_unique_speeches=17,actual_matching_holds=67,natural_event190_not_selected=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);rootnames=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated',
            'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']
        freshnames=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']
        routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
        back=dict(root_values={k:deepcopy(old[k]) for k in rootnames},fresh_values={k:deepcopy(fresh[k]) for k in freshnames},
            active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[190],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,
            revised_count=10,retained_count=7,fresh_revisions=10,fresh_retentions=7,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=6088,records_with_source_and_prose_pass=6091,records_with_source_prose_drafts=6091,records_revised_and_integrated=3849,retained_wordings_editorially_completed=2239)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC2.DK4']==4186;new[key]['/data/SC2.DK4']=4203
        keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871']
        note='6088 contextual rereads integrated;source/prose6091. B190 counted once;all wider families and earlier premature wrapping remain open.'
        for key in ['record_keys','integrated_record_keys']:f[key].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=6088,fresh_pass_records_integrated=6088,latest_contextual_manuscript=str(DOC),
            latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=17,final_review=str(FINAL),new_revisions=10,justified_retentions=7,new_completed_records=17,historical_reconciliation_only=False,
            actual_selected_source190_events=[],actual_B22_content_speeches=17,new_current_candidate_emulator_runs=2,explicit_content_fixture_runs=2,batch_new_frames=39404,goal_turn_new_frames=39404))
        active=new['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'] and str(DOC) not in active['route_record_subsets_pending']
        active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
        new['coverage_units'][routeindex].update(reviewed_route_records=4489,completed_route_records=4489,next=NEXT)
        new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[190],
            completion_credit_added=17,final_review=str(FINAL),actual_source_event190_selected=False,batch_new_emulator_runs=4,goal_turn_new_emulator_runs=4,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all17-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),
            no_record_specific_ordinary_boundary_exception_required=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
            patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        new[PARENT_KEY]=old['current_integrated_candidate'];new['current_integrated_candidate']=current;new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=summary
        inventory=deepcopy(read(old['unfinished_editorial_scope_v5309']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B190_completed_v5351']=dict(final_review=str(FINAL),completed_objects=17,registered_candidate=release['candidate'],natural_event190_not_selected=True)
        inventory['historical_Lil_B190_clean_only_before_v5351']=inventory.pop('next_Lil_B190_clean_only_v5313')
        inventory['next_Lil_B191_clean_only_v5355']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=13,uncredited=True,
            conditional38_commands_three_predicates16_relatives_four_alternatives=True)
        inventory['B190_carried_result_and_stopped_audit_preserved']=dict(path=doc['carried_result_proof'],sha256=doc['carried_result_proof_sha256'],
            original_result2_C200_3_2_end_0_2_preserved=True,no_emulator_rerun=True)
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4489,completed_route_records=4489,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B190_previously_uncredited_objects_completed=17,Lil_B191_clean_only_uncredited_objects=13,untranslated_Alexandria_alias_caller_and_display_open=True,incomplete_COMMON=3,
            incomplete_credited_route_drafts=0,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,
            record_IDs=[r['id'] for r in rows],new_source_prose_reviews=17,new_completed_records=17,revised=10,retained=7,goal_turn_classification='progress',previous_goal_turn_classification='progress',batch_new_emulator_runs=4,goal_turn_new_emulator_runs=4,
            batch_new_frames=39404,goal_turn_new_frames=39404,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
        assert new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5351: Seventeen Lil B190 reviews integrated once in cumulative V5346\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5351\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=17,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six targets staged;seventeen reviews counted once in proposed ledger. Audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6088,6091,3849,2239)
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates();assert new['current_integrated_candidate']['sha256']==release['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists()
            save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,
                exactly17_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False))
            print('Six targets,all historical values and seventeen disjoint new keys audited.')
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
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();assert len(read(FINAL)['records'])==17
            oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};allkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(oldkeys)==6071 and len(allkeys)==6088
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly17_new_disjoint_source_prose_and_completed_records=True,
                completed=6088,source_prose=6091,revised=3849,retained=2239,SC2=4203,SC3=96,reviewed_routes=4489,completed_routes=4489,
                all574_manifest_batches114_accepted18_checks_verified=True,actual_unique_B190_speeches=17,actual_matching_holds=67,
                startup31_frames_and_five_actor_controls_match_V5304=True,source190_natural_eligibility_and_earned_fashion_not_claimed=True,
                nine_timing_two_indicator_shadows_and_original_carried_result_preserved=True,new_clean_only_Lil_B191_uncredited_objects=13,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5346 integration verified;6088 completed/6091 source-prose. Thirteen conditional B191 clean-only glosses pending;full goal active.')
