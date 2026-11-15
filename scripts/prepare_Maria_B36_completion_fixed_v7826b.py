"""Repair hash-key spelling caught before the completion transaction was executed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_B36_completion_repair_v7826b')
    assert not root.exists()
    result=derive('scripts/complete_Maria_B36_v7826.py','scripts/complete_Maria_B36_v7826b.py',
        {'sha120':'sha256'})
    root.mkdir(parents=True)
    save(root/'provenance.json',dict(derivation=result,
        issue='Pre-execution inspection caught broad count substitution touching sha256 key spellings.',
        only_hash_key_spelling_repaired=True,all_numeric_native_andtransaction_guards_preserved=True,
        original_preparer_andgenerated_source_preserved=True,no_completion_targets_changed=True,full_goal_complete=False))
