"""Integrate fifteen disjoint decisions with exact references and a deep six-target inverse."""
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
from scripts.lil_B224_completion_gates_v7174 import gates,RELEASE,START,VIEW,REG,PIN
from scripts.lil_B224_completion_text_v7174 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_completion_v7174');VERIFY=Path('work/analysis/editorial_handoff_verification_v7175')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7163/verified_handoff.json')
DOC=Path('translations/lil_B224_editorial_manuscript_v4.json');FINAL=Path('translations/lil_B224_contextual_final_review_v1.json')
KEY='lil_B224_completion_v7174';SCOPE='unfinished_editorial_scope_v7174';FAMILY='Lil-B224-Julian-Safia-Medusa-Shield-flirtation-whole-exchange15'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];BEFORE=(6652,6655,6655,4162,2490);AFTER=(6667,6670,6670,4172,2495)
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
    assert doc['current_ROM_sha256']==read(PRIOR)['candidate_sha256'] and Counter(r['editorial_decision'] for r in rows)=={'revise':10,'retain-wording':5} and len(panels)==15 and sum(p['native_pages'] for p in panels.values())==15
    block=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC2.DK4')).blocks[224];refs={r['id']:r for r in spec['all_object_references']};changed={r['id']:r for r in release['stage']['changed_records']}
    assert sha(block)==spec['target_block_sha256'] and len(block)==1040 and len(spec['command_map'])==18
    for row in rows:
        ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);body=value[1:]
        assert block[at:at+len(value)+1]==value+b'\0' and changed[row['id']]['new_offset']==at and block[:at].count(b'\0')==ref['new_record_index']
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'];command=next(c for c in spec['command_map'] if c['new_offset']==at-5)
        newref=dict(block=224,offset=at,bytes=len(value),record_index=ref['new_record_index'],header_offset=at-5)
        # One retained original CP932 glyph; never normalize it to three ASCII dots.
        template=body.decode('cp932');assert ' '.join(template.split())==row['english'].split('}',1)[1] and all(row['review'].values())
        if row['source_record_index']==11:assert row['source_hex']==row['current_hex']==value.hex()=='1a8163' and template=='…'
        else:assert all(c<128 for c in body)
        assert row['actual_record_observed'] and not row['native_plane_verified_not_actual_English_gameplay']
        history=['current_reference','current_hex','current_record_index','current_native_extent','current_raw_storage_English','current_effective_paragraph','current_effective_runtime_template_hex','current_expanded_runtime_hex','registered_integration_pending','source_prose_or_completion_credit_added','formatting_reason']
        row['historical_preintegration_fields']={k:deepcopy(row[k]) for k in history if k in row}
        row.update(current_reference=newref,integrated_reference=deepcopy(newref),current_hex=value.hex(),integrated_hex=value.hex(),current_record_index=newref['record_index'],current_native_extent=command['new_extent'],integrated_command_extent=command['new_extent'],current_stored_English=template,current_raw_storage_English=template,current_effective_runtime_English=template,current_effective_runtime_template_hex=body.hex(),current_expanded_runtime_hex=body.hex(),current_effective_paragraph=' '.join(template.split()),current_expanded_paragraph=' '.join(template.split()),current_registered_catalogue_match=None,completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],registered_integration_pending=False,source_prose_or_completion_credit_added=1,decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-reference-representative-and-registered-release',actual_complete_display_proof=doc['actual_English_proof'],actual_representative_scene_evidence_is_separate=True,formatting_reason='Complete original216x64/four-row native page,120 logical/compiled and60 stored alignments,all complete glyphs/guards/bounds andnine zero-ink tails verified. Five row reasons,three exact waivers andall base QA remain. All15 actual pages/59body59headers verified andviewed. Original R11 exact CP932 glyph,lighter gray andfour full source RGB holds preserved. Registered V7168,exact clean-input patch andcurrent startup pass;historical preintegration reasoning andexplicit initialized-scene/comparison limits remain.')
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in rows}
    assert len(oldkeys)==6652 and len(keys)==15 and not oldkeys&keys
    fresh=old['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==6652 and not fresh['pending_record_keys']
    summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
    paths=[DOC,RELEASE,START,VIEW,REG,PIN,PRIOR,Path(doc['reference_map']),Path(doc['reference_approval']),Path('translations/lil_B224_editorial_release_v1.json'),*[Path(doc[k]) for k in ['actual_source_proof','actual_English_proof','actual_English_view','later_scope_proof','speaker_name_review','relocated_control_proof','ellipsis_palette_proof']],Path('work/analysis/lil_B224_regressions_v7168/terminal.json'),Path('work/analysis/lil_B224_atomic_v7166/atomic_validation_receipt.json'),Path('work/analysis/current_V7168_native_v7173/current_native_input.json'),Path('work/analysis/current_V7168_native_v7173/registered_current_native_input_binding.json'),Path('scripts/lil_B224_completion_gates_v7174.py'),Path('scripts/lil_B224_completion_text_v7174.py'),Path(__file__)]
    nextsource=Path('work/analysis/lil_B225_clean_context_v7177/all13_clean_children_hero_play_and_remembrance_glosses_before_old_English.json');assert read(nextsource)['all13_clean_glosses_precede_old_English'] and read(nextsource)['prior_English_unread'];paths.append(nextsource)
    evidence={str(p):sha(p.read_bytes()) for p in paths};ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=10,retained=5,source_prose_and_completion_credit_added_once=15,previous_B224_objects_uncredited=True,all15_exact_clean_predecessor_runtime_logical_and_integrated_references_bound=True,actual_speech_objects=15,actual_native_pages=15,actual_complete_body_holds=59,actual_complete_name_holds=59,offline_only_object_IDs=[],source_event224_no_explicit_dependencies_does_not_prove_natural_activation_location_earned_progress_or_full_effects=True,two_contextual_names_no_asset_or_duplicate_credit_Basra_not_surname=True,full_catalogue_UI_unvisited_full207_review_active=True,five_row_reasons_three_exact_wrap_waivers_all_original_QA_preserved=True,retained_R11_exact_CP932_lighter_gray_and_four_full_source_RGB_holds_bound=True,all_measured_equality_within_recorded_scope_no_broad_simulation_or_causal_claim=True,evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[k]['/data/SC2.DK4']==4766;put([k,'/data/SC2.DK4'],4781)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[224],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=10,retained_count=5,fresh_revisions=10,fresh_retentions=5,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    note='6667 contextual rereads integrated;6670 source-prose. Fifteen disjoint B224 decisions counted once:10 revisions/5 justified retentions. All15 initialized actual speeches/pages,59body59headers. Two contextual name retentions add no assets or duplicate credit;Basra isnot a surname. Original CP932 ellipsis andsource palette remain. Full-editorial/207-name/retrospective-wrap objective andolder-record technical re-audit stay active.'
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=6667,fresh_pass_records_integrated=6667,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=note).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=15,final_review=str(FINAL),new_revisions=10,justified_retentions=5,new_completed_records=15,historical_reconciliation_only=False,actual_selected_source224_events=[],actual_B22_content_objects=15,actual_speeches=15,actual_pages=15,offline_only_objects=0,current_candidate_emulator_runs=2,current_candidate_frames=21402,prior_source_and_English16001_runs_reused_without_replay=True)])
    ap=['active_source_prose_drafts']
    if str(DOC) not in new[ap[0]]['manuscripts']:append(ap+['manuscripts'],[str(DOC)])
    put(ap+['route_record_subsets_pending',str(DOC)],[]);put(ap+['note'],note)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5052
    for k,v in dict(reviewed_route_records=5067,completed_route_records=5067,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',file_path='/data/SC2.DK4',blocks=[224],completion_credit_added=15,final_review=str(FINAL),actual_source_event224_selected=False,actual_objects=15,actual_pages=15,offline_only_objects=0,current_candidate_emulator_runs=2,full_goal_complete=False)])
    put(['formatting_watchlist','lil_B224_v7174'],dict(status='15-source-native-reference-representative-registered-release-pass',final_review=str(FINAL),all18_commands_A000_C200_full_end_source_tail2_full960_inverse=True,original216x64_four_rows15_complete_pages=True,five_row_reasons_three_exact_waivers_all_base_QA_preserved=True,actual15_pages59_body59_headers=True,original_R11_CP932_source_palette_four_full_RGB_holds_preserved=True,two_contextual_names_Basra_not_surname_no_duplicate_credit=True,full_catalogue_UI_and207_scope_open=True,all_comparison_limits_and_later_reaudit_leads_preserved=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False);current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)});put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    put(['lil_B224_sealed_pending_v7162','registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],new_credit_added_here=0))
    prior=old['unfinished_editorial_scope_v7162'];assert sha(Path(prior['path']).read_bytes())==prior['sha256'];inventory=deepcopy(read(prior['path']));inventory['next_focus']=NEXT
    inventory['Lil_B224_completed_v7174']=dict(final_review=str(FINAL),completed_objects=15,registered_candidate=release['candidate'],actual_speeches=15,actual_pages=15,all_earlier_pending_B224_flags_preserved_as_superseded_history=True,source_event224_natural_eligibility_location_activation_earned_progress_full_effects_unproved=True,two_contextual_names_no_asset_or_duplicate_credit_Basra_not_surname=True,source_palette_lesson_and_all_comparison_scope_preserved=True)
    inventory['next_Lil_B225_clean_gloss_complete_current_review_pending']=dict(source_context=str(nextsource),source_context_sha256=sha(nextsource.read_bytes()),all13_clean_glosses_before_old_English=True,selector97_child_label_and_original630B_consumers_require_review=True,character_historical_religious_counterfactual_not_authorial_fact=True,actual_names_entry_conditions_current_prose_native_actual_and_release_pending=True,new_credit=0)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5067,completed_route_records=5067,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B22415_previously_uncredited_objects_completed=True,full207_name_role_alias_and_retrospective_wrapping_scope_preserved=True,all_prior_unresolved_leads_and_completed_name_history_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,broader_four_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,B218_metadata217_actual218_B222_B223_differences_and_B224_source_palette_lesson_preserved=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(inv)]=sha(inv.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,record_IDs=[r['id'] for r in rows],new_source_prose_reviews=15,new_completed_records=15,revised=10,retained=5,goal_turn_classification='progress',new_current_candidate_emulator_runs=2,new_current_candidate_frames=21402,prior_source_and_English_content_runs_reused_without_replay=True,all_jobs_terminal_and_reaped=True,full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete'];f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7174: B224 integrated in cumulative V7168; full editorial goal active\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V7174; V7168 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all15_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;15 disjoint objects,10 revisions/5 retentions. Deep inverse audit next.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);release=gates()
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_nested_record_and_counter=True,all_six_before_and_planned_hashes_verified=True,exactly15_disjoint_new_objects=True,full_goal_complete=False));print('Six targets inverse-audited;every prior root,nested record andhistory value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited cumulative completion targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],profile=release['profile'],ARM9_sha256=release['ARM9_sha256'],all_original_root_and_nested_history_recover_exactly=True,exactly15_new_disjoint_source_prose_and_completed_records=True,completed=6667,source_prose=6670,revised=4172,retained=2495,SC2=4781,SC3=96,reviewed_routes=5067,completed_routes=5067,all617_manifest_batches114_accepted18_checks_and110_regressions_verified=True,actual_B224_speeches=15,actual_B224_pages=15,actual_body_holds=59,actual_name_holds=59,offline_only_B224_objects=[],startup31_frames_and_five_actor_controls_match_V7118=True,source224_natural_eligibility_location_activation_earned_progress_full_effects_not_claimed=True,two_contextual_name_retentions_no_asset_or_duplicate_credit_Basra_not_surname=True,full_catalogue_UI_and_full207_name_review_open=True,five_row_reasons_three_exact_soft_wrap_waivers_all_original_QA_preserved=True,retained_original_CP932_ellipsis_lighter_gray_four_full_source_RGB_holds=True,no_global_QA_font_viewport_pairphase_guard_or_literal_I_change=True,all_measured_equality_scopes_and_earlier_differences_preserved=True,no_broad_simulation_equivalence_or_causal_claim=True,full_four_storyline_editorial_names_retrospective_wrap_and_all_prior_leads_active=True,current_native_input='work/analysis/current_V7168_native_v7173/current_native_input.json',current_native_input_sha256=sha(Path('work/analysis/current_V7168_native_v7173/current_native_input.json').read_bytes()),main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V7174 verified:V7168 cumulative,6667 completed/6670 source-prose.15 B224 objects counted once;full goal active.')
