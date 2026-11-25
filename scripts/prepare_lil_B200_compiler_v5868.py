"""Derive B200's atomic compiler with its own complete source and measured-scene guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.seal_lil_B200_references_v5865 import FLAGS
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B200_compiler_tools_v5868')
TERM_FLAGS=['actor19_Carlo_Sinat_existing_project_spelling_retained_from_clean_fields',
    'explicit_not_a_doctor_denial_preserved','spoken_thankyou_object_stays_unnamed_no_new_item_title_widget_or_full_effect_fidelity_credit',
    'source_portrait_name_absence_and_outdoor_inn_picture_and_stat_transitions_preserved',
    'source_roster_funds_RNG_conditions_and_effect_results_unforced',
    'initialized_Amsterdam_B22_fixture_not_natural_event200_activation_original_location_full_route_or_hardware']
GATES='''    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all19_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged']
        and seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())
        and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed references differ')
    require(mapping['format']=='dk4-lil-B200-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    require(conf['required_map_flags']==FLAGS and conf['required_term_flags']==TERM_FLAGS,'complete required flags differ')
    for flag in FLAGS:require(mapping.get(flag) is True,'map approval required:'+flag)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','source_bound_wrap_retention_proof']
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B200_layout_v2.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B200_profile.py'),'exact formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in keys[:6]]
    state=load(doc['postscene_native_state_proof']);actual=load(sample['actual_proof']);approval=load(conf['native_approval'])
    require(len(native['cases'])==19 and native['current_original_macro_alignment_calls']==152 and native['complete_progressive_planes']==17
        and native['complete_FE_logical_and_physical_planes']==2 and len(native['negative_controls'])==18
        and all(r['rejected'] for r in native['negative_controls']),'complete native consumers required')
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28,'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==19 and stored['current_final_stored_macro_alignment_cases']==76
        and stored['new_parity_macro_alignment_cases']==36 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
        and stored['all19_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored proof required')
    require(len(controls['relocated_dispatch_cases'])==19 and len(controls['all12_source_current_target_control_leaves'])==12
        and len(controls['picture_and_short47xx_pairs'])==2 and controls['no_FI_FA_FO_inherited']
        and controls['all17_progressive_and_two_distinct_null_actor_FE_objects_preserved'],'relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',926),('research',824)],'complete guarded end required')
    expected_names={'19':'Carlo Sinat','172':'Collapsed Person'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected_names,'current name values differ;Stranger target remains separate')
    name_cases=names['native_four_consumer_cases']['rows']
    require(len(name_cases)==4 and {(r['actor_ID'],r['consumer']) for r in name_cases}=={(i,c) for i in [19,172] for c in ['progressive-nameplate','full-catalogue']}
        and all(r['text']==expected_names[str(r['actor_ID'])] and r['all_actor_models_and_unowned4MiB_exact'] for r in name_cases),'four complete current name consumers required')
    voices=load(doc['actor_voice_contract']);terms=load(doc['actor_terminology_reconciliation'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={19:7,172:0},'source voices differ')
    require(terms['approved_prose_names']=={'19':'Carlo','172':'Stranger'} and terms['source_FE_impact_index']==5 and terms['source_FE_stat_notice_index']==72
        and terms['source_FI_FA_FO_counts']=={'FI':0,'FA':0,'FO':0},'source names/FE roles differ')
    draft=terms['actor172_label_localization_draft']
    require(draft['current']=='Collapsed Person' and draft['proposed']=='Stranger' and draft['source']=='行き倒れ'
        and draft['source_secondary_field']=='アフリカ水夫' and draft['secondary_field_retained_as_evidence_not_silently_promoted_to_player_label']
        and draft['target_not_encoded_or_applied'] and draft['new_name_completion_credit']==0,'anonymous label target scope differs')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no transferred weak-boundary exceptions')
    wrap=load(doc['source_bound_wrap_retention_proof'])
    require(wrap['all19_prose_wordings_controls_metrics_guards_phase_and_four_row_limits_unchanged']
        and wrap['protected_pairs']==[['still','you'],['take','care'],['care','of'],['please','accept'],['accept','it']],'complete request/courtesy phrase planning required')
    require(len(approval['six_individual_rowcount_reasons'])==6 and approval['stale_rowcount_waiver_removed']==['DK4_MES_B200_R0065'],'individual source-rowcount reasons required')
    require(not actual['failures'] and not actual['paired_region_differences'] and actual['actual_unique_speech_panels']==actual['complete_matching_observations']==19
        and actual['complete_matching_holds']==73 and actual['offline_only_source_indices']==[],'19 actual panels/73 holds required')
    require(len(actual['actual_panels'])==19 and [p['id'] for p in actual['actual_panels']]==mapping['actual_sampled_display_IDs']
        and sum(len(p['holds']) for p in actual['actual_panels'])==73,'individual actual panels/holds required')
    for panel,row in zip(actual['actual_panels'],doc['records'],strict=True):
        require(panel['id']==row['id'] and panel['prefix']==row['source_selector'] and panel['holds']
            and panel['native_plane_sha256']==row['native_font_case']['whole_native_plane_sha256'],'actual panel identity/native plane differs')
        for hold in panel['holds']:
            require(hold['complete_ink_gray_masks_equal_native_plane'] and hold['upper_portrait_name_and_item_regions_equal_source']
                and sha(Path(hold['capture']).read_bytes())==hold['capture_sha256']
                and sha(Path(hold['clean_capture']).read_bytes())==hold['clean_capture_sha256'],'complete source-paired actual capture required')
    require([len(v['command_pairs']) for v in actual['versions']]==[40,40] and [v['fixture_exit_frame'] for v in actual['versions']]==[7676,7677]
        and actual['versions'][0]['input_schedule_sha256']==actual['versions'][1]['input_schedule_sha256'],'actual paths/inputs/return differ')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1]),'actual command results differ')
    expected_ids=[(r['id'],r['source_record_index'],r['source_selector']) for r in doc['records']]
    expected_source_offsets=[None]*9+[r['old_offset'] for r in mapping['blocks'][0]['command_map']]
    for version in actual['versions']:
        require([(r['id'],r['source_record_index'],r['prefix']) for r in version['selected_intervals']]==expected_ids,'individual actual source identity differs')
        require([r['source_offset'] for r in version['command_pairs']]==expected_source_offsets,'complete actual source-command identity differs')
        report=load(version['capture_report'])
        require(report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==13001,'cold-boot scope differs')
        for photo in report['frames_captured']:require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'sampled capture hash differs')
    timed=[dict(source=a,English=b) for a,b in zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'],strict=True) if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    require(actual['actual_timing_differences']==timed and len(timed)==19 and len(actual['later_whole_RGB_differences'])==16,'measured differences must remain explicit')
    require(state['actual_proof_sha256']==sample['actual_proof_sha256']==sha(Path(sample['actual_proof']).read_bytes()),'actual proof binding differs')
    duration_changes=[dict(source_offset=a['source_offset'],word=a['word'],source_duration=a['returned']-a['start'],English_duration=b['returned']-b['start'],
        duration_delta=b['returned']-b['start']-a['returned']+a['start']) for a,b in zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'],strict=True)
        if a['returned']-a['start']!=b['returned']-b['start']]
    require(duration_changes==state['actual_command_duration_changes'] and len(duration_changes)==8
        and [r['duration_delta'] for r in duration_changes]==[-1,4,-1,-1,-4,5,-4,3] and all(r['word']==0x4000 for r in duration_changes),
        'all opaque-control durations must remain exact;measured speech differences required')
    require(state['native_final_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and state['native_final_component_values'][0]==state['native_final_component_values'][1],'queried final native outcomes differ')
    require(state['final_PRNG_seeds_equal'] is False and sample['PRNG_seeds_differ']
        and sample['final_13001_PRNG_seeds']==state['final_13001_PRNG_seeds'] and len(set(state['final_13001_PRNG_seeds']))==2
        and state['complete_RNG_timing_cause_not_traced'] and sample['native_cloud_object_and_complete_RNG_timing_cause_not_traced']
        and state['no_full_RAM_future_random_sequence_or_broad_world_equivalence_claim'],'honest measured RNG scope required')
    require(state['later_whole_RGB_differences_unmodified']==actual['later_whole_RGB_differences'] and state['no_pixels_masked_retimed_or_edited'],'unmodified later differences required')
    prompt=[];sky=[]
    for diff in actual['later_whole_RGB_differences']:
        if diff['nontext_region_difference_bbox'] is None:
            require(diff['difference_bbox'][0:3:2]==[224,240] and diff['difference_bbox'][1]==360 and diff['difference_bbox'][3]<=376,'advance-prompt difference bounds differ');prompt.append(diff)
        else:
            require(diff['difference_bbox']==diff['nontext_region_difference_bbox']==[137,192,191,243] and diff['frame']>=12490,'following sky difference bounds differ');sky.append(diff)
    require(len(prompt)==6 and len(sky)==10 and sample['following_sailing_cloud_position_difference_not_masked_or_retimed'],'explicit prompt and sky samples required')
    require(sample['sampled_nontext_frames']==len(actual['all_sampled_frame_comparisons'])==182 and sample['nontext_equal_samples']==172
        and sum(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])==172
        and [r for r in actual['all_sampled_frame_comparisons'] if r['nontext_region_difference_bbox'] is not None]==sky
        and sample['all19_actual_native_panels73_complete_holds_and_changed_scene_source_regions_match']
        and sample['all31_source_commands_plus9_initializers_stored_and40_observed_without_omission']
        and sample['original_inn_transition_picture47xx6003_two_A000_final4640_and_complete_end_results_preserved']
        and sample['six_prompt_blink_samples_and_ten_following_sailing_cloud_samples_visually_reviewed']
        and sample['no_open_translation_specific_display_or_control_finding'] and sample['representative_shared_rules_approved'],'complete representative scene evidence required')
    views=sample['four_actual_and_six_paired_sheets_viewed']
    require(len(views)==10 and all(r['viewed_in_full_current_turn'] and r['viewed_after_image_return'] and r['original_detail']
        and sha(Path(r['path']).read_bytes())==r['sha256'] for r in views),'viewed actual and paired screens required')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets']
        and all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['reviewed_sheets']),'native screen approvals differ')
    require(not any(p.get('full_goal_complete') for p in [doc,mapping,seal,native,stored,controls,sample,state,approval]),'full editorial goal remains incomplete')
'''
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B199_editorial_v3.py').read_text(encoding='utf-8')
    a=source.index("    doc,mapping,seal=");b=source.index("    rows=doc['records']",a)
    e=source.index("        if row['source_record_index']==58:");f=source.index("        old_prose=",e)
    g=source.index("        if row['source_record_index']==70:");h=source.index('        value=encoded.encoded;',g)
    flagline=next(l for l in source.splitlines() if l.startswith('FLAGS='));termline=next(l for l in source.splitlines() if l.startswith('TERM_FLAGS='))
    exactline=next(l for l in source.splitlines() if l.startswith('    exact='))
    changes={source[a:b]:GATES,source[e:f]:"        require(row['registered_runtime_catalog_entry'] is None,'no current B200 runtime override belongs here')\n",
        source[g:h]:"        require(not logical_prose.startswith('(') and not logical_prose.endswith(')'),'no private thought objects belong to B200')\n",
        flagline:'FLAGS='+repr(FLAGS),termline:'TERM_FLAGS='+repr(TERM_FLAGS),
        exactline:"    exact=[(8,'2d63'),(94,'0143'),(96,'00460b80'),(100,'8143'),(618,'304865a8'),(718,'3547'),(864,'0360'),(866,'2e63'),(906,'00a0ffff01021360'),(914,'00a0ffff01006530'),(922,'4046081d'),(926,'00000000')]",
        'B199':'B200','lil_B199_layout_v3':'lil_B200_layout_v2','SELECTORS={2,9,22,254}':'SELECTORS={19,172,254}',
        "len(rows)==len(set(ids))==31":"len(rows)==len(set(ids))==19",
        "{'progressive':30,'system-FE':1}":"{'progressive':17,'system-FE':2}","{'revise':11,'retain-wording':20}":"{'revise':13,'retain-wording':6}",
        'exact31':'exact19','all31 actual':'all19 actual',
        "catalog['all467_rows_complete_keys_targets_route_masks_and_current_calls_verified'] and len(catalog['records'])==467":
        "catalog['all467_rows_complete_keys_targets_route_masks_and_current_calls_verified'] and len(catalog['records'])==467 and all(c['registered_catalog_match'] is None for c in original_dispatch['speech_dispatch_cases'])",
        "['block']==199":"['block']==200",'old_blocks[199]':'old_blocks[200]','blocks[199]':'blocks[200]','block=199':'block=200','==[199]':'==[200]',
        "spec['source_bytes']==len(block)==1168 and spec['source_logical_end']==1166 and spec['research_bytes']==1116 and spec['research_logical_end']==1114":
        "spec['source_bytes']==len(block)==932 and spec['source_logical_end']==930 and spec['research_bytes']==828 and spec['research_logical_end']==828",
        "require(macros==Counter({b'FI':1}),'exactly one source FI required')":"require(not macros,'B200 has no source FI/FA/FO')",
        "spec['original2000_pause_and_resume_maps']==[dict(old_offset=56,new_offset=66,source_resume=58,target_resume=68,source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]":
        "not spec['original2000_pause_and_resume_maps']",
        "end==1166 and len(block)==1168":"end==930 and len(block)==932",'mapped(end)==1114':'mapped(end)==828',
        "len(target)==1116 and target[1114:]==bytes(2)":"len(target)==828 and len(logical)==828",
        "len(commands)==47 and sum(c['word']==0x4000 for c in commands)==31":"len(commands)==31 and sum(c['word']==0x4000 for c in commands)==19",
        '[(1162,1110)]':'[(926,824)]','16 exact leaves':'12 exact leaves',
        '[0x4631,0x0505,0x2000,0x632D,0x4621,0x630B,0x632A,0x0503,0x4821,0x4735,0x632B,0x4630,0x4895,0xA000,0x4720,0]':
        '[0x632D,0x4301,0x4600,0x4381,0x4830,0x4735,0x6003,0x632E,0xA000,0xA000,0x4640,0]',
        'source_commands=47':'source_commands=31',
        'all31_progressive_FE_speeches_one_FI_pause_pictures47xx_A000_and_single_end_preserved':
        'all19_progressive_two_FE_no_macros_inn_picture47xx6003_two_A000_and_single_end_preserved',
        'actual_two_complete_B22_fixtures31_panels182_regions120_holds34_timings6_prompt_differences_unequal_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures19_panels73_holds172_equal_regions19_timings6_prompt10_sky_differences_unequal_PRNG_not_natural_activation'}
    tool=derive('dk4tool/patch/lil_B199_editorial_v3.py','dk4tool/patch/lil_B200_editorial_v1.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler_prepared.json',dict(tool=tool,
        reconstructs_all19_approved_targets_before_single_image_mutation=True,source_current_native_reference_actual_scope_and_full_goal_flags_bound=True,
        all_existing_compilers_profiles_and_ROMs_preserved=True,no_new_ROM_registry_or_review_credit=True,full_goal_complete=False))
    print('B200 atomic compiler prepared with complete source/native/actual guards and measured later cloud scope;single mutation after validation.')
