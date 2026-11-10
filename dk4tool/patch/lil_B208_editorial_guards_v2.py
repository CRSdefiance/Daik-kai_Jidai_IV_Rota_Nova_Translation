"""Read-only B208 native/source/actual proof guards; never mutate an archive."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

def validate_observations(doc,mapping,conf,load,require):
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','loader_proof','source_census','termination_decode_proof','actual_proof','postscene_native_state_proof','representative_proof','native_approval','speaker_name_approval','phase_capacity_proof']
    p={k:load(doc[k]) for k in keys};native,stored,controls,loader,census,ends,actual,state,view,approval,names,phase=p.values()
    require(native['current_original_macro_alignment_calls']==192 and native['complete_progressive_planes']==23 and native['complete_FE_logical_and_physical_planes']==1 and native['progressive_alignment_calls']==184 and native['FE_null_actor_alignment_calls']==8,'native consumer split')
    require(approval['all24_five_gates_approved'] and approval['source_and_formatter_negative_controls']==30 and len(approval['four_individual_source_target_rowcount_reasons'])==4 and len(approval['one_reviewed_ordinary_boundary'])==1,'individual native approval')
    require(len(native['negative_controls'])==30 and all(c['rejected'] for c in native['negative_controls']),'native/formatter negatives')
    require(phase['fresh_original_compiled_alignment_cases']==12 and phase['first36_cell_preLF_auto_wrap_rejected'] and phase['thirty_five_visible_continuation_characters_with_original_guard_fit_and_complete'] and phase['odd35_row_emits_no_preLF_phase_space_even34_does'] and phase['unchanged216px_sixpx_font_four_rows_guards_and_pair_phase'] and phase['no_changed_words_or_production_authored_breaks'],'exact native phase capacity')
    require(phase['unchanged_codec_sha256']==sha(Path(phase['unchanged_codec_source']).read_bytes()) and len(phase['cases'])==3,'unchanged codec/three capacity probes')
    for c in phase['cases']:
        require(c['all_complete_independent_glyphs_canaries_bounds_origins_and_three_rows_equal'] and len(c['native_macro_cases']['cases'])==4 and sha(Path(c['preview']).read_bytes())==c['preview_sha256'],'complete phase probe')
    require(stored['current_final_stored_macro_alignment_cases']==96 and stored['new_parity_macro_alignment_cases']==52 and stored['exact_byte_identical_reused_macro_alignment_cases']==44 and stored['new_parity_tail_planes']==13 and stored['all24_final_targets_complete_native_planes_equal_reviewed_planes'],'stored parity proof')
    require(len(controls['relocated_dispatch_cases'])==24 and len(controls['all5_source_current_target_nontext_leaves'])==5 and len(controls['fresh_current_four_structural_effect_cases'])==4 and len(controls['fresh_current_target10_complete_end_cases'])==10 and controls['original_Cristina_Erneco_Mysterious_Old_Man_names_and_unknown_metadata_preserved'] and controls['no_natural_event_or_full_stat_inventory_quest_or_eligibility_claim'],'all controls/names')
    require(loader['all336_whole_blocks_and672_modes_each_pass'] and loader['B208_fits_original_0x2400_cache'] and loader['SDK_IO_bridges_only_no_loader_or_cache_success_stub'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'],'whole loader/cache')
    require([r['ROM_sha256'] for r in loader['versions']]==[doc['current_ROM_sha256'],conf['reference_ROM_sha256']],'whole-ROM loader identities')
    for r in loader['versions']:
        require(r['whole_SC2_loads_and_cache_hits']==336 and r['original_parent_modes']==672,'loader cases')
        for k in ['load','parent']:require(sha(Path(r[k+'_proof']).read_bytes())==r[k+'_sha256'],'loader evidence')
    require(census['all29_clean_current_target_commands_and_no_relative_sites_reexecuted'] and census['research_ROM_sha256']==conf['reference_ROM_sha256'] and census['blocks'][0]['mapped_commands']==mapping['blocks'][0]['mapped_native_commands'],'independent command census')
    require(ends['no_end_decode_zero_tail_dependency'] and ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',1182),('research',1190)],'guarded complete ends')
    require(names['two_native_name_planes_four_getters32_macro_alignments91_actual_header_holds_approved'] and names['source_specific_ASCII_flush_and_original_style11_bound'] and names['no_Unknown_nationality_expansion_or_unsupported_name_respelling'] and names['all_other_names_aliases_full_goal_and_later_technical_reaudit_open'],'contextual names')
    require(actual['actual_unique_speech_panels']==actual['actual_English_speech_observations']==24 and actual['complete_native_text_and_nameplate_holds']==95,'actual coverage')
    require(sum(len(r['holds']) for r in actual['actual_panels'])==95,'all95 individual holds')
    require(not any(actual[k] for k in ['failures','offline_only_display_IDs','command_result_differences','command_UI_word_differences','paired_nontext_region_differences']),'actual findings')
    rows=doc['records'];ids=[r['id'] for r in rows];require(ids==[r['id'] for r in actual['actual_panels']]==mapping['actual_sampled_display_IDs'] and mapping['offline_only_display_IDs']==[],'actual IDs')
    for panel,row in zip(actual['actual_panels'],rows,strict=True):
        fe=row['source_selector']==254
        require(panel['prefix']==row['source_selector'] and panel['name']==(None if fe else {7:'Cristina Erneco',170:'Mysterious Old Man'}[row['source_selector']]) and panel['kind']==row['kind'] and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'] and panel['holds'],'actual panel identity')
        for h in panel['holds']:
            require(all(h[k] for k in ['all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane','source_correct_nameplate_or_FE_absence_verified','both_versions_in_same_semantic_speech_at_this_frame','paired_upper_portrait_name_region_equal']) and sha(Path(h['capture']).read_bytes())==h['capture_sha256'],'complete actual body/name/source hold')
            require(h['nameplate_expected']==(not fe) and (h['FE_null_actor_absent_nameplate_region_matches_source'] is True and h['complete_current_style11_nameplate_glyphs_and_blank_guards_equal'] is None if fe else h['complete_current_style11_nameplate_glyphs_and_blank_guards_equal'] is True),'distinct FE absent nameplate')
    feholds=sum(len(c['holds']) for c in actual['actual_panels'] if c['prefix']==254);require(feholds==4,'four actual FE holds')
    left,right=actual['versions'];require([v['frames'] for v in [left,right]]==[16001,16001] and [v['exit_frame'] for v in [left,right]]==[8616,8616] and all(len(v['command_pairs'])==38 for v in [left,right]),'actual run extents')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']];require(shape(left)==shape(right),'actual paths/results')
    expected=[None]*9+[r['old_offset'] for r in mapping['blocks'][0]['command_map']]
    for v in [left,right]:
        require([r['source_offset'] for r in v['command_pairs']]==expected and [(r['id'],r['source_record_index'],r['prefix']) for r in v['speech_intervals']]==[(r['id'],r['source_record_index'],r['source_selector']) for r in rows],'actual complete source identities')
        report=load(v['capture_report']);require(report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==16001,'cold-boot input scope')
        require([r['frame'] for r in v['following_commands'] if r['word']==0 and r['native_result'][0]==0]==[13414],'complete following B120 end')
    require(left['input_schedule_sha256']==right['input_schedule_sha256'],'identical ordinary inputs')
    timing=[];rng=[];durations=[]
    for a,b in zip(left['command_pairs'],right['command_pairs'],strict=True):
        identity=dict(source_offset=a['source_offset'],word=a['word'])
        if [a['start'],a['returned']]!=[b['start'],b['returned']]:timing.append(dict(**identity,Japanese=[a['start'],a['returned']],English=[b['start'],b['returned']]))
        if [a['before_RNG'],a['after_RNG']]!=[b['before_RNG'],b['after_RNG']]:rng.append(dict(**identity,Japanese=[a['before_RNG'],a['after_RNG']],English=[b['before_RNG'],b['after_RNG']]))
        da,db=a['returned']-a['start'],b['returned']-b['start']
        if da!=db:durations.append(dict(**identity,source_duration=da,English_duration=db,delta=db-da))
    require(actual['command_timing_differences']==timing and len(timing)==16 and actual['command_RNG_differences']==rng and len(rng)==18,'all measured timing/RNG witnesses')
    require(state['command_duration_changes']==durations and len(durations)==8 and all(r['word']==0x4000 for r in durations),'eight speech duration witnesses')
    later=[r for r in actual['postscene_whole_RGB_comparisons'] if not r['whole_RGB_equal']]
    require(later==actual['later_whole_RGB_differences']==state['all44_unmasked_later_differences']==state['broader_later_differences'] and len(later)==44 and not state['prompt_bounded_later_differences'],'all44 unmasked broader RGB differences')
    require(state['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False) and not state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['final_PRNG_seeds']==[4024327688,3039668243] and state['no_whole_RAM_future_sequence_broad_simulation_or_complete_timing_cause_claim'],'different bounded final state')
    require([v['components']['calendar']['ticks'] for v in state['native_values']]==[1008,1005] and [v['captain_ID'] for v in state['native_values']]==[2,2],'measured calendar/captain')
    require(view['actual_proof_sha256']==state['actual_proof_sha256']==sha(Path(doc['actual_proof']).read_bytes()) and not view['visual_review_pending'] and view['no_open_translation_specific_display_control_or_return_finding'] and view['all16_timing18_RNG44_broader_RGB_eight_duration_and_different_final_state_witnesses_retained'] and view['broad_postscene_full_RAM_future_world_equivalence_unproven'] and view['natural_event208_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed'] and view['final16001_both_sailing_viewed'],'honest representative scope')
    require(view['source_exit_frame']==view['English_exit_frame']==8616 and view['normal_port_return_frame']==8710 and view['following_B120_end_frame']==13414,'observed return frames')
    require(len(view['viewed_sheets'])==6 and all(r['viewed'] and r['viewed_after_image_return'] and sha(Path(r['path']).read_bytes())==r['sha256'] for r in view['viewed_sheets']),'six viewed sheets')
    require(actual['source_and_English_same_ARM9_COMMON_components_all_other_files_all335_other_blocks_and_input_schedules'] and actual['no_capture_masking_pixel_edit_or_retiming'] and actual['all_jobs_terminal_and_reaped'],'paired code/input provenance')
    thought=next(r for r in rows if r['source_record_index']==86);notice=next(r for r in rows if r['source_record_index']==90)
    require(thought['kind']=='progressive' and thought['source_selector']==7 and thought['english'].split('}',1)[1].startswith('(') and thought['english'].endswith(')'),'private thought')
    require(notice['kind']=='system-FE' and notice['source_selector']==254 and notice['english']=='{SPEAKER:FE}Cristina: Charm +1!','literal character/Charm/one-point notice')
    require(not any(d.get('full_goal_complete') for d in [doc,mapping,*p.values()]),'full objective remains open')
    return p
