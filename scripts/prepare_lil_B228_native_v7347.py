"""Prepare thirteen complete native pages andall unchanged base-QA diagnostics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_native_tools_v7347')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B226':'B228','layout_v7251b/twenty_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7346b/thirteen_whole_paragraph_plans_no_macros_no_prose_changes','[2,23]':'[2,22]'}
    native={**common,'current_V7230_native_v7235':'current_V7324_native_v7329','native_pages_v7252':'native_pages_v7347','source_pages_v7247/all20_clean_objects':'source_pages_v7342/all13_clean_objects',"len(plan['records'])==20":"len(plan['records'])==13",'len(cases)==20 and len(pictures)==20 and alignments==160':'len(cases)==13 and len(pictures)==13 and alignments==104','all20_complete_pages_sheet':'all13_complete_pages_sheet','all20_paragraphs20_complete_native_pages160_alignments':'all13_paragraphs13_complete_native_pages104_alignments','complete_native_pages=20,logical_compiled_input_alignment_cases=160':'complete_native_pages=13,logical_compiled_input_alignment_cases=104','all20_single_original_four_row_pages':'all13_single_original_four_row_pages','all20_complete_prose_paragraphs':'all13_complete_prose_paragraphs','only_original_static_selectors2_23':'only_original_static_selectors2_22','all20_formatting_gates_remain_false':'all13_formatting_gates_remain_false','20 paragraphs/20 complete native pages/160 alignments':'13 paragraphs/13 complete native pages/104 alignments'}
    qa={**common,'base_QA_v7253':'base_QA_v7348','native_pages_v7252/all20_paragraphs20_complete_native_pages160_alignments':'native_pages_v7347/all13_paragraphs13_complete_native_pages104_alignments','all20_base_QA_diagnostics':'all13_base_QA_diagnostics','twenty':'thirteen'}
    jobs=[('scripts/verify_lil_B226_native_pages_v7252.py','scripts/verify_lil_B228_native_pages_v7347.py',native),('scripts/probe_lil_B226_base_QA_v7253.py','scripts/probe_lil_B228_base_QA_v7348.py',qa)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_native_andbase_QA.json',dict(tools=rows,all13_English_paragraphs_unchanged=True,original216x64_four_rows_native_font_guard_pairphase_bounds_canaries_andbare_I_rules_preserved=True,all_base_QA_diagnostics_preserved_pending_individual_classification=True,new_credit=0,full_goal_complete=False))
