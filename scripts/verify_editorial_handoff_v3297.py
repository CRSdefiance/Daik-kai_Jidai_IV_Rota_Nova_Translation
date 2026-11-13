"""Independent audit of ready159 and unchanged V3251/count/broader scope."""
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3297')
CHECKPOINT=Path('work/analysis/lil_B122_B127_ready_checkpoint_v3296')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    for k in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','native_source_universe_inventory_v2701c','lil_B122_B127_scope_reconciliation_v3286','Proof_terminology_consistency_lead_v3286']:assert ledger[k]==before[k],k
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','record_IDs','integrated_record_keys','pending_record_keys','fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release']:assert fresh[k]==old[k]
    keys={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']}
    assert len(keys)==4734 and len(integrated)==4575 and len(pending)==159 and not integrated&pending and keys==integrated|pending
    doc,menu=map(read,[fresh['latest_contextual_manuscript'],fresh['latest_contextual_choice_draft']]);rows=doc['records']+menu['records']
    for d in [doc,menu]:
        validate_natural_dialogue_batch(d);previous=read(d['previous_manuscript']);assert [r['english'] for r in d['records']]==[r['english'] for r in previous['records']]
        for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','conditional_return_proof']:assert sha(Path(d[key]).read_bytes())==d[key+'_sha256']
    assert len(rows)==159 and {historical_key(r) for r in rows}==pending and Counter(r['editorial_decision'] for r in rows)=={'revise':55,'retain-wording':104}
    mapping=read(doc['reference_map']);sample=read(doc['representative_proof']);padding=read(doc['final_padding_proof']);controls=read(doc['relocated_control_proof']);branch=read(doc['conditional_return_proof'])
    for p,digest in mapping['evidence'].items():assert sha(Path(p).read_bytes())==digest
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest
    assert mapping['external_references_complete'] and mapping['representative_shared_rules_approved'] and mapping['all312_physical_nested_command_boundaries_and64_relative_sites_verified'] and mapping['all320_relocated_relative_skip_cases_preserve_original_targets']
    assert len(mapping['blocks'])==6 and sum(len(b['text_records']) for b in mapping['blocks'])==155 and sum(len(b['choice_commands']) for b in mapping['blocks'])==2 and sum(len(b['original2000_pause_and_resume_maps']) for b in mapping['blocks'])==2
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_B122_B127_IDs']==[] and sample['new_emulator_runs']==0
    assert padding['all155_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==620 and padding['all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound'] and padding['both_original_pause_resume_words_and20_decoder_cases_bound']
    assert controls['all155_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text'] and controls['all14_predicate_current_relocated_results_and_source_operands_equal'] and len(controls['relocated_dispatch_cases'])==155 and len(controls['relocated_predicate_pairs'])==14 and controls['original_event_queries']==[]
    assert branch['source_current_target_branch_endings_preserved'] and len(branch['conditional_native_paths'])==6 and len(branch['original_VM_return_cases'])==12
    inventory=read(ledger['unfinished_editorial_scope_v3296']['path']);oldinventory=read(before['unfinished_editorial_scope_v3286']['path'])
    for k in oldinventory:
        if k!='next_focus':assert inventory[k]==oldinventory[k],k
    assert inventory['incomplete_route_source_prose_count']==159 and inventory['incomplete_COMMON_count']==3 and inventory['canonical_Maria_SC3_B97_uncredited32_source_lead']['records']==32
    c=ledger['current_integrated_candidate'];manifest=read(c['manifest']);registry=read('translations/release_stack.json');assert sha(Path(c['path']).read_bytes())==c['sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256'] and manifest['profile']==c['profile']=='all-routes-unified-v3251' and len(manifest['batches'])==517 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and all(manifest['checks'].values())
    req=read(receipt['next_requirements']);assert req['expected_manifest_batches']==519 and req['parent_profile']=='all-routes-unified-v3251' and req['expected_accepted_layers']==114 and req['reference_map']==doc['reference_map']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3296')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3296',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4734,fresh_integrated=4575,fresh_pending=159,source_prose=4737,new_source_prose_reviews=0,new_completed_records=0,completed_records=4575,historical_revised=3087,historical_retained=1488,incomplete_COMMON=3,incomplete_route=159,all159_source_native_references_and_representative_rules_verified=True,both2000_pauses_two2100_menus_and_conditional_return0_verified=True,all312_commands64spans320skipcases_and_inverse_bytes_verified=True,all155_final_native_planes620_macro_cases_verified=True,prior_ledger_count_and_updated_file_chains_verified=True,broader_Proof_consistency_source00_Maria32_graphics_and_later_technical_audit_preserved=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],next_requirements=receipt['next_requirements'],expected_next_manifest_batches=519,actual_selected_B122_B127_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3296 audit passes:159 ready reviews,4734reread/4575integrated/159pending;V3251/517batches and full wider scope preserved. Registered release/startup next.')
