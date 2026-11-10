"""Keep two normal verb/complement wraps source-bound instead of forcing extra short rows."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_layout_tools_v6462d')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/plan_lil_B209_research_v6462c.py','scripts/plan_lil_B209_research_v6462d.py',{
        'layout_research_v6462c\')':'layout_research_v6462d\')',
        "('come','in'),(\"that's\",'yukihisa')}":"('come','in'),(\"that's\",'yukihisa'),('wipe','them')}",
        "weak=int(not final and (((word in WEAK and not terminal) and not particle_in) or pair in PAIRS))":"ordinary_report=(row['id']=='DK4_MES_B209_R0027' and pair in [('said','to'),('are','afoot')])\n            weak=int(not final and (((word in WEAK and not terminal) and not particle_in and not ordinary_report) or pair in PAIRS))",
        'first_letter_wrap_reasons_pending_exact_visual_review=True':'first_letter_wrap_reasons_pending_exact_visual_review=True,exact_report_complement_boundaries_researched=[\'said/to\',\'are/afoot\'],report_boundary_reason=\'These are normal complete-word wraps between the reporting verb and its to-infinitive complement,and between the copula and afoot. Allowing only these exact source/prose combinations avoids an unnecessary extra short row while preserving the complete clause and all words. No global auxiliary,phrase,glyph,guard,bounds or page exemption.\'',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,all_manuscript_words_punctuation_and_controls_unchanged=True,only_exact_first_letter_report_boundaries_changed_in_research_cost=True,actual_native_pages_and_visual_editorial_review_still_pending=True,full_goal_complete=False))
