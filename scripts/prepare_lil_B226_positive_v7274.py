"""Preserve B225 validation and derive the exact twenty-speech successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_positive_tools_v7274')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/validate_lil_B225_atomic_v7227.py','scripts/validate_lil_B226_atomic_v7274.py',{
        'B225':'B226','lil_B225_final_paths_v7223':'lil_B226_final_paths_v7267','lil_B225_atomic_v7227':'lil_B226_atomic_v7274','seal_lil_B225_references_v7225':'seal_lil_B226_references_v7269','lil_B225_atomic_tools_v7226':'lil_B226_atomic_tools_v7273','prepare_lil_B225_atomic_v7226':'prepare_lil_B226_atomic_v7273',
        "len(proof['changed_records'])==13":"len(proof['changed_records'])==20",'positive_records=13':'positive_records=20','source976_bytes_inverse_including_tail2_recovered':'source1196_bytes_inverse_including_tail2_recovered','all13_actual14_pages55_body55_headers_bound':'all20_actual20_pages79_body79_headers_bound','13 speeches/14 pages,complete976-byte':'20 speeches/20 pages,complete1196-byte'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validator.json',r)
