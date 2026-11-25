"""Freeze atomic B190 integration with complete source,prose and actual-state guards."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B190_references_v5343 import FLAGS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B190_compiler_tools_v5344')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B186_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    require(names['progressive_nameplate_values']");e=text.index('    require(sample[',c)
    terms=read('work/analysis/lil_B190_terms_v5320/Sailor_Port_Worker_Havana_Medicine_and_reported_cure_reconciliation.json')
    flags=[k for k,v in terms.items() if v is True and k not in ['full_goal_complete']]
    roles="""    require(names['progressive_nameplate_values']=={'119':'Port Worker','159':'Sailor'}
        and names['full_catalogue_values']=={'119':'Port Worker','159':'Retainer'},'distinct progressive/catalogue identities required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        ('progressive-nameplate',119):'Port Worker',('full-catalogue',119):'Port Worker',
        ('progressive-nameplate',159):'Sailor',('full-catalogue',159):'Retainer'}
        and all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in names['native_four_consumer_cases']['rows']),'four source name consumers required')
    voice=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voice['fresh2_actor_names']['rows']}=={119:0,159:4},'original Port Worker/Sailor voice classes required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']=={'119':'Port Worker','159':'Sailor'}
        and terms['full_catalogue_names']=={'119':'Port Worker','159':'Retainer'} and terms['city']=='Havana'
        and terms['one_source_current_city_alias']['source_text']=='ハバナ' and terms['one_source_current_city_alias']['text']=='Havana'
        and terms['category_index']==13 and terms['source_category']=='薬' and terms['approved_full_category']=='Medicine'
        and terms['compact_UI_category']=='Med' and [r['text'] for r in terms['current_category_binding']['rows']]==['Med']*5+['Medicine']
        and len(terms['all12_category13_native_bindings'])==12,'exact city and category13 rather than invented commodity required')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'whole-exchange source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no inherited record-specific wrap exception')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all17_panels_on_three_native_sheets_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={
        'DK4_MES_B190_R0032','DK4_MES_B190_R0036','DK4_MES_B190_R0056','DK4_MES_B190_R0059','DK4_MES_B190_R0071','DK4_MES_B190_R0074'}
        and all(r['reason'] for r in layout['retained_layouts']),'individual native layout reasons required')
    carry=load(doc['carried_result_proof'])
    require(carry['original_interpreter_preserves_caller_second_result_word'] and len(carry['cases'])==15
        and {(r['version'],r['prior_result']) for r in carry['cases']}=={(v,p) for v in ['clean','current','relocated'] for p in [0,1,2,3,0xFFFFFFFF]}
        and all(r['C200']['native_result']==[3,r['prior_result'],0,0,0,0] and r['end_native_result']==[0,r['prior_result'],0,0,0,0]
            and r['all4MiB_owner_payload_and_guards_exact'] for r in carry['cases']),'original caller-owned result propagation required')
""".replace('TERM_FLAGS',repr(flags))
    oldobserved=text[text.index("    require(observed['PRNG_equality'] is False"):text.index('    actual=load')]
    observed="""    require(observed['PRNG_equality'] is True and observed['postscene9001_PRNG_seeds']==[2467799992,2467799992]
        and observed['future_world_equivalence_and_full_RAM_equality_not_claimed'],'measured final RNG equality and scope required')
    require([(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (7690,[225,371,239,376]),(7870,[225,371,239,376])]
        and observed['nine_timing_and_two_original_indicator_shadow_differences_retained_without_masking_or_retiming']
        and observed['original_carried_result2_C200_3_2_and_end_0_2_preserved'],'all timing/shadow/result observations required')
    require(len(observed['all_actual_consumer_sheets_viewed'])==3 and len(observed['paired_full_screen_views'])==4
        and all(s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
"""
    oldboundary=text[text.index("        if row['source_record_index']==13:"):text.index('        value=encoded.encoded;pad=')]
    newboundary="        require(not row.get('reviewed_ordinary_boundaries') and not qa.get('reviewed_ordinary_boundaries'),'no inherited boundary exceptions')\n"
    changes={text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,oldobserved:observed,oldboundary:newboundary,
        'B186':'B190','lil_B186_layout_v4':'lil_B190_layout_v1','SELECTORS={174,175,254}':'SELECTORS={119,159,254}',
        "'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof']":"'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof','layout_retention_review_proof','carried_result_proof']",
        "len(native['cases'])==12 and native['current_original_macro_alignment_calls']==96":"len(native['cases'])==17 and native['current_original_macro_alignment_calls']==136",
        "native['complete_progressive_planes']==11":"native['complete_progressive_planes']==16",
        "len(stored['final_target_parity_cases'])==12 and stored['current_final_stored_macro_alignment_cases']==48":"len(stored['final_target_parity_cases'])==17 and stored['current_final_stored_macro_alignment_cases']==68",
        "stored['new_parity_macro_alignment_cases']==36 and stored['exact_byte_identical_reused_macro_alignment_cases']==12":"stored['new_parity_macro_alignment_cases']==40 and stored['exact_byte_identical_reused_macro_alignment_cases']==28",
        'all12_final_targets':'all17_final_targets',"len(controls['relocated_dispatch_cases'])==12":"len(controls['relocated_dispatch_cases'])==17",'==[(540,478)]':'==[(8,8)]',
        "pair['new_offset']%4==2":"pair['new_offset']%4==0","not a['operand_pointer_unaligned'] and b['operand_pointer_unaligned']":"not a['operand_pointer_unaligned'] and not b['operand_pointer_unaligned']",
        "b['unaligned_operand_scratch_writes']==[dict(PC=0x0202A5D8,address=0x02279600,size=4,value=700)]":"b['unaligned_operand_scratch_writes']==([dict(PC=0x0202A5D8,address=0x02279600,size=4,value=500)] if b['operand_pointer_unaligned'] else [])",
        "sum(r['operand_pointer_unaligned'] for r in ownership['cases'])==4":"sum(r['operand_pointer_unaligned'] for r in ownership['cases'])==0",
        'aligned and unaligned coverage':'aligned source/current/target coverage',"[('clean',[540]),('current',[540]),('relocated',[478])]":"[('clean',[8]),('current',[8]),('relocated',[8])]",
        'value=700':'value=500','roll<700':'roll<500','roll==700':'roll==500',"r['threshold']==700":"r['threshold']==500",'{699,700,701}':'{499,500,501}',
        "[('current',646),('research',578)]":"[('current',602),('research',698)]",'all12_panels_eleven_progressive':'all17_panels_sixteen_progressive',
        'source_all24_commands':'source_all29_commands','original_scene_predicate_results_equal_draws_seeds_timing_and_indicator_differences_disclosed':'original_scene_result2_carried_through_UI_and_end_timing_shadow_differences_disclosed',
        'all12_complete_held_planes':'all17_complete_held_planes','all12_speeches11_progressive1':'all17_speeches16_progressive1',
        'dict(total=10,speech=4,control_or_end=6)':'dict(total=9,speech=7,control_or_end=2)',"len(observed['actual_timing_differences'])==10":"len(observed['actual_timing_differences'])==9",
        "actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==12":"actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==17",
        '==[27,27]':'==[34,34]','==[5735,5737]':'==[6934,6937]','dict(clean_Japanese=[560],reviewed_English=[560])':'dict(clean_Japanese=[52],reviewed_English=[52])',
        "len(version['selected_intervals'])==12":"len(version['selected_intervals'])==17",'single_source_end646':'single_source_end602',
        "version['selected_B22_command_pairs'][-1]['result_words']==[0,0]":"version['selected_B22_command_pairs'][-1]['result_words']==[0,2]",
        "original_source_offset']==646":"original_source_offset']==602","original_source_offset']==560":"original_source_offset']==52","original_source_offset']==644":"original_source_offset']==600",
        "{'clean_Japanese':(540,297,0),'reviewed_English':(540,592,0)}":"{'clean_Japanese':(8,875,2),'reviewed_English':(8,875,2)}",
        'len(rows)==len(set(ids))==12':'len(rows)==len(set(ids))==17','twelve exact records':'seventeen exact records',"{'progressive':11,'system-FE':1}":"{'progressive':16,'system-FE':1}","{'revise':7,'retain-wording':5}":"{'revise':10,'retain-wording':7}",
        "mapping['blocks'][0]['block']==186":"mapping['blocks'][0]['block']==190",'old_blocks[186]':'old_blocks[190]','.blocks[186]':'.blocks[190]',
        "spec['source_bytes']==len(block)==652 and spec['source_logical_end']==650":"spec['source_bytes']==len(block)==608 and spec['source_logical_end']==606",
        "spec['research_bytes']==584 and spec['research_logical_end']==582":"spec['research_bytes']==704 and spec['research_logical_end']==702",
        "row['source_reference']['block']==186":"row['source_reference']['block']==190","row['block']==186":"row['block']==190",'block=186':'block=190',
        'end == 650 and len(block)==652':'end == 606 and len(block)==608','[548,552,556,568,580,592]':'[16,20,24,36,48,60]',
        'mapped(end)==582':'mapped(end)==702','len(target)==584 and target[582:]':'len(target)==704 and target[702:]',
        'len(commands) == 24':'len(commands) == 29',"sum(command['word'] == 0x4000 for command in commands) == 12":"sum(command['word'] == 0x4000 for command in commands) == 17",
        "[c['old_offset'] for c in stops]==[646] and len(stops)==1 and stops[0]['new_offset']==578":"[c['old_offset'] for c in stops]==[602] and len(stops)==1 and stops[0]['new_offset']==698",'target[578:582]':'target[698:702]',
        "exact=[(540,'0080ffffbc020000'),(560,'00a0ffff010b19a1'),(572,'00a0ffff011219a1'),\n        (584,'00a0ffff010c19a1'),(644,'00c2'),(646,'00000000')]":"exact=[(8,'0080fffff4010000'),(28,'00a0ffff014c41a1'),(40,'00a0ffff014b41a1'),\n        (52,'00a0ffff014d41a1'),(600,'00c2'),(602,'00000000')]",
        'new_blocks[186]':'new_blocks[190]','== [186]':'== [190]','source_commands=24':'source_commands=29','all12_progressive_FE_speeches_one700_predicate':'all17_progressive_FE_speeches_one500_predicate',
    }
    row=derive(source,'dk4tool/patch/lil_B190_editorial_v1.py',changes)
    before,after=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert before-after==Counter({1803218166:1}) and after-before==Counter({2467799992:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_conditional_compiler.json',dict(derivation=row,
        native_high_constants_preserved_except_measured_PRNG_data=True,complete_metadata_both_maps_original_result_propagation_and_terms_guarded=True,
        no_record_specific_wrap_exception=True,all_checks_precede_single_replace_file=True,no_credit=True,full_goal_complete=False))
