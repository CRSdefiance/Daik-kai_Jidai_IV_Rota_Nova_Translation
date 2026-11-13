"""Derive a source-bound linear compiler without inherited wrap exceptions."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B187_references_v5216 import FLAGS
from scripts.verify_village_wrap_v608 import save

SOURCE=Path('dk4tool/patch/lil_B185_editorial_v1.py')
OUTPUT=Path('dk4tool/patch/lil_B187_editorial_v1.py')
ROOT=Path('work/analysis/lil_B187_compiler_tools_v5217')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();text=SOURCE.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index('    expected_names=');e=text.index('    require(sample[',c)
    roles="""    require(names['progressive_nameplate_values']=={'87':'Square Shopkeeper','155':'Sailor'}
        and names['full_catalogue_values']=={'87':'Square Shopkeeper','155':'Retainer'},'source progressive/catalogue distinction required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        ('progressive-nameplate',87):'Square Shopkeeper',('full-catalogue',87):'Square Shopkeeper',
        ('progressive-nameplate',155):'Sailor',('full-catalogue',155):'Retainer'},'four original name consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={87:0,155:4},'original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['commodity_index']==78 and terms['commodity']=='Almond' and terms['city']=='Malacca'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Malacca','Malacca'] and terms['commodity_binding']['text']=='Almond','approved commodity/city identities required')
    for flag in ['Sailor155_progressive_label_does_not_establish_player_employment_or_use_catalogue_Retainer_as_dialogue_rank',
        'natural_dialogue_plural_Almonds_is_inflection_of_approved_Almond_not_UI_rename_or_new_commodity',
        'cough_observation_and_speculative_illness_question_not_diagnosis_or_verified_outbreak',
        'remedy_name_explicitly_forgotten_and_almonds_reported_as_ingredient_not_complete_recipe',
        'source_explicit_reported_remedy_effectiveness_and_strong_sales_both_must_be_preserved',
        'remedy_sales_are_hearsay_not_raw_almond_price_shortage_profit_or_verified_medical_effect',
        'both_later_searches_are_intentions_not_purchase_use_or_recovery','continuing_cough_and_casual_gratitude_preserved',
        'closing_Malacca_Almonds_notice_still_tentative','all16_clean_first_glosses_precede_predecessor_English','no_predecessor_English_exposed']:
        require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no inherited per-record wrap exception')
"""
    g=text.index("    require(not observed['PRNG_equality']");h=text.index('    actual=load',g)
    observed="""    require(observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[2467799992,2467799992]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured final RNG and limits required')
    require(not observed['sampled_postscene_whole_RGB_differences_unmasked'] and observed['all_sampled_postscene_whole_RGB_equal']
        and observed['sixteen_timing_differences_retained_without_masking_retiming_or_future_equivalence_claim'],'measured RGB/timing scope differs')
    require(len(observed['all_actual_consumer_sheets_viewed'])==3 and len(observed['paired_full_screen_views'])==3
        and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
"""
    j=text.index("        if row['source_record_index']==16:");k=text.index('        value=encoded.encoded;',j)
    changes={text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[g:h]:observed,
        text[j:k]:"        require(not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries'),'unapproved inherited boundary exception')\n",
        'B185':'B187','lil_B185_layout_v2':'lil_B187_layout_v1','SELECTORS={164,165,254}':'SELECTORS={87,155,254}',
        "len(native['cases'])==8":"len(native['cases'])==16","native['current_original_macro_alignment_calls']==64":"native['current_original_macro_alignment_calls']==128",
        "native['complete_progressive_planes']==7":"native['complete_progressive_planes']==15",
        "len(stored['final_target_parity_cases'])==8":"len(stored['final_target_parity_cases'])==16",
        "stored['current_final_stored_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==64",
        "stored['new_parity_macro_alignment_cases']==16":"stored['new_parity_macro_alignment_cases']==32",
        "stored['exact_byte_identical_reused_macro_alignment_cases']==16":"stored['exact_byte_identical_reused_macro_alignment_cases']==32",
        'all8_final_targets':'all16_final_targets',"len(controls['relocated_dispatch_cases'])==8":"len(controls['relocated_dispatch_cases'])==16",
        "[('current',384),('research',372)]":"[('current',674),('research',710)]",
        'all8_panels7_progressive1_FE':'all16_panels15_progressive1_FE','original11_commands':'original19_commands',
        'all8_complete_held_planes':'all16_complete_held_planes','all8_speeches7_progressive1':'all16_speeches15_progressive1',
        'dict(total=8,speech=6,control_or_end=2)':'dict(total=16,speech=14,control_or_end=2)',"len(observed['actual_timing_differences'])==8":"len(observed['actual_timing_differences'])==16",
        "actual['fresh_actual_unique_speech_panels']==8":"actual['fresh_actual_unique_speech_panels']==16",'==[20,20]':'==[28,28]','==[4777,4775]':'==[6694,6695]',
        "len(v['selected_intervals'])==8":"len(v['selected_intervals'])==16",'single_source_end384':'single_source_end674',
        "original_source_offset']==384":"original_source_offset']==674","original_source_offset']==382":"original_source_offset']==672",
        'len(rows)==len(set(ids))==8':'len(rows)==len(set(ids))==16','eight exact records':'sixteen exact records',
        "{'progressive':7,'system-FE':1}":"{'progressive':15,'system-FE':1}","{'revise':4,'retain-wording':4}":"{'revise':7,'retain-wording':9}",
        "mapping['blocks'][0]['block']==185":"mapping['blocks'][0]['block']==187",'old_blocks[185]':'old_blocks[187]','blocks[185]':'blocks[187]',
        "row['source_reference']['block']==185":"row['source_reference']['block']==187","row['block']==185":"row['block']==187",'block=185':'block=187',
        "spec['source_bytes']==spec['source_logical_end']==len(block)==388 and spec['research_bytes']==spec['research_logical_end']==376":
        "spec['source_bytes']==len(block)==680 and spec['source_logical_end']==678 and spec['research_bytes']==716 and spec['research_logical_end']==714",
        'end==388 and len(block)==388 and not any(block[end:])':'end==678 and len(block)==680 and block[end:]==bytes(2)',
        'mapped(end)==376':'mapped(end)==714','len(target)==376':'len(target)==716 and target[714:]==bytes(2)',
        'len(commands)==11':'len(commands)==19',"sum(c['word']==0x4000 for c in commands)==8":"sum(c['word']==0x4000 for c in commands)==16",
        '==[(384,372)]':'==[(674,710)]',"[(8,'00a0ffff013807a1'),(382,'00c2'),(384,'00000000')]":"[(8,'00a0ffff014e2fa1'),(672,'00c2'),(674,'00000000')]",
        "require(bytes(restored)==block[:end],'inverse does not restore every predecessor logical byte')":
        "require(bytes(restored)==block[:end] and bytes(restored)+block[end:]==block,'inverse does not restore every predecessor byte')",
        'new_blocks[185]':'new_blocks[187]','==[185]':'==[187]','source_commands=11':'source_commands=19',
        'all8_progressive_FE_speeches':'all16_progressive_FE_speeches',
        'actual_two_complete_B22_fixtures_115_regions_equal_8_timing_and7_later_indicator_differences_unequal_measured_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_115_regions_63_holds_equal_16_timings_disclosed_sampled_RGB_final_PRNG_equal_not_natural_activation',
    }
    row=derive(SOURCE,OUTPUT,changes)
    old,new=native_numbers(text),native_numbers(OUTPUT.read_text(encoding='utf-8'))
    assert old-new==Counter({463267532:1,790984746:1}) and new-old==Counter({2467799992:2})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_linear_compiler.json',dict(derivation=row,
        native_high_constants_preserved_except_measured_PRNG_data=True,all_source_current_metadata_and_both_command_maps_guarded=True,
        source680_678_target716_714_and_two_tailzeros_guarded=True,no_inherited_boundary_exception=True,
        source_role_voices_reported_efficacy_sales_and_search_intentions_guarded=True,every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
