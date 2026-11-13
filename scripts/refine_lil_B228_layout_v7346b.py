"""Avoid a seven-cell opening andfragmented emphasis without changing any prose orgeometry."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_layout_tools_v7346b')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/plan_lil_B228_layout_v7346.py','scripts/plan_lil_B228_layout_v7346b.py',{'layout_v7346':'layout_v7346b',"ordinary=False;weak=":"ordinary=row['id']=='DK4_MES_B228_R0034' and pair==('that',\"it's\");weak=",'if best is None or candidate[0]<best[0]:best=candidate':"if best is None or ((candidate[0][0],candidate[0][2],candidate[0][1],candidate[0][3]) if row['id']=='DK4_MES_B228_R0028' else candidate[0]) < ((best[0][0],best[0][2],best[0][1],best[0][3]) if row['id']=='DK4_MES_B228_R0028' else best[0]):best=candidate",'minimize_orphans_then_rows_before_weak_boundaries=True':'minimize_orphans_then_R28_coherent_boundaries_within_original_four_rows_other_rows_before_weak_boundaries=True'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_two_record_boundary_refinement.json',dict(tool=r,all13_English_paragraphs_exact=True,R34_that_its_complete_word_clause_boundary_review_required=True,R28_uses_original_four_rows_to_avoid_fragmented_comparative_andJust_think=True,no_global_QA_font_viewport_guard_pair_phase_orbare_I_change=True,new_credit=0,full_goal_complete=False))
