"""Source-lock original logical,automatic layout,font andevent adapters forB36."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
MANUSCRIPT='translations/maria_B36_editorial_manuscript_v1.json'
NAMES='work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json'
LOGICAL='work/analysis/maria_confrontation_logical_v7792/16_logical_paragraphs64_original_native_macro_literal_alignments.json'
PLAN='work/analysis/maria_confrontation_layout_v7793/16_automatic_full_width_plans_all_base_QA_preserved.json'
if __name__=='__main__':
    root=Path('work/analysis/maria_confrontation_native_tools_v7792');assert not root.exists();results=[]
    results.append(derive('scripts/prove_Maria_story_logical_v7732.py','scripts/prove_Maria_confrontation_logical_v7792.py',{
        'maria_story_logical_v7732':'maria_confrontation_logical_v7792',
        'translations/maria_B34_B108_B35_editorial_manuscript_v1.json':MANUSCRIPT,
        'work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json':NAMES,
        'len(rows)==67':'len(rows)==16','67_logical_paragraphs268_original_native_macro_literal_alignments.json':'16_logical_paragraphs64_original_native_macro_literal_alignments.json',
        'fresh_native_alignment_cases=268':'fresh_native_alignment_cases=64',
        'source_macro_totals=dict(FI=1,FA=4,FO=7)':'source_macro_totals=dict(FI=2,FA=0,FO=1)',
        '67 complete proposed logical paragraphs/268 native alignments':'16 complete proposed logical paragraphs/64 native alignments',
        '12 real macros':'3 real substitutions',
    }))
    results.append(derive('scripts/plan_Maria_story_layout_v7733.py','scripts/plan_Maria_confrontation_layout_v7793.py',{
        'maria_story_layout_v7733':'maria_confrontation_layout_v7793',
        'translations/maria_B34_B108_B35_editorial_manuscript_v1.json':MANUSCRIPT,
        'work/analysis/maria_story_logical_v7732/67_logical_paragraphs268_original_native_macro_literal_alignments.json':LOGICAL,
        'frozenset({1,3,9,10,26,74,116,155})':'frozenset({2,3,10})',
        "ENV={**old_plan.__globals__":"""ADAPTER=checked_text(ADAPTER,{'cost[0]+tiny,cost[1]+1,cost[2]+weak':'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak'})
ENV={**old_plan.__globals__""",
        "logical['fresh_native_alignment_cases']==268":"logical['fresh_native_alignment_cases']==64",
        '67_automatic_full_width_plans_all_base_QA_preserved.json':'16_automatic_full_width_plans_all_base_QA_preserved.json',
        'all67_formatting_gates_remain_false':'all16_formatting_gates_remain_false',
    }))
    results.append(derive('scripts/prove_Maria_story_pages_v7738.py','scripts/prove_Maria_confrontation_pages_v7794.py',{
        'maria_story_pages_v7738':'maria_confrontation_pages_v7794',
        'work/analysis/maria_story_refined_v7735/67_refined_decisions_native_logical_bindings_automatic_plans_QA.json':PLAN,
        'translations/maria_B34_B108_B35_editorial_manuscript_v2.json':MANUSCRIPT,
        'work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json':NAMES,
        "and not plan['unresolved']":"and not plan['failures'] and not any(i['severity'] in ['warning','error'] for p in plan['records'] for i in p['base_QA']['issues'])",
        "len(rows)==67 and not ctx.machines and sum(len(r['pages']) for r in rows)==68":"len(rows)==16 and not ctx.machines and sum(len(r['pages']) for r in rows)==sum(p['expected_native_pages'] for p in plan['records'])",
        '67_compiled268_alignments68_complete_native_pages.json':'16_compiled64_alignments_complete_native_pages.json',
        'fresh_compiled_alignment_cases=268,fresh_complete_native_page_renders=68':"fresh_compiled_alignment_cases=64,fresh_complete_native_page_renders=sum(len(r['pages']) for r in rows)",
        'all67_formatting_gates_false':'all16_formatting_gates_false',
        'PASS:67compiled paragraphs/268fresh alignments/68fresh native complete pages.':'PASS:16compiled paragraphs/64fresh alignments/all planned native complete pages.',
    }))
    results.append(derive('scripts/prove_Maria_story_entries_predicates_v7731.py','scripts/prove_Maria_confrontation_entry_v7795.py',{
        'maria_story_entries_predicates_v7731':'maria_confrontation_entry_v7795',
        'work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json':
        'work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json',
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':
        'work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json',
        'work/analysis/current_V7717_native_v7720/route3/current_native_input.json':
        'work/analysis/current_V7779_native_v7782/route3/current_native_input.json',
        "r['event_ID'] in [34,108,35]":"r['event_ID'] in [36]",
        '{34:(35,34,()),108:(109,108,(34,)),35:(36,35,(108,))}':'{36:(37,36,(35,))}',
        'len(cases)==10':'len(cases)==0',
        'three_original_EV3_getters_ten_source_current_predicates.json':'one_original_EV3_getter_no_inblock_predicates.json',
        'source_completion_dependency_chain=[34,108,35]':'source_completion_dependency_chain=[35,36]',
        'Three exact EV3 getters;ten original source/current predicates with all guards pass.':'One exact EV3 getter;no in-block predicate commands. Outer eligibility remains separate.',
    }))
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=results,
        all_original_native_numeric_constants_canaries_ownership_glyph_bounds_andconsumption_guards_preserved=True,
        same_scoped_weak_boundary_cost_asfinal_Maria67_no_global_width_QA_change=True,
        actual_source_actors02_03_0A_andFI5_FA2_FO7_only=True,new_credit=0,no_ROM_registry_orname_asset_change=True,full_goal_complete=False))
