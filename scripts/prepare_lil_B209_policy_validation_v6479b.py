"""Require the six written rowcount reasons even when shared QA reports informational differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_policy_validation_tools_v6479b')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/validate_lil_B209_native_policy_v6479.py','scripts/validate_lil_B209_native_policy_v6479b.py',{
        'policy_validation_v6479\')':'policy_validation_v6479b\')',
        "if issue['severity']=='warning' and issue['code']=='line-break-count' and bound['row_count_reason']:":"if issue['code']=='line-break-count' and bound['row_count_reason']:",
    });ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,prior_rejection='All20 compiled paragraphs and22 pages passed;the validator counted zero rowcount warnings because shared QA correctly reports those differences as info. Successor requires all six individual reasons regardless of diagnostic severity. Original failure retained;no prose,profile,native guard or source changed.',no_ROM_ledger_or_release_mutation=True,full_goal_complete=False))
