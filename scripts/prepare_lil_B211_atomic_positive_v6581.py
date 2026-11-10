"""Prepare the immutable-evidence positive reconstruction through the twelve-record atomic compiler."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_atomic_positive_tools_v6581')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/validate_lil_B210_atomic_v6534.py','scripts/validate_lil_B211_atomic_v6581.py',{'B210':'B211','atomic_v6534':'atomic_v6581','seal_lil_B210_references_v6530':'seal_lil_B211_references_v6578','lil_B210_editorial_manuscript_v4.json':'lil_B211_editorial_manuscript_v3.json','lil_B210_name_gate_reconciliation_v6531':'lil_B211_reference_approval_v6578',"==10":"==12",'positive_records=10':'positive_records=12','source688_bytes':'source640_bytes','ten-record':'twelve-record','complete688-byte':'complete640-byte'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_runner.json',dict(proof=proof,all_prior_producers_and_native_constants_preserved=True,full_goal_complete=False))
