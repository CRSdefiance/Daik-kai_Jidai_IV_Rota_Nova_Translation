"""Credit28 disjoint B206 objects only after registered release and actual checks."""
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
from scripts.lil_B206_completion_text_v6333 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B206_completion_v6333')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6334')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B206_editorial_manuscript_v9.json')
MENU=Path('translations/lil_B206_choice_manuscript_v5.json')
FINAL=Path('translations/lil_B206_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_B206_release_v6328/registered_release_verification.json')
START=Path('work/analysis/lil_B206_startup_v6331/cold_boot_Lil_startup_town_verification.json')
VIEW=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B206_actual_v6319/all24_English_panels55_observations217_native_holds_five_menus_three_same_code_paths.json')
TRANSITIONS=Path('work/analysis/lil_B206_actual_review_v6321/viewed24_panels_four_labels_three_paths_and_measured_later_scope.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6324/verified_handoff.json')
REG=Path('work/analysis/lil_B206_registration_v6326/registration_receipt.json')
PIN=Path('work/analysis/lil_B206_retention_v6329/pin_receipt.json')
FAMILY='Lil-B206-ceramic-earring-legend-friendship-price-and-two-refusals28'
KEY='Lil_B206_completion_v6333'
SCOPE='unfinished_editorial_scope_v6333'
WATCH='Lil_B206_v6333'
ROOTVALUES=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','current_integrated_candidate','latest_checkpoint']
FRESHVALUES=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']

def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all597_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6270']
    assert start['all_current_requested_and_final_framebuffers_equal_V6270'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==81 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_native_text_and_nameplate_holds'])==(24,55,217)
    assert len(actual['actual_menu_cases'])==5 and sum(len(r['holds']) for r in actual['actual_menu_cases'])==13
    assert not any(actual[k] for k in ['failures','paired_nontext_region_differences','command_result_differences','command_UI_word_differences','offline_only_display_IDs'])
    assert actual['source_and_English_all51_commands42_source_plus9_initializers_observed'] and actual['all_command_paths_and_results_preserved'] and actual['all_jobs_terminal_and_reaped']
    assert transitions['no_open_translation_specific_display_menu_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==9 and len(transitions['viewed_acquisition_frames'])==2
    assert [len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[81,8,114]
    assert transitions['paired_command_timing_differences']==actual['command_timing_differences'] and transitions['within_scene_RNG_differences']==actual['command_RNG_differences'] and transitions['postscene_RGB_differences']==actual['later_whole_RGB_differences']
    assert transitions['broad_postscene_full_RAM_future_world_equivalence_unproven'] and transitions['original_source_asking9000_not_completed_debit_affordability_or_outer_event_proof'] and transitions['natural_event206_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed']
    tests=read('work/analysis/lil_B206_regressions_v6327/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B206_reference_v6307_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==597 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release

def restore(value):
    d=deepcopy(value);entry=d.pop(KEY);back=entry['inverse_preserved_values'];d.pop(SCOPE);d.update(back['root_values'])
    assert d['completed_editorial_families'].pop()['id']==FAMILY
    fresh=d['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert fresh[k][-28:]==entry['record_keys'];del fresh[k][-28:]
    assert fresh['record_IDs'][-28:]==entry['record_IDs'];del fresh['record_IDs'][-28:]
    assert fresh['reconciled_families'].pop()['id']==FAMILY;fresh.update(back['fresh_values'])
    active=d['active_source_prose_drafts']
    for p in reversed([DOC,MENU]):assert active['manuscripts'].pop()==str(p) and active['route_record_subsets_pending'].pop(str(p))==[]
    active['note']=back['active_note'];assert d['coverage_units'].pop()['id']==FAMILY;d['coverage_units'][back['route_unit_index']]=back['route_unit'];d['formatting_watchlist'].pop(WATCH)
    return d

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==read(PRIOR)['ledger_sha256'];release=gates();doc,menu=map(read,[DOC,MENU]);mapping=read(doc['reference_map']);rows=deepcopy(doc['records']+menu['records'])
        assert Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':12}
        block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[206];refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for command in mapping['blocks'][0]['choice_commands']:refs.update({r['id']:{**r,'target_hex':block[r['new_offset']:r['new_offset']+r['new_length']].hex(),'target_command_offset':command['new_offset']} for r in command['label_references']})
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);speech='source_selector' in row
            assert block[at:at+len(value)+1]==value+b'\0' and stage[row['id']]['new_offset']==at
            if speech:assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_effective_macro_template_English','current_effective_paragraph','current_raw_storage_English','current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','source_prose_or_completion_credit_added','command_offset','current_native_voice_macro_entry_and_context_pending','native_plane_verified_not_actual_English_gameplay','current_native_UI_body_explicit_unexecuted_boundary','current_native_extent','formatting_reason']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row};body=value[1:] if speech else value;template=body.decode('cp932');logical=' '.join(template.split())
            newref=dict(block=206,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'))
            if speech:
                newref['header_offset']=at-5;command=next(c for c in mapping['blocks'][0]['mapped_native_commands'] if c['new_offset']==at-5);assert command['word']==0x4000 and command['new_native_extent']>=len(value)+6
                row['integrated_native_extent']=row['current_native_extent']=command['new_native_extent']
            else:newref['command_offset']=ref['target_command_offset'];row['current_command_offset']=ref['target_command_offset']
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),record_index=newref['record_index'],current_record_index=newref['record_index'],current_English=template,current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=template,current_effective_paragraph=logical,registered_runtime_catalog_entry=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,current_native_voice_macro_entry_and_context_pending=False,native_plane_verified_not_actual_English_gameplay=False,actual_English_complete_panel_and_native_holds_verified=True,current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release')
            row.update(current_native_UI_body_explicit_unexecuted_boundary=False,formatting_reason='The historical native-only proof and its UI-boundary limitation remain preserved. Separate actual three-path evidence now verifies complete text/nameplate holds or typed labels,visible selections and returns;registered cumulative bytes equal the approved reference. Native rules,all five exact-source ordinary boundaries and all ten individual rowcount reasons remain exact.',actual_complete_display_proof=str(ACTUAL),actual_complete_display_proof_sha256=sha(ACTUAL.read_bytes()))
            assert logical==(row['english'].split('}',1)[1] if speech else row['english']) and all(row['review'].values())
        oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows};assert len(oldkeys)==6387 and len(keys)==28 and not oldkeys&keys
        fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6387 and not fresh['pending_record_keys']
        summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        paths=[DOC,MENU,RELEASE,START,VIEW,REG,PIN,ACTUAL,TRANSITIONS,PRIOR,Path(doc['reference_map']),Path(__file__),Path('scripts/lil_B206_completion_text_v6333.py'),Path('work/analysis/lil_B206_regressions_v6327/terminal.json')];evidence={str(p):sha(p.read_bytes()) for p in paths}
        ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(p):sha(p.read_bytes()) for p in [DOC,MENU]},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=16,retained=12,source_prose_and_completion_credit_added_once=28,previous_B206_objects_uncredited=True,all28_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_unique_speeches=24,actual_speech_observations=55,offline_only_speeches=0,actual_menu_cases=5,actual_matching_holds=217,actual_menu_matching_holds=13,natural_event206_not_selected=True,evidence=evidence,summary=summary,full_goal_complete=False))
        new=deepcopy(old);routeindex=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');back=dict(root_values={k:deepcopy(old[k]) for k in ROOTVALUES},fresh_values={k:deepcopy(fresh[k]) for k in FRESHVALUES},active_note=old['active_source_prose_drafts']['note'],route_unit_index=routeindex,route_unit=deepcopy(old['coverage_units'][routeindex]))
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[206],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=16,retained_count=12,fresh_revisions=16,fresh_retentions=12,actual_verification_scope=DETAILS))
        new.update(records_editorially_completed=6415,records_with_source_and_prose_pass=6418,records_with_source_prose_drafts=6418,records_revised_and_integrated=4005,retained_wordings_editorially_completed=2410)
        for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[key]['/data/SC2.DK4']==4501;new[key]['/data/SC2.DK4']=4529
        keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows];f=new['contextual_story_natural_dialogue_pass_v1871'];note='6415 contextual rereads integrated;source/prose6418. All28 B206 speech/choice objects counted once. Full four-storyline,earlier dialogue,shared town/shop/random/Help/prose,name/role/alias and premature-wrap review remains active.'
        for key in ['record_keys','integrated_record_keys']:f[key].extend(deepcopy(keyrows))
        f['record_IDs'].extend(r['id'] for r in rows);f.update(fresh_pass_records_explicitly_reread=6415,fresh_pass_records_integrated=6415,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=28,final_review=str(FINAL),new_revisions=16,justified_retentions=12,new_completed_records=28,historical_reconciliation_only=False,actual_selected_source206_events=[],actual_B22_content_speeches=24,actual_speech_observations=55,offline_only_speeches=0,actual_menu_cases=5,complete_text_nameplate_holds=217,complete_menu_holds=13,current_candidate_emulator_runs=2,current_candidate_frames=21402,source_English_content_runs=6,source_English_content_frames=96006,content_phase_new_runs=5,content_phase_new_frames=80005,reused_prior_source_buy_frames=16001))
        active=new['active_source_prose_drafts']
        for p in [DOC,MENU]:assert str(p) not in active['manuscripts'] and str(p) not in active['route_record_subsets_pending'];active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[]
        active['note']=note;new['coverage_units'][routeindex].update(reviewed_route_records=4815,completed_route_records=4815,next=NEXT)
        new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-references-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[206],completion_credit_added=28,final_review=str(FINAL),actual_source_event206_selected=False,current_candidate_emulator_runs=2,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='all28-source-native-reference-actual-registered-release-pass',final_review=str(FINAL),all42_commands24_preambles_two_menus8spans8leaves_and_original_results_preserved=True,five_exact_source_ordinary_boundaries_ten_rowcount_reasons=True,no_glyph_bounds_pagination_or_control_waivers=True)
        current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});new['current_integrated_candidate']=current;new['latest_checkpoint']=summary
        inventory=deepcopy(read(old['unfinished_editorial_scope_v6323']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B206_completed_v6333']=dict(final_review=str(FINAL),completed_objects=28,registered_candidate=release['candidate'],actual_speeches=24,complete_native_text_nameplate_holds=217,actual_menu_cases=5,complete_menu_holds=13,all42_source_commands_and9_initializers_observed=True,natural_event206_not_selected=True,old_pending_native_reference_actual_flags_preserved_as_history_and_superseded_here=True,all81timing8RNG114RGB_and_queried_state_limits_preserved=True)
        inventory['next_Lil_B207_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=207,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B206_actor_macro_price_material_menu_branch_effect_or_end_assumptions_inherited=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4815,completed_route_records=4815,next=NEXT)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B206_previously_uncredited_objects_completed=28,next_Lil_B207_clean_review_pending=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_and_role_labels_open=True,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=28,new_completed_records=28,revised=16,retained=12,goal_turn_classification='progress',previous_goal_turn_classification='progress',goal_turn_new_emulator_runs=2,goal_turn_new_frames=21402,reused_verified_content_frames=96006,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V6333: B206 complete exchange integrated once in cumulative V6327\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V6333\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(target.read_bytes(),mtime=0))
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=28,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;28 reviews proposed once. Deep-inverse audit/application pending.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6415,6418,4005,2410)
        for entry in plan['files']:assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256'] and sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        release=gates()
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_all_original_root_and_nested_history=True,exactly28_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False));print('Six targets,all historical values and28 disjoint new keys audited.')
        elif mode=='apply':
            assert not (ROOT/'native_application_receipt.json').exists() and read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False));print('Six audited files applied exactly.')
        else:
            assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();assert len(read(FINAL)['records'])==28
            allkeys={historical_key(r) for family in new['completed_editorial_families'] for r in family['records']};assert len(allkeys)==6415
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_preserved=True,exactly28_new_disjoint_source_prose_and_completed_records=True,completed=6415,source_prose=6418,revised=4005,retained=2410,SC2=4529,SC3=96,reviewed_routes=4815,completed_routes=4815,all597_manifest_batches114_accepted18_checks_verified=True,actual_unique_B206_speeches=24,actual_speech_observations=55,offline_only_B206_speeches=0,actual_matching_holds=217,actual_menu_cases=5,actual_menu_holds=13,startup31_frames_and_five_actor_controls_match_V6270=True,source206_natural_activation_original_location_earned_inventory_full_payment_and_effect_semantics_not_claimed=True,measured81timing8RNG114RGB_and_queried_final_state_limits_preserved=True,no_broad_postscene_equivalence_or_causal_claim=True,next_Lil_B207_clean_review_pending=True,retrospective207_name_queue_and_all_prior_leads_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V6327 verified:6415 completed/6418 source-prose. B207 and the full broader editorial/name-review objective remain active.')
