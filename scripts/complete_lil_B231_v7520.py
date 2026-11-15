"""Integrate sixteen disjoint decisions only after release gates; preserve an exact deep inverse."""
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
from scripts.lil_B231_completion_gates_v7520 import gates,RELEASE,START,VIEW,REG,PIN
from scripts.lil_B231_completion_text_v7520 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B231_completion_v7520');VERIFY=Path('work/analysis/editorial_handoff_verification_v7521')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7509/verified_handoff.json')
DOC=Path('translations/lil_B231_editorial_manuscript_v4.json');FINAL=Path('translations/lil_B231_contextual_final_review_v1.json')
KEY='lil_B231_completion_v7520';SCOPE='unfinished_editorial_scope_v7520';FAMILY='Lil-B231-medical-book-fatigue-report-old-Mediterranean-clue-andwarm-reassurance-whole-exchange16'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];BEFORE=(6756,6759,6759,4220,2536);AFTER=(6772,6775,6775,4230,2542)
def digest(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
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
    doc=read(DOC);spec=read(doc['reference_map'])['blocks'][0];rows=deepcopy(doc['records']);actual=read(doc['actual_English_proof']);panels={r['id']:r for r in actual['actual_panels']}
    assert doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256'] and Counter(r['editorial_decision'] for r in rows)=={'revise':10,'retain-wording':6} and len(panels)==16 and sum(p['native_pages'] for p in panels.values())==16
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[231];refs={r['id']:r for r in spec['all_object_references']};changed={r['id']:r for r in release['stage']['changed_records']}
    assert sha(block)==spec['target_block_sha256'] and len(block)==752 and len(spec['command_map'])==18
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);body=value[1:]
        assert block[at:at+len(value)+1]==value+b'\0' and changed[row['id']]['new_offset']==at and block[:at].count(b'\0')==ref['new_record_index']
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'];command=next(c for c in spec['command_map'] if c['new_offset']==at-5)
        newref=dict(block=231,offset=at,bytes=len(value),record_index=ref['new_record_index'],header_offset=at-5)
        template=body.decode('ascii');assert ' '.join(template.split())==row['english'].split('}',1)[1] and all(row['review'].values()) and row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
        history=['current_reference','current_hex','current_record_index','current_native_extent','current_raw_storage_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
        row['historical_preintegration_fields']={k:deepcopy(row[k]) for k in history if k in row}
        row.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=newref['record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(template.split()),current_expanded_paragraph=' '.join(template.split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,formatting_reason='All16 original216x64/four-row single pages pass128 logical/compiled and64 stored alignments,including complete glyphs,guards,bounds andeight zero-ink tails. Four individual row reasons andone exact justified R35 article continuation preserve all base QA. All63 complete body and63 progressive header holds wereverified andviewed. Registered V7514,exact clean-input patch andown-current startup pass. Static item99 retains its unapproved legacy Medicine title consumer lead;two personal names/null middles,six fresh name planes and24 alignments arebound without catalogue UI approval. Source231 hasno explicit requires/excludes. Reported fatigue management,conditional desire,tentative old Mediterranean report andwarm reassurance remain. All measured late differences andinitialized-scene limits stay explicit.')
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6756 and len(keys)==16 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6756 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[DOC,RELEASE,START,VIEW,REG,PIN,PRIOR,Path(doc['reference_map']),Path(doc['reference_approval']),Path('translations/lil_B231_editorial_release_v1.json'),*[Path(doc[k]) for k in ['actual_source_proof','actual_English_proof','actual_English_view','later_scope_proof','speaker_name_review','relocated_control_proof','native_policy_validation']],Path('work/analysis/lil_B231_regressions_v7514/terminal.json'),Path('work/analysis/lil_B231_atomic_v7512/atomic_validation_receipt.json'),Path('work/analysis/current_V7514_native_v7519/current_native_input.json'),Path('work/analysis/current_V7514_native_v7519/registered_current_native_input_binding.json'),Path('scripts/lil_B231_completion_gates_v7520.py'),Path('scripts/lil_B231_completion_text_v7520.py'),Path(__file__)]
    paths.append(Path(doc['source_context']))
    nextsource=Path('work/analysis/lil_B233_clean_context_v7524/all11_clean_legendary_chisel_paper_library_tools_joke_glosses_before_old_English.json');assert read(nextsource)['all11_clean_glosses_precede_old_English'] and read(nextsource)['prior_English_unread'];empty=Path('work/analysis/lil_B232_clean_inventory_v7522/all_clean_B232_speeches_before_predecessor_comparison.json');assert read(empty)['physical_speech_objects']==0;paths.extend([nextsource,empty])
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=10,retained=6,source_prose_and_completion_credit_added_once=16,previous_B231_objects_uncredited=True,all16_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=16,actual_native_pages=16,actual_complete_body_holds=63,actual_complete_name_holds=63,offline_only_object_IDs=[],source_event231_hasno_explicit_requires_excludes_natural_activation_location_earned_progress_full_effects_unproved=True,two_contextual_progressive_names_null_middles_no_assets_or_duplicate_credit=True,legacy_item99_title_ambiguity_unapproved_static_storage_bound=True,reported_fatigue_management_conditional_desire_uncertain_old_report_andwarm_reassurance_preserved=True,full_catalogue_UI_unvisited_full207_review_active=True,four_row_reasons_one_exact_R35_article_warning_all_base_QA_preserved=True,all16_single_original_four_row_pages_without_authored_layout=True,one_A000_normal_end_source724_logical722_tail2_target752_logical750_tail2_full_inverse_preserved=True,all_measured_late_differences_retained_no_broad_simulation_orcausal_claim=True,all253_fresh_production_rejections_no_prior_case_reuse_bound=True,evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[k]['/data/SC2.DK4']==4870;put([k,'/data/SC2.DK4'],4886)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[231],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=10,retained_count=6,fresh_revisions=10,fresh_retentions=6,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6772 contextual rereads integrated;6775 source-prose. Sixteen disjoint B231 decisions counted once:ten revisions andsix justified retentions. All16 initialized speeches/pages,63 complete body andheader holds;four row reasons andone exact R35 article warning. Exact static item99 legacy Medicine title remains unapproved forbroader consumers. Lil Argot/Carlo Sinat,null middles,six fresh name planes24 alignments;catalogue UI unvisited. Reported fatigue benefit,conditional desire,tentative old Mediterranean clue andwarm reassurance preserved. Source231 hasno explicit requires/excludes;natural activation/location/earned progress/full effects unproved. Full207 names,earlier wraps,all measured late differences andolder-record technical re-audit remain active.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6772,fresh_pass_records_integrated=6772,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=16,final_review=str(FINAL),new_revisions=10,justified_retentions=6,new_completed_records=16,historical_reconciliation_only=False,actual_selected_source231_events=[],actual_B22_content_objects=16,actual_speeches=17,actual_pages=16,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,prior_source_and_final_English16001_runs_reused_without_replay=True)])
    ap=['active_source_prose_drafts']
    if str(DOC) not in new[ap[0]]['manuscripts']:append(ap+['manuscripts'],[str(DOC)])
    put(ap+['route_record_subsets_pending',str(DOC)],[]);put(ap+['note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5156
    for k,v in dict(reviewed_route_records=5172,completed_route_records=5172,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[231],completion_credit_added=16,final_review=str(FINAL),actual_source_event231_selected=False,actual_objects=16,actual_pages=16,offline_only_objects=0,current_candidate_emulator_runs=2,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B231_v7520'],dict(status='16-source-native-reference-representative-registered-release-pass',final_review=str(FINAL),all18_commands_A000_full_end_source724_logical722_tail2_target752_logical750_tail2_inverse=True,original216x64_four_rows16_complete_pages=True,four_row_reasons_one_exact_R35_article_warning_all_base_QA_preserved=True,actual16_pages63_body63_headers=True,two_contextual_progressive_names_null_middles_no_assets_or_duplicate_credit=True,legacy_item99_title_ambiguity_unapproved_static_storage_bound=True,full207_scope_open=True,all_late_differences_andcomparison_limits_preserved=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False);current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    put(['lil_B231_review_pending_v7508','registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior=old['unfinished_editorial_scope_v7508'];assert sha(Path(prior['path']).read_bytes())==prior['sha256'];inventory=deepcopy(read(prior['path']));inventory['next_focus']=NEXT
    inventory['Lil_B231_completed_v7520']=dict(final_review=str(FINAL),completed_objects=16,registered_candidate=release['candidate'],actual_speeches=16,actual_pages=16,source_event231_hasno_explicit_requires_excludes_natural_activation_location_earned_progress_full_effects_unproved=True,two_contextual_progressive_names_null_middles_no_assets_or_duplicate_credit=True,legacy_item99_title_ambiguity_unapproved_static_storage_bound=True,all_late_differences_andearlier_full_objective_leads_preserved=True)
    inventory['Lil_B231_pending_v7508']['registered_integration_completed_by']=dict(final_review=str(FINAL),registered_candidate=release['candidate'],all_historical_pending_flags_preserved_as_superseded_history=True,new_credit_here=0)
    inventory['next_Lil_B233_source_only_gloss_complete']=dict(source_context=str(nextsource),source_context_sha256=sha(nextsource.read_bytes()),clean_speeches=11,all11_clean_glosses_precede_old_English=True,paper_fragment_chisel_legend_Balkan_clue_ship_repair_teasing_kings_tools_joke_andconditional_request_preserved=True,names_voices_historical_spelling_item97_entry_A000_current_prose_native_actual_andrelease_pending=True,new_credit=0)
    inventory['Lil_B232_clean_empty_block_v7522']=dict(proof=str(empty),sha256=sha(empty.read_bytes()),stored_bytes=12,commands=1,speech_objects=0,no_dialogue_credit=True,natural_activation_andfull_effects_not_claimed=True,new_credit=0)
    # Preserve all earlier B225/B226 technical audit leads from the full prior inventory.
    inventory['later_B231_measurement_andmetadata_technical_reaudit_v7520']=dict(actual=doc['actual_English_proof'],later=doc['later_scope_proof'],thirteen_command_three_duration_92of155_RGB_calendar_PRNG_components_actor_differences_preserved=True,both_final_Sailor_Food_dialogues_complete_butwhole_frames_differ=True,item99_legacy_title_unapproved_source_audit_copied_key_failure_successor_R9_neutral_gloss_R12_metadata_correction_andpending_label_correction_preserved=True,all_layouts_andsole_exact_R35_article_warning_preserved=True,all253_fresh_production_rejections_bound_no_prior_case_reuse=True,no_broad_simulation_orcausal_claim=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5172,completed_route_records=5172,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B23116_previously_uncredited_objects_completed=True,full207_name_role_alias_and_retrospective_wrapping_scope_preserved=True,all_prior_unresolved_leads_and_completed_name_history_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,broader_four_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,all_B218_B222_B223_B224_B225_B226_B227_B228_B229_B230_andB231_technical_leads_preserved=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=16,new_completed_records=16,revised=10,retained=6,goal_turn_classification='progress',new_current_candidate_emulator_runs=2,new_current_candidate_frames=21402,prior_source_and_final_English_content_runs_reused_without_replay=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7472: B231 integrated in cumulative V7514; full editorial goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7472; V7514 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all16_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;16 disjoint objects,ten revisions/six retentions. Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_nested_record_and_counter=True,all_six_before_and_planned_hashes_verified=True,exactly16_disjoint_new_objects=True,full_goal_complete=False));print('Six targets inverse-audited;every prior root,nested record andhistory value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited cumulative completion targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_recover_exactly=True,exactly16_new_disjoint_source_prose_and_completed_records=True,completed=6772,source_prose=6775,revised=4230,retained=2542,SC2=4886,SC3=96,reviewed_routes=5172,completed_routes=5172,all624_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_B231_speeches=16,actual_B231_pages=16,actual_body_holds=63,actual_name_holds=63,offline_only_B231_objects=[],startup31_frames_and_five_actor_controls_match_V7466=True,source231_hasno_explicit_requires_excludes_natural_eligibility_location_activation_earned_progress_full_effects_not_claimed=True,two_contextual_progressive_names_null_middles_no_assets_or_duplicate_credit=True,legacy_item99_title_ambiguity_unapproved=True,full207_review_open=True,four_row_reasons_one_exact_R35_article_warning_all_original_QA_preserved=True,all16_single_original_four_row_pages_no_authored_layout=True,no_global_QA_font_viewport_pairphase_guard_or_literal_I_change=True,all_measured_late_differences_preserved=True,no_broad_simulation_equivalence_or_causal_claim=True,full_four_storyline_editorial_names_retrospective_wrap_and_all_prior_leads_active=True,current_native_input='work/analysis/current_V7514_native_v7519/current_native_input.json',current_native_input_sha256=sha(Path('work/analysis/current_V7514_native_v7519/current_native_input.json').read_bytes()),next_B232_zero_speeches_B23311_clean_glosses_before_old_English=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7520 verified:V7514 cumulative,6772 completed/6775 source-prose.16 B231 objects counted once;full goal active.')
