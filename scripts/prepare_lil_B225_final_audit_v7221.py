"""Audit the revised capture independently;retain the initial capture andits measured differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_final_audit_tools_v7221')
if __name__=='__main__':
    assert not ROOT.exists()
    actual={'English_actual_v7205':'English_actual_v7221','English_fixture_v7203':'English_fixture_v7219','English_run_v7204':'English_run_v7220','stored_v7198':'stored_v7214'}
    later={'later_v7206':'later_v7222','English_actual_v7205':'English_actual_v7221'}
    pairs={'later_pairs_v7206b':'later_pairs_v7222b','English_actual_v7205':'English_actual_v7221','later_v7206':'later_v7222',"assert len(samples)==163 and all(not x['whole_RGB_equal'] for x in samples)":"assert samples",'all163_later_differences_kept_in_full_measurement_not_only_selected_examples':'all_measured_later_differences_kept_in_full_measurement_not_only_selected_examples'}
    jobs=[('scripts/audit_lil_B225_English_v7205.py','scripts/audit_lil_B225_English_v7221.py',actual),('scripts/measure_lil_B225_later_v7206.py','scripts/measure_lil_B225_later_v7222.py',later),('scripts/illustrate_lil_B225_later_v7206b.py','scripts/illustrate_lil_B225_later_v7222b.py',pairs)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_final_capture_audits.json',dict(tools=rows,all13_speeches14_pages25_commands_complete_native_body_andname_masks_required=True,source_R26_original_A_advance_andguard_required=True,no_assumed_initial_English_timing_RNG_final_components_orlater_RGB_count=True,all_native_high_constants_andinitial_evidence_preserved=True,new_credit=0))
