"""Source-lock the complete native-mask, header and observed-flow actual audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_actual_tools_v8576')
    assert not root.exists()
    result = derive('scripts/audit_Hodram_B50_actual_v8507.py', 'scripts/audit_Hodram_B51_actual_v8576.py', {
        'Hodram_B50_actual_v8507': 'Hodram_B51_actual_v8576',
        'Hodram_B50_fixtures_v8504': 'Hodram_B51_fixtures_v8573',
        'Hodram_B50_models_v8506': 'Hodram_B51_models_v8575',
        'Hodram_B50_scene_runs_v8505': 'Hodram_B51_scene_runs_v8574',
        'choices=[50]': 'choices=[51]',
        '{50:10001}[number]': '{51:10001}[number]',
        'full_resource_4800_layout0_hide4700_andlater_state_comparison_separate_pending': 'full_query_branch_transition_andlater_state_comparison_separate_pending',
        'progressive216x64_FE228x48_physical64_masks_not_full_scene_orfuture_simulation_proof': 'progressive216x64_masks_not_full_scene_orfuture_simulation_proof_no_B51_FE_panel',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, all_original_native_constants_coordinates_andmultiplicity_preserved=True,
        original_complete_glyph_masks_full_name_masks_observed_relative_flow_results_andend_guards_preserved=True,
        unvisited_conditional_membership_recorded_without_forcing_orrequiring_individual_gameplay_visits=True,
        no_capture_retiming_ROM_write_orcredit_by_preparer=True))
