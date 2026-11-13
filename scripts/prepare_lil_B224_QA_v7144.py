"""Expose every original base-QA diagnostic before classifying reviewed boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_QA_tools_v7144')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/probe_lil_B223_base_QA_v7093.py';b='scripts/probe_lil_B224_base_QA_v7144.py'
    c={'B223':'B224','base_QA_v7093':'base_QA_v7144','layout_v7091d/seventeen_complete_paragraph_plans_original_width_no_prose_changes':'layout_v7142b/fifteen_whole_paragraph_plans_no_macros_no_prose_changes','native_pages_v7092c/all17_paragraphs19_complete_pages136_native_alignments':'native_pages_v7143/all15_paragraphs15_complete_native_pages120_alignments','[2,13,21,208]':'[26,197]','all17_base_QA_diagnostics_before_any_scoped_classification':'all15_base_QA_diagnostics_before_any_scoped_classification','seventeen measured native paragraphs':'fifteen measured native paragraphs','virtual_selector_for_formatter_only_not_a_stored_4100_body_byte=True':'no_virtual_selector_needed_in_fifteen_progressive_objects=True'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_base_QA_probe.json',dict(tool=row,no_QA_issue_removed_or_waived=True,fuller_openings_and_working_ellipsis_preserved=True,new_credit=0,full_goal_complete=False))
