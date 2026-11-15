"""Use the unchanged registered shared hook with the real82-record planner and late-target failure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_shared_tools_v8860');assert not root.exists()
    result=derive('scripts/validate_Hodram_B31_B53_shared_v8773.py','scripts/validate_Hodram_B54_B60_shared_v8860.py',{
        'B31_B53':'B54_B60','Hodram_B31_B53_release_paths_v8767':'Hodram_B54_B60_release_paths_v8853',
        'Hodram_B31_B53_shared_extension_v8773':'Hodram_B54_B60_shared_extension_v8860',
        'hodram_b31_b53_extension_v2':'hodram_b54_b60_extension_v1',
        'hodram_B31_B53_editorial_v2':'hodram_B54_B60_editorial_v1',
        "id='hodram-b31_b53'":"id='hodram-b54-b60'",
        "len(reports[0]['changed_records'])==3":"len(reports[0]['changed_records'])==82",
        "prior['evidence'][str(shared)]":"prior['evidence'][shared.as_posix()]",
    })
    root.mkdir(parents=True);save(root/'source_locked_shared_validation.json',dict(derivation=result,one_whole_NDS_commit_in_real_shared_adapter_path_andzero_commit_after_late_target_identity_failure_required=True,unchanged_framework_six_previous_semantic_cases_reused_only_after_exact_source_hash_match=True,no_guard_orsemantic_bypass_no_new_capture_ROM_orcredit=True,new_credit=0,full_goal_complete=False))
