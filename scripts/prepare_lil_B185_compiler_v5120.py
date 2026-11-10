"""Prepare atomic B185 integration with exact references and source fact gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B185_compiler_tools_v5120')
if __name__=='__main__':
    assert not ROOT.exists()
    text=Path('dk4tool/patch/lil_B184_editorial_v2.py').read_text(encoding='utf-8')
    a=text.index("    terms=load(doc['actor_terminology_reconciliation'])");b=text.index("    require(sample[",a)
    terms="""    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['commodity_index']==56 and terms['commodity']=='Furs' and terms['city']=='Stockholm'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['Stockholm','Stockholm'] and terms['commodity_binding']['text']=='Furs','current Furs and Stockholm bindings required')
    require(terms['source_explicit_reported_current_fur_sales_and_rising_prices_due_to_cold_must_be_preserved']
        and terms['source_couple_roles_do_not_establish_marriage_age_or_kinship'],'source reported prices and role boundaries required')
    wrap=load(doc['source_bound_wrap_refinement_proof'])
    require(sha(Path(doc['source_bound_wrap_refinement_proof']).read_bytes())==doc['source_bound_wrap_refinement_proof_sha256']
        and wrap['only_changed_record_IDs']==['DK4_MES_B185_R0016'] and wrap['all8_words_controls_and_prose_unchanged']
        and wrap['seven_other_compiled_targets_exact'] and wrap['seven_other_native_planes_exact']
        and len(wrap['exact_source_and_prose_mutation_controls'])==6
        and all(r.get('rejected') or r.get('exact_reviewed_boundary_not_inherited') for r in wrap['exact_source_and_prose_mutation_controls']),'exact ordinary-boundary proof required')
    paragraph=next(c for c in native['cases'] if c['id']=='DK4_MES_B185_R0016')
    require([s.strip() for s in bytes.fromhex(paragraph['encoded_hex'])[1:].decode('ascii').splitlines()]==[
        'I hear furs are selling well in','this cold, and prices are going up.'],'reviewed complete reported-market paragraph required')
"""
    r=derive('dk4tool/patch/lil_B184_editorial_v2.py','dk4tool/patch/lil_B185_editorial_v1.py',{
        text[a:b]:terms,'B184':'B185','all12':'all11','all9':'all8','progressive8_impersonal_FE1':'progressive7_impersonal_FE1',
        'single_end428_actual_target412':'single_end384_actual_target372',
        "len(native['cases'])==9":"len(native['cases'])==8","native['current_original_macro_alignment_calls']==72":"native['current_original_macro_alignment_calls']==64",
        "native['complete_progressive_planes']==8":"native['complete_progressive_planes']==7",
        "len(stored['final_target_parity_cases'])==9":"len(stored['final_target_parity_cases'])==8",
        "stored['current_final_stored_macro_alignment_cases']==36":"stored['current_final_stored_macro_alignment_cases']==32",
        "stored['new_parity_macro_alignment_cases']==24":"stored['new_parity_macro_alignment_cases']==16",
        "stored['exact_byte_identical_reused_macro_alignment_cases']==12":"stored['exact_byte_identical_reused_macro_alignment_cases']==16",
        "len(controls['relocated_dispatch_cases'])==9":"len(controls['relocated_dispatch_cases'])==8",
        "[('current',428),('research',412)]":"[('current',384),('research',372)]",
        'all9_panels8_progressive1_FE':'all8_panels7_progressive1_FE','original12_commands':'original11_commands','all9_speeches8_progressive1':'all8_speeches7_progressive1',
        "observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[403514907,403514907]":"not observed['PRNG_equality'] and observed['postscene9001_PRNG_seeds']==[463267532,790984746]",
        'measured equal RNG scope required':'measured unequal RNG scope required',
        "len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==4":"len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==7",
        'later_four_original_A_indicator':'later_seven_original_A_indicator',
        '[(6970,[224,360,240,376]),(7150,[224,360,240,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]':
        '[(5530,[225,371,239,376]),(5710,[225,371,239,376]),(6310,[224,360,240,376]),(6730,[224,360,240,376]),(6910,[224,360,240,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]',
        "len(observed['paired_full_screen_views'])==5":"len(observed['paired_full_screen_views'])==7",
        "actual['fresh_actual_unique_speech_panels']==9":"actual['fresh_actual_unique_speech_panels']==8",'==[21,21]':'==[20,20]','==[5014,5015]':'==[4777,4775]',
        "len(v['selected_intervals'])==9":"len(v['selected_intervals'])==8",'single_source_end428':'single_source_end384',
        "original_source_offset']==428":"original_source_offset']==384","original_source_offset']==426":"original_source_offset']==382",
        'len(rows)==len(set(ids))==9':'len(rows)==len(set(ids))==8','nine exact records':'eight exact records',
        "{'progressive':8,'system-FE':1}":"{'progressive':7,'system-FE':1}","{'revise':4,'retain-wording':5}":"{'revise':4,'retain-wording':4}",
        "mapping['blocks'][0]['block']==184":"mapping['blocks'][0]['block']==185",'old_blocks[184]':'old_blocks[185]','blocks[184]':'blocks[185]',
        "row['block']==184":"row['block']==185","row['source_reference']['block']==184":"row['source_reference']['block']==185",'block=184':'block=185',
        "spec['source_logical_end']==len(block)==432":"spec['source_logical_end']==len(block)==388",
        "spec['research_bytes']==spec['research_logical_end']==416":"spec['research_bytes']==spec['research_logical_end']==376",
        'end==432 and len(block)==432':'end==388 and len(block)==388','mapped(end)==416':'mapped(end)==376','len(target)==416':'len(target)==376',
        'len(commands)==12':'len(commands)==11',"sum(c['word']==0x4000 for c in commands)==9":"sum(c['word']==0x4000 for c in commands)==8",
        '==[(428,412)]':'==[(384,372)]',"[(8,'00a0ffff011f22a1'),(426,'00c2'),(428,'00000000')]":"[(8,'00a0ffff013807a1'),(382,'00c2'),(384,'00000000')]",
        'new_blocks[184]':'new_blocks[185]','==[184]':'==[185]','source_commands=12':'source_commands=11',
        'actual_two_complete_B22_fixtures_115_regions_equal_8_timing_and4_later_indicator_differences_equal_measured_PRNG_not_natural_activation':
        'actual_two_complete_B22_fixtures_115_regions_equal_8_timing_and7_later_indicator_differences_unequal_measured_PRNG_not_natural_activation',
        '        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b\' \' if pad else b\'\'':
        "        if row['source_record_index']==16:\n            require(len(qa.get('reviewed_ordinary_boundaries',[]))==1 and row.get('reviewed_ordinary_boundaries')==qa['reviewed_ordinary_boundaries'],'exact source/prose ordinary-boundary reason required')\n        else:require(not row.get('reviewed_ordinary_boundaries'),'unreviewed boundary reason on other record')\n        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''"})
    ROOT.mkdir(parents=True);save(ROOT/'prepared.json',dict(tool=r,all_source_current_metadata_and_both_command_maps_guarded=True,
        source_explicit_reported_prices_preserved=True,exact_R16_reviewed_ordinary_boundary_reason_required=True,
        no_original_native_getter_call_address_changed=True,new_review_credit=0,full_goal_complete=False))
