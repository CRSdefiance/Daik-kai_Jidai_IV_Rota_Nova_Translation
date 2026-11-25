"""Review name/title boundaries locally; avoid an unnecessary fourth row in R72."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_readable_layout_tools_v6605b')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/plan_lil_B212_layout_v6605.py').read_text();pairs=next(l for l in source.splitlines() if l.startswith('PAIRS='));weak=next(l for l in source.splitlines() if l.startswith('WEAK.update'));newpairs=pairs[:-1]+",('cao',\"cao's\"),(\"cao's\",'army')}"
    ordinary="ordinary=(row['id']=='DK4_MES_B212_R0072' and pair==('magnificent','beard')) or (row['id']=='DK4_MES_B212_R0078' and pair==('before','the'))"
    proof=derive('scripts/plan_lil_B212_layout_v6605.py','scripts/plan_lil_B212_layout_v6605b.py',{'lil_B212_layout_v6605':'lil_B212_layout_v6605b',pairs:newpairs,weak:weak+'\nWEAK.update({"he\'s","on","about","before","through"})','ordinary=False':ordinary})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_name_title_boundary_review.json',dict(proof=proof,R72_reason='All94 characters fit three native rows. The unavoidable complete-word boundary within the literary epithet Magnificent/Beard is preferable to an unnecessary fourth row and a stranded He\'s. No name, honorific, praise or punctuation changes.',R78_reason='All129 characters require four rows. Before/the is a complete-word soft wrap within the named memorial title; it preserves the full title, emotional response and preference without a fifth row or prose reduction.',Cao_Cao_possessive_name_and_army_stay_together=True,no_runtime_font_viewport_guard_or_global_QA_waiver=True,prose_unchanged=True,all14_formatting_gates_still_false=True,new_credit=0,full_goal_complete=False))
