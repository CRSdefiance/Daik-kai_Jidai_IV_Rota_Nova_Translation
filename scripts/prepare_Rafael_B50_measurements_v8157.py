"""Derive B50 comparison tools without carrying forward B49 measured outcomes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_measurement_tools_v8157')
if __name__=='__main__':
    assert not ROOT.exists()
    common={
        'Rafael_B49_actual_v8107/paired_source_English_observed_path_complete_pages_names_C281_andreturn.json':'Rafael_B50_actual_v8156/paired_source_English_all28_pages_three_names_4821_departure_andreturn.json',
        'Rafael_B49_actual_comparison_v8108':'Rafael_B50_actual_comparison_v8157',
    }
    pair=derive('scripts/measure_Rafael_B49_pairs_v8108.py','scripts/measure_Rafael_B50_pairs_v8157.py',{
        **common,"frames[-1]==24001":"frames[-1]==16001",
    })
    rng=derive('scripts/measure_Rafael_B49_waits_v8109.py','scripts/measure_Rafael_B50_waits_v8158.py',{
        **common,'Rafael_B49_waits_v8109':'Rafael_B50_waits_v8158',
        'out/all_routes_combined_v8066_candidate.nds':'out/all_routes_combined_v8122_candidate.nds',
        "C281_original_command_measurement=next(r for r in rows if r['word']==0xC281)":"original_4821_A000_4720_4681_measurements=[r for r in rows if r['word'] in [0x4821,0xA000,0x4720,0x4681]]",
        'original_wait_code_measured_C281_RNG_phases_andlater_limits.json':'original_wait_code_measured_4821_departure_RNG_phases_andlater_limits.json',
        'original_single_page_waits_andC281_measured_with_identical_ordinary_inputs':'original_single_page_waits_4821_A000_4720_4681_measured_with_identical_ordinary_inputs',
        "'C281_original_command_measurement'":"'original_4821_A000_4720_4681_measurements'",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[pair,rng])
    print('Prepared B50 measured timing/RNG/components/RGB tools;all outcomes must be observed.')
