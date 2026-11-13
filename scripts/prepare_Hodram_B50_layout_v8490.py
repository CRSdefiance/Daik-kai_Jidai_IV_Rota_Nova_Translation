"""Derive original guarded logical/automatic/full-native-page checks for three ordinary B50 paragraphs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_layout_tools_v8490')
DOC='translations/hodram_B50_editorial_manuscript_v1.json'
SOURCE='work/analysis/Hodram_B50_source_display_v8487/source_display.json'
INPUT='work/analysis/current_V8475_Hodram_native_v8478/current_native_input.json'
LOGICAL='work/analysis/Hodram_B50_logical_v8490/logical_paragraphs.json'
PLAN='work/analysis/Hodram_B50_layout_v8491/automatic_plans.json'
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/prove_Hodram_B47_B48_logical_v8320.py','scripts/prove_Hodram_B50_logical_v8490.py',{
        'scripts.Hodram_registered_route_context_v8303':'scripts.Hodram_B49_registered_route_context_v8478',
        'Hodram_B47_B48_logical_v8320':'Hodram_B50_logical_v8490','translations/hodram_B47_B48_editorial_manuscript_v1.json':DOC,
        'work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json':SOURCE,
        'work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json':INPUT,
        "doc['source_display_proof_sha256']==sha(SOURCE.read_bytes()) and len(doc['records'])==6":"read(doc['current_packet'])['source_display_proof_sha256']==sha(SOURCE.read_bytes()) and len(doc['records'])==3",
        'len(rows)==6':'len(rows)==3','six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json':'logical_paragraphs.json',
        'fresh_native_alignment_cases=24,progressive_alignment_cases=20':'fresh_native_alignment_cases=12,progressive_alignment_cases=8',
        'source_macro_counts=dict(FI=1,FA=0,FO=0)':'source_macro_counts=dict(FI=0,FA=0,FO=0)','all_six_formatting_gates_remain_false':'all_three_formatting_gates_remain_false',
        'Six logical English paragraphs:20progressive+4nullactorFE guarded alignments/one real FI;all literal bytes andfull4MiB/ABI/scratch guards pass.Formatting/actual/release pending.':'B50logical:8progressive+4nullactorFE guarded alignments/zero source macros;allliteral bytes/full4MiB/ABI/scratch guards pass.Formatting/actual/release pending.',
    }))
    results.append(derive('scripts/plan_Hodram_B47_B48_v8323.py','scripts/plan_Hodram_B50_v8491.py',{
        'Hodram_B47_B48_layout_v8323':'Hodram_B50_layout_v8491','translations/hodram_B47_B48_editorial_manuscript_v1.json':DOC,
        'work/analysis/Hodram_B47_B48_logical_v8320/six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json':LOGICAL,
        "logical['fresh_native_alignment_cases']==24 and len(doc['records'])==6":"logical['fresh_native_alignment_cases']==12 and len(doc['records'])==3",
        'Hodram B47/B48 plan:':'Hodram B50 plan:','Hodram-B47-B48-RESEARCH-ONLY:':'Hodram-B50-RESEARCH-ONLY:',
        'six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json':'automatic_plans.json',
        'all_words_punctuation_andone_source_FI_preserved_without_shortening':'all_words_punctuation_andzero_source_macros_preserved_without_shortening',
        'not failures and len(rows)==6':'not failures and len(rows)==3',
    }))
    results.append(derive('scripts/prove_Hodram_B47_B48_pages_v8324.py','scripts/prove_Hodram_B50_pages_v8492.py',{
        'scripts.Hodram_registered_route_context_v8303':'scripts.Hodram_B49_registered_route_context_v8478',
        'Hodram_B47_B48_pages_v8324':'Hodram_B50_pages_v8492','translations/hodram_B47_B48_editorial_manuscript_v1.json':DOC,
        'work/analysis/Hodram_B47_B48_layout_v8323/six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json':PLAN,
        'work/analysis/Hodram_B47_B48_logical_v8320/six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json':LOGICAL,
        'work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json':SOURCE,
        'work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json':INPUT,
        "len(plan['records'])==6":"len(plan['records'])==3",'len(rows)==6 and not ctx.machines and len(pictures)==6':'len(rows)==3 and not ctx.machines and len(pictures)==3',
        'six_complete_English_native_pages.png':'three_complete_English_native_pages.png','six_complete_native_pages24_compiled_alignments_distinct_FE.json':'compiled_native_pages.json',
        'fresh_compiled_alignment_cases=24,progressive_alignment_cases=20':'fresh_compiled_alignment_cases=12,progressive_alignment_cases=8',
        'complete_progressive_pages=5':'complete_progressive_pages=2','all_six_single_pages_no_blank_orunintended_extra_page':'all_three_single_pages_no_blank_orunintended_extra_page',
        'one_source_FI_preserved_no_shortening_orprose_manual_wrap':'all_zero_source_macros_preserved_no_shortening_orprose_manual_wrap','all_six_formatting_gates_still_false':'all_three_formatting_gates_still_false',
        'Six complete one-page English displays/24compiled alignments:fiveprogressive+oneoriginalFE;all glyphs/guards/bounds/consumption pass.Direct view,stored/native effects/actual/release pending.':'B50three complete one-page English displays/12compiled alignments:two progressive+oneoriginalFE;allglyphs/guards/bounds/consumption pass.Directview/stored/actual/release pending.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'derivations.json',dict(derivations=results,all_native_addresses_metrics_values_andmultiplicity_preserved=True,full216px_available_width_ordinary_automatic_wrap_andoriginal_QA_preserved=True,no_B49_ellipsis_orNewWorld_specific_exceptions_added=True,no_original_producer_profile_orapproved_wording_modified=True,own_current_V8475_context=True,no_ROM_native_run_orcredit_by_preparer=True,new_credit=0,full_goal_complete=False))
