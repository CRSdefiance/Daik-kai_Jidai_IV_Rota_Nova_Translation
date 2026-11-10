"""Keep the short favorite-general question intact without adding a row or changing prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_question_tools_v6608')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/plan_lil_B212_layout_v6605b.py').read_text();anchor=next(l for l in source.splitlines() if l.startswith('PAIRS='));proof=derive('scripts/plan_lil_B212_layout_v6605b.py','scripts/plan_lil_B212_layout_v6608.py',{'lil_B212_layout_v6605b':'lil_B212_layout_v6608',anchor:anchor+'\nWEAK.add("who\'s");PAIRS.add(("who\'s","your"))'});ROOT.mkdir(parents=True);save(ROOT/'whole_question_same_two_rows_no_prose_change.json',dict(proof=proof,record='DK4_MES_B212_R0032',reason='The greeting and complete favorite-general question each fit their own row. Keep Who\'s your favorite general? intact rather than ending the first row at Who\'s. Same words, two rows and original native geometry.',all_other_paragraph_plans_expected_unchanged=True,new_credit=0,full_goal_complete=False))
