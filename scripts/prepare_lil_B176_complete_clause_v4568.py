"""Recognize the complete source-reviewed flavor clause without weakening other wrap rules."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_complete_clause_v4568')
if __name__=='__main__':
    assert not ROOT.exists()
    old='''def _noun_will_at(labels,index):
    # Exact complete first clause: will is a noun, not a stranded auxiliary.
    return (index >= 3 and labels[index].endswith(',')
        and tuple(_word(v) for v in labels[index-3:index+1]) == ('where',"there's",'a','will'))'''
    new='''def _complete_clause_at(labels,index):
    # Exact complete clauses: the final word belongs to the completed phrase.
    return ((index >= 3 and labels[index].endswith(',')
        and tuple(_word(v) for v in labels[index-3:index+1]) == ('where',"there's",'a','will'))
        or (index >= 4 and labels[index].endswith(',')
        and tuple(_word(v) for v in labels[index-4:index+1]) == ('with','a','flavor','like','this')))'''
    tools=[derive('dk4tool/dialogue/lil_B176_layout_v1.py','dk4tool/dialogue/lil_B176_layout_v4.py',{
        old:new,'_noun_will_at':'_complete_clause_at',
    }),derive('scripts/plan_lil_B176_layout_v4560.py','scripts/plan_lil_B176_layout_v4569.py',{
        'lil_B176_layout_v1':'lil_B176_layout_v4','lil_B176_layout_v4560':'lil_B176_layout_v4569',
    }),derive('scripts/verify_lil_B176_fonts_v4561.py','scripts/verify_lil_B176_fonts_v4570.py',{
        'lil_B176_layout_v1':'lil_B176_layout_v4','lil_B176_fonts_v4561':'lil_B176_fonts_v4570',
    })]
    from dk4tool.dialogue.lil_B176_layout_v4 import _complete_clause_at
    assert _complete_clause_at('Yes! With a flavor like this,'.split(),5)
    assert not _complete_clause_at(['this,'],0)
    assert not _complete_clause_at('Buy this,'.split(),1)
    assert not _complete_clause_at('With a flavor like this'.split(),4)
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        corrected_diagnosis='The shared balanced planner already normalizes punctuation. R13 has a grammatically complete with-a-flavor-like-this clause. The scoped weak-word QA needs the same narrow complete-clause recognition already used for a noun will.',
        previous_punctuation_hypothesis_drafts_and_failed_plans_preserved=True,exact_reviewed_comma_clause_positive_case=True,
        unrelated_this_comma_and_missing_comma_cases_stay_rejected=True,prose_and_native_metrics_guards_and_all_other_wrap_rules_unchanged=True,
        no_manual_break_or_QA_waiver_orcredit_added=True,full_goal_complete=False))
    print('Prepared B176-only exact complete-clause rule;prose and all native metrics/guards unchanged. Earlier failed hypotheses preserved.')
