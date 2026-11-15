"""Credit16 disjoint B222 speeches with a six-target reversible coverage/history update."""
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
from scripts.lil_B222_completion_gates_v7072 import gates
from scripts.lil_B222_completion_text_v7072 import DETAILS,NEXT,CURRENT_NATIVE_NOTE
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_completion_v7072');VERIFY=Path('work/analysis/editorial_handoff_verification_v7073')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7035/verified_handoff.json')
DOC=Path('translations/lil_B222_editorial_manuscript_v5.json');FINAL=Path('translations/lil_B222_contextual_final_review_v1.json')
KEY='lil_B222_completion_v7072';SCOPE='unfinished_editorial_scope_v7072';FAMILY='Lil-B222-Noritsune-sunset-armor-whole-exchange16'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(6619,6622,6622,4134,2485);AFTER=(6635,6638,6638,4146,2489)
def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256'];del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==read(PRIOR)['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE
    doc=read(DOC);mapping=read(doc['reference_map']);actual=read(doc['actual_English_proof']);later=read(doc['later_scope_proof'])
    assert doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256'] and actual['actual_unique_speeches']==16 and actual['actual_complete_body_holds']==actual['actual_complete_name_holds']==63 and actual['all27_commands_observed']
    assert len(later['command_comparison_differences'])==7 and len(later['later_sampled_RGB_differences'])==92 and later['total_later_sampled_frames']==155
    rows=deepcopy(doc['records']);spec=mapping['blocks'][0];refs={r['id']:r for r in spec['text_records']};commands={r['new_offset']:r for r in spec['command_map']}
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[222]
    assert sha(block)==spec['target_block_sha256'] and len(block)==1336 and len(commands)==18
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);command=commands[at-5]
        assert block[at:at+len(value)+1]==value+b'\0' and block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and block[:at].count(b'\0')==ref['new_record_index']
        body=value[1:];template=body.decode('ascii');assert ' '.join(template.split())==row['english'].split('}',1)[1] and all(row['review'].values()) and row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
        newref=dict(block=222,offset=at,bytes=len(value),record_index=ref['new_record_index'],header_offset=at-5)
        history=['current_reference','current_hex','current_record_index','current_native_extent','current_stored_English','current_raw_storage_English','current_effective_runtime_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','current_registered_catalogue_match','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
        row['historical_preintegration_fields']={k:deepcopy(row[k]) for k in history if k in row}
        row.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=newref['record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(template.split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,current_native_voice_macro_entry_and_context_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,formatting_reason='Complete logical/compiled/stored and actual English pages,first/internal/final glyphs,guards,bounds,pagination,all18 commands/preambles/voices,zero macros,A000,complete normal end/no tail and full1112-byte inverse pass. Seven individual row-count explanations and two exact record-local weak-boundary waivers preserve every original base QA diagnostic. All16 source/English speeches and both current names have complete actual holds. Registered cumulative integration,exact clean-input patch reconstruction and current startup pass. Initialized location/eligibility limits,full catalogue UI and all later-world differences remain explicit. Historical preintegration reason is retained.')
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6619 and len(keys)==16 and not oldkeys&keys and Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':4}
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6619 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+CURRENT_NATIVE_NOTE+'\n\n'+NEXT
    nextsource=Path('work/analysis/lil_B223_clean_context_v7076/all17_clean_Timur_armor_letter_reaction_and_notice_glosses_before_old_English.json');assert read(nextsource)['all17_clean_objects_read_before_prior_English'] and read(nextsource)['prior_English_unread']
    paths=[nextsource,DOC,PRIOR,Path(doc['reference_map']),Path(doc['reference_approval']),Path(doc['actual_source_proof']),Path(doc['actual_English_proof']),Path(doc['actual_English_view']),Path(doc['later_scope_proof']),Path(doc['speaker_name_review']),Path('work/analysis/lil_B222_release_v7068/registered_release_verification.json'),Path('work/analysis/lil_B222_startup_v7071/cold_boot_Lil_startup_town_verification.json'),Path('work/analysis/lil_B222_startup_v7071/current_six_frame_visual_review.json'),Path('work/analysis/lil_B222_registration_v7066/registration_receipt.json'),Path('work/analysis/lil_B222_retention_v7069/pin_receipt.json'),Path('work/analysis/lil_B222_atomic_v7065/atomic_validation_receipt.json'),Path('work/analysis/lil_B222_regressions_v7067/terminal.json'),Path('scripts/lil_B222_completion_gates_v7072.py'),Path('scripts/lil_B222_completion_text_v7072.py'),Path(__file__)]
    native_input=Path('work/analysis/current_V7067_native_v7077/current_native_input.json');assert read(native_input)['current_ROM_sha256']==release['candidate_sha256']
    paths.extend([native_input,Path('work/analysis/current_V7067_native_v7077/registered_current_native_input_binding.json')]);evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=12,retained=4,source_prose_and_completion_credit_added_once=16,previous_B222_objects_uncredited=True,all16_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=16,actual_native_pages=16,actual_complete_body_holds=63,actual_complete_name_holds=63,offline_only_object_IDs=[],all27_fixture_commands_stored_and_executed=True,two_contextual_native_name_retentions_no_asset_or_duplicate_credit=True,seven_individual_rowcount_reasons_two_exact_waivers_all_base_diagnostics_preserved=True,no_global_QA_or_geometry_change=True,full_catalogue_UI_unvisited=True,all_measured_later_world_differences_and_natural_gameplay_limits_preserved=True,later_scope_proof=doc['later_scope_proof'],evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[k]['/data/SC2.DK4']==4733;put([k,'/data/SC2.DK4'],4749)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[222],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=12,retained_count=4,fresh_revisions=12,fresh_retentions=4,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6635 contextual rereads integrated;6638 source-prose. Sixteen B222 decisions counted once:12 revisions/4 justified retentions. All16 Japanese/English speeches,63 complete body/name holds each,all27 fixture commands. Two contextual personal-name retentions,no asset/duplicate credit. Seven row reasons,two exact ordinary soft-wrap waivers and all original diagnostics retained. Full editorial/207-name/retrospective-wrap scope and later-world limits remain active.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6635,fresh_pass_records_integrated=6635,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=16,final_review=str(FINAL),new_revisions=12,justified_retentions=4,new_completed_records=16,historical_reconciliation_only=False,actual_selected_source222_events=[],actual_B22_content_objects=16,actual_speeches=16,actual_pages=16,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,new_content_English_runs=1,new_content_English_frames=16001,source_Japanese_run16001_separately_bound=True)])
    ap=['active_source_prose_drafts'];assert str(DOC) not in new[ap[0]]['manuscripts'];append(ap+['manuscripts'],[str(DOC)]);put(ap+['route_record_subsets_pending',str(DOC)],[]);put(ap+['note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
    for k,v in dict(reviewed_route_records=5035,completed_route_records=5035,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[222],completion_credit_added=16,final_review=str(FINAL),actual_source_event222_selected=False,actual_objects=16,actual_pages=16,offline_only_objects=0,current_candidate_emulator_runs=2,all_measured_later_world_limits_preserved=True,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B222_v7072'],dict(status='16-source-native-reference-16-actual-registered-release-pass',final_review=str(FINAL),all18_commands_preambles_A000_complete_normal_end_no_tail1112_inverse=True,original216x64_four_rows16_complete_pages=True,seven_rowcount_reasons_two_exact_weak_boundary_waivers_all_diagnostics_retained=True,no_global_weak_rule_font_geometry_guard_or_literal_I_change=True,actual16_objects63_body63_name_holds=True,two_name_retentions_no_asset_or_duplicate_credit=True,full_catalogue_UI_unvisited_and207_scope_open=True,all_measured_later_world_limits_preserved=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    previous=old['unfinished_editorial_scope_v7034'];assert sha(Path(previous['path']).read_bytes())==previous['sha256'];inventory=deepcopy(read(previous['path']));inventory['next_focus']=NEXT
    inventory['Lil_B222_completed_v7072']=dict(final_review=str(FINAL),completed_objects=16,registered_candidate=release['candidate'],actual_speeches=16,actual_pages=16,offline_only_object_IDs=[],all_earlier_pending_B222_flags_preserved_as_history_superseded_here=True,event222_natural_activation_earned_progress_full_effects_unproved=True,two_native_name_retentions_no_asset_or_duplicate_credit=True,all_measured_later_world_differences_retained=True)
    inventory['next_Lil_B223_clean_gloss_complete_current_review_pending']=dict(source_context=str(nextsource),source_context_sha256=sha(nextsource.read_bytes()),all17_clean_objects_read_before_prior_English=True,ten_speeches_seven_stored_notices_eight_style_slots=True,old_English_unread=True,current_prose_names_voices_controls_native_actual_and_release_pending=True,new_credit=0)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5035,completed_route_records=5035,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B22216_previously_uncredited_speeches_completed=True,next_Lil_B223_all17_clean_glosses_before_old_English_current_review_pending=True,full207_name_role_alias_and_retrospective_wrapping_scope_preserved=True,Shopkeeper82_91_and_Man_Woman_and_Stranger_Shady_Man_completed_history_preserved=True,remaining_occupational_groups_and_Sailor_Retainer151_open=True,five_other_Janus_Pasha_consumers_pending=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,all_prior_unresolved_leads_preserved=True,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,B218_metadata217_actual218_deferred_technical_lead_preserved=True,B222_measured_later_world_limits_preserved=True,full_goal_complete=False))
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=16,new_completed_records=16,revised=12,retained=4,goal_turn_classification='progress',new_current_candidate_emulator_runs=2,new_current_candidate_frames=21402,new_English_content_emulator_runs=1,new_English_content_frames=16001,source_Japanese16001_run_separately_bound=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7072: B222 integrated in cumulative V7067; full editorial and207-name goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7072\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes());save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all16_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;16 disjoint objects,12 revisions/4 retentions. Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_nested_record_and_counter=True,all_six_before_and_planned_hashes_verified=True,exactly16_disjoint_new_objects=True,full_goal_complete=False));print('Six targets inverse-audited;every prior root,nested record and history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited cumulative completion targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_preserved=True,exactly16_new_disjoint_source_prose_and_completed_records=True,completed=6635,source_prose=6638,revised=4146,retained=2489,SC2=4749,SC3=96,reviewed_routes=5035,completed_routes=5035,all615_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_unique_B222_speeches=16,actual_B222_pages=16,actual_body_holds=63,actual_name_holds=63,offline_only_B222_objects=[],startup31_frames_and_five_actor_controls_match_V7029=True,source222_outer_eligibility_natural_Japan_activation_earned_progress_full_effects_not_claimed=True,two_contextual_native_name_retentions_no_asset_or_duplicate_credit=True,full_catalogue_UI_unvisited=True,seven_row_reasons_two_exact_soft_wrap_waivers_all_diagnostics_preserved=True,no_global_QA_rule_font_viewport_pairphase_guard_or_literal_I_change=True,all_measured_later_timing_RNG_actor_and_RGB_differences_preserved=True,no_broad_simulation_equivalence_or_causal_claim=True,full_editorial207_name_retrospective_wrap_and_all_prior_leads_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7072 verified:V7067 cumulative,6635 completed/6638 source-prose.16 B222 objects counted once;full goal active.')
