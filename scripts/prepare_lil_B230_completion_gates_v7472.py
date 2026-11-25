"""Prepare exact final registered-release/startup/current-input gates before any credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    assert not Path('scripts/lil_B230_completion_gates_v7472.py').exists()
    derive('scripts/lil_B229_completion_gates_v7424.py','scripts/lil_B230_completion_gates_v7472.py',{'B229':'B230','release_v7419':'release_v7467','startup_v7422':'startup_v7470','registration_v7417':'registration_v7465','retention_v7420':'retention_v7468','all622_manifest_batches':'all623_manifest_batches','V7371':'V7418','v7418':'v7466',"reg['negative_count']==242":"reg['negative_count']==253", "len(manifest['batches'])==622":"len(manifest['batches'])==623","r['block']==229":"r['block']==230","for r in doc['records'])==5":"for r in doc['records'])==7",'runs_v7421':'runs_v7469','current_V7418_native_v7423':'current_V7466_native_v7471'})
