"""Preserve the rejected stale-profile assertion; bind completion to verified V8377 exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_completion_profile_tools_v8382c');assert not root.exists()
    d=derive('scripts/complete_Hodram_outcomes_v8382b.py','scripts/complete_Hodram_outcomes_v8382c.py',{'all-routes-unified-v8362':'all-routes-unified-v8377','v8382b':'v8382c','V8382b':'V8382c'})
    root.mkdir(parents=True);save(root/'exact_registered_profile_derivation.json',dict(derivation=d,prior_attempt_stopped_before_any_completion_staging_orcredit=True,only_exact_profile_andcheckpoint_identity_corrected=True,all_source_native_actual_release_startup_andinverse_gates_retained=True,new_credit=0,full_goal_complete=False))
