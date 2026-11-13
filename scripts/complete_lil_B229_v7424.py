"""Integrate seventeen disjoint decisions only after release gates; preserve an exact deep inverse."""
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
from scripts.lil_B229_completion_gates_v7424 import gates,RELEASE,START,VIEW,REG,PIN
from scripts.lil_B229_completion_text_v7424 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B229_completion_v7424');VERIFY=Path('work/analysis/editorial_handoff_verification_v7425')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7413/verified_handoff.json')
DOC=Path('translations/lil_B229_editorial_manuscript_v4.json');FINAL=Path('translations/lil_B229_contextual_final_review_v1.json')
KEY='lil_B229_completion_v7424';SCOPE='unfinished_editorial_scope_v7424';FAMILY='Lil-B229-giant-tortoise-shield-running-joke-andconditional-reassurance-whole-exchange17'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];BEFORE=(6722,6725,6725,4205,2517);AFTER=(6739,6742,6742,4211,2528)
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
    assert doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256'] and Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':11} and len(panels)==17 and sum(p['native_pages'] for p in panels.values())==17
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[229];refs={r['id']:r for r in spec['all_object_references']};changed={r['id']:r for r in release['stage']['changed_records']}
    assert sha(block)==spec['target_block_sha256'] and len(block)==920 and len(spec['command_map'])==19
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);body=value[1:]
        assert block[at:at+len(value)+1]==value+b'\0' and changed[row['id']]['new_offset']==at and block[:at].count(b'\0')==ref['new_record_index']
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'];command=next(c for c in spec['command_map'] if c['new_offset']==at-5)
        newref=dict(block=229,offset=at,bytes=len(value),record_index=ref['new_record_index'],header_offset=at-5)
        template=body.decode('ascii');assert ' '.join(template.split())==row['english'].split('}',1)[1] and all(row['review'].values()) and row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
        history=['current_reference','current_hex','current_record_index','current_native_extent','current_raw_storage_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
        row['historical_preintegration_fields']={k:deepcopy(row[k]) for k in history if k in row}
        row.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=newref['record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(template.split()),current_expanded_paragraph=' '.join(template.split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,formatting_reason='All17 original216x64/four-row single pages pass136 logical/compiled and68 stored alignments,including complete glyphs,guards,bounds andeight zero-ink parity tails. Five informational row reasons preserve all base QA;zero errors,warnings orwaivers. All67 complete body and67 progressive header holds wereverified andviewed. Registered V7418,exact clean-input patch andown-current startup pass. Historical reasoning,staged item53,source229 requires228 andthe two exact B228 echoes remain bound. Samwell full catalogue middle stays unapproved. All measured late differences andinitialized-scene limits remain explicit.')
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6722 and len(keys)==17 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6722 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[DOC,RELEASE,START,VIEW,REG,PIN,PRIOR,Path(doc['reference_map']),Path(doc['reference_approval']),Path('translations/lil_B229_editorial_release_v1.json'),*[Path(doc[k]) for k in ['actual_source_proof','actual_English_proof','actual_English_view','later_scope_proof','speaker_name_review','relocated_control_proof','native_policy_validation']],Path('work/analysis/lil_B229_regressions_v7418/terminal.json'),Path('work/analysis/lil_B229_atomic_v7416b/atomic_validation_receipt.json'),Path('work/analysis/current_V7418_native_v7423/current_native_input.json'),Path('work/analysis/current_V7418_native_v7423/registered_current_native_input_binding.json'),Path('scripts/lil_B229_completion_gates_v7424.py'),Path('scripts/lil_B229_completion_text_v7424.py'),Path(__file__)]
    paths.append(Path(doc['source_context']))
    nextsource=Path('work/analysis/lil_B230_clean_context_v7427/all17_clean_phoenix_bascinet_callback_glosses_before_old_English.json');assert read(nextsource)['all17_clean_glosses_precede_old_English'] and read(nextsource)['prior_English_unread'];paths.append(nextsource)
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=6,retained=11,source_prose_and_completion_credit_added_once=17,previous_B229_objects_uncredited=True,all17_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=17,actual_native_pages=17,actual_complete_body_holds=67,actual_complete_name_holds=67,offline_only_object_IDs=[],source_event229_requires228_does_not_prove_natural_activation_location_earned_completion_or_full_effects=True,two_contextual_progressive_names_no_assets_or_duplicate_credit=True,Samwell_full_catalogue_middle_unapproved_anditem53_staged_storage_bound=True,exact_source_supported_B228_pitch_andpersonal_reassurance_echoes_preserved=True,full_catalogue_UI_unvisited_full207_review_active=True,five_row_reasons_zero_warning_waivers_all_base_QA_preserved=True,all17_single_original_four_row_pages_without_authored_layout=True,one_A000_normal_end_source944_target920_both_no_tail_full_inverse_preserved=True,all_measured_late_differences_retained_no_broad_simulation_orcausal_claim=True,malformed_callback_fixture_not_counted_225_exact_case_reuse_and17_fresh_cases_bound=True,evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[k]['/data/SC2.DK4']==4836;put([k,'/data/SC2.DK4'],4853)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[229],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=6,retained_count=11,fresh_revisions=6,fresh_retentions=11,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6739 contextual rereads integrated;6742 source-prose. Seventeen disjoint B229 decisions counted once:six revisions andeleven justified retentions. All17 initialized speeches/pages,67 complete body andheader holds. Exact B228 callbacks,source229 requires228 anditem53 payload-relative storage arebound. Samwell full catalogue middle stays unapproved. No name assets orduplicate credits. All207 names/roles/aliases,earlier wrapping,all measured late differences andolder-record technical re-audit remain active.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6739,fresh_pass_records_integrated=6739,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=17,final_review=str(FINAL),new_revisions=6,justified_retentions=11,new_completed_records=17,historical_reconciliation_only=False,actual_selected_source229_events=[],actual_B22_content_objects=17,actual_speeches=17,actual_pages=17,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,prior_source_and_final_English16001_runs_reused_without_replay=True)])
    ap=['active_source_prose_drafts']
    if str(DOC) not in new[ap[0]]['manuscripts']:append(ap+['manuscripts'],[str(DOC)])
    put(ap+['route_record_subsets_pending',str(DOC)],[]);put(ap+['note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5122
    for k,v in dict(reviewed_route_records=5139,completed_route_records=5139,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[229],completion_credit_added=17,final_review=str(FINAL),actual_source_event229_selected=False,actual_objects=17,actual_pages=17,offline_only_objects=0,current_candidate_emulator_runs=2,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B229_v7424'],dict(status='17-source-native-reference-representative-registered-release-pass',final_review=str(FINAL),all19_commands_A000_full_end_source944_target920_no_tail_inverse=True,original216x64_four_rows17_complete_pages=True,five_row_reasons_zero_warning_waivers_all_base_QA_preserved=True,actual17_pages67_body67_headers=True,two_contextual_progressive_names_no_assets_or_duplicate_credit=True,Samwell_full_catalogue_middle_unapproved=True,item53_staged_payload_relative132_andexact_B228_echoes_bound=True,full207_scope_open=True,all_late_differences_andcomparison_limits_preserved=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False);current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    put(['lil_B229_review_pending_v7412','registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior=old['unfinished_editorial_scope_v7412'];assert sha(Path(prior['path']).read_bytes())==prior['sha256'];inventory=deepcopy(read(prior['path']));inventory['next_focus']=NEXT
    inventory['Lil_B229_completed_v7424']=dict(final_review=str(FINAL),completed_objects=17,registered_candidate=release['candidate'],actual_speeches=17,actual_pages=17,source_event229_requires228_natural_activation_location_earned_progress_full_effects_unproved=True,two_contextual_progressive_names_no_assets_or_duplicate_credit=True,Samwell_full_catalogue_middle_unapproved=True,item53_staged_storage_andexact_B228_callback_review_bound=True,all_late_differences_andearlier_full_objective_leads_preserved=True)
    inventory['Lil_B229_pending_v7412']['registered_integration_completed_by']=dict(final_review=str(FINAL),registered_candidate=release['candidate'],all_historical_pending_flags_preserved_as_superseded_history=True,new_credit_here=0)
    inventory['next_Lil_B230_source_only_gloss_complete']=dict(source_context=str(nextsource),source_context_sha256=sha(nextsource.read_bytes()),clean_speeches=17,all17_clean_glosses_precede_old_English=True,reported_phoenix_iron_flame_forged_helmet_anduncertain_name_preserved=True,anticipatory_pitch_joke_loose_Africa_India_callback_better_clue_effort_andpraise_preserved=True,stronger_determined_find_vow_not_prior_luck_condition=True,names_voices_entry_item_place_wording_A000_current_prose_native_actual_andrelease_pending=True,new_credit=0)
    # Preserve all earlier B225/B226 technical audit leads from the full prior inventory.
    inventory['later_B229_measurement_andmetadata_technical_reaudit_v7424']=dict(actual=doc['actual_English_proof'],later=doc['later_scope_proof'],ten_command_three_duration_88of151_RGB_calendar_PRNG_components_actor_differences_andfinal_water_exhaustion_contrast_preserved=True,item53_staged_relative_offset_andsourceview_console_Item50_label_preserved=True,all_preflight_failures_successors_malformed_callback_fixture_andverified225_case_reuse_preserved=True,no_broad_simulation_orcausal_claim=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5139,completed_route_records=5139,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B22917_previously_uncredited_objects_completed=True,full207_name_role_alias_and_retrospective_wrapping_scope_preserved=True,all_prior_unresolved_leads_and_completed_name_history_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,broader_four_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,all_B218_B222_B223_B224_B225_B226_B227_B228_andB229_technical_leads_preserved=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=17,new_completed_records=17,revised=6,retained=11,goal_turn_classification='progress',new_current_candidate_emulator_runs=2,new_current_candidate_frames=21402,prior_source_and_final_English_content_runs_reused_without_replay=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7424: B229 integrated in cumulative V7418; full editorial goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7424; V7418 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all17_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;17 disjoint objects,six revisions/eleven retentions. Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_nested_record_and_counter=True,all_six_before_and_planned_hashes_verified=True,exactly17_disjoint_new_objects=True,full_goal_complete=False));print('Six targets inverse-audited;every prior root,nested record andhistory value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited cumulative completion targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_recover_exactly=True,exactly17_new_disjoint_source_prose_and_completed_records=True,completed=6739,source_prose=6742,revised=4211,retained=2528,SC2=4853,SC3=96,reviewed_routes=5139,completed_routes=5139,all622_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_B229_speeches=17,actual_B229_pages=17,actual_body_holds=67,actual_name_holds=67,offline_only_B229_objects=[],startup31_frames_and_five_actor_controls_match_V7371=True,source229_requires228_natural_eligibility_location_activation_earned_completion_full_effects_not_claimed=True,two_contextual_progressive_names_no_assets_or_duplicate_credit_Samwell_catalogue_unapproved=True,full207_review_open=True,five_row_reasons_zero_warning_waivers_all_original_QA_preserved=True,all17_single_original_four_row_pages_no_authored_layout=True,no_global_QA_font_viewport_pairphase_guard_or_literal_I_change=True,all_measured_late_differences_preserved=True,no_broad_simulation_equivalence_or_causal_claim=True,full_four_storyline_editorial_names_retrospective_wrap_and_all_prior_leads_active=True,current_native_input='work/analysis/current_V7418_native_v7423/current_native_input.json',current_native_input_sha256=sha(Path('work/analysis/current_V7418_native_v7423/current_native_input.json').read_bytes()),main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7424 verified:V7418 cumulative,6739 completed/6742 source-prose.17 B229 objects counted once;full goal active.')
