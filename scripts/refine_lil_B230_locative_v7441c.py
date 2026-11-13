"""Keep in northern Europe together, preserving the measured warning and earlier pages."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_layout_tools_v7441c')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/plan_lil_B230_layout_v7441b.py','scripts/plan_lil_B230_layout_v7441c.py',{'layout_v7441b':'layout_v7441c',"('in','northern')":"('somewhere','in')"}),('scripts/verify_lil_B230_native_pages_v7442.py','scripts/verify_lil_B230_native_pages_v7442b.py',{'layout_v7441b':'layout_v7441c','native_pages_v7442':'native_pages_v7442b'}),('scripts/probe_lil_B230_base_QA_v7443.py','scripts/probe_lil_B230_base_QA_v7443b.py',{'layout_v7441b':'layout_v7441c','native_pages_v7442':'native_pages_v7442b','base_QA_v7443':'base_QA_v7443b'})]
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_R50_locative_refinement.json',dict(tools=rows,all17_prose_paragraphs_unchanged=True,R50_complete_in_northern_Europe_phrase_preserved=True,earlier_warning_andnative_planes_retained=True,no_global_weak_word_QA_guard_literal_I_orfont_change=True,new_credit=0,full_goal_complete=False))
