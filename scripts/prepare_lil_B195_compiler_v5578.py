"""Prepare source-locked B195 integration without weakening any native guard."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.seal_lil_B195_references_v5575 import FLAGS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B195_compiler_tools_v5578')

if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B193_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    expected={'166'");e=text.index('    require(sample[',c)
    terms=read('work/analysis/lil_B195_terms_v5547/three_roles_both_Veracruz_aliases_Cheese8_and_unnamed_specialty_reconciliation.json')
    term_flags=[k for k,v in terms.items() if v is True and k not in ['predecessor_English_prose_comparison_pending']]
    roles="""    expected={'92':'Barkeep','103':'Patron','119':'Port Worker'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected,'three exact original roles required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_six_consumer_cases']['rows']}=={
        (c,int(i)):v for i,v in expected.items() for c in ['progressive-nameplate','full-catalogue']},'six original readonly name consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}=={92:0,103:0,119:0},'three original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']==expected and terms['commodity_index']==8 and terms['source_commodity']=='チーズ'
        and terms['commodity']=='Cheese' and terms['city']=='Veracruz'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Veracruz','Veracruz'] and terms['commodity_binding']['text']=='Cheese'
        and terms['original_commodity_metadata_hex']=='b00400db58020100','exact source city aliases and individual commodity required')
    for flag in TERM_FLAGS:
        require(terms.get(flag) is True,'source context required:'+flag)
    require(doc['no_record_specific_ordinary_boundary_exception_required'],'no inherited native boundary exception')
    layout=load(doc['source_bound_wrap_retention_proof'])
    require(layout['all11_two_row_splits_fail_unchanged_native_lint'] and len(layout['all_complete_word_two_row_splits'])==11
        and layout['no_ordinary_boundary_exception_adopted'] and layout['selected_formatter_unchanged']
        and layout['paragraph_ASCII_characters']==68 and layout['all20_paragraphs_compiled_bytes_and_current_native_planes_unchanged'],
        'source-bound three-row retention under unchanged native guard required')
    r17=next(r for r in doc['records'] if r['source_record_index']==17)
    require(r17['native_layout_retention_reason']==layout['retention_reason'] and bool(layout['retention_reason'])
        and r17['english']==layout['exact_logical_prose'] and r17['compiled_hex']==layout['retained_compiled_hex'],
        'exact R17 prose,compiled target and justified retention required')
""".replace('TERM_FLAGS',repr(term_flags))
    g=text.index("    require(observed['PRNG_equality']");h=text.index('    actual=load',g)
    observed="""    require(not observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[3942509462,3085513495]
        and observed['no_PRNG_causal_or_future_world_equivalence_claim'],'measured unequal final RNG and limits required')
    require(not observed['all_sampled_postscene_whole_RGB_equal']
        and [(r['frame'],r['whole_frame_difference_bbox'],r['nontext_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[
            (f,[224,370,240,376],None) for f in [8410,8590,8770,8950]]
        and observed['fifteen_timing_four_later_indicator_RGB_and_unequal_PRNG_differences_retained_without_masking_or_retiming']
        and observed['original_three_roles_R17_three_rows_two_chewing_beats_R69_intention_and_FE_clear_observed'],'measured RGB/timing and original-role scope differs')
    require(len(observed['all_actual_consumer_sheets_viewed'])==4 and len(observed['paired_full_screen_views'])==5
        and all(s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002
        and observed['all79_complete_native_holds_and115_paired_nontext_samples_pass'],'viewed current evidence required')
"""
    row=derive(source,'dk4tool/patch/lil_B195_editorial_v1.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[g:h]:observed,
        'B193':'B195','SELECTORS={166,167,168,254}':'SELECTORS={92,103,119,254}',
        "'layout_retention_review_proof'":"'source_bound_wrap_retention_proof'",
        "len(native['cases'])==15":"len(native['cases'])==20","native['current_original_macro_alignment_calls']==120":"native['current_original_macro_alignment_calls']==160",
        "native['complete_progressive_planes']==14":"native['complete_progressive_planes']==19",
        "len(stored['final_target_parity_cases'])==15":"len(stored['final_target_parity_cases'])==20",
        "stored['current_final_stored_macro_alignment_cases']==60":"stored['current_final_stored_macro_alignment_cases']==80",
        "stored['new_parity_macro_alignment_cases']==32":"stored['new_parity_macro_alignment_cases']==24",
        "stored['exact_byte_identical_reused_macro_alignment_cases']==28":"stored['exact_byte_identical_reused_macro_alignment_cases']==56",
        'all15_final_targets':'all20_final_targets',"len(controls['relocated_dispatch_cases'])==15":"len(controls['relocated_dispatch_cases'])==20",
        "[('current',662),('research',672)]":"[('current',706),('research',612)]",
        'all15_panels14_progressive1_FE':'all20_panels19_progressive1_FE','original18_commands':'original23_commands',
        'all15_complete_held_planes':'all20_complete_held_planes','all15_speeches14_progressive1':'all20_speeches19_progressive1',
        'dict(total=10,speech=10,control_or_end=0)':'dict(total=15,speech=13,control_or_end=2)',
        "len(observed['actual_timing_differences'])==10":"len(observed['actual_timing_differences'])==15",
        "actual['fresh_actual_unique_speech_panels']==15":"actual['fresh_actual_unique_speech_panels']==20",
        '==[27,27]':'==[32,32]','==[6457,6457]':'==[7655,7657]',"len(v['selected_intervals'])==15":"len(v['selected_intervals'])==20",
        'single_source_end662':'single_source_end706',"original_source_offset']==662":"original_source_offset']==706",
        "original_source_offset']==660":"original_source_offset']==704",
        'len(rows)==len(set(ids))==15':'len(rows)==len(set(ids))==20','fifteen exact records':'twenty exact records',
        "{'progressive':14,'system-FE':1}":"{'progressive':19,'system-FE':1}","{'revise':8,'retain-wording':7}":"{'revise':3,'retain-wording':17}",
        "mapping['blocks'][0]['block']==193":"mapping['blocks'][0]['block']==195",'old_blocks[193]':'old_blocks[195]','blocks[193]':'blocks[195]',
        "row['source_reference']['block']==193":"row['source_reference']['block']==195","row['block']==193":"row['block']==195",'block=193':'block=195',
        "spec['source_bytes']==len(block)==668 and spec['source_logical_end']==666 and spec['research_bytes']==spec['research_logical_end']==676":
        "spec['source_bytes']==len(block)==712 and spec['source_logical_end']==710 and spec['research_bytes']==spec['research_logical_end']==616",
        'end==666 and len(block)==668':'end==710 and len(block)==712','mapped(end)==676':'mapped(end)==616',
        'len(target)==676 and target[676:]==bytes()':'len(target)==616 and target[616:]==bytes()',
        'len(commands)==18':'len(commands)==23',"sum(c['word']==0x4000 for c in commands)==15":"sum(c['word']==0x4000 for c in commands)==20",
        '==[(662,672)]':'==[(706,612)]',"[(8,'00a0ffff011d39a1'),(660,'00c2'),(662,'00000000')]":"[(8,'00a0ffff010841a1'),(704,'00c2'),(706,'00000000')]",
        'new_blocks[193]':'new_blocks[195]','==[193]':'==[195]','source_commands=18':'source_commands=23',
        'all15_progressive_FE_speeches':'all20_progressive_FE_speeches',
        'actual_two_complete_B22_fixtures_three_portraits_115_regions_59_holds_10_speech_timings_equal_postscene_RGB_and_measured_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_three_roles_115_regions_79_holds_15_timings4_lower_indicator_differences_unequal_PRNG_not_natural_activation'})
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert old-new==Counter({463267532:2}) and new-old==Counter({3942509462:1,3085513495:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_compiler.json',dict(derivation=row,
        native_high_constants_preserved_except_exact_measured_PRNG_data=True,
        complete_source_current_metadata_both_maps_all712_source_bytes_inverse_and_single_mutation_guarded=True,
        source_roles_terms_shared_order_coaxing_taste_claims_intention_two_chewing_beats_and_R17_guarded_rows_required=True,
        actual_timing_indicator_and_PRNG_differences_explicit=True,new_review_credit=0,full_goal_complete=False))
