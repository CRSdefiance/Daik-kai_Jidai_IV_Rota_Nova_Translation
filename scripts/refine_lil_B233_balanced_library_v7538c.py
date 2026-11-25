"""Keep the complete Alexandria phrase while balancing the library paragraph."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B233_layout_tools_v7538c')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/plan_lil_B233_layout_v7538b.py','scripts/plan_lil_B233_layout_v7538c.py',{'layout_v7538b':'layout_v7538c',"{('scrap','of')}":"{('scrap','of'),('library','in')}"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_balanced_library_refinement.json',dict(tool=row,R12_complete_word_noun_complement_andlocation_boundaries_reviewed_as_preferences=True,R20_ancient_Greece_kept_on_same_native_page_not_forced_onto_one_row=True,R20_last_clause_with_ancient_would_be36_cells_exceeding35_continuation_capacity=True,all_prose_prior_plans_geometry_font_guards_andQA_preserved=True,no_warning_waiver_orprose_credit_from_planning=True,new_credit=0,full_goal_complete=False))
