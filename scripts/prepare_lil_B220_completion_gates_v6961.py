"""Preflight release/patch/current-startup gates for the seventeen-object completion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B220_completion_gate_tools_v6961');assert not root.exists();root.mkdir(parents=True)
    p=derive('scripts/lil_B218_completion_gates_v6915.py','scripts/lil_B220_completion_gates_v6961.py',{'B218':'B220','release_v6911':'release_v6957','startup_v6914':'startup_v6960','registration_v6909':'registration_v6955','retention_v6912':'retention_v6958','regressions_v6910':'regressions_v6956','runs_v6913':'runs_v6959','all13_five_gates':'all17_five_gates',"len(doc['records'])==13":"len(doc['records'])==17",'all610_manifest_batches':'all611_manifest_batches','V6865':'V6910',"reg['negative_count']==18":"reg['negative_count']==21","len(manifest['batches'])==610":"len(manifest['batches'])==611","len(stage['changed_records'])==13":"len(stage['changed_records'])==17",'all13_objects13_pages':'all17_objects17_pages',"stage['actual_complete_name_holds']==51":"stage['actual_complete_name_holds']==67"})
    save(root/'source_locked_derivation.json',p)
