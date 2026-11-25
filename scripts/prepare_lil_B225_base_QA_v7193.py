"""Preserve all ordinary QA diagnostics before scoped paragraph/layout review."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_QA_tools_v7193')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/probe_lil_B224_base_QA_v7144.py';b='scripts/probe_lil_B225_base_QA_v7193.py';assert not Path(b).exists()
    changes={'B224':'B225','base_QA_v7144':'base_QA_v7193','layout_v7142b/fifteen_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7191b/thirteen_whole_paragraph_plans_no_macros_no_prose_changes','native_pages_v7143/all15_paragraphs15_complete_native_pages120_alignments':'native_pages_v7192/all13_paragraphs14_complete_native_pages104_alignments','[26,197]':'[2,16,151,162]','all15_base_QA':'all13_base_QA','fifteen measured':'thirteen measured','fifteen_progressive_objects':'thirteen_progressive_objects'}
    row=derive(a,b,changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_unmodified_base_QA.json',dict(tool=row,source_R26_two_pages_are_original_four_row_pages_not_taller_geometry=True,all_original_base_QA_diagnostics_retained=True,no_warning_waiver_or_native_font_guard_change=True,new_credit=0))
