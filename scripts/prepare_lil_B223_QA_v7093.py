"""Expose unmodified per-object QA with virtual typed selectors and native total-row bounds."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_QA_tools_v7093')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/probe_lil_B214_base_QA_v6707.py','scripts/probe_lil_B223_base_QA_v7093.py',{'B214':'B223','base_QA_v6707':'base_QA_v7093','layout_v6705b':'layout_v7091d','native_pages_v6706/all17_complete_single_pages136_native_alignments':'native_pages_v7092c/all17_paragraphs19_complete_pages136_native_alignments','max_lines=4,leading_speaker_bytes=frozenset([2,4,23,208])':"max_lines=p['max_total_rows'],leading_speaker_bytes=frozenset([2,13,21,208])"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_unmodified_base_QA.json',dict(tool=tool,all_diagnostics_preserved_without_waiver_or_filter=True,maximum_total_rows_not_physical_page_height=True,new_credit=0,full_goal_complete=False))
