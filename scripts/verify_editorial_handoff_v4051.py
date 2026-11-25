"""Independently verify B165 references, counts, release and honest representative coverage."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v4051')
CHECKPOINT=Path('work/analysis/lil_B165_completion_v4050')
OFFLINE={'DK4_MES_B165_R0020'}
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/(lp.name+'.before'))
    for p,digest in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==digest,p
    for p,digest in receipt['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];allrows=[r for g in ledger['completed_editorial_families'] for r in g['records']];keys={historical_key(r) for r in allrows}
    assert len(allrows)==len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==5529
    assert keys=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5529,5529,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[]
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5532,5532,5529,3527,2002)
    def decision(r):
        v=r.get('historical_editorial_decision') or r.get('decision') or r.get('editorial_decision');assert isinstance(v,str) and v.startswith(('revis','retain'));return 'revise' if v.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in allrows)=={'revise':3527,'retain':2002}
    assert dict(Counter(historical_key(r)[0] for r in allrows))==ledger['completed_editorial_record_counts_by_file']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families'] and ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5532 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3676 and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    family=ledger['completed_editorial_families'][-1];final=read(family['final_review'])
    assert family['id']=='Lil-B165-Julio-argument-active-navigator-recruitment24' and family['records']==final['records'] and len(final['records'])==24
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':14,'retain-wording':10}
    release=read('work/analysis/lil_B165_release_v4047/registered_release_verification.json');candidate=ledger['current_integrated_candidate']
    rom,old,clean=[NdsImage.open(p) for p in [candidate['path'],'out/all_routes_combined_v4002_candidate.nds','work/clean.nds']]
    blocks,oldblocks,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [rom,old,clean]]
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert [n for n,(a,b) in enumerate(zip(oldblocks,blocks,strict=True)) if a!=b]==[165] and (len(oldblocks[165]),len(blocks[165]))==(1544,1512)
    assert [p for _,p,v in old.iter_files() if rom.read_file(p)!=v]==['/data/SC2.DK4'] and all(rom.read_file(p)==v for p,v in old.iter_components())
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v4046' and len(manifest['batches'])==539 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    conf=read('translations/lil_B165_editorial_release_v1.json')
    for p,digest in conf['dependencies'].items():assert sha(Path(p).read_bytes())==digest,p
    doc=read(final['manuscript']);mapping=read(doc['reference_map']);stored=read(doc['final_padding_proof']);glossdoc=read(doc['whole_exchange_context_notes']);gloss={r['id']:r for r in glossdoc['records']}
    expanded={r['id']:r['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'] for r in stored['final_target_parity_cases']}
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']};sample=read(doc['representative_proof']);sampled=set(sample['actual_sampled_display_IDs'])
    assert len(sampled)==23 and set(sample['offline_only_display_IDs'])==OFFLINE and sampled|OFFLINE==set(refs) and not sampled&OFFLINE
    for r in final['records']:
        assert r['kind']=='progressive' and r['block']==165 and all(r['review'].values()) and r['fresh_source_gloss']==r['source_meaning']==gloss[r['id']]['fresh_source_gloss']
        assert r['whole_exchange_context']==gloss[r['id']]['whole_exchange_context'] and r['full_clean_context_precedes_comparison']
        at=r['source_reference']['offset'];value=bytes.fromhex(r['source_hex']);assert jp[165][at:at+len(value)]==value and jp[165][at+len(value)]==0
        ref=r['integrated_reference'];at=ref['offset'];value=bytes.fromhex(r['integrated_hex'])
        assert blocks[165][at:at+len(value)]==value and blocks[165][at+len(value)]==0 and r['current_hex']==r['integrated_hex'] and r['current_reference']==ref
        assert r['record_index']==blocks[165][:at].count(b'\0')==refs[r['id']]['new_record_index']
        pred=r['historical_source_prose_predecessor_fields'];pa=pred['current_reference']['offset'];pv=bytes.fromhex(pred['current_hex']);assert oldblocks[165][pa:pa+len(pv)]==pv and oldblocks[165][pa+len(pv)]==0
        assert jp[165][r['source_reference']['offset']-5:r['source_reference']['offset']+1].hex()==r['source_complete_preamble_hex']==blocks[165][at-5:at+1].hex()
        assert refs[r['id']]['new_offset']==at and value[0]==r['source_selector'] in [2,6,9]
        assert bytes.fromhex(expanded[r['id']]).decode('ascii')==r['current_effective_runtime_English']
        assert all(bytes.fromhex(r['source_hex']).count(m.encode())==r['english'].count('{MACRO:'+m+'}') for m in ['FI','FA','FO'])
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==r['effective_predecessor_macro_paragraph']==r['effective_predecessor_paragraph']
        assert r['actual_B22_display_fixture_observed']==(r['id'] in sampled) and r['offline_only_complete_native_display_verified']==(r['id'] in OFFLINE)
        assert r['actual_display_or_byte_identical_reuse_claim']==(r['id'] in sampled) and not r['actual_source_event165_selected'] and r['individual_actual_source_event_activation_not_claimed']
        assert not r['registered_integration_pending'] and not r['current_complete_native_display_pending']
    assert sum(bytes.fromhex(r['source_hex']).count(b'FI') for r in final['records'])==3 and stored['current_final_stored_macro_alignment_cases']==96
    names=read(doc['source_nameplate_consumer_proof']);assert names['source_current_progressive_nameplate']==names['current_full_catalogue_name']=='Julio Erneco' and names['later_older_record0D_reaudit_stays_open']
    controls=read(doc['relocated_control_proof']);assert len(controls['relocated_dispatch_cases'])==24 and len(controls['relocated_predicate_pairs'])==5 and len(controls['all12_source_current_target_nonrelative_nonspeech_leaves'])==12
    assert all(r['resolved_actor_ID']==r['source_selector'] for r in controls['relocated_dispatch_cases'])
    b=mapping['blocks'][0];assert len(b['command_map'])==56 and len(b['relative_skip_fixups'])==20 and len(b['target_native_skip_cases'])==100
    assert [e['source_offset'] for e in b['original_declared_end_word_maps']]==[1540] and not b['choice_commands'] and not b['actor_style_commands'] and not b['original2000_pause_and_resume_maps']
    ends=read(doc['termination_decode_proof']);assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and ends['no_end_decode_zero_tail_dependency']
    actual=read('work/analysis/lil_B165_actual_v4041/actual23_panels_five_unforced_Camille_queries_FI3_and_one_offline_alternative.json')
    assert not actual['failures'] and actual['fresh_actual_unique_speech_panels']==actual['complete_matching_fresh_panels']==23 and actual['offline_only_panel_count']==1 and actual['actual_new_cold_boot_runs']==2
    assert {r['id'] for r in actual['actual_panels']}==sampled and actual['actual_FI3_default_name_expansions_verified_by_complete_native_masks'] and actual['all5_original_membership_queries20_relative_commands_retained_not_flattened']
    assert sample['actual23_panels58_commands_FI3_five_queries_and_normal_return_pass'] and sample['source_solo_alternative_not_actual_or_byte_identical_reuse'] and not sample['offline_only_display_cases'][0]['actual_display_or_byte_identical_reuse_claim']
    transition=read('work/analysis/lil_B165_transition_review_v4042/source_full_figure_FI_aside_town_return_and_four_sheets_review.json')
    assert len(transition['all4_actual_sheets_viewed'])==4 and len(transition['English_full_screen_views'])==8 and len(transition['Japanese_full_screen_views'])==3
    assert transition['actual_Julio06_nameplate_portrait_full_figure_and_full_spoken_name_observed'] and transition['actual_three_FI_expansions_and_parenthesized_thought_observed'] and transition['source_R20_solo_alternative_only_offline_native_not_byte_identical_actual_reuse']
    for s in transition['all4_actual_sheets_viewed']+transition['English_full_screen_views']+transition['Japanese_full_screen_views']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    startup=read('work/analysis/lil_B165_startup_v4049/cold_boot_Lil_startup_town_verification.json');view=read('work/analysis/lil_B165_startup_v4049/current_six_frame_visual_review.json')
    assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31 and startup['all_current_requested_and_final_framebuffers_equal_V4002'] and startup['all_five_postload_actor_model_and_captain_checks_equal'] and startup['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==sha(Path(view['sheet']).read_bytes())
    registration=read('work/analysis/lil_B165_registration_v4045/registration_receipt.json');negative=read(registration['negative_cases'])
    assert registration['negative_count']==len(negative['cases'])==63 and registration['all_negatives_reject_before_mutation'] and all(r['rejected'] for r in negative['cases'])
    units={u['id']:u for u in ledger['coverage_units']};assert units['all-route-scenes']['reviewed_route_records']==units['all-route-scenes']['completed_route_records']==3930
    assert units[family['id']]['new_emulator_runs']==4 and set(units[family['id']]['actual_sampled_B22_display_IDs'])==sampled and set(units[family['id']]['offline_only_display_IDs'])==OFFLINE
    assert all(not ids for ids in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values()) and not ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']
    for k in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784']:assert ledger[k]==before[k],k
    scope=ledger['unfinished_editorial_scope_v4050'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0 and scope['other390_physical_B166_B180_not_fully_read_or_gloss_approved'] and scope['two_choice_command_leads_uncredited'] and scope['canonical_Maria32_pending_uncredited']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4050')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4050',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_reread=5529,integrated=5529,pending=0,source_prose=5532,revised=3527,retained=2002,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=539,accepted_layers=114,all24_clean_predecessor_integrated_references_and_retentions_verified=True,all56_commands20_spans100_skips96_stored_cases_five_predicates12_leaves_one_effect_one_end_and_name_consumers_bound=True,actual_two_disclosed_B22_fixtures23_panels58_commands_FI3_and_transitions_verified=True,offline_only_display_IDs=sorted(OFFLINE),no_false_actual_or_byte_identical_reuse_credit=True,actual_registered_opening_town_coldboots31_frame_pairs_verified=True,no_natural_event_eligibility_full_route_or_hardware_claim=True,all_prior_completions_and_wider_scope_preserved=True,other390_physical_B166_B180_and_two_choice_command_leads_uncredited=True,not_full_Lil_or_project_completion=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4050 independently verified:5529/5529/0;5532 source/prose;539 batches/114 layers;clean patch,23actual/1offline andstartup evidence pass. Full goal active.')
