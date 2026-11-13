"""Keep prepared completion guards intact while binding the newest independently verified ledger."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_completion_prior_v8870b');assert not root.exists()
    producer=derive('scripts/complete_Hodram_B54_B60_v8870.py','scripts/complete_Hodram_B54_B60_v8870b.py',{
      'work/analysis/Hodram_B54_B60_checkpoint_v8861/verified_handoff_v8862.json':'work/analysis/Hodram_B54_B60_checkpoint_v8874/verified_handoff_v8875.json',
      "old['unfinished_editorial_scope_v8861']":"old['unfinished_editorial_scope_v8874']",
    })
    auditor=derive('scripts/audit_Hodram_B54_B60_completion_v8871.py','scripts/audit_Hodram_B54_B60_completion_v8871b.py',{
      'complete_Hodram_B54_B60_v8870 as completion':'complete_Hodram_B54_B60_v8870b as completion',
      "old['unfinished_editorial_scope_v8861']":"old['unfinished_editorial_scope_v8874']",
    })
    root.mkdir(parents=True);save(root/'source_locked_latest_prior_binding.json',dict(producer=producer,auditor=auditor,only_latest_prior_handoff_andscope_descriptor_andmatching_auditor_import_changed=True,all_original_registered_build_patch_startup_names_direct_ROM_refs_disjoint_onceonly_counter_andfull_historical_inverse_gates_preserved=True,no_completion_stage_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
