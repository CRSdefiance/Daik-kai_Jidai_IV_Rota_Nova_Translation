"""Prepare atomic linear B192 integration with exact context and measured display."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B192_references_v5434 import FLAGS
from scripts.record_lil_B192_actual_view_v5433 import DIFFERENCES
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_compiler_tools_v5435')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B188_editorial_v2.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    expected={'130'");e=text.index('    require(sample[',c)
    roles="""    progressive={'115':'Port Worker','153':'Sailor'}
    catalogue={'115':'Port Worker','153':'Retainer'}
    require(names['progressive_nameplate_values']==progressive and names['full_catalogue_values']==catalogue,'exact progressive/catalogue distinction required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        **{('progressive-nameplate',int(i)):v for i,v in progressive.items()},
        **{('full-catalogue',int(i)):v for i,v in catalogue.items()}},'four original name consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={115:0,153:4},'original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['commodity_index']==33 and terms['source_commodity']=='タバコ' and terms['commodity']=='Tobacco' and terms['city']=='Istanbul'
        and terms['one_source_current_city_alias']['text']=='Istanbul' and terms['commodity_binding']['text']=='Tobacco'
        and terms['original_commodity_metadata_hex']=='a00f040cf4010100','exact source city and individual commodity required')
    for flag in ['tobacco_is_individual_commodity33_not_category_or_new_UI_name',
        'no_unproved_second_Istanbul_alias_or_new_widget_completion',
        'Sailor153_catalogue_Retainer_does_not_prove_player_employment_rank_or_smoking_experience',
        'Port_Worker115_familiar_aniki_role_does_not_prove_brotherhood_or_kinship',
        'question_reversal_lack_of_opportunity_popularity_hyperbole_stammered_curiosity_offer_and_hesitant_assent_preserved',
        'probably_only_person_in_this_town_is_character_hyperbole_not_narrator_statistics_or_named_location',
        'source_tobacco_and_smoking_not_sanitized_or_changed_to_pipe_cigar_cigarette_or_brand',
        'no_invented_age_rank_employment_smoking_history_dependence_coercion_or_health_claim',
        'offer_and_follow_me_assent_not_completed_smoking_purchase_gift_or_specific_destination',
        'tentative_Tobacco_Istanbul_FE_distinct_from_character_popularity_claim_prior_location_or_earned_fashion',
        'source11_linear_commands_one_A000_C200_end_two_tailzeros_no_predicates_or_relatives',
        'all8_clean_first_glosses_precede_predecessor_English','no_predecessor_English_exposed']:
        require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no inherited native boundary exception')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all8_panels_on_one_native_sheet_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={'DK4_MES_B192_R0016','DK4_MES_B192_R0023'}
        and all(r['reason'] for r in layout['retained_layouts']),'individual native layout retention reasons required')
"""
    g=text.index("    require(not observed['all_sampled_postscene_whole_RGB_equal']");h=text.index('    actual=load',g)
    observed="""    require(not observed['all_sampled_postscene_whole_RGB_equal']
        and [(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==DIFFERENCES
        and observed['nine_timing_seven_original_indicator_and_unequal_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim'],'measured RGB/timing scope differs')
    require(len(observed['all_actual_consumer_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==7
        and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
""".replace('==DIFFERENCES','=='+repr(DIFFERENCES))
    row=derive(source,'dk4tool/patch/lil_B192_editorial_v1.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[g:h]:observed,'B188':'B192','SELECTORS={130,150,254}':'SELECTORS={115,153,254}',
        "len(native['cases'])==11":"len(native['cases'])==8","native['current_original_macro_alignment_calls']==88":"native['current_original_macro_alignment_calls']==64",
        "native['complete_progressive_planes']==10":"native['complete_progressive_planes']==7",
        "len(stored['final_target_parity_cases'])==11":"len(stored['final_target_parity_cases'])==8","stored['current_final_stored_macro_alignment_cases']==44":"stored['current_final_stored_macro_alignment_cases']==32",
        "stored['new_parity_macro_alignment_cases']==28":"stored['new_parity_macro_alignment_cases']==16",'all11_final_targets':'all8_final_targets',
        "len(controls['relocated_dispatch_cases'])==11":"len(controls['relocated_dispatch_cases'])==8",
        "[('current',478),('research',420)]":"[('current',398),('research',372)]",'all11_panels10_progressive1_FE':'all8_panels7_progressive1_FE',
        'original14_commands':'original11_commands','all11_complete_held_planes':'all8_complete_held_planes','all11_speeches10_progressive1':'all8_speeches7_progressive1',
        'dict(total=11,speech=9,control_or_end=2)':'dict(total=9,speech=7,control_or_end=2)',"len(observed['actual_timing_differences'])==11":"len(observed['actual_timing_differences'])==9",
        '[403514907,1520957695]':'[790984746,3723009301]',"actual['fresh_actual_unique_speech_panels']==11":"actual['fresh_actual_unique_speech_panels']==8",
        '==[23,23]':'==[20,20]','==[5495,5497]':'==[4775,4777]',"len(v['selected_intervals'])==11":"len(v['selected_intervals'])==8",'single_source_end478':'single_source_end398',
        "original_source_offset']==478":"original_source_offset']==398","original_source_offset']==476":"original_source_offset']==396",
        'len(rows)==len(set(ids))==11':'len(rows)==len(set(ids))==8','eleven exact records':'eight exact records',
        "{'progressive':10,'system-FE':1}":"{'progressive':7,'system-FE':1}","{'revise':4,'retain-wording':7}":"{'revise':5,'retain-wording':3}",
        "mapping['blocks'][0]['block']==188":"mapping['blocks'][0]['block']==192",'old_blocks[188]':'old_blocks[192]','blocks[188]':'blocks[192]',
        "row['source_reference']['block']==188":"row['source_reference']['block']==192","row['block']==188":"row['block']==192",'block=188':'block=192',
        "spec['source_bytes']==len(block)==484 and spec['source_logical_end']==482 and spec['research_bytes']==spec['research_logical_end']==424":
        "spec['source_bytes']==len(block)==404 and spec['source_logical_end']==402 and spec['research_bytes']==spec['research_logical_end']==376",
        'end==482 and len(block)==484':'end==402 and len(block)==404','mapped(end)==424':'mapped(end)==376','len(target)==424 and target[424:]==bytes()':'len(target)==376 and target[376:]==bytes()',
        'len(commands)==14':'len(commands)==11',"sum(c['word']==0x4000 for c in commands)==11":"sum(c['word']==0x4000 for c in commands)==8",
        '==[(478,420)]':'==[(398,372)]',"[(8,'00a0ffff01293ba1'),(476,'00c2'),(478,'00000000')]":"[(8,'00a0ffff012116a1'),(396,'00c2'),(398,'00000000')]",
        'new_blocks[188]':'new_blocks[192]','==[188]':'==[192]','source_commands=14':'source_commands=11','all11_progressive_FE_speeches':'all8_progressive_FE_speeches',
        'actual_two_complete_B22_fixtures_115_regions_43_holds_equal_11_timings12_indicator_differences_and_unequal_final_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_115_regions_31_holds_equal_9_timings7_indicator_differences_and_unequal_final_PRNG_not_natural_activation',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({403514907:1,1520957695:1}) and new-old==Counter({790984746:1,3723009301:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_compiler.json',dict(derivation=row,native_high_constants_preserved_except_measured_PRNG_data=True,
        exact_source404_402_target376_376_complete_metadata_both_maps_and_inverse_guarded=True,
        source_curiosity_hyperbole_hesitation_intentions_and_distinct_names_voices_guarded=True,every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
