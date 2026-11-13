"""Keep the reviewed B176 wording and align scoped wrap costs with punctuation-aware QA."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_punctuation_wrap_v4562')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B176_layout_v1.py','dk4tool/dialogue/lil_B176_layout_v2.py',{
        'end_word in weak':'_word(labels[end]) in weak',
        'end_word in BASE_WEAK':'_word(labels[end]) in BASE_WEAK',
        "'STRONG_ENDINGS':STRONG_ENDINGS":"'_word':_word,'STRONG_ENDINGS':STRONG_ENDINGS",
    }),derive('scripts/plan_lil_B176_layout_v4560.py','scripts/plan_lil_B176_layout_v4563.py',{
        'lil_B176_layout_v1':'lil_B176_layout_v2','lil_B176_layout_v4560':'lil_B176_layout_v4563',
    }),derive('scripts/verify_lil_B176_fonts_v4561.py','scripts/verify_lil_B176_fonts_v4564.py',{
        'lil_B176_layout_v1':'lil_B176_layout_v2','lil_B176_fonts_v4561':'lil_B176_fonts_v4564',
    })]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        original_failed_layout='work/analysis/lil_B176_layout_v4560/all10_paragraph_layout_QA.json',
        finding='Planner cost did not normalize a trailing comma while QA correctly recognized this,as a weak line ending.',
        reviewed_English_unchanged=True,scoped_cost_now_uses_same_word_normalization_as_QA=True,
        no_shared_metric_guard_selector_source_macro_or_bounds_change=True,no_waiver_orcredit_added=True,full_goal_complete=False))
    print('Prepared B176-only punctuation-aware wrap cost;prose and native metrics unchanged;initial failed plan preserved.')
