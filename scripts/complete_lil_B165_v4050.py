"""Complete the previously credited B165 reviews after registered release and startup checks."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B165_completion_text_v4050 import NEXT,ACTUAL_SCOPE,make_summary
ROOT=Path('work/analysis/lil_B165_completion_v4050')
FINAL=Path('translations/lil_B165_contextual_final_review_v1.json')
DOC=Path('translations/lil_B165_editorial_manuscript_v7.json')
RELEASE=Path('work/analysis/lil_B165_release_v4047/registered_release_verification.json')
START=Path('work/analysis/lil_B165_startup_v4049/cold_boot_Lil_startup_town_verification.json')
VISUAL=START.parent/'current_six_frame_visual_review.json'
ACTUAL=Path('work/analysis/lil_B165_actual_v4041/actual23_panels_five_unforced_Camille_queries_FI3_and_one_offline_alternative.json')
TRANSITIONS=Path('work/analysis/lil_B165_transition_review_v4042/source_full_figure_FI_aside_town_return_and_four_sheets_review.json')
PRIOR=Path('work/analysis/lil_B165_checkpoint_v4029/checkpoint_receipt.json')
REG=Path('work/analysis/lil_B165_registration_v4045/registration_receipt.json')
FAMILY='Lil-B165-Julio-argument-active-navigator-recruitment24'
OFFLINE={'DK4_MES_B165_R0020'}
if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    docsfiles=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    prior=read(PRIOR)
    for p in [lp,*docsfiles]:assert sha(p.read_bytes())==prior['updated_files'][str(p)]
    release,start,view,actual,reg=map(read,[RELEASE,START,VISUAL,ACTUAL,REG])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all539_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V4002'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged'] and not start['actual_selected_B165_IDs']
    assert view['viewed'] and view['sheet']==start['review_sheet'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_fresh_panels']==23 and actual['offline_only_panel_count']==1 and actual['actual_new_cold_boot_runs']==2 and not actual['failures']
    assert reg['negative_count']==63 and reg['all_negatives_reject_before_mutation']
    doc=read(DOC);mapping=read(doc['reference_map']);sample=read(doc['representative_proof']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':14,'retain-wording':10}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert set(sample['offline_only_display_IDs'])==OFFLINE and sample['source_solo_alternative_not_actual_or_byte_identical_reuse']
    assert len(sample['viewed_actual_sheets'])==4
    for sheet in sample['viewed_actual_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    image=NdsImage.open(release['candidate']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    parity={r['id']:r for r in read(doc['final_padding_proof'])['final_target_parity_cases']}
    stage={r['id']:r for r in release['stage']['changed_records']}
    sampled={r['id'] for r in actual['actual_panels']}
    assert len(sampled)==23 and sampled==set(sample['actual_sampled_display_IDs']) and sampled|OFFLINE==set(refs) and not sampled&OFFLINE
    for r in rows:
        ident=r['id'];spec=refs[ident];at=spec['new_offset'];block=blocks[165];value=bytes.fromhex(spec['target_hex']);body=value[1:]
        cases=parity[ident]['current_final_target_macro_alignment_cases']['cases'];effective=bytes.fromhex(cases[0]['output_hex'])
        assert len(cases)==4 and all(bytes.fromhex(c['output_hex'])==effective for c in cases)
        expanded=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'ArgotCo')
        assert effective==expanded and stage[ident]['new_offset']==at and block[at:at+len(value)]==value and block[at+len(value)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and value[0]==r['source_selector']
        fields=['current_reference','current_hex','current_English','current_record_index','record_index','current_raw_storage_English','current_effective_runtime_English','current_effective_macro_template_hex','current_effective_macro_template_English','current_effective_paragraph','registered_runtime_catalog_entry']
        r['historical_source_prose_predecessor_fields']={k:deepcopy(r[k]) for k in fields if k in r}
        ref=dict(block=165,offset=at,bytes=len(value),record_index=block[:at].count(b'\0'),header_offset=at-5)
        assert ref['record_index']==spec['new_record_index']
        paragraph=r['english'].split('}',1)[1]
        r.update(current_reference=ref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=ref,integrated_hex=value.hex(),current_record_index=ref['record_index'],record_index=ref['record_index'],completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),current_effective_runtime_English=effective.decode('ascii'),current_effective_macro_template_hex=body.hex(),current_effective_macro_template_English=body.decode('ascii'),current_effective_paragraph=paragraph,registered_runtime_catalog_entry=None,effective_predecessor_macro_paragraph=r['effective_predecessor_paragraph'],historical_editorial_decision=r['editorial_decision'],actual_B22_display_fixture_observed=ident in sampled,offline_only_complete_native_display_verified=ident in OFFLINE,actual_display_or_byte_identical_reuse_claim=ident in sampled,actual_source_event165_selected=False,individual_actual_source_event_activation_not_claimed=True,current_complete_native_display_pending=False,registered_integration_pending=False,status='complete-contextual-current-native-references-representative-and-registered-release')
        if r['editorial_decision']=='retain-wording':assert paragraph==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};selected={historical_key(r) for r in rows}
    assert len(oldkeys)==5505 and len(selected)==24 and not oldkeys&selected and selected=={historical_key(r) for r in fresh['pending_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5529,5505,24)
    assert ledger['records_with_source_and_prose_pass']==5532 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3676
    assert docsfiles[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4029')
    ROOT.mkdir(parents=True)
    for p in [lp,*docsfiles]:copy2(p,ROOT/(p.name+'.before'))
    SUMMARY=make_summary(release)
    proofpaths=[DOC,RELEASE,START,VISUAL,ACTUAL,TRANSITIONS,PRIOR,REG,Path(doc['reference_map']),Path(doc['representative_proof']),Path(doc['final_padding_proof']),Path(doc['source_nameplate_consumer_proof']),Path('scripts/lil_B165_completion_text_v4050.py'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    final=dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscripts={str(DOC):sha(DOC.read_bytes())},candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=14,retained=10,source_prose_credit_already_recorded_in_V4029=True,all24_exact_source_predecessor_runtime_logical_and_integrated_references_bound=True,actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=sorted(OFFLINE),actual_verification_scope=ACTUAL_SCOPE,evidence=evidence,summary=SUMMARY,full_goal_complete=False)
    save(FINAL,final)
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[165],record_IDs=[r['id'] for r in rows],final_review=str(FINAL),records=rows,revised_count=14,retained_count=10,fresh_revisions=14,fresh_retentions=10,actual_verification_scope=ACTUAL_SCOPE))
    ledger.update(records_editorially_completed=5529,records_revised_and_integrated=3527,retained_wordings_editorially_completed=2002)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=3676
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():active['route_record_subsets_pending'][p]=[i for i in ids if ('/data/SC2.DK4',i) not in selected]
    if str(DOC) not in active['manuscripts']:active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(DOC)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',note='5529 fresh contextual rereads integrated;source/prose5532. Other390 physical B166-B180 speech leads,two choice-command leads andevery wider editorial family remain open.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=5529,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=24,final_review=str(FINAL),new_revisions=14,justified_retentions=10,new_completed_records=24,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=14,retained=10),actual_selected_B165_source_events=[],actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=sorted(OFFLINE),new_current_candidate_emulator_runs=2,new_explicit_display_fixture_runs=2))
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=3930,completed_route_records=3930,next=NEXT)
        if u['id']==FAMILY:u.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=24,final_review=str(FINAL),new_emulator_runs=4,new_current_candidate_emulator_runs=2,new_explicit_source_English_fixture_runs=2,actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=sorted(OFFLINE),full_goal_complete=False)
    ledger['formatting_watchlist']['lil_B165_v4029'].update(status='complete-through-V4050',registered_release_pending=False,final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_B165_v4050']=dict(status='all24-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,no_glyph_bounds_pagination_or_control_waivers=True,actual_selected_B165_source_events=[],actual_sampled_B22_display_IDs=sorted(sampled),offline_only_display_IDs=sorted(OFFLINE))
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False)
    for i in range(4):candidate[f'SC{i}_sha256']=release['story_hashes'][f'SC{i}']
    ledger['current_integrated_candidate']=candidate
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4029']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,next_focus=NEXT)
    inventory['lil_B165_completed_v4050']=dict(completed_targets=24,final_review=str(FINAL),registered_candidate=release['candidate'],explicit_display_fixture_count=2,actual_unique_speeches=23,offline_only_display_IDs=sorted(OFFLINE),natural_source_event_not_selected=True,source_A000_effect_not_earned=True)
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=3930,completed_route_records=3930,source_prose_pending_records=0,source_prose_pending_family=None,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4050']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,other390_physical_B166_B180_not_fully_read_or_gloss_approved=True,two_choice_command_leads_uncredited=True,later_untouched_storylines_shared_town_shop_random_help_prose_open=True,Proof_terminology_consistency_open=True,canonical_Maria32_pending_uncredited=True,full_goal_complete=False)
    ledger['lil_B165_completion_v4050']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={historical_key(r) for r in fresh['integrated_record_keys']}=={historical_key(r) for r in fresh['record_keys']} and len(keys)==5529
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==5532
    for k in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784']:assert ledger[k]==before[k],k
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families'] and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(lp,ledger)
    section='## V4050:24 Lil B165 reviews completed in V4046\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docsfiles):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V4050' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V4050',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docsfiles]},prior_checkpoint=str(PRIOR),new_source_prose_reviews=0,new_completed_records=24,revised=14,retained=10,fresh_reread=5529,fresh_integrated=5529,fresh_pending=0,source_prose=5532,completed=5529,historical_revised=3527,historical_retained=2002,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=539,accepted_layers=114,new_actual_emulator_runs=4,new_actual_fixture_runs=2,new_registered_startup_runs=2,actual_unique_speech_panels=23,offline_only_display_IDs=sorted(OFFLINE),other390_physical_B166_B180_and_two_choice_command_leads_uncredited=True,all_jobs_terminal=True,full_goal_complete=False))
    print('V4050:5529 reread/integrated,0pending;source/prose5532,3527revised/2002retained.24 B165 records complete inV4046. Full goal active.')
