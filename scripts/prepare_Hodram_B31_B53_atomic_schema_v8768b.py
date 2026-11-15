"""Bind the exact existing four-sheet approval schema before any atomic execution."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_atomic_tools_v8768b');assert not root.exists()
    receipt=derive('dk4tool/patch/hodram_B31_B53_editorial_v1.py','dk4tool/patch/hodram_B31_B53_editorial_v2.py',{
        "approval['measured_limits']['directly_viewed_sheets']":"approval['measured_limits']['directly_viewed_dialogue_andtransition_sheets']",
        "'entire verified registered V8609 stack'":"'entire verified registered V8704 stack'",
        "'directly reviewed complete scene/menu/header evidence'":"'directly reviewed complete dialogue/transition/header evidence'",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_guards_andnative_constants_preserved=True,
        exact_existing_four_sheet_approval_key_qualified_from_readonly_schema_inspection_before_any_atomic_execution=True,
        prepared_v1_preserved_not_executed_oroverwritten=True,no_atomic_configuration_ROM_orcredit_yet=True,full_goal_complete=False))
