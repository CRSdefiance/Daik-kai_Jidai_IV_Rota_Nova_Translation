"""Credit eighteen disjoint decisions once; stage, inverse-audit, apply and verify six files."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.complete_B210_Ferid_v6547 import digest,parent_at
from scripts.lil_B213_completion_gates_v6691 import gates,RELEASE,START,VIEW,REG,PIN
from scripts.lil_B213_completion_text_v6691 import DETAILS,NEXT
ROOT=Path('work/analysis/lil_B213_completion_v6691')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6692')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B213_editorial_manuscript_v4.json')
FINAL=Path('translations/lil_B213_contextual_final_review_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6670/verified_handoff.json')
NEXT_SOURCE=Path('work/analysis/lil_B214_clean_context_v6695/all17_clean_letter_reaction_and_notice_glosses_before_old_English.json')
KEY='lil_B213_completion_v6691';FAMILY='Lil-B213-Kublai-Khan-prophecy-whole-exchange18';SCOPE='unfinished_editorial_scope_v6691'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6508,6511,6511,4068,2440);AFTER=(6526,6529,6529,4080,2446)
def restore(value):
    doc=deepcopy(value);entry=doc.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(doc,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][-op['count']:])==op['appended_sha256'];del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return doc
def stage():
    assert not ROOT.exists() and not FINAL.exists();before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==read(PRIOR)['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE
    release=gates();doc=read(DOC);spec=read(doc['reference_map'])['blocks'][0];rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':6}
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[213]
    refs={r['id']:r for r in spec['all_object_references']};changed={r['id']:r for r in release['stage']['changed_records']}
    actual=read(doc['actual_English_proof']);panels={r['id']:r for r in actual['actual_panels']}
    assert len(panels)==18 and sum(r['native_pages'] for r in panels.values())==19
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);body=value[1:]
        assert block[at:at+len(value)+1]==value+b'\0' and changed[row['id']]['new_offset']==at and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        command=next(c for c in spec['command_map'] if c['new_offset']==at-5);template=body.decode('cp932');expanded=body.replace(b'FI',b'Lil')
        assert ' '.join(template.split())==row['english'].split('}',1)[1].replace('{MACRO:FI}','FI') and all(row['review'].values())
        assert row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
        historical_keys=['current_reference','current_hex','current_record_index','current_native_extent','current_raw_storage_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
        row['historical_preintegration_fields']={k:deepcopy(row[k]) for k in historical_keys if k in row}
        newref=dict(block=213,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
        row.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=newref['record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=expanded.decode('cp932'),current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=expanded.hex(),current_effective_paragraph=' '.join(template.split()),current_expanded_paragraph=' '.join(expanded.decode('cp932').split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_record_observed=True,native_plane_verified_not_actual_English_gameplay=False,actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,formatting_reason=row['formatting_reason']+' Registered cumulative integration, exact clean-input reconstruction and current startup are verified. All measured timing, RNG, duration, later RGB and final-world differences remain explicit; no broad simulation or causal equality is claimed.')
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6508 and len(keys)==18 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6508 and not fresh['pending_record_keys']
    assert read(NEXT_SOURCE)['all17_clean_objects_read_before_prior_English']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[DOC,RELEASE,START,VIEW,REG,PIN,PRIOR,NEXT_SOURCE,Path(doc['reference_map']),Path(doc['reference_approval']),Path('translations/lil_B213_editorial_release_v1.json'),*[Path(doc[k]) for k in ['actual_source_proof','actual_English_proof','actual_English_view','speaker_name_review','relocated_control_proof','item150_card_name_contextual_lead']],Path('work/analysis/lil_B213_regressions_v6686/terminal.json'),Path('work/analysis/lil_B213_atomic_v6684/atomic_validation_receipt.json'),Path(__file__),Path('scripts/lil_B213_completion_gates_v6691.py'),Path('scripts/lil_B213_completion_text_v6691.py')]
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=12,retained=6,source_prose_and_completion_credit_added_once=18,previous_B213_objects_uncredited=True,all18_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=18,actual_native_pages=19,actual_complete_body_holds=74,actual_complete_name_holds=74,offline_only_speech_IDs=[],source_event213_natural_activation_location_earned_progress_full_effects_unclaimed=True,all_measured_timing_RNG_duration_RGB_following_and_final_world_limits_preserved=True,three_contextual_name_retentions_no_asset_or_duplicate_credit=True,full_catalogue_UI_unvisited=True,item150_contextual_consumer_review_open=True,evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[k]['/data/SC2.DK4']==4622;put([k,'/data/SC2.DK4'],4640)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[213],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=12,retained_count=6,fresh_revisions=12,fresh_retentions=6,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6526 contextual rereads integrated; 6529 source-prose. Eighteen B213 decisions counted once: twelve revisions and six justified retentions. Actual eighteen speeches/nineteen pages/74 body and name holds; no offline-only speech. Three contextual name retentions add no asset or duplicate dialogue/UI/name credit. All measured later-world limits and the full four-storyline, earlier dialogue, town/shop/random/Help/prose, 207-name and premature-wrap objective remain active.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6526,fresh_pass_records_integrated=6526,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=18,final_review=str(FINAL),new_revisions=12,justified_retentions=6,new_completed_records=18,historical_reconciliation_only=False,actual_selected_source213_events=[],actual_B22_content_objects=18,actual_speeches=18,actual_pages=19,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,new_content_English_runs=1,new_content_English_frames=16001,prior_source16001_run_reused=True)])
    ap=['active_source_prose_drafts'];assert str(DOC) not in new[ap[0]]['manuscripts'];append(ap+['manuscripts'],[str(DOC)]);put(ap+['route_record_subsets_pending',str(DOC)],[]);put(ap+['note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
    for k,v in dict(reviewed_route_records=4926,completed_route_records=4926,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[213],completion_credit_added=18,final_review=str(FINAL),actual_source_event213_selected=False,actual_objects=18,actual_pages=19,offline_only_objects=0,current_candidate_emulator_runs=2,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B213_v6691'],dict(status='eighteen-source-native-reference-representative-registered-release-pass',final_review=str(FINAL),all27_commands_four_relative_predicate_staging_A000_end_and1028_byte_inverse=True,original216x64_four_rows_and19_complete_pages=True,eight_rowcount_reasons_three_ordinary_boundaries_no_global_safety_waiver=True,all18_actual_speeches74_body74_name_holds=True,unaligned_predicate_owned_scratch_and_normal_residual1_preserved=True,all_later_world_limits_preserved=True,three_name_retentions_no_asset_or_duplicate_credit=True,full_catalogue_UI_unvisited_207_scope_and_item150_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    previous=old['unfinished_editorial_scope_v6669'];assert sha(Path(previous['path']).read_bytes())==previous['sha256'];inventory=deepcopy(read(previous['path']))
    inventory['next_focus']=NEXT;inventory['Lil_B213_completed_v6691']=dict(final_review=str(FINAL),completed_objects=18,registered_candidate=release['candidate'],actual_speeches=18,actual_pages=19,offline_speech_IDs=[],all_earlier_pending_B213_flags_preserved_as_history_superseded_here=True,natural_event213_full_effects_earned_progress_unproved=True,three_name_retentions_no_asset_or_duplicate_credit=True)
    inventory['next_Lil_B214_clean_whole_exchange_review_pending']=dict(source_context=str(NEXT_SOURCE),all17_clean_objects_glossed_before_old_English=True,ten_speeches_seven_automatic_bodies_eight_slots=True,no_B213_actor_control_layout_or_effect_assumptions=True,current_prose_consumers_names_native_actual_release_pending=True,new_completion_credit=0)
    inventory['B213_later_world_scope_for_older_record_technical_reaudit_v6691']=dict(proof=doc['actual_English_proof'],view=doc['actual_English_view'],timing=24,RNG=15,duration=4,later_RGB=143,later_split=[79,63,1],final_source_Sea_View_English_Food_notice=True,no_broad_simulation_or_complete_causal_equivalence_claim=True,no_automatic_reopening_of_completed_older_reviews=True)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4926,completed_route_records=4926,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B21318_previously_uncredited_objects_completed=True,next_Lil_B214_clean_review_pending=True,initial_paired_label_review_completed_history_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_item150_and_all_prior_unresolved_leads_open=True,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=18,new_completed_records=18,revised=12,retained=6,goal_turn_classification='progress',goal_turn_new_emulator_runs=3,goal_turn_new_frames=37403,prior_source16001_run_reused=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V6691: B213 integrated in cumulative V6686; contextual name review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V6691\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if target!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    for p in [FINAL,inv]:evidence[str(p)]=sha(p.read_bytes())
    save(ROOT/'staged_completion.json',dict(files=files,new_completed_records=18,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six targets staged; eighteen disjoint B213 decisions counted once. Deep inverse audit next.')
def finish(mode):
    plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
    assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER
    for i,e in enumerate(plan['files']):
        assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        if i:assert Path(e['planned']).read_bytes().endswith(gzip.decompress((ROOT/f'{i:02d}.before.gz').read_bytes()))
    release=gates()
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    if mode=='audit':
        assert not (ROOT/'independent_preapplication_audit.json').exists();save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_and_planned_hashes_verified=True,deep_inverse_recovers_every_original_root_and_nested_history_value=True,every_document_retains_all_original_bytes_as_suffix=True,exactly18_new_disjoint_completed_keys=True,staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),full_goal_complete=False));print('Six targets audited; deep inverse and all original document bytes preserved.')
    elif mode=='apply':
        assert not (ROOT/'native_application_receipt.json').exists() and read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
        for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
        for e in plan['files']:
            with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
        save(ROOT/'native_application_receipt.json',dict(all6_staged_targets_hash_exact=True,all_before_hashes_verified_before_first_write=True,full_goal_complete=False));print('Six audited completion files applied exactly.')
    else:
        assert read(ROOT/'native_application_receipt.json')['all6_staged_targets_hash_exact'] and not VERIFY.exists();final=read(FINAL)
        assert len(final['records'])==18 and all(r['actual_record_observed'] for r in final['records']) and sum(r['native_page_count'] for r in final['records'])==19 and not final['offline_only_speech_IDs']
        assert len({historical_key(r) for family in new['completed_editorial_families'] for r in family['records']})==6526
        VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_preserved=True,exactly18_new_disjoint_source_prose_and_completed_records=True,completed=6526,source_prose=6529,revised=4080,retained=2446,SC2=4640,SC3=96,reviewed_routes=4926,completed_routes=4926,all605_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_unique_B213_speeches=18,actual_B213_pages=19,actual_body_holds=74,actual_name_holds=74,offline_only_B213_speeches=0,startup31_frames_and_five_actor_controls_match_V6641=True,source213_outer_eligibility_natural_activation_location_earned_progress_full_effects_not_claimed=True,all_measured_timing_RNG_duration_RGB_following_and_final_world_limits_preserved=True,unaligned_predicate_owned_scratch_and_normal_residual_value1_preserved=True,three_contextual_name_retentions_no_asset_or_duplicate_credit=True,full_catalogue_UI_unvisited=True,item150_contextual_consumer_review_open=True,no_broad_postscene_equivalence_or_causal_claim=True,next_B214_all17_clean_glosses_before_old_English_pending_current_review=True,retrospective207_name_queue_paired_completed_history_and_all_prior_leads_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V6686 verified: 6526 completed/6529 source-prose. B214 and full editorial/name review remain active.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    stage() if mode=='stage' else finish(mode)
