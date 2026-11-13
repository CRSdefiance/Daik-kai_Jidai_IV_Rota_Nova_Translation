"""Independent34-completion ledger,source/runtime/release and coverage audit."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import lil_kuhn_alliance_editorial as owned
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2888')
CHECKPOINT=Path('work/analysis/lil_Kuhn_Alliance_completion_v2887')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read('work/analysis/editorial_handoff_verification_v2875c/verified_handoff.json')
    assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows};assert len(selected)==len(rows)==82
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':63,'retain-wording':19}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};integrated={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    priorcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==completed==priorcompleted|selected and not priorcompleted&selected
    assert keys=={(r['file_path'],r['id']) for r in oldfresh['record_keys']} and len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==2753
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2753,2753,0)
    assert Counter(path for path,key in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':926,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2753,1938,815)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2756
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for key in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    candidate=ledger['current_integrated_candidate'];rompath=Path(candidate['path']);image=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds')
    release=read('work/analysis/lil_Kuhn_Alliance_release_v2884/registered_release_verification.json')
    assert sha(rompath.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==rompath.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v2883' and len(manifest['batches'])==502 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_Kuhn_Alliance_registration_v2882/registration_receipt.json')['builder_sha256']
    parent=NdsImage.open(before['current_integrated_candidate']['path']);base=NdsImage.open(manifest['base_rom'])
    assert sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    result=owned.apply_release(parent,base);assert parent.read_file('/data/SC2.DK4')==image.read_file('/data/SC2.DK4') and result==release['stage']
    assert release['file_changes']==['/data/SC2.DK4'] and release['component_changes']==[]
    assert sha(image.read_file('/__arm9__.bin'))==before['current_integrated_candidate']['ARM9_sha256']
    en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    for row in rows:
        sr,cr=row['source_reference'],row['integrated_reference'];b=row['block']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(row['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(row['integrated_hex'])==bytes.fromhex(row['current_hex'])
        assert row['current_reference']==cr and cr['record_index']==en[b][:cr['offset']].count(b'\0')
        assert en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00') and bytes.fromhex(row['integrated_hex'])[:1]==bytes.fromhex(row['source_hex'])[:1]
        if row['editorial_decision']=='retain-wording':
            old=' '.join(row['historical_source_prose_predecessor_fields']['current_English'].split())
            for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            assert row['fresh_retained_wording_justification'] and row['english'].split('}',1)[1]==old
    mapping=read('translations/lil_kuhn_alliance_editorial_relocation_map_v1.json')
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==195 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==60
    assert mapping['all300_relocated_relative_skip_cases_preserve_original_targets'] and mapping['representative_shared_rules_approved'] and mapping['all15_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor']
    manuscript=read(final['manuscript']);font=read(manuscript['native_font_proof']);padding=read(manuscript['final_padding_proof'])
    assert len(font['cases'])==len(font['all82_full_QA_reports'])==82 and font['current_original_macro_alignment_calls']==656 and font['all82_progressive_full_QA_and_complete_native_fonts_pass']
    assert padding['all82_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==328 and len(padding['final_target_parity_cases'])==82
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']};fonts={r['id']:r for r in font['cases']}
    for row in rows:
        spec=refs[row['id']];encoded=bytes.fromhex(row['compiled_hex'])
        assert spec['target_hex']==row['integrated_hex'] and bytes.fromhex(row['integrated_hex'])==encoded+(b' ' if spec['parity_space_added'] else b'') and fonts[row['id']]['encoded_hex']==row['compiled_hex']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==22 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    assert manuscript['all11_review_sheets_viewed'] and manuscript['phrase_flow_refinement_preserves_complete_source_meaning']
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'],font['newly_executed_current_macro_alignment_cases'],font['reused_current_macro_alignment_cases'])==(1,81,8,648)
    approval=read('work/analysis/lil_Kuhn_Alliance_font_approval_v2873/approval_receipt.json');assert len(approval['source_bound_formatter_negatives'])==14 and len(approval['source_English_control_macro_invariants'])==82
    source=read(manuscript['source_context']);control=read(manuscript['control_contract'])
    assert source['total_editorial_objects']==source['progressive_speeches']==82 and source['system_FE_panels']==source['typed_choice_labels']==0
    assert [(q['block'],q['event']) for q in control['original_event_queries']]==[]

    # This batch has zero original8100 queries and no selected-scene activation claim.
    sample=read(manuscript['representative_proof'])
    assert sample['actual_selected_Kuhn_Alliance_IDs']==[] and sample['new_emulator_runs']==0 and sample['no_open_translation_specific_display_or_control_finding']
    assert sample['all15_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments'] and len(sample['relocated_predicate_cases'])==15
    for p in sample['relocated_predicate_cases']:
        assert p['source_operand_and_original_predicate_result_exact'] and p['event_getter_arguments0_1_2_exact_and_caller_r3_source_cursor_mapped']
        assert p['relocated_predicate']['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['relocated_predicate']['sole_scratch_restore_recovers_all4MiB_exact']

    negative=read('work/analysis/lil_Kuhn_Alliance_registration_v2882/negative_cases.json');assert len(negative['cases'])==17 and negative['all_rejected_before_mutation']
    start=read('work/analysis/lil_Kuhn_Alliance_startup_v2886/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V2840'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['actual_selected_Kuhn_Alliance_IDs']==[]
    assert read('work/analysis/lil_Kuhn_Alliance_completion_v2887/current_six_frame_visual_review.json')['viewed']
    assert start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    for case in ['newgame','town']:assert read(Path('work/analysis/lil_Kuhn_Alliance_runs_v2885')/(case+'_terminal.json'))['terminal']
    inventory=read(ledger['unfinished_editorial_scope_v2887']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0 and inventory['incomplete_route_source_prose_groups']==[]
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert unit['reviewed_route_records']==unit['completed_route_records']==1154
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    handoff=Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8');assert handoff.startswith('# Current editorial handoff - V2887') and '2753 reread /2753 integrated-reconciled /zero pending' in handoff and 'Kuhn alliance' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2887',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        fresh_records=2753,fresh_integrated=2753,fresh_pending=0,source_prose=2756,new_completed_records=82,new_source_prose_reviews=0,revisions=63,justified_retentions=19,
        completed_records=2753,historical_revised=1938,historical_retained=815,incomplete_COMMON=3,incomplete_route=0,
        all82_clean_current_integrated_references_and_five_review_gates_verified=True,all195commands60relative_sites_and300relocated_cases_bound=True,
        current656plus328macro_cases_82font_planes_and_no_FE_or_choices_bound=True,all17negative_cases_rejected_before_mutation=True,
        historical_shared_rules_and_new_current_startup_scope_distinct=True,actual_selected_Kuhn_Alliance_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        whole_clean_input_patch_reconstruction_exact=True,all502batches114accepted_layers_previous_profiles_and_V1492_promotion_preserved=True,
        prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2887 audit passes:82completed/63revisions/19retentions;registeredV2883/502batches/exactcleanpatch/current31frame pairs.2753integrated,source-prose2756;fullgoalactive.')
