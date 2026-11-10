"""Avoid an imprecise item-name shorthand in unexecuted release-profile metadata."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B234_release_note_v7610b');assert not root.exists()
    tool=derive('scripts/register_lil_B234_v7610.py','scripts/register_lil_B234_v7610b.py',{'Item106 Gregory Crown is unchanged':'Item106 is unchanged'})
    root.mkdir(parents=True);save(root/'source_locked_profile_note_clarification.json',dict(tool=tool,unexecuted_original_prepared_registration_preserved=True,no_item_name_asset_orbody_change=True,no_native_constant_orrelease_stack_change=True,new_credit=0,full_goal_complete=False))
