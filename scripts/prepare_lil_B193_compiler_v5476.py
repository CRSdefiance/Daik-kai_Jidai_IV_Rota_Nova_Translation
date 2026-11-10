"""Prepare atomic fifteen-record integration with three actors and measured timing."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B193_references_v5475 import FLAGS
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_compiler_tools_v5476')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B192_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index('    progressive=');e=text.index('    require(sample[',c)
    roles="""    expected={'166':'Lady','167':'Lady','168':'Lady'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected,'three exact original Ladies required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_six_consumer_cases']['rows']}=={
        (c,int(i)):v for i,v in expected.items() for c in ['progressive-nameplate','full-catalogue']},'six original name consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}=={166:0,167:0,168:0},'three original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']==expected and terms['commodity_index']==29 and terms['source_commodity']=='トウガラシ'
        and terms['commodity']=='Chili' and terms['source_supported_prose']=='chili peppers' and terms['city']=='Seoul'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Seoul','Seoul'] and terms['commodity_binding']['text']=='Chili'
        and terms['original_commodity_metadata_hex']=='d80e03db58020100','exact source city and individual commodity required')
    for flag in ['three_distinct_source_Ladies_and_original_voice0_without_invented_personal_names_or_new_titles',
        'source_cooking_preparation_question_and_immediate_teaching_offer_not_trade_advice',
        'first_time_meal_praise_stimulating_flavor_reported_spice_classification_and_local_ingredient_compatibility_preserved',
        'source_price_question_and_relative_reassurance_preserved_as_character_claims_without_amount_scarcity_or_profit',
        'tonight_tentative_household_use_and_now_teaching_offer_not_completed_purchase_cooking_or_lesson',
        'friendship_explicit_in_otomodachi_preserved_without_invented_kinship_romance_marriage_employment_or_prior_history',
        'Chili29_individual_commodity_not_category_or_chili_stew_powder_recipe_origin_or_specific_quantity',
        'existing_Chili29_older_fidelity_review_remains_open_no_UI_rename_or_new_widget_credit',
        'both_Seoul_aliases_bound_to_source_Keijo_without_unapproved_place_rename',
        'tentative_Chili_Seoul_FE_does_not_establish_earlier_location_or_earned_fashion',
        'source18_linear_commands_one_A000_C200_end_two_tailzeros_no_predicates_relatives_or_item_presentation',
        'all15_clean_first_glosses_precede_predecessor_English','no_predecessor_English_exposed']:
        require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no inherited native boundary exception')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all15_panels_on_two_native_sheets_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={
        'DK4_MES_B193_R0006','DK4_MES_B193_R0025','DK4_MES_B193_R0037','DK4_MES_B193_R0044'}
        and all(r['reason'] for r in layout['retained_layouts']) and layout['exact_paragraph_ASCII_characters']==111
        and layout['three_row_maximum_cells']==106 and layout['count_transcription_corrected_without_prose_layout_or_native_plane_change'],'individual corrected layout reasons required')
"""
    g=text.index("    require(not observed['PRNG_equality']");h=text.index('    actual=load',g)
    observed="""    require(observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[463267532,463267532]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured final RNG and limits required')
    require(observed['all_sampled_postscene_whole_RGB_equal'] and not observed['sampled_postscene_whole_RGB_differences_unmasked']
        and observed['ten_speech_timing_differences_retained_without_masking_retiming_or_equivalence_claim']
        and observed['three_distinct_original_Lady_portraits_and_four_row_explanation_cooking_offer_and_friendship_observed'],'measured RGB/timing and three-portrait scope differs')
    require(len(observed['all_actual_consumer_sheets_viewed'])==3 and len(observed['paired_full_screen_views'])==3
        and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
"""
    row=derive(source,'dk4tool/patch/lil_B193_editorial_v1.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[g:h]:observed,'B192':'B193','SELECTORS={115,153,254}':'SELECTORS={166,167,168,254}',
        "len(native['cases'])==8":"len(native['cases'])==15","native['current_original_macro_alignment_calls']==64":"native['current_original_macro_alignment_calls']==120",
        "native['complete_progressive_planes']==7":"native['complete_progressive_planes']==14","len(native['negative_controls'])==18":"len(native['negative_controls'])==20",
        "len(stored['final_target_parity_cases'])==8":"len(stored['final_target_parity_cases'])==15","stored['current_final_stored_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==60",
        "stored['new_parity_macro_alignment_cases']==16":"stored['new_parity_macro_alignment_cases']==32","stored['exact_byte_identical_reused_macro_alignment_cases']==16":"stored['exact_byte_identical_reused_macro_alignment_cases']==28",
        'all8_final_targets':'all15_final_targets',"len(controls['relocated_dispatch_cases'])==8":"len(controls['relocated_dispatch_cases'])==15",
        "[('current',398),('research',372)]":"[('current',662),('research',672)]",'all8_panels7_progressive1_FE':'all15_panels14_progressive1_FE',
        'original11_commands':'original18_commands','all8_complete_held_planes':'all15_complete_held_planes','all8_speeches7_progressive1':'all15_speeches14_progressive1',
        'dict(total=9,speech=7,control_or_end=2)':'dict(total=10,speech=10,control_or_end=0)',"len(observed['actual_timing_differences'])==9":"len(observed['actual_timing_differences'])==10",
        "actual['fresh_actual_unique_speech_panels']==8":"actual['fresh_actual_unique_speech_panels']==15",'==[20,20]':'==[27,27]','==[4775,4777]':'==[6457,6457]',
        "len(v['selected_intervals'])==8":"len(v['selected_intervals'])==15",'single_source_end398':'single_source_end662',
        "original_source_offset']==398":"original_source_offset']==662","original_source_offset']==396":"original_source_offset']==660",
        'len(rows)==len(set(ids))==8':'len(rows)==len(set(ids))==15','eight exact records':'fifteen exact records',
        "{'progressive':7,'system-FE':1}":"{'progressive':14,'system-FE':1}","{'revise':5,'retain-wording':3}":"{'revise':8,'retain-wording':7}",
        "mapping['blocks'][0]['block']==192":"mapping['blocks'][0]['block']==193",'old_blocks[192]':'old_blocks[193]','blocks[192]':'blocks[193]',
        "row['source_reference']['block']==192":"row['source_reference']['block']==193","row['block']==192":"row['block']==193",'block=192':'block=193',
        "spec['source_bytes']==len(block)==404 and spec['source_logical_end']==402 and spec['research_bytes']==spec['research_logical_end']==376":
        "spec['source_bytes']==len(block)==668 and spec['source_logical_end']==666 and spec['research_bytes']==spec['research_logical_end']==676",
        'end==402 and len(block)==404':'end==666 and len(block)==668','mapped(end)==376':'mapped(end)==676','len(target)==376 and target[376:]==bytes()':'len(target)==676 and target[676:]==bytes()',
        'len(commands)==11':'len(commands)==18',"sum(c['word']==0x4000 for c in commands)==8":"sum(c['word']==0x4000 for c in commands)==15",
        '==[(398,372)]':'==[(662,672)]',"[(8,'00a0ffff012116a1'),(396,'00c2'),(398,'00000000')]":"[(8,'00a0ffff011d39a1'),(660,'00c2'),(662,'00000000')]",
        'new_blocks[192]':'new_blocks[193]','==[192]':'==[193]','source_commands=11':'source_commands=18','all8_progressive_FE_speeches':'all15_progressive_FE_speeches',
        'actual_two_complete_B22_fixtures_115_regions_31_holds_equal_9_timings7_indicator_differences_and_unequal_final_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_three_portraits_115_regions_59_holds_10_speech_timings_equal_postscene_RGB_and_measured_PRNG_not_natural_activation'} )
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({790984746:1,3723009301:1}) and new-old==Counter({463267532:2})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_compiler.json',dict(derivation=row,native_high_constants_preserved_except_measured_PRNG_data=True,
        exact_source668_666_target676_676_complete_metadata_both_maps_and_inverse_guarded=True,
        six_names_three_voices_cooking_reportedness_price_intentions_friendship_and_corrected_layout_receipt_guarded=True,every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
