"""Preserve unmodified base QA before classifying reviewed B222 line boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_QA_tools_v7048')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/probe_lil_B221_paragraph_QA_v6982b.py','scripts/probe_lil_B222_paragraph_QA_v7048.py',{
        'B221':'B222','base_QA_v6982b':'base_QA_v7048','editorial_manuscript_v1.json':'editorial_manuscript_v2.json',
        'layout_v6976c/fourteen_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7046b/sixteen_whole_paragraph_plans_no_macros_no_prose_changes',
        'native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments':'native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments',
        'frozenset([2,17,85])':'frozenset([2,16])','all14_base_QA':'all16_base_QA'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_unmodified_QA.json',dict(tool=tool,no_diagnostic_filter_or_warning_waiver=True,new_credit=0,full_goal_complete=False))
