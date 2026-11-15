"""Prefer coherent source-sized R20 rows and an ordinary R38 verb/complement boundary."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_layout_refiner_v7393b')
if __name__=='__main__':
    assert not ROOT.exists()
    old="ordinary=row['id']=='DK4_MES_B229_R0048' and pair==('that',\"it's\")"
    new="ordinary=(row['id']=='DK4_MES_B229_R0048' and pair==('that',\"it's\")) or (row['id']=='DK4_MES_B229_R0038' and pair==('said','about'))"
    compare="if best is None or candidate[0]<best[0]:best=candidate"
    refined="if best is None or ((candidate[0][0],candidate[0][2],candidate[0][1],candidate[0][3]) if row['id']=='DK4_MES_B229_R0020' else candidate[0]) < ((best[0][0],best[0][2],best[0][1],best[0][3]) if row['id']=='DK4_MES_B229_R0020' else best[0]):best=candidate"
    r=derive('scripts/plan_lil_B229_layout_v7393.py','scripts/plan_lil_B229_layout_v7393b.py',{'layout_v7393':'layout_v7393b',old:new,compare:refined,'minimize_orphans_then_rows_before_weak_boundaries':'minimize_orphans_R20_coherent_boundaries_within_source_four_rows_ordinary_R38_complement_other_rows_before_weak_boundaries'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_two_record_layout_refinement.json',dict(tool=r,no_prose_word_punctuation_ororiginal_page_capacity_change=True,R20_from_andcalled_boundaries_require_coherent_review_before_native_freeze=True,R38_said_about_is_ordinary_verb_complement_not_global_weak_word_waiver=True,new_credit=0,full_goal_complete=False))
