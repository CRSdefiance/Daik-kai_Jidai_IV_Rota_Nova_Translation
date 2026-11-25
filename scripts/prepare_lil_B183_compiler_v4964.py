"""Derive a source-locked atomic B183 compiler without changing frozen compilers."""
from pathlib import Path
from scripts.prepare_lil_B181_compiler_v4865 import alter
from scripts.seal_lil_B183_references_v4963b import FLAGS
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B183_compiler_tools_v4964')
OUT=Path('dk4tool/patch/lil_B183_editorial_v1.py')
NAMES="""    expected_names={'85':'Square Shopkeeper','110':'Shipwright','132':'Priest','148':'Guildmaster','153':'Sailor'}
    require(names['progressive_nameplate_values']==expected_names and names['full_catalogue_values']=={**expected_names,'153':'Retainer'},'progressive and catalogue role distinction required')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_ten_consumer_cases']['rows']}=={
        (c,int(i)):('Retainer' if c=='full-catalogue' and i=='153' else text) for i,text in expected_names.items() for c in ['progressive-nameplate','full-catalogue']},'ten original role consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh5_actor_names']['rows']}=={85:0,110:0,132:0,148:0,153:4},'five original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['commodity_index']==57 and terms['commodity']=='Artwork' and terms['city']=='Basra'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Basra','Basra'] and terms['commodity_binding']['text']=='Artwork','current Artwork and Basra bindings required')
    wrap=load(doc['source_bound_wrap_refinement_proof'])
    require(sha(Path(doc['source_bound_wrap_refinement_proof']).read_bytes())==doc['source_bound_wrap_refinement_proof_sha256']
        and wrap['only_changed_record_IDs']==['DK4_MES_B183_R0035'] and wrap['all25_words_controls_and_prose_unchanged']
        and wrap['all24_other_compiled_targets_and_native_planes_exact'],'fitting-question wrap proof required')
    question=next(c for c in native['cases'] if c['id']=='DK4_MES_B183_R0035')
    require([s.strip() for s in bytes.fromhex(question['encoded_hex'])[1:].decode('ascii').splitlines()]==[
        'What are you two talking about?','That one over there','is obviously better!'],'intact fitting question and locative required')
"""

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    source=Path('dk4tool/patch/lil_B181_editorial_v1.py');text=source.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a);text=text[:a]+'FLAGS='+repr(FLAGS)+'\n'+text[b:]
    a=text.index("    require(names['approved_prose_names']");b=text.index("    require(sample[",a);text=text[:a]+NAMES+text[b:]
    text=alter(text,{
        'B181':'B183','lil_B181_layout_v1':'lil_B183_layout_v3','SELECTORS={166,167,168,254}':'SELECTORS={85,110,132,148,153,254}',
        "len(native['cases'])==10":"len(native['cases'])==25",'current_original_macro_alignment_calls\']==80':"current_original_macro_alignment_calls']==200",
        "native['complete_progressive_planes']==9":"native['complete_progressive_planes']==23","native['complete_FE_logical_and_physical_planes']==1":"native['complete_FE_logical_and_physical_planes']==2",
        "len(native['negative_controls'])==20":"len(native['negative_controls'])==24",
        "len(stored['final_target_parity_cases'])==10":"len(stored['final_target_parity_cases'])==25",
        "stored['current_final_stored_macro_alignment_cases']==40":"stored['current_final_stored_macro_alignment_cases']==100",
        "stored['new_parity_macro_alignment_cases']==12":"stored['new_parity_macro_alignment_cases']==64",
        "stored['exact_byte_identical_reused_macro_alignment_cases']==28":"stored['exact_byte_identical_reused_macro_alignment_cases']==36",
        'all10_final_targets':'all25_final_targets',"len(controls['relocated_dispatch_cases'])==10":"len(controls['relocated_dispatch_cases'])==25",
        "[('current',392),('research',376)]":"[('current',952),('research',1050)]",
        'all10_panels9_progressive1_FE':'all25_panels23_progressive2_FE','original13_commands':'original28_commands',
        'all10_complete_held':'all25_complete_held','all10_speeches9_progressive1':'all25_speeches23_progressive2',
        "len(observed['all115_sampled_nontext_region_checks'])==115":"len(observed['all149_sampled_nontext_region_checks'])==149",
        '9001':'11001',
        "dict(total=0,speech=0,control_or_end=0) and not observed['actual_timing_differences']":"dict(total=11,speech=9,control_or_end=2) and len(observed['actual_timing_differences'])==11",
        "observed['PRNG_equality']":"not observed['PRNG_equality']",'[790984746,790984746]':'[1228390232,713326998]',
        'measured equal RNG scope required':'measured unequal RNG scope required',
        "len(observed['all2_actual_sheets_viewed'])==2":"len(observed['all5_actual_sheets_viewed'])==5",
        "observed['all2_actual_sheets_viewed']":"observed['all5_actual_sheets_viewed']",
        "len(observed['paired_full_screen_views'])==3":"len(observed['paired_full_screen_views'])==4",'==18002':'==22002',
        "actual['fresh_actual_unique_speech_panels']==10":"actual['fresh_actual_unique_speech_panels']==25",'==[22,22]':'==[37,37]','==[5257,5257]':'==[8855,8854]',
        "len(v['selected_intervals'])==10":"len(v['selected_intervals'])==25",'single_source_end392':'single_source_end952',
        "original_source_offset']==392":"original_source_offset']==952","original_source_offset']==390":"original_source_offset']==950",
        'len(rows)==len(set(ids))==10':'len(rows)==len(set(ids))==25','ten exact records':'25 exact records',
        "{'progressive':9,'system-FE':1}":"{'progressive':23,'system-FE':2}","{'revise':5,'retain-wording':5}":"{'revise':16,'retain-wording':9}",
        "mapping['blocks'][0]['block']==181":"mapping['blocks'][0]['block']==183",'[181]':'[183]',"row['block']==181":"row['block']==183",'block=181':'block=183',
        'end==396 and len(block)==396':'end==956 and len(block)==956','len(logical)==mapped(end)==380':'len(logical)==mapped(end)==1054','len(target)==380':'len(target)==1056',
        'len(commands)==13':'len(commands)==28',"sum(c['word']==0x4000 for c in commands)==10":"sum(c['word']==0x4000 for c in commands)==25",'==[(392,376)]':'==[(952,1050)]',
        "[(8,'00a0ffff014913a1'),(390,'00c2'),(392,'00000000')]":"[(8,'00a0ffff013926a1'),(950,'00c2'),(952,'00000000')]",
        'source_commands=13':'source_commands=28','all10_progressive_FE_speeches':'all25_progressive_FE_speeches',
        'actual_two_retained_B22_fixtures_115_regions_equal_zero_timing_or_RGB_differences_and_equal_PRNG_not_natural_activation':
        'actual_two_retained_B22_fixtures_149_regions_equal_11_timing_differences_no_postscene_RGB_difference_unequal_PRNG_not_natural_activation',
    })
    compile(text,str(OUT),'exec');OUT.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),compiler=str(OUT),compiler_sha256=sha(OUT.read_bytes()),
        all_checks_precede_single_replace_file=True,source956_target1056_logical1054_commands28_speeches25_three_leaves=True,
        source_bound_layout_v3_fitting_question_and_five_roles_two_FE_preserved=True,no_registry_ROM_or_credit_change=True,full_goal_complete=False))
