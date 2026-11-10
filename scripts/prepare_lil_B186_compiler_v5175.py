"""Freeze the conditional B186 compiler with exact metadata,prose and measured scope."""
from pathlib import Path
from collections import Counter
import re
from scripts.seal_lil_B186_references_v5172 import FLAGS
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_compiler_tools_v5175')
SOURCE=Path('dk4tool/patch/lil_B182_editorial_v1.py')
OUTPUT=Path('dk4tool/patch/lil_B186_editorial_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index('FLAGS=');b=text.index('\ndef load',a)
    oldflags=text[a:b]
    nameblock="""    require(names['approved_prose_names']=={'166':'Lady','167':'Lady'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
            (c,i):'Lady' for i in [166,167] for c in ['progressive-nameplate','full-catalogue']},'four original role consumers required')
"""
    roleblock="""    require(names['progressive_nameplate_values']==names['full_catalogue_values']=={'174':'Owner','175':'Cook'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
            (c,i):name for i,name in [(174,'Owner'),(175,'Cook')] for c in ['progressive-nameplate','full-catalogue']}
        and all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in names['native_four_consumer_cases']['rows']),'four original role consumers required')
    voice=load(doc['actor_voice_contract'])
    require({r['actor_ID']:r['original_voice_class'] for r in voice['fresh2_actor_names']['rows']}=={174:0,175:0},'original Owner/Cook voice classes required')
    terms=load(doc['actor_terminology_reconciliation'])
    require(terms['approved_prose_names']=={'174':'Owner','175':'Cook'} and terms['city']=='Alexandria'
        and [r['text'] for r in terms['two_source_current_city_aliases']]==['アレキサンドリア','Alexandria']
        and terms['one_current_alias_still_Japanese_and_caller_unreviewed'],'actual role/city identities and unresolved alias required')
    require(terms['Sweets_is_broad_source_supported_collective_not_a_single_commodity_ID_or_new_UI_category']
        and terms['source_notice_says_sweet_things_not_UI_category4'] and terms['missing_sweetness_is_food_flavor_preparation_not_trade_advice']
        and terms['Owners_self_authority_and_confident_future_prediction_are_character_claims']
        and terms['Cooks_doubt_then_practical_question_and_two_perfunctory_replies_remain_distinct']
        and not terms['no_predecessor_English_exposed'] and terms['exposure_disclosure'],'source context and exposure limits required')
    wrap=load(doc['source_bound_wrap_refinement_proof'])
    require(sha(Path(doc['source_bound_wrap_refinement_proof']).read_bytes())==doc['source_bound_wrap_refinement_proof_sha256']
        and wrap['only_changed_record_IDs']==['DK4_MES_B186_R0013'] and wrap['all12_words_controls_and_prose_unchanged']
        and wrap['eleven_other_compiled_targets_exact'] and wrap['eleven_other_native_planes_exact']
        and len(wrap['exact_source_and_prose_mutation_controls'])==6
        and all(r.get('rejected') or r.get('exact_reviewed_boundaries_not_inherited') for r in wrap['exact_source_and_prose_mutation_controls']),'exact R13 ordinary-boundary proof required')
    paragraph=next(c for c in native['cases'] if c['id']=='DK4_MES_B186_R0013')
    require([s.strip() for s in bytes.fromhex(paragraph['encoded_hex'])[1:].decode('ascii').splitlines()]==[
        "Yes! The customers won't be",'satisfied with a flavor this','light. It has to be sweeet! Sweet!'],'reviewed complete R13 paragraph required')
"""
    metadata="""    require(spec['source_bytes']==len(block)==652 and spec['source_logical_end']==650
        and spec['research_bytes']==584 and spec['research_logical_end']==582,'source/target extent metadata differs')
    require([{k:r[k] for k in ['word','old_offset','new_offset']}|{'old_extent':r['old_native_extent'],'new_extent':r['new_native_extent']} for r in spec['mapped_native_commands']]==spec['command_map'],'both complete command maps must agree')
"""
    rowmeta="""        require(row['source_reference']['header_offset']==sa-5 and row['current_reference']['header_offset']==at-5
            and row['source_reference']['bytes']==len(raw) and row['current_reference']['bytes']==len(old),'complete source/current reference metadata differs:'+ident)
        require(row['source_reference']['block']==186 and row['source_reference']['record_index']==row['source_record_index']==original[:sa].count(b'\\0')
            and row['current_record_index']==block[:at].count(b'\\0'),'complete source/current record identity differs:'+ident)
"""
    boundary="""        if row['source_record_index']==13:
            require(len(qa.get('reviewed_ordinary_boundaries',[]))==2 and row.get('reviewed_ordinary_boundaries')==qa['reviewed_ordinary_boundaries'],'exact source/prose ordinary-boundary reasons required')
        else:require(not row.get('reviewed_ordinary_boundaries'),'unreviewed boundary reason on other record')
"""
    changes={
        oldflags:'FLAGS='+repr(FLAGS)+'\n',
        'B182':'B186','lil_B182_layout_v1':'lil_B186_layout_v4',
        'SELECTORS={166,167,254}':'SELECTORS={174,175,254}',
        "len(native['cases'])==8 and native['current_original_macro_alignment_calls']==64":"len(native['cases'])==12 and native['current_original_macro_alignment_calls']==96",
        "native['complete_progressive_planes']==7":"native['complete_progressive_planes']==11",
        "len(stored['final_target_parity_cases'])==8 and stored['current_final_stored_macro_alignment_cases']==32":"len(stored['final_target_parity_cases'])==12 and stored['current_final_stored_macro_alignment_cases']==48",
        "stored['new_parity_macro_alignment_cases']==16 and stored['exact_byte_identical_reused_macro_alignment_cases']==16":
        "stored['new_parity_macro_alignment_cases']==36 and stored['exact_byte_identical_reused_macro_alignment_cases']==12",
        'all8_final_targets':'all12_final_targets',
        "len(controls['relocated_dispatch_cases'])==8 and len(controls['all7_exact_nonrelative_leaves'])==7":"len(controls['relocated_dispatch_cases'])==12 and len(controls['all6_exact_nonrelative_leaves'])==6",
        "len(controls['predicate_pairs'])==2":"len(controls['predicate_pairs'])==1",
        "len(controls['all25_source_and_relocated_structural_paths_identical'])==25":"len(controls['all5_source_and_relocated_structural_paths_identical'])==5",
        '==[(512,530),(544,562)]':'==[(540,478)]','value=500':'value=700',
        "len(ownership['cases'])==24 and ownership['unforced_cases']==6 and ownership['CPU_only_boundary_fixture_cases']==18":
        "len(ownership['cases'])==12 and ownership['unforced_cases']==3 and ownership['CPU_only_boundary_fixture_cases']==9",
        "{'clean':8,'current':8,'relocated':8}":"{'clean':4,'current':4,'relocated':4}",
        "for r in ownership['cases'])==8":"for r in ownership['cases'])==4",
        "[('clean',[512,544]),('current',[512,544]),('relocated',[530,562])]":"[('clean',[540]),('current',[540]),('relocated',[478])]",
        'roll<500':'roll<700','roll==500':'roll==700',"r['threshold']==500":"r['threshold']==700",'{499,500,501}':'{699,700,701}',
        "[('current',632),('research',648)]":"[('current',646),('research',578)]",
        nameblock:roleblock,
        'all8_panels_seven_progressive_one_FE':'all12_panels_eleven_progressive_one_FE',
        'source_all25_commands_ten_branches_two_predicates':'source_all24_commands_six_branches_one_predicate',
        'original_scene_RNG_outcome_equal_final_RNG_and_timing_indicator_differences_disclosed':
        'original_scene_predicate_results_equal_draws_seeds_timing_and_indicator_differences_disclosed',
        'all8_complete_held_planes':'all12_complete_held_planes','all8_speeches7_progressive1':'all12_speeches11_progressive1',
        'dict(total=13,speech=7,control_or_end=6)':'dict(total=10,speech=4,control_or_end=6)',
        "len(observed['actual_timing_differences'])==13":"len(observed['actual_timing_differences'])==10",
        '[3723009301,403514907]':'[1803218166,2467799992]',
        "observed['no_PRNG_causal_trace_or_future_world_equivalence_claim']":"observed['future_world_equivalence_and_full_RAM_equality_not_claimed']",
        """require(len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==18
        and all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in observed['sampled_postscene_whole_RGB_differences_unmasked'])
        and observed['measured_timing_RGB_and_final_RNG_differences_retained_without_equivalence_claim']""":
        """require(len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==4
        and [(r['frame'],r['whole_frame_difference_bbox']) for r in observed['sampled_postscene_whole_RGB_differences_unmasked']]==[
            (6490,[225,371,239,376]),(6670,[225,371,239,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]
        and observed['different_measured_draws_and_final_RNG_seeds_retained_without_causal_or_future_equivalence_claim']
        and observed['ten_timing_and_four_original_indicator_differences_retained_without_masking_or_retiming']""",
        "len(observed['paired_full_screen_views'])==12":"len(observed['paired_full_screen_views'])==5",
        "s['viewed']":"s['viewed_after_image_return']","sheet['viewed']":"sheet['viewed_after_image_return']",
        "actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==8":"actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==12",
        '==[23,23]':'==[27,27]','==[4776,4775]':'==[5735,5737]',
        'dict(clean_Japanese=[532],reviewed_English=[532])':'dict(clean_Japanese=[560],reviewed_English=[560])',
        "len(version['selected_intervals'])==8":"len(version['selected_intervals'])==12",'single_source_end632':'single_source_end646',
        "original_source_offset']==632":"original_source_offset']==646",
        "original_source_offset']==532":"original_source_offset']==560",
        "original_source_offset']==630":"original_source_offset']==644",
        "(r['source_offset'],r['roll'],r['result'])==(512,52,0)":"(r['source_offset'],r['roll'],r['result'])=={'clean_Japanese':(540,297,0),'reviewed_English':(540,592,0)}[version['case']]",
        'len(rows)==len(set(ids))==8':'len(rows)==len(set(ids))==12','eight exact records':'twelve exact records',
        "{'progressive':7,'system-FE':1}":"{'progressive':11,'system-FE':1}","{'revise':6,'retain-wording':2}":"{'revise':7,'retain-wording':5}",
        "mapping['blocks'][0]['block']==182":"mapping['blocks'][0]['block']==186",'old_blocks[182]':'old_blocks[186]','.blocks[182]':'.blocks[186]',
        "    fonts={c['id']:c for c in native['cases']}":metadata+"    fonts={c['id']:c for c in native['cases']}",
        "        require(row['block']==182":rowmeta+"        require(row['block']==186",
        "        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''":boundary+"        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''",
        'block=182':'block=186',
        'end == len(block) == 636 and not any(block[end:])':'end == 650 and len(block)==652 and block[end:]==bytes(2)',
        "len(edges)==10 and [e['offset'] for e in edges]==[520, 524, 528, 540, 552, 556, 560, 572, 584, 588]":
        "len(edges)==6 and [e['offset'] for e in edges]==[548,552,556,568,580,592]",
        "len(spec['target_native_skip_cases'])==50 and len(logical)==mapped(end)==652":"len(spec['target_native_skip_cases'])==30 and len(logical)==mapped(end)==582",
        "    require(sha(target) == spec['target_block_sha256'], 'target block differs')":
        "    require(len(target)==584 and target[582:]==bytes(2) and sha(target) == spec['target_block_sha256'], 'target block differs')",
        "len(commands) == 25 and sum(command['word'] == 0x4000 for command in commands) == 8":
        "len(commands) == 24 and sum(command['word'] == 0x4000 for command in commands) == 12",
        "[c['old_offset'] for c in stops]==[632] and len(stops)==1 and stops[0]['new_offset']==648":
        "[c['old_offset'] for c in stops]==[646] and len(stops)==1 and stops[0]['new_offset']==578",
        'target[648:652]':'target[578:582]',
        """exact=[(512,'0080fffff4010000'),(532,'00a0ffff014700a1'),(544,'0080fffff4010000'),
        (564,'00a0ffff014800a1'),(576,'00a0ffff014600a1'),(630,'00c2'),(632,'00000000')]""":
        """exact=[(540,'0080ffffbc020000'),(560,'00a0ffff010b19a1'),(572,'00a0ffff011219a1'),
        (584,'00a0ffff010c19a1'),(644,'00c2'),(646,'00000000')]""",
        'seven complete source leaves':'six complete source leaves',
        '[0x8000,0xA000,0x8000,0xA000,0xA000,0xC200,0]':'[0x8000,0xA000,0xA000,0xA000,0xC200,0]',
        "require(bytes(restored) == block[:end], 'inverse does not restore every predecessor byte')":
        "require(bytes(restored) == block[:end] and bytes(restored)+block[end:]==block, 'inverse does not restore every predecessor byte')",
        'new_blocks[182]':'new_blocks[186]','== [182]':'== [186]',
        'relative_operands=10, source_commands=25':'relative_operands=6, source_commands=24',
        'all8_progressive_FE_speeches_two_predicates_three_A000_C200_ten_relative_sites_and7_leaves_preserved':
        'all12_progressive_FE_speeches_one700_predicate_three_A000_C200_six_relative_sites_and6_leaves_preserved',
    }
    row=derive(SOURCE,OUTPUT,changes)
    oldnums,newnums=native_numbers(text),native_numbers(OUTPUT.read_text(encoding='utf-8'))
    assert oldnums-newnums==Counter({3723009301:1,403514907:1})
    assert newnums-oldnums==Counter({1803218166:1,2467799992:1})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_conditional_compiler.json',dict(derivation=row,
        all_existing_native_high_integer_constants_and_multiplicities_preserved_except_two_measured_PRNG_data_values=True,
        source_current_reference_lengths_headers_record_identities_and_both_command_maps_guarded=True,
        exact_R13_source_prose_and_two_ordinary_boundary_reasons_required=True,source652_650_target584_582_and_two_tailzeros_guarded=True,
        one700_predicate_and_original_optional_operand_scratch_RNG_ownership_guarded=True,
        every_check_precedes_single_replace_file=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared atomic B186 compiler:12 rows,24 commands,six branches,exact700 ownership,complete metadata and measured actual scope.')
