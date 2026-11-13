"""Preserve the stopped checkpoint preparer; bind replacement keys to original source text."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_checkpoint_preparer_repair_v8640b');assert not root.exists()
    extra="""        'V8600 staged: six targets, five uncredited all-gate/frozen-policy/all-production decisions. Exact inverse audit next.':'V8640 staged: six targets, five uncredited four-prose-gate decisions; native speech/menu reviewed, formatting false. Exact inverse audit next.',
        'Audited zero-credit B51 contextual/native/stored checkpoint; full goal intact.':'Audited zero-credit B52 contextual/native-speech/menu checkpoint; full goal intact.',
        'V8600':'V8640','V8601':'V8641',"""
    result=derive('scripts/prepare_Hodram_B52_checkpoint_v8640.py','scripts/prepare_Hodram_B52_checkpoint_v8640b.py',{
        "Path('work/analysis/Hodram_B52_checkpoint_tools_v8640')":"Path('work/analysis/Hodram_B52_checkpoint_tools_v8640b')",
        "'Verified V8641/current V8543: 7224 completed;":"'Verified V8601/current V8543: 7224 completed;",
        "        'V8600':'V8640','V8601':'V8641',":extra,
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,prior_failure='Derivation key used successor label V8641; original frozen source says V8601',original_failed_preparer_preserved=True,no_prior_checkpoint_orshared_targets_written=True,all_counter_inverse_native_scope_andformatting_false_guards_preserved=True,new_credit=0,full_goal_complete=False))
