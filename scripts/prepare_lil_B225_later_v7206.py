"""Measure the observed final components without changing timing,RNG orcaptain assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_later_tools_v7206')
if __name__=='__main__':
    assert not ROOT.exists();target='scripts/measure_lil_B225_later_v7206.py';assert not Path(target).exists()
    row=derive('scripts/measure_lil_B224_later_v7158.py',target,{'B224':'B225','later_v7158':'later_v7206','English_actual_v7157/all15_English_speeches_complete_native_masks27_commands_C200_source_comparison':'English_actual_v7205/all13_English_speeches14_pages_complete_native_masks25_commands_630B_source_comparison'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_final_measurements.json',dict(tool=row,all_original_native_getters_and_high_constants_preserved=True,actual_captains_all0_to3_andunequal_final_components_allowed_for_measurement=True,no_replay_retiming_RNG_forcing_orwhole_simulation_equivalence=True,new_credit=0))
