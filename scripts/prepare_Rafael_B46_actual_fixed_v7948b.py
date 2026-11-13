"""Preserve the failed derivation and correct only its quoted display-label match."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_actual_correction_v7948b');assert not root.exists()
    row=derive('scripts/prepare_Rafael_B46_actual_v7948.py','scripts/prepare_Rafael_B46_actual_v7948b.py',{
        '"f\'Rafael {version} R":"f\'Rafael {version} {choice} R"':'"Rafael {version} R":"Rafael {version} {choice} R"'})
    root.mkdir(parents=True);save(root/'source_locked_correction.json',dict(derivation=row,
        prior_absent_display_label_key_before_any_audit_orROM_mutation_preserved=True,new_credit=0,full_goal_complete=False))
