"""Expose unchanged base QA for the new full-width single/multipage plans."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_QA_tools_v6659')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/probe_lil_B212_paragraph_QA_v6613.py','scripts/probe_lil_B213_paragraph_QA_v6659.py',{'B212':'B213','base_QA_v6613':'base_QA_v6659','editorial_manuscript_v2':'editorial_manuscript_v1','layout_v6608/nine_whole_paragraph_research_plans':'layout_v6655b/eighteen_whole_paragraph_plans_one_original_page_continuation','question_native_v6609/all9_complete_pages72_alignments8_fresh64_exact_reused':'native_pages_v6657/all18_paragraphs19_complete_native_pages144_alignments','max_lines=4':"max_lines=p['max_total_rows']",'frozenset([149])':'frozenset([2,9,170])','all9_base_QA':'all18_base_QA'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_base_QA.json',proof)
