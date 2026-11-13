"""Freeze read-only later-state measurements; preserve every measured difference."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_later_tools_v7061')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/measure_lil_B220_later_v6949.py','scripts/measure_lil_B222_later_v7061.py',{'B220':'B222','later_v6949':'later_v7061','English_actual_v6948/all17_English_speeches_complete_native_masks29_commands_C200_source_comparison':'English_actual_v7060/all16_English_speeches_complete_native_masks27_commands_source_comparison','aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_later_measurements.json',dict(tool=tool,no_native_addresses_changed=True,no_new_emulator_or_state_mutation=True,new_credit=0,full_goal_complete=False))
