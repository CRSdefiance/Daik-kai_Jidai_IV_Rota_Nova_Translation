"""Freeze an atomic B198 compiler retaining complete source/control/inverse ownership guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.seal_lil_B198_references_v5746 import FLAGS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_compiler_tools_v5752')
GATES='''    doc,mapping,seal=[load(conf[k]) for k in ['manuscript','reference_map','reference_approval']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and not doc['formatting_review_pending']
        and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'approved map differs')
    require(seal['all17_source_native_reference_and_representative_rules_approved'] and seal['source_prose_English_and_compiled_targets_unchanged'],'source/reference approval required')
    require(seal['manuscript']==conf['manuscript'] and seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()),'sealed manuscript changed')
    require(seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed reference map changed')
    require(mapping['format']=='dk4-lil-B198-source-relocation-map-v1' and mapping['external_references_complete'] and mapping['entry_point_offset']==8
        and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete map required')
    require(conf['required_map_flags']==FLAGS,'complete map requirements required')
    for name in FLAGS:require(mapping.get(name) is True,'required source shape:'+name)
    keys=['native_font_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','representative_proof',
        'postscene_native_state_proof','source_bound_wrap_retention_proof','source_original_progressive_style_proof']
    proofs={k:load(doc[k]) for k in keys}
    for k in keys:require(doc[k+'_sha256']==sha(Path(doc[k]).read_bytes()),'proof hash differs:'+k)
    native,stored,control,ends,sample,observed,wrap,style=[proofs[k] for k in keys]
    approval=load(conf['native_approval']);actual=load(observed['actual_proof'])
    require(len(native['cases'])==17 and native['current_original_macro_alignment_calls']==136 and native['complete_progressive_planes']==11
        and native['complete_FE_logical_and_physical_planes']==6 and len(native['negative_controls'])==18,'complete native consumers required')
    require(all(r['rejected'] for r in native['negative_controls']) and len(approval['formatter_negatives'])==28,'consumer/formatter negatives required')
    require(len(stored['final_target_parity_cases'])==17 and stored['current_final_stored_macro_alignment_cases']==68
        and stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
        and stored['all17_final_targets_complete_native_planes_equal_reviewed_planes'],'stored speech proof required')
    require(native['source_original_progressive_caller_style']==stored['source_original_progressive_caller_style']==11
        and style['source_explicit_style']==11 and style['source_context_style_field']==0x30
        and len(style['cases'])==3 and all(c['exact_actual_ink'] and c['exact_actual_gray']
            and all(e['style']==11 for e in c['native_events']) for c in style['cases']),'original story style11 required')
    require(native['source_original_progressive_style_proof']==stored['source_original_progressive_style_proof']==doc['source_original_progressive_style_proof']
        and native['source_original_progressive_style_proof_sha256']==stored['source_original_progressive_style_proof_sha256']==doc['source_original_progressive_style_proof_sha256'],
        'source-correct native style proof required')
    require(len(control['relocated_dispatch_cases'])==17 and len(control['all12_source_current_target_control_leaves'])==12
        and len(control['original_unforced_predicate_pairs'])==2 and len(control['original4835_picture_pair'])==1,'relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['no_relative_destination_at_or_beyond_logical_end']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',540),('research',640)],'guarded original ending required')
    require(not actual['failures'] and not actual['paired_region_differences'] and not actual['actual_timing_differences']
        and not actual['later_whole_RGB_differences'] and actual['same_observed_source_path_original_results_predicates_and_end540'],
        'source/English display and control results differ')
    require(len(actual['actual_panels'])==actual['complete_matching_observations']==15 and actual['complete_matching_holds']==56
        and actual['offline_only_source_indices']==[65,95],'actual/offline scope differs')
    require([len(v['command_pairs']) for v in actual['versions']]==[40,40]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[6697,6697]
        and all(len(v['selected_intervals'])==15 for v in actual['versions']),'source path/return scope differs')
    require(sample['fifteen_actual_native_panels56_holds_and_two_offline_conditionals_explicit']
        and sample['all37_source_commands_plus9_initializers_stored_without_omission']
        and sample['source_story_style11_binds_complete_CP932_pause_planes_without_ROM_change']
        and sample['original_predicate_results_and_single_source540_target640_end_and_return_preserved']
        and sample['representative_shared_rules_approved'] and sample['no_open_translation_specific_display_or_control_finding'],
        'representative display/control approval required')
    require(sample['sampled_nontext_frames']==observed['sampled_nontext_frames']==len(actual['all_sampled_frame_comparisons'])==182
        and all(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])
        and sample['source_and_English_return_frames']==observed['source_and_English_return_frames']==[6697,6697]
        and sample['command_timing_difference_count']==observed['command_timing_difference_count']==0
        and sample['later_sampled_whole_RGB_difference_count']==observed['later_sampled_whole_RGB_difference_count']==0,
        'measured scene scope differs')
    require(sample['final_13001_PRNG_seeds']==observed['final_13001_PRNG_seeds'] and len(set(observed['final_13001_PRNG_seeds']))==1
        and sample['no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim']
        and observed['no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim'],'honest postscene scope required')
    require(observed['all17_native_glyphs_complete_15_actual_panels56_complete_holds_match']
        and observed['source_story_caller_style11_CP932_pause_reference_corrected_without_ROM_or_prose_change']
        and observed['source_matched_name_portrait_item_and_background_visibility_not_normalized']
        and observed['no_open_changed_scene_translation_display_or_control_finding'],'viewed actual approval required')
    views=observed['all_current_native_sheets_viewed']+observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views']
    require(len(views)==9 and all(s['viewed_in_full_current_turn'] and s['viewed_after_image_return'] and s['original_detail']
        and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views),'viewed screens changed')
    require(observed['actual_source_English_cold_boots']==2 and observed['new_English_runs']==1 and observed['total_successful_frames']==26002
        and observed['original_source_run_reused_not_a_new_run'] and observed['offline_only_source_indices']==[65,95],
        'run counts and conditional limits required')
    terms=load(doc['actor_terminology_reconciliation']);voices=load(doc['actor_voice_contract']);names=load(doc['source_nameplate_consumer_proof'])
    require(terms['approved_prose_names']=={'12':'Yukihisa Shiraki','15':'Angelo Puccini'},'approved names differ')
    require(conf['required_term_flags']==TERM_FLAGS,'complete source-context requirements required')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'source context required:'+flag)
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={12:1,15:4},'two source voices differ')
    require(names['progressive_nameplate_values']=={'12':'Yukihisa Shiraki','15':'Angelo Puccini'}
        and names['full_catalogue_values']=={'12':'Yukihisa Genjo Shiraki','15':'Angelo Puccini'}
        and len(names['native_four_consumer_cases']['rows'])==4,'source-bound name consumers required')
    require(wrap['exact_source_indices']==[10,14] and wrap['phrase_protection']==['any','naughty']
        and wrap['all_words_native_metrics_width_guard_phase_bounds_pagination_and_runtime_unchanged']
        and wrap['no_authored_line_break_or_exact_row_override'],'complete repeated-call phrase grouping required')
    rows=doc['records'];ids={r['id'] for r in rows}
    require(len(rows)==len(ids)==17,'17 unique objects required')
    require({r['source_selector'] for r in rows}==SELECTORS and Counter(r['kind'] for r in rows)=={'progressive':11,'system-FE':6},'speaker/consumer scope differs')
    require(Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':5}
        and all(r.get('fresh_retained_wording_justification') for r in rows if r['editorial_decision']=='retain-wording'),'individual decisions required')
    observed_ids=set(mapping['actual_sampled_display_IDs']);offline=set(mapping['offline_only_display_IDs'])
    require(len(observed_ids)==15 and offline=={'DK4_MES_B198_R0065','DK4_MES_B198_R0095'} and not observed_ids&offline and observed_ids|offline==ids
        and observed_ids=={r['id'] for r in actual['actual_panels']}
        and observed_ids==set(sample['actual_sampled_display_IDs'])==set(observed['actual_sampled_display_IDs'])
        and offline==set(sample['offline_only_display_IDs']),'actual/offline ownership differs')
'''
QA='''        require(row.get('qa_waivers') in [None,['line-break-count']],'unapproved safety waiver')
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning'
            and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        if row['source_record_index'] in [10,14]:
            require(qa['visible_lines']==['Any naughty children here?','Any naughty children here?']
                and row.get('native_layout_retention_reason'),'complete repeated call rows required')
        require(row['native_font_case']==case,'source-correct native reference differs:'+ident)
        old_prose=' '.join(old[1:].decode('cp932').split())
        require(row['effective_predecessor_paragraph']==old_prose,'predecessor prose differs:'+ident)
        require((row['english'].split('}',1)[1]!=old_prose)==(row['editorial_decision']=='revise'),'revision/retention differs:'+ident)
'''
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/lil_B197_editorial_v1.py').read_text(encoding='utf-8')
    g0=source.index('    doc,menu,mapping,seal=');g1=source.index("    require(len(mapping['blocks'])",g0)
    q0=source.index("        if row['source_record_index']==74:");q1=source.index('        value=encoded.encoded;',q0)
    m0=source.index("    for command in spec['choice_commands']:");m1=source.index('    patches.sort(',m0)
    terms=read('work/analysis/lil_B198_context_v5715/clean_first_context_Namahage_dream_and_original_unforced_path.json')
    term_flags=[k for k,v in terms.items() if v is True]
    tool=derive('dk4tool/patch/lil_B197_editorial_v1.py','dk4tool/patch/lil_B198_editorial_v1.py',{
        source[g0:g1]:GATES,source[q0:q1]:QA,source[m0:m1]:'',
        'B197':'B198','lil_B197_layout_v1':'lil_B198_layout_v2',
        'SELECTORS={21,169,254}':'SELECTORS={12,15,254}',
        'MENUS=[230]':'MENUS=[]\nFLAGS='+repr(FLAGS)+'\nTERM_FLAGS='+repr(term_flags),
        'END_MAP=[(874,998)]':'END_MAP=[(540,640)]',"['block']==197":"['block']==198",'oldblocks[197]':'oldblocks[198]',
        'blocks[197]':'blocks[198]','==(880,878,1004,1002) and len(block)==880':'==(544,544,644,644) and len(block)==544',
        "row['block']==row['source_reference']['block']==197":"row['block']==row['source_reference']['block']==198",'block=197':'block=198',
        'len(patches)==22':'len(patches)==17','end==878 and block[end:]==bytes(2)':'end==544 and block[end:]==bytes(0)',
        "len(edges)==6 and len(spec['target_native_skip_cases'])==30 and len(logical)==mapped(end)==1002":
        "len(edges)==8 and len(spec['target_native_skip_cases'])==40 and len(logical)==mapped(end)==644",
        'len(target)==1004':'len(target)==644',
        'Counter({0x4000:21,0x2200:1,0xA000:5,0x4821:1,0x4720:1,0x4735:1,0x632E:1,0x6003:1,0:1,0x100:3,0x200:1,0x300:1,0x400:1})':
        'Counter({0x4000:17,0x6000:1,0x4500:1,0x633F:1,0xA000:2,0x623F:1,0x4621:1,0x61FF:1,0x8000:2,0x4835:1,0:1,0x100:4,0x200:2,0x300:2})',
        'all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves':'all12_source_current_target_control_leaves',
        'all11 original opaque leaves':'all12 original control leaves','every880 predecessor byte':'every544 predecessor byte',
        'newblocks[197]':'newblocks[198]','==[197]':'==[198]',"choices=conf['choices'],":'',
        'relative_operands=6,source_commands=39':'relative_operands=8,source_commands=37',
        'all24_reviewed_objects_three_labels_common_end_no_macros_and11_leaves_preserved':'all17_reviewed_objects_common_end_no_macros_and12_leaves_preserved',
        'actual21_speech_panels35_observations_three_options_common_end_not_natural_event_eligibility':'actual15_speech_panels56_holds_two_offline_conditionals_not_natural_event_eligibility',
        'speech, three-option and common-ending':'seventeen-speech and common-ending'})
    ROOT.mkdir(parents=True);save(ROOT/'atomic_source_locked_compiler_prepared.json',dict(tool=tool,required_map_flags=FLAGS,required_term_flags=term_flags,
        all_original_source_current_target_preambles_relative_spans_control_leaves_inverse_and_sole_mutation_guards_retained=True,
        source_story_style11_native_reference_and15_actual_two_offline_scope_required=True,
        no_prior_R74_wrap_exception_menu_or_financial_context_inherited=True,
        positive_reconstruction_and_semantic_negatives_before_mutation_still_required=True,new_review_credit=0,full_goal_complete=False))
    print('B198 atomic compiler prepared:17 speeches,37 commands,eight spans,12 control leaves,exact inverse and sole mutation. Positive/negative validation next.')
