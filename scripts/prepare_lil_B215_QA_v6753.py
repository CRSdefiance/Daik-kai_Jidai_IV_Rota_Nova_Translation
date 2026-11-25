"""Keep the complete unmodified base QA report for every measured paragraph."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B215_QA_tools_v6753')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/probe_lil_B213_paragraph_QA_v6659.py';b='scripts/probe_lil_B215_paragraph_QA_v6753.py';c={'B213':'B215','base_QA_v6659':'base_QA_v6753','layout_v6655b/eighteen_whole_paragraph_plans_one_original_page_continuation':'layout_v6747c/fifteen_whole_paragraph_plans_two_FA_no_prose_changes','native_pages_v6657/all18_paragraphs19_complete_native_pages144_alignments':'native_pages_v6752/all15_paragraphs15_complete_native_pages120_alignments','[2,9,170]':'[2,23,120]','all18_base_QA':'all15_base_QA'};assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);proof=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_base_QA.json',proof)
