"""Freeze B199's atomic compiler with complete source, runtime and measured scene guards."""
from pathlib import Path
from scripts.lil_B199_compiler_data_derivation_v5812b import derive_with_reviewed_data as derive
from scripts.seal_lil_B199_references_v5809 import FLAGS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_compiler_tools_v5812b')
GATES='''    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all31_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged']
        and seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes())
        and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed references differ')
    require(mapping['format']=='dk4-lil-B199-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    require(conf['required_map_flags']==FLAGS and conf['required_term_flags']==TERM_FLAGS,'complete required flags differ')
    for flag in FLAGS:require(mapping.get(flag) is True,'map approval required:'+flag)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','source_bound_wrap_retention_proof']
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B199_layout_v3.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B199_profile.py'),'exact formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in keys[:6]]
    state=load(doc['postscene_native_state_proof']);actual=load(sample['actual_proof']);approval=load(conf['native_approval'])
    require(len(native['cases'])==31 and native['current_original_macro_alignment_calls']==248 and native['complete_progressive_planes']==30
        and native['complete_FE_logical_and_physical_planes']==1 and len(native['negative_controls'])==22
        and all(r['rejected'] for r in native['negative_controls']),'complete native consumers required')
    require(len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28,'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==31 and stored['current_final_stored_macro_alignment_cases']==124
        and stored['new_parity_macro_alignment_cases']==52 and stored['exact_byte_identical_reused_macro_alignment_cases']==72
        and stored['all31_final_targets_complete_native_planes_equal_reviewed_planes'],'final stored proof required')
    require(len(controls['relocated_dispatch_cases'])==31 and len(controls['all16_source_current_target_control_leaves'])==16
        and len(controls['picture_and_short47xx_pairs'])==4 and controls['one_FI_no_FA_FO_preserved'],'relocated controls required')
    require(controls['one_source_pause_and_resume_map']==dict(old_offset=56,new_offset=66,source_resume=58,target_resume=68,
        source_two_byte_pause_and_mapped_resumption_boundary_exact=True),'original pause/resume required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',1162),('research',1110)],'complete guarded end required')
    require(names['progressive_nameplate_values']=={'2':'Lil Argot','9':'Camille Overijssel','22':'Samwell Khan'}
        and names['full_catalogue_values']=={'2':'Lil Argot','9':'Camille Marinus Overijssel','22':'Samwell ダ Khan'}
        and len(names['native_six_consumer_cases']['rows'])==6,'six original name consumers required;Samwell finding stays separate')
    voices=load(doc['actor_voice_contract']);terms=load(doc['actor_terminology_reconciliation'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}=={2:3,9:2,22:2},'source voices differ')
    require(terms['approved_prose_names']=={'2':'Lil','9':'Camille','22':'Samwell'} and terms['private_parentheses_source_indices']==[70,115]
        and terms['portrait_subject_name']['Japanese']=='ロッコ＝アレムケル' and terms['portrait_subject_name']['project_English']=='Rocco Alemkel','source names/context differ')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no transferred weak-boundary exceptions')
    wrap=load(doc['source_bound_wrap_retention_proof'])
    require(wrap['source70_full_idiom_protected_without_new_word_or_manual_break'] and wrap['all_other_native_metrics_and_prose_and_runtime_preserved']
        and wrap['R95_complete_first_candidate_characters']==36 and wrap['R95_no_word_shortened_and_no_width_guard_phase_or_four_row_limit_changed'],
        'complete idiom and three-row thought required')
    require(not actual['failures'] and not actual['paired_region_differences'] and actual['actual_unique_speech_panels']==actual['complete_matching_observations']==31
        and actual['complete_matching_holds']==120 and actual['offline_only_source_indices']==[],'31 actual panels/120 holds required')
    require([len(v['command_pairs']) for v in actual['versions']]==[56,56] and [v['fixture_exit_frame'] for v in actual['versions']]==[10776,10778]
        and actual['versions'][0]['input_schedule_sha256']==actual['versions'][1]['input_schedule_sha256'],'actual paths/inputs/return differ')
    shape=lambda v:[(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    require(shape(actual['versions'][0])==shape(actual['versions'][1]),'actual command results differ')
    require(len(actual['actual_timing_differences'])==34 and len(actual['later_whole_RGB_differences'])==6,'measured differences must remain explicit')
    require(state['actual_proof_sha256']==sample['actual_proof_sha256']==sha(Path(sample['actual_proof']).read_bytes()),'actual proof binding differs')
    duration_changes=[dict(source_offset=a['source_offset'],word=a['word'],source_duration=a['returned']-a['start'],English_duration=b['returned']-b['start'],
        duration_delta=b['returned']-b['start']-a['returned']+a['start']) for a,b in zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'])
        if a['returned']-a['start']!=b['returned']-b['start']]
    require(duration_changes==state['six_actual_speech_duration_changes'] and len(duration_changes)==6
        and [r['duration_delta'] for r in duration_changes]==[3,-4,3,-1,-4,5] and all(r['word']==0x4000 for r in duration_changes),
        'all opaque-control durations must remain exact;measured speech differences required')
    require(state['native_final_component_equality']==dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True)
        and state['native_final_component_values'][0]==state['native_final_component_values'][1],'queried final native outcomes differ')
    require(state['final_PRNG_seeds_equal'] is False and sample['PRNG_seeds_differ']
        and sample['final_13001_PRNG_seeds']==state['final_13001_PRNG_seeds'] and len(set(state['final_13001_PRNG_seeds']))==2
        and state['PRNG_difference_preserved_not_removed_or_reseeded'] and state['complete_RNG_timing_cause_not_traced']
        and state['no_full_RAM_future_random_sequence_or_broad_world_equivalence_claim'],'honest measured RNG scope required')
    require(state['later_whole_RGB_differences_unmodified']==actual['later_whole_RGB_differences']
        and all(r['nontext_region_difference_bbox'] is None and 224<=r['difference_bbox'][0]<=r['difference_bbox'][2]<=240
            and 360<=r['difference_bbox'][1]<=r['difference_bbox'][3]<=376 for r in actual['later_whole_RGB_differences'])
        and state['no_pixels_masked_retimed_or_edited'],'unmodified prompt-region differences required')
    require(sample['sampled_nontext_frames']==len(actual['all_sampled_frame_comparisons'])==182
        and all(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])
        and sample['all31_actual_native_panels120_complete_holds_and_all182_sampled_nontext_regions_match']
        and sample['all47_source_commands_plus9_initializers_stored_and56_observed_without_omission']
        and sample['original_pause_two_picture_layouts_short47xx_A000_and_complete_end_results_preserved']
        and sample['six_later_differences_visually_confirmed_advance_prompt_blink'] and sample['no_open_translation_specific_display_or_control_finding']
        and sample['representative_shared_rules_approved'],'complete representative scene evidence required')
    views=sample['six_actual_and_six_paired_sheets_viewed']
    require(len(views)==12 and all(r['viewed_in_full_current_turn'] and r['viewed_after_image_return'] and r['original_detail']
        and sha(Path(r['path']).read_bytes())==r['sha256'] for r in views),'viewed actual and paired screens required')
    require([{k:s[k] for k in ['path','sha256']} for s in approval['reviewed_sheets']]==native['review_sheets']
        and all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['reviewed_sheets']),
        'prior native screen approvals differ')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==31 and {r['source_selector'] for r in rows}==SELECTORS
        and Counter(r['kind'] for r in rows)=={'progressive':30,'system-FE':1}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':11,'retain-wording':20},'exact31 decisions/consumers required')
    require(all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']) and sample['actual_sampled_display_IDs']==ids
        and mapping['actual_sampled_display_IDs']==ids and sample['offline_only_display_IDs']==mapping['offline_only_display_IDs']==[],
        'all31 actual display IDs required')
    original_dispatch=load(doc['control_contract']);catalog=load(original_dispatch['registered_catalog_binding'])
    require(catalog['all467_rows_complete_keys_targets_route_masks_and_current_calls_verified'] and len(catalog['records'])==467,'complete current name catalog binding required')
'''
QA='''        require(row.get('qa_waivers') in [None,['line-break-count']],'no additional safety waiver')
        require(row['native_font_case']==case,'approved native reference differs:'+ident)
        effective=old[1:]
        if row['source_record_index']==58:
            entry=catalog['records'][305]
            require(entry['key_hex']==effective.hex() and entry['route_mask']==4
                and entry['requests']==[dict(owner=[PATH,ident],form='body')] and row['registered_runtime_catalog_entry']==entry,
                'exact existing R58 runtime override required')
            effective=bytes.fromhex(entry['target_hex'])
        old_prose=' '.join(effective.decode('cp932').split())
        logical_prose=row['english'].split('}',1)[1]
        for macro in ['FI','FA','FO']:logical_prose=logical_prose.replace('{MACRO:'+macro+'}',macro)
        require(row['effective_predecessor_paragraph']==old_prose,'effective predecessor differs:'+ident)
        require((logical_prose!=old_prose)==(row['editorial_decision']=='revise'),'revision/retention decision differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row.get('fresh_retained_wording_justification'),'individual retention reason required')
        if row['source_record_index']==70:require(qa['visible_lines']==['(Got away again.',"Samwell's quick on his feet.)"] and row.get('native_layout_retention_reason'),'complete private idiom required')
        if row['source_record_index']==95:require(qa['visible_lines']==['It looks old,',"but it's not every day",'I get a present from you, Camille!'] and row.get('native_layout_retention_reason'),'complete gift response required')
        require(logical_prose.startswith('(')==(row['source_record_index'] in [70,115]) and logical_prose.endswith(')')==(row['source_record_index'] in [70,115]),'private thoughts must stay private')
'''
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/lil_B195_editorial_v1.py').read_text(encoding='utf-8')
    a=source.index('    doc,mapping=');b=source.index("    require(len(mapping['blocks'])",a)
    q=source.index('        value=encoded.encoded;')
    terms=read('work/analysis/lil_B199_comparison_v5783b/complete_clean_context_actual_source_and_project_name_reconciliation.json')
    term_flags=[k for k,v in terms.items() if v is True and k!='no_new_ROM_or_run_beyond_the_already_recorded_source_fixture']
    cp=read('work/analysis/lil_B199_controls_v5778/sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json')
    leaves=[(c['offset'],c['whole_command_hex']) for c in cp['all16_source_current_nonspeech_leaves']]
    f0=source.index('FLAGS=');f1=source.index('\n\ndef load(',f0)
    oldret="        if row['editorial_decision']=='retain-wording':require(row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification'],'unjustified retention')\n"
    result=derive('dk4tool/patch/lil_B195_editorial_v1.py','dk4tool/patch/lil_B199_editorial_v1.py',{
        source[a:b]:GATES,source[f0:f1]:'FLAGS='+repr(FLAGS)+'\nTERM_FLAGS='+repr(term_flags),oldret:'',
        'B195':'B199','lil_B195_layout_v1':'lil_B199_layout_v3','SELECTORS={92,103,119,254}':'SELECTORS={2,9,22,254}',
        '[195]':'[199]','==195':'==199','block=195':'block=199',
        "spec['source_bytes']==len(block)==712 and spec['source_logical_end']==710 and spec['research_bytes']==spec['research_logical_end']==616":
        "spec['source_bytes']==len(block)==1168 and spec['source_logical_end']==1166 and spec['research_bytes']==1116 and spec['research_logical_end']==1114",
        '        value=encoded.encoded;':QA+'        value=encoded.encoded;',
        "require(not macros,'source has no FI/FA/FO substitutions')":"require(macros==Counter({b'FI':1}),'exactly one source FI required')",
        "not spec['original2000_pause_and_resume_maps']":"spec['original2000_pause_and_resume_maps']==[dict(old_offset=56,new_offset=66,source_resume=58,target_resume=68,source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]",
        'end==710 and len(block)==712':'end==1166 and len(block)==1168','len(logical)==mapped(end)==616':'len(logical)==mapped(end)==1114',
        'len(target)==616 and target[616:]==bytes()':'len(target)==1116 and target[1114:]==bytes(2)',
        'len(commands)==23':'len(commands)==47',"sum(c['word']==0x4000 for c in commands)==20":"sum(c['word']==0x4000 for c in commands)==31",
        '[(706,612)]':'[(1162,1110)]',"exact=[(8,'00a0ffff010841a1'),(704,'00c2'),(706,'00000000')]":'exact='+repr(leaves),
        "[c['word'] for c in leaves]==[0xA000,0xC200,0]":"[c['word'] for c in leaves]==[0x4631,0x0505,0x2000,0x632D,0x4621,0x630B,0x632A,0x0503,0x4821,0x4735,0x632B,0x4630,0x4895,0xA000,0x4720,0]",
        'three exact leaves required':'16 exact leaves required','source_commands=23':'source_commands=47',
        'all20_progressive_FE_speeches_no_macros_A000_C200_and_single_end_preserved':'all31_progressive_FE_speeches_one_FI_pause_pictures47xx_A000_and_single_end_preserved',
        'actual_two_complete_B22_fixtures_three_roles_115_regions_79_holds_15_timings4_lower_indicator_differences_unequal_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures31_panels182_regions120_holds34_timings6_prompt_differences_unequal_PRNG_not_natural_activation'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler.json',dict(tool=result,required_map_flags=FLAGS,required_term_flags=term_flags,
        all_source_current_preambles_control_bytes_boundaries_inverse_and_sole_mutation_guards_retained=True,
        one_FI_pause_two_pictures_two47xx_effective_R58_and_actual_measured_limits_required=True,
        positive_reconstruction_and_semantic_negatives_still_required=True,new_review_credit=0,full_goal_complete=False))
    print('B199 atomic compiler prepared:31 targets,47 commands,16 exact leaves,one FI/pause and complete inverse. Semantic validation next.')
