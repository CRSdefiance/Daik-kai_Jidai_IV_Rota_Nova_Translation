"""Derive B50 independent production semantics without carrying B49 branch/C281 assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_atomic_tools_v8167')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/rafael_B49_editorial_v1.py').read_text('utf8')
    unvisited=source[source.index('UNVISITED='):source.index('\n',source.index('UNVISITED='))]
    c281=source[source.index('        c281=next('):source.index('        count=0',source.index('        c281=next('))]
    flow="    require(flow['structural_compositions_evaluated']==int('156250') and len(flow['representative_text_paths'])==256 and flow['all154_commands61_speeches_in_structural_union'],'complete structural branch scope')"
    newflow="    require(len(flow['groups'])==1 and flow['groups'][0]['block']==50 and flow['groups'][0]['commands']==packet['groups'][0]['all_source_commands'] and len(flow['groups'][0]['records'])==28,'complete linear source scope')"
    actualcontrols='''        focused=next(v for v in focus['groups'] if v['version']==version)
        actualcontrols=[p for p in g['command_pairs'] if p['canonical_source_offset'] is not None and p['word'] in [0x4821,0xA000,0x4720,0x4681]]
        require(focused['controls']==actualcontrols,'focused original picture/effect/departure associations')
        require([(c['word'],c['canonical_source_offset'],c['decoded_length']) for c in actualcontrols]==[(0x4821,244,4),(0xA000,340,8),(0x4720,348,2),(0x4681,1510,4)],'actual original picture/effect/departure extents')
        require([c['returned']-c['start'] for c in actualcontrols]==[60,240,0,88] and all(c['native_result']==[3,0] for c in actualcontrols),'actual original effect results/durations')
        require([expected[c['fixture_offset']]['whole_command_hex'] for c in actualcontrols]==['2148b5a8','00a0ffff0100b530','2047','81460002'],'actual complete original effect bytes')
        require(focused['original_andrepeat_all_observer_rows_exact_except_output_paths'] and focused['all_eight_capture_PNGs_framebuffers_andfinal_whole_RAM_exact_to_first_run'],'same-input focused repeat integrity')
        visited=[p['canonical_source_offset'] for p in g['command_pairs'] if p['exchange_command_ordinal'] is not None]
        require(visited==[c['offset'] for c in packet['groups'][0]['all_source_commands']] and [s['id'] for s in g['speech_observations']]==[r['id'] for r in rows],'actual all37 linear source commands/all28 speeches in order')
'''
    oldphase=next(line for line in source.splitlines() if "'first measured phase and original C281 timing'" in line)
    newphase="    require(r['first_observed_phase_difference']['word']==0x4000 and r['first_observed_phase_difference']['canonical_source_offset']==350 and r['first_observed_phase_difference']['source_duration']==237 and r['first_observed_phase_difference']['English_duration']==241,'first measured phase and original single-page wait timing')\n    require([(m['word'],m['canonical_source_offset'],m['source_duration'],m['English_duration']) for m in r['original_4821_A000_4720_4681_measurements'] if m['canonical_source_offset'] is not None]==[(0x4821,244,60,60),(0xA000,340,240,240),(0x4720,348,0,0),(0x4681,1510,88,88)],'original effect wait measurements')\n    check_bounded_risk(data['focused_picture_transition_andrisk'],actual,later)"
    macro=next(line for line in source.splitlines() if "'exact original twoFI sites/no added macro orprintf:'" in line)
    newmacro="        require(expanded.hex()==store['expanded_stored_hex'] and b'%' not in value[1:] and b'FO' not in value[1:] and value[1:].count(b'FI')==int(ident=='DK4_MES_B50_R0108') and value[1:].count(b'FA')==int(ident in ['DK4_MES_B50_R0040','DK4_MES_B50_R0061']),'exact original FA2/FI1 sites/no added macro orprintf:'+ident)"
    result=derive('dk4tool/patch/rafael_B49_editorial_v1.py','dk4tool/patch/rafael_B50_editorial_v1.py',{
        'from scripts.Rafael_B49_release_paths_v8114':'from scripts.Rafael_B50_release_paths_v8164',
        'from scripts.seal_Rafael_B49_references_v8114':'from scripts.seal_Rafael_B50_references_v8164',
        'CONFIG=\'translations/rafael_B49_editorial_release_v1.json\'':"from dk4tool.patch.rafael_B50_risk_v1 import check_bounded_risk\nCONFIG='translations/rafael_B50_editorial_release_v1.json'",
        unvisited:'UNVISITED=[]',c281:actualcontrols,flow:newflow,oldphase:newphase,macro:newmacro,
        'B49':'B50','Rafael61':'Rafael28','eleven native-only conditional speeches':'no unvisited B50 speeches',
        "sum(g['complete_body_holds'] for g in actual['groups'])==318":"sum(g['complete_body_holds'] for g in actual['groups'])==184",
        "sum(g['complete_progressive_header_holds'] for g in actual['groups'])==318":"sum(g['complete_progressive_header_holds'] for g in actual['groups'])==184",
        "len(sourcefont['source_records'])==61":"len(sourcefont['source_records'])==28","len(native['records'])==61":"len(native['records'])==28",
        "fixture['source_block']==49":"fixture['source_block']==50",
        "g['actual_unique_speeches']==len(g['speech_observations'])==50":"g['actual_unique_speeches']==len(g['speech_observations'])==28",
        'actual selected unique fifty speeches':'actual selected all twentyeight speeches',
        "(16013 if version=='clean_Japanese' else 16016)":"(10822 if version=='clean_Japanese' else 10824)",
        "len(g['command_pairs'])==129 and g['observed_original_exchange_commands']==119":"len(g['command_pairs'])==47 and g['observed_original_exchange_commands']==37",
        "report['frames']==24001":"report['frames']==16001",
        "len(expected)==164 and len(fixture['all_original_exchange_commands'])==154 and len(fixture['original_text_records'])==61":"len(expected)==47 and len(fixture['all_original_exchange_commands'])==37 and len(fixture['original_text_records'])==28",
        'all56_relative_spans_unchanged_under_constant32_byte_shift':'zero_relative_sites_no_span_relocation_under_constant32_byte_shift',
        "g['actual_complete_native_pages']==50":"g['actual_complete_native_pages']==28",
        'all61_five_gates':'all28_five_gates',
        "native['reused_compiled_alignment_cases']==224 and native['total_bound_compiled_alignment_cases']==244 and native['complete_progressive_paragraphs']==61 and native['complete_progressive_pages']==61":"native['reused_compiled_alignment_cases']==92 and native['total_bound_compiled_alignment_cases']==112 and native['complete_progressive_paragraphs']==28 and native['complete_progressive_pages']==28",
        "stored['fresh_native_alignment_cases']==124 and stored['exact_reused_native_alignment_cases']==120 and len(stored['fresh_parity_tail_records'])==31":"stored['fresh_native_alignment_cases']==60 and stored['exact_reused_native_alignment_cases']==52 and len(stored['fresh_parity_tail_records'])==15",
        'all61_native_ink':'all28_native_ink','all61_complete_stored_single_pages':'all28_complete_stored_single_pages',
        "policy['positive_count']==len(policy['positives'])==61 and policy['negative_count']==len(policy['negatives'])==1014":"policy['positive_count']==len(policy['positives'])==28 and policy['negative_count']==len(policy['negatives'])==511",
        "len(approval['directly_viewed_sheets'])==22":"len(approval['directly_viewed_sheets'])==14",
        "approval['eleven_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage']":"approval['observed_all37_original_commands_eachlanguage_and10_initializers']",
        'exact_three_QA_waivers22_infos_all_original_diagnostics_preserved':'exact_two_QA_waivers18_infos_all_original_diagnostics_preserved',
        "{0: 'Rafael Castor', 2: 'Lil Argot', 4: 'Janus Pasar', 5: 'Claudio Manaus', 6: 'Julio Erneco', 8: 'Arcadius Eudoxios', 9: 'Camille Overijssel'}":"{0:'Rafael Castor',2:'Lil Argot',9:'Camille Overijssel'}",
        '[0,2,5,9]':'[0,2,9]','[4,6,8]':'[]','actual four names/three native-only headers':'actual three names/no native-only headers',
        "len(census['all_command_maps'])==154 and len(census['relative_operand_maps'])==56":"len(census['all_command_maps'])==37 and not census['relative_operand_maps']",
        "len(controls['final_dispatches'])==61 and sum(len(r['cases']) for r in controls['relocated_relative_cases'])==280 and len(controls['relocated_predicates_andqueries'])==14":"len(controls['final_dispatches'])==28 and not controls['relocated_relative_cases'] and not controls['relocated_predicates_andqueries']",
        "controls['all37_nonrelative_controls_sevenA000_C281_andcomplete_end_bytes_exact'] and controls['all13_raw_predicates_andone_completion_query_current_unforced_values_andunaligned_scratch_restore_preserved']":"controls['all_nine_nonrelative_controls_oneA000_4821_4720_4681_andcomplete_end_bytes_exact'] and controls['zero_relative_predicate_query_sites_not_fabricated_execution_coverage'] and controls['source_relocated4821_descriptor_layout_calls_andall_4MiB_ABI_guards_equal']",
        "g['source_English_exits']==[16013,16016] and len(g['command_comparison_differences'])==111 and len(g['duration_differences'])==18":"g['source_English_exits']==[10822,10824] and len(g['command_comparison_differences'])==35 and len(g['duration_differences'])==11",
        "[int('3456469704'),int('204362374')]":"[int('3888306843'),int('2225786845')]",
        "r['exit_English_phase']==3 and r['final_English_phase']==2":"r['exit_English_phase']==2 and r['final_English_phase']==-10",
        "dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True) and g['whole_actors_equal']":"dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True) and not g['whole_actors_equal']",
        'actual later sampled component/calendar/actor equality with other limits':'actual later sampled component/calendar/actor differences with bounded limits',
        "r['later_RGB_differences']==19":"r['later_RGB_differences']==17","r['later_samples']==134":"r['later_samples']==87",
        "sum(r['decision']=='revision' for r in rows)==31 and sum(r['decision']=='retention' for r in rows)==30":"sum(r['decision']=='revision' for r in rows)==13 and sum(r['decision']=='retention' for r in rows)==15",
        'thirtyone revisions/thirty retentions':'thirteen revisions/fifteen retentions',
        "data['focused_C281_transition']":"data['focused_picture_transition_andrisk']",
        "group['block']==49":"group['block']==50",'len(stored[\'records\'])==61':"len(stored['records'])==28",'blocks[49]':'blocks[50]',
        "expanded=value[1:].replace(b'FI',b'Rafael')":"expanded=value[1:].replace(b'FI',b'Rafael').replace(b'FA',b'Castor')",
        'block=49':'block=50','targetblocks[49]':'targetblocks[50]','cleanblocks[49]':'cleanblocks[50]','restored[49]':'restored[50]','==[49]':'==[50]',
        "len({r['id'] for r in changes})==61":"len({r['id'] for r in changes})==28",'all sixtyone unique manifest changes':'all twentyeight unique manifest changes',
        'all61_preambles154_commands56_relatives_13predicates_onequery_sevenA000_C281_andfull_end_preserved':'all28_preambles37_commands_zero_relative_predicate_query_sites_FA2_FI1_nine_nontext_controls_andfull_end_preserved',
        'all61_single_pages_three_exact_warnings22_infos_eleven_native_only_speeches_preserved':'all28_single_pages_two_exact_warnings18_infos_all28_actual_speeches_preserved',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B50 independent atomic producer;bounded-risk helper/config/positive/challenges still required.')
