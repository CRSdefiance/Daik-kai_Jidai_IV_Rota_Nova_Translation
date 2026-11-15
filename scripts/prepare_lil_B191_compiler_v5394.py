"""Freeze atomic integration for mixed thresholds,no-effect gameplay and R64 wrap."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B191_seal_v5393 import FLAGS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B191_compiler_tools_v5394')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('dk4tool/patch/lil_B190_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    c=text.index("    require(names['progressive_nameplate_values']");e=text.index('    carry=load',c)
    terms=read('work/analysis/lil_B191_terms_v5364b/Square_Shopkeeper_Sailor_Calicut_Dyes_and_persuasive_claims.json');termflags=[k for k,v in terms.items() if v is True]
    roles="""    require(names['progressive_nameplate_values']=={'86':'Square Shopkeeper','154':'Sailor'}
        and names['full_catalogue_values']=={'86':'Square Shopkeeper','154':'Retainer'},'distinct source names required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        ('progressive-nameplate',86):'Square Shopkeeper',('full-catalogue',86):'Square Shopkeeper',
        ('progressive-nameplate',154):'Sailor',('full-catalogue',154):'Retainer'}
        and all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in names['native_four_consumer_cases']['rows']),'four original name consumers required')
    voice=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voice['fresh2_actor_names']['rows']}=={86:0,154:4},'original Shopkeeper/Sailor voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']=={'86':'Square Shopkeeper','154':'Sailor'}
        and terms['full_catalogue_names']=={'86':'Square Shopkeeper','154':'Retainer'} and terms['city']=='Calicut'
        and [(r['source_text'],r['text']) for r in terms['two_source_current_city_aliases']]==[('カリカット','Calicut')]*2
        and terms['category_index']==14 and terms['source_category']=='染料' and terms['approved_full_category']==terms['compact_UI_category']=='Dyes'
        and [r['text'] for r in terms['current_category_binding']['rows']]==['Dyes']*6 and len(terms['all12_category14_native_bindings'])==12,'source category14 and two city aliases required')
    for flag in TERM_FLAGS:require(terms.get(flag) is True,'whole-exchange source context required:'+flag)
    require(doc['exact_source_prose_R64_after_be_boundary_reviewed'] and not doc['no_record_specific_ordinary_boundary_exception_required'],'exact R64 boundary approval required')
    wrap=load(doc['source_bound_wrap_refinement_proof'])
    require(wrap['only_changed_record_IDs']==['DK4_MES_B191_R0064'] and wrap['all13_words_controls_and_prose_unchanged']
        and wrap['twelve_other_compiled_targets_exact'] and wrap['twelve_other_native_planes_exact']
        and len(wrap['exact_source_and_prose_mutation_controls'])==6
        and all(r.get('rejected') or r.get('exact_reviewed_boundary_not_inherited') for r in wrap['exact_source_and_prose_mutation_controls']),'exact source/prose wrap proof required')
    layout=load(doc['layout_retention_review_proof'])
    require(layout['all13_panels_on_two_native_sheets_viewed_after_image_return'] and {r['id'] for r in layout['retained_layouts']}=={
        'DK4_MES_B191_R0056','DK4_MES_B191_R0064','DK4_MES_B191_R0068','DK4_MES_B191_R0072','DK4_MES_B191_R0088'}
        and all(r['reason'] for r in layout['retained_layouts']),'individual native layout reasons required')
""".replace('TERM_FLAGS',repr(termflags))
    aa=text.index("    require({(r['version'],r['offset'],r['supplied_CPU_only_seed_fixture'])");bb=text.index('    for r in ownership[',aa)
    coverage="""    require(len({(r['version'],r['offset'],r['supplied_CPU_only_seed_fixture']) for r in ownership['cases']})==36
        and Counter((r['version'],r['offset']) for r in ownership['cases'])=={(v,at):4 for v in ['clean','current','relocated'] for at in [8,28,76]},'exact mixed-predicate coverage keys required')
    for r in ownership['cases']:
        require((r['supplied_CPU_only_seed_fixture'] is None)==r['unforced_current_snapshot']
            and (r['unforced_current_snapshot'] or r['before_seed']==r['supplied_CPU_only_seed_fixture']),'CPU fixture provenance differs')
"""
    ca=text.index("    require({r['roll'] for r in ownership['cases']");cb=text.index("    ui=controls[",ca)
    boundaries="""    for version in ['clean','current','relocated']:
        for at,threshold in [(8,500),(28,700),(76,500)]:
            group=[r for r in ownership['cases'] if r['version']==version and r['offset']==at]
            require(len(group)==4 and sum(r['unforced_current_snapshot'] for r in group)==1
                and {r['roll'] for r in group if not r['unforced_current_snapshot']}=={threshold-1,threshold,threshold+1},'three native threshold boundary classes per site required')
"""
    oa=text.index("    require(observed['PRNG_equality'] is True");ob=text.index('    actual=load',oa)
    observed="""    require(observed['PRNG_equality'] is False and observed['postscene9001_PRNG_seeds']==[759362961,1803218166]
        and observed['future_world_equivalence_and_full_RAM_equality_not_claimed'],'measured unequal final RNG and limits required')
    require([(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (6730,[225,371,239,376]),(6910,[225,371,239,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]
        and observed['twelve_timing_four_indicator_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim']
        and observed['original_carried_result2_C200_3_2_and_end_0_2_preserved']
        and observed['both_actual_rolls875_988_at8_76_return2_skip700_at28_and_apply_no_source_A000']
        and observed['four_source_effect_alternatives_native_structural_only_not_actually_executed'],'all measured no-effect/timing/state scope required')
    require(len(observed['all_actual_consumer_sheets_viewed'])==3 and len(observed['paired_full_screen_views'])==5
        and all(s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all_actual_consumer_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==2 and observed['total_frames']==18002,'viewed current evidence required')
"""
    xa=text.index('    actual=load');xb=text.index("    require([{k:s[k]",xa)
    actual="""    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==13
        and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'all13 actual panels required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[34,34]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[5977,5975]
        and actual['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[],reviewed_English=[]),'original no-effect paths required')
    for version in actual['versions']:
        require(len(version['selected_intervals'])==13 and version['single_source_end730_actually_reached']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,2]
            and version['selected_B22_command_pairs'][-1]['original_source_offset']==730
            and not version['source_A000'] and len(version['source_C200'])==1
            and version['source_C200'][0]['word']==0xC200 and version['source_C200'][0]['original_source_offset']==728
            and version['source_C200'][0]['result_words']==[3,2] and version['source_C200'][0]['UI_request_after']==[1,2,13,0,2,0,1],'actual no-effect/UI/end controls differ')
        require([(r['source_offset'],r['roll'],r['result'],r['threshold']) for r in version['actual_predicate_transitions']]==[(8,875,2,500),(76,988,2,500)]
            and all(r['actual_unforced_original_LCG_transition'] for r in version['actual_predicate_transitions']),'two original actual draws and skipped700 site required')
"""
    boundary="""        if row['source_record_index']==64:
            require(len(qa.get('reviewed_ordinary_boundaries',[]))==1 and row.get('reviewed_ordinary_boundaries')==qa['reviewed_ordinary_boundaries']
                and qa['reviewed_ordinary_boundaries'][0]['after_word']=='be'
                and qa['visible_lines']==["What are you waiting for? It'll be","too late once it's sold out."],'exact source/prose R64 soft wrap reason required')
        else:require(not row.get('reviewed_ordinary_boundaries') and not qa.get('reviewed_ordinary_boundaries'),'unreviewed ordinary boundary on another record')
"""
    row=derive(source,'dk4tool/patch/lil_B191_editorial_v1.py',{
        text[a:b]:'FLAGS='+repr(FLAGS)+'\n',text[c:e]:roles,text[aa:bb]:coverage,text[ca:cb]:boundaries,text[oa:ob]:observed,text[xa:xb]:actual,
        "        require(not row.get('reviewed_ordinary_boundaries') and not qa.get('reviewed_ordinary_boundaries'),'no inherited boundary exceptions')\n":boundary,
        'B190':'B191','lil_B190_layout_v1':'lil_B191_layout_v3','SELECTORS={119,159,254}':'SELECTORS={86,154,254}',
        "'layout_retention_review_proof','carried_result_proof']":"'layout_retention_review_proof','carried_result_proof','source_bound_wrap_refinement_proof']",
        "len(native['cases'])==17 and native['current_original_macro_alignment_calls']==136":"len(native['cases'])==13 and native['current_original_macro_alignment_calls']==104","native['complete_progressive_planes']==16":"native['complete_progressive_planes']==12",
        "len(stored['final_target_parity_cases'])==17 and stored['current_final_stored_macro_alignment_cases']==68":"len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52",
        "stored['new_parity_macro_alignment_cases']==40 and stored['exact_byte_identical_reused_macro_alignment_cases']==28":"stored['new_parity_macro_alignment_cases']==12 and stored['exact_byte_identical_reused_macro_alignment_cases']==40",'all17_final_targets':'all13_final_targets',
        "len(controls['relocated_dispatch_cases'])==17 and len(controls['all6_exact_nonrelative_leaves'])==6":"len(controls['relocated_dispatch_cases'])==13 and len(controls['all9_exact_nonrelative_leaves'])==9",
        "len(controls['predicate_pairs'])==1":"len(controls['predicate_pairs'])==3","len(controls['A000_structural_pairs'])==3":"len(controls['A000_structural_pairs'])==4",
        "len(controls['all5_source_and_relocated_structural_paths_identical'])==5":"len(controls['all125_source_and_relocated_structural_paths_identical'])==125",'==[(8,8)]':'==[(8,8),(28,28),(76,76)]',
        "        a,b=pair['cases'];require":"        threshold={8:500,28:700,76:500}[pair['old_offset']]\n        require(all(r['threshold']==threshold for r in pair['cases']),'source raw threshold differs')\n        a,b=pair['cases'];require",
        'value=500':'value=threshold',"len(ownership['cases'])==12 and ownership['unforced_cases']==3 and ownership['CPU_only_boundary_fixture_cases']==9":"len(ownership['cases'])==36 and ownership['unforced_cases']==9 and ownership['CPU_only_boundary_fixture_cases']==27",
        "{'clean':4,'current':4,'relocated':4}":"{'clean':12,'current':12,'relocated':12}",
        "        expected_seed=(r['before_seed']":"        threshold={8:500,28:700,76:500}[r['offset']]\n        expected_seed=(r['before_seed']",'roll<500':'roll<threshold','roll==500':'roll==threshold',"r['threshold']==500":"r['threshold']==threshold",
        "[('current',602),('research',698)]":"[('current',730),('research',676)]",
        'all17_panels_sixteen_progressive_one_FE_selected_effect':'all13_panels_twelve_progressive_one_FE_original_no_effect_path',
        'source_all29_commands_six_branches_one_predicate_three_alternative_effects':'source_all38_commands_16_branches_three_mixed_predicates_four_alternative_effects_and_no_effect_paths',
        'original_scene_result2_carried_through_UI_and_end_timing_shadow_differences_disclosed':'original_scene_two_unforced500_draws_skip700_and_no_A000_preserved',
        'all17_complete_held_planes':'all13_complete_held_planes','all17_speeches16_progressive1':'all13_speeches12_progressive1','dict(total=9,speech=7,control_or_end=2)':'dict(total=12,speech=10,control_or_end=2)',"len(observed['actual_timing_differences'])==9":"len(observed['actual_timing_differences'])==12",
        'len(rows)==len(set(ids))==17':'len(rows)==len(set(ids))==13','seventeen exact records':'thirteen exact records',"{'progressive':16,'system-FE':1}":"{'progressive':12,'system-FE':1}","{'revise':10,'retain-wording':7}":"{'revise':5,'retain-wording':8}",
        "mapping['blocks'][0]['block']==190":"mapping['blocks'][0]['block']==191",'old_blocks[190]':'old_blocks[191]','.blocks[190]':'.blocks[191]',
        "spec['source_bytes']==len(block)==608 and spec['source_logical_end']==606":"spec['source_bytes']==len(block)==736 and spec['source_logical_end']==734",
        "spec['research_bytes']==704 and spec['research_logical_end']==702":"spec['research_bytes']==680 and spec['research_logical_end']==680",
        "row['source_reference']['block']==190":"row['source_reference']['block']==191","row['block']==190":"row['block']==191",'block=190':'block=191','end == 606 and len(block)==608':'end == 734 and len(block)==736',
        "len(edges)==6 and [e['offset'] for e in edges]==[16,20,24,36,48,60]":"len(edges)==16 and [e['offset'] for e in edges]==[16,20,24,36,40,44,56,68,72,84,88,92,104,116,120,124]",
        "len(spec['target_native_skip_cases'])==30 and len(logical)==mapped(end)==702":"len(spec['target_native_skip_cases'])==80 and len(logical)==mapped(end)==680",
        "len(target)==704 and target[702:]==bytes(2)":"len(target)==680 and target[680:]==bytes() and target[6:128]==block[6:128]",
        'len(commands) == 29':'len(commands) == 38',"sum(command['word'] == 0x4000 for command in commands) == 17":"sum(command['word'] == 0x4000 for command in commands) == 13",
        "[c['old_offset'] for c in stops]==[602] and len(stops)==1 and stops[0]['new_offset']==698":"[c['old_offset'] for c in stops]==[730] and len(stops)==1 and stops[0]['new_offset']==676",'target[698:702]':'target[676:680]',
        "exact=[(8,'0080fffff4010000'),(28,'00a0ffff014c41a1'),(40,'00a0ffff014b41a1'),\n        (52,'00a0ffff014d41a1'),(600,'00c2'),(602,'00000000')]":"exact=[(8,'0080fffff4010000'),(28,'0080ffffbc020000'),(48,'00a0ffff01512aa1'),(60,'00a0ffff01522aa1'),\n        (76,'0080fffff4010000'),(96,'00a0ffff01542aa1'),(108,'00a0ffff01552aa1'),(728,'00c2'),(730,'00000000')]",
        'six complete source leaves':'nine complete source leaves','[0x8000,0xA000,0xA000,0xA000,0xC200,0]':'[0x8000,0x8000,0xA000,0xA000,0x8000,0xA000,0xA000,0xC200,0]',
        'new_blocks[190]':'new_blocks[191]','== [190]':'== [191]','relative_operands=6, source_commands=29':'relative_operands=16, source_commands=38',
        'all17_progressive_FE_speeches_one500_predicate_three_A000_C200_six_relative_sites_and6_leaves_preserved':'all13_progressive_FE_speeches_three_mixed_predicates_four_A000_C200_16_relative_sites9_leaves_and_no_effect_paths_preserved',
    })
    before,after=native_numbers(text),native_numbers(Path(row['successor']).read_text(encoding='utf-8'))
    assert before-after==Counter({2467799992:2}) and after-before==Counter({759362961:1,1803218166:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_mixed_conditional_compiler.json',dict(derivation=row,
        native_high_constants_preserved_except_measured_final_PRNG_data=True,all_three_site_specific_thresholds_and36_exact_cases_guarded=True,
        no_effect_actual_scope_distinct_from_four_offline_alternatives=True,exact_R64_wrap_source_prose_and_six_mutations_guarded=True,
        complete_metadata_both_maps_source_tailzeros_and_zero_target_tail_guarded=True,all_checks_precede_single_mutation=True,no_credit=True,full_goal_complete=False))
