"""Prepare independent completion audit for all history and B173 exact references."""
from pathlib import Path
import io,re,tokenize
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_final_audit_tools_v4450')
SOURCE=Path('scripts/verify_editorial_handoff_v4409b.py')
TARGET=Path('scripts/verify_editorial_handoff_v4450.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index("    spec=mapping['blocks'][0]");b=text.index('    startup=read(',a)
    text=text[:a]+'''    spec=mapping['blocks'][0]
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
''' + text[b:]
    a=text.index("    save(ROOT/'verified_handoff.json'");text=text[:a]
    changes={
        'B172':'B173','editorial_handoff_verification_v4409b':'editorial_handoff_verification_v4450',
        'completion_v4408':'completion_v4449','V4408':'V4449',
        'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27':'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11',
        "{'revise':19,'retain-wording':8}":"{'revise':8,'retain-wording':3}",
        'release_v4405':'release_v4446','startup_v4407':'startup_v4448','registration_v4403':'registration_v4444',
        'all_routes_combined_v4353':'all_routes_combined_v4404','lil_B172_reference_v4384':'lil_B173_reference_v4431',
        'all-routes-unified-v4404':'all-routes-unified-v4445','(1884,1936)':'(768,800)','[2,26,201]':'[2,202]',
        "stored['current_final_stored_macro_alignment_cases']==108":"stored['current_final_stored_macro_alignment_cases']==44",'(68,40)':'(24,20)',
        'actual_source_event172_selected':'actual_source_event173_selected',
        'all_current_requested_and_final_framebuffers_equal_V4353':'all_current_requested_and_final_framebuffers_equal_V4404',
        "len(negatives['cases'])==69":"len(negatives['cases'])==81",'unfinished_editorial_scope_v4408':'unfinished_editorial_scope_v4449',
        'remaining_B173_B180':'remaining_B174_B180',"units[family['id']]['new_emulator_runs']==6":"units[family['id']]['new_emulator_runs']==4",
        "len(manifest['batches'])==548":"len(manifest['batches'])==549",
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5789':'5800','5792':'5803','3678':'3686','2111':'2114','3936':'3947','4190':'4201','27':'11','134':'123','172':'173'}
    tokens=[]
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type==tokenize.NUMBER and token.string in numbers:token=token._replace(string=numbers[token.string])
        tokens.append(token)
    text=tokenize.untokenize(tokens)
    text+='''    changed_roots={'completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
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
'''
    assert not re.search(r'B172|\[172\]|==172|all27|1880|1930|all5_actual',text)
    assert 'utf-8' in text and 'utf-3' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),target_sha256=sha(TARGET.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),all_block173_literals_and_eight_vs_three_decisions_checked=True,
        new_completion_once=11,source_credit_again=0,full_goal_complete=False))
    print('Prepared independent full-history/B173 completion audit;four total family boots and preserved VM result1 bound.')
