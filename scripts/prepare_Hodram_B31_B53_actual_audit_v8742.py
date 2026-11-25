"""Preserve pixel/flow guards and use the original carried-value normal-end contract."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_actual_audit_tools_v8742');assert not root.exists()
    controls=read('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
    assert controls['normal_ends192_and132_preserve_carried_values_all6words_andguards'] and controls['normal_seeded_end_cases']==50
    receipt=derive('scripts/audit_Hodram_B52_actual_v8651.py','scripts/audit_Hodram_B31_B53_actual_v8742.py',{
        'Hodram_B52_actual_v8651':'Hodram_B31_B53_actual_v8742','Hodram_B52_fixtures_v8648/two_whole_scripts.json':'Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json',
        'Hodram_B52_models_v8650':'Hodram_B31_B53_models_v8741','Hodram_B52_scene_runs_v8649':'Hodram_B31_B53_scene_runs_v8740',
        'choices=[52]':'choices=[31,53]','{52:10001}':'{31:6001,53:6001}',
        "assert row['result_words']==[0,pairs[-2]['native_result'][1]]":"assert row['result_words']==[0,entry['mode']]",
        'progressive216x64_masks_not_full_scene_orfuture_simulation_proof_no_B51_FE_panel':'progressive216x64_masks_not_full_scene_orfuture_simulation_proof_no_FE_panel',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        all_original_complete_body_name_masks_source_payload_hostslot_readonly_ABI_andflow_guards_preserved=True,
        normal_end_expected_value_is_actual_before_end_carried_mode_not_previous_kind3_zero_result_word=True,
        source_of_end_contract='work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json',
        source_of_end_contract_sha256=__import__('hashlib').sha256(Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json').read_bytes()).hexdigest(),
        older_immutable_B52_auditor_andlater_older_record_technical_reaudit_preserved=True,
        no_predicate_RNG_role_orinput_retiming_forcoverage=True,no_actual_coverage_yet_credited=True,new_credit=0,full_goal_complete=False))
