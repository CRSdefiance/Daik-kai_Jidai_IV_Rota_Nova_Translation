"""Extend the established source reader to all seven blocks, without inventing effect semantics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_source_control_tools_v8791');assert not root.exists()
    source=Path('scripts/prove_Hodram_B31_B53_source_controls_v8718.py').read_text('utf-8')
    a=source.index('        if number==31:');z=source.index('        groups.append(',a)
    counts="""        expected={54:(7,4,0,0,2),55:(3,1,0,0,1),56:(7,3,0,0,3),57:(11,8,0,0,2),58:(98,49,24,6,18),59:(14,7,0,0,6),60:(12,10,0,0,1)}
        assert (len(commands),len(speeches),len(branches),len(queries),len(opaque))==expected[number]
        assert len(ends)==25 and sum(len(r['cases']) for r in branches)==5*len(branches)
"""
    spans="""    # Derive the complete decoder ranges from the unchanged original bridge's
    # own comparisons, preserving every original native integer verbatim.
    import ast
    ranges=[]
    for node in ast.walk(ast.parse(inspect.getsource(walk))):
        if isinstance(node,ast.Compare) and isinstance(node.left,ast.Constant) and type(node.left.value)is int and len(node.comparators)==2 and isinstance(node.comparators[0],ast.Name) and node.comparators[0].id=='pc' and isinstance(node.comparators[1],ast.Constant):
            assert isinstance(node.ops[0],ast.LtE) and isinstance(node.ops[1],ast.Lt)
            ranges.append((node.left.value-BASE,node.comparators[1].value-BASE))
    assert len(set(ranges))==2
    for start,end in sorted(set(ranges)):
        assert arm[start:end]==ja[start:end]
        spans.append(dict(start=start,end=end,sha256=sha(arm[start:end])))
"""
    receipt=derive('scripts/prove_Hodram_B31_B53_source_controls_v8718.py','scripts/prove_Hodram_B54_B60_source_controls_v8791.py',{
        'scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext':'scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext,BASE',
        'Hodram_B31_B53_source_controls_v8718':'Hodram_B54_B60_source_controls_v8791',
        'work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json':'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json',
        'work/analysis/Hodram_B53_clean_v8711/complete_clean_SC1_B53_EV1_andcoverage_before_current_English.json':'work/analysis/Hodram_next_clean_v8785/complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json',
        'current_V8704_Hodram_native_v8707':'current_V8778_Hodram_native_v8781',
        "assert gloss['all_three_complete_clean_utterances_glossed_before_earlier_English'] and gloss['current_English_for_B31_andB53_still_unconsulted']":"assert gloss['all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English'] and all(r['current_English_dialogue_still_unconsulted'] for g in gloss['groups'] for r in g['records'])",
        'all-routes-unified-v8704':'all-routes-unified-v8778',
        "spans=prior['unchanged_source_runtime_spans']":"spans=[dict(s) for s in prior['unchanged_source_runtime_spans']]",
        "    ev=image.read_file('/data/EV1.DK4');":spans+"    ev=image.read_file('/data/EV1.DK4');",
        "assert [e['event_ID'] for e in events]==[31,52,53,74]":"assert [e['event_ID'] for e in events]==[15,54,55,56,57,58,59,60,65,76,128,129,142]",
        'not_current_eligibility_or_selected_Hodram_B31_B53_activation':'not_current_eligibility_or_selected_Hodram_B54_B60_activation',
        'entry-ownV8704':'entry-ownV8778',
        'assert number in [31,53] and len(block)==logical==source[\'clean_stored_bytes\'] and source[\'clean_tail_bytes\']==0':"assert number in [54,55,56,57,58,59,60] and len(block)==source['clean_stored_bytes']==logical+source['clean_tail_bytes'] and block[logical:]==bytes(source['clean_tail_bytes'])",
        'assert word!=0x2100 and word not in [0x4820,0x4800,0x4700]':'assert word!=0x2100',
        source[a:z]:counts,
        'separate_tail_bytes=0':'separate_tail_bytes=source[\'clean_tail_bytes\']',
        'len(groups)==2 and sum(len(g[\'complete_source_preambles\']) for g in groups)==3':'len(groups)==7 and sum(len(g[\'complete_source_preambles\']) for g in groups)==82',
        'complete_source_commands=18,complete_speech_preambles=3,relative_sites=4,native_relative_cases=20,raw_unforced_query_cases=1,opaque_structural_decode_pairs=8,normal_seeded_end_cases=50':'complete_source_commands=152,complete_speech_preambles=82,relative_sites=24,native_relative_cases=120,raw_unforced_query_cases=6,opaque_structural_decode_pairs=33,normal_seeded_end_cases=175',
        'explicit_event_chain=[52,31,53],event53_excludes74=True':'explicit_event_links_only_not_continuous_conversation=True,original_event_anddependency_getters=13',
        'normal_ends192_and132_preserve_carried_values_all6words_andguards':'all7_complete_normal_ends_preserve_existing_result_values_all6words_andguards',
        'opaque6000_6311_633F_623F_A000_effect_semantics_not_invented':'all33_nonprose_resource_scene_andgameplay_bridges_are_structural_not_invented_effect_semantics',
        'current_B31_B53_English_dialogue_bodies_still_unconsulted':'current_B54_B60_English_dialogue_bodies_still_unconsulted',
        "B31/B53 source:18commands/3preambles/20branchcases/1unforcedquery/8opaque pairs/50whole normalends inownV8704.":"B54-B60 source:152commands/82preambles/120branchcases/6unforcedqueries/33nonprose pairs/175whole normalends inownV8778.",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,
        all_original_native_queries_branch_arguments_resultwords_ABI_memory_canaries_source_events_andterminal_guards_preserved=True,
        complete_original_decoder_ranges_derived_from_unchanged_bridge_source_not_new_addresses=True,
        B59_item_display_commands_included_as_structural_pairs_not_claimed_item_identity_oractual_effect=True,
        all_seven_source_blocks_82utterances_no_current_English_orstate_forcing=True,
        no_ROM_emulator_capture_orcredit_by_preparer=True,full_goal_complete=False))
