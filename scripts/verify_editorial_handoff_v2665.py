"""Independent completion,classification,source/native/sampling and release audit."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2665')
CHECKPOINT=Path('work/analysis/admiral_shot_completion_v2664')
IDS=set(range(1924,1931))

if __name__=='__main__':
    assert not ROOT.exists()
    receiptpath=CHECKPOINT/'completion_receipt.json';receipt=read(receiptpath)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    beforepath=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(beforepath)
    audit=read('work/analysis/editorial_handoff_verification_v2661/verified_handoff.json')
    assert sha(beforepath.read_bytes())==audit['ledger_sha256']
    oldreceipt=read(audit['handoff_receipt'])
    for p,digest in oldreceipt['updated_files'].items():assert sha((CHECKPOINT/(Path(p).name+'.before')).read_bytes())==digest,p
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    oldcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==completed and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2150
    expected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS}
    assert completed-oldcompleted==expected and oldcompleted<=completed and len(oldcompleted)==2143
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2150,2150,0)
    assert {(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}==keys
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[]
    assert fresh['latest_pending_contextual_family'] is None
    assert Counter(p for p,n in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1493,'/data/SC2.DK4':429,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2150,1504,646)
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2259
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert set(ledger['reviewed_but_incomplete_COMMON_IDs'])==set(before['reviewed_but_incomplete_COMMON_IDs'])-IDS
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==109 and ledger['current_integrated_candidate']==before['current_integrated_candidate']
    assert set(ledger['active_source_prose_drafts']['native_message_IDs'])==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert all(not IDS&set(ns) for ns in ledger['active_source_prose_drafts']['manuscript_record_subsets_pending'].values())
    docpath=Path(fresh['latest_contextual_manuscript']);doc=read(docpath);validate_natural_dialogue_batch(doc)
    finalpath=Path('translations/admiral_shot_contextual_final_review_v1.json');final=read(finalpath)
    assert final['records']==doc['records'] and final['new_completed_records']==7 and final['revised_count']==0 and final['retained_count']==7
    assert final['historical_decisions_newly_completed']=={'revised':6,'retained':1}
    assert final['actual_shot_IDs']==[] and final['new_emulator_runs']==0 and final['all_review_sheets_viewed']
    assert not doc['distinct_post_shot_transition_pending'] and not doc['current_native_and_representative_transition_reconciliation_pending']
    assert Counter(r['historical_editorial_decision'] for r in doc['records'])=={'revise':6,'retain':1}
    for p,digest in final['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    rom=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds')
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    en=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for row in doc['records']:
        n=row['message_id'];assert n in IDS and all(row['review'].values()) and row['editorial_decision']=='retain-wording'
        assert row['source_meaning'] and row['localization_note'] and row['fresh_retained_wording_justification']
        assert row['source_hex']==jp[n].text.hex() and row['source_reference']==ref(jp[n]) and row['current_reference']==ref(en[n])
        assert compiled(row)==en[n].text==bytes.fromhex(row['current_hex'])==bytes.fromhex(row['integrated_hex'])
        assert row['integrated_reference']==ref(en[n]) and row['actual_holds']==[] and row['individual_actual_activation_not_claimed']
    font=read(doc['current_native_font_proof']);gate=read(doc['focused_original_gate_proof'])
    assert len(font['cases'])==7 and len(font['all8_original_role7_speech_pipelines'])==8
    assert len(font['all14_cold_warm_copies'])==len(font['invalid_compiler_inputs_rejected'])==14 and font['findings']==[]
    assert font['all_executed_pipeline_instructions_current_ROM_byte_exact'] and font['all_original_actor_models_unchanged']
    assert len(gate['exclusion_cases'])==len(gate['threshold_cases'])==3 and len(gate['post_RNG_arithmetic_cases'])==20
    for c in [*gate['exclusion_cases'],*gate['threshold_cases'],*gate['post_RNG_arithmetic_cases']]:assert c['all_main4MiB_bytes_unchanged'] and c['no_RNG_effect_speech_or_outcome_called']
    sample=read(doc['representative_reconciliation']);assert sample['actual_admiral_shot_IDs']==[] and sample['new_emulator_runs']==0
    assert sample['current_native_shot_IDs']==sorted(IDS) and sample['current_original_role7_voice_pipelines']==8
    assert sample['historical_actual_role7_ID']==2229 and sample['historical_actual_regular_outcome_ID']==2011
    assert sample['original_UI_construction_dismissal_and_return_code_exact_to_clean_and_both_representative_builds']
    assert sample['regular_capture_reward_cargo_return_reuses_original_72368_mode0'] and sample['special_B5_handler_dispatch_tested_offline_no_individual_activation_claim']
    assert sample['no_open_translation_specific_display_or_transition_finding'] and sample['companion_context_credit_added']==0
    returned=read(sample['focused_post_report_cleanup_and_regular_special_dispatch_proof'])
    assert returned['main4MiB_changes']==[dict(address=returned['original_enemy_mobile']+13,before=4,after=0)]
    assert returned['not_actual_UI_dismissal_shot_effect_chance_eligibility_or_gameplay_outcome']
    assert returned['original_cleanup_calls'][-1]['PC']==0x02072368 and returned['original_cleanup_calls'][-1]['args'][1]==0
    assert len(returned['isolated_original_regular_and_B5_dispatch_tests'])==2
    for c in returned['isolated_original_regular_and_B5_dispatch_tests']:assert c['all_main4MiB_unchanged'] and c['no_outcome_callee_executed']
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    assert sha(Path(sample['review_sheet']).read_bytes())==sample['review_sheet_sha256']
    stage=read(Path(doc['current_ROM']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['reinforcement_sniping_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript'])
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['manuscript_sha256']
    assert IDS<=set(stage['proof']['reviewed_native_IDs'])
    original={r['message_id']:r for r in read(mp)['records']}
    assert all(original[r['message_id']]['english']==r['english'] and original[r['message_id']]['editorial_decision']==r['historical_editorial_decision'] for r in doc['records'])
    release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json')
    manifestpath=Path(doc['current_ROM']).with_suffix('.manifest.json');manifest=read(manifestpath)
    assert sha(Path(doc['current_ROM']).read_bytes())==release['candidate_sha256']==receipt['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256'] and sha(manifestpath.read_bytes())==release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']==receipt['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    registry=read('translations/release_stack.json');assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    assert len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    inventory=read(ledger['unfinished_editorial_scope_v2664']['path'])
    assert inventory['incomplete_COMMON_count']==109 and sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==109
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert ledger['next_named_target_reports_source_lead_v2664']['IDs']==list(range(2187,2192))
    assert ledger['next_named_target_reports_source_lead_v2664']['source_prose_credit_added']==ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    handoff=Path('docs/editorial_handoff_current.md').read_text();assert handoff.startswith('# Current editorial handoff - V2664')
    assert '2150 reread /2150 integrated-reconciled /zero pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2664',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        fresh_records=2150,fresh_integrated=2150,fresh_pending=0,new_completed_records=7,new_current_prose_revisions=0,fresh_retentions=7,
        historical_revised=1504,historical_retained=646,source_prose=2259,incomplete_COMMON=109,
        seven_exact_clean_current_registered_owner_native_and_representative_scope_reconciliations_verified=True,
        actual_shot_IDs=[],new_emulator_runs=0,special_outcome_offline_only_and_companion5_uncredited=True,
        prior_ledger_and_updated_file_backup_chain_verified=True,handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        no_ROM_registry_profile_manifest_or_patch_change=True,prior_clean_input_reconstruction_proof_still_bound=True,
        all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V2664 audit passes:7new completions;2150fresh reconciled;109incompleteCOMMON;historical/current decision counts,source/native/sampling and unchanged release verified.')
