"""Derive atomic B179 compilation with separate Sailor/catalog identity and no C200."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_compiler_tools_v4747')
assert not ROOT.exists()
source=Path('dk4tool/patch/lil_B178_editorial_v2.py');text=source.read_text(encoding='utf-8')
doc=read('translations/lil_B179_editorial_manuscript_v4.json');visual=read(doc['postscene_native_state_proof'])
timings=[(r['source']['original_source_offset'],r['source']['start'],r['source']['returned'],r['English']['start'],r['English']['returned'])
         for r in visual['actual_timing_differences']]
assert len(timings)==8 and visual['exact_timing_difference_counts']=={'total':8,'speech':7,'control_or_end':1}
start=text.index("    ui=controls['relocated_C200_pairs'][0]");end=text.index("    require(ends[",start)
old_timing=text[text.index("    expected_timings="):text.index('    indicator=',text.index("    expected_timings="))]
new_timing="""    expected_timings=TIMINGS
    require([(r['source']['original_source_offset'],r['source']['start'],r['source']['returned'],r['English']['start'],r['English']['returned'])
        for r in timings]==expected_timings and all(r['source']['original_source_offset']==r['English']['original_source_offset']
        and r['source']['word']==r['English']['word']==(0 if r['source']['original_source_offset']==508 else 0x4000) for r in timings)
        and observed['exact_timing_difference_counts']=={'total':8,'speech':7,'control_or_end':1},
        'all eight exact command timings must remain disclosed')
""".replace('TIMINGS',repr(timings))
old_names="""    expected_names={'166':'Lady','167':'Lady','168':'Lady'}
    require(names['approved_prose_names']==names['progressive_nameplate_values']==names['full_catalogue_values']==expected_names,'source-bound role labels differ')"""
new_names="""    expected_names={'92':'Barkeep','96':'Patron','152':'Sailor'}
    expected_catalog={'92':'Barkeep','96':'Patron','152':'Retainer'}
    require(names['approved_prose_names']==names['progressive_nameplate_values']==expected_names
        and names['full_catalogue_values']==expected_catalog,'separate source-bound dialogue/catalog role labels differ')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_six_consumer_cases']['rows']}=={
        ('progressive-nameplate',92):'Barkeep',('progressive-nameplate',96):'Patron',('progressive-nameplate',152):'Sailor',
        ('full-catalogue',92):'Barkeep',('full-catalogue',96):'Patron',('full-catalogue',152):'Retainer'},'individual source name consumers differ')"""
tool=derive(source,'dk4tool/patch/lil_B179_editorial_v1.py',{
    text[start:end]:"    require(controls['relocated_C200_pairs']==[],'source has no C200 consumer')\n",
    old_timing:new_timing,old_names:new_names,
    'lil_B178_layout_v1':'lil_B179_layout_v1','lil_B178':'lil_B179','B178':'B179',
    'SELECTORS={166,167,168,254}':'SELECTORS={92,96,152,254}',
    'all13':'all14','all12_progressive':'all13_progressive',
    'all3_leaves_one_A000_C200_and_single_end_exact':'all2_leaves_one_A000_and_single_end_no_C200_exact',
    'progressive12_impersonal_FE1':'progressive13_impersonal_FE1',
    'single_end490_actual_target452_offline':'single_end508_actual_target492_offline',
    "len(native['cases'])==13 and native['current_original_macro_alignment_calls']==104":
        "len(native['cases'])==14 and native['current_original_macro_alignment_calls']==112",
    "(native['progressive_planes'],native['FE_planes'])==(12,1)":"(native['progressive_planes'],native['FE_planes'])==(13,1)",
    "len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52":
        "len(stored['final_target_parity_cases'])==14 and stored['current_final_stored_macro_alignment_cases']==56",
    "stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==24":
        "stored['new_parity_macro_alignment_cases']==20 and stored['exact_byte_identical_reused_macro_alignment_cases']==36",
    "len(controls['relocated_dispatch_cases'])==13 and len(controls['all3_source_current_target_nonrelative_nonspeech_leaves'])==3":
        "len(controls['relocated_dispatch_cases'])==14 and len(controls['all2_source_current_target_nonrelative_nonspeech_leaves'])==2",
    "len(controls['relocated_C200_pairs'])==len(controls['relocated_A000_structural_pairs'])==1":
        "len(controls['relocated_C200_pairs'])==0 and len(controls['relocated_A000_structural_pairs'])==1",
    "[('current',490),('research',452)]":"[('current',508),('research',492)]",
    'all13_panels12_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_parent_return_pass':
        'all14_panels13_progressive1_impersonal_FE_source_A000_single_end_no_C200_and_normal_parent_return_pass',
    'source_end490_actual_target452_offline_and_fixture_end_actual':'source_end508_actual_target492_offline_and_fixture_end_actual',
    'all115_upper_portrait_name_samples_equal_and14_command_timing_differences_retained':
        'all115_upper_portrait_name_samples_equal_and8_command_timing_differences_retained',
    'PRNG3306586022':'PRNG403514907','[3306586022,3306586022]':'[403514907,403514907]',
    'all13_speeches12_progressive1':'all14_speeches13_progressive1',
    'source_A0008_C200488_single_end490_actually_executed':'source_A0008_single_end508_actually_executed_no_C200',
    "len(observed['paired_full_screen_views'])==4":"len(observed['paired_full_screen_views'])==5",
    "for s in observed['paired_full_screen_views'])==16":"for s in observed['paired_full_screen_views'])==20",
    'actual_all13_progressive_FE_A000_C200_and_single_end.json':'actual_all14_progressive_FE_A000_and_single_end_no_C200.json',
    "actual['fresh_actual_unique_speech_panels']==13":"actual['fresh_actual_unique_speech_panels']==14",
    '[5977,5976]':'[6216,6215]',"len(version['selected_intervals'])==13":"len(version['selected_intervals'])==14",
    'single_source_end490_actually_reached':'single_source_end508_actually_reached',
    "['original_source_offset']==490":"['original_source_offset']==508",
    "and version['source_C200']['original_source_offset']==488 and version['source_C200']['result_words']==[3,0]\n            and version['source_C200']['word']==0xC200 and version['source_C200']['extent']==2":
        "and version['source_C200']==[]",
    'len(rows)==len(set(ids))==13':'len(rows)==len(set(ids))==14','thirteen exact records':'fourteen exact records',
    "=={'progressive':12,'system-FE':1}":"=={'progressive':13,'system-FE':1}",
    "=={'revise':2,'retain-wording':11}":"=={'revise':8,'retain-wording':6}",
    "mapping['blocks'][0]['block']==178":"mapping['blocks'][0]['block']==179",'[178]':'[179]',
    "row['block']==178":"row['block']==179",'block=178':'block=179',
    'end==494 and len(block)==496':'end==512 and len(block)==512',
    'len(logical)==mapped(end)==456':'len(logical)==mapped(end)==496','len(target)==456':'len(target)==496',
    "sum(c['word']==0x4000 for c in commands)==13":"sum(c['word']==0x4000 for c in commands)==14",
    '==[(490,452)]':'==[(508,492)]',
    "exact=[(8,'00a0ffff010002a1'),(488,'00c2'),(490,'00000000')]":
        "exact=[(8,'00a0ffff01221da1'),(508,'00000000')]",
    'three exact leaves required':'two exact leaves required','[0xA000,0xC200,0]':'[0xA000,0]',
    'all13_progressive_impersonal_FE_speeches_no_macros_A000_C200_and_single_end_preserved':
        'all14_progressive_impersonal_FE_speeches_no_macros_A000_and_single_end_no_C200_preserved',
    '115_regions_equal_14_timings_4_indicator':'115_regions_equal_8_timings_4_indicator',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,all_checks_readonly_until_single_replace_file=True,
    source512_target496_A0008_end508_target492_no_C200=True,progressive_Sailor152_and_catalog_Retainer152_guarded=True,
    exact8_timings4_indicator_boxes112_native56_stored_and51_negatives_bound=True,
    no_registry_builder_ROM_orledger_change=True,full_goal_complete=False))
print('Prepared B179 atomic compiler; separate native name consumers,no C200,fresh actual limits guarded.')
