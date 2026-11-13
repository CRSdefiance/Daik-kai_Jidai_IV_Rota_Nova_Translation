"""Independently verify reference readiness and unchanged44 pending integrations."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3447b')
CHECKPOINT=Path('work/analysis/lil_B138_reference_checkpoint_v3447')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    changed={'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units','formatting_watchlist','lil_B138_reference_approval_v3447','unfinished_editorial_scope_v3447','latest_checkpoint'}
    assert all(ledger[k]==v for k,v in before.items() if k not in changed) and set(ledger)-set(before)=={'lil_B138_reference_approval_v3447','unfinished_editorial_scope_v3447'}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871'];doc=read(fresh['latest_contextual_manuscript']);old=read(oldfresh['latest_contextual_manuscript'])
    assert len(doc['records'])==44 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':16,'retain-wording':28}
    for a,b in zip(old['records'],doc['records'],strict=True):
        expected=deepcopy(a);expected.update(status=doc['status'],current_text_hex=a['current_hex'],native_display_consumer='original_progressive_54020');assert expected==b
    expected=deepcopy(oldfresh);expected['latest_contextual_manuscript']=fresh['latest_contextual_manuscript']
    for p in expected['pending_contextual_families']:p.update(manuscript=fresh['latest_contextual_manuscript'],manuscript_sha256=sha(Path(fresh['latest_contextual_manuscript']).read_bytes()),pending=read(receipt['next_requirements'])['next'],reference_map=doc['reference_map'])
    assert expected==fresh and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4924,4880,44)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4927
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4880,3207,1673)
    approval=read('work/analysis/lil_B138_reference_approval_v3446/approval_receipt.json')
    for p,digest in approval['hashes'].items():assert sha(Path(p).read_bytes())==digest
    mapping=read(doc['reference_map']);control=read(doc['relocated_control_proof']);padding=read(doc['final_padding_proof']);sample=read(doc['representative_proof']);font=read(doc['native_font_proof'])
    assert mapping['external_references_complete'] and mapping['entry_point_offset']==8 and mapping['preserve_record_parity']
    assert [b['block'] for b in mapping['blocks']]==[138] and sum(len(b['text_records']) for b in mapping['blocks'])==44 and sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==111
    assert sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==45 and sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==225
    assert mapping['all111_physical_nested_command_boundaries_and45_relative_sites_verified'] and mapping['all225_relocated_relative_skip_cases_preserve_original_targets']
    assert mapping['all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'] and len(mapping['original_event_queries'])==1 and mapping['original_event_queries'][0]['event']==137
    assert len(control['relocated_dispatch_cases'])==44 and len(control['relocated_predicate_pairs'])==11 and len(control['original_event_queries'])==1
    assert control['source_predicate_result_constants']['0080ffff200301a1']==2 and control['portable_source_owned_adapters']['predicate'].startswith('SCOPED_RESULTS=')
    for pair in control['relocated_predicate_pairs']:
        a,b=pair['cases'];assert a['native_result']==b['native_result'] and a['source_command_hex']==b['source_command_hex'] and all(c['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] for c in [a,b])
    assert padding['current_final_padded_macro_alignment_cases']==176 and len(padding['final_target_parity_cases'])==44
    assert padding['all44_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['all335_other_SC2_blocks_every_other_file_and_native_component_exact']
    for ident in ['DK4_MES_B138_R0078','DK4_MES_B138_R0253']:
        c=next(c for c in padding['final_target_parity_cases'] if c['id']==ident);assert c['stored_target_hex']=='023f20' and [(e['code'],e['x'],e['y']) for e in c['complete_native_glyph_events'] if e['code']!=32]==[(63,0,0)] and all(p['output_hex']=='3f20' for p in c['current_final_target_macro_alignment_cases']['cases'])
    assert len(font['cases'])==44 and font['current_original_macro_alignment_calls']==352 and len(font['source_consumer_negative_controls'])==23 and len(font['source_bound_formatter_negatives'])==14 and len(font['review_sheets'])==6
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==21 and all(all(r['review'].values()) for r in doc['records'])
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['all44_final_planes176_macros_static_dispatches10_predicates_and1_query_bound'] and sample['actual_selected_B138_IDs']==[] and sample['new_emulator_runs']==0
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest
    current=NdsImage.open(doc['current_ROM']);target=NdsImage.open(padding['research_ROM']);assert sha(Path(padding['research_ROM']).read_bytes())==padding['research_ROM_sha256']==control['research_ROM_sha256']
    assert [p for _,p,data in current.iter_files() if target.read_file(p)!=data]==['/data/SC2.DK4']
    for p,data in current.iter_components():assert target.read_file(p)==data
    a,b=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [current,target]];assert [n for n,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[138] and (len(a[138]),len(b[138]))==(2756,2356)
    inventory=read(ledger['unfinished_editorial_scope_v3447']['path']);oldinventory=read(before['unfinished_editorial_scope_v3439']['path'])
    for k,v in oldinventory.items():
        if k!='next_focus':assert inventory[k]==v,k
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==44 and ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B137_release_v3417/registered_release_verification.json')
    assert sha(Path(c['path']).read_bytes())==c['sha256']==doc['current_ROM_sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3416' and len(manifest['batches'])==523 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3447')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3447',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4924,fresh_integrated=4880,fresh_pending=44,source_prose=4927,completed_records=4880,historical_revised=3207,historical_retained=1673,new_source_prose_reviews=0,new_completed_records=0,proposed_revisions=16,justified_retentions=28,all44_source_native_reference_representative_approvals_verified=True,all111_commands45_spans225_skips10_predicates_and1_query_preserved=True,raw_result2_portable_constants_original_globals_and_two_question_glyphs_verified=True,all_old_completed_scope_graphics_separation_and_later_reaudit_preserved=True,prior_ledger_release_and_document_hash_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],manifest_batches=523,accepted_layers=114,next_expected_manifest_batches=524,actual_selected_B138_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3447 audit passes:4924 reread/4880 integrated/44 pending;source-native-reference-representative gates pass. Registered integration/exactpatch/startup next;full goal active.')
