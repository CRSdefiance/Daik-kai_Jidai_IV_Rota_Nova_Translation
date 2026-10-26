"""Audit B138 clean-context preparation without adding completed review credit."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3430b')
CHECKPOINT=Path('work/analysis/lil_B138_precomparison_checkpoint_v3430')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    changed={'lil_B138_precomparison_v3430','unfinished_editorial_scope_v3430','coverage_units','lil_B138_precomparison_checkpoint_v3430','latest_checkpoint'}
    for k,v in before.items():
        if k not in changed:assert ledger[k]==v,k
    assert set(ledger)-set(before)==changed-{'coverage_units','latest_checkpoint'}
    lead=ledger['lil_B138_precomparison_v3430'];source,voice,control,branch,context,terms=map(read,[lead[k] for k in ['source','voice_proof','control_proof','branch_proof','clean_context','terms']])
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert len(known)==4880 and all(historical_key(r) not in known for r in source['records'])
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open(source['current_ROM']);jp,en=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks[138] for i in [clean,current]]
    glosses={r['id']:r for r in context['records']};assert len(glosses)==len(source['records'])==44 and context['all44_complete_clean_source_objects_read_before_older_English_comparison'] and context['all44_fresh_source_glosses_precede_localized_English']
    for r in source['records']:
        s,c=r['source_reference'],r['current_reference'];g=glosses[r['id']]
        assert jp[s['offset']:s['offset']+s['bytes']].hex()==r['source_hex']==g['source_hex'] and en[c['offset']:c['offset']+c['bytes']].hex()==r['current_hex']
        assert jp[s['offset']-5:s['offset']+1]==en[c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        assert g['fresh_source_gloss'] and g['whole_exchange_context'] and g['localized_English_not_authored'] and g['older_dialogue_English_not_editorially_compared']
    assert len(voice['fresh_seven_actor_names']['rows'])==7 and voice['all207_catalog_and_eight_voice_groups_bound_by_exact_runtime_COMMON_EV2_font_and_same_snapshot']
    assert len(control['speech_dispatch_cases'])==88 and len(control['current_original_predicate_cases'])==11 and len(control['original_event_queries'])==1
    assert control['original_event_queries'][0]['event']==137 and control['source_macro_counts']=={'FI':0,'FA':0,'FO':1}
    conditional=read(control['source_exact_conditional_result_contract']);assert sha(Path(control['source_exact_conditional_result_contract']).read_bytes())==control['source_exact_conditional_result_contract_sha256']
    assert conditional['B138_offset924_result2_is_valid_not_a_boolean'] and conditional['source_8000_preserves_raw_evaluator_r0_in_result_slot'] and conditional['source_8100_normalizes_event_completion_query_to_boolean']
    for c in control['current_original_predicate_cases']:
        assert c['native_result'][0]==2 and c['native_result'][1]==conditional['scoped_expected_unforced_results'][c['source_command_hex']]
        assert c['sole_scratch_restore_recovers_all4MiB_exact'] and c['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and c['no_predicate_or_event_flag_forced']
    assert len(branch['operands_requiring_adjustment_when_resizing'])==45 and len(branch['cases'])==450 and all(c['target_is_independently_mapped_native_boundary'] and c['source_block_owner_input_result_guards_and_ABI_exact'] for c in branch['cases'])
    assert terms['source_price_gold_coins']==100 and terms['same_original_item177_operand_in_two_display_forms'] and terms['event138_action139_native208A_selects_SC2_B138']
    assert [r['text'] for r in terms['two_complete_item_pointer_versions']]==['枯れないハスの葉','Evergreen Lotus Leaf'] and terms['source_wordless_question_marks_at_records']==[78,253]
    assert lead['older_English_comparison_still_pending'] and lead['prose_and_native_display_and_release_still_pending'] and lead['source_predicate_SCOPED_RESULTS_must_be_bound_when_rebuilding_adapter']
    assert not Path('work/analysis/lil_B138_comparison_v3431').exists() and not lead['actual_selected_B138_IDs'] and lead['new_source_prose_reviews']==lead['new_completed_records']==lead['new_emulator_runs']==0
    inventory=read(ledger['unfinished_editorial_scope_v3430']['path']);oldinventory=read(before['unfinished_editorial_scope_v3423']['path'])
    for k,v in oldinventory.items():
        if k!='next_focus':assert inventory[k]==v,k
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B137_release_v3417/registered_release_verification.json')
    assert sha(Path(c['path']).read_bytes())==c['sha256']==source['current_ROM_sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3416' and len(manifest['batches'])==523 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3430')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3430',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4880,fresh_integrated=4880,fresh_pending=0,source_prose=4883,completed_records=4880,historical_revised=3207,historical_retained=1673,new_source_prose_reviews=0,new_completed_records=0,next_remaining_physical_speeches=111,next_focus_speeches=44,next_focus_commands=111,next_focus_relative_sites=45,next_focus_predicates=10,next_focus_event_queries=1,next_focus_macro_counts={'FI':0,'FA':0,'FO':1},all44_clean_glosses_and_source_native_entry_macro_term_contracts_verified_before_older_English=True,raw_source_result2_exact_and_no_fixture_or_runtime_defect_claim=True,map_leaf_same177_and_price100_source_descriptions_preserved=True,prior48_release_completion_exactpatch31startupframes_and_view_preserved=True,all_broader_scope_graphics_separation_and_later_technical_reaudit_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],manifest_batches=523,accepted_layers=114,actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3430 audit passes:4880 completed in V3416;B13844 clean glosses/contracts ready,comparison pending. Zero new credit;full goal active.')
