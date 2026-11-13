"""Prepare independent final B172 history,reference,payload and playback audit."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_final_audit_tools_v4409')
SOURCE=Path('scripts/verify_editorial_handoff_v4358c.py')
TARGET=Path('scripts/verify_editorial_handoff_v4409.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index("    spec=mapping['blocks'][0]");b=text.index('    startup=read(',a)
    text=text[:a]+'''    spec=mapping['blocks'][0]
    assert len(spec['command_map'])==38 and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases']
    assert spec['original_declared_end_word_maps']==[dict(source_offset=1880,target_offset=1930,extent=4,source_four_zero_bytes_exact=True)]
    assert mapping['all11_leaves_five_presentations_three_resources_C200_A000_and_single_end_exact']
    assert mapping['source_C200_before_A000_raw00a0ffff010cc960_then6240_preserved']
    assert not spec['original2000_pause_and_resume_maps']
    actual=read('work/analysis/lil_B172_actual_v4394/actual_all27_presentations_resources_C200_A000_and_end.json')
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==27
    assert actual['actual_new_cold_boot_runs']==2 and not actual['offline_only_display_IDs'] and not actual['failures']
    assert actual['paired_region_differences']==[dict(id='DK4_MES_B172_R0007',frame=2950,native_text_plane_exact=True,paired_source_upper_or_portrait_region_differs=True,not_masked_or_retimed=True)]
    assert [(v['case'],v['fixture_exit_frame']) for v in actual['versions']]==[('clean_Japanese',9336),('reviewed_English',9335)]
    assert all(v['actual_C200']['result_words']==[3,0] and v['actual_source_A000']['result_words']==[3,0]
        and v['source_A000_hex']=='00a0ffff010cc960' and v['single_source_end_offset']==1880
        and len(v['selected_B22_command_pairs'])==47 and v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        and [r['word'] for r in v['actual_presentation_commands']]==[0x6000,0x45FF,0x4651,0x4620,0x6240]
        and [r['word'] for r in v['actual_resources']]==[0x6329,0x6340,0x632A] for v in actual['versions'])
    transition=read('work/analysis/lil_B172_transition_review_v4398/all5_sheets_departure_C200_A000_and_paired_return_review.json')
    assert (len(transition['all5_actual_sheets_viewed']),len(transition['English_full_screen_views']),len(transition['Japanese_full_screen_views']))==(5,10,10)
    assert len(transition['all4_paired_full_screen_sheets_viewed'])==4
    assert transition['exact_timing_differences']==dict(total=30,speech=24,control_or_end=6)
    assert len(transition['early_two_transient_nontext_differences'])==2 and len(transition['later99_sailing_samples_including_final20001'])==99
    assert transition['no_open_translation_specific_display_or_control_finding'] and transition['source_A000_packed_semantics_not_inferred']
    for view in transition['all5_actual_sheets_viewed']+transition['English_full_screen_views']+transition['Japanese_full_screen_views']+transition['all4_paired_full_screen_sheets_viewed']:
        assert sha(Path(view['path']).read_bytes())==view['sha256']
    names=read(doc['source_nameplate_consumer_proof'])
    assert names['approved_prose_names']=={'2':'Lil','26':'Julian','201':'Mihwa'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','26':'Julian Lopes','201':'Mihwa'}
    cases=names['native_six_consumer_cases']['rows']
    assert len(cases)==6 and all(c['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for c in cases)
    assert sum(bool(c['original_scratch_rings']) and bool(c['original_getter_writes']) for c in cases)==4
    assert sum(c['actor_ID']==201 and not c['original_scratch_rings'] and not c['original_getter_writes'] for c in cases)==2
''' + text[b:]
    a=text.index("    save(ROOT/'verified_handoff.json'")
    text=text[:a]+'''    from scripts.editorial_ledger_storage_v1 import encode_ledger
    assert encode_ledger(ledger)==lp.read_bytes() and lp.stat().st_size<100*1024*1024
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4408',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receipt_path),
        handoff_receipt_sha256=sha(receipt_path.read_bytes()),fresh_reread=5789,integrated=5789,pending=0,source_prose=5792,revised=3678,retained=2111,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=548,accepted_layers=114,all27_clean_predecessor_integrated_references_and8_retentions_verified=True,
        all38_commands_zero_spans108_stored_cases_presentations_resources_C200_then_A000_single_end_and_names_bound=True,
        actual_two_B22_fixtures27_complete_planes_departure_and_normal_return_verified=True,source_single_end1880_actually_reached=True,
        two_transient_and99_later_nontext_differences_preserved=True,source_A000_raw_semantics_not_inferred=True,
        actual_registered_startup31_whole_frames_and_five_models_verified=True,atomic_compiler_negatives=69,regression_tests_passed=78,
        V4353_promoted_main_unchanged=True,all_prior_completions_and_wider_scope_preserved=True,one_space_complete_ledger_preserved=True,
        remaining_B173_B180_physical_speeches=134,remaining_choice_command_leads=0,full_goal_active=True,
        failed_V4396_pre_view_V4401_field_and_V4408_derivation_producers_preserved=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4408 independently verified:5789/5789/0;5792 source/prose;548/114 stack;exact patch and scoped actual/native/startup pass. V4353 main unchanged;full goal active.')
'''
    changes={
        'B171':'B172','v4358c':'v4409','completion_v4357':'completion_v4408','V4357':'V4408',
        'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37':'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27',
        'release_v4354':'release_v4405','startup_v4356':'startup_v4407','registration_v4352':'registration_v4403',
        'all_routes_combined_v4303':'all_routes_combined_v4353','lil_B171_reference_v4335':'lil_B172_reference_v4384',
        'all-routes-unified-v4353':'all-routes-unified-v4404','all-routes-unified-v4303':'all-routes-unified-v4353',
        '(2120,2312)':'(1884,1936)','[2,25,81]':'[2,26,201]',
        "macros=={'FI':1,'FA':0,'FO':0}":"macros=={'FI':0,'FA':0,'FO':0}",
        "stored['current_final_stored_macro_alignment_cases']==148":"stored['current_final_stored_macro_alignment_cases']==108",'(88,60)':'(68,40)',
        'actual_source_event171_selected':'actual_source_event172_selected',
        'all_current_requested_and_final_framebuffers_equal_V4303':'all_current_requested_and_final_framebuffers_equal_V4353',
        "len(negatives['cases'])==63":"len(negatives['cases'])==69",'unfinished_editorial_scope_v4357':'unfinished_editorial_scope_v4408',
        'remaining_B172_B180':'remaining_B173_B180',
        "'promoted_main_build_v4331']":"'promoted_main_build_v4331','promoted_main_build_v4392']",
        "len(manifest['batches'])==547":"len(manifest['batches'])==548",
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5762':'5789','5765':'5792','3659':'3678','2103':'2111','3909':'3936','4163':'4190','37':'27','24':'19','13':'8','161':'134','171':'172'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(numbers)+r')(?!\d)',lambda m:numbers[m[0]],text)
    assert not re.search(r'B171|\[171\]|==171|all37|2112|2116|2312|all7_actual',text)
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_block172_literals_checked=True,
        all27_references_and8_retentions_to_be_independently_checked=True,full_goal_complete=False))
    print('Prepared independent V4408 full-ledger and B172 completion audit;completion remains gated on actual release/startup.')
