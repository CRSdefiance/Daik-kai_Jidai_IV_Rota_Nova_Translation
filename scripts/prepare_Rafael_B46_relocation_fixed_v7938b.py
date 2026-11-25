"""Preserve failed path binding; correct only duplicated research path prefixes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_relocation_tools_v7938b');assert not root.exists()
    row=derive('scripts/relocate_Rafael_B46_v7938.py','scripts/relocate_Rafael_B46_v7938b.py',{
        'work/analysis/work/analysis/':'work/analysis/'})
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=row,path_only_no_relocation_guard_orbyte_change=True,
        previous_missing_path_failure_before_any_archive_orROM_mutation_preserved=True,new_credit=0,full_goal_complete=False))
