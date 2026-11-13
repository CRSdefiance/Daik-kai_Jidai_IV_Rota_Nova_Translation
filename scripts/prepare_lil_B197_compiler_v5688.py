"""Derive atomic B197 integration from the guarded final typed-reference compiler."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_compiler_tools_v5688')
GATES='''    proofs={k:load(doc[k]) for k in ['native_font_proof','final_padding_proof','final_choice_proof','relocated_control_proof','termination_decode_proof','representative_proof','postscene_native_state_proof','source_bound_wrap_retention_proof']}
    native,stored,typed,control,ends,sample,observed,wrap=[proofs[k] for k in proofs]
    approval=load(conf['native_approval']);actual=load(observed['actual_proof'])
    require(len(native['cases'])==21 and native['current_original_macro_alignment_calls']==168 and native['complete_progressive_planes']==20
        and native['complete_FE_logical_and_physical_planes']==1 and len(native['negative_controls'])==18,'complete native consumers/negatives required')
    require(all(r['rejected'] for r in native['negative_controls']) and len(approval['formatter_negatives'])==28,'formatter/consumer negatives required')
    require(len(stored['final_target_parity_cases'])==21 and stored['current_final_stored_macro_alignment_cases']==84
        and stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==56
        and stored['all21_final_targets_complete_native_planes_equal_reviewed_planes'],'stored speech proof required')
    require(typed['source_count3_option_order_and_original_selection_cancel_results_preserved'] and len(typed['actual_target_record_references'])==3
        and typed['fresh_count_calls']==2 and typed['fresh_label_pointer_calls']==6 and typed['reused_native_selection_cancel_cases']==8
        and typed['reused_complete_current_reviewed_style_planes']==12,'stored menu proof required')
    require(len(control['relocated_dispatch_cases'])==21 and len(control['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==11
        and len(control['picture_and47xx_current_relocated_pairs'])==3 and control['original47xx_R3_is_exact_mapped_stream_instruction_pointer'],'relocated controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['no_relative_destination_at_or_beyond_logical_end'],'guarded common ending required')
    require(sample['actual_original_menu_indices']==[0,1,2] and sample['original_menu_offset']==230
        and sample['all_three_label_meanings_and_visible_selection_return_associations_verified'],'honest representative menu scope required')
    require(observed['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not observed['visual_review_pending']
        and observed['no_open_translation_specific_display_menu_control_or_return_finding']
        and observed['new_successful_English_runs']==4 and observed['new_successful_English_frames']==43604
        and observed['reused_prior_source_runs']==3 and observed['total_successful_frames']==82607,'viewed actual approval required')
    require(not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences'],'actual display/control differences changed')
    require(len(actual['actual_panels'])==21 and len(actual['all_actual_speech_observations'])==35 and len(actual['actual_menu_cases'])==3
        and actual['complete_native_holds']==128,'actual scope differs')
    require(len(actual['command_timing_differences'])==59 and len(actual['later_whole_RGB_differences'])==82
        and observed['paired_command_timing_differences']==actual['command_timing_differences'] and observed['postscene_whole_RGB_differences']==actual['later_whole_RGB_differences']
        and observed['broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks']
        and observed['no_causal_explanation_of_timing_RNG_or_world_differences_certified'],'honest difference accounting required')
    require(observed['source_matched_blank_portrait_name_additional_records']==[64,89]
        and observed['all128_complete_native_holds_match_source_upper_portrait_name_and_picture_regions'],'source display baseline required')
    require(observed['all_three_actual_indices0_1_2_complete_labels_and_visible_highlights_verified']
        and observed['initial_menu_sampling_failure_resolved_by16_new_complete_active_highlight_holds_without_retiming'],'visible menu evidence required')
    views=observed['all_actual_consumer_menu_sheets_viewed']+observed['paired_full_screen_views']
    require(len(views)==9 and all(s['viewed'] and s['viewed_after_image_return'] and s['original_detail'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in views),'viewed screens changed')
    require(len(observed['paired_final_state_measurements'])==3 and observed['no_buy_five_native_groups_actor_captain_and_PRNG_equal']
        and observed['buy_delegate_models_persistent_objects_actor_and_PRNG_differ_buy_calendar_group_also_differs'],'measured state scope differs')
    terms=load(doc['actor_terminology_reconciliation']);funds=load(doc['source_financial_context'])
    require(terms['money_term']=='gold' and terms['stat_term']['English']=='Charm' and terms['exact_native_payment_amount']==8500,'source terms differ')
    require(terms['approved_prose_names']=={'21':'Ian Dukov','169':'Alluring Woman'},'approved prose names differ')
    for flag in conf['required_term_flags']:require(terms.get(flag) is True,'source context required:'+flag)
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={21:1,169:0},'two source voices differ')
    require(funds['source8500_price_matches_exact_native_payment_amount'] and len(funds['cases'])==6,'exact8500 source price required')
    require(wrap['exact_record']=='DK4_MES_B197_R0074' and wrap['visible_rows']==["I'd like to buy it, but I don't",'have that kind of money.']
        and wrap['formatter_font_width_phase_guard_and_all_prose_bytes_unchanged'] and wrap['no_global_weak_word_waiver'],'exact R74 wrap proof required')
'''
QA='''        if row['source_record_index']==74:
            require(row['source_hex']==wrap['source_hex'] and row['english']==wrap['english'] and row['qa_waiver_reason']==wrap['reason']
                and qa['visible_lines']==row['exact_reviewed_soft_wrap_rows']==wrap['visible_rows'] and row.get('qa_waivers')==['weak-line-ending']
                and [i['code'] for i in qa['issues']]==['weak-line-ending'],'exact R74 ordinary soft wrap differs')
        else:
            require(row.get('qa_waivers') in [None,['line-break-count']],'waiver transferred outside exact record')
            require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
'''
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B196_editorial_v3.py');text=source.read_text(encoding='utf-8')
    start=text.index('    proofs={');stop=text.index('    rows,labels=',start)
    qa_start=text.index("        require(not [i for i in qa['issues']");qa_stop=text.index('        value=encoded.encoded;',qa_start)
    counts_start=text.index("    require(len(commands)==119");counts_end=text.index('    boundaries=',counts_start)
    counts="""    require(counts==Counter({0x4000:21,0x2200:1,0xA000:5,0x4821:1,0x4720:1,0x4735:1,0x632E:1,0x6003:1,0:1,0x100:3,0x200:1,0x300:1,0x400:1}),'complete command scope differs')
"""
    tool=derive(source,'dk4tool/patch/lil_B197_editorial_v1.py',{
        text[start:stop]:GATES,text[qa_start:qa_stop]:QA,text[counts_start:counts_end]:counts,
        'B196':'B197','lil_B196_layout_v3':'lil_B197_layout_v1','lil_B196_profile_v2':'lil_B197_profile',
        'six-menu and seven-ending':'three-option and common-ending',
        'SELECTORS={2,6,19,20,25,173,254}':'SELECTORS={21,169,254}',
        'MENUS=[218,582,832,1156,1370,1588]':'MENUS=[230]',
        'END_MAP=[(364,316),(694,624),(938,838),(1266,1144),(1464,1334),(1708,1560),(1810,1664)]':'END_MAP=[(874,998)]',
        'all36_source_native_reference_and_representative_rules_approved':'all24_source_native_reference_and_representative_rules_approved',
        'len(rows)==len(ids)==24 and len(labels)==len(label_ids)==12':'len(rows)==len(ids)==21 and len(labels)==len(label_ids)==3',
        '36 unique objects':'24 unique objects',"{'progressive':23,'system-FE':1}":"{'progressive':20,'system-FE':1}",
        "{'revise':15,'retain-wording':21}":"{'revise':16,'retain-wording':8}",
        'len(observed_ids)==13 and len(offline)==11':'len(observed_ids)==21 and len(offline)==0',
        "['block']==196":"['block']==197",'oldblocks[196]':'oldblocks[197]','blocks[196]':'blocks[197]',
        '==(1816,1814,1668,1668) and len(block)==1816':'==(880,878,1004,1002) and len(block)==880',
        "row['block']==row['source_reference']['block']==196":"row['block']==row['source_reference']['block']==197",
        'block=196':'block=197','require(macros=={b\'FI\':1},\'exact one FI required\')':"require(not macros,'no source macros may be invented')",
        'len(rs)==2 and [r[\'option_index\'] for r in rs]==[0,1]':"len(rs)==3 and [r['option_index'] for r in rs]==[0,1,2]",
        "b'\\0\\x21' and command['count']==2":"b'\\0\\x22' and command['count']==3",
        "row['block']==196":"row['block']==197",'original2100_two_option_modal51FC0':'original2200_three_option_modal51FC0',
        "['買う','買わない'][i]":"['買おう','買わない','任せる'][i]",'sa==at+6+':'sa==at+8+','ca==at+6+':'ca==at+8+',
        "value==[b'Buy',b'Pass'][i] and row['editorial_decision']=='retain-wording' and row.get('fresh_retained_wording_justification')":
        "value==[b\"Let's buy it\",b'Pass',b'You decide'][i] and row['editorial_decision']==['revise','retain-wording','revise'][i] and (i!=1 or row.get('fresh_retained_wording_justification'))",
        "command['new_offset']+6+offsets[i]":"command['new_offset']+8+offsets[i]",
        "struct.pack('<3H',0x2100,*offsets)":"struct.pack('<4H',0x2200,*offsets)",
        "command['old_length']==22 and command['new_length']==len(value)==16":"command['old_length']==34 and command['new_length']==len(value)==40",
        'len(patches)==30':'len(patches)==22','end==1814':'end==878',
        'len(edges)==52 and len(spec[\'target_native_skip_cases\'])==260 and len(logical)==mapped(end)==1668':"len(edges)==6 and len(spec['target_native_skip_cases'])==30 and len(logical)==mapped(end)==1002",
        "len(target)==1668":"len(target)==1004",'0x400,0x2100]':'0x400,0x2200]',
        'all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves':'all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves',
        'all37 original opaque leaves':'all11 original opaque leaves','seven separate ends differ':'single common end differs',
        'every1816 predecessor byte':'every880 predecessor byte','newblocks[196]':'newblocks[197]','==[196]':'==[197]',
        'relative_operands=52,source_commands=119':'relative_operands=6,source_commands=39',
        'all36_reviewed_objects_six_menus_seven_ends_FI_and37_leaves_preserved':'all24_reviewed_objects_three_labels_common_end_no_macros_and11_leaves_preserved',
        'actual13_speech_panels11_offline_only_speeches13_menu_cases_three_endings_not_natural_event_eligibility':'actual21_speech_panels35_observations_three_options_common_end_not_natural_event_eligibility'})
    ROOT.mkdir(parents=True);save(ROOT/'atomic_source_locked_compiler_prepared.json',dict(tool=tool,
        native_high_instruction_constants_and_multiplicity_preserved=True,
        all_source_current_target_references_controls_complete_typed_labels_inverse_and_single_mutation_guards_retained=True,
        B19739_commands21_speeches_one2200_three_labels_six_spans_common_end_and_no_macros=True,
        exact_R74_soft_wrap_waiver_not_transferred_and_measured_differences_explicit=True,
        positive_and_semantic_negative_validation_still_required=True,new_credit=0,full_goal_complete=False))
