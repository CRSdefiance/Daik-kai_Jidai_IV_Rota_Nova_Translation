"""Preserve the caught predecessor label guard and bind the exact20-object seal key."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_atomic_tools_v6150b')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/patch/lil_B204_editorial_v1.py','dk4tool/patch/lil_B204_editorial_v2.py',{'all22_source_native_reference_and_representative_rules_approved':'all20_source_native_reference_and_representative_rules_approved'})]
    tools.append(derive('scripts/validate_lil_B204_atomic_v6150.py','scripts/validate_lil_B204_atomic_v6150b.py',{'lil_B204_editorial_v1':'lil_B204_editorial_v2',"ROOT=Path('work/analysis/lil_B204_atomic_v6150')":"ROOT=Path('work/analysis/lil_B204_atomic_v6150b')"}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_successor.json',dict(tools=tools,caught_predecessor22_object_seal_label_before_any_image_mutation_preserved=True,no_native_addresses_prose_source_map_or_safety_checks_changed=True,full_goal_complete=False));print('Correct20-object seal-key successor prepared;failed producer/config preserved;no native or prose change.')
