"""Prepare nine complete native pages and unchanged base-QA diagnostics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_native_tools_v7299')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B226':'B227','manuscript_v1.json':'manuscript_v1b.json','layout_v7251b/twenty_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7298b/nine_whole_paragraph_plans_no_macros_no_prose_changes','[2,23]':'[2,25]','native_pages_v7252/all20_paragraphs20_complete_native_pages160_alignments':'native_pages_v7299/all9_paragraphs9_complete_native_pages72_alignments'}
    native={**common,'current_V7230_native_v7235':'current_V7277_native_v7282','native_pages_v7252':'native_pages_v7299','source_pages_v7247/all20_clean_objects':'source_pages_v7294/all9_clean_objects',"len(plan['records'])==20":"len(plan['records'])==9",'len(cases)==20 and len(pictures)==20 and alignments==160':'len(cases)==9 and len(pictures)==9 and alignments==72','all20_complete_pages_sheet':'all9_complete_pages_sheet','all20_paragraphs20_complete_native_pages160_alignments':'all9_paragraphs9_complete_native_pages72_alignments','complete_native_pages=20,logical_compiled_input_alignment_cases=160':'complete_native_pages=9,logical_compiled_input_alignment_cases=72','all20_single_original_four_row_pages':'all9_single_original_four_row_pages','all20_complete_prose_paragraphs':'all9_complete_prose_paragraphs','only_original_static_selectors2_23':'only_original_static_selectors2_25','all20_formatting_gates_remain_false':'all9_formatting_gates_remain_false','20 paragraphs/20 complete native pages/160 alignments':'9 paragraphs/9 complete native pages/72 alignments'}
    # The native tool has the combined path split into ROOT and filename literals.
    native.pop('native_pages_v7252/all20_paragraphs20_complete_native_pages160_alignments')
    qa={**common,'base_QA_v7253':'base_QA_v7300','all20_base_QA_diagnostics':'all9_base_QA_diagnostics','twenty':'nine'}
    jobs=[('scripts/verify_lil_B226_native_pages_v7252.py','scripts/verify_lil_B227_native_pages_v7299.py',native),('scripts/probe_lil_B226_base_QA_v7253.py','scripts/probe_lil_B227_base_QA_v7300.py',qa)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_native_pages_andbase_QA.json',dict(tools=rows,all9_prose_paragraphs_unchanged=True,original216x64_four_rows_native_font_guard_pairphase_bounds_canaries_andbare_I_rules_preserved=True,all_base_QA_diagnostics_preserved_pending_individual_review=True,new_credit=0,full_goal_complete=False))
