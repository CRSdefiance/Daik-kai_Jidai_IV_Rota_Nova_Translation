"""Derive B52 native controls with both ends and exact reused caller evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_controls_tools_v8678')
    assert not root.exists()
    source = Path('dk4tool/patch/hodram_B51_controls_v1.py').read_text(encoding='utf-8')
    start = source.index("        terminal = g['all_target_commands'][-1]")
    stop = source.index("        span = flow['original_caller_span']", start)
    ends = """        terminals=[c for c in g['all_target_commands'] if c['word']==0]
        require(len(terminals)==2 and [c['whole_command_hex'] for c in terminals]==['00000000','00000080'] and terminals[-1]['offset']+4==g['target_logical_end'],'both distinct full ends before separate tail')
        endmap={c['old_offset']:c['new_offset'] for c in g['command_map'] if c['word']==0}
        require(endmap=={166:158,224:232},'exact source/current normal/flagged end maps')
        ends=[ee['end_case'](arm,block,endmap[c['source_offset']],c['previous_result'],c['initial_value_word']) for c in source['distinct_seeded_ends']]
        require(len(ends)==50 and ends==stored['distinct_seeded_ends'],'all fifty original distinct seeded ends andguard fields')
        require(sum(e['flagged_terminal'] for e in ends)==25 and all(e['native_result']==([1,0,0,0,0,0] if e['flagged_terminal'] else [0,e['initial_value_word'],0,0,0,0]) for e in ends),'normal carries value/flagged returns1clears value/all six words')
"""
    start2 = source.index('        forwarded = []')
    stop2 = source.index('    return dict(', start2)
    forwarding = """        require(menu_flow['caller_fragment_reused_from']==str(FLOW) and menu_flow['caller_fragment_reused_sha256']==sha(FLOW.read_bytes()) and menu_flow['reused_original_kind2_value_forwarding_kind3_carry_cases']==50,'exact source-qualified caller reuse')
        forwarded=flow['caller_fragment_cases']
        require(len(forwarded)==50 and {c['result'][0] for c in forwarded}=={2,3},'all fifty original caller cases')
        for case in forwarded:
            require(len(case['result'])==6 and case['all_six_return_words_preserved'] and case['full_unowned4MiB_actors_stream_runtime_stack_canaries_andSP_exact'],'reused caller complete six words andoriginal guards')
            require(case['next_parser_r3']==(case['result'][1] if case['result'][0]==2 else case['previous_structural_value']),'original kind2 value forwarding/kind3 carry')
        require(not ctx.machines,'no native context machine remains')
"""
    changes = {
        'B51 control': 'B52 control', 'Hodram-B51-controls-': 'Hodram-B52-controls-',
        'hodram_B51_profile_v1': 'hodram_B52_profile_v1', 'hodram_B51_native_guards_v1': 'hodram_B52_native_guards_v1',
        'Hodram_B50_registered_route_context_v8546': 'Hodram_B51_registered_route_context_v8612',
        'work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json': 'work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json',
        'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json': 'work/analysis/Hodram_B52_source_controls_v8620/source_controls.json',
        'work/analysis/Hodram_B51_relocation_v8565/reconstruction.json': 'work/analysis/Hodram_B52_relocation_v8642/reconstruction.json',
        "mapping, current, source, display, stored, flow = [data[k] for k in ['relocation', 'current', 'source_controls', 'source_display', 'stored', 'result_flow']]": "mapping,current,source,display,stored,flow,menu_flow=[data[k] for k in ['relocation','current','source_controls','source_display','stored','result_flow','source_menu_VM']]",
        "require(g['block'] == 51 and len(rows) == 5": "require(g['block'] == 52 and len(rows) == 3",
        'complete five-speech B51 target': 'complete three-speech B52 target',
        "len(g['all_target_commands']) == 20 and len(g['relative_fixups']) == len(g['relocated_skip_cases']) == 8": "len(g['all_target_commands']) == 14 and len(g['relative_fixups']) == len(g['relocated_skip_cases']) == 4",
        'all twenty commands/eight relative sites': 'all fourteen commands/four relative sites',
        "== 40, 'all forty native branch cases'": "== 20, 'all twenty native branch cases'",
        "[113, 1, 113, 18, 16], 'five original progressive actors'": "[113,113,113], 'three original progressive actors'",
        "elif after['word'] in [0x100, 0x200, 0x300, 0x400]:": "elif after['word']==0x2100:\n            require(after['whole_command_hex']==g['choice_commands'][0]['target_hex'],'complete independently compiled typed menu')\n        elif after['word'] in [0x100, 0x200, 0x300, 0x400]:",
        '    from scripts.prove_Hodram_B51_result_flow_v8558c import forward\n': '',
        "events = source['source_event_andexplicit_query_records']": "events = source['source_event_anddependency_records']",
        "[30, 51] and [(e['event_ID'], e['script_block'], e['must_be_completed'], e['must_not_be_completed']) for e in source['source_event_records']] == [(51, 51, [], [])]": "[30,52,74] and [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in source['source_event_records']]==[(52,52,[30],[74])]",
        'original selected event51 and separate explicit event30 query': 'original selected event52 andits30/74 dependencies without outer eligibility claim',
        "{1: 1, 16: 1, 18: 0, 113: 0}[raw[0]]": "{113:0}[raw[0]]",
        'all five complete original dispatch records': 'all three complete original dispatch records',
        "elif word not in [0, 0x4000, 0x100, 0x200, 0x300, 0x400]:": "elif word not in [0,0x2100,0x4000,0x100,0x200,0x300,0x400]:",
        "require(len(queries) == 2 and queries == stored['stored_queries']": "require(len(queries) == 0 and queries == stored['stored_queries']",
        source[start:stop]: ends,
        source[start2:stop2]: forwarding,
        'independent_final_dispatches=5, relative_sites=8, native_relative_cases=40, raw_query_cases=2': 'independent_final_dispatches=3, relative_sites=4, native_relative_cases=20, raw_query_cases=0',
        'original_EV1_entries=2, opaque_structural_decode_pairs=4, normal_seeded_ends=25, original_result_channel_cases=50': 'original_EV1_entries=3, opaque_structural_decode_pairs=4, distinct_seeded_ends=50, exact_reused_original_result_channel_cases=50',
        'all_twenty_commands_five_preambles_queries_branches_full_end_tail_andvalue_carries_bound': 'all14_commands_three_preambles_zeroqueries_typed_menu_branches_both_fullends_tail_andvalue_carries_bound',
    }
    receipt = derive('dk4tool/patch/hodram_B51_controls_v1.py', 'dk4tool/patch/hodram_B52_controls_v1.py', changes)
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=receipt,
         native_dispatch_entry_skip_end_andopaque_decode_guards_retained=True,
         original50_caller_cases_reused_only_through_exact_immutable_artifact_script_andwhole_native_span=True,
         no_completed_gameplay_orproducer_replay=True))
