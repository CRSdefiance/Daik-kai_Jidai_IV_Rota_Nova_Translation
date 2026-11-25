"""Repair an audit-only copied dispatch key while preserving its failure and source capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_source_audit_repair_v7486b')
if __name__=='__main__':
    assert not ROOT.exists();jobs=[('scripts/audit_lil_B231_source_v7486.py','scripts/audit_lil_B231_source_v7486b.py',{'source_actual_v7486':'source_actual_v7486b','all34_source_current_dispatches':'all32_source_current_dispatches'}),('scripts/record_lil_B231_source_view_v7487.py','scripts/record_lil_B231_source_view_v7487b.py',{'source_actual_v7486':'source_actual_v7486b'})];rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_audit_reference_repair.json',dict(tools=rows,first_audit_failed_at_copied_all34_dispatch_key_before_body_proof_orapproval=True,first_audit_producer_andpartial_directory_preserved=True,completed_Japanese_capture_reused_without_rerun=True,correct_source_consumer_has32_dispatches_for16_speeches=True,no_ROM_input_runtime_dialogue_orcredit_change=True,new_credit=0,full_goal_complete=False))
