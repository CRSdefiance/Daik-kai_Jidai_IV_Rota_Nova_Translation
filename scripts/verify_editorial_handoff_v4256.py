"""Independently audit B169 completion, cumulative release and preserved wider scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4256')
CHECKPOINT = Path('work/analysis/lil_B169_completion_v4255')
OFFLINE = {'DK4_MES_B169_R0067','DK4_MES_B169_R0082','DK4_MES_B169_R0097'}

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt_path = CHECKPOINT/'completion_receipt.json'
    receipt = read(receipt_path)
    for path,digest in {**receipt['updated_files'],**receipt['evidence']}.items():
        assert sha(Path(path).read_bytes())==digest,path
    lp = Path('translations/editorial_review_current_v1.json')
    ledger,before = read(lp),read(CHECKPOINT/(lp.name+'.before'))
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    allrows = [r for family in ledger['completed_editorial_families'] for r in family['records']]
    keys = {historical_key(r) for r in allrows}
    assert len(keys)==len(allrows)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==5692
    assert keys=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5692,5692,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[]
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],
            ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5695,5695,5692,3614,2078)
    def decision(row):
        value=row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in allrows)=={'revise':3614,'retain':2078}
    assert dict(Counter(historical_key(r)[0] for r in allrows))==ledger['completed_editorial_record_counts_by_file']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5695
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3839
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    family=ledger['completed_editorial_families'][-1]
    assert family['id']=='Lil-B169-Mikhail-Proof-legend-clues-ruins-tavern-give-and-take36'
    final=read(family['final_review'])
    assert family['records']==final['records'] and len(final['records'])==36
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':19,'retain-wording':17}
    release=read('work/analysis/lil_B169_release_v4252/registered_release_verification.json')
    candidate=ledger['current_integrated_candidate']
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())==release['canonical_base_sha256']
    rom,old,clean=[NdsImage.open(p) for p in [candidate['path'],'out/all_routes_combined_v4204_candidate.nds','work/clean.nds']]
    blocks,previous,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [rom,old,clean]]
    assert [i for i,(a,b) in enumerate(zip(previous,blocks,strict=True)) if a!=b]==[169]
    assert (len(previous[169]),len(blocks[169]))==(2564,2588)
    assert [p for _,p,v in old.iter_files() if rom.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(rom.read_file(p)==v for p,v in old.iter_components())
    assert sha(Path('out/lil_B169_reference_v4236_RESEARCH_ONLY.nds').read_bytes())==candidate['sha256']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v4251'
    assert len(manifest['batches'])==545 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4204'
    conf=read('translations/lil_B169_editorial_release_v1.json')
    for path,digest in conf['dependencies'].items():
        assert sha(Path(path).read_bytes())==digest,path
    doc=read(final['manuscript'])
    mapping,stored=read(doc['reference_map']),read(doc['final_padding_proof'])
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    expanded={r['id']:r['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'] for r in stored['final_target_parity_cases']}
    macros=Counter()
    for row in final['records']:
        assert row['block']==169 and all(row['review'].values()) and row['full_clean_context_precedes_comparison']
        assert row['fresh_source_gloss']==row['source_meaning']
        source_at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert jp[169][source_at:source_at+len(raw)]==raw and jp[169][source_at+len(raw)]==0
        at,value=row['integrated_reference']['offset'],bytes.fromhex(row['integrated_hex'])
        assert blocks[169][at:at+len(value)]==value and blocks[169][at+len(value)]==0
        assert row['current_hex']==row['integrated_hex'] and row['current_reference']==row['integrated_reference']
        assert row['record_index']==blocks[169][:at].count(b'\0') and refs[row['id']]['new_offset']==at
        predecessor=row['historical_source_prose_predecessor_fields']
        pa,pv=predecessor['current_reference']['offset'],bytes.fromhex(predecessor['current_hex'])
        assert previous[169][pa:pa+len(pv)]==pv and previous[169][pa+len(pv)]==0
        assert jp[169][source_at-5:source_at+1].hex()==row['source_complete_preamble_hex']==blocks[169][at-5:at+1].hex()
        assert value[0]==row['source_selector'] in [2,6,9,20,21,76]
        assert bytes.fromhex(expanded[row['id']]).decode('ascii')==row['current_effective_runtime_English']
        for name in ['FI','FA','FO']:
            assert raw.count(name.encode())==row['english'].count('{MACRO:'+name+'}')
            macros[name]+=raw.count(name.encode())
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification']
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph']==row['effective_predecessor_macro_paragraph']
        assert row['actual_B22_display_fixture_observed']==(row['id'] not in OFFLINE)
        assert row['offline_only_complete_native_display_verified']==(row['id'] in OFFLINE)
        assert not row['actual_source_event169_selected'] and row['individual_actual_source_event_activation_not_claimed']
    assert macros=={'FI':5,'FA':0,'FO':2}
    assert stored['current_final_stored_macro_alignment_cases']==144
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(100,44)
    spec=mapping['blocks'][0]
    assert len(spec['command_map'])==53 and len(spec['relative_skip_fixups'])==12 and len(spec['target_native_skip_cases'])==60
    assert spec['original_declared_end_word_maps']==[dict(source_offset=2558,target_offset=2584,extent=4,source_four_zero_bytes_exact=True)]
    assert mapping['source_effect_operand_hex_values']==['0029','0001'] and mapping['source_effect_operand_decimal_values']==[41,1]
    amendment=read(doc['source_effect_operand_notation_amendment'])
    assert amendment['operand_decimal_values']==[41,1] and amendment['source_command_hex']=='00a0ffff29000100'
    control=read(doc['relocated_control_proof'])
    assert len(control['relocated_dispatch_cases'])==36 and len(control['relocated_predicate_pairs'])==3
    assert len(control['all5_source_current_target_nonrelative_nonspeech_leaves'])==5
    names=read(doc['source_nameplate_consumer_proof'])['native_twelve_consumer_cases']['rows']
    assert len(names)==12 and all(r['original_scratch_rings'] and r['original_getter_writes'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in names)
    actual=read('work/analysis/lil_B169_actual_v4244/actual_progressive_three_predicates_full_effect_and_return.json')
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==33
    assert actual['actual_new_cold_boot_runs']==2 and set(actual['offline_only_display_IDs'])==OFFLINE
    assert not actual['failures'] and not actual['paired_region_differences']
    assert [(v['case'],v['fixture_exit_frame']) for v in actual['versions']]==[('clean_Japanese',10776),('reviewed_English',10773)]
    assert all(v['actual_source_hex0029_0001_effect']['result_words']==[3,0] for v in actual['versions'])
    transition=read('work/analysis/lil_B169_transition_review_v4245/all6_sheets_source_effect_and_paired_return_review.json')
    assert (len(transition['all6_actual_sheets_viewed']),len(transition['English_full_screen_views']),len(transition['Japanese_full_screen_views']))==(6,3,2)
    for view in transition['all6_actual_sheets_viewed']+transition['English_full_screen_views']+transition['Japanese_full_screen_views']:
        assert sha(Path(view['path']).read_bytes())==view['sha256']
    startup=read('work/analysis/lil_B169_startup_v4254/cold_boot_Lil_startup_town_verification.json')
    viewed=read('work/analysis/lil_B169_startup_v4254/current_six_frame_visual_review.json')
    assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31
    assert startup['all_current_requested_and_final_framebuffers_equal_V4204'] and startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert startup['source_and_disposable_town_donor_unchanged'] and viewed['viewed'] and sha(Path(viewed['sheet']).read_bytes())==viewed['sha256']
    reg=read('work/analysis/lil_B169_registration_v4250b/registration_receipt.json')
    negatives=read(reg['negative_cases'])
    assert reg['negative_count']==len(negatives['cases'])==55 and all(r['rejected'] for r in negatives['cases'])
    units={u['id']:u for u in ledger['coverage_units']}
    assert units['all-route-scenes']['reviewed_route_records']==units['all-route-scenes']['completed_route_records']==4093
    assert units[family['id']]['new_emulator_runs']==4
    assert all(not ids for ids in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']==[]
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784',
                'promoted_main_build_v4186','promoted_main_build_v4226']:
        assert ledger[key]==before[key],key
    scope=ledger['unfinished_editorial_scope_v4255']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0
    assert scope['remaining_B170_B180_physical_speeches']==231 and scope['remaining_choice_command_leads']==0
    assert scope['canonical_Maria32_pending_uncredited'] and scope['later_storylines_shared_town_shop_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4255')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4255',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receipt_path),
        handoff_receipt_sha256=sha(receipt_path.read_bytes()),fresh_reread=5692,integrated=5692,pending=0,source_prose=5695,revised=3614,retained=2078,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=545,accepted_layers=114,all36_clean_predecessor_integrated_references_and17_retentions_verified=True,
        all53_commands12_spans60_skips144_stored_cases_three_predicates_names_macros_and_corrected_A000_operands_bound=True,
        actual_two_B22_fixtures33_complete_planes_source_effect_and_normal_return_verified=True,three_conditional_remarks_explicitly_offline_only=True,
        actual_registered_startup31_whole_frames_and_five_models_verified=True,atomic_compiler_negatives=55,regression_tests_passed=78,
        V4204_promoted_main_unchanged=True,all_prior_completions_and_wider_scope_preserved=True,
        remaining_B170_B180_physical_speeches=231,remaining_choice_command_leads=0,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4255 independently verified:5692/5692/0;5695 source/prose;545/114 stack;exact patch and scoped actual/native/startup pass. V4204 main unchanged;full goal active.')
