"""Freeze an atomic source-locked B184 compiler with exact reference metadata."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B184_compiler_tools_v5074')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/lil_B183_editorial_v1.py').read_text(encoding='utf-8')
    start=source.index('    expected_names=');end=source.index("    require(sample[",start)
    names="""    expected_names={'164':'Man in a Couple','165':'Woman in a Couple'}
    require(names['progressive_nameplate_values']==names['full_catalogue_values']==expected_names,'couple roles required without marital inference')
    require({(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
        (c,int(i)):text for i,text in expected_names.items() for c in ['progressive-nameplate','full-catalogue']},'four original role consumers required')
    voices=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voices['fresh2_actor_names']['rows']}=={164:0,165:0},'two original source voices required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['commodity_index']==31 and terms['commodity']=='Tea' and terms['city']=='Sofala'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Sofala','Sofala'] and terms['commodity_binding']['text']=='Tea','current Tea and Sofala bindings required')
    require(terms['household_tea_is_low_not_city_or_trade_cargo_shortage'] and terms['source_couple_roles_do_not_establish_marriage_age_or_kinship'],'source fact boundaries required')
    wrap=load(doc['source_bound_wrap_refinement_proof'])
    require(sha(Path(doc['source_bound_wrap_refinement_proof']).read_bytes())==doc['source_bound_wrap_refinement_proof_sha256']
        and wrap['only_changed_record_IDs']==['DK4_MES_B184_R0014'] and wrap['all9_words_controls_and_prose_unchanged']
        and wrap['eight_other_compiled_targets_exact'] and len(wrap['exact_source_and_prose_mutation_controls'])==6,'exact ordinary-boundary proof required')
    paragraph=next(c for c in native['cases'] if c['id']=='DK4_MES_B184_R0014')
    require([s.strip() for s in bytes.fromhex(paragraph['encoded_hex'])[1:].decode('ascii').splitlines()]==[
        "It's strange that something this","delicious didn't catch on sooner."],'reviewed whole paragraph required')
"""
    changes={source[start:end]:names,
        'B183':'B184','lil_B183_layout_v3':'lil_B184_layout_v2','SELECTORS={85,110,132,148,153,254}':'SELECTORS={164,165,254}',
        'all28':'all12','all25':'all9','progressive23_impersonal_FE2':'progressive8_impersonal_FE1',
        'single_end952_actual_target1050':'single_end428_actual_target412',
        "len(native['cases'])==25":"len(native['cases'])==9","native['current_original_macro_alignment_calls']==200":"native['current_original_macro_alignment_calls']==72",
        "native['complete_progressive_planes']==23":"native['complete_progressive_planes']==8","native['complete_FE_logical_and_physical_planes']==2":"native['complete_FE_logical_and_physical_planes']==1",
        "len(native['negative_controls'])==24":"len(native['negative_controls'])==18",
        "len(stored['final_target_parity_cases'])==25":"len(stored['final_target_parity_cases'])==9",
        "stored['current_final_stored_macro_alignment_cases']==100":"stored['current_final_stored_macro_alignment_cases']==36",
        "stored['new_parity_macro_alignment_cases']==64":"stored['new_parity_macro_alignment_cases']==24",
        "stored['exact_byte_identical_reused_macro_alignment_cases']==36":"stored['exact_byte_identical_reused_macro_alignment_cases']==12",
        "len(controls['relocated_dispatch_cases'])==25":"len(controls['relocated_dispatch_cases'])==9",
        "[('current',952),('research',1050)]":"[('current',428),('research',412)]",
        'all25_panels23_progressive2_FE':'all9_panels8_progressive1_FE','original28_commands':'original12_commands',
        'all25_speeches23_progressive2':'all9_speeches8_progressive1',
        "len(observed['all149_sampled_nontext_region_checks'])==149":"len(observed['all115_sampled_nontext_region_checks'])==115",
        'postscene11001':'postscene9001','whole_RGB_final11001':'whole_RGB_final9001',
        "observed['nontext_equal_samples']==len(observed['all149_sampled_nontext_region_checks'])==149":"observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115",
        'dict(total=11,speech=9,control_or_end=2)':'dict(total=8,speech=6,control_or_end=2)',"len(observed['actual_timing_differences'])==11":"len(observed['actual_timing_differences'])==8",
        "not observed['PRNG_equality']":"observed['PRNG_equality']",'[1228390232,713326998]':'[403514907,403514907]','measured unequal RNG scope required':'measured equal RNG scope required',
        "not observed['sampled_postscene_whole_RGB_differences_unmasked'] and observed['all_sampled_postscene_whole_RGB_equal']":
        "len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==4 and not observed['all_sampled_postscene_whole_RGB_equal'] and observed['later_four_original_A_indicator_differences_reviewed_without_masking_or_retiming'] and [(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[(6970,[224,360,240,376]),(7150,[224,360,240,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]",
        "len(observed['all5_actual_sheets_viewed'])==5 and len(observed['paired_full_screen_views'])==4":"len(observed['all2_actual_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==5",
        "observed['all5_actual_sheets_viewed']":"observed['all2_actual_sheets_viewed']",'==22002':'==18002',
        "actual['fresh_actual_unique_speech_panels']==25":"actual['fresh_actual_unique_speech_panels']==9",'==[37,37]':'==[21,21]','==[8855,8854]':'==[5014,5015]',
        "len(v['selected_intervals'])==25":"len(v['selected_intervals'])==9",'single_source_end952':'single_source_end428',
        "original_source_offset']==952":"original_source_offset']==428","original_source_offset']==950":"original_source_offset']==426",
        'len(rows)==len(set(ids))==25':'len(rows)==len(set(ids))==9','25 exact records':'nine exact records',
        "{'progressive':23,'system-FE':2}":"{'progressive':8,'system-FE':1}","{'revise':16,'retain-wording':9}":"{'revise':4,'retain-wording':5}",
        "mapping['blocks'][0]['block']==183":"mapping['blocks'][0]['block']==184",'old_blocks[183]':'old_blocks[184]','blocks[183]':'blocks[184]',
        "row['block']==183":"row['block']==184",'block=183':'block=184',
        'end==956 and len(block)==956':'end==432 and len(block)==432','mapped(end)==1054':'mapped(end)==416','len(target)==1056':'len(target)==416',
        'len(commands)==28':'len(commands)==12',"sum(c['word']==0x4000 for c in commands)==25":"sum(c['word']==0x4000 for c in commands)==9",
        '==[(952,1050)]':'==[(428,412)]',"[(8,'00a0ffff013926a1'),(950,'00c2'),(952,'00000000')]":"[(8,'00a0ffff011f22a1'),(426,'00c2'),(428,'00000000')]",
        'new_blocks[183]':'new_blocks[184]','==[183]':'==[184]','source_commands=28':'source_commands=12',
        'actual_two_retained_B22_fixtures_149_regions_equal_11_timing_differences_no_postscene_RGB_difference_unequal_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_115_regions_equal_8_timing_and4_later_indicator_differences_equal_measured_PRNG_not_natural_activation',
        "        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])":
        "        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])\n        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5 and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'complete source/current reference metadata differs:'+ident)"}
    assert all(k in source for k in changes),[k for k in changes if k not in source]
    tool=derive('dk4tool/patch/lil_B183_editorial_v1.py','dk4tool/patch/lil_B184_editorial_v1.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'atomic_compiler_provenance.json',dict(tool=tool,source_end428_maps412=True,source432_target416_logical_and_stored=True,
        all_checks_precede_single_mutation=True,four_later_indicator_differences_retained_without_masking=True,
        complete_source_current_reference_header_and_length_metadata_guarded=True,new_review_credit=0,full_goal_complete=False))
