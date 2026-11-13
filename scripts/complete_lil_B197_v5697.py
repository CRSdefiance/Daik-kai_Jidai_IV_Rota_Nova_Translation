"""Credit twenty-four newly integrated reviews once;preserve the complete ledger history."""
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

ROOT=Path('work/analysis/lil_B197_completion_v5697')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5698')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B197_editorial_manuscript_v4.json')
MENU=Path('translations/lil_B197_choice_manuscript_v3.json')
FINAL=Path('translations/lil_B197_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B197_release_v5693/registered_release_verification.json')
START=Path('work/analysis/lil_B197_startup_v5695/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=Path('work/analysis/lil_B197_registration_v5691/registration_receipt.json')
ACTUAL=Path('work/analysis/lil_B197_actual_v5684b/three_paths_and_focused_refusal_highlight.json')
TRANSITIONS=Path('work/analysis/lil_B197_actual_review_v5686/viewed21_panels_three_options_returns_and_measured_scope.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5675/verified_handoff.json')
FAMILY='Lil-B197-book-offer-romantic-rebuff-delegated-gift-three-choices-common-Ian-Charm24'
KEY='Lil_B197_completion_v5697'
PARENT_KEY='previous_integrated_candidate_before_Lil_B197_completion_v5697'
PREVIOUS='previous_latest_checkpoint_before_Lil_B197_completion_v5697'
SCOPE='unfinished_editorial_scope_v5697'
WATCH='Lil_B197_v5697'
from scripts.lil_B197_completion_text_v5697 import NEXT,DETAILS

def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all583_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert start['all_current_requested_and_final_framebuffers_equal_V5637'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==95 and reg['all_negatives_reject_before_mutation']
    assert actual['actual_unique_speech_panels']==21 and len(actual['all_actual_speech_observations'])==35 and len(actual['actual_menu_cases'])==3
    assert actual['complete_native_holds']==128 and not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences']
    assert not actual['offline_only_display_IDs'] and len(actual['command_timing_differences'])==59 and len(actual['later_whole_RGB_differences'])==82
    assert transitions['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and transitions['no_open_translation_specific_display_menu_control_or_return_finding']
    assert transitions['new_successful_English_runs']==4 and transitions['new_successful_English_frames']==43604 and transitions['total_successful_frames']==82607
    assert len(transitions['terminal_reaped_tool_sessions'])==6 and transitions['two_failed_English_runs_not_counted_as_passes']
    assert transitions['broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks']
    assert transitions['source_matched_blank_portrait_name_additional_records']==[64,89]
    tests=read('work/analysis/lil_B197_regressions_v5692/terminal.json');assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==583 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B197_retention_v5696/pin_receipt.json')['all_prior_pins_preserved']
    return release

def restore(new):
    inverse=deepcopy(new);entry=inverse.pop(KEY);back=entry['inverse_preserved_values']
    inverse['current_integrated_candidate']=inverse.pop(PARENT_KEY);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(SCOPE)
    assert inverse['completed_editorial_families'].pop()['id']==FAMILY;inverse.update(back['root_values'])
    fresh=inverse['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert fresh[k][-24:]==entry['record_keys'];del fresh[k][-24:]
    assert fresh['record_IDs'][-24:]==entry['record_IDs'];del fresh['record_IDs'][-24:]
    assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values'])
    active=inverse['active_source_prose_drafts']
    for p in reversed([DOC,MENU]):
        assert active['manuscripts'].pop()==str(p) and active['route_record_subsets_pending'].pop(str(p))==[]
    active['note']=back['active_note']
    assert inverse['coverage_units'].pop()['id']==FAMILY;inverse['coverage_units'][back['route_unit_index']]=back['route_unit'];inverse['formatting_watchlist'].pop(WATCH)
    return inverse

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records']+read(MENU)['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':8} and doc['source_prose_or_completion_credit_added']==0
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[197]
        refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for command in mapping['blocks'][0]['choice_commands']:
            refs.update({r['id']:{**r,'target_hex':block[r['new_offset']:r['new_offset']+r['new_length']].hex(),'target_command_offset':command['new_offset']} for r in command['label_references']})
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);speech='source_selector' in row
            assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at
            if speech:assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','source_prose_or_completion_credit_added','command_offset']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
            body=value[1:] if speech else value;template=body.decode('ascii');runtime=template.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')
            logical=' '.join(template.split())
            for macro in ['FI','FA','FO']:logical=logical.replace(macro,'{MACRO:'+macro+'}')
            newref=dict(block=197,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'))
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
        assert len(oldkeys)==6191 and len(keys)==24 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6191 and not fresh['pending_record_keys']
        summary=DETAILS+'Candidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MENU,RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS,PRIOR,Path(doc['reference_map']),Path(doc['native_font_proof']),
            Path('work/analysis/lil_B197_regressions_v5692/terminal.json'),Path('work/analysis/lil_B197_retention_v5696/pin_receipt.json'),Path(__file__)]}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
            revised=16,retained=8,source_prose_and_completion_credit_added_once=24,previous_B197_objects_uncredited=True,all24_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,
            actual_unique_speeches=21,offline_only_speeches=0,actual_menu_cases=3,actual_matching_holds=128,natural_event197_not_selected=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);rootnames=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated',
            'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']
        freshnames=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']
        routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
        back=dict(root_values={k:deepcopy(old[k]) for k in rootnames},fresh_values={k:deepcopy(fresh[k]) for k in freshnames},
            active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[197],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,
            revised_count=16,retained_count=8,fresh_revisions=16,fresh_retentions=8,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=6215,records_with_source_and_prose_pass=6218,records_with_source_prose_drafts=6218,records_revised_and_integrated=3905,retained_wordings_editorially_completed=2310)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC2.DK4']==4306;new[key]['/data/SC2.DK4']=4330
        keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871']
        note='6215 contextual rereads integrated;source/prose6218. B197 counted once;all wider families and earlier premature wrapping remain open.'
        for key in ['record_keys','integrated_record_keys']:f[key].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=6215,fresh_pass_records_integrated=6215,latest_contextual_manuscript=str(DOC),
            latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=24,final_review=str(FINAL),new_revisions=16,justified_retentions=8,new_completed_records=24,historical_reconciliation_only=False,
            actual_selected_source197_events=[],actual_B22_content_speeches=21,offline_only_speeches=0,actual_menu_cases=3,new_current_candidate_emulator_runs=2,explicit_content_fixture_runs=7,batch_new_frames=104009,goal_turn_new_frames=65006))
        active=new['active_source_prose_drafts']
        for p in [DOC,MENU]:
            assert str(p) not in active['manuscripts'] and str(p) not in active['route_record_subsets_pending']
            active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[]
        active['note']=note
        new['coverage_units'][routeindex].update(reviewed_route_records=4616,completed_route_records=4616,next=NEXT)
        new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[197],
            completion_credit_added=24,final_review=str(FINAL),actual_source_event197_selected=False,batch_new_emulator_runs=9,goal_turn_new_emulator_runs=6,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all24-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),
            only_exact_R74_dont_have_ordinary_boundary_approved=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
            patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        new[PARENT_KEY]=old['current_integrated_candidate'];new['current_integrated_candidate']=current;new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=summary
        inventory=deepcopy(read(old['unfinished_editorial_scope_v5674']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B197_completed_v5697']=dict(final_review=str(FINAL),completed_objects=24,registered_candidate=release['candidate'],natural_event197_not_selected=True,
            actual_speeches=21,offline_only_speeches=0,actual_menu_cases=3,actual_original_menu_indices=[0,1,2],timing_differences=59,later_RGB_differences=82,
            no_broad_postscene_simulation_equivalence_claim=True)
        inventory['historical_Lil_B197_native_approved_before_v5697']=inventory.pop('next_Lil_B197_native_approved_uncredited_v5674')
        inventory['next_Lil_B198_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=198,clean_inventory_and_full_exchange_gloss_before_prior_English=True,
            reviewed_objects=0,new_completion_credit=0,no_B198_command_actor_or_control_assumptions_inherited=True)
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4616,completed_route_records=4616,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B197_previously_uncredited_objects_completed=24,Lil_B198_clean_review_pending=True,untranslated_Alexandria_alias_caller_and_display_open=True,incomplete_COMMON=3,
            incomplete_credited_route_drafts=0,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,
            record_IDs=[r['id'] for r in rows],new_source_prose_reviews=24,new_completed_records=24,revised=16,retained=8,goal_turn_classification='progress',previous_goal_turn_classification='progress',batch_new_emulator_runs=9,goal_turn_new_emulator_runs=6,
            batch_new_frames=104009,goal_turn_new_frames=65006,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
        assert new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5697: Twenty-four Lil B197 reviews integrated once in cumulative V5692\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5697\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=24,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six targets staged;twenty-four reviews counted once in proposed ledger. Audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6215,6218,3905,2310)
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates();assert new['current_integrated_candidate']['sha256']==release['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists()
            save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,
                exactly24_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False))
            print('Six targets,all historical values and twenty-four disjoint new keys audited.')
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
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();assert len(read(FINAL)['records'])==24
            oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};allkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(oldkeys)==6191 and len(allkeys)==6215
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly24_new_disjoint_source_prose_and_completed_records=True,
                completed=6215,source_prose=6218,revised=3905,retained=2310,SC2=4330,SC3=96,reviewed_routes=4616,completed_routes=4616,
                all583_manifest_batches114_accepted18_checks_verified=True,actual_unique_B197_speeches=21,offline_only_B197_speeches=0,actual_menu_cases=3,actual_matching_holds=128,
                startup31_frames_and_five_actor_controls_match_V5637=True,source197_natural_eligibility_and_earned_affordability_not_claimed=True,
                all59_timing82_later_RGB_and_explicit_state_RNG_differences_preserved=True,no_broad_postscene_equivalence_or_causal_claim=True,
                next_Lil_B198_clean_review_pending=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5692 integration verified;6215 completed/6218 source-prose. Next B198 clean-source review pending;full goal active.')
