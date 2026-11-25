"""Keep the complete named shield together and avoid a dangling about in the callback."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_named_item_wrap_refiner_v7393c')
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/plan_lil_B229_layout_v7393b.py').read_text('utf8');old=next(s for s in src.splitlines() if s.startswith('PAIRS='));pairs=ast.literal_eval(old.split('=',1)[1]);pairs.add(('about','the'))
    boundary="ordinary=(row['id']=='DK4_MES_B229_R0048' and pair==('that',\"it's\")) or (row['id']=='DK4_MES_B229_R0038' and pair==('said','about'))"
    updated=boundary+" or (row['id']=='DK4_MES_B229_R0020' and pair==('it','the'))"
    r=derive('scripts/plan_lil_B229_layout_v7393b.py','scripts/plan_lil_B229_layout_v7393c.py',{old:'PAIRS='+repr(pairs),boundary:updated,'layout_v7393b':'layout_v7393c'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_named_item_boundary_review.json',dict(tool=r,R20_People_called_it_then_full_named_item_is_ordinary_predicate_complement_boundary=True,R38_said_about_preposition_starts_complement_instead_of_dangling_end=True,no_prose_change_added_page_or_global_QA_weak_word_bare_I_font_guard_change=True,new_credit=0,full_goal_complete=False))
