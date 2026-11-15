"""Remove unnecessary short openings using exact ordinary grammatical boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_layout_tools_v7489b')
if __name__=='__main__':
    assert not ROOT.exists();ordinary="ordinary=pair in {'DK4_MES_B231_R0005':{('you','heard')},'DK4_MES_B231_R0020':{('how','to')},'DK4_MES_B231_R0024':{('it','if')},'DK4_MES_B231_R0035':{('but','i'),('the','far')},'DK4_MES_B231_R0062':{(\"we'll\",'have')}}.get(row['id'],set())"
    row=derive('scripts/plan_lil_B231_layout_v7489.py','scripts/plan_lil_B231_layout_v7489b.py',{'layout_v7489':'layout_v7489b','ordinary=False':ordinary});ROOT.mkdir(parents=True);save(ROOT/'source_locked_contextual_boundary_refinement.json',dict(tool=row,all16_prose_paragraphs_unchanged=True,R5_subject_predicate_R20_clause_infinitive_R24_condition_R62_subject_predicate_boundaries=True,R35_conjunction_subject_andarticle_modifier_complete_word_wrap_preserves_whole_last_region_phrase=True,R35_exact_base_QA_article_warning_must_be_retained_andindividually_reviewed_not_globally_weakened=True,no_font_viewport_guard_pairphase_literal_I_orbase_QA_change=True,new_credit=0,full_goal_complete=False))
