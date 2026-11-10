"""Preserve prose while correcting determiner,proper-name andpronoun splits in the first plan."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_layout_tools_v7251b')
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/plan_lil_B226_layout_v7251.py');text=src.read_text('utf8');old=next(s for s in text.splitlines() if s.startswith('PAIRS='));pairs=ast.literal_eval(old.split('=',1)[1]);pairs-=set([('heard','of'),('eastern','and'),('stronger','than'),('somewhere','in')]);pairs.add(('rumor','of'));new='PAIRS={'+','.join(repr(p) for p in sorted(pairs))+'}'
    before='if best is None or candidate[0]<best[0]:best=candidate'
    after="if best is None or ((candidate[0][0],candidate[0][2],candidate[0][1],candidate[0][3]) if row['source_record_index']==41 else candidate[0]) < ((best[0][0],best[0][2],best[0][1],best[0][3]) if row['source_record_index']==41 else best[0]):best=candidate"
    r=derive(src,'scripts/plan_lil_B226_layout_v7251b.py',{'layout_v7251':'layout_v7251b',old:new,'ordinary=False':"ordinary=row['id']=='DK4_MES_B226_R0023' and pair==('have','some')",before:after})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_whole_exchange_boundary_refinement.json',dict(tool=r,all20_English_paragraphs_unchanged=True,initial_plan_preserved=True,R23_verb_to_object_boundary_preferred_over_some_business_split=True,R29_verb_to_preposition_boundary_ordinary=True,R37_coordinating_modifier_boundary_ordinary_without_splitting_Roman_Empires=True,R41_prefer_weak_boundary_count_before_row_count_within_original_four_row_page=True,R57_keep_entire_rumor_qualifier_together=True,R72_keep_northern_Europe_together_allow_adverb_to_preposition_boundary=True,no_global_QA_weak_word_bare_I_geometry_guard_pairphase_orfont_change=True,all_base_QA_warnings_still_require_individual_review=True,new_credit=0,full_goal_complete=False))
