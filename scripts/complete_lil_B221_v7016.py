"""Integrate sixteen disjoint B221 decisions with a six-target deep history inverse."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B221_completion_gates_v7016 import gates
from scripts.lil_B221_completion_text_v7016 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_completion_v7016')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7017')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6991/verified_handoff.json')
DOC=Path('translations/lil_B221_editorial_manuscript_v3.json')
MENU=Path('translations/lil_B221_choice_manuscript_v3.json')
FINAL=Path('translations/lil_B221_contextual_final_review_v1.json')
KEY='lil_B221_completion_v7016';SCOPE='unfinished_editorial_scope_v7016'
FAMILY='Lil-B221-Crusades-Saladin-two-choices-whole-exchange16'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6603,6606,6606,4126,2477);AFTER=(6619,6622,6622,4134,2485)

def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())

def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count']
            assert digest(parent[key][op['before_length']:])==op['appended_sha256']
            del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates()
    before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==read(PRIOR)['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE
    doc,menu=read(DOC),read(MENU);mapping=read(doc['reference_map']);spec=mapping['blocks'][0]
    assert doc['current_ROM_sha256']==menu['current_ROM_sha256']==read(PRIOR)['candidate_sha256']
    rows=deepcopy(doc['records']+menu['records'])
    refs={r['id']:r for r in spec['text_records']+spec['choice_commands'][0]['label_references']}
    commands={r['new_offset']:r for r in spec['command_map']}
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[221]
    assert sha(block)==spec['target_block_sha256'] and len(block)==1224
    assert len(spec['command_map'])==21 and len(spec['relative_skip_fixups'])==4 and len(spec['choice_commands'])==1
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(value)+1]==value+b'\0' and block[:at].count(b'\0')==ref['new_record_index']
        assert all(row['review'].values()) and not row['current_complete_native_display_pending']
        speech=row['kind']=='progressive'
        newref=dict(block=221,offset=at,bytes=len(value),record_index=ref['new_record_index'])
        row['historical_preintegration_record']=deepcopy(row)
        if speech:
            assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            assert ' '.join(value[1:].decode('ascii').split())==row['english'].split('}',1)[1]
            assert row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
            newref['header_offset']=at-5;body=value[1:];extent=commands[at-5]['new_extent']
        else:
            assert value.decode('ascii')==row['english'] and row['actual_observed_choice_paths']==[0,1]
            assert row['native_indices_and_original_return_values_preserved']
            body=value;extent=len(value)+1
        row.update(current_reference=deepcopy(newref),integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),
            current_record_index=newref['record_index'],current_native_extent=extent,integrated_command_extent=extent,
            current_raw_storage_English=body.decode('ascii'),current_stored_English=body.decode('ascii'),current_effective_runtime_English=body.decode('ascii'),
            current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(body.decode('ascii').split()),
            current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],
            registered_integration_pending=False,current_native_voice_macro_entry_and_context_pending=False,current_native_typed_choice_font_reference_and_outcome_binding_pending=False,
            source_prose_or_completion_credit_added=1,new_review_credit=1,
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',
            status='complete-contextual-current-native-reference-representative-and-registered-release',
            actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,
            formatting_reason='All final logical/compiled/stored native glyphs,bounds,guards,pages,voices,preambles,four relative sites,typed menu,A000 and complete normal-end value words pass. Both original choices,all14 speeches,30 actual page observations and118 complete body/name holds are observed. Exact clean-input reconstruction,registered release,current startup and110 regressions pass. Historical preintegration reason and all individual wrap/page/row reasons remain. Shared Shopkeeper localization,catalogue UI,natural eligibility/full effects and all later-world differences remain open in their documented scopes.')
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':8}
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6603 and len(keys)==16 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6603 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[DOC,MENU,PRIOR,Path(__file__),Path('scripts/lil_B221_completion_gates_v7016.py'),Path('scripts/lil_B221_completion_text_v7016.py')]
    paths += [Path(doc[k]) for k in ['reference_map','reference_approval','actual_source_proof','actual_English_proof','actual_English_view','later_scope_proof','speaker_name_review','native_stored_proof','policy_validation']]
    paths += [Path('work/analysis')/p for p in [
        'lil_B221_release_v7012/registered_release_verification.json','lil_B221_startup_v7015/cold_boot_Lil_startup_town_verification.json',
        'lil_B221_startup_v7015/current_six_frame_visual_review.json','lil_B221_registration_v7010/registration_receipt.json',
        'lil_B221_retention_v7013/pin_receipt.json','lil_B221_atomic_v7009/atomic_validation_receipt.json','lil_B221_regressions_v7011/terminal.json']]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscripts={str(p):sha(p.read_bytes()) for p in [DOC,MENU]},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
        revised=8,retained=8,source_prose_and_completion_credit_added_once=16,previous_B221_objects_uncredited=True,
        all16_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=14,actual_choice_labels=2,actual_native_pages=16,
        actual_native_page_observations=30,actual_complete_body_holds=118,actual_complete_name_holds=118,offline_only_object_IDs=[],
        both_original_choice_paths_and_all30_fixture_commands_observed=True,source_normal_values=[0,1],English_normal_values=[0,1],
        personal_name_retentions_no_asset_or_duplicate_credit=True,shared_ten_Shopkeeper_layer_pending=True,full_catalogue_UI_unvisited=True,
        all_measured_later_world_differences_and_natural_gameplay_limits_preserved=True,later_scope_proof=doc['later_scope_proof'],evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
        ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[k]['/data/SC2.DK4']==4717;put([k,'/data/SC2.DK4'],4733)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[221],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,
        revised_count=8,retained_count=8,fresh_revisions=8,fresh_retentions=8,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6619 contextual rereads integrated;6622 source-prose/drafts. B22116 disjoint decisions:eight revisions/eight justified retentions. All14 speeches,both options,30 actual page observations,118 body/name holds and all30 fixture commands observed. Shared ten Shopkeeper labels and wider207-name/retrospective-wrap objective remain open;all timing,RNG,calendar,actor,RGB and original normal-end residuals preserved for later technical re-audit.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6619,fresh_pass_records_integrated=6619,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=16,final_review=str(FINAL),new_revisions=8,justified_retentions=8,new_completed_records=16,
        historical_reconciliation_only=False,actual_selected_source221_events=[],actual_B22_content_objects=16,actual_speeches=14,actual_choice_labels=2,actual_pages=16,
        actual_page_observations=30,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,
        new_content_English_runs=2,new_content_English_frames=32002,prior_source_two16001_runs_reused=True)])
    for p in [DOC,MENU]:
        assert str(p) not in new['active_source_prose_drafts']['manuscripts']
        append(['active_source_prose_drafts','manuscripts'],[str(p)]);put(['active_source_prose_drafts','route_record_subsets_pending',str(p)],[])
    put(['active_source_prose_drafts','note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
    for k,v in dict(reviewed_route_records=5019,completed_route_records=5019,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[221],
        completion_credit_added=16,final_review=str(FINAL),actual_source_event221_selected=False,actual_objects=16,actual_pages=16,actual_page_observations=30,
        offline_only_objects=0,current_candidate_emulator_runs=2,all_measured_later_world_limits_preserved=True,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B221_v7016'],dict(status='16-source-native-reference-16-actual-registered-release-pass',final_review=str(FINAL),
        all21_commands_four_relatives_whole_menu_A000_normal_end_and1208_inverse=True,original216x64_four_rows16_complete_pages=True,
        seven_rowcount25_boundary_R67_auxiliary_and_two_page_reasons_preserved=True,zero_QA_warnings_all_diagnostics_retained=True,
        both_actual_choices14_speeches30_page_observations118_body_name_holds=True,shared_Shopkeeper_layer_and207_names_open=True,all_measured_later_world_limits_preserved=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    previous=old['unfinished_editorial_scope_v6990'];assert sha(Path(previous['path']).read_bytes())==previous['sha256']
    inventory=deepcopy(read(previous['path']));inventory['next_focus']=NEXT
    inventory['Lil_B221_completed_v7016']=dict(final_review=str(FINAL),completed_objects=16,registered_candidate=release['candidate'],actual_speeches=14,actual_choice_labels=2,
        actual_pages=16,actual_page_observations=30,offline_only_object_IDs=[],all_earlier_pending_B221_flags_preserved_as_history_superseded_here=True,
        event221_natural_activation_earned_progress_full_effects_unproved=True,shared_ten_Shopkeeper_layer_pending=True,all_measured_later_world_differences_retained=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5019,completed_route_records=5019,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B22116_previously_uncredited_objects_completed=True,
        ten_Shopkeeper_source_contexts_complete_target_shared_native_and_release_pending=True,next_Lil_B222_whole_exchange_review_pending=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_item150_and_all_prior_unresolved_leads_open=True,
        broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=16,new_completed_records=16,revised=8,retained=8,
        goal_turn_classification='progress',goal_turn_new_emulator_runs=4,goal_turn_new_frames=53404,prior_source_two16001_runs_reused=True,
        all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V7016: B221 integrated in cumulative V7011; full speaker-name review remains active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7016\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all16_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six targets staged;16 disjoint objects,8 revisions/8 retentions. Deep inverse audit next.',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))
        new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:
            assert sha(Path(e['planned']).read_bytes())==e['planned_sha256']
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h,p
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_nested_record_and_counter=True,
                all_six_before_and_planned_hashes_verified=True,exactly16_disjoint_new_objects=True,full_goal_complete=False))
            print('Six targets inverse-audited;all prior root,nested records,counters and history recover exactly.',flush=True)
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for e in plan['files']:assert Path(e['target']).is_relative_to(Path.cwd().resolve()) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False))
            print('Six audited completion targets applied exactly.',flush=True)
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],
                patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_preserved=True,
                exactly16_new_disjoint_source_prose_and_completed_records=True,completed=6619,source_prose=6622,revised=4134,retained=2485,SC2=4733,SC3=96,reviewed_routes=5019,completed_routes=5019,
                all613_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_unique_B221_speeches=14,actual_B221_choice_labels=2,actual_B221_pages=16,
                actual_native_page_observations=30,actual_body_holds=118,actual_name_holds=118,offline_only_B221_objects=[],startup31_frames_and_five_actor_controls_match_V6956=True,
                source221_outer_eligibility_natural_activation_location_earned_progress_full_effects_not_claimed=True,personal_name_retentions_no_asset_or_duplicate_credit=True,
                shared_ten_Shopkeeper_layer_pending=True,full_catalogue_UI_unvisited=True,all_individual_wrap_page_row_reasons_and_QA_diagnostics_retained=True,
                all_measured_later_timing_RNG_calendar_actor_and_RGB_differences_preserved=True,no_broad_simulation_equivalence_or_causal_claim=True,
                retrospective207_name_queue_paired_completed_history_and_all_prior_leads_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7016 verified:V7011 cumulative,6619 completed/6622 source-prose. Sixteen B221 objects credited once;full goal active.',flush=True)
