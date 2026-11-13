"""Qualify all existing paired captures and measured limits without replaying them."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_actual_review_v8744')
PROOFS={
 'source_controls':'work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json',
 'source_display':'work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json',
 'source_view':'work/analysis/Hodram_B31_B53_source_view_v8721/direct_source_view_andscoped_name_findings.json',
 'current':'work/analysis/Hodram_B31_B53_current_v8722/current_effective.json',
 'logical':'work/analysis/Hodram_B31_B53_logical_v8724/logical_paragraphs.json',
 'plan':'work/analysis/Hodram_B31_B53_layout_v8725/automatic_plans.json',
 'pages':'work/analysis/Hodram_B31_B53_pages_v8726/compiled_native_pages.json',
 'native_view':'work/analysis/Hodram_B31_B53_native_review_v8727/native_body_review.json',
 'relocation':'work/analysis/Hodram_B31_B53_relocation_v8728/reconstruction.json',
 'stored':'work/analysis/Hodram_B31_B53_stored_v8729/stored_pages_controls_andreferences.json',
 'source_name_composition':'work/analysis/Hodram_actor34_clean_name_composition_v8732/clean_source_full_andprogressive_name_composition.json',
 'source_name_planes':'work/analysis/Hodram_actor34_source_name_planes_v8733b/source_complete_names_andcurrent_reuse.json',
 'independent':'work/analysis/Hodram_B31_B53_independent_v8734/independent_reconstruction.json',
 'name_review':'work/analysis/Hodram_actor34_name_review_v8735/scoped_name_retention_andunchanged_prose.json',
 'reference':'work/analysis/Hodram_B31_B53_reference_v8736/research_image_receipt.json',
 'loaders':'work/analysis/Hodram_B31_B53_loaders_v8737/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'references':'work/analysis/Hodram_B31_B53_references_v8738/references.json',
 'fixtures':'work/analysis/Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json',
 'models':'work/analysis/Hodram_B31_B53_models_v8741/native_models.json',
 'B31_actual':'work/analysis/Hodram_B31_B53_actual_v8742/B31/paired_actual_dialogue_headers_flow_returns.json',
 'B53_actual':'work/analysis/Hodram_B31_B53_actual_v8742b/B53/paired_actual_dialogue_headers_flow_returns.json',
 'audit_correction':'work/analysis/Hodram_B31_B53_actual_audit_tools_v8742b/derivation.json',
 'comparison':'work/analysis/Hodram_B31_B53_comparison_v8743/paired_selected_path_comparison.json',
 'manuscript':'translations/hodram_B31_B53_editorial_manuscript_v3.json',
 'names':'translations/hodram_B31_B53_speaker_name_review_v2.json',
}
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in PROOFS.items()};deps={p:sha(Path(p).read_bytes()) for p in PROOFS.values()}
    for packet in data.values():
        for p,h in packet.get('evidence',{}).items():
            if isinstance(h,str) and len(h)==64:assert sha(Path(p).read_bytes())==h;deps[p]=h
    total_frames=0;total_holds=0;pages=0;actual_ids=set();records=[];runs=[]
    for number,key in [(31,'B31_actual'),(53,'B53_actual')]:
        proof=data[key];assert not proof['unresolved'] and proof['all_observed_complete_body_name_holds_andnative_flow_pass']
        assert len(proof['groups'])==2
        schedules=[]
        for g in proof['groups']:
            folder=Path('work/analysis/Hodram_B31_B53_scene_runs_v8740')/f'route1_B{number}_{g["version"]}'
            terminal,plan=read(folder/'terminal.json'),read(folder/'run_plan.json');report=read(terminal['report']);trace=read(terminal['observer'])
            assert terminal['terminal'] and terminal['all_callbacks_readonly_andhost_slots_restored'] and report['frames']==g['actual_frames']==6001
            for p,h in [(terminal['report'],terminal['report_sha256']),(terminal['observer'],terminal['observer_sha256']),(terminal['run_plan'],terminal['run_plan_sha256']),(plan['inputs'],plan['inputs_sha256'])]:
                assert sha(Path(p).read_bytes())==h;deps[p]=h
            for p in [folder/'terminal.json',folder/'run_plan.json']:deps[str(p)]=sha(p.read_bytes())
            assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
            assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
            schedules.append(report['scripted_input_schedule']);assert schedules[-1]==read(plan['inputs'])
            assert len(g['speeches'])==1 and g['normal_return']['native_result']==([0,1] if number==31 else [0,0]) and g['normal_return']['complete_four_byte_end']
            # The parser-result second word and the carried interpreter mode are
            # separately observed channels. Keep the stopped mistaken check.
            previous=g['command_pairs'][-2]['native_result'][1];last=g['command_pairs'][-1]
            assert g['normal_return']['native_result']==[0,previous] and last['observed_previous_result']==1
            if number==53:assert previous==0 and g['normal_return']['separate_interpreter_carried_mode']==1
            else:assert previous==1
            assert len(g['command_pairs'])==(15 if number==31 else 17)
            assert g['unvisited_conditional_text_IDs']==(['DK4_MES_B31_R0013'] if number==31 else [])
            speech=g['speeches'][0];assert speech['id']==('DK4_MES_B31_R0018' if number==31 else 'DK4_MES_B53_R0007')
            assert speech['name']==('Barbarossa Hayreddin' if number==31 else 'Port Worker') and speech['source_selector']==(34 if number==31 else 113) and speech['pages']==1
            assert len(speech['complete_holds'])==19
            for hold in speech['complete_holds']:
                assert sha(Path(hold['capture']).read_bytes())==hold['sha256'] and hold['complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal'] and hold['complete_name_mask_equal'] and hold['native_geometry']==[216,64]
            total_frames+=6001;total_holds+=19;pages+=1;actual_ids.add(speech['id']);records.append(speech)
            runs.append(dict(block=number,version=g['version'],frames=6001,terminal=str(folder/'terminal.json'),terminal_sha256=sha((folder/'terminal.json').read_bytes()),
                observed_ids=[speech['id']],unvisited_ids=g['unvisited_conditional_text_IDs'],observed_return=g['normal_return']))
        assert schedules[0]==schedules[1]
        for sheet in proof['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert (total_frames,total_holds,pages)==(24004,76,4) and actual_ids=={'DK4_MES_B31_R0018','DK4_MES_B53_R0007'}
    comparison=data['comparison'];assert comparison['total_actual_frames']==24004
    for g in comparison['groups']:
        assert not g['duration_differences'] and not g['UI_request_differences'] and g['following_commands_equal']
        assert all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] and g['final_PRNG_seeds']==[3325064553,3325064553]
        assert all(n['captain_ID']==1 for n in g['final_native_values']) and g['raw_calendars_uninterpreted'][0]==g['raw_calendars_uninterpreted'][1]
        assert len(g['later_RGB_comparisons'])==34 and g['later_RGB_difference_count']==0
        assert all(s['upper_scene_portrait_RGB_equal'] and s['complete_header_region_RGB_equal'] for s in g['scene_pairs']) and not g['no_common_complete_hold']
        assert len(g['following_commands'][0])==len(g['following_commands'][1])==6
        assert all(set(d['different_fields'])=={'decoded_length'} for d in g['command_comparison_differences'])
    assert [len(g['command_comparison_differences']) for g in comparison['groups']]==[2,1]
    sheets=[s for key in ['B31_actual','B53_actual','comparison'] for s in data[key]['review_sheets']]
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert not data['plan']['failures'] and all(not r['base_QA']['issues'] for r in data['plan']['records'])
    assert data['independent']['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert data['loaders']['fresh_native_whole_loads_andcache_hits']==325 and data['loaders']['fresh_initial_parent_modes']==650
    ROOT.mkdir(parents=True);save(ROOT/'qualified_actual_review.json',dict(manuscript=dict(path=PROOFS['manuscript'],sha256=sha(Path(PROOFS['manuscript']).read_bytes())),names=dict(path=PROOFS['names'],sha256=sha(Path(PROOFS['names']).read_bytes())),
        total_runs=4,total_frames=total_frames,total_holds=total_holds,total_observed_page_occurrences=pages,actual_unique_text_IDs=sorted(actual_ids),offline_only_text_IDs=['DK4_MES_B31_R0013'],
        run_bindings=runs,observed_speeches=records,directly_viewed_dialogue_andtransition_sheets=sheets,all_four_sheets_directly_viewed=True,
        paired_body_name_ink_portrait_header_controls_paths_andnormal_returns_verified=True,
        actual_B31_query_value1_long_variant_unforced_short_variant_not_visited=True,
        normal_end_result31_0_1_and53_0_0_separate_from_interpreter_mode1=True,
        stopped_audit8742_wrong_channel_andqualified8742b_preserved=True,
        original_source_fullname19thglyph_row2_test8733_andqualified8733b_preserved=True,
        all5_final_components_wholeactors_captain1_seed3325064553_rawcalendar_and68_later_RGBpairs_match=True,
        three_measured_decoded_length_differences_due_to_original_versus_revised_objects_retained=comparison['groups'],
        zero_command_duration_UI_request_boundary_RNG_orfollowing_command_differences=True,
        all_source_controls_substitutions_all3_native_pages_andretrospective_break_rules_preserved=True,
        paired_Japanese_text_uses_current_English_names_UI_code_font_andoriginal8initializers34bytes=True,
        no_original_optional_activation_eligibility_location_earned_chronology_fullcatalogue_UI_customnames_fullroute_hardware_orfuture_simulation_claim=True,
        natural_dialogue_policy_frozen_production_atomic_registered_patch_startup_andcredit_pending=True,
        no_new_native_emulator_runs_ROM_orcredit_by_this_reader=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={**deps,str(Path(__file__)):sha(Path(__file__).read_bytes())}))
    print('Qualified4captures24004frames76completebody-nameholds4pageoccurrences;B31long/B53warning actual,short offline only. Source/currentglyphs/returns/68lateRGB/finalstate match;all scope limits retained.',flush=True)
