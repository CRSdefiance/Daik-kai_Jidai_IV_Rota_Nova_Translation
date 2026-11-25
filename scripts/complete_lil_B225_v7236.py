"""Integrate thirteen disjoint decisions only after release gates; preserve an exact deep inverse."""
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
from scripts.lil_B225_completion_gates_v7236 import gates,RELEASE,START,VIEW,REG,PIN
from scripts.lil_B225_completion_text_v7236 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_completion_v7236');VERIFY=Path('work/analysis/editorial_handoff_verification_v7237')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7212/verified_handoff.json')
DOC=Path('translations/lil_B225_editorial_manuscript_v4.json');FINAL=Path('translations/lil_B225_contextual_final_review_v1.json')
KEY='lil_B225_completion_v7236';SCOPE='unfinished_editorial_scope_v7236';FAMILY='Lil-B225-Charles-Martel-hero-play-history-and-remembrance-whole-exchange13'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];BEFORE=(6667,6670,6670,4172,2495);AFTER=(6680,6683,6683,4180,2500)
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
    assert doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256'] and Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':5} and len(panels)==13 and sum(p['native_pages'] for p in panels.values())==14
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[225];refs={r['id']:r for r in spec['all_object_references']};changed={r['id']:r for r in release['stage']['changed_records']}
    assert sha(block)==spec['target_block_sha256'] and len(block)==1072 and len(spec['command_map'])==16
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);body=value[1:]
        assert block[at:at+len(value)+1]==value+b'\0' and changed[row['id']]['new_offset']==at and block[:at].count(b'\0')==ref['new_record_index']
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'];command=next(c for c in spec['command_map'] if c['new_offset']==at-5)
        newref=dict(block=225,offset=at,bytes=len(value),record_index=ref['new_record_index'],header_offset=at-5)
        template=body.decode('ascii');assert ' '.join(template.split())==row['english'].split('}',1)[1] and all(row['review'].values()) and row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
        history=['current_reference','current_hex','current_record_index','current_native_extent','current_raw_storage_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
        row['historical_preintegration_fields']={k:deepcopy(row[k]) for k in history if k in row}
        row.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=newref['record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(template.split()),current_expanded_paragraph=' '.join(template.split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,formatting_reason='All 14 original 216x64/four-row pages pass 104 logical/compiled and 52 stored alignment cases, including complete glyphs, guards, bounds, six zero-ink tails and R26 ordinary A pagination. R16 fills a 35-cell opening without changing words. Two informational row reasons, zero warnings/waivers and all base QA remain. All 55 complete body and 55 header holds were verified and viewed. Registered V7230, exact clean-input patch and current startup pass. Historical reasoning, four contextual name retentions and all measured late differences and initialized-scene limits remain explicit.')
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6667 and len(keys)==13 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6667 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[DOC,RELEASE,START,VIEW,REG,PIN,PRIOR,Path(doc['reference_map']),Path(doc['reference_approval']),Path('translations/lil_B225_editorial_release_v1.json'),*[Path(doc[k]) for k in ['actual_source_proof','actual_English_proof','actual_English_view','later_scope_proof','speaker_name_review','relocated_control_proof','native_policy_validation']],Path('work/analysis/lil_B225_regressions_v7230/terminal.json'),Path('work/analysis/lil_B225_atomic_v7228/atomic_validation_receipt.json'),Path('work/analysis/current_V7230_native_v7235/current_native_input.json'),Path('work/analysis/current_V7230_native_v7235/registered_current_native_input_binding.json'),Path('scripts/lil_B225_completion_gates_v7236.py'),Path('scripts/lil_B225_completion_text_v7236.py'),Path(__file__)]
    nextsource=Path('work/analysis/lil_B226_clean_context_v7239/all20_clean_Attila_armor_glosses_before_old_English.json');assert read(nextsource)['all20_clean_glosses_precede_old_English'] and read(nextsource)['prior_English_unread'];paths.append(nextsource)
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=8,retained=5,source_prose_and_completion_credit_added_once=13,previous_B225_objects_uncredited=True,all13_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=13,actual_native_pages=14,actual_complete_body_holds=55,actual_complete_name_holds=55,offline_only_object_IDs=[],source_event225_no_explicit_dependencies_does_not_prove_natural_activation_location_earned_progress_or_full_effects=True,four_contextual_progressive_names_no_assets_or_duplicate_credit=True,source_Sailor_not_recast_as_child_catalogue151_Retainer_andbroader_consumers_open=True,full_catalogue_UI_unvisited_full207_review_active=True,two_row_reasons_zero_warning_waivers_all_original_QA_preserved=True,R16_fuller35_cell_opening_R26_original_second_page_guard_andordinary_A_verified=True,all_measured_late_differences_retained_no_broad_simulation_or_causal_claim=True,evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[k]['/data/SC2.DK4']==4781;put([k,'/data/SC2.DK4'],4794)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[225],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=8,retained_count=5,fresh_revisions=8,fresh_retentions=5,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6680 contextual rereads integrated; 6683 source-prose. Thirteen disjoint B225 decisions counted once: eight revisions and five justified retentions. All 13 initialized speeches/14 pages, 55 complete body and header holds. Four contextual progressive-name retentions change no assets and receive no duplicate credit. Catalogue151 Retainer/shared151-159 consumers and the full207 name/role/alias review remain open. All measured late differences, earlier-wrap objective and older-record technical re-audit stay active.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6680,fresh_pass_records_integrated=6680,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=13,final_review=str(FINAL),new_revisions=8,justified_retentions=5,new_completed_records=13,historical_reconciliation_only=False,actual_selected_source225_events=[],actual_B22_content_objects=13,actual_speeches=13,actual_pages=14,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,prior_source_and_final_English16001_runs_reused_without_replay=True)])
    ap=['active_source_prose_drafts']
    if str(DOC) not in new[ap[0]]['manuscripts']:append(ap+['manuscripts'],[str(DOC)])
    put(ap+['route_record_subsets_pending',str(DOC)],[]);put(ap+['note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5067
    for k,v in dict(reviewed_route_records=5080,completed_route_records=5080,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[225],completion_credit_added=13,final_review=str(FINAL),actual_source_event225_selected=False,actual_objects=13,actual_pages=14,offline_only_objects=0,current_candidate_emulator_runs=2,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B225_v7236'],dict(status='13-source-native-reference-representative-registered-release-pass',final_review=str(FINAL),all16_commands_630B_A000_full_end_source_tail2_full976_inverse=True,original216x64_four_rows14_complete_pages=True,two_row_reasons_zero_warning_waivers_all_base_QA_preserved=True,actual14_pages55_body55_headers=True,R16_fuller35_R26_guarded_second_page_andordinary_A=True,four_contextual_progressive_names_no_assets_or_duplicate_credit=True,catalogue151_andfull207_scope_open=True,all_late_differences_andcomparison_limits_preserved=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False);current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    put(['lil_B225_review_pending_v7211','registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    prior=old['unfinished_editorial_scope_v7211'];assert sha(Path(prior['path']).read_bytes())==prior['sha256'];inventory=deepcopy(read(prior['path']));inventory['next_focus']=NEXT
    inventory['Lil_B225_completed_v7236']=dict(final_review=str(FINAL),completed_objects=13,registered_candidate=release['candidate'],actual_speeches=13,actual_pages=14,all_earlier_pending_B225_flags_preserved_as_superseded_history=True,source_event225_natural_eligibility_location_activation_earned_progress_full_effects_unproved=True,four_contextual_progressive_names_no_assets_or_duplicate_credit=True,catalogue151_Retainer_andshared151_159_consumer_review_open=True,all_late_differences_source_label_correction_andearlier_full_objective_leads_preserved=True)
    inventory['next_Lil_B226_source_only_gloss_complete']=dict(source_context=str(nextsource),source_context_sha256=sha(nextsource.read_bytes()),clean_speeches=20,all20_clean_glosses_precede_old_English=True,familiar_ojisan_not_kinship=True,reported_Attila_history_anduncertain_armor_rumor_not_authorial_confirmed_fact=True,actual_names_voices_consumers_conditions_current_prose_native_actual_andrelease_pending=True,new_credit=0)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5080,completed_route_records=5080,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B22513_previously_uncredited_objects_completed=True,full207_name_role_alias_and_retrospective_wrapping_scope_preserved=True,all_prior_unresolved_leads_and_completed_name_history_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,broader_four_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,all_B218_B222_B223_B224_andB225_technical_leads_preserved=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=13,new_completed_records=13,revised=8,retained=5,goal_turn_classification='progress',new_current_candidate_emulator_runs=2,new_current_candidate_frames=21402,prior_source_and_final_English_content_runs_reused_without_replay=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7236: B225 integrated in cumulative V7230; full editorial goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7236; V7230 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all13_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;13 disjoint objects,eight revisions/five retentions. Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_nested_record_and_counter=True,all_six_before_and_planned_hashes_verified=True,exactly13_disjoint_new_objects=True,full_goal_complete=False));print('Six targets inverse-audited;every prior root,nested record andhistory value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited cumulative completion targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_recover_exactly=True,exactly13_new_disjoint_source_prose_and_completed_records=True,completed=6680,source_prose=6683,revised=4180,retained=2500,SC2=4794,SC3=96,reviewed_routes=5080,completed_routes=5080,all618_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_B225_speeches=13,actual_B225_pages=14,actual_body_holds=55,actual_name_holds=55,offline_only_B225_objects=[],startup31_frames_and_five_actor_controls_match_V7168=True,source225_natural_eligibility_location_activation_earned_progress_full_effects_not_claimed=True,four_contextual_progressive_names_no_assets_or_duplicate_credit=True,catalogue151_andfull207_review_open=True,two_row_reasons_zero_warning_waivers_all_original_QA_preserved=True,R16_fuller35_R26_second_page_guard_andordinary_A=True,no_global_QA_font_viewport_pairphase_guard_or_literal_I_change=True,all_measured_late_differences_preserved=True,no_broad_simulation_equivalence_or_causal_claim=True,full_four_storyline_editorial_names_retrospective_wrap_and_all_prior_leads_active=True,current_native_input='work/analysis/current_V7230_native_v7235/current_native_input.json',current_native_input_sha256=sha(Path('work/analysis/current_V7230_native_v7235/current_native_input.json').read_bytes()),main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7236 verified:V7230 cumulative,6680 completed/6683 source-prose.13 B225 objects counted once;full goal active.')
