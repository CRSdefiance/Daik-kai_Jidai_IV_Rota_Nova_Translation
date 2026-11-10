"""Prepare atomic B188 integration with exact metadata and measured actual limits."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B188_references_v5260 import FLAGS
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_compiler_tools_v5261')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B187_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    require(names['progressive_nameplate_values']");e=text.index('    require(sample[',c)
    roles="""    expected={'130':'Daimyo','150':'Guildmaster'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected,'original role names required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        (c,int(i)):v for i,v in expected.items() for c in ['progressive-nameplate','full-catalogue']},'four original name consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={130:0,150:0},'original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['commodity_index']==41 and terms['commodity']=='Glass' and terms['city']=='Osaka'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Osaka','Osaka'] and terms['commodity_binding']['text']=='Glass','approved commodity/city identities required')
    for flag in ['source_explicit_giyaman_parenthetical_glass_and_new_name_echo_preserved',
        'giyaman_is_scene_vocabulary_not_new_commodity_UI_rename_or_asserted_etymology',
        'praise_and_famous_craftsman_attribution_are_character_judgment_and_conjecture_not_named_maker_or_proven_origin',
        'source_Daimyo_role_bound_without_invented_personal_name_kinship_or_extra_rank',
        'source_Guildmaster_deference_does_not_require_invented_address_or_relationship',
        'source_explicit_collection_decision_and_order_to_gather_all_giyaman_in_town_preserved',
        'gather_not_explicit_buy_no_price_payment_museum_donation_shortage_item_shape_or_completed_collection_invented',
        'existing_fashion_in_character_discovery_distinct_from_tentative_Glass_Osaka_FE',
        'all11_clean_first_glosses_precede_predecessor_English','no_predecessor_English_exposed']:
        require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required']
        and doc['my_lord_supported_by_clean_Daimyo_role_and_marked_deference_not_inferred_kinship_or_new_title'],'source address and native layout context required')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all11_panels_on_two_native_sheets_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={'DK4_MES_B188_R0022','DK4_MES_B188_R0038'}
        and all(r['reason'] for r in layout['retained_layouts']),'individual native layout retention reasons required')
"""
    g=text.index("    require(observed['PRNG_equality']");h=text.index('    actual=load',g)
    observed="""    require(not observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[403514907,1520957695]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured unequal final RNG and limits required')
    require(not observed['all_sampled_postscene_whole_RGB_equal']
        and [(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[
            (6250,[225,371,239,376]),(6430,[225,371,239,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376]),
            (7690,[224,360,240,376]),(7870,[224,360,240,376]),(7930,[224,360,240,376]),(8110,[224,360,240,376]),
            (8410,[224,360,240,376]),(8590,[224,360,240,376]),(8770,[224,360,240,376]),(8950,[224,360,240,376])]
        and observed['eleven_timing_twelve_original_indicator_and_unequal_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim'],'measured RGB/timing scope differs')
    require(len(observed['all_actual_consumer_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==9
        and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
"""
    row=derive(source,'dk4tool/patch/lil_B188_editorial_v1.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[g:h]:observed,'B187':'B188','SELECTORS={87,155,254}':'SELECTORS={130,150,254}',
        "'postscene_native_state_proof']":"'postscene_native_state_proof','layout_retention_review_proof']",
        "len(native['cases'])==16":"len(native['cases'])==11","native['current_original_macro_alignment_calls']==128":"native['current_original_macro_alignment_calls']==88",
        "native['complete_progressive_planes']==15":"native['complete_progressive_planes']==10",
        "len(stored['final_target_parity_cases'])==16":"len(stored['final_target_parity_cases'])==11","stored['current_final_stored_macro_alignment_cases']==64":"stored['current_final_stored_macro_alignment_cases']==44",
        "stored['new_parity_macro_alignment_cases']==32":"stored['new_parity_macro_alignment_cases']==28","stored['exact_byte_identical_reused_macro_alignment_cases']==32":"stored['exact_byte_identical_reused_macro_alignment_cases']==16",
        'all16_final_targets':'all11_final_targets',"len(controls['relocated_dispatch_cases'])==16":"len(controls['relocated_dispatch_cases'])==11",
        "[('current',674),('research',710)]":"[('current',478),('research',420)]",'all16_panels15_progressive1_FE':'all11_panels10_progressive1_FE',
        'original19_commands':'original14_commands','all16_complete_held_planes':'all11_complete_held_planes','all16_speeches15_progressive1':'all11_speeches10_progressive1',
        'dict(total=16,speech=14,control_or_end=2)':'dict(total=11,speech=9,control_or_end=2)',"len(observed['actual_timing_differences'])==16":"len(observed['actual_timing_differences'])==11",
        "actual['fresh_actual_unique_speech_panels']==16":"actual['fresh_actual_unique_speech_panels']==11",'==[28,28]':'==[23,23]','==[6694,6695]':'==[5495,5497]',
        "len(v['selected_intervals'])==16":"len(v['selected_intervals'])==11",'single_source_end674':'single_source_end478',
        "original_source_offset']==674":"original_source_offset']==478","original_source_offset']==672":"original_source_offset']==476",
        'len(rows)==len(set(ids))==16':'len(rows)==len(set(ids))==11','sixteen exact records':'eleven exact records',
        "{'progressive':15,'system-FE':1}":"{'progressive':10,'system-FE':1}","{'revise':7,'retain-wording':9}":"{'revise':4,'retain-wording':7}",
        "mapping['blocks'][0]['block']==187":"mapping['blocks'][0]['block']==188",'old_blocks[187]':'old_blocks[188]','blocks[187]':'blocks[188]',
        "row['source_reference']['block']==187":"row['source_reference']['block']==188","row['block']==187":"row['block']==188",'block=187':'block=188',
        "spec['source_bytes']==len(block)==680 and spec['source_logical_end']==678 and spec['research_bytes']==716 and spec['research_logical_end']==714":
        "spec['source_bytes']==len(block)==484 and spec['source_logical_end']==482 and spec['research_bytes']==spec['research_logical_end']==424",
        'end==678 and len(block)==680':'end==482 and len(block)==484','mapped(end)==714':'mapped(end)==424','len(target)==716 and target[714:]==bytes(2)':'len(target)==424 and target[424:]==bytes()',
        'len(commands)==19':'len(commands)==14',"sum(c['word']==0x4000 for c in commands)==16":"sum(c['word']==0x4000 for c in commands)==11",
        '==[(674,710)]':'==[(478,420)]',"[(8,'00a0ffff014e2fa1'),(672,'00c2'),(674,'00000000')]":"[(8,'00a0ffff01293ba1'),(476,'00c2'),(478,'00000000')]",
        'new_blocks[187]':'new_blocks[188]','==[187]':'==[188]','source_commands=19':'source_commands=14','all16_progressive_FE_speeches':'all11_progressive_FE_speeches',
        'actual_two_complete_B22_fixtures_115_regions_63_holds_equal_16_timings_disclosed_sampled_RGB_final_PRNG_equal_not_natural_activation':
        'actual_two_complete_B22_fixtures_115_regions_43_holds_equal_11_timings12_indicator_differences_and_unequal_final_PRNG_not_natural_activation',
    })
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({2467799992:2}) and new-old==Counter({403514907:1,1520957695:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_linear_compiler.json',dict(derivation=row,native_high_constants_preserved_except_measured_PRNG_data=True,
        source484_482_target424_424_source_two_tailzeros_guarded=True,complete_metadata_and_both_command_maps_guarded=True,
        source_cultural_roles_collection_and_individual_layout_retention_reasons_guarded=True,every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
