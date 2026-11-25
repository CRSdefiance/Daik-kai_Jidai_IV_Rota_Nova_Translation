"""Review two ordinary soft boundaries to avoid unnecessarily early openings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_fuller_wrap_tools_v7142b')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/plan_lil_B224_layout_v7142.py';b='scripts/plan_lil_B224_layout_v7142b.py'
    old="terminal=words[stop-1].rstrip('\"\\\')').endswith(('.', '!', '?', ';', ':'));weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS));tiny="
    # Bind the exact existing expression, leaving the source punctuation/terminal code intact.
    s=Path(a).read_text('utf8');weak="weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS))"
    replacement="ordinary=(row['id']=='DK4_MES_B224_R0005' and pair==('as','mysterious')) or (row['id']=='DK4_MES_B224_R0026' and pair==('the','medusa'));weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS))"
    c={"ROOT=Path('work/analysis/lil_B224_layout_v7142')":"ROOT=Path('work/analysis/lil_B224_layout_v7142b')",weak:replacement,'no_inherited_letter_style_or_multipage_exception=True':'no_inherited_letter_style_or_multipage_exception=True,two_exact_fuller_opening_soft_boundaries_not_global_weak_rule_change=True'}
    assert not Path(b).exists();checked_text(s,c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_fuller_openings.json',dict(tool=row,initial20_and22_character_openings_preserved_as_history=True,only_R5_as_mysterious_and_R26_the_Medusa_scoped_for_native_review=True,all_prose_guards_geometry_pair_phase_and_bare_I_ineligibility_unchanged=True,base_QA_diagnostics_not_waived_by_this_planning_step=True,new_credit=0,full_goal_complete=False))
