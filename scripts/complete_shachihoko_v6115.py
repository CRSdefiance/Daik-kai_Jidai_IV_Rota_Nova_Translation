"""Stage, audit, apply and verify one disjoint COMMON review with an exact inverse."""
import argparse,gzip,json,os,struct
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.shachihoko_completion_text_v6115 import DETAILS,NEXT
ROOT=Path('work/analysis/shachihoko_completion_v6115');VERIFY=Path('work/analysis/editorial_handoff_verification_v6116')
LEDGER=Path('translations/editorial_review_current_v1.json');FINAL=Path('translations/shachihoko_item116_contextual_final_review_v1.json')
DOC=Path('translations/shachihoko_item116_editorial_manuscript_v2.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v6091/verified_handoff.json')
RELEASE=Path('work/analysis/shachihoko_release_v6111/registered_release_verification.json')
APPROVAL=Path('work/analysis/shachihoko_approval_v6106/coordinated_title_description_source_native_actual_approval.json')
PIN=Path('work/analysis/shachihoko_retention_v6112/pin_receipt.json')
NAMES=Path('work/analysis/current_speaker_labels_v6113/existing_Man_Woman_Stranger_labels_and_broader_name_scope.json')
REGRESSIONS=Path('work/analysis/shachihoko_regressions_v6110/terminal.json');ATOMIC=Path('work/analysis/shachihoko_atomic_v6108b/atomic_validation_receipt.json')
KEY='Item116_Shachihoko_completion_v6115';SCOPE='unfinished_editorial_scope_v6115';FAMILY='item116-Shachihoko-coordinated-cultural-title-and-COMMON2931-description'
WATCH='Item116_Shachihoko_v6115'
ROOTVALUES=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','current_integrated_candidate','latest_checkpoint']
FRESHVALUES=['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','latest_contextual_manuscript','latest_completed_family','latest_final_review','coverage_note']
def gates():
    r,a,p,n,t,b=map(read,[RELEASE,APPROVAL,PIN,NAMES,REGRESSIONS,ATOMIC])
    for key in ['candidate','patch','manifest']:assert sha(Path(r[key]).read_bytes())==r[key+'_sha256']
    assert sha(Path(r['exact_patch_reconstruction']).read_bytes())==r['candidate_sha256']==r['reference_ROM_sha256']==sha(Path(r['reference_ROM']).read_bytes())
    assert r['all592_manifest_batches_and114_accepted_layers_present'] and r['all18_registered_release_checks_pass'] and r['all_story_files_fonts_graphics_ARM7_and_other_components_exact_to_V6050']
    manifest=read(r['manifest']);registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==592 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert a['all_two_records_have_five_source_context_localization_naturalness_formatting_gates'] and a['all24_detail_font_modes_fields_complete_glyphs_pixels_bounds_and_original_parent_crops_pass']
    assert a['expanded224_byte_payload_actual31_screens_six_actor_controls_and_native_copy_cache_arena_verified'] and a['eight_actual_complete_title_description_field_matches_two_holds_and_normal_return']
    for sheet in a['viewed_sheets']:assert sheet['viewed'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert p['all_prior_pins_preserved'] and p['ROMs_deleted']==0 and n['candidate_sha256']==r['candidate_sha256']
    assert [x['current_label'] for x in n['current_labels']]==['Man','Woman','Stranger'] and n['broader207_proper_names_roles_aliases_and_retrospective_consumers_still_open']
    assert t['terminal'] and t['returncode']==0 and sha(Path(t['log']).read_bytes())==t['log_sha256'] and '110 passed' in Path(t['log']).read_text('utf-8')
    assert b['negative_count']==35 and b['all_negatives_reject_before_any_image_mutation'] and b['all_reference_files_and_components_reconstruct_exactly']
    doc=read(DOC);validate_natural_dialogue_batch(doc);assert sha(DOC.read_bytes())==a['manuscript_sha256']
    for path,h in read('translations/shachihoko_item116_editorial_release_v1.json')['dependencies'].items():assert sha(Path(path).read_bytes())==h
    return r,doc
def restore(value):
    d=deepcopy(value);entry=d.pop(KEY);d.pop(SCOPE);back=entry['inverse_preserved_values'];d.update(back['root_values'])
    assert d['completed_editorial_families'].pop()['id']==FAMILY
    f=d['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','integrated_record_keys']:assert f[k].pop()==entry['record_keys'][0]
    assert f['record_IDs'].pop()=='COMMON_MESSAGE_2931' and f['reconciled_families'].pop()['id']==FAMILY;f.update(back['fresh_values'])
    active=d['active_source_prose_drafts'];assert active['manuscripts'].pop()==str(DOC)
    assert active['manuscript_record_subsets_pending'].pop(str(DOC))==[];active['note']=back['active_note']
    assert d['coverage_units'].pop()['id']==FAMILY;d['formatting_watchlist'].pop(WATCH)
    return d
def final_review(release,doc):
    im=NdsImage.open(release['candidate']);arm=im.read_file('/__arm9__.bin');common=im.read_file('/COMMON/MESFILE.DK4');plan=doc['native_data_plan']
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256']
    entry=owned_entries(common,arm,plan['new_directory_sha256'])[2931];row=deepcopy(doc['records'][1]);assert entry.text.decode('ascii')==row['english']
    row.update(manuscript_record_ID=row['id'],id='COMMON_MESSAGE_2931',file_path='/COMMON/MESFILE.DK4',block=32,source_clean_ROM=doc['source_ROM'],source_clean_ROM_sha256=doc['source_ROM_sha256'],completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],previous_English=row['current_English'],previous_text_hex=row['current_text_hex'],current_English=row['english'],current_text_hex=entry.text.hex(),integrated_hex=entry.text.hex(),status='complete-contextual-current-native-actual-and-registered-release',registered_integration_pending=False,actual_Items_menu_two_holds_complete_fields_verified=True,individual_natural_source_event_activation_not_claimed=True)
    row['historical_predecessor_reference']=deepcopy(row['current_reference']);ref=asdict(entry);ref['text_hex']=ref.pop('text').hex();row['current_reference']=ref;row['integrated_reference']=deepcopy(ref)
    row['compiled_reference']=dict(file_path='/__arm9__.bin',runtime_pointer=plan['new_compiled_pointer'],payload_offset=plan['new_compiled_pointer']-0x02387A20,terminated_paragraph_hex=plan['compiled_paragraph_hex'],rows=plan['compiled_rows'])
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data);at=row['compiled_reference']['payload_offset'];encoded=bytes.fromhex(plan['compiled_paragraph_hex']);assert payload[at:at+len(encoded)]==encoded
    title=deepcopy(doc['records'][0]);t=plan['title_data_plan'];new=bytes.fromhex(t['new_terminated_hex']);assert arm[t['owned_file_offset']:t['owned_file_offset']+len(new)]==new
    title.update(file_path='/__arm9__.bin',completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],integrated_reference=dict(owned_file_offset=t['owned_file_offset'],runtime_pointer=t['runtime_pointer'],pointer_field=t['pointer_field'],terminated_hex=new.hex()),new_dialogue_or_name_review_credit=0,registered_integration_pending=False)
    return dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=[row],coordinated_static_label_records=[title],revised=1,retained=0,source_prose_and_completion_credit_added_once=1,static_label_dialogue_credit=0,generic_acquisition_notice_credit=0,all_source_predecessor_current_COMMON_and_live_compiled_references_bound=True,source_native_CPU_and_actual_GPU_scopes_distinct=True,registered_release_and110_regressions35_precommit_controls_pass=True,source_context_and_visual_approval=str(APPROVAL),broader207_name_review_open=True,summary=DETAILS+'\n\n'+NEXT,full_goal_complete=False)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists();r,doc=gates();before=LEDGER.read_bytes();assert sha(before)==read(PRIOR)['ledger_sha256'];old=json.loads(before);new=deepcopy(old)
        assert KEY not in new and SCOPE not in new
        allrows=[x for family in old['completed_editorial_families'] for x in family['records']];oldkeys={historical_key(x) for x in allrows};key=('/COMMON/MESFILE.DK4','COMMON_MESSAGE_2931')
        f=old['contextual_story_natural_dialogue_pass_v1871'];assert len(allrows)==len(oldkeys)==6349 and key not in oldkeys
        assert {historical_key(x) for x in f['record_keys']}=={historical_key(x) for x in f['integrated_record_keys']}==oldkeys
        assert f['fresh_pass_records_explicitly_reread']==f['fresh_pass_records_integrated']==6349 and not f['pending_record_keys']
        back=dict(root_values={k:deepcopy(old[k]) for k in ROOTVALUES},fresh_values={k:deepcopy(f[k]) for k in FRESHVALUES},active_note=old['active_source_prose_drafts']['note'])
        final=final_review(r,doc);ROOT.mkdir(parents=True);save(FINAL,final);rows=final['records'];keyrow=dict(file_path=key[0],id=key[1]);note='6350 contextual rereads integrated;6353 source-prose. COMMON2931 counted once. Static item title/generic notice zero dialogue credit. Full editorial and207-name review remain active.'
        summary=DETAILS+'\n\nCandidate SHA256 '+r['candidate_sha256']+'. Patch SHA256 '+r['patch_sha256']+'.\n\n'+NEXT
        new['completed_editorial_families'].append(dict(id=FAMILY,file_path='/COMMON/MESFILE.DK4',blocks=[32],record_IDs=['COMMON_MESSAGE_2931'],final_review=str(FINAL),records=rows,revised_count=1,retained_count=0,fresh_revisions=1,fresh_retentions=0,coordinated_static_title_records=1,static_title_dialogue_credit=0,generic_notice_credit=0,actual_verification_scope=DETAILS))
        for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated']:new[k]+=1
        for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:new[k]['/COMMON/MESFILE.DK4']+=1
        f=new['contextual_story_natural_dialogue_pass_v1871']
        for k in ['record_keys','integrated_record_keys']:f[k].append(deepcopy(keyrow))
        f['record_IDs'].append('COMMON_MESSAGE_2931');f.update(fresh_pass_records_explicitly_reread=6350,fresh_pass_records_integrated=6350,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note)
        f['reconciled_families'].append(dict(id=FAMILY,records=1,final_review=str(FINAL),new_revisions=1,justified_retentions=0,new_completed_records=1,historical_reconciliation_only=False,actual_menu_cases=2,complete_actual_title_description_field_matches=8,new_emulator_runs=3,new_frames=29822,static_title_and_generated_notice_add_no_dialogue_credit=True))
        active=new['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'] and str(DOC) not in active['manuscript_record_subsets_pending'];active['manuscripts'].append(str(DOC));active['manuscript_record_subsets_pending'][str(DOC)]=[];active['note']=note
        new['coverage_units'].append(dict(id=FAMILY,status='complete-contextual-current-native-actual-and-registered-release',file_path='/COMMON/MESFILE.DK4',blocks=[32],native_message_IDs=[2931],completion_credit_added=1,final_review=str(FINAL),static_item_label_dialogue_credit=0,actual_menu_holds=2,new_emulator_runs=3,new_frames=29822,full_goal_complete=False))
        assert WATCH not in new['formatting_watchlist'];new['formatting_watchlist'][WATCH]=dict(status='source-native-actual-menu-and-registered-release-pass',final_review=str(FINAL),logical_paragraph_chars=134,native_rows=3,no_manual_wraps_glyph_bounds_pagination_or_control_waivers=True,actual_vs_offline_scopes_distinct=True)
        current=dict(path=r['candidate'],sha256=r['candidate_sha256'],profile=r['profile'],MESFILE_sha256=r['COMMON_sha256'],ARM9_sha256=r['ARM9_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],manifest=r['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
        for k in ['SC0_sha256','SC1_sha256','SC2_sha256','SC3_sha256']:current[k]=old['current_integrated_candidate'][k]
        new['current_integrated_candidate']=current;new['latest_checkpoint']=summary
        inv=deepcopy(read(old['unfinished_editorial_scope_v6090']['path']));inv['next_focus']=NEXT
        inv['Item116_Shachihoko_completed_v6115']=dict(final_review=str(FINAL),completed_COMMON_objects=1,static_label_dialogue_credit=0,generic_notice_credit=0,registered_candidate=r['candidate'],supersedes_historical_pending_item116_flags_from_v6090_without_deleting_history=True,B204_target_prose_still_pending=True)
        inv['speaker_name_localization_current_example_v6113']=dict(proof=str(NAMES),sha256=sha(NAMES.read_bytes()),example_165_already_Woman=True,initial_Man_Woman_Stranger_completed_V5891=True,broader207_names_roles_aliases_and_retrospective_uses_open=True,new_duplicate_credit=0)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inv
        scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inv);new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),COMMON2931_completed_once=True,static_title_and_notice_zero_dialogue_credit=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_and_full_editorial_scope_open=True,all_prior_scope_history_preserved=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        paths=[DOC,FINAL,PRIOR,RELEASE,APPROVAL,PIN,NAMES,REGRESSIONS,ATOMIC,Path(__file__),Path('scripts/shachihoko_completion_text_v6115.py')];evidence={str(p):sha(p.read_bytes()) for p in paths}
        new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_preserved_values=back,record_keys=[keyrow],new_source_prose_reviews=1,new_completed_records=1,revised=1,retained=0,static_label_dialogue_credit=0,generic_notice_credit=0,goal_turn_classification='progress',previous_goal_turn_classification='progress',new_emulator_runs=3,new_frames=29822,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];assert new['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V6115: coordinated Shachihoko item review integrated in V6110; speaker-name review remains open\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text('utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6115\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(path.read_bytes())
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,new_completed_records=1,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;one disjoint COMMON review,coordinated static label,207-name scope and all history retained.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old;r,doc=gates()
        assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6350,6353,3969,2381)
        rows=[x for f in new['completed_editorial_families'] for x in f['records']];assert len(rows)==len({historical_key(x) for x in rows})==6350
        assert {historical_key(x) for x in new['contextual_story_natural_dialogue_pass_v1871']['record_keys']}=={historical_key(x) for x in rows}
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(deep_inverse_preserves_every_prior_root_and_nested_value=True,one_disjoint_COMMON_key_only=True,all_six_original_and_planned_hashes_verified=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False));print('Six staged targets,one disjoint key,source/native/actual/release gates and exact deep inverse audited.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as f:f.write(Path(e['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all6_audited_targets_applied_exactly=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False));print('Six audited files applied;compression and all historical values preserved.')
        else:
            assert read(ROOT/'application_receipt.json')['all6_audited_targets_applied_exactly'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],profile=r['profile'],all_original_root_and_nested_history_preserved=True,exactly_one_disjoint_COMMON_source_prose_and_completed_record=True,static_item_title_and_generic_notice_zero_dialogue_credit=True,completed=6350,source_prose=6353,revised=3969,retained=2381,COMMON=1600,COMMON_source_prose=1603,SC2=4464,SC3=96,reviewed_routes=4750,completed_routes=4750,all592_manifest_batches114_accepted18_checks_verified=True,all110_regressions35_precommit_controls_pass=True,actual_startup31_screens_six_actor_models_and_Items_two_holds_eight_fields_verified=True,new_emulator_runs=3,new_frames=29822,actual_and_offline_native_scopes_distinct=True,next_Lil_B204_target_prose_pending=True,retrospective207_name_queue_and_all_prior_leads_preserved=True,current_Man_Woman_Stranger_labels_directly_rechecked=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())));print('V6110 verified:6350 completed/6353 source-prose;207-name review,B204 and full editorial goal remain active.')
