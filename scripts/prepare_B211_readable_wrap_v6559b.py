"""Prefer a complete introductory phrase over an unnecessary fourth row in the swan question."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_layout_tools_v6559b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/plan_lil_B211_layout_v6559.py','scripts/plan_lil_B211_layout_v6559b.py',{
        'lil_B211_layout_v6559':'lil_B211_layout_v6559b',
        'WEAK.update({':'WEAK.update({\'on\',\'there\',\'like\',',
        "weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS))":"ordinary=(row['id']=='DK4_MES_B211_R0013' and words[stop-1]=='me,' and not final and words[stop]=='are');weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS))"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_readable_wrap_receipt.json',dict(proof=proof,whole_prose_punctuation_macros_and_native_geometry_unchanged=True,initial_R13_four_rows_revisited_for_unnecessary_early_wrapping=True,exact_R13_complete_introductory_Tell_me_comma_boundary_not_global_waiver=True,full_native_glyphs_bounds_pages_and_QA_still_required=True,full_goal_complete=False))
