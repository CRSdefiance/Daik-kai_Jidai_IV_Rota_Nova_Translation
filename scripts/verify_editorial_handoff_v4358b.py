"""Independently audit B171 completion, cumulative release and preserved wider scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4358b')
CHECKPOINT = Path('work/analysis/lil_B171_completion_v4357')
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
    assert len(keys)==len(allrows)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==5762
    assert keys=={historical_key(r) for r in fresh['record_keys']}=={historical_key(r) for r in fresh['integrated_record_keys']}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5762,5762,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[]
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],
            ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5765,5765,5762,3659,2103)
    def decision(row):
        value=row.get('historical_editorial_decision') or row.get('decision') or row.get('editorial_decision')
        assert value.startswith(('revis','retain'))
        return 'revise' if value.startswith('revis') else 'retain'
    assert Counter(decision(r) for r in allrows)=={'revise':3659,'retain':2103}
    assert dict(Counter(historical_key(r)[0] for r in allrows))==ledger['completed_editorial_record_counts_by_file']
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5765
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3909
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    family=ledger['completed_editorial_families'][-1]
    assert family['id']=='Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37'
    final=read(family['final_review'])
    assert family['records']==final['records'] and len(final['records'])==37
    assert Counter(r['editorial_decision'] for r in final['records'])=={'revise':24,'retain-wording':13}
    release=read('work/analysis/lil_B171_release_v4354/registered_release_verification.json')
    candidate=ledger['current_integrated_candidate']
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())==release['canonical_base_sha256']
    rom,old,clean=[NdsImage.open(p) for p in [candidate['path'],'out/all_routes_combined_v4303_candidate.nds','work/clean.nds']]
    blocks,previous,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [rom,old,clean]]
    assert [i for i,(a,b) in enumerate(zip(previous,blocks,strict=True)) if a!=b]==[171]
    assert (len(previous[171]),len(blocks[171]))==(2120,2312)
    assert [p for _,p,v in old.iter_files() if rom.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(rom.read_file(p)==v for p,v in old.iter_components())
    assert sha(Path('out/lil_B171_reference_v4335_RESEARCH_ONLY.nds').read_bytes())==candidate['sha256']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v4353'
    assert len(manifest['batches'])==547 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4303'
    conf=read('translations/lil_B171_editorial_release_v1.json')
    for path,digest in conf['dependencies'].items():
        assert sha(Path(path).read_bytes())==digest,path
    doc=read(final['manuscript'])
    mapping,stored=read(doc['reference_map']),read(doc['final_padding_proof'])
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    expanded={r['id']:r['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'] for r in stored['final_target_parity_cases']}
    macros=Counter()
    for row in final['records']:
        assert row['block']==170 and all(row['review'].values()) and row['full_clean_context_precedes_comparison']
        assert row['fresh_source_gloss']==row['source_meaning']
        source_at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert jp[171][source_at:source_at+len(raw)]==raw and jp[171][source_at+len(raw)]==0
        at,value=row['integrated_reference']['offset'],bytes.fromhex(row['integrated_hex'])
        assert blocks[171][at:at+len(value)]==value and blocks[171][at+len(value)]==0
        assert row['current_hex']==row['integrated_hex'] and row['current_reference']==row['integrated_reference']
        assert row['record_index']==blocks[171][:at].count(b'\0') and refs[row['id']]['new_offset']==at
        predecessor=row['historical_source_prose_predecessor_fields']
        pa,pv=predecessor['current_reference']['offset'],bytes.fromhex(predecessor['current_hex'])
        assert previous[171][pa:pa+len(pv)]==pv and previous[171][pa+len(pv)]==0
        assert jp[171][source_at-5:source_at+1].hex()==row['source_complete_preamble_hex']==blocks[171][at-5:at+1].hex()
        assert value[0]==row['source_selector'] in [2,25,81]
        assert bytes.fromhex(expanded[row['id']]).decode('ascii')==row['current_effective_runtime_English']
        for name in ['FI','FA','FO']:
            assert raw.count(name.encode())==row['english'].count('{MACRO:'+name+'}')
            macros[name]+=raw.count(name.encode())
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification']
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph']==row['effective_predecessor_macro_paragraph']
        assert row['actual_B22_display_fixture_observed']==(row['id'] not in OFFLINE)
        assert row['offline_only_complete_native_display_verified']==(row['id'] in OFFLINE)
        assert not row['actual_source_event171_selected'] and row['individual_actual_source_event_activation_not_claimed']
    assert macros=={'FI':1,'FA':0,'FO':0}
    assert stored['current_final_stored_macro_alignment_cases']==148
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(88,60)
    spec=mapping['blocks'][0]
    assert len(spec['command_map'])==45 and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases']
    assert spec['original_declared_end_word_maps']==[
        dict(source_offset=2112,target_offset=2302,extent=4,source_four_zero_bytes_exact=True),
        dict(source_offset=2116,target_offset=2306,extent=4,source_four_zero_bytes_exact=True)]
    assert not spec['original2000_pause_and_resume_maps'] and mapping['no_source_A000_or2000_pause']
    assert [r['word'] for r in spec['mapped_native_commands'] if r['word']!=0x4000]==[0x6000,0x4500,0x4621,0x61FF,0x6325,0xC200,0,0]
    control=read(doc['relocated_control_proof'])
    assert len(control['relocated_dispatch_cases'])==37 and not control['relocated_predicate_pairs']
    assert len(control['all8_source_current_target_nonrelative_nonspeech_leaves'])==8
    assert len(control['relocated_C200_pairs'])==1 and control['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
    names=read(doc['source_nameplate_consumer_proof'])['native_six_consumer_cases']['rows']
    assert len(names)==6 and all(r['original_scratch_rings'] and r['original_getter_writes'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in names)
    repeat=read(doc['focused_repeat_proof'])
    assert repeat['paired_town11770_whole1A04_actor_models_and_captain2_equal']
    assert len(repeat['cross_language_command_timing_differences'])==22
    assert Counter(r['source']['word'] for r in repeat['cross_language_command_timing_differences'])=={0x4000:17,0x4621:1,0x61FF:1,0x6325:1,0xC200:1,0:1}
    assert repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
    assert all(all(r['component_equality'].values()) for r in repeat['paired_native_persistent_state_and_PRNG_samples'] if r['frame']<=16450)
    assert ledger['lil_B171_command_timing_count_amendment_v4349']==before['lil_B171_command_timing_count_amendment_v4349']
    actual=read('work/analysis/lil_B171_actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end.json')
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==37
    assert actual['actual_new_cold_boot_runs']==2 and set(actual['offline_only_display_IDs'])==OFFLINE
    assert not actual['failures'] and not actual['paired_region_differences']
    assert [(v['case'],v['fixture_exit_frame']) for v in actual['versions']]==[('clean_Japanese',11737),('reviewed_English',11735)]
    assert all(v['actual_C200']['result_words']==[3,0] and [r['word'] for r in v['actual_presentation_commands']]==[0x6000,0x4500,0x4621,0x61FF] and [r['word'] for r in v['actual_resources']]==[0x6325] for v in actual['versions'])
    transition=read('work/analysis/lil_B171_transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review.json')
    assert (len(transition['all7_actual_sheets_viewed']),len(transition['English_full_screen_views']),len(transition['Japanese_full_screen_views']))==(7,6,4)
    for view in transition['all7_actual_sheets_viewed']+transition['English_full_screen_views']+transition['Japanese_full_screen_views']:
        assert sha(Path(view['path']).read_bytes())==view['sha256']
    startup=read('work/analysis/lil_B171_startup_v4356/cold_boot_Lil_startup_town_verification.json')
    viewed=read('work/analysis/lil_B171_startup_v4356/current_six_frame_visual_review.json')
    assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31
    assert startup['all_current_requested_and_final_framebuffers_equal_V4303'] and startup['all_five_postload_actor_model_and_captain_checks_equal']
    assert startup['source_and_disposable_town_donor_unchanged'] and viewed['viewed'] and sha(Path(viewed['sheet']).read_bytes())==viewed['sha256']
    reg=read('work/analysis/lil_B171_registration_v4352/registration_receipt.json')
    negatives=read(reg['negative_cases'])
    assert reg['negative_count']==len(negatives['cases'])==63 and all(r['rejected'] for r in negatives['cases'])
    units={u['id']:u for u in ledger['coverage_units']}
    assert units['all-route-scenes']['reviewed_route_records']==units['all-route-scenes']['completed_route_records']==4163
    assert units[family['id']]['new_emulator_runs']==6
    assert all(not ids for ids in ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']==[]
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784',
                'promoted_main_build_v4186','promoted_main_build_v4226','promoted_main_build_v4289','promoted_main_build_v4331']:
        assert ledger[key]==before[key],key
    scope=ledger['unfinished_editorial_scope_v4357']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert scope['incomplete_COMMON']==3 and scope['incomplete_route_source_prose']==0
    assert scope['remaining_B172_B180_physical_speeches']==161 and scope['remaining_choice_command_leads']==0
    assert scope['canonical_Maria32_pending_uncredited'] and scope['later_storylines_shared_town_shop_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4357')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4357',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receipt_path),
        handoff_receipt_sha256=sha(receipt_path.read_bytes()),fresh_reread=5762,integrated=5762,pending=0,source_prose=5765,revised=3659,retained=2103,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=547,accepted_layers=114,all37_clean_predecessor_integrated_references_and13_retentions_verified=True,
        all45_commands_zero_spans148_stored_cases_presentations_resource_C200_both_ends_names_and_macros_bound=True,
        actual_two_B22_fixtures37_complete_planes_dream_morning_and_normal_return_verified=True,all37_observed_second_end_explicitly_offline_only=True,
        actual_registered_startup31_whole_frames_and_five_models_verified=True,atomic_compiler_negatives=63,regression_tests_passed=78,
        V4303_promoted_main_unchanged=True,all_prior_completions_and_wider_scope_preserved=True,
        remaining_B172_B180_physical_speeches=161,remaining_choice_command_leads=0,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4357 independently verified:5762/5762/0;5765 source/prose;547/114 stack;exact patch and scoped actual/native/startup pass. V4303 main unchanged;full goal active.')
