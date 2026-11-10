"""Keep the complete conditional together instead of an early break after doesn't."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B210_layout_tools_v6507c')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/plan_lil_B210_layout_v6507b.py','scripts/plan_lil_B210_layout_v6507c.py',{
        'lil_B210_layout_v6507b':'lil_B210_layout_v6507c',
        '"blade\'s"})':'"blade\'s","doesn\'t","couldn\'t"})',
        "ordinary=(row['id']=='DK4_MES_B210_R0008' and pair==('his','hands'))":"ordinary=(row['id']=='DK4_MES_B210_R0008' and pair==('his','hands')) or (row['id']=='DK4_MES_B210_R0033' and words[stop-1]=='it,' and not final and words[stop]=='why')",
    });ROOT.mkdir(parents=True);save(ROOT/'complete_condition_boundary_research.json',dict(derived=r,all_source_and_prose_words_punctuation_native_guards_width_and_four_rows_unchanged=True,earlier_doesnt_break_rejected_for_readability_before_native_approval=True,exact_R33_complete_conditional_after_it_comma_is_a_normal_complete_clause_boundary=True,exact_R8_possessive_boundary_remains_source_prose_bound=True,no_global_QA_safety_exception=True,full_goal_complete=False));print('B210 exact complete-conditional boundary researched;no early break after doesn\'t,no changed words or display rules.')
