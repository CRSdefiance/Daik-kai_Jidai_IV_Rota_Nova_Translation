"""Independently audit the reference-ready B167 handoff without re-executing completed probes."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v4156')
CHECKPOINT=Path('work/analysis/lil_B167_checkpoint_v4155')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read(CHECKPOINT/'checkpoint_receipt.json')
    for p,h in {**receipt['evidence'],**receipt['updated_files'],**receipt['preserved_release_files']}.items():assert sha(Path(p).read_bytes())==h,p
    assert sha(Path(receipt['staged_checkpoint']).read_bytes())==receipt['staged_checkpoint_sha256']
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/(lp.name+'.before'))
    prior=read(receipt['prior_verified_handoff']);assert sha((CHECKPOINT/(lp.name+'.before')).read_bytes())==prior['ledger_sha256']
    assert {k:v for k,v in before.items() if k!='latest_checkpoint'}=={k:v for k,v in ledger.items() if k not in ['latest_checkpoint','lil_B167_references_ready_v4155']}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5602,5573,29)
    keys,integrated,pending=[{historical_key(r) for r in fresh[k]} for k in ['record_keys','integrated_record_keys','pending_record_keys']]
    assert len(keys)==len(fresh['record_keys'])==5602 and len(integrated)==5573 and len(pending)==29 and keys==integrated|pending and not integrated&pending
    assert (ledger['records_with_source_and_prose_pass'],ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5605,3749,5573,3551,2022)
    ready=ledger['lil_B167_references_ready_v4155'];approval=read('work/analysis/lil_B167_reference_approval_v4154/approval_receipt.json')
    assert approval['manuscripts']==ready['approved_manuscripts'] and approval['all29_source_native_reference_and_representative_rules_approved']
    docs=[read(p) for p in approval['manuscripts']];rows=[r for d in docs for r in d['records']]
    assert len(rows)==29 and {historical_key(r) for r in rows}==pending and all(all(r['review'].values()) for r in rows)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':13}
    for d in docs:
        old=read(d['previous_manuscript']);assert sha(Path(d['previous_manuscript']).read_bytes())==d['previous_manuscript_sha256']
        assert [r['english'] for r in d['records']]==[r['english'] for r in old['records']]
        for p,h in approval['manuscripts'].items():assert sha(Path(p).read_bytes())==h
        for k in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','native_choice_proof','native_font_proof','source_nameplate_consumer_proof']:assert sha(Path(d[k]).read_bytes())==d[k+'_sha256']
    mapping=read(approval['reference_map']);assert sha(Path(approval['reference_map']).read_bytes())==approval['reference_map_sha256']
    for p,h in mapping['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    spec=mapping['blocks'][0];assert len(mapping['blocks'])==1 and spec['block']==167
    assert (len(spec['text_records']),len(spec['command_map']),len(spec['relative_skip_fixups']),len(spec['target_native_skip_cases']))==(27,46,12,60)
    assert [r['source_offset'] for r in spec['original_declared_end_word_maps']]==[430,2172]
    assert spec['inverse_restoration_recovers_every_original_logical_byte'] and spec['external_references_complete']
    d=next(d for d in docs if len(d['records'])==27);parent=NdsImage.open(d['current_ROM']);target=Path(spec['research_block']).read_bytes()
    assert sha(target)==spec['target_block_sha256'] and len(target)==2052 and len(IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks[167])==2176
    byid={r['id']:r for r in d['records']}
    for r in spec['text_records']:
        row=byid[r['id']];at=r['new_offset'];value=bytes.fromhex(r['target_hex'])
        assert target[at:at+len(value)]==value and target[at+len(value)]==0 and value[0]==row['source_selector']
        assert target[at-5:at+1].hex()==row['source_complete_preamble_hex']
    controls=read(mapping['relocated_control_proof']);assert len(controls['relocated_dispatch_cases'])==27 and len(controls['relocated_predicate_pairs'])==2
    assert len(controls['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==6 and len(controls['relocated_choice_getter_phases'])==2
    assert all(r['current_source_case']['native_result']==r['relocated_case']['native_result'] for r in controls['relocated_predicate_pairs'])
    actual=read('work/analysis/lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns.json')
    visual=read('work/analysis/lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review.json')
    assert visual['actual_proof_sha256']==sha(Path(visual['actual_proof']).read_bytes())
    assert (actual['fresh_actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_matching_observations'])==(25,28,28)
    assert not actual['failures'] and actual['offline_only_display_IDs']==['DK4_MES_B167_R0045','DK4_MES_B167_R0131']
    assert len(actual['versions'])==4 and actual['both_versions_visible_highlight_matches_returned_option_and_unselected_never_highlighted']
    assert visual['final_type0_second_word_is_later_membership_result_not_forced_menu_index'] and len(visual['paired_source_English_whole_RGB_returns'])==2
    assert len(visual['all5_actual_sheets_viewed'])==5 and len(visual['English_full_screen_views'])==8 and len(visual['Japanese_full_screen_views'])==3
    for s in visual['all5_actual_sheets_viewed']+visual['English_full_screen_views']+visual['Japanese_full_screen_views']:assert s['review'].startswith('Viewed') and sha(Path(s['path']).read_bytes())==s['sha256']
    for v in actual['versions']:
        report=read(v['capture_report']);trace=read(v['observer_report'])
        assert report['frames']==14401 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert v['actual_unforced_Cesare_predicate']['result_words']==[2,0] and v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert v['source_end_offset']==(2172 if v['option_index']==0 else 430)
        assert v['actual_choice_command_pair']['result_words']==[2,v['option_index']]
        run=Path('work/analysis/lil_B167_display_run_v4149_O'+str(v['option_index'])+'_'+v['case']);assert read(run/'terminal.json')['terminal']
    candidate=ledger['current_integrated_candidate'];assert sha(Path(candidate['path']).read_bytes())==candidate['sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4046'
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and ready['new_source_prose_reviews']==ready['new_completed_records']==0
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4155',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(CHECKPOINT/'checkpoint_receipt.json'),handoff_receipt_sha256=sha((CHECKPOINT/'checkpoint_receipt.json').read_bytes()),fresh_reread=5602,integrated=5573,pending=29,source_prose=5605,revised=3551,retained=2022,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=541,accepted_layers=114,all29_contextual_native_reference_and_representative_approvals_verified=True,actual25_distinct28_observations_both_choices_and_separate_returns_verified=True,two_Cesare_remarks_explicitly_offline_only=True,no_new_credit_or_registry_ROM_promotion=True,registered_B167_release_and_current_startup_pending=True,V4046_main_and_V4110_experimental_preserved=True,all_prior_completions_and_wider_scope_preserved=True,all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4155 independently verified:29 reference-ready B167 reviews,25 actual/2 offline speeches,both choices and distinct returns. Counts unchanged; registered release pending;full goal active.')
