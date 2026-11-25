"""Prepare original event entry,all source branches/queries andfull normal-end coverage."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/prove_Rafael_B48_source_controls_v8024.py','scripts/prove_Rafael_B49_source_controls_v8081.py',{
        'B48':'B49','Rafael_B48_source_controls_v8024':'Rafael_B49_source_controls_v8081',
        'Rafael_next_clean_v8020':'Rafael_next_clean_v8073',
        'Rafael_B48_clean_gloss_v8022/91_fresh_clean_glosses_nine_source_identities_before_current_English.json':'Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json',
        'current_V8013_Rafael_native_v8016':'current_V8066_Rafael_native_v8069',
        'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json':'Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json',
        "len(block)==g['clean_logical_end']==5252 and g['clean_tail_bytes']==0 and len(commands)==163 and len(g['records'])==91":"len(block)==3976 and g['clean_logical_end']==3974 and g['clean_tail_bytes']==2 and block[3974:]==bytes(2) and len(commands)==154 and len(g['records'])==61",
        "for r in g['records'])==1":"for r in g['records'])==2",
        '[(48,49,48,[],[])]':'[(49,50,49,[39],[151])]',
        '{5252}':'{3974}','block=48':'block=49',
        'len(branches)==28':'len(branches)==56',"for r in branches)==140":"for r in branches)==280",
        'len(predicates)==7':'len(predicates)==14',"for p in predicates)==5":"for p in predicates)==13",'len(same)==5':'len(same)==8',
        'len(current_speeches)==91':'len(current_speeches)==61',
        "end['offset']==5248 and end['native_extent']==4 and block[5248:]==bytes(4)":"end['offset']==3970 and end['native_extent']==4 and block[3970:3974]==bytes(4)",
        'end_case\'](arm,block,5248':'end_case\'](arm,block,3970',
        'source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends':'source_EV0_56_relative_sites280_cases13_raw_predicates1_query25_seeded_ends',
        'all163_source_commands91_speeches':'all154_source_commands61_speeches',
        'source_Ev48_no_explicit_dependency_list_not_proof_ofouter_scheduler_city_conditions_orcurrent_eligibility':'source_EV49_requires39_excludes151_not_proof_ofouter_scheduler_city_conditions_orcurrent_eligibility',
        '28 relative sites/140 cases,5 raw predicates/2completion queries':'56 relative sites/280 cases,13 raw predicates/1completion query',
        'all163commands/91speeches':'all154commands/61speeches',
        '    save(ROOT/':"    C281=Path('work/analysis/Rafael_B49_C281_structural_v8080/exact_C281_source_original_structural_boundary.json');opaque=read(C281)\n    assert len(opaque['cases'])==1 and opaque['cases'][0]['source_offset']==72 and opaque['cases'][0]['source_word']==0xC281\n    save(ROOT/",
        'source_terminal=end,normal_seeded_ends=ends':'source_terminal=end,separate_two_zero_tail_bytes_preserved=True,normal_seeded_ends=ends,C281_structural_proof=str(C281),C281_structural_proof_sha256=sha(C281.read_bytes()),C281_actual_transition_andopaque_effect_semantics_not_claimed=True',
        '[SOURCE,GLOSS,INPUT,NAMES,ep,Path(__file__)]':'[SOURCE,GLOSS,INPUT,NAMES,ep,C281,Path(__file__)]',
    }))
