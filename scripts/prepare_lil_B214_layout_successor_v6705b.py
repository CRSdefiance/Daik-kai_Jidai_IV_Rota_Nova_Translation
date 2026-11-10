"""Keep the first research plan; refine only individually reviewed natural phrase boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_layout_successor_v6705b')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/plan_lil_B214_layout_v6705.py','scripts/plan_lil_B214_layout_v6705b.py',{
        "layout_v6705')":"layout_v6705b')",
        "('letter','from'),":"",
        "('lead','to')}":"('lead','to'),('after','all'),('like','janus')}",
        "weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS));tiny=":"ordinary=pair in {'DK4_MES_B214_R0034':{('you','from')},'DK4_MES_B214_R0044':{('to','judas'),('twelve','disciples')}}.get(row['id'],set());weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS));tiny=",
        "exact_weak_boundaries_and_native_first_last_glyphs_require_review=True":"exact_weak_boundaries_and_native_first_last_glyphs_require_review=True,exact_ordinary_boundary_research_reasons={'DK4_MES_B214_R0034':'The completed to-you recipient phrase may precede the from-road adjunct across an ordinary wrap; do not force an early break after writing to avoid the pronoun you.','DK4_MES_B214_R0044':'Ordinary complete-word to/Judas and twelve/disciples wraps are researched to avoid an unnecessarily short opening row. All source ownership, appositive and location words remain intact. Native full-width, glyph, guard, bound and QA checks remain required.'},letter_from_sender_adjunct_is_ordinary_not_inseparable_phrase=True,after_all_and_like_Janus_groups_preferred_without_added_rows=True,no_global_QA_warning_glyph_guard_or_bounds_waiver=True"
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_phrase_boundary_successor.json',dict(derivation=proof,first_plan_retained=True,all_editable_prose_and_native_width_guards_unchanged=True,all_formatting_gates_still_false=True,full_goal_complete=False))
