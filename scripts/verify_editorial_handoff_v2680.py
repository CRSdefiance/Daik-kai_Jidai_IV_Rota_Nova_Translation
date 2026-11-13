"""Independent ledger/current-reference/release/startup and evidence-scope audit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2680')
CHECKPOINT=Path('work/analysis/aftermath_remaining_completion_v2679')
IDS={*range(1994,2011),*range(2022,2038),2192}

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    beforepath=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(beforepath)
    auditpath=Path('work/analysis/editorial_handoff_verification_v2671/verified_handoff.json');prior=read(auditpath)
    assert sha(beforepath.read_bytes())==prior['ledger_sha256']
    previousreceipt=read(prior['handoff_receipt'])
    for p,digest in previousreceipt['updated_files'].items():assert sha((CHECKPOINT/(Path(p).name+'.before')).read_bytes())==digest,p
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    oldcompleted={historical_key(r) for f in before['completed_editorial_families'] for r in f['records']}
    assert keys==completed and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2184
    assert {(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}==keys
    assert completed-oldcompleted=={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS} and oldcompleted<=completed
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2184,2184,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert Counter(p for p,n in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1527,'/data/SC2.DK4':429,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2184,1527,657)
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==ledger['records_with_source_and_prose_pass']==2259
    assert set(ledger['reviewed_but_incomplete_COMMON_IDs'])==set(before['reviewed_but_incomplete_COMMON_IDs'])-IDS and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==75
    assert set(ledger['active_source_prose_drafts']['native_message_IDs'])==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert all(not IDS&set(ns) for ns in ledger['active_source_prose_drafts']['manuscript_record_subsets_pending'].values())
    dp=Path(fresh['latest_contextual_manuscript']);doc=read(dp);validate_natural_dialogue_batch(doc)
    fp=Path('translations/aftermath_remaining_contextual_final_review_v1.json');final=read(fp)
    assert final['records']==doc['records'] and final['new_completed_records']==34 and final['revised_count']==1 and final['retained_count']==33
    assert final['historical_decisions_newly_completed']=={'revised':23,'retained':11}
    assert Counter(r['completed_editorial_decision'] for r in doc['records'])=={'revise':23,'retain':11}
    assert final['all_review_sheets_viewed'] and not doc['registered_revision_integration_pending'] and not doc['current_native_and_representative_reconciliation_pending']
    assert final['actual_selected34_IDs']==[] and final['current2029_actual_activation_claimed'] is False and final['current_startup_emulator_runs']==2
    for p,digest in final['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    release=read(doc['registered_release_proof']);rompath=Path(doc['current_ROM']);rom=NdsImage.open(rompath)
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');en=current_entries(common,arm)
    oldrom=NdsImage.open(before['current_integrated_candidate']['path']);old=previous_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldrom.read_file('/__arm9__.bin'))
    clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert [a.message_id for a,b in zip(old,en,strict=True) if a.text!=b.text]==[2029]
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for r in doc['records']:
        n=r['message_id'];assert n in IDS and all(r['review'].values()) and r['source_meaning'] and r['localization_note']
        assert r['source_hex']==jp[n].text.hex() and r['source_reference']==ref(jp[n])
        assert r['fresh_review_input_current_hex']==old[n].text.hex() and r['fresh_review_input_current_reference']==ref(old[n])
        assert r['current_reference']==r['integrated_reference']==ref(en[n])
        assert r['current_hex']==r['current_text_hex']==r['integrated_hex']==compiled(r).hex()==en[n].text.hex()
        assert r['current_stored_English']==en[n].text.decode('ascii') and r['current_English']==en[n].text[1:].decode('ascii')
        assert r['actual_holds']==[] and r['individual_actual_activation_not_claimed']
        if n==2029:assert r['editorial_decision']=='revise' and r['english']=='You cannot win! I suggest you surrender at once!'
        else:assert r['editorial_decision']=='retain-wording' and r['fresh_retained_wording_justification']
    manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);registry=read('translations/release_stack.json')
    assert manifest['profile']=='all-routes-unified-v2674' and len(manifest['batches'])==494 and len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256'] and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    regroot=Path('work/analysis/surrender_advice_registration_v2673');previousregistry=read(regroot/'registry_before_raw.json');restored=deepcopy(registry);restored['profiles'].pop(manifest['profile'])
    assert restored==previousregistry and sha((regroot/'registry_before_raw.json').read_bytes())==read(Path(before['current_integrated_candidate']['path']).with_suffix('.manifest.json'))['release_stack_sha256']
    builder=Path('scripts/build_integrated_release.py').read_bytes();stage=(regroot/'builder_added_optional_stage.bin').read_bytes()
    assert builder.count(stage)==1 and builder.replace(stage,b'',1)==(regroot/'builder_before.py').read_bytes()
    assert len(read(regroot/'negative_cases.json')['cases'])==8 and all(c['rejected_before_mutation'] for c in read(regroot/'negative_cases.json')['cases'])
    assert sha(rompath.read_bytes())==release['candidate_sha256']==receipt['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(arm)==release['ARM9_sha256']==doc['current_ARM9_sha256'] and sha(common)==release['COMMON_sha256']==doc['current_COMMON_sha256']
    assert sha(manifestpath.read_bytes())==release['manifest_sha256'] and release['file_changes']==['/COMMON/MESFILE.DK4'] and release['component_changes']==['/__arm9__.bin']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']==receipt['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256'] and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    current=ledger['current_integrated_candidate'];assert current['path']==str(rompath) and current['sha256']==release['candidate_sha256'] and current['ARM9_sha256']==sha(arm) and current['MESFILE_sha256']==sha(common)
    assert ledger['previous_current_integrated_candidate_before_V2674']==before['current_integrated_candidate']
    assert ledger['current_native_relocation_reference']['module']=='dk4tool.patch.surrender_advice_contextual_v1'
    font=read(doc['current_native_font_proof']);payload=read(doc['revision_payload_plan']);native=read(doc['current_released_native_proof'])
    assert len(font['cases'])==712 and len(font['complete_native_planes'])==34 and len(font['current_deployed_original_pipelines'])==34 and len(font['current_deployed_cold_warm_copies'])==68
    assert font['findings']==[] and len(payload['native_cold_warm_copies_all123_repacked_records'])==246
    assert payload['target_ARM9_sha256']==sha(arm) and payload['target_COMMON_sha256']==sha(common) and payload['unchanged_compiled_strings_and_exact_native_copies']==3667
    assert native['candidate_sha256']==release['candidate_sha256'] and native['loaded_template_hex']==en[2029].text.hex() and native['complete_native_independent_plane_and_prior_reviewed_pixels_equal']
    assert native['successor_parser_rejects_modified_COMMON'] and native['current_executed_instructions_and_actor_models_exact']
    sample=read(doc['representative_reconciliation']);assert len(sample['four_original_constructor_boundaries'])==4 and sample['all_three_entry_paths_share_original_kind0_panel'] and sample['no_open_translation_specific_display_or_control_finding']
    assert sample['actual_selected34_IDs']==[] and sample['new_emulator_runs']==0 and sample['numeric2192_constructor_proved_offline_not_individually_activated']
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    start=read(doc['current_startup_proof']);assert start['candidate_sha256']==release['candidate_sha256'] and start['all_current_requested_and_final_framebuffers_equal_V2284']
    assert [r['frames'] for r in start['runs']]==[4001,17401] and sum(len(r['paired_whole_frames']) for r in start['runs'])==30
    assert sum(len(r['postload_actor_identity_controls']) for r in start['runs'])==5 and start['source_and_disposable_town_donor_unchanged']
    for run in start['runs']:
        terminal=read(run['terminal']);assert terminal['terminal'] and sha(Path(run['terminal']).read_bytes())==run['terminal_sha256']
        report=read(run['report']);assert sha(Path(run['report']).read_bytes())==run['report_sha256'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete']
    inventory=read(ledger['unfinished_editorial_scope_v2679']['path']);assert inventory['incomplete_COMMON_count']==75
    assert sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==75 and {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0 and ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    testlog=regroot/'workflow_tests_v2680.log';assert '34 passed' in testlog.read_text()
    handoff=Path('docs/editorial_handoff_current.md').read_text();assert handoff.startswith('# Current editorial handoff - V2679')
    assert '2184 reread /2184 integrated-reconciled /zero pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2679',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        fresh_records=2184,fresh_integrated=2184,fresh_pending=0,new_completed_records=34,new_current_prose_revisions=1,fresh_retentions=33,
        historical_revised=1527,historical_retained=657,source_prose=2259,incomplete_COMMON=75,
        all34_clean_current_before_after_and_registered_representative_reconciliation_verified=True,
        actual_selected34_IDs=[],current_startup_runs=2,current_captured_whole_frames=30,
        registered_profile='all-routes-unified-v2674',registered_batches=494,accepted_layers=114,promoted_profile='all-routes-unified-v1492',
        workflow_tests=34,workflow_test_log=str(testlog),workflow_test_log_sha256=sha(testlog.read_bytes()),
        prior_ledger_updated_file_and_registry_builder_chains_verified=True,handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        candidate=str(rompath),candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        whole_clean_input_reconstruction_proof_still_bound=True,all_jobs_terminal=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V2679 audit passes:34new completions,2184fresh reconciled;registered2674/494batches,exactpatch,30current frames,34workflow tests;75incompleteCOMMON andwider objective remain open.')
