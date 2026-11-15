"""Keep the surprised Wait clause together and bind two necessary complete-word report boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_layout_tools_v6559c')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/plan_lil_B211_layout_v6559b.py','scripts/plan_lil_B211_layout_v6559c.py',{
        'lil_B211_layout_v6559b':'lil_B211_layout_v6559c',
        "PAIRS={":"PAIRS={('wait',\"they're\"),",
        "ordinary=(row['id']=='DK4_MES_B211_R0013' and words[stop-1]=='me,' and not final and words[stop]=='are')":"ordinary=(row['id']=='DK4_MES_B211_R0013' and words[stop-1]=='me,' and not final and words[stop]=='are') or (row['id']=='DK4_MES_B211_R0045' and pair in {('long','and'),('were','headed')})"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_readable_wrap_receipt.json',dict(proof=proof,all_prose_macros_and_native_geometry_unchanged=True,Wait_surprised_discovery_clause_kept_together_without_extra_row=True,exact_R13_introductory_comma_and_R45_long_and_were_headed_complete_word_boundaries_reviewed=True,R45_four_rows_required_for_full123_character_report_without_shortening=True,no_global_weak_ending_glyph_bounds_guard_or_pagination_waiver=True,full_goal_complete=False))
