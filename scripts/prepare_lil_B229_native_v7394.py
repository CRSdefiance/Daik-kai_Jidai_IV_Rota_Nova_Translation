"""Prepare all seventeen native pages and unchanged base QA against the final whole-paragraph plan."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_native_tools_v7394')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B228':'B229','layout_v7346b/thirteen_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7393c/seventeen_whole_paragraph_plans_no_macros_no_prose_changes'}
    native={**common,'current_V7324_native_v7329':'current_V7371_native_v7376','native_pages_v7347':'native_pages_v7394','source_pages_v7342/all13_clean_objects':'source_pages_v7389/all17_clean_objects',"len(plan['records'])==13":"len(plan['records'])==17",'len(cases)==13 and len(pictures)==13 and alignments==104':'len(cases)==17 and len(pictures)==17 and alignments==136','all13_complete_pages_sheet':'all17_complete_pages_sheet','all13_paragraphs13_complete_native_pages104_alignments':'all17_paragraphs17_complete_native_pages136_alignments','complete_native_pages=13,logical_compiled_input_alignment_cases=104':'complete_native_pages=17,logical_compiled_input_alignment_cases=136','all13_single_original_four_row_pages':'all17_single_original_four_row_pages','all13_complete_prose_paragraphs':'all17_complete_prose_paragraphs','all13_formatting_gates_remain_false':'all17_formatting_gates_remain_false','13 paragraphs/13 complete native pages/104 alignments':'17 paragraphs/17 complete native pages/136 alignments'}
    qa={**common,'base_QA_v7348':'base_QA_v7395','native_pages_v7347/all13_paragraphs13_complete_native_pages104_alignments':'native_pages_v7394/all17_paragraphs17_complete_native_pages136_alignments','all13_base_QA_diagnostics':'all17_base_QA_diagnostics','thirteen':'seventeen'}
    jobs=[('scripts/verify_lil_B228_native_pages_v7347.py','scripts/verify_lil_B229_native_pages_v7394.py',native),('scripts/probe_lil_B228_base_QA_v7348.py','scripts/probe_lil_B229_base_QA_v7395.py',qa)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_native_andbase_QA.json',dict(tools=rows,all17_English_paragraphs_unchanged=True,source216x64_four_rows_guard_pairphase_font_bounds_canaries_andbare_I_rules_preserved=True,all_base_QA_diagnostics_pending_individual_classification=True,new_credit=0,full_goal_complete=False))
