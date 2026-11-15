"""Bind the unmodified base QA to all eleven complete native paragraphs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B216_QA_tools_v6797')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/probe_lil_B215_paragraph_QA_v6753.py';b='scripts/probe_lil_B216_paragraph_QA_v6797.py';c={'B215':'B216','base_QA_v6753':'base_QA_v6797','layout_v6747c/fifteen_whole_paragraph_plans_two_FA_no_prose_changes':'layout_v6791b/eleven_whole_paragraph_plans_no_macros_no_prose_changes','native_pages_v6752/all15_paragraphs15_complete_native_pages120_alignments':'native_pages_v6792/all11_paragraphs11_complete_native_pages88_alignments','[2,23,120]':'[2,9,82,151,169]','all15_base_QA':'all11_base_QA'};assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);proof=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_base_QA.json',proof)
