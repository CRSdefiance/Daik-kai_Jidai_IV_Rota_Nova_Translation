"""Repair the stopped successor preparer's duplicate separator before derivation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_shared_schema_repair_v8773c');assert not root.exists()
    receipt=derive('scripts/prepare_Hodram_B31_B53_shared_schema_v8773b.py','scripts/prepare_Hodram_B31_B53_shared_schema_v8773c_ready.py',{
        "positive_source_sha256=sha(old_positive.read_bytes()),'":"positive_source_sha256=sha(old_positive.read_bytes())'",
        'Hodram_B31_B53_shared_schema_v8773b':'Hodram_B31_B53_shared_schema_v8773c',
        'Hodram_B31_B53_shared_extension_v8773b':'Hodram_B31_B53_shared_extension_v8773c',
        'validate_Hodram_B31_B53_shared_v8773b.py':'validate_Hodram_B31_B53_shared_v8773c.py',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,duplicate_separator_fixed_before_any_target_module_was_created=True,
        stopped_preparer_andcompleted_original_positive_preserved=True,no_completed_actual_native_orpositive_replay=True,new_credit=0,full_goal_complete=False))
