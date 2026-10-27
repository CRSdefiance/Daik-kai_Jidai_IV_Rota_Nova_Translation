"""Independent34-completion ledger,source/runtime/release and coverage audit."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import lil_india_polder_editorial as owned
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2819')
CHECKPOINT=Path('work/analysis/lil_India_Polder_completion_v2818')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read('work/analysis/editorial_handoff_verification_v2806/verified_handoff.json')
    assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows};assert len(selected)==len(rows)==119
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':84,'retain-wording':35}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};integrated={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    priorcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==completed==priorcompleted|selected and not priorcompleted&selected
    assert keys=={(r['file_path'],r['id']) for r in oldfresh['record_keys']} and len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==2581
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2581,2581,0)
    assert Counter(path for path,key in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':754,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2581,1808,773)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2584
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for key in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    candidate=ledger['current_integrated_candidate'];rompath=Path(candidate['path']);image=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds')
    release=read('work/analysis/lil_India_Polder_release_v2815/registered_release_verification.json')
    assert sha(rompath.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==rompath.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v2814' and len(manifest['batches'])==500 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_India_Polder_registration_v2813/registration_receipt.json')['builder_sha256']
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
    mapping=read('translations/lil_india_polder_editorial_relocation_map_v1.json')
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==193 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==40
    assert mapping['all200_relocated_relative_skip_cases_preserve_original_targets'] and mapping['representative_shared_rules_approved'] and mapping['all10_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor']
    manuscript=read(final['manuscript']);font=read(manuscript['native_font_proof']);padding=read(manuscript['final_padding_proof'])
    assert len(font['cases'])==len(font['all119_full_QA_reports'])==119 and font['current_original_macro_alignment_calls']==952 and font['all119_progressive_full_QA_and_complete_native_fonts_pass']
    assert padding['all119_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==476 and len(padding['final_target_parity_cases'])==119
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']};fonts={r['id']:r for r in font['cases']}
    for row in rows:
        spec=refs[row['id']];encoded=bytes.fromhex(row['compiled_hex'])
        assert spec['target_hex']==row['integrated_hex'] and bytes.fromhex(row['integrated_hex'])==encoded+(b' ' if spec['parity_space_added'] else b'') and fonts[row['id']]['encoded_hex']==row['compiled_hex']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==39 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    assert manuscript['all15_review_sheets_viewed'] and manuscript['phrase_flow_refinement_preserves_complete_source_meaning']
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'],font['newly_executed_current_macro_alignment_cases'],font['reused_current_macro_alignment_cases'])==(3,116,24,928)
    approval=read('work/analysis/lil_India_Polder_font_approval_v2804/approval_receipt.json');assert len(approval['source_bound_formatter_negatives'])==14 and len(approval['source_English_control_macro_invariants'])==119
    source=read(manuscript['source_context']);control=read(manuscript['control_contract'])
    assert source['total_editorial_objects']==source['progressive_speeches']==119 and source['system_FE_panels']==source['typed_choice_labels']==0
    assert [(q['block'],q['event']) for q in control['original_event_queries']]==[(37,129),(38,48),(38,48),(129,130),(130,26)]

    sample=read(manuscript['representative_proof'])
    assert sample['actual_selected_India_Polder_IDs']==[] and sample['new_emulator_runs']==0 and sample['no_open_translation_specific_display_or_control_finding']
    assert sample['all10_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments'] and len(sample['relocated_predicate_cases'])==10
    for p in sample['relocated_predicate_cases']:
        assert p['source_operand_and_original_predicate_result_exact'] and p['event_getter_arguments0_1_2_exact_and_caller_r3_source_cursor_mapped']
        assert p['relocated_predicate']['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['relocated_predicate']['sole_scratch_restore_recovers_all4MiB_exact']

    negative=read('work/analysis/lil_India_Polder_registration_v2813/negative_cases.json');assert len(negative['cases'])==17 and negative['all_rejected_before_mutation']
    start=read('work/analysis/lil_India_Polder_startup_v2817/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V2783'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['actual_selected_India_Polder_IDs']==[]
    assert read('work/analysis/lil_India_Polder_completion_v2818/current_six_frame_visual_review.json')['viewed']
    assert start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    for case in ['newgame','town']:assert read(Path('work/analysis/lil_India_Polder_runs_v2816')/(case+'_terminal.json'))['terminal']
    inventory=read(ledger['unfinished_editorial_scope_v2818']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0 and inventory['incomplete_route_source_prose_groups']==[]
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert unit['reviewed_route_records']==unit['completed_route_records']==982
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    handoff=Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8');assert handoff.startswith('# Current editorial handoff - V2818') and '2581 reread /2581 integrated-reconciled /zero pending' in handoff and 'India, Camille, polder and gift' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2818',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        fresh_records=2581,fresh_integrated=2581,fresh_pending=0,source_prose=2584,new_completed_records=119,new_source_prose_reviews=0,revisions=84,justified_retentions=35,
        completed_records=2581,historical_revised=1808,historical_retained=773,incomplete_COMMON=3,incomplete_route=0,
        all119_clean_current_integrated_references_and_five_review_gates_verified=True,all193commands40relative_sites_and200relocated_cases_bound=True,
        current952plus476macro_cases_119font_planes_and_no_FE_or_choices_bound=True,all17negative_cases_rejected_before_mutation=True,
        historical_shared_rules_and_new_current_startup_scope_distinct=True,actual_selected_India_Polder_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        whole_clean_input_patch_reconstruction_exact=True,all500batches114accepted_layers_previous_profiles_and_V1492_promotion_preserved=True,
        prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2818 audit passes:119completed/84revisions/35retentions;registeredV2814/500batches/exactcleanpatch/current31frame pairs.2581integrated,source-prose2584;fullgoalactive.')
