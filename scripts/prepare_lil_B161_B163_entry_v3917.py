"""Derive original EV2 event/action/dependency getter bindings without natural-eligibility claims."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    ROOT=Path('work/analysis/lil_B161_B163_entry_tools_v3917');assert not ROOT.exists();row=derive('scripts/prove_lil_B142_B145_entry_v3575.py','scripts/prove_lil_B161_B163_entry_v3917.py',{'lil_B142_B145_entry_v3575':'lil_B161_B163_entry_v3917','lil_B142_B145_source_v3571/all38_clean_current_complete_context':'lil_B161_B163_source_v3912/all45_clean_current_complete_context','[142,143,144,145]':'[161,162,163]','len(chosen)==4':'len(chosen)==3','lil_B142_B145_voices_v3572':'lil_B161_B163_voices_v3914','B142_B145':'B161_B163','historical_snapshot_is_Lil_opening_not_current':'historical_snapshot_is_Lil_London_not_current'});ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=row,original_EV2_action_dependency_native_getter_scope_only=True,no_source_location_elapsed_search_time_current_eligibility_earned_recovery_or_recruitment_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
