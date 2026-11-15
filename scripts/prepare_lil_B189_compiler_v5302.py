"""Prepare atomic four-speaker integration with complete source and native evidence."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B189_references_v5301 import FLAGS
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_compiler_tools_v5302')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B188_editorial_v2.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    expected={'130'");e=text.index('    require(sample[',c)
    roles="""    expected={'82':'Square Shopkeeper','104':'Trader','113':'Port Worker','147':'Guildmaster'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected,'four original role names required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_eight_consumer_cases']['rows']}=={
        (c,int(i)):v for i,v in expected.items() for c in ['progressive-nameplate','full-catalogue']},'eight original name consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh4_actor_names']['rows']}=={82:0,104:0,113:0,147:0},'four original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']==expected and terms['commodity_index']==42 and terms['commodity_UI']=='China'
        and terms['source_commodity']=='陶磁器' and terms['source_supported_prose_collective']=='ceramics' and terms['city']=='Hamburg'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Hamburg','Hamburg'] and terms['commodity_binding']['text']=='China','source prose and exact existing UI identities required')
    require(terms['actual_source_selectors_hex']==['93','52','68','71'] and terms['actual_source_selectors_decimal']==[147,82,104,113]
        and doc['source_selectors_hex93_52_68_71_equal_decimal147_82_104_113'],'exact hexadecimal/decimal selector distinction required')
    for flag in ['ceramics_is_broad_source_term_not_a_new_commodity_UI_rename_or_Chinese_origin_claim',
        'legacy_UI_China42_older_fidelity_review_remains_open_no_defect_or_new_widget_completion_claim',
        'Guildmaster_and_Square_Shopkeeper_collection_discussion_then_Trader_and_Port_Worker_private_exchange_preserved',
        'source_role_familiar_forms_do_not_establish_father_brother_master_kinship_or_new_rank',
        'completed_first_acquisition_and_reported_first_sale_preserved_without_invented_price_quantity_shape_or_origin',
        'source_explicit_collecting_craze_good_piece_scarcity_and_hearsay_buying_up_preserved_as_character_claims',
        'dramatic_irony_between_collector_praise_and_sellers_private_worthless_ware_unbelievable_price_claim_preserved',
        'no_narrator_verified_value_authenticity_forgery_or_market_state',
        'second_pairs_short_funds_belong_to_Trader_Port_Worker_not_collector_customers',
        'good_customers_does_not_require_repeated_prior_sales','proposed_approach_and_final_hail_not_second_sale_threat_or_robbery',
        'humble_home_invitation_not_mansion_or_completed_visit','ingratiating_danna_hail_not_employment_marriage_or_kinship',
        'tentative_ceramics_Hamburg_FE_distinct_from_character_market_claims_earlier_location_and_earned_state',
        'all17_clean_first_glosses_precede_predecessor_English','no_predecessor_English_exposed']:
        require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no inherited native boundary exception')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all17_panels_on_three_native_sheets_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={
        'DK4_MES_B189_R0006','DK4_MES_B189_R0016','DK4_MES_B189_R0022','DK4_MES_B189_R0046','DK4_MES_B189_R0049'}
        and all(r['reason'] for r in layout['retained_layouts']),'individual native layout retention reasons required')
"""
    g=text.index("    require(not observed['PRNG_equality']");h=text.index('    actual=load',g)
    observed="""    require(not observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[463267532,3723009301]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured unequal final RNG and limits required')
    require(observed['all_sampled_postscene_whole_RGB_equal'] and not observed['sampled_postscene_whole_RGB_differences_unmasked']
        and observed['eight_speech_timing_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim']
        and observed['four_original_speakers_and_two_pair_portrait_transition_observed'],'measured RGB/timing and four-speaker scope differs')
    require(len(observed['all_actual_consumer_sheets_viewed'])==3 and len(observed['paired_full_screen_views'])==3
        and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
"""
    row=derive(source,'dk4tool/patch/lil_B189_editorial_v1.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[g:h]:observed,'B188':'B189','SELECTORS={130,150,254}':'SELECTORS={82,104,113,147,254}',
        "len(native['cases'])==11":"len(native['cases'])==17","native['current_original_macro_alignment_calls']==88":"native['current_original_macro_alignment_calls']==136",
        "native['complete_progressive_planes']==10":"native['complete_progressive_planes']==16","len(native['negative_controls'])==18":"len(native['negative_controls'])==22",
        "len(stored['final_target_parity_cases'])==11":"len(stored['final_target_parity_cases'])==17","stored['current_final_stored_macro_alignment_cases']==44":"stored['current_final_stored_macro_alignment_cases']==68",
        "stored['new_parity_macro_alignment_cases']==28":"stored['new_parity_macro_alignment_cases']==40","stored['exact_byte_identical_reused_macro_alignment_cases']==16":"stored['exact_byte_identical_reused_macro_alignment_cases']==28",
        'all11_final_targets':'all17_final_targets',"len(controls['relocated_dispatch_cases'])==11":"len(controls['relocated_dispatch_cases'])==17",
        "[('current',478),('research',420)]":"[('current',766),('research',844)]",'all11_panels10_progressive1_FE':'all17_panels16_progressive1_FE',
        'original14_commands':'original20_commands','all11_complete_held_planes':'all17_complete_held_planes','all11_speeches10_progressive1':'all17_speeches16_progressive1',
        'dict(total=11,speech=9,control_or_end=2)':'dict(total=8,speech=8,control_or_end=0)',"len(observed['actual_timing_differences'])==11":"len(observed['actual_timing_differences'])==8",
        "actual['fresh_actual_unique_speech_panels']==11":"actual['fresh_actual_unique_speech_panels']==17",'==[23,23]':'==[29,29]','==[5495,5497]':'==[6937,6937]',
        "len(v['selected_intervals'])==11":"len(v['selected_intervals'])==17",'single_source_end478':'single_source_end766',
        "original_source_offset']==478":"original_source_offset']==766","original_source_offset']==476":"original_source_offset']==764",
        'len(rows)==len(set(ids))==11':'len(rows)==len(set(ids))==17','eleven exact records':'seventeen exact records',
        "{'progressive':10,'system-FE':1}":"{'progressive':16,'system-FE':1}","{'revise':4,'retain-wording':7}":"{'revise':10,'retain-wording':7}",
        "mapping['blocks'][0]['block']==188":"mapping['blocks'][0]['block']==189",'old_blocks[188]':'old_blocks[189]','blocks[188]':'blocks[189]',
        "row['source_reference']['block']==188":"row['source_reference']['block']==189","row['block']==188":"row['block']==189",'block=188':'block=189',
        "spec['source_bytes']==len(block)==484 and spec['source_logical_end']==482 and spec['research_bytes']==spec['research_logical_end']==424":
        "spec['source_bytes']==len(block)==772 and spec['source_logical_end']==770 and spec['research_bytes']==spec['research_logical_end']==848",
        'end==482 and len(block)==484':'end==770 and len(block)==772','mapped(end)==424':'mapped(end)==848','len(target)==424 and target[424:]==bytes()':'len(target)==848 and target[848:]==bytes()',
        'len(commands)==14':'len(commands)==20',"sum(c['word']==0x4000 for c in commands)==11":"sum(c['word']==0x4000 for c in commands)==17",
        '==[(478,420)]':'==[(766,844)]',"[(8,'00a0ffff01293ba1'),(476,'00c2'),(478,'00000000')]":"[(8,'00a0ffff012a05a1'),(764,'00c2'),(766,'00000000')]",
        'new_blocks[188]':'new_blocks[189]','==[188]':'==[189]','source_commands=14':'source_commands=20','all11_progressive_FE_speeches':'all17_progressive_FE_speeches',
        'actual_two_complete_B22_fixtures_115_regions_43_holds_equal_11_timings12_indicator_differences_and_unequal_final_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_four_speakers_115_regions_67_holds_equal_8_speech_timings_unequal_final_PRNG_not_natural_activation',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({403514907:1,1520957695:1}) and new-old==Counter({463267532:1,3723009301:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_four_speaker_compiler.json',dict(derivation=row,native_high_constants_preserved_except_measured_PRNG_data=True,
        source772_770_target848_848_source_two_tailzeros_guarded=True,complete_metadata_and_both_command_maps_guarded=True,
        eight_native_name_consumers_four_voices_source_irony_market_claims_antecedent_and_layout_reasons_guarded=True,
        every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
