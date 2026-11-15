"""Derive independent B49 production validation; preserve every original command and actual/native scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_atomic_tools_v8117')
if __name__=='__main__':
    assert not ROOT.exists()
    src=Path('dk4tool/patch/rafael_B48_editorial_v1.py').read_text('utf8')
    actual=read('work/analysis/Rafael_B49_actual_v8107/paired_source_English_observed_path_complete_pages_names_C281_andreturn.json')
    names=read('translations/rafael_B49_speaker_name_review_v3.json')
    old_unvisited=src[src.index('UNVISITED='):src.index('\n',src.index('UNVISITED='))]
    pagebranch=src[src.index('            if pages==2:'):src.index('            count+=',src.index('            if pages==2:'))]
    c281='''        c281=next(p for p in g['command_pairs'] if p['word']==0xC281)
        require(c281['canonical_source_offset']==72 and c281['start']==4016 and c281['returned']==4017 and c281['decoded_length']==2 and c281['native_result']==[3,0] and c281['before_RNG']==c281['after_RNG'],'actual original C281 effect/extent/result/timing')
        require(expected[c281['fixture_offset']]['whole_command_hex']=='81c2','actual exact C281 source bytes')
        focused=next(v for v in focus['groups'] if v['version']==version)
        require(focused['C281_command']==c281 and focused['original_C281_effect_body_executed_in_core_no_opaque_bridge'] and focused['first_exchange_complete_andnormal_return_verified'],'focused full C281 transition')
        require(focused['observed_nameplate_actors']==[0,2,5,9] and focused['native_only_nameplate_actors']==[4,6,8],'focused nameplate scope')
        for n in focused['actual_complete_Lil_Camille_nameplates']:
            scene=next(s for s in g['speech_observations'] if s['source_selector']==n['actor_ID'])
            require(n['actor_ID'] in [2,9] and n['name']==scene['actual_name'] and n['holds']==scene['complete_body_holds'],'focused complete Lil/Camille names')
        visited=[p['canonical_source_offset'] for p in g['command_pairs'] if p['exchange_command_ordinal'] is not None]
        matches=[p for p in flow['representative_text_paths'] if p['visited_source_offsets']==visited]
        require(matches and all(p['source_speech_IDs']==[s['id'] for s in g['speech_observations']] for p in matches),'actual complete conditional source text path')
'''
    changes={
        'Rafael_B48_release_paths_v8060':'Rafael_B49_release_paths_v8114',
        'seal_Rafael_B48_references_v8060':'seal_Rafael_B49_references_v8114',
        'B48':'B49','Rafael91':'Rafael61',old_unvisited:'UNVISITED='+repr(actual['native_only_unvisited_speech_IDs']),
        'thirteen native-only conditional speeches':'eleven native-only conditional speeches',
        "sum(g['complete_body_holds'] for g in actual['groups'])==486 and sum(g['complete_progressive_header_holds'] for g in actual['groups'])==462 and sum(g['complete_FE_absent_header_holds'] for g in actual['groups'])==24":"sum(g['complete_body_holds'] for g in actual['groups'])==318 and sum(g['complete_progressive_header_holds'] for g in actual['groups'])==318 and sum(g['complete_FE_absent_header_holds'] for g in actual['groups'])==0",
        "len(sourcefont['source_records'])==91":"len(sourcefont['source_records'])==61", "len(native['records'])==91":"len(native['records'])==61",
        "fixture['source_block']==48":"fixture['source_block']==49",
        "g['actual_unique_speeches']==len(g['speech_observations'])==78":"g['actual_unique_speeches']==len(g['speech_observations'])==50",
        'actual selected unique seventyeight speeches':'actual selected unique fifty speeches',
        "len(g['unreturned_following_dialogues'])==1 and g['later_fixture_reentry_frames']==([35462] if version=='clean_Japanese' else [35702])":"not g['unreturned_following_dialogues'] and not g['later_fixture_reentry_frames']",
        "(22735 if version=='clean_Japanese' else 22973)":"(16013 if version=='clean_Japanese' else 16016)",
        "len(g['command_pairs'])==146 and g['observed_original_exchange_commands']==136":"len(g['command_pairs'])==129 and g['observed_original_exchange_commands']==119",
        "report['frames']==40001":"report['frames']==24001",
        "len(expected)==173 and len(fixture['all_original_exchange_commands'])==163 and len(fixture['original_text_records'])==91":"len(expected)==164 and len(fixture['all_original_exchange_commands'])==154 and len(fixture['original_text_records'])==61",
        'all28_relative_spans_unchanged':'all56_relative_spans_unchanged',
        "pages=2 if version=='English' and row['id']=='DK4_MES_B48_R0347' else 1":"pages=1",
        "scene['kind']==('system-FE' if row['source_selector']==254 else 'progressive')":"scene['kind']=='progressive'",
        "(hold['original_FE_absent_nameplate_preserved'] if row['source_selector']==254 else hold['complete_name_mask_equal'])":"hold['complete_name_mask_equal']",
        "[228 if row['source_selector']==254 or version=='clean_Japanese' and row['id']=='DK4_MES_B48_R0129' else 216,64]":"[216,64]",
        pagebranch:"            require(not scene['ordinary_page_transitions'],'no invented single-page transitions')\n",
        "(78 if version=='clean_Japanese' else 79)":"50",
        'all91_five_gates':'all61_five_gates',
        "native['fresh_compiled_alignment_cases']==4 and native['reused_compiled_alignment_cases']==360 and native['total_bound_compiled_alignment_cases']==364 and native['complete_progressive_paragraphs']==87 and native['complete_progressive_pages']==88 and native['FE_null_actor_alignment_cases']==16 and native['complete_FE_logical_andphysical_pages']==4":"native['fresh_compiled_alignment_cases']==20 and native['reused_compiled_alignment_cases']==224 and native['total_bound_compiled_alignment_cases']==244 and native['complete_progressive_paragraphs']==61 and native['complete_progressive_pages']==61 and native['FE_null_actor_alignment_cases']==0",
        "stored['fresh_native_alignment_cases']==192 and stored['exact_reused_native_alignment_cases']==172 and len(stored['fresh_parity_tail_records'])==48":"stored['fresh_native_alignment_cases']==124 and stored['exact_reused_native_alignment_cases']==120 and len(stored['fresh_parity_tail_records'])==31",
        'all91_native_ink':'all61_native_ink','R347_both_complete_stored_pages_exact_to_viewed':'all61_complete_stored_single_pages_exact_to_viewed',
        "policy['positive_count']==len(policy['positives'])==91 and policy['negative_count']==len(policy['negatives'])==1454":"policy['positive_count']==len(policy['positives'])==61 and policy['negative_count']==len(policy['negatives'])==1014",
        "len(approval['directly_viewed_sheets'])==31":"len(approval['directly_viewed_sheets'])==22",
        'thirteen_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage':'eleven_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage',
        'exact_two_QA_waivers_with_all_original_diagnostics_preserved':'exact_three_QA_waivers22_infos_all_original_diagnostics_preserved',
        repr({0:'Rafael Castor',4:'Janus Pasar',5:'Claudio Manaus',6:'Julio Erneco',7:'Cristina Erneco',8:'Arcadius Eudoxios',13:'Cesare Tony',75:'Hans Letzel',113:'Port Worker'}):repr({r['actor_ID']:r['name'] for r in names['records']}),
        '[0,5,6,8,75,113]':'[0,2,5,9]','[4,7,13]':'[4,6,8]',
        'actual six names/three native-only headers':'actual four names/three native-only headers',
        "len(census['all_command_maps'])==163 and len(census['relative_operand_maps'])==28":"len(census['all_command_maps'])==154 and len(census['relative_operand_maps'])==56",
        "len(controls['final_dispatches'])==91":"len(controls['final_dispatches'])==61",
        "controls['relocated_relative_cases'])==140":"controls['relocated_relative_cases'])==280",
        "len(controls['relocated_predicates_andqueries'])==7":"len(controls['relocated_predicates_andqueries'])==14",
        'all44_nonrelative_controls_threeA000_andcomplete_end_bytes_exact':'all37_nonrelative_controls_sevenA000_C281_andcomplete_end_bytes_exact',
        'all_five_raw_predicates_andtwo_completion_queries_current_unforced_values_andunaligned_scratch_restore_preserved':'all13_raw_predicates_andone_completion_query_current_unforced_values_andunaligned_scratch_restore_preserved',
        '[22735,22973]':'[16013,16016]',
        "len(g['command_comparison_differences'])==129 and len(g['duration_differences'])==34":"len(g['command_comparison_differences'])==111 and len(g['duration_differences'])==18",
        "[int('1328542105'),int('448695880')]":"[int('3456469704'),int('204362374')]",
        "r['exit_English_phase']==63 and r['final_English_phase']==-393":"r['exit_English_phase']==3 and r['final_English_phase']==2",
        "dict(state=True,models=True,persistent_objects=False,tasks=True,calendar=True) and not g['whole_actors_equal']":"dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True) and g['whole_actors_equal']",
        'actual later component/calendar/actor differences':'actual later sampled component/calendar/actor equality with other limits',
        "len(g['later_RGB_differences'])==r['later_RGB_differences']==285 and len(g['later_full_RGB_comparisons'])==g['later_sample_count']==r['later_samples']==285":"len(g['later_RGB_differences'])==r['later_RGB_differences']==19 and len(g['later_full_RGB_comparisons'])==g['later_sample_count']==r['later_samples']==134",
        'all78_whole_upper_scene_portrait_andheader_RGB_equal':'all_observed_whole_upper_scene_portrait_andheader_RGB_equal',
        "r['first_observed_phase_difference']['canonical_source_offset']==832 and r['first_observed_phase_difference']['source_duration']==173 and r['first_observed_phase_difference']['English_duration']==177 and r['R347_two_page_measurement']['source_duration']==241 and r['R347_two_page_measurement']['English_duration']==481":"r['first_observed_phase_difference']['canonical_source_offset']==114 and r['first_observed_phase_difference']['source_duration']==237 and r['first_observed_phase_difference']['English_duration']==241 and r['C281_original_command_measurement']['word']==0xC281 and r['C281_original_command_measurement']['source_duration']==r['C281_original_command_measurement']['English_duration']==1 and r['C281_original_command_measurement']['after_English_phase']==0",
        'first measured phase andR347 extra-page phase':'first measured phase and original C281 timing',
        "sum(r['decision']=='revision' for r in rows)==42 and sum(r['decision']=='retention' for r in rows)==49":"sum(r['decision']=='revision' for r in rows)==31 and sum(r['decision']=='retention' for r in rows)==30",
        'fortytwo revisions/fortynine retentions':'thirtyone revisions/thirty retentions',
        "group['block']==48":"group['block']==49",'[48]':'[49]','block=48':'block=49',
        "len(stores)==len(stored['records'])==91":"len(stores)==len(stored['records'])==61",
        "(1 if ident=='DK4_MES_B48_R0370' else 0)":"int(ident in ['DK4_MES_B49_R0311','DK4_MES_B49_R0388'])",
        'exact original oneFI expansion/no added macro orprintf':'exact original twoFI sites/no added macro orprintf',
        "len(changes)==len({r['id'] for r in changes})==91":"len(changes)==len({r['id'] for r in changes})==61",
        'all ninetyone unique':'all sixtyone unique',
        'all91_preambles163_commands28_relatives_five_predicates_two_queries_andfull_end_preserved':'all61_preambles154_commands56_relatives_13predicates_onequery_sevenA000_C281_andfull_end_preserved',
        'R347_two_pages_four_FE_two_exact_warning_exceptions_andthirteen_native_only_speeches_preserved':'all61_single_pages_three_exact_warnings22_infos_eleven_native_only_speeches_preserved',
        'def check_actual(actual,sourcefont,native,names,rows):':'def check_actual(actual,sourcefont,native,names,rows,packet,flow,focus):',
        "check_actual(actual,data['source_font_proof'],native,names,rows)":"check_actual(actual,data['source_font_proof'],native,names,rows,packet,data['source_path_proof'],data['focused_C281_transition'])",
        '        count=0\n':c281+'        count=0\n',
        "            at=pair['fixture_offset'];command=expected[at];word=command['word']":"            at=pair['fixture_offset'];command=expected[at];word=command['word']\n            original=next(((i,o) for i,o in enumerate(fixture['all_original_exchange_commands']) if o['fixture_command_offset']==at),None)\n            require(pair['exchange_command_ordinal']==(None if original is None else original[0]) and pair['canonical_source_offset']==(None if original is None else packet['groups'][0]['all_source_commands'][original[0]]['offset']),'actual canonical command/source association')",
        "    expected_names={r['actor_ID']:r['name'] for r in names['records']}":"    expected_names={r['actor_ID']:r['name'] for r in names['records']}\n    require(flow['structural_compositions_evaluated']==int('156250') and len(flow['representative_text_paths'])==256 and flow['all154_commands61_speeches_in_structural_union'],'complete structural branch scope')",
    }
    result=derive('dk4tool/patch/rafael_B48_editorial_v1.py','dk4tool/patch/rafael_B49_editorial_v1.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared independent B49 production semantics, including source path/C281/name bindings. Atomic checks pending.')
