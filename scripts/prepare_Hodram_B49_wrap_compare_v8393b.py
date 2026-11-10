"""Compare only two additional phrase-preserving alternatives; retain the earlier read-only comparisons."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_wrap_compare_tools_v8393b');assert not root.exists()
    d=derive('scripts/compare_Hodram_B49_wrap_v8393a.py','scripts/compare_Hodram_B49_wrap_v8393b.py',{
        'Hodram_B49_wrap_compare_v8393a':'Hodram_B49_wrap_compare_v8393b',
        "[('article-before-New-World',('the','new')),('preposition-before-the-New-World',('in','the'))]":"[('coherent-four-rows',None),('complete-word-New-World-boundary',('new','world'))]",
        "{(\"i'd\",'trade'),('give','me')}":"{(\"i'd\",'trade'),('give','me'),('now','give'),('find','it'),('give','you')}",
    })
    root.mkdir(parents=True);save(root/'two_additional_read_only_candidates.json',dict(derivation=d,no_prose_native_metric_orQA_guard_change=True,new_credit=0,full_goal_complete=False))
