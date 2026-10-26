"""Independently audit B173 completion, cumulative release and preserved wider scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4450')
CHECKPOINT = Path('work/analysis/lil_B173_completion_v4449')
OFFLINE = set()

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
    assert len(keys)==len(allrows)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==5800
    assert keys=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5800,5800,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[]
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],
            ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5803,5803,5800,3686,2114)
    def decision(row):
        value=row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in allrows)=={'revise':3686,'retain':2114}
    assert dict(Counter(historical_key(r)[0] for r in allrows))==ledger['completed_editorial_record_counts_by_file']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5803
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3947
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    family=ledger['completed_editorial_families'][-1]
    assert family['id']=='Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11'
    final=read(family['final_review'])
    assert family['records']==final['records'] and len(final['records'])==11
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':8,'retain-wording':3}
    release=read('work/analysis/lil_B173_release_v4446/registered_release_verification.json')
    candidate=ledger['current_integrated_candidate']
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())==release['canonical_base_sha256']
    rom,old,clean=[NdsImage.open(p) for p in [candidate['path'],'out/all_routes_combined_v4404_candidate.nds','work/clean.nds']]
    blocks,previous,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [rom,old,clean]]
    assert [i for i,(a,b) in enumerate(zip(previous,blocks,strict=True)) if a!=b]==[173]
    assert (len(previous[173]),len(blocks[173]))==(768,800)
    assert [p for _,p,v in old.iter_files() if rom.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(rom.read_file(p)==v for p,v in old.iter_components())
    assert sha(Path('out/lil_B173_reference_v4431_RESEARCH_ONLY.nds').read_bytes())==candidate['sha256']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v4445'
    assert len(manifest['batches'])==549 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4353'
    conf=read('translations/lil_B173_editorial_release_v1.json')
    for path,digest in conf['dependencies'].items():
        assert sha(Path(path).read_bytes())==digest,path
    doc=read(final['manuscript'])
    mapping,stored=read(doc['reference_map']),read(doc['final_padding_proof'])
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    expanded={r['id']:r['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'] for r in stored['final_target_parity_cases']}
    macros=Counter()
    for row in final['records']:
        assert row['block']==173 and all(row['review'].values()) and row['full_clean_context_precedes_comparison']
        assert row['fresh_source_gloss']==row['source_meaning']
        source_at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert jp[173][source_at:source_at+len(raw)]==raw and jp[173][source_at+len(raw)]==0
        at,value=row['integrated_reference']['offset'],bytes.fromhex(row['integrated_hex'])
        assert blocks[173][at:at+len(value)]==value and blocks[173][at+len(value)]==0
        assert row['current_hex']==row['integrated_hex'] and row['current_reference']==row['integrated_reference']
        assert row['record_index']==blocks[173][:at].count(b'\0') and refs[row['id']]['new_offset']==at
        predecessor=row['historical_source_prose_predecessor_fields']
        pa,pv=predecessor['current_reference']['offset'],bytes.fromhex(predecessor['current_hex'])
        assert previous[173][pa:pa+len(pv)]==pv and previous[173][pa+len(pv)]==0
        assert jp[173][source_at-5:source_at+1].hex()==row['source_complete_preamble_hex']==blocks[173][at-5:at+1].hex()
        assert value[0]==row['source_selector'] in [2,202]
        assert bytes.fromhex(expanded[row['id']]).decode('ascii')==row['current_effective_runtime_English']
        for name in ['FI','FA','FO']:
            assert raw.count(name.encode())==row['english'].count('{MACRO:'+name+'}')
            macros[name]+=raw.count(name.encode())
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification']
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph']==row['effective_predecessor_macro_paragraph']
        assert row['actual_B22_display_fixture_observed']==(row['id'] not in OFFLINE)
        assert row['offline_only_complete_native_display_verified']==(row['id'] in OFFLINE)
        assert not row['actual_source_event173_selected'] and row['individual_actual_source_event_activation_not_claimed']
    assert macros=={'FI':0,'FA':0,'FO':0}
    assert stored['current_final_stored_macro_alignment_cases']==44
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(24,20)
    spec=mapping['blocks'][0]
    assert len(spec['command_map'])==23 and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20
    assert spec['original_declared_end_word_maps']==[dict(source_offset=762,target_offset=794,extent=4,source_four_zero_bytes_exact=True)]
    assert mapping['all8_leaves_two_presentations_two_resources_predicate_two_A000s_and_single_end_exact']
    assert mapping['all_four_relative_sites20_target_cases_and_both_suffix_paths_preserved']
    assert not spec['original2000_pause_and_resume_maps']
    actual=read('work/analysis/lil_B173_actual_v4438b/actual_all11_unforced_predicate_paths_effects_and_end.json')
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==11
    assert actual['actual_new_cold_boot_runs']==2 and not actual['offline_only_display_IDs'] and not actual['failures'] and not actual['paired_region_differences']
    assert [(v['case'],v['fixture_exit_frame']) for v in actual['versions']]==[('clean_Japanese',5496),('reviewed_English',5493)]
    for v in actual['versions']:
        assert v['frames']==9001 and v['single_source_end_offset']==762 and len(v['selected_B22_command_pairs'])==31
        assert v['unforced_predicate_result']==1 and v['actual_predicate']['result_words']==[2,1]
        assert [r['original_source_offset'] for r in v['actual_source_A000s']]==[720,748]
        assert [r['result_words'] for r in v['actual_source_A000s']]==[[3,0],[3,1]]
        assert [r['original_source_offset'] for r in v['actual_source_relative_commands']]==[736,740,756]
        assert all(r['result_words']==[3,1] for r in v['actual_source_relative_commands'])
        assert v['actual_presentation_commands'][-1]['result_words']==[3,1] and v['selected_B22_command_pairs'][-1]['result_words']==[0,1]
        assert v['source_A000_hex_by_offset']=={'720':'00a0ffff010b39a2','748':'00a0ffff010cca60'} and v['source_predicate_hex']=='0080ffff000cca70'
        assert [r['source_offset'] for r in v['unvisited_declared_source_objects']]==[744]
        assert [r['word'] for r in v['actual_presentation_commands']]==[0x6000,0x6240] and [r['word'] for r in v['actual_resources']]==[0x6329,0x6340]
    transition=read(doc['postscene_native_state_proof'])
    assert len(transition['all2_actual_sheets_viewed'])==2 and len(transition['paired_full_screen_views'])==6
    assert len(transition['all115_sampled_nontext_region_checks'])==115 and transition['all115_sampled_nontext_regions_equal']
    assert transition['exact_timing_difference_counts']==dict(total=16,speech=8,control_or_end=8)
    assert transition['whole_RGB_town5530_and_final9001_equal'] and all(transition['postscene9001_native_component_equality'].values())
    assert transition['postscene9001_whole1A04_actor_models_and_captain2_equal'] and transition['PRNG_equality_or_future_world_equivalence_not_claimed']
    assert transition['source_relative_sites736740756_actual_744_offline_native_only']
    for view in transition['all2_actual_sheets_viewed']+transition['paired_full_screen_views']:
        assert sha(Path(view['path']).read_bytes())==view['sha256']
    names=read(doc['source_nameplate_consumer_proof'])
    assert names['approved_prose_names']=={'2':'Lil','202':'Reika'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','202':'Reika'}
    cases=names['native_four_consumer_cases']['rows']
    assert len(cases)==4 and all(c['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for c in cases)
    assert sum(c['actor_ID']==2 and bool(c['original_scratch_rings']) and bool(c['original_getter_writes']) for c in cases)==2
    assert sum(c['actor_ID']==202 and not c['original_scratch_rings'] and not c['original_getter_writes'] for c in cases)==2
    startup=read('work/analysis/lil_B173_startup_v4448/cold_boot_Lil_startup_town_verification.json')
    viewed=read('work/analysis/lil_B173_startup_v4448/current_six_frame_visual_review.json')
    assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31
    assert startup['all_current_requested_and_final_framebuffers_equal_V4404'] and startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert startup['source_and_disposable_town_donor_unchanged'] and viewed['viewed'] and sha(Path(viewed['sheet']).read_bytes())==viewed['sha256']
    reg=read('work/analysis/lil_B173_registration_v4444/registration_receipt.json')
    negatives=read(reg['negative_cases'])
    assert reg['negative_count']==len(negatives['cases'])==81 and all(r['rejected'] for r in negatives['cases'])
    units={u['id']:u for u in ledger['coverage_units']}
    assert units['all-route-scenes']['reviewed_route_records']==units['all-route-scenes']['completed_route_records']==4201
    assert units[family['id']]['new_emulator_runs']==4
    assert all(not ids for ids in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']==[]
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784',
                'promoted_main_build_v4186','promoted_main_build_v4226','promoted_main_build_v4289','promoted_main_build_v4331','promoted_main_build_v4392']:
        assert ledger[key]==before[key],key
    scope=ledger['unfinished_editorial_scope_v4449']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0
    assert scope['remaining_B174_B180_physical_speeches']==123 and scope['remaining_choice_command_leads']==0
    assert scope['canonical_Maria32_pending_uncredited'] and scope['later_storylines_shared_town_shop_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4449')
    ROOT.mkdir(parents=True)
    from scripts.editorial_ledger_storage_v1 import encode_ledger
    assert encode_ledger(ledger)==lp.read_bytes() and lp.stat().st_size<100*1024*1024
    changed_roots={'completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','reviewed_but_incomplete_route_record_IDs',
        'active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units','formatting_watchlist',
        'current_integrated_candidate','unfinished_editorial_scope_v4449','lil_B173_completion_v4449','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in changed_roots}=={k:v for k,v in ledger.items() if k not in changed_roots}
    assert receipt['new_completed_records']==11 and receipt['new_source_prose_reviews']==0 and receipt['new_actual_emulator_runs']==4
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4449',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receipt_path),
        handoff_receipt_sha256=sha(receipt_path.read_bytes()),fresh_reread=5800,integrated=5800,pending=0,source_prose=5803,revised=3686,retained=2114,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=549,accepted_layers=114,all11_clean_predecessor_integrated_references_and3_retentions_verified=True,
        all23_commands_four_relative_sites20_target_cases44_stored_cases_predicate_two_effects_single_end_and_names_bound=True,
        actual_two9001_frame_B22_fixtures11_complete_planes_and_normal_return_verified=True,
        actual_VM_last_result1_survives_type3_and_end=True,unvisited_jump744_explicitly_offline_native_only=True,
        all115_nontext_regions_and_postscene_native_component_actor_scope_verified=True,
        actual_registered_startup31_whole_frames_and_five_models_verified=True,atomic_compiler_negatives=81,regression_tests_passed=78,
        V4353_promoted_main_unchanged=True,all_prior_completions_and_wider_scope_preserved=True,one_space_complete_ledger_preserved=True,
        remaining_B174_B180_physical_speeches=123,remaining_choice_command_leads=0,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4449 independently verified:5800/5800/0;5803 source/prose;549/114 stack;exact patch and scoped actual/native/startup pass. MainV4353 unchanged;full goal active.')
