"""Correct only the replacement wrap cost; retain the original-source matching needle."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_punctuation_wrap_v4565')
if __name__=='__main__':
    assert not ROOT.exists()
    old="new='''                tail_cost[0] + int(not final and ((end_word in weak and not _noun_will_at(labels,end) and (end_word in BASE_WEAK or not _terminal_label(labels[end]))) or _split_pair(labels,end))),"
    new=old.replace('end_word in weak','_word(labels[end]) in weak').replace('end_word in BASE_WEAK','_word(labels[end]) in BASE_WEAK')
    tools=[derive('dk4tool/dialogue/lil_B176_layout_v1.py','dk4tool/dialogue/lil_B176_layout_v3.py',{
        old:new,"'STRONG_ENDINGS':STRONG_ENDINGS":"'_word':_word,'STRONG_ENDINGS':STRONG_ENDINGS",
    }),derive('scripts/plan_lil_B176_layout_v4560.py','scripts/plan_lil_B176_layout_v4566.py',{
        'lil_B176_layout_v1':'lil_B176_layout_v3','lil_B176_layout_v4560':'lil_B176_layout_v4566',
    }),derive('scripts/verify_lil_B176_fonts_v4561.py','scripts/verify_lil_B176_fonts_v4567.py',{
        'lil_B176_layout_v1':'lil_B176_layout_v3','lil_B176_fonts_v4561':'lil_B176_fonts_v4567',
    })]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        original_failed_plan_and_v2_import_failure_preserved=True,old_original_function_match_needle_unchanged=True,
        only_scoped_replacement_cost_and_namespace_corrected=True,reviewed_prose_native_metrics_guards_and_waivers_unchanged=True,
        no_credit_added=True,full_goal_complete=False))
    print('Prepared B176 layout v3:punctuation-normalized cost,original matching needle preserved;earlier drafts/failures retained.')
