"""Preserve every original base-QA diagnostic before any individual classification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_base_QA_tools_v7253')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/probe_lil_B225_base_QA_v7193.py','scripts/probe_lil_B226_base_QA_v7253.py',{'B225':'B226','base_QA_v7193':'base_QA_v7253','layout_v7191b/thirteen_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7251b/twenty_whole_paragraph_plans_no_macros_no_prose_changes','native_pages_v7192/all13_paragraphs14_complete_native_pages104_alignments':'native_pages_v7252/all20_paragraphs20_complete_native_pages160_alignments','[2,16,151,162]':'[2,23]','all13_base_QA_diagnostics':'all20_base_QA_diagnostics','thirteen':'twenty'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_unmodified_base_QA.json',r)
