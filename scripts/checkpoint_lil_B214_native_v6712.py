"""Publish zero-credit source/prose/native/name progress with an audited inverse of all prior state."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.lil_B213_completion_gates_v6691 import gates
from scripts.lil_B214_checkpoint_text_v6712 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_native_checkpoint_v6712');VERIFY=Path('work/analysis/editorial_handoff_verification_v6713');LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v6692/verified_handoff.json')
KEY='lil_B214_native_source_checkpoint_v6712';SCOPE='unfinished_editorial_scope_v6712';COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];COUNTS=(6526,6529,6529,4080,2446)
DOC=Path('translations/lil_B214_editorial_manuscript_v1.json');NAME=Path('translations/lil_B214_speaker_name_review_v1.json');PLAN=Path('work/analysis/lil_B214_layout_v6705b/seventeen_complete_paragraph_plans_original_width_no_prose_changes.json');FONT=Path('work/analysis/lil_B214_native_pages_v6706/all17_complete_single_pages136_native_alignments.json');VIEW=Path('work/analysis/lil_B214_view_v6711/seventeen_native_pages_eleven_names_nine_source_panels_and_scope_viewed.json');NPLANES=Path('work/analysis/lil_B214_name_planes_v6710/four_actors_eight_getters_eleven_name_planes44_alignments.json');CONTROL=Path('work/analysis/lil_B214_controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models.json');ENTRY=Path('work/analysis/lil_B214_entry_v6704/source_EV2_B214_action_dependency_and_native_getter_binding.json');ACTUAL=Path('work/analysis/lil_B214_source_actual_v6709b/eight_speeches_one_selected_style_complete_source_masks30_commands_and_return.json');QA=Path('work/analysis/lil_B214_base_QA_v6707/all17_base_QA_diagnostics_before_any_scoped_classification.json');NBIND=Path('work/analysis/lil_B214_names_v6699/four_names_eight_getters_signature_mismatch_and_other_raw_occurrence_leads.json');SOURCE=Path('work/analysis/lil_B214_source_v6697/all17_clean_current_letter_notices_reactions_full1316_inverse.json');CURRENT=Path('work/analysis/lil_B214_consumers_v6698/all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json');RUN=Path('work/analysis/lil_B214_source_run_v6703/terminal.json');FIXTURE=Path('work/analysis/lil_B214_source_fixture_v6702/complete_B214_source_B22_fixture.json');PIN=Path('work/analysis/lil_B214_source_fixture_v6702/pin_receipt.json')
def validate():
    release=gates();d,n,p,f,v,np,c,e,a,q,nb,s,cu=map(read,[DOC,NAME,PLAN,FONT,VIEW,NPLANES,CONTROL,ENTRY,ACTUAL,QA,NBIND,SOURCE,CURRENT])
    assert len(d['records'])==17 and Counter(r['editorial_decision'] for r in d['records'])=={'revise':12,'retain-wording':5} and all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in d['records'])
    assert p['manuscript_sha256']==f['manuscript_sha256']==sha(DOC.read_bytes()) and f['layout_plan_sha256']==sha(PLAN.read_bytes()) and f['complete_native_pages']==17 and f['logical_compiled_input_alignment_cases']==136 and len(f['records'])==17 and all(len(r['pages'])==1 for r in f['records'])
    assert v['font_proof_sha256']==sha(FONT.read_bytes()) and v['name_proof_sha256']==sha(NPLANES.read_bytes()) and v['source_actual_proof_sha256']==sha(ACTUAL.read_bytes()) and not v['visual_review_pending'] and v['all_seven_sheets_individually_returned_and_viewed']
    for sh in v['viewed_sheets']:assert sha(Path(sh['path']).read_bytes())==sh['sha256']
    assert np['native_name_literal_alignment_cases']==44 and len(np['name_planes'])==11 and n['three_contextual_native_proper_name_retentions_approved_no_asset_change'] and len(n['records'])==3 and all(all(r['review'].values()) for r in n['records']) and n['full_catalogue_UI_unvisited'] and n['Manuel_actual_header_unvisited']
    assert len(c['predicate_cases'])==4 and all(r['native_result'][:2]==[2,0] for r in c['predicate_cases']) and len(c['normal_terminal_seed_cases'])==50 and len(c['source4500_4621_A000_structural_cases'])==10 and [len(r['speech_offsets']) for r in c['four_structural_route_models']]==[8,9,9,10]
    assert [(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in e['selected_B214_source_events']]==[(214,214,215,[87],[])]
    issues=[i for r in q['records'] for i in r['base_QA']['issues']];assert len(q['records'])==17 and not [i for i in issues if i['severity'] in ['warning','error']] and len(issues)==11 and all(i['code']=='line-break-count' for i in issues)
    assert a['actual_source_unique_speeches']==8 and a['actual_automatic_style_bodies']==1 and a['actual_complete_source_body_holds']==len(a['actual_complete_name_holds'])==29 and len(a['command_pairs'])==30 and a['stored_commands']==36 and a['native_terminal_result']==[0,0] and a['exit_frame']==5015 and a['normal_port_sample_frame']==5110 and a['unvisited_source_speech_IDs']==['DK4_MES_B214_R0062','DK4_MES_B214_R0087'] and len(a['offline_only_object_IDs'])==8 and not a['incomplete_sampled_body_holds']
    assert a['unvisited_original_command_offsets']==[894,902,966,1176,1184,1298] and a['unvisited_fixture_command_offsets']==[942,950,1014,1224,1232,1346] and v['final16001_Sea_View_with_Sailor_Dizzy_Im_starving_I_cant_go_on_notice_viewed']
    assert len(nb['other_raw_story_occurrences_for_contextual_review'])==8 and nb['current_native_progressive_and_catalogue_name']=='Janus Pasar' and nb['current_stored_signature']=='Janus Pasha' and d['Janus_signature_Pasha_corrected_to_current_native_Pasar_without_name_asset']
    assert s['all17_source_glosses_precede_old_English_comparison'] and s['blocks'][0]['all_control_headers_operands_ends_and_complete1316_byte_inverse_exact'] and len(cu['speech_and_alternative_dispatch_cases'])==34 and len(cu['whole_4100_commands'])==2 and len(cu['all207_catalog_style_pointer_cases']['cases'])==414
    assert read(RUN)['terminal'] and read(PIN)['all_prior_pins_preserved'] and d['current_ROM_sha256']==release['candidate_sha256'] and not d['full_goal_complete']
    return release
def restore(value):
    doc=deepcopy(value);entry=doc.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(doc,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return doc
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==read(PRIOR)['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==COUNTS;release=validate();ROOT.mkdir(parents=True);new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        paths=[DOC,NAME,PLAN,FONT,VIEW,NPLANES,CONTROL,ENTRY,ACTUAL,QA,NBIND,SOURCE,CURRENT,PRIOR,FIXTURE,PIN,RUN,Path('work/analysis/current_V6686_native_v6696/verified_current_context_binding.json'),Path('work/analysis/lil_B214_source_offset_fix_v6709b/source_locked_offset_coordinate_correction.json'),Path('scripts/lil_B214_checkpoint_text_v6712.py'),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
        summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        pending=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),name_review=str(NAME),name_review_sha256=sha(NAME.read_bytes()),paragraph_plan=str(PLAN),native_font_proof=str(FONT),native_name_proof=str(NPLANES),source_actual_proof=str(ACTUAL),view=str(VIEW),all17_four_prose_gates_true_formatting_false=True,proposed_revisions=12,justified_retentions=5,native17_single_pages136_alignments=True,native11_name_planes44_alignments_three_proper_name_retentions=True,source_actual8_speeches_one_style29_body29_names30_commands=True,source_unvisited_speech_IDs=read(ACTUAL)['unvisited_source_speech_IDs'],source_offline_only_object_IDs=read(ACTUAL)['offline_only_object_IDs'],source_normal_state0_value0_end5015_port5110=True,source_final16001_Sailor_starvation_notice=True,frozen_policy_negative_checks_final_stored_reference_English_actual_and_registered_release_pending=True,new_completed_records=0,new_source_prose_credit=0,full_goal_complete=False)
        put(['lil_B214_native_pending_v6712'],pending)
        nb=read(NBIND);other=[r for r in nb['other_raw_story_occurrences_for_contextual_review'] if r['term']=='Janus Pasha' and not(r['file_path']=='/data/SC2.DK4' and r['block']==214)];assert len(other)==5
        lead=dict(proof=str(NBIND),proof_sha256=sha(NBIND.read_bytes()),native_name='Janus Pasar',clean_name='ジェナス・パサー',B214_signature_draft_corrected_not_yet_integrated=True,five_other_Pasha_consumers_pending_clean_whole_exchange_review=other,no_global_substitution_or_name_asset_change=True,no_new_name_UI_or_dialogue_credit=True)
        put(['Janus_Pasar_consumer_review_lead_v6699'],lead);put(['latest_checkpoint'],summary)
        put(['formatting_watchlist','lil_B214_v6712'],dict(status='17-native-pages136-alignments-source-nine-panels-three-name-retentions-English-and-release-pending',manuscript=str(DOC),all17_formatting_gates_false=True,eleven_info_rowcount_reasons_and_scoped_boundaries_require_frozen_policy=True,source_normal_residual_value0_preserved=True,signature_Janus_Pasar_native_complete=True,new_credit=0))
        previous=old['unfinished_editorial_scope_v6691'];assert sha(Path(previous['path']).read_bytes())==previous['sha256'];inventory=deepcopy(read(previous['path']));inventory['next_focus']=NEXT;inventory['Lil_B214_native_pending_v6712']=pending;inventory['Janus_Pasar_consumer_review_lead_v6699']=lead;inventory['historical_B214_clean_pending_flags_superseded_by_v6712']=True
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':assert unit['reviewed_route_records']==unit['completed_route_records']==4926;unit['next']=NEXT
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),B21417_uncredited_objects_native_source_progress=True,five_other_Janus_Pasha_consumers_pending=True,actor151_and_item150_contextual_name_leads_open=True,initial_paired_label_review_completed_history_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,retrospective207_names_and_all_prior_unresolved_leads_open=True,broader_storylines_shared_town_shop_random_help_prose_open=True,graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');put(['coverage_units',ri,'next'],NEXT)
        new[KEY]=dict(summary=summary,next=NEXT,evidence=evidence,inverse_operations=ops,new_completed_records=0,new_source_prose_credit=0,new_emulator_runs=1,new_emulator_frames=16001,new_ROMs=1,goal_turn_classification='progress',all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V6712: B214 whole letter draft, source gameplay and native pages; Janus signature consistency\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V6712\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            staged=ROOT/f'{i:02d}.after';staged.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(staged.resolve()),planned_sha256=sha(data)))
        evidence[str(inv)]=sha(inv.read_bytes());save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,new_credit=0,no_shared_mutation_yet=True,full_goal_complete=False));print('Six checkpoint targets staged; seventeen B214 decisions remain uncredited. Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old and tuple(new[k] for k in COUNTERS)==COUNTS and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'];release=validate()
        for i,e in enumerate(plan['files']):
            assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
            if i:assert Path(e['planned']).read_bytes().endswith(gzip.decompress((ROOT/f'{i:02d}.before.gz').read_bytes()))
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),deep_inverse_recovers_every_prior_root_and_nested_value=True,all_six_before_and_planned_hashes_verified=True,all_original_document_bytes_preserved_as_suffix=True,all_counters_completed_families_and_current_release_unchanged=True,full_goal_complete=False));print('Six targets audited; all history inverse-recovers exactly, zero duplicate credit.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited B214 source/native/name checkpoint targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True);out=deepcopy(read(PRIOR))
            out.update(ledger_sha256=sha(LEDGER.read_bytes()),prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),zero_credit_native_source_checkpoint_v6712=True,B214_manuscript=str(DOC),B214_all17_four_prose_gates_true_formatting_false=True,B21417_native_single_pages136_alignments11_name_planes44_alignments=True,B214_source_actual8_speeches_one_style29_body29_name30_commands_normal0_value0_5015=True,B214_unvisited_source_speeches=['DK4_MES_B214_R0062','DK4_MES_B214_R0087'],B214_source_other_six_automatic_styles_unvisited=True,B214_three_native_proper_name_retentions_no_asset_or_duplicate_credit=True,B214_signature_draft_corrected_to_existing_Janus_Pasar=True,five_other_Janus_Pasha_consumers_pending_contextual_review=True,next_B214_all17_clean_glosses_before_old_English_pending_current_review=False,B214_policy_stored_relocation_reference_English_actual_and_release_pending=True,new_source_cold_boots=1,new_source_frames=16001,source_current_ROM_counters_and_all_completed_families_unchanged=True,all_prior_root_nested_history_inverse_preserved=True,all_sessions_terminal_and_reaped=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',out);print('V6712 verified: V6686 and6526 completed records unchanged; seventeen B214 decisions uncredited. Full editorial/name goal remains active.')
