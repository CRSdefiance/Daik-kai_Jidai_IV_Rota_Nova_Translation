"""Refine complete-word paragraph preferences without changing any prose or native rule."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B233_layout_tools_v7538b')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/plan_lil_B233_layout_v7538.py','scripts/plan_lil_B233_layout_v7538b.py',{'layout_v7538':'layout_v7538b','ordinary=False':"ordinary=pair in {'DK4_MES_B233_R0012':{('scrap','of')},'DK4_MES_B233_R0020':{('of','ancient')},'DK4_MES_B233_R0039':{('they','deserve'),('look','for')}}.get(row['id'],set())"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_contextual_refinement.json',dict(tool=row,all_prose_andinitial_plan_preserved=True,R12_balanced_rows_R20_ancient_Greece_R39_for_it_complete_word_preferences=True,all_original_native_geometry_font_guards_pairphase_literal_I_rules_unchanged=True,all_actual_QA_diagnostics_remain_pending_individual_review_no_waiver_from_planning=True,new_credit=0,full_goal_complete=False))
