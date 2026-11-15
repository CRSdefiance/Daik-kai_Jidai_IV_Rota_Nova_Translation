"""Preserve failed B48 audit; correct exact native FE indices instead of old binarized-plane format."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_FE_actual_tools_v8335b');assert not root.exists()
    result=derive('scripts/audit_Hodram_outcomes_actual_v8335.py','scripts/audit_Hodram_outcomes_FE_actual_v8335b.py',{
        'Hodram_outcome_actual_v8335':'Hodram_outcome_actual_v8335b','choices=[47,48]':'choices=[48]',
        "assert set(physical)<=({0,14,15} if version=='clean_Japanese' else {0,1})":"assert set(physical)<=({0,14,15} if version=='clean_Japanese' else {0,15})",
        "if v==(15 if version=='clean_Japanese' else 1)":"if v==15",
        'actual_typed_FE_descriptors_palette_andlater_native_state_comparison_separate_pending=True':'native_FE_physical_indices_preserved_not_binarized=True,actual_typed_FE_descriptors_palette_andlater_native_state_comparison_separate_pending=True',
    })
    root.mkdir(parents=True);save(root/'exact_native_FE_indices_successor_no_capture_repeated.json',dict(derivation=result,
        reason='The current source-capable native FE painter preserves index15 for original ASCII ink;the older ASCII-only factory normalized its physical plane to1. Clean CP932 retains native15 ink/14 shadow. Actual English frame3910 contains443black pixels,matching443native index15 pixels.',
        failed_original_audit_andpartial_Japanese_sheet_preserved=True,no_pixel_coverage_guard_suppressed_no_ROM_orcapture_orcontroller_change=True,
        B47_successful_audit_not_repeated=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
