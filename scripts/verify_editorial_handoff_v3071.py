"""Independent completed145/source/native/registered-release/startup audit."""
from pathlib import Path
from collections import Counter
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import lil_christina_mivor_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3071')
CHECKPOINT=Path('work/analysis/lil_Christina_Mivor_completion_v3070')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read('work/analysis/editorial_handoff_verification_v3058/verified_handoff.json');assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows};assert len(selected)==len(rows)==145
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':130,'retain-wording':15}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    keys={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};priorcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==completed==priorcompleted|selected and not priorcompleted&selected
    assert keys=={historical_key(r) for r in oldfresh['record_keys']} and len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==3791
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3791,3791,0)
    assert Counter(path for path,key in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':1964,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3791,2642,1149)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==3794
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values()) and not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for key in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:assert ledger[key]==before[key],key
    candidate=ledger['current_integrated_candidate'];rompath=Path(candidate['path']);image=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds')
    release=read('work/analysis/lil_Christina_Mivor_release_v3067/registered_release_verification.json')
    assert sha(rompath.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==rompath.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3066' and len(manifest['batches'])==508 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_Christina_Mivor_registration_v3065d/registration_receipt.json')['builder_sha256']
    parent=NdsImage.open(before['current_integrated_candidate']['path']);base=NdsImage.open(manifest['base_rom']);result=owned.apply_release(parent,base)
    assert parent.read_file('/data/SC2.DK4')==image.read_file('/data/SC2.DK4') and result==release['stage']
    assert release['file_changes']==['/data/SC2.DK4'] and release['component_changes']==[] and release['all508_manifest_batches_and114_accepted_layers_present']
    assert sha(image.read_file('/__arm9__.bin'))==before['current_integrated_candidate']['ARM9_sha256']
    en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    mapping=read('translations/lil_christina_mivor_editorial_relocation_map_v1.json');refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==236 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==12 and sum(len(b['choice_commands']) for b in mapping['blocks'])==0
    assert mapping['all60_relocated_relative_skip_cases_preserve_original_targets'] and mapping['representative_shared_rules_approved'] and mapping['all3_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor']
    for row in rows:
        sr,cr=row['source_reference'],row['integrated_reference'];b=row['block'];value=bytes.fromhex(row['integrated_hex'])
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(row['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==value==bytes.fromhex(row['current_hex']) and row['current_reference']==cr
        if row['kind']=='typed-choice-label':
            assert value.decode('ascii')==row['english'] and en[b][cr['offset']+cr['bytes']]==0
            at=cr['command_offset'];option=row['option_index'];assert int.from_bytes(en[b][at:at+2],'little')==0x2100
            assert at+6+int.from_bytes(en[b][at+2+option*2:at+4+option*2],'little')==cr['offset']
        else:
            assert cr['record_index']==en[b][:cr['offset']].count(b'\0') and en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00')
            assert value[:1]==bytes.fromhex(row['source_hex'])[:1] and refs[row['id']]['target_hex']==row['integrated_hex']
        if row['editorial_decision']=='retain-wording':
            old=' '.join(row['historical_source_prose_predecessor_fields']['current_English'].split())
            for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            assert row['fresh_retained_wording_justification'] and row['english'].split('}',1)[-1]==old
    doc=read(final['manuscript']);font=read(doc['native_font_proof']);padding=read(doc['final_padding_proof']);sample=read(doc['representative_proof'])
    fe=read(doc['native_FE_font_proof']);assert len(fe['cases'])==3 and fe['current_original_null_actor_macro_alignment_cases']==24 and len(fe['source_FI_null_actor_cases'])==0
    assert fe['all3_source_Boy_labels_remain_visible'] and fe['all3_original_source_visible_Boy_labels_preserved']
    assert doc['source_4F_A2_A7_cross_consumer_and_missing_selector_negatives_pass']
    mivor=[r for r in rows if r['source_presentation_prefix_hex']=='4f'];assert mivor and all(r['speaker']=='Mivor Genz;current registered actor79' and r['native_display_consumer']=='original_progressive_54020' for r in mivor)
    assert len(font['cases'])==145 and font['current_original_macro_alignment_calls']==1160 and font['all145_current_native_planes_and_complete_glyphs_pass']
    assert len(font['source_bound_formatter_negatives'])==28 and len(font['source_English_macro_control_invariants'])==145 and len(font['all19_review_sheets'])==19
    assert padding['all145_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==580 and len(padding['final_target_parity_cases'])==145
    for case in padding['final_target_parity_cases']:assert case['complete_final_target_native_plane_equals_reviewed_plane'] and case['tail_padding_consumed_without_blank_page_or_lost_glyph']
    assert doc['all19_review_sheets_viewed'] and doc['formatter_phrase_flow_findings_resolved_without_waiver']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==51 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    assert sample['actual_selected_Christina_Mivor_IDs']==[] and sample['new_emulator_runs']==0 and sample['no_open_translation_specific_display_or_control_finding']
    assert sample['all3_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments'] and len(sample['relocated_predicate_cases'])==3
    assert mapping['all3_FE_source_Boy_labels_preserved']
    assert all(r['english'].split('}',1)[1].startswith('Boy: ') for r in rows if r['kind']=='system-FE')
    names=read(doc['name_identity_contract']);assert names['Mivor_full_name']=='Mivor Genz' and names['original_name_ring_scratch_restored_recovers_all4MiB']
    for p in sample['relocated_predicate_cases']:
        assert p['source_operand_and_original_predicate_result_exact'] and p['event_getter_arguments0_1_2_exact_and_caller_r3_source_cursor_mapped']
        assert p['relocated_predicate']['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['relocated_predicate']['sole_scratch_restore_recovers_all4MiB_exact']
    negative=read('work/analysis/lil_Christina_Mivor_registration_v3065d/negative_cases.json');assert len(negative['cases'])==28 and negative['all_rejected_before_mutation']
    start=read('work/analysis/lil_Christina_Mivor_startup_v3069/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V3029'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Christina_Mivor_IDs']==[] and [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    review=read(CHECKPOINT/'current_six_frame_visual_review.json');assert review['viewed'] and review['sha256']==start['review_sheet_sha256']==sha(Path(review['sheet']).read_bytes())
    inventory=read(ledger['unfinished_editorial_scope_v3070']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (unit['reviewed_route_records'],unit['completed_route_records'])==(2192,2192)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    text=Path('docs/editorial_handoff_current.md').read_text(encoding='utf8');assert text.startswith('# Current editorial handoff - V3070') and '3791 reread /3791 integrated-reconciled /zero pending' in text
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3070',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=3791,fresh_integrated=3791,fresh_pending=0,source_prose=3794,new_source_prose_reviews=0,new_completed_records=145,revisions=130,justified_retentions=15,completed_records=3791,historical_revised=2642,historical_retained=1149,incomplete_COMMON=3,incomplete_route=0,source_native_reference_representative_registered_release_and_current_startup_all_bound=True,native145panels1160macro_plus580parity_no_choices=True,all145_exact_clean_predecessor_and_integrated_references_verified=True,all19_font_FE_sheets_and_current6frame_sheet_reviewed=True,narrow_line_count_notes=51,actual_selected_Christina_Mivor_IDs=[],new_current_candidate_emulator_runs=2,paired_current_whole_framebuffers=31,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=508,accepted_layers=114,whole_clean_input_patch_reconstruction_exact=True,prior_ROMs_profiles_translation_and_V1492_promotion_preserved=True,legacy_console_count_literals_not_used_as_evidence=True,prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3070audit passes:145completed inV3066;3791reread/integrated,3794source-prose;508batches/114layers/exactpatch/current31framepairs. Fullgoalactive.')
